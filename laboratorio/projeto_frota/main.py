# main.py
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Base
from etl import FrotaETL

def configurar_logger():
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=Config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def criar_banco():
    """Cria o banco de dados e retorna a sessão"""
    engine = create_engine(Config.DB_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def main():
    """Função principal"""
    try:
        # Configuração inicial
        configurar_logger()
        logger = logging.getLogger(__name__)
        logger.info("Iniciando processo de ETL")

        # Verifica arquivo Excel
        if not Path(Config.EXCEL_FILE).exists():
            raise FileNotFoundError(f"Arquivo {Config.EXCEL_FILE} não encontrado")

        # Cria banco e sessão
        session = criar_banco()
        
        # Executa ETL
        etl = FrotaETL(session)
        etl.executar()
        
        logger.info("Processo concluído com sucesso")

    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        raise
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()