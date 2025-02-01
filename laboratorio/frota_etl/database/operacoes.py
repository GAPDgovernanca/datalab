# database/operacoes.py
"""
Módulo: Operações do Banco de Dados
Objetivo: Gerenciar operações de banco de dados SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import logging
from .esquema import EsquemaDimensional

class GerenciadorBanco:
    """Gerencia operações no banco SQLite"""
    
    def __init__(self, nome_banco: str, logger: logging.Logger):
        self.caminho_banco = Path(nome_banco)
        self.logger = logger
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        """Estabelece conexão com o banco"""
        try:
            self.conn = sqlite3.connect(self.caminho_banco)
            self.cursor = self.conn.cursor()
            self.logger.info(f"Conexão estabelecida com {self.caminho_banco}")
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco: {str(e)}")
            raise
    
    def criar_estrutura(self):
        """Cria estrutura inicial do banco"""
        try:
            self.conectar()
            for comando_sql in EsquemaDimensional.obter_todos_schemas():
                self.cursor.execute(comando_sql)
            self.conn.commit()
            self.logger.info("Estrutura do banco criada com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao criar estrutura: {str(e)}")
            raise
        finally:
            self.desconectar()
    
    def inserir_lote(self, tabela: str, dados: list):
        """Insere lote de dados em uma tabela garantindo valores nulos tratados"""
        try:
            self.conectar()
            if not dados:
                self.logger.warning(f"Nenhum dado disponível para inserir em {tabela}")
                return

            # Garante que todas as colunas esperadas estejam presentes
            colunas = ', '.join(dados[0].keys())
            placeholders = ', '.join(['?' for _ in dados[0].values()])
            
            # Substituir valores None por 0 antes da inserção
            dados_processados = [tuple(d.values()) for d in dados]

            self.cursor.executemany(
                f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})",  
                dados_processados
            )
            self.conn.commit()
            self.logger.info(f"Inseridos {len(dados)} registros em {tabela}")
        except Exception as e:
            self.logger.error(f"Erro ao inserir lote em {tabela}: {str(e)}")
            raise
        finally:
            self.desconectar()
    
    def desconectar(self):
        """Encerra conexão com o banco"""
        if self.conn:
            self.conn.close()
            self.logger.info("Conexão com banco encerrada")