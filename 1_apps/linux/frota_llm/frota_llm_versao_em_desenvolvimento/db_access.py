# db_access.py
import sqlite3
import os
import pandas as pd
import streamlit as st

def get_db_connection(db_filename: str = "frota.db") -> sqlite3.Connection:
    """
    Estabelece a conexão com o banco de dados SQLite.
    """
    try:
        db_path = os.path.join(os.path.dirname(__file__), db_filename)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def get_date_defaults() -> tuple:
    """
    Obtém as datas mínimas e máximas para inicialização dos filtros,
    consultando várias tabelas de fatos.
    """
    conn = get_db_connection()
    if not conn:
        return None, None
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
        conn.close()
        if result:
            min_date = min(result["min_data_referencia"], result["min_data_processamento"])
            max_date = max(result["max_data_referencia"], result["max_data_processamento"])
            return min_date, max_date
        else:
            return None, None
    except Exception as e:
        st.error(f"Erro ao obter datas padrão: {e}")
        return None, None

def build_filters(filtros: dict, alias: str = 'fc') -> str:
    """
    Constrói dinamicamente a cláusula WHERE da query SQL com base nos filtros.
    """
    conditions = []
    if filtros.get("data_referencia") and len(filtros["data_referencia"]) == 2:
        start_date, end_date = filtros["data_referencia"]
        conditions.append(f"{alias}.data_referencia BETWEEN '{start_date}' AND '{end_date}'")
    if filtros.get("id_equipamento"):
        ids = ",".join(map(str, filtros["id_equipamento"]))
        conditions.append(f"{alias}.id_equipamento IN ({ids})")
    if filtros.get("usuario") and "Todos" not in filtros["usuario"]:
        usuarios = "', '".join(filtros["usuario"])
        conditions.append(f"de.usuario IN ('{usuarios}')")
    if filtros.get("classe") and "Todos" not in filtros["classe"]:
        classes = "', '".join(filtros["classe"])
        conditions.append(f"de.classe IN ('{classes}')")
    return " AND ".join(conditions)

def get_filtered_data(filtros: dict) -> pd.DataFrame:
    """
    Carrega os dados filtrados a partir do banco de dados.
    """
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    query = """
        SELECT fc.id_equipamento, 
               fc.custo_hora_estimado, 
               fc.custo_hora_realizado, 
               -fc.custo_hora_diferenca AS custo_hora_diferenca, 
               fc.total_estimado, 
               fc.total_realizado, 
               -fc.total_diferenca AS total_diferenca, 
               de.classe, 
               de.usuario
        FROM fato_custo AS fc
        INNER JOIN dim_equipamento AS de
            ON fc.id_equipamento = de.id_equipamento
    """
    filters_str = build_filters(filtros)
    if filters_str:
        query += f" WHERE {filters_str}"
    query += " ORDER BY fc.data_referencia, de.classe, fc.id_equipamento"
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def get_additional_data(filtros: dict) -> dict:
    """
    Extrai dados adicionais de outras tabelas para enriquecer o dataset.
    """
    conn = get_db_connection()
    if not conn:
        return {}
    additional_data = {}
    tables_to_include = ["fato_combustivel", "fato_manutencao", "fato_reforma", "fato_uso"]
    for table in tables_to_include:
        query = f"""
            SELECT t.*
            FROM {table} AS t
            INNER JOIN dim_equipamento AS de
                ON t.id_equipamento = de.id_equipamento
            WHERE t.id_equipamento IN (SELECT id_equipamento FROM dim_equipamento)
        """
        filters_str = build_filters(filtros, alias='t')
        if filters_str:
            query += f" AND {filters_str}"
        try:
            additional_data[table] = pd.read_sql_query(query, conn).to_dict(orient='records')
        except Exception as e:
            st.error(f"Erro ao carregar dados da tabela {table}: {e}")
    conn.close()
    return additional_data

def get_unique_values(column_name: str) -> list:
    """
    Retorna os valores únicos de uma coluna da tabela de dimensão,
    auxiliando na criação dos filtros.
    """
    conn = get_db_connection()
    if not conn:
        return []
    query = f"SELECT DISTINCT {column_name} FROM dim_equipamento"
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return sorted(df[column_name].dropna().tolist())
    except Exception as e:
        st.error(f"Erro ao carregar valores únicos para {column_name}: {e}")
        return []
