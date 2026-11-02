"""
Testes de aceitação do star schema — replicam o gabarito do ADR-001.

Constroem o star a partir das planilhas reais em ./data para um DuckDB temporário
e verificam o DB materializado (não a memória): âncora, contagens, taxonomia
fechada, universos de contrato, dedup e não-aditividade da exposição.

Rodar:  pytest -q
"""
from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from star import config as cfg
from star import ingest, load, queries, transform, validate

RAIZ = Path(__file__).resolve().parents[1]
SOURCES = RAIZ / "data"


@pytest.fixture(scope="session")
def db(tmp_path_factory) -> Path:
    gar = ingest.ler_garantias(SOURCES)
    pg = ingest.ler_pgtos(SOURCES)
    validate.validar(gar, pg, estrito=True)  # levanta se algum teste duro falhar
    data_base = cfg.data_base_do_arquivo(gar.caminho)
    star = transform.construir(gar, pg, data_base)
    destino = tmp_path_factory.mktemp("build") / "gapd_star.duckdb"
    return load.gravar_duckdb(star, destino)


@pytest.fixture(scope="session")
def con(db):
    c = duckdb.connect(str(db), read_only=True)
    yield c
    c.close()


# --- Validação passa sem falhas duras -------------------------------------
def test_validacao_aprovada():
    gar = ingest.ler_garantias(SOURCES)
    pg = ingest.ler_pgtos(SOURCES)
    rel = validate.validar(gar, pg, estrito=False)
    assert rel.aprovado, rel.render()


# --- Âncora ----------------------------------------------------------------
def test_ancora_saldo(con):
    soma = con.execute("SELECT SUM(saldo_devedor) FROM fato_saldo").fetchone()[0]
    assert abs(soma - cfg.ANCORA_SALDO) <= cfg.ANCORA_TOL


def test_fato_saldo_dedup_por_contrato(con):
    total, distintos = con.execute(
        "SELECT COUNT(*), COUNT(DISTINCT contrato) FROM fato_saldo"
    ).fetchone()
    assert total == distintos == cfg.N_CONTRATOS_VIVOS


# --- Contagens de referência ----------------------------------------------
@pytest.mark.parametrize(
    "tabela,esperado",
    [
        ("fato_saldo", cfg.N_CONTRATOS_VIVOS),
        ("ponte_contrato_garantia", cfg.N_LINHAS_GARANTIA),
        ("fato_pagamento", cfg.N_PAGAMENTO),
        ("fato_liberacao", cfg.N_LIBERACAO),
    ],
)
def test_contagens(con, tabela, esperado):
    n = con.execute(f'SELECT COUNT(*) FROM "{tabela}"').fetchone()[0]
    assert n == esperado


# --- Taxonomia fechada -----------------------------------------------------
def test_taxonomia_fechada(con):
    tipos = {r[0] for r in con.execute("SELECT DISTINCT tipo_garantia FROM ponte_contrato_garantia").fetchall()}
    classes = {r[0] for r in con.execute("SELECT DISTINCT classe FROM ponte_contrato_garantia").fetchall()}
    assert tipos <= cfg.TIPOS_GARANTIA_VALIDOS
    assert classes <= cfg.CLASSES_VALIDAS


def test_rotulos_dentro_da_enumeracao(con):
    rotulos = {r[0] for r in con.execute("SELECT DISTINCT garantia_rotulo FROM ponte_contrato_garantia").fetchall()}
    assert rotulos <= set(cfg.TAXONOMIA_GARANTIA)


# --- Universos de contrato -------------------------------------------------
def test_universos_contrato(con):
    vivos = con.execute("SELECT COUNT(*) FROM dim_contrato WHERE is_vivo").fetchone()[0]
    total = con.execute("SELECT COUNT(*) FROM dim_contrato").fetchone()[0]
    assert vivos == cfg.N_CONTRATOS_VIVOS
    # união = vivos(31) + só-liquidados(109) = 140
    assert total == cfg.N_CONTRATOS_VIVOS + (cfg.N_PGTOS_CONTRATOS - cfg.N_INTERSECAO_CONTRATOS)


# --- Não-aditividade da exposição -----------------------------------------
def test_exposicao_nao_aditiva(db):
    todas = queries.exposicao_por_garantidor(db)
    soma_ingenua = todas["exposicao"].sum()
    # somar entre garantidores dupla-conta o aval cruzado: excede a âncora
    assert soma_ingenua > cfg.ANCORA_SALDO
    # nenhum garantidor isolado excede a âncora
    assert todas["exposicao"].max() <= cfg.ANCORA_SALDO + cfg.ANCORA_TOL


def test_exposicao_por_contratos_distintos(db):
    pf = queries.exposicao_por_garantidor(db, classe="PF")
    # cada exposição PF é soma de contratos distintos -> ≤ âncora
    assert (pf["exposicao"] <= cfg.ANCORA_SALDO + cfg.ANCORA_TOL).all()
    assert set(pf["garantidor"]) == {"Ana", "Arthur", "Marcelo"}


# --- Medida canônica nan-safe (parcela só-juros) --------------------------
def test_pagamento_nansafe_juros(con):
    # linhas só-juros: principal NULL, juros preenchido -> pagamento == juros
    r = con.execute(
        """
        SELECT COUNT(*) FROM fato_pagamento
        WHERE principal IS NULL AND juros IS NOT NULL
          AND ABS(pagamento - juros) > 0.005
        """
    ).fetchone()[0]
    assert r == 0


def test_pagamento_soma_principal_juros(con):
    r = con.execute(
        """
        SELECT COUNT(*) FROM fato_pagamento
        WHERE ABS(pagamento - (COALESCE(principal,0) + COALESCE(juros,0))) > 0.005
        """
    ).fetchone()[0]
    assert r == 0


# --- Perfil de vencimentos concilia com a âncora --------------------------
def test_perfil_vencimentos_concilia(db):
    perfil = queries.perfil_vencimentos(db)
    assert abs(perfil["saldo"].sum() - cfg.ANCORA_SALDO) <= cfg.ANCORA_TOL


# --- Garantia contra rótulo fora da taxonomia -----------------------------
def test_rotulo_desconhecido_falha(tmp_path):
    """Rótulo fora da enumeração deve derrubar a validação (estrito)."""
    import pandas as pd

    gar = ingest.ler_garantias(SOURCES)
    gar.df.loc[0, cfg.ColGarantias.GARANTIA] = "Garantia Inexistente XPTO"
    pg = ingest.ler_pgtos(SOURCES)
    with pytest.raises(validate.ErroIngestao):
        validate.validar(gar, pg, estrito=True)
