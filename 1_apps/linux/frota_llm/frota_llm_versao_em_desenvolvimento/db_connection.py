# Arquivo: db_connection.py

import sqlite3
import streamlit as st
import os
from typing import Tuple, Optional


def get_db_connection(db_filename: str = "frota.db") -> Optional[sqlite3.Connection]:
    """
    Estabelece uma conexão com o banco de dados SQLite.

    Parameters:
        db_filename (str): Nome do arquivo SQLite.

    Returns:
        sqlite3.Connection: conexão SQLite configurada, ou None em caso de falha.
    """
    try:
        db_path = os.path.join(os.path.dirname(__file__), db_filename)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None


# Função otimizada para obter datas mínimas e máximas

def get_date_defaults(conn: sqlite3.Connection) -> Tuple[Optional[str], Optional[str]]:
    """
    Obtém datas mínimas e máximas das tabelas do banco para inicialização dos filtros.

    Parameters:
        conn (sqlite3.Connection): Conexão ativa com o banco de dados.

    Returns:
        Tuple contendo datas mínima e máxima no formato 'YYYY-MM-DD', ou (None, None).
    """
    query = """
        SELECT 
            MIN(data_referencia) AS min_data_referencia, 
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
    try:
        result = conn.execute(query).fetchone()
        if result:
            min_date = min(result["min_data_referencia"], result["min_data_processamento"])
            max_date = max(result["max_data_referencia"], result["max_data_processamento"])
            return min_date, max_date
        else:
            return None, None
    except sqlite3.Error as e:
        st.error(f"Erro ao obter datas padrão: {e}")
        return None, None
