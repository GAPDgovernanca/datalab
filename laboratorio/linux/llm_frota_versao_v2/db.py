import sqlite3
import logging
from contextlib import contextmanager

class Database:
    """
    Classe para gerenciamento da conexão e execução de operações no banco de dados SQLite.
    
    Esquema do Banco de Dados:
    
    Tabela: dim_equipamento
    - id_equipamento, modelo, usuario, classe, data_criacao
    
    Tabela: fato_uso
    - id, id_equipamento, tipo_medidor, uso_estimado, uso_realizado, uso_diferenca, data_referencia, data_processamento
    
    Tabela: sqlite_sequence
    - name, seq
    
    Tabela: fato_custo
    - id, id_equipamento, custo_hora_estimado, custo_hora_realizado, custo_hora_diferenca, total_estimado, total_realizado, total_diferenca, data_referencia, data_processamento
    
    Tabela: fato_combustivel
    - id, id_equipamento, comb_litros_estimado, comb_litros_realizado, comb_litros_diferenca, comb_valor_unitario_estimado, comb_valor_unitario_realizado, comb_valor_unitario_diferenca, comb_total_estimado, comb_total_realizado, comb_total_diferenca, data_referencia, data_processamento
    
    Tabela: fato_manutencao
    - id, id_equipamento, lubrificantes_estimado, lubrificantes_realizado, lubrificantes_diferenca, filtros_estimado, filtros_realizado, filtros_diferenca, graxas_estimado, graxas_realizado, graxas_diferenca, pecas_servicos_estimado, pecas_servicos_realizado, pecas_servicos_diferenca, data_referencia, data_processamento
    
    Tabela: fato_reforma
    - id, id_equipamento, reforma_estimado, reforma_realizado, reforma_diferenca, data_referencia, data_processamento
    
    Relacionamentos:
    - fato_uso.id_equipamento        -> dim_equipamento.id_equipamento
    - fato_custo.id_equipamento       -> dim_equipamento.id_equipamento
    - fato_combustivel.id_equipamento -> dim_equipamento.id_equipamento
    - fato_manutencao.id_equipamento  -> dim_equipamento.id_equipamento
    - fato_reforma.id_equipamento     -> dim_equipamento.id_equipamento
    """

    def __init__(self, db_path: str):
        """
        Inicializa a classe Database com o caminho para o banco de dados.

        :param db_path: Caminho para o arquivo SQLite.
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # Configuração básica do logger (pode ser ajustada conforme necessidade)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    @contextmanager
    def get_connection(self):
        """
        Context manager para criar uma conexão apenas para leitura.
        """
        conn = None
        try:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)  # 🔹 Ativa modo READ-ONLY
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao conectar com o banco: {e}")
            raise
        finally:
            if conn:
                conn.close()
                self.logger.debug("Conexão com o banco fechada.")

    def execute_query(self, query: str, params: tuple = None):
        """
        Executa apenas consultas (SELECT) no banco de dados.
        
        :param query: Instrução SQL de leitura.
        :param params: Parâmetros para a consulta.
        :return: Cursor com os resultados da execução.
        """
        if not query.strip().lower().startswith("select"):  # 🔹 Bloqueia qualquer coisa que não seja SELECT
            self.logger.error(f"Tentativa de modificação do banco bloqueada: {query}")
            raise PermissionError("Modificação no banco não permitida! Apenas consultas são permitidas.")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                self.logger.debug(f"Executando consulta: {query} com parâmetros: {params}")
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
            except sqlite3.Error as e:
                self.logger.error(f"Erro na execução da consulta: {e}\nQuery: {query}\nParâmetros: {params}")
                raise


    def fetch_all(self, query: str, params: tuple = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    self.logger.debug(f"Executando query: {query} com parâmetros: {params}")
                    cursor.execute(query, params)
                else:
                    self.logger.debug(f"Executando query: {query}")
                    cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()  # ✅ Fecha cursor antes de sair
                self.logger.debug(f"Retornados {len(results)} registros.")
                return results
            except sqlite3.Error as e:
                self.logger.error(f"Erro na execução da query: {e}\nQuery: {query}\nParâmetros: {params}")
                raise

    def fetch_one(self, query: str, params: tuple = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    self.logger.debug(f"Executando query: {query} com parâmetros: {params}")
                    cursor.execute(query, params)
                else:
                    self.logger.debug(f"Executando query: {query}")
                    cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()  # ✅ Fecha cursor antes de sair
                self.logger.debug("Retornado um registro." if result else "Nenhum registro encontrado.")
                return result
            except sqlite3.Error as e:
                self.logger.error(f"Erro na execução da query: {e}\nQuery: {query}\nParâmetros: {params}")
                raise

    def get_date_defaults(self):
        """
        Recupera as datas mínimas e máximas (data_referencia e data_processamento)
        combinadas de todas as tabelas de fato (fato_custo, fato_combustivel, fato_manutencao, fato_reforma, fato_uso).

        :return: Objeto sqlite3.Row contendo min_data_referencia, max_data_referencia,
                 min_data_processamento e max_data_processamento.
        """
        query = """
            SELECT MIN(data_referencia) AS min_data_referencia, 
                   MAX(data_referencia) AS max_data_referencia, 
                   MIN(data_processamento) AS min_data_processamento, 
                   MAX(data_processamento) AS max_data_processamento
            FROM (
                SELECT data_referencia, data_processamento FROM fato_custo
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_combustivel
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_manutencao
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_reforma
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_uso
            )
        """
        result = self.fetch_one(query)
        self.logger.debug("Datas padrão recuperadas com sucesso.")
        return result

# Caso haja a necessidade de implementar métodos adicionais, como inserções, atualizações ou consultas específicas,
# eles podem ser adicionados abaixo com o mesmo padrão de tratamento, logging e uso de parâmetros.
