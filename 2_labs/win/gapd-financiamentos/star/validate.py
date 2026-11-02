"""
Validação: a porta de entrada como contrato de qualidade.

Separa falhas duras (recusam o build) de achados brandos (avisos registrados,
build prossegue). Falhas duras replicam os testes de aceitação do ADR: rótulo de
garantia fora da taxonomia, âncora de saldo divergente, contagens de referência
divergentes. Achados brandos: colunas fantasma, células fora do esquema, linhas
órfãs, conflitos de banco por contrato.

`garbage-in` é mitigado, não eliminado — mas passa a esbarrar em validação
explícita, nunca em divergência silenciosa que só aparece no Conselho.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pandas as pd

from . import config as cfg
from .ingest import FonteGarantias, FontePgtos


class Nivel(str, Enum):
    OK = "OK"
    AVISO = "AVISO"
    FALHA = "FALHA"


@dataclass
class Achado:
    nivel: Nivel
    verificacao: str
    detalhe: str


@dataclass
class RelatorioValidacao:
    achados: list[Achado] = field(default_factory=list)

    def add(self, nivel: Nivel, verificacao: str, detalhe: str = "") -> None:
        self.achados.append(Achado(nivel, verificacao, detalhe))

    @property
    def falhas(self) -> list[Achado]:
        return [a for a in self.achados if a.nivel is Nivel.FALHA]

    @property
    def avisos(self) -> list[Achado]:
        return [a for a in self.achados if a.nivel is Nivel.AVISO]

    @property
    def aprovado(self) -> bool:
        return not self.falhas

    def render(self) -> str:
        simbolo = {Nivel.OK: "  ok ", Nivel.AVISO: "AVISO", Nivel.FALHA: "FALHA"}
        linhas = ["Relatório de validação da ingestão", "=" * 72]
        for a in self.achados:
            linhas.append(f"[{simbolo[a.nivel]}] {a.verificacao}")
            if a.detalhe:
                linhas.append(f"         {a.detalhe}")
        linhas.append("=" * 72)
        veredito = "APROVADO" if self.aprovado else "REPROVADO"
        linhas.append(f"Veredito: {veredito}  ({len(self.falhas)} falha(s), {len(self.avisos)} aviso(s))")
        return "\n".join(linhas)


class ErroIngestao(Exception):
    """Ingestão recusada: um ou mais testes de aceitação duros falharam."""


def validar(gar: FonteGarantias, pg: FontePgtos, estrito: bool = True) -> RelatorioValidacao:
    r = RelatorioValidacao()
    g = gar.df
    p = pg.df

    # --- 1. Esquema presente -------------------------------------------------
    if gar.diagnostico["colunas_faltando"]:
        r.add(Nivel.FALHA, "GARANTIAS: colunas obrigatórias", str(gar.diagnostico["colunas_faltando"]))
    else:
        r.add(Nivel.OK, "GARANTIAS: colunas obrigatórias presentes")
    if pg.diagnostico["colunas_faltando"]:
        r.add(Nivel.FALHA, "PGTOS: colunas obrigatórias", str(pg.diagnostico["colunas_faltando"]))
    else:
        r.add(Nivel.OK, "PGTOS: colunas obrigatórias presentes")

    # --- 2. Taxonomia de garantia (enumeração fechada) -----------------------
    rotulos = g[cfg.ColGarantias.GARANTIA].dropna().unique().tolist()
    fora = sorted(set(rotulos) - set(cfg.TAXONOMIA_GARANTIA))
    if fora:
        r.add(Nivel.FALHA, "Taxonomia: rótulos fora da enumeração", f"{fora} — corrigir fonte ou taxonomia")
    else:
        r.add(Nivel.OK, f"Taxonomia: {len(rotulos)} rótulos, todos na enumeração de {cfg.N_ROTULOS_GARANTIA}")

    # --- 3. Âncora de saldo (dedup por contrato) -----------------------------
    dedup = g.drop_duplicates(subset=["contrato"])
    soma = float(dedup[cfg.ColGarantias.PRINCIPAL].sum())
    if abs(soma - cfg.ANCORA_SALDO) <= cfg.ANCORA_TOL:
        r.add(Nivel.OK, "Âncora Σ saldo_devedor (dedup)", f"R$ {soma:,.2f}")
    else:
        r.add(Nivel.FALHA, "Âncora Σ saldo_devedor (dedup)",
              f"obtido R$ {soma:,.2f} ≠ esperado R$ {cfg.ANCORA_SALDO:,.2f}")

    # --- 4. Contagens de referência ------------------------------------------
    def _cont(nome, obtido, esperado):
        nivel = Nivel.OK if obtido == esperado else Nivel.FALHA
        r.add(nivel, f"Contagem: {nome}", f"obtido {obtido} / esperado {esperado}")

    n_contratos = dedup["contrato"].nunique()
    _cont("contratos vivos (GARANTIAS)", n_contratos, cfg.N_CONTRATOS_VIVOS)
    _cont("linhas de garantia", len(g), cfg.N_LINHAS_GARANTIA)
    _cont("linhas PGTOS", len(p), cfg.N_PGTOS)
    _cont("linhas de pagamento (Parcela N#)", int(p["_e_pagamento"].sum()), cfg.N_PAGAMENTO)
    _cont("linhas de liberação (Valor liberado)", int(p["_e_liberacao"].sum()), cfg.N_LIBERACAO)

    pgtos_contratos = p["contrato"].dropna().nunique()
    _cont("contratos distintos (PGTOS)", pgtos_contratos, cfg.N_PGTOS_CONTRATOS)
    intersec = len(set(g["contrato"].dropna()) & set(p["contrato"].dropna()))
    _cont("interseção de contratos", intersec, cfg.N_INTERSECAO_CONTRATOS)

    # --- 5. Achados brandos (avisos) -----------------------------------------
    for c in pg.diagnostico["celulas_fora_esquema"]:
        r.add(Nivel.AVISO, "PGTOS: célula fora do esquema (coluna fantasma)",
              f"linha {c['linha_excel']}, {c['coluna']} = {c['valor']}")
    if pg.diagnostico["colunas_fantasma"]:
        r.add(Nivel.AVISO, "PGTOS: colunas fantasma descartadas", str(pg.diagnostico["colunas_fantasma"]))
    for o in pg.diagnostico["linhas_orfas"]:
        r.add(Nivel.AVISO, "PGTOS: linha com valor sem predicado (excluída dos fatos)",
              f"linha {o['linha_excel']} · {o['banco']} · contrato {o['contrato']} · "
              f"parcela=R$ {o['valor_parcela']} juros=R$ {o['juros']}")
    if pg.diagnostico["linhas_vazias"]:
        r.add(Nivel.AVISO, "PGTOS: linhas inteiramente vazias (descartadas)",
              f"linhas Excel {pg.diagnostico['linhas_vazias']}")

    # Conflito de banco por contrato (após conformação) na interseção
    conflitos = _conflitos_banco(g, p)
    if conflitos:
        r.add(Nivel.AVISO, "Banco divergente por contrato entre fontes", str(conflitos))
    else:
        r.add(Nivel.OK, "Banco conforme entre fontes (interseção)")

    if estrito and not r.aprovado:
        raise ErroIngestao(
            "Ingestão recusada — testes de aceitação duros falharam:\n" + r.render()
        )
    return r


def _conflitos_banco(g: pd.DataFrame, p: pd.DataFrame) -> list[dict]:
    gb = (
        g.dropna(subset=["contrato"])
        .assign(banco=g[cfg.ColGarantias.BANCO].map(cfg.conformar_banco))
        .groupby("contrato")["banco"].agg(lambda s: sorted(set(s)))
    )
    pb = (
        p.dropna(subset=["contrato"])
        .assign(banco=p[cfg.ColPgtos.BANCO].map(cfg.conformar_banco))
        .groupby("contrato")["banco"].agg(lambda s: sorted(set(s)))
    )
    conflitos = []
    for contrato in gb.index.intersection(pb.index):
        bg, bp = set(gb[contrato]), set(pb[contrato])
        if bg and bp and not (bg & bp):
            conflitos.append({"contrato": contrato, "garantias": sorted(bg), "pgtos": sorted(bp)})
    return conflitos
