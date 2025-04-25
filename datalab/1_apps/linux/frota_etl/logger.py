"""
Módulo: Configuração de Logging
Objetivo: Centralizar configuração do sistema de logs
"""

import logging
from pathlib import Path
from datetime import datetime

def configurar_logger(arquivo_log: Path) -> logging.Logger:
    """
    Configura sistema de logging
    Args:
        arquivo_log: Caminho do arquivo de log
    Returns:
        Logger configurado
    """
    formatador = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger('ETL_Frotas')
    logger.setLevel(logging.INFO)
    
    # Handler de arquivo
    arquivo_handler = logging.FileHandler(arquivo_log)
    arquivo_handler.setFormatter(formatador)
    logger.addHandler(arquivo_handler)
    
    # Handler de console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatador)
    logger.addHandler(console_handler)
    
    return logger