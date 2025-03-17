# Arquivo: db_dashboard.py

import streamlit as st
import pandas as pd
from db_connection import get_db_connection, get_date_defaults
from db_filters import build_filters, calcular_multiplicadores, apply_flags
import plotly.express as px


# Função para carregar dados filtrados
def get_filtered_data(filtros: dict) -> pd.DataFrame:
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

    filters = build_filters(filtros)

    if filters:
        query += f" WHERE {filters}"

    query += " ORDER BY fc.data_referencia, de.classe, fc.id_equipamento"

    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


def display_metrics(df: pd.DataFrame):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'<div class="custom-card"><h3>Total de Registros</h3><p>{len(df):,}</p></div>', unsafe_allow_html=True)

    with col2:
        total_estimado_soma = df["total_estimado"].sum() if "total_estimado" in df.columns else 0
        st.markdown(f'<div class="custom-card"><h3>Total Estimado</h3><p>R$ {total_estimado_soma:,.0f}</p></div>', unsafe_allow_html=True)


def plot_chart(df: pd.DataFrame):
    plot_data = pd.DataFrame({
        'equipamento': df['id_equipamento'].astype(str),
        'Uso vs Planejado': df['Taxa Utilização Multiplicador'],
        'Consumo vs Planejado': df['Consumo Multiplicador']
    })

    fig = px.bar(
        plot_data.melt(id_vars='equipamento', var_name='Métrica'), 
        x='equipamento', 
        y='value', 
        color='Métrica',
        barmode='group',
        title='Indicadores de Uso e Consumo por Equipamento',
        labels={'value': 'Valor', 'equipamento': 'Equipamento'},
        color_discrete_map={
            'Uso vs Planejado': '#1f77b4',
            'Consumo vs Planejado': '#ff7f0e'
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_type='category',
        legend_title_text='Indicadores',
        yaxis_title="Multiplicador (Realizado/Planejado)",
        hovermode="x unified"
    )

    fig.add_hline(
        y=1, 
        line_dash="dot", 
        line_color="red",
        annotation_text="Planejado (1.0)", 
        annotation_position="bottom right"
    )

    st.plotly_chart(fig, use_container_width=True)

