# Arquivo: frota_llm.py

from typing import Dict, List, Any
import pandas as pd
import sqlite3
import streamlit as st
from db_connection import get_db_connection, get_date_defaults
from db_filters import build_filters, calcular_multiplicadores, apply_flags
from db_dashboard import get_filtered_data, display_metrics, plot_chart

st.set_page_config(layout="wide")

st.title("Dashboard Operacional da Frota")

# Conexão e datas padrão
conn = get_db_connection()
min_date, max_date = get_date_defaults(conn)

# Sidebar - Filtros interativos
st.sidebar.header("Filtros")
date_range = st.sidebar.date_input("Data de Referência", [min_date, max_date])
usuario = st.sidebar.multiselect("Usuário", ["Todos"], default=["Todos"])
classe = st.sidebar.multiselect("Classe", ["Todos"], default=["Todos"])
id_equipamento = st.sidebar.text_input("IDs de Equipamento (separados por vírgula)")

def build_filters(filtros: Dict, alias: str = 'fc') -> str:
    conditions = []

    data_referencia = filtros.get("data_referencia")
    if data_referencia and len(data_referencia) == 2:
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


def calcular_multiplicadores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula os multiplicadores de uso e consumo com base nos valores estimados e realizados.

    Parameters:
        df (pd.DataFrame): DataFrame contendo os dados para cálculo dos multiplicadores.

    Returns:
        pd.DataFrame com as novas colunas adicionadas para multiplicadores.
    """
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
    """
    Aplica sinalizadores para indicar o desempenho financeiro com base na diferença percentual.

    Parameters:
        df (pd.DataFrame): DataFrame contendo dados financeiros para sinalização.

    Returns:
        DataFrame com a coluna adicional 'Sinalizador' indicando status financeiro.
    """

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


filtros = {
    "data_referencia": date_range if date_range else None,
    "id_equipamento": [int(x) for x in id_equipamento.split(',')] if id_equipamento else None,
    "classe": classe if "Todos" not in classe else None,
    "usuario": usuario if "Todos" not in usuario else None,
}

# Carrega os dados filtrados com base nos filtros escolhidos
df = get_filtered_data(filtros)

if not df.empty:
    df = apply_flags(df)
    df = calcular_multiplicadores(df)

    display_metrics(df)
    plot_chart(df)

    st.subheader("Dados Detalhados")
    st.dataframe(df)
else:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
