# main.py
"""
Módulo: Execução Principal
Objetivo: Coordenar processo ETL de dados de frotas para banco dimensional
Autor: Claude
Data: 01/02/2025
"""

import sys
from pathlib import Path
from datetime import datetime
import logging
from config import ConfigETL
from transformador.excel import ProcessadorExcel
from database.operacoes import GerenciadorBanco

def configurar_ambiente() -> tuple:
    """
    Prepara ambiente de execução
    Returns:
        tuple: Configuração e logger configurados
    """
    config = ConfigETL()
    
    # Garante existência do diretório de logs
    config.DIRETORIO_LOGS.mkdir(exist_ok=True)
    
    # Configura logger
    logging.basicConfig(
        filename=config.ARQUIVO_LOG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger('ETL_Frotas')
    
    return config, logger

def executar_etl(arquivo: str, config: ConfigETL, logger: logging.Logger) -> bool:
    """
    Executa processo ETL completo
    Args:
        arquivo: Caminho do arquivo Excel
        config: Configurações do sistema
        logger: Logger configurado
    Returns:
        bool: Status da execução
    """
    try:
        logger.info(f"Iniciando ETL - Arquivo: {arquivo}")
        
        # Inicializa banco de dados
        banco = GerenciadorBanco(config.NOME_BANCO, logger)
        banco.criar_estrutura()
        
        # Processa dados
        processador = ProcessadorExcel(arquivo, logger)
        dimensoes, fatos = processador.executar()
        
        # Carrega dimensões
        for nome_tabela, dados in dimensoes.items():
            banco.inserir_lote(nome_tabela, dados)
        
        # Carrega fatos
        for nome_tabela, dados in fatos.items():
            banco.inserir_lote(nome_tabela, dados)
        
        logger.info("Processo ETL concluído com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro fatal no processo ETL: {str(e)}")
        return False

def main():
    """Função principal de execução"""
    try:
        # Configuração inicial
        config, logger = configurar_ambiente()
        
        # Verifica arquivo de entrada
        if not config.ARQUIVO_DADOS.exists():
            logger.error(f"Arquivo não encontrado: {config.ARQUIVO_DADOS}")
            sys.exit(1)
        
        # Executa ETL
        sucesso = executar_etl(config.ARQUIVO_DADOS, config, logger)
        
        # Finaliza execução
        codigo_saida = 0 if sucesso else 1
        sys.exit(codigo_saida)
        
    except Exception as e:
        print(f"Erro crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()