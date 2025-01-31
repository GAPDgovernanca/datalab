# database.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DatabaseConfig
from models import Base

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DatabaseConfig.SQLITE_DB}')
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Tabelas criadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            raise
            
    def get_session(self):
        return self.Session()