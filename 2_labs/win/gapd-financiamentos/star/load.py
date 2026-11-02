"""
Carga: materializa o star em DuckDB (destino físico primário) e, opcionalmente,
em parquet tipado. O destino é detalhe de implementação — o VertiPaq do Power BI
é, ele próprio, um star schema; DuckDB dá a mesma forma com trilha de auditoria.
"""
from __future__ import annotations

from pathlib import Path

import duckdb

from .transform import Star

# Ordem de criação respeitando dependência lógica (dims antes de fatos/ponte).
_ORDEM = [
    "dim_banco",
    "dim_garantidor",
    "dim_tipo_garantia",
    "dim_tempo",
    "dim_contrato",
    "fato_saldo",
    "fato_pagamento",
    "fato_liberacao",
    "ponte_contrato_garantia",
]


def gravar_duckdb(star: Star, destino: str | Path) -> Path:
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        destino.unlink()  # build determinístico: recriar do zero

    tabelas = star.tabelas()
    con = duckdb.connect(str(destino))
    try:
        con.execute("BEGIN TRANSACTION;")
        for nome in _ORDEM:
            df = tabelas[nome]  # noqa: F841 — referenciado pelo DuckDB via nome local
            con.register("_tmp", df)
            con.execute(f'CREATE TABLE "{nome}" AS SELECT * FROM _tmp;')
            con.unregister("_tmp")
        con.execute("COMMIT;")
    finally:
        con.close()
    return destino


def exportar_parquet(db: str | Path, pasta: str | Path) -> list[Path]:
    """Exporta cada tabela do DuckDB para parquet tipado via COPY nativo.

    Usa o próprio motor do DuckDB (sem pyarrow/fastparquet), preservando tipos.
    """
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    escritos = []
    con = duckdb.connect(str(db), read_only=True)
    try:
        for nome in _ORDEM:
            alvo = pasta / f"{nome}.parquet"
            con.execute(
                f"COPY \"{nome}\" TO '{alvo.as_posix()}' (FORMAT PARQUET);"
            )
            escritos.append(alvo)
    finally:
        con.close()
    return escritos
