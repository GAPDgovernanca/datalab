"""
Ingestão: fonte -> DataFrame normalizado + diagnóstico bruto.

Responsabilidade única: ler as duas planilhas, aparar cabeçalhos, normalizar a
chave `contrato` para texto e devolver estruturas limpas + um dicionário de
diagnósticos brutos (colunas fantasma, células fora do esquema, linhas órfãs)
para a validação decidir o que é falha e o que é aviso. Nenhuma regra de negócio
aqui — só higiene e detecção.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from . import config as cfg


def normalizar_contrato(valor) -> str | None:
    """int64 (GARANTIAS) e object misto (PGTOS) -> texto canônico.

    Remove `.0` de floats e espaços. Devolve None para vazio — única junção
    robusta entre fontes exige tipo idêntico dos dois lados.
    """
    if pd.isna(valor):
        return None
    s = str(valor).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s or None


def _canon(texto: str) -> str:
    """Normaliza para casamento tolerante: underscores/espaços/caixa."""
    return " ".join(str(texto).replace("_", " ").split()).upper()


def _localizar(fontes: Path, padrao: str) -> Path:
    alvo = _canon(padrao)
    achados = sorted(p for p in Path(fontes).glob("*.xlsx") if alvo in _canon(p.name))
    if not achados:
        raise FileNotFoundError(f"Nenhuma planilha casando {padrao!r} em {fontes}")
    if len(achados) > 1:
        raise ValueError(f"Múltiplas planilhas casando {padrao!r}: {[a.name for a in achados]}")
    return achados[0]


@dataclass
class FonteGarantias:
    df: pd.DataFrame
    caminho: Path
    diagnostico: dict = field(default_factory=dict)


@dataclass
class FontePgtos:
    df: pd.DataFrame
    caminho: Path
    diagnostico: dict = field(default_factory=dict)


def ler_garantias(fontes: Path) -> FonteGarantias:
    caminho = _localizar(fontes, cfg.PADRAO_GARANTIAS)
    df = pd.read_excel(caminho, sheet_name=0, header=0)
    df.columns = [str(c).strip() for c in df.columns]

    diag: dict = {}
    faltando = [c for c in cfg.ColGarantias.OBRIGATORIAS if c not in df.columns]
    diag["colunas_faltando"] = faltando

    df["contrato"] = df[cfg.ColGarantias.CONTRATO].map(normalizar_contrato)
    diag["linhas_sem_contrato"] = int(df["contrato"].isna().sum())

    return FonteGarantias(df=df, caminho=caminho, diagnostico=diag)


def ler_pgtos(fontes: Path) -> FontePgtos:
    caminho = _localizar(fontes, cfg.PADRAO_PGTOS)
    df = pd.read_excel(caminho, sheet_name=0, header=0)
    df.columns = [str(c).strip() for c in df.columns]

    diag: dict = {}

    # Colunas fantasma "Unnamed: N" — registrar existência e QUALQUER célula
    # remanescente fora do esquema declarado antes de descartar.
    fantasmas = [c for c in df.columns if str(c).lower().startswith("unnamed")]
    celulas_fora_esquema = []
    for c in fantasmas:
        nn = df[df[c].notna()]
        for idx, val in nn[c].items():
            celulas_fora_esquema.append({"linha_excel": int(idx) + 2, "coluna": c, "valor": val})
    diag["colunas_fantasma"] = fantasmas
    diag["celulas_fora_esquema"] = celulas_fora_esquema
    df = df.drop(columns=fantasmas)

    faltando = [c for c in cfg.ColPgtos.OBRIGATORIAS if c not in df.columns]
    diag["colunas_faltando"] = faltando

    df["contrato"] = df[cfg.ColPgtos.CONTRATO].map(normalizar_contrato)

    # Predicados de grão (linha, não aba)
    df["_e_pagamento"] = df[cfg.ColPgtos.PARCELA].notna()
    df["_e_liberacao"] = df[cfg.ColPgtos.VALOR_LIBERADO].notna()

    ambos = int((df["_e_pagamento"] & df["_e_liberacao"]).sum())
    nenhum_mask = ~df["_e_pagamento"] & ~df["_e_liberacao"]

    # Linhas "nenhum predicado": separar vazias (lixo) de órfãs com valor.
    nenhum = df[nenhum_mask]
    tem_valor = (
        nenhum[cfg.ColPgtos.VALOR_PARCELA].notna()
        | nenhum[cfg.ColPgtos.JUROS].notna()
        | nenhum[cfg.ColPgtos.VALOR_LIBERADO].notna()
    )
    orfas = nenhum[tem_valor]
    vazias = nenhum[~tem_valor]

    diag["pred_ambos"] = ambos
    diag["pred_nenhum"] = int(nenhum_mask.sum())
    diag["linhas_orfas"] = [
        {
            "linha_excel": int(idx) + 2,
            "banco": r[cfg.ColPgtos.BANCO],
            "contrato": r["contrato"],
            "valor_parcela": r[cfg.ColPgtos.VALOR_PARCELA],
            "juros": r[cfg.ColPgtos.JUROS],
        }
        for idx, r in orfas.iterrows()
    ]
    diag["linhas_vazias"] = [int(idx) + 2 for idx in vazias.index]
    diag["linhas_sem_contrato"] = int(df["contrato"].isna().sum())

    return FontePgtos(df=df, caminho=caminho, diagnostico=diag)
