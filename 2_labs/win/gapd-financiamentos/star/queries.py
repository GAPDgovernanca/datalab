"""
Consultas canônicas do Conselho sobre o star (DuckDB).

As três perguntas típicas do ADR: exposição por garantidor (não-aditiva),
perfil de vencimentos, quitado/a quitar por janela. Servem de protótipo de
validação do modelo e de biblioteca reutilizável pelas skills mensais.
"""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def _con(db: str | Path) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(db), read_only=True)


def exposicao_por_garantidor(db: str | Path, classe: str | None = None) -> pd.DataFrame:
    """Exposição = Σ saldo_devedor dos CONTRATOS DISTINTOS cobertos pelo garantidor.

    Não-aditiva por construção: somar entre garantidores dupla-conta o aval
    cruzado. O DISTINCT no par (garantidor, contrato) evita dupla-contagem de um
    mesmo contrato coberto por múltiplas linhas de garantia do mesmo garantidor.
    """
    filtro = f"WHERE pg.classe = '{classe}'" if classe else ""
    sql = f"""
    WITH cobertura AS (
        SELECT DISTINCT pg.garantidor, pg.classe, pg.contrato
        FROM ponte_contrato_garantia pg
        {filtro}
    )
    SELECT c.classe,
           c.garantidor,
           COUNT(DISTINCT c.contrato)        AS contratos,
           SUM(fs.saldo_devedor)             AS exposicao
    FROM cobertura c
    JOIN fato_saldo fs USING (contrato)
    GROUP BY c.classe, c.garantidor
    ORDER BY exposicao DESC;
    """
    with _con(db) as con:
        return con.execute(sql).df()


def perfil_vencimentos(db: str | Path) -> pd.DataFrame:
    """Saldo dos contratos vivos por janela de vencimento relativa à data-base."""
    sql = """
    WITH base AS (SELECT MAX(data_base) AS data_base FROM fato_saldo)
    SELECT
        CASE
            WHEN dc.data_vencimento IS NULL THEN '9. sem vencimento'
            WHEN dc.data_vencimento <= b.data_base + INTERVAL 12 MONTH THEN '1. ate 12m'
            WHEN dc.data_vencimento <= b.data_base + INTERVAL 24 MONTH THEN '2. 12-24m'
            WHEN dc.data_vencimento <= b.data_base + INTERVAL 36 MONTH THEN '3. 24-36m'
            ELSE '4. acima 36m'
        END                              AS janela,
        COUNT(*)                         AS contratos,
        SUM(fs.saldo_devedor)            AS saldo
    FROM fato_saldo fs
    JOIN dim_contrato dc USING (contrato)
    CROSS JOIN base b
    GROUP BY janela
    ORDER BY janela;
    """
    with _con(db) as con:
        return con.execute(sql).df()


def quitado_e_a_quitar(db: str | Path) -> pd.DataFrame:
    """Quitado (data ≤ data-base) × a quitar/vincendo por janela.

    A janela vincenda ≤ 12m alimenta diretamente o índice de Conselho
    "principal vincendo em 12 meses".
    """
    sql = """
    WITH base AS (SELECT MAX(data_base) AS data_base FROM fato_saldo)
    SELECT
        CASE
            WHEN fp.data <= b.data_base THEN '0. quitado'
            WHEN fp.data <= b.data_base + INTERVAL 12 MONTH THEN '1. vincendo ate 12m'
            WHEN fp.data <= b.data_base + INTERVAL 24 MONTH THEN '2. vincendo 12-24m'
            ELSE '3. vincendo acima 24m'
        END                     AS situacao,
        COUNT(*)                AS parcelas,
        SUM(fp.principal)       AS principal,
        SUM(fp.juros)           AS juros,
        SUM(fp.pagamento)       AS pagamento
    FROM fato_pagamento fp
    CROSS JOIN base b
    WHERE fp.data IS NOT NULL
    GROUP BY situacao
    ORDER BY situacao;
    """
    with _con(db) as con:
        return con.execute(sql).df()


def reconciliacao(db: str | Path) -> pd.DataFrame:
    """Placar de reconciliação: âncora, contagens e não-aditividade."""
    with _con(db) as con:
        ancora = con.execute("SELECT SUM(saldo_devedor) FROM fato_saldo").fetchone()[0]
        n_contr = con.execute("SELECT COUNT(*) FROM fato_saldo").fetchone()[0]
        n_ponte = con.execute("SELECT COUNT(*) FROM ponte_contrato_garantia").fetchone()[0]
        n_pag = con.execute("SELECT COUNT(*) FROM fato_pagamento").fetchone()[0]
        n_lib = con.execute("SELECT COUNT(*) FROM fato_liberacao").fetchone()[0]
        soma_ingenua = con.execute(
            """
            WITH e AS (
                SELECT DISTINCT garantidor, contrato FROM ponte_contrato_garantia
            )
            SELECT SUM(fs.saldo_devedor)
            FROM e JOIN fato_saldo fs USING (contrato)
            """
        ).fetchone()[0]
    return pd.DataFrame(
        [
            {"metrica": "ancora_saldo (fato_saldo)", "valor": ancora},
            {"metrica": "contratos (fato_saldo)", "valor": n_contr},
            {"metrica": "linhas ponte", "valor": n_ponte},
            {"metrica": "linhas fato_pagamento", "valor": n_pag},
            {"metrica": "linhas fato_liberacao", "valor": n_lib},
            {"metrica": "soma exposicao (todos garantidores) — NAO ADITIVA", "valor": soma_ingenua},
        ]
    )
