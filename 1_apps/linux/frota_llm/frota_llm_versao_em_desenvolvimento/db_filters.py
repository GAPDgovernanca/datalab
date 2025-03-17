# Arquivo: db_filters.py

from typing import Dict, List, Any
import pandas as pd  # ESSA LINHA É OBRIGATÓRIA E PRECISA SER ADICIONADA
import sqlite3


def build_filters(filtros: Dict, alias: str = 'fc') -> str:
    conditions = []

    data_referencia = filtros.get("data_referencia")
    if data_referencia and len(data_referencia := filtros["data_referencia"]) == 2:
        start_date, end_date = data_referencia
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


def get_unique_values(conn, column_name: str) -> list:
    """
    Obtém valores únicos de uma coluna específica para filtros dimensionais.

    Parameters:
        conn (sqlite3.Connection): Conexão ativa com o banco de dados.
        column_name (str): Nome da coluna a ser consultada.

    Returns:
        List contendo valores únicos ordenados alfabeticamente.
    """
    try:
        cursor = conn.execute(f"SELECT DISTINCT {column_name} FROM dim_equipamento")
        unique_values = sorted([row[0] for row in cursor.fetchall() if row[0]])
        return unique_values
    except Exception as e:
        print(f"Erro ao carregar valores únicos para {column_name}: {e}")
        return []


def calcular_multiplicadores(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df['Taxa Utilização Multiplicador'] = df.apply(
        lambda row: row['custo_hora_realizado'] / row['custo_hora_estimado']
        if row['custo_hora_estimado'] != 0 else 0.0,
        axis=1
    )

    df['Consumo Multiplicador'] = df.apply(
        lambda row: row['total_realizado'] / row['total_estimado']
        if row['total_estimado'] != 0 else 0.0,
        axis=1
    )

    return df


def apply_flags(df: pd.DataFrame) -> pd.DataFrame:
    def flag_diferenca(row):
        if row['total_estimado'] == 0 and row['total_realizado'] > 0:
            return '🔶'
        if row['total_estimado'] != 0:
            percentual = (row['total_realizado'] - row['total_estimado']) / row['total_estimado'] * 100
            if percentual > 10:
                return '🟢'
            elif percentual < -10:
                return '🔴'
        return '⚪'

    df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df
