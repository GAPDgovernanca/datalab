#!/usr/bin/env python3
"""
Pipeline determinístico: fonte -> validação -> star (DuckDB).

Uso típico (a partir da raiz do projeto, com a venv ativa):

    python build_star.py --sources ./data --out ./build
    python build_star.py --sources ./data --out ./build --parquet
    python build_star.py --sources ./data --check      # valida sem gravar
    python build_star.py --sources ./data --out ./build --queries

Descobre as duas planilhas por padrão de nome dentro de --sources; a data-base do
ciclo é lida do prefixo AAAAMMDD do arquivo. Recusa gravar se qualquer teste de
aceitação duro falhar (exit code 2).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from star import config as cfg
from star import ingest, load, queries, transform, validate


def _fmt(df, casas=2):
    import pandas as pd

    with pd.option_context("display.max_rows", 100, "display.width", 200,
                           "display.float_format", lambda v: f"{v:,.{casas}f}"):
        return df.to_string(index=False)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build do star schema de contratos de financiamento (GAPD).")
    ap.add_argument("--sources", type=Path, default=Path("./data"),
                    help="pasta com as duas planilhas do Financeiro (default: ./data)")
    ap.add_argument("--out", type=Path, default=Path("./build"),
                    help="pasta de saída do DuckDB / parquet (default: ./build)")
    ap.add_argument("--db-name", default="gapd_star.duckdb", help="nome do arquivo DuckDB")
    ap.add_argument("--parquet", action="store_true", help="também exporta parquet tipado por tabela")
    ap.add_argument("--queries", action="store_true", help="roda as consultas do Conselho ao final")
    ap.add_argument("--check", action="store_true", help="apenas valida; não grava artefatos")
    args = ap.parse_args(argv)

    # 1) Ingestão -----------------------------------------------------------
    print("→ Ingestão")
    gar = ingest.ler_garantias(args.sources)
    pg = ingest.ler_pgtos(args.sources)
    db_gar = cfg.data_base_do_arquivo(gar.caminho)
    db_pg = cfg.data_base_do_arquivo(pg.caminho)
    if db_gar != db_pg:
        print(f"FALHA: data-base divergente entre fontes ({db_gar} vs {db_pg})", file=sys.stderr)
        return 2
    data_base = db_gar
    print(f"  GARANTIAS: {gar.caminho.name}")
    print(f"  PGTOS    : {pg.caminho.name}")
    print(f"  data-base: {data_base.isoformat()}\n")

    # 2) Validação (porta de qualidade) ------------------------------------
    print("→ Validação")
    try:
        rel = validate.validar(gar, pg, estrito=True)
    except validate.ErroIngestao as e:
        print(str(e), file=sys.stderr)
        return 2
    print(rel.render(), "\n")

    if args.check:
        print("Modo --check: nenhum artefato gravado.")
        return 0

    # 3) Transformação ------------------------------------------------------
    print("→ Transformação")
    star = transform.construir(gar, pg, data_base)
    for nome, df in star.tabelas().items():
        print(f"  {nome:28s} {len(df):>5d} linhas × {df.shape[1]} colunas")
    print()

    # 4) Carga --------------------------------------------------------------
    print("→ Carga")
    destino = load.gravar_duckdb(star, args.out / args.db_name)
    print(f"  DuckDB → {destino}")
    if args.parquet:
        escritos = load.exportar_parquet(destino, args.out / "parquet")
        print(f"  parquet → {len(escritos)} tabelas em {args.out / 'parquet'}")
    print()

    # 5) Reconciliação pós-carga (verifica o DB, não a memória) -------------
    print("→ Reconciliação pós-carga")
    print(_fmt(queries.reconciliacao(destino)), "\n")

    if args.queries:
        print("→ Consultas do Conselho\n")
        print("Exposição por garantidor — avais PF:")
        print(_fmt(queries.exposicao_por_garantidor(destino, classe="PF")), "\n")
        print("Exposição por garantidor — avais PJ-holding:")
        print(_fmt(queries.exposicao_por_garantidor(destino, classe="PJ-holding")), "\n")
        print("Perfil de vencimentos (contratos vivos):")
        print(_fmt(queries.perfil_vencimentos(destino)), "\n")
        print("Quitado × a quitar (parcelas, relativo à data-base):")
        print(_fmt(queries.quitado_e_a_quitar(destino)), "\n")

    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
