"""
Transformação: fontes normalizadas -> tabelas do star schema.

Emite 3 fatos, 4 dimensões conformadas e 1 ponte M:N, conforme o ADR. Toda a
não-aditividade da exposição por garantidor é carregada na ponte, propriedade
estrutural do modelo — não nota de rodapé.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd

from . import config as cfg
from .ingest import FonteGarantias, FontePgtos


@dataclass
class Star:
    fato_saldo: pd.DataFrame
    fato_pagamento: pd.DataFrame
    fato_liberacao: pd.DataFrame
    dim_contrato: pd.DataFrame
    dim_banco: pd.DataFrame
    dim_garantidor: pd.DataFrame
    dim_tipo_garantia: pd.DataFrame
    dim_tempo: pd.DataFrame
    ponte_contrato_garantia: pd.DataFrame

    def tabelas(self) -> dict[str, pd.DataFrame]:
        return {
            "fato_saldo": self.fato_saldo,
            "fato_pagamento": self.fato_pagamento,
            "fato_liberacao": self.fato_liberacao,
            "dim_contrato": self.dim_contrato,
            "dim_banco": self.dim_banco,
            "dim_garantidor": self.dim_garantidor,
            "dim_tipo_garantia": self.dim_tipo_garantia,
            "dim_tempo": self.dim_tempo,
            "ponte_contrato_garantia": self.ponte_contrato_garantia,
        }


def construir(gar: FonteGarantias, pg: FontePgtos, data_base: date) -> Star:
    g = gar.df
    p = pg.df

    fato_saldo = _fato_saldo(g, data_base)
    fato_pagamento = _fato_pagamento(p)
    fato_liberacao = _fato_liberacao(p)
    ponte = _ponte(g)

    dim_contrato = _dim_contrato(g, p)
    dim_banco = _dim_banco(g, p)
    dim_garantidor = _dim_garantidor(ponte)
    dim_tipo_garantia = _dim_tipo_garantia(ponte)
    dim_tempo = _dim_tempo(fato_saldo, fato_pagamento, fato_liberacao, dim_contrato)

    return Star(
        fato_saldo=fato_saldo,
        fato_pagamento=fato_pagamento,
        fato_liberacao=fato_liberacao,
        dim_contrato=dim_contrato,
        dim_banco=dim_banco,
        dim_garantidor=dim_garantidor,
        dim_tipo_garantia=dim_tipo_garantia,
        dim_tempo=dim_tempo,
        ponte_contrato_garantia=ponte,
    )


# --------------------------------------------------------------------------- #
# Fatos
# --------------------------------------------------------------------------- #
def _fato_saldo(g: pd.DataFrame, data_base: date) -> pd.DataFrame:
    """1 linha por Contrato × Data-base. Dedup por contrato ANTES de qualquer soma."""
    dedup = g.dropna(subset=["contrato"]).drop_duplicates(subset=["contrato"]).copy()
    out = pd.DataFrame(
        {
            "contrato": dedup["contrato"].values,
            "data_base": pd.Timestamp(data_base),
            "saldo_devedor": dedup[cfg.ColGarantias.PRINCIPAL].astype(float).values,
        }
    )
    return out.sort_values("contrato").reset_index(drop=True)


def _fato_pagamento(p: pd.DataFrame) -> pd.DataFrame:
    """1 linha por Contrato × Parcela × Data (predicado: Parcela N# preenchida).

    Medida canônica: pagamento = principal + juros, com semântica nan-safe
    (parcela só-juros -> pagamento = juros). `Valor Total da Parcela` é ignorada.
    """
    pay = p[p["_e_pagamento"]].copy()
    principal = pd.to_numeric(pay[cfg.ColPgtos.VALOR_PARCELA], errors="coerce")
    juros = pd.to_numeric(pay[cfg.ColPgtos.JUROS], errors="coerce")
    pagamento = np.nansum(np.vstack([principal.values, juros.values]), axis=0)

    out = pd.DataFrame(
        {
            "contrato": pay["contrato"].values,
            "parcela": pay[cfg.ColPgtos.PARCELA].astype(str).values,
            "data": pd.to_datetime(pay[cfg.ColPgtos.DATA]).values,
            "principal": principal.values,     # NaN preservado
            "juros": juros.values,             # NaN preservado
            "pagamento": pagamento,            # medida canônica nan-safe
        }
    )
    return out.reset_index(drop=True)


def _fato_liberacao(p: pd.DataFrame) -> pd.DataFrame:
    """1 linha por Contrato × Data de desembolso (predicado: Valor liberado preenchido).

    data_desembolso reusa a coluna física `Data Pagto da Parcela N#`.
    """
    lib = p[p["_e_liberacao"]].copy()
    out = pd.DataFrame(
        {
            "contrato": lib["contrato"].values,
            "data_desembolso": pd.to_datetime(lib[cfg.ColPgtos.DATA]).values,
            "valor_liberado": pd.to_numeric(lib[cfg.ColPgtos.VALOR_LIBERADO], errors="coerce").values,
        }
    )
    return out.reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Ponte (coração da decisão)
# --------------------------------------------------------------------------- #
def _ponte(g: pd.DataFrame) -> pd.DataFrame:
    """M:N garantidor↔contrato. 1 linha por (Contrato × Garantia) = 124.

    tipo e garantidor derivam do parse da coluna composta `Garantia`.
    """
    linhas = []
    for _, row in g.dropna(subset=["contrato"]).iterrows():
        rotulo = row[cfg.ColGarantias.GARANTIA]
        if pd.isna(rotulo):
            continue
        tipo, garantidor, classe = cfg.TAXONOMIA_GARANTIA[rotulo]  # KeyError impossível pós-validação
        linhas.append(
            {
                "contrato": row["contrato"],
                "garantia_rotulo": rotulo,
                "tipo_garantia": tipo,
                "garantidor": garantidor,
                "classe": classe,
            }
        )
    return pd.DataFrame(linhas).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Dimensões conformadas
# --------------------------------------------------------------------------- #
def _dim_contrato(g: pd.DataFrame, p: pd.DataFrame) -> pd.DataFrame:
    """União de contratos (GARANTIAS ∪ PGTOS), com atributos conformados.

    GARANTIAS é autoritativa para os vivos (banco/emitente por extenso,
    vencimento). PGTOS fornece banco/emitente conformados para os liquidados.
    """
    vivos = set(g["contrato"].dropna())
    universo = sorted(vivos | set(p["contrato"].dropna()))

    # banco por contrato — GARANTIAS prioritária, senão modal do PGTOS
    g_banco = (
        g.dropna(subset=["contrato"])
        .assign(banco=g[cfg.ColGarantias.BANCO].map(cfg.conformar_banco))
        .groupby("contrato")["banco"].agg(lambda s: s.mode().iat[0])
    )
    p_banco = (
        p.dropna(subset=["contrato"])
        .assign(banco=p[cfg.ColPgtos.BANCO].map(cfg.conformar_banco))
        .groupby("contrato")["banco"].agg(lambda s: s.mode().iat[0])
    )
    # emitente conformado — GARANTIAS prioritária
    g_emit = (
        g.dropna(subset=["contrato"])
        .assign(emit=g[cfg.ColGarantias.EMITENTE].map(cfg.conformar_emitente))
        .groupby("contrato")["emit"].agg(lambda s: s.mode().iat[0])
    )
    p_emit = (
        p.dropna(subset=["contrato"])
        .assign(emit=p[cfg.ColPgtos.EMITENTE].map(cfg.conformar_emitente))
        .groupby("contrato")["emit"].agg(lambda s: s.mode().iat[0])
    )
    g_venc = (
        g.dropna(subset=["contrato"])
        .groupby("contrato")[cfg.ColGarantias.VENCIMENTO].max()
    )

    registros = []
    for c in universo:
        registros.append(
            {
                "contrato": c,
                "banco": g_banco.get(c, p_banco.get(c)),
                "emitente": g_emit.get(c, p_emit.get(c)),
                "data_vencimento": g_venc.get(c, pd.NaT),
                "is_vivo": c in vivos,
            }
        )
    out = pd.DataFrame(registros)
    out["data_vencimento"] = pd.to_datetime(out["data_vencimento"])
    return out.sort_values("contrato").reset_index(drop=True)


def _dim_banco(g: pd.DataFrame, p: pd.DataFrame) -> pd.DataFrame:
    brutos = set(g[cfg.ColGarantias.BANCO].dropna().map(str.strip)) | set(
        p[cfg.ColPgtos.BANCO].dropna().map(str.strip)
    )
    linhas = []
    conformados: dict[str, list[str]] = {}
    for b in brutos:
        canon = cfg.conformar_banco(b)
        conformados.setdefault(canon, [])
        if b != canon:
            conformados[canon].append(b)
    for canon in sorted(conformados):
        linhas.append({"banco": canon, "aliases": ", ".join(sorted(conformados[canon])) or "—"})
    return pd.DataFrame(linhas).reset_index(drop=True)


def _dim_garantidor(ponte: pd.DataFrame) -> pd.DataFrame:
    out = (
        ponte[["garantidor", "classe"]]
        .drop_duplicates()
        .sort_values(["classe", "garantidor"])
        .reset_index(drop=True)
    )
    return out


def _dim_tipo_garantia(ponte: pd.DataFrame) -> pd.DataFrame:
    return (
        ponte[["tipo_garantia"]]
        .drop_duplicates()
        .sort_values("tipo_garantia")
        .reset_index(drop=True)
    )


def _dim_tempo(
    fato_saldo: pd.DataFrame,
    fato_pagamento: pd.DataFrame,
    fato_liberacao: pd.DataFrame,
    dim_contrato: pd.DataFrame,
) -> pd.DataFrame:
    """Dimensão de tempo enxuta: datas distintas efetivamente presentes.

    Origem: vencimentos (dim_contrato), pagamentos e desembolsos (fatos).
    """
    datas = pd.concat(
        [
            pd.to_datetime(fato_pagamento["data"], errors="coerce"),
            pd.to_datetime(fato_liberacao["data_desembolso"], errors="coerce"),
            pd.to_datetime(dim_contrato["data_vencimento"], errors="coerce"),
        ]
    ).dropna().dt.normalize().drop_duplicates().sort_values()

    out = pd.DataFrame({"data": datas.values})
    dt = pd.to_datetime(out["data"])
    out["ano"] = dt.dt.year
    out["mes"] = dt.dt.month
    out["ano_mes"] = dt.dt.strftime("%Y-%m")
    out["trimestre"] = dt.dt.quarter
    return out.reset_index(drop=True)
