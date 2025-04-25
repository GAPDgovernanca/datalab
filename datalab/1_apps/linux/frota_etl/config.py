# config.py
"""
Módulo: Configurações ETL Frotas
Objetivo: Centralizar configurações e constantes do sistema
"""

from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ConfigETL:
    # Configurações de Sistema
    DIRETORIO_BASE = Path(__file__).parent
    DIRETORIO_LOGS = DIRETORIO_BASE / 'logs'
    ARQUIVO_LOG = DIRETORIO_LOGS / 'etl_log.log'
    ARQUIVO_DADOS = DIRETORIO_BASE / 'totalorcadofrotas.xlsx'  # Adicionado

    
    # Configurações de Negócio
    DATA_REFERENCIA = datetime(2025, 4, 1)
    TIPOS_MEDIDOR = ["H", "KM/H", "IND"]
    
    # Configurações de Banco
    NOME_BANCO = 'frota.db'
    TAMANHO_LOTE = 1000