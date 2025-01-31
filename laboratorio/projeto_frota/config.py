# config.py
from dataclasses import dataclass, field
from pathlib import Path
import logging

@dataclass
class Config:
    # Configurações do Banco de Dados
    DB_NAME: str = "frota.db"
    DB_URL: str = f"sqlite:///{DB_NAME}"
    
    # Configurações do Excel
    EXCEL_FILE: str = "totalorcadofrotas.xlsx"
    SHEET_NAME: str = "Gatec"
    
    # Configurações de Log
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE: str = "frota_etl.log"

    # Validadores
    MEDIDORES_VALIDOS: list = field(default_factory=lambda: ["H", "KM/H", "IND"])