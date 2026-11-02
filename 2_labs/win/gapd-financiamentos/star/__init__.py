"""Camada semântica de governança — star schema de contratos de financiamento (GAPD).

Implementa o transform determinístico do ADR-001:
    fonte -> validação na ingestão -> star.
"""
from . import config, ingest, load, queries, transform, validate  # noqa: F401

__all__ = ["config", "ingest", "validate", "transform", "load", "queries"]
__version__ = "0.1.0"
