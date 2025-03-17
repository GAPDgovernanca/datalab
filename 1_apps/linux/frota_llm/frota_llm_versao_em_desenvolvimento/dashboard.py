# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_access import (
    get_date_defaults,
    get_filtered_data,
    get_additional_data,
    get_unique_values
)
from llm_session import query_groq

# Configuração da página
st.set_page_config(layout="wide")
st.markdown('<h1 style="text-align: center; color: #2c3e50;">Dashboard Operacional da Frota</h1>', unsafe_allow_html=True)

# Obter datas padrão para os filtros
default_min_date, default_max_date = get_date_defaults()

# Sidebar - Filtros
date_range = st.sidebar.date_input("Data de Referência", [default_min_date, default_max_date])
usuarios_opcoes = ["Todos"] + get_unique_values("usuario")
usuario = st.sidebar.multiselect("Usuário", usuarios_opcoes, default=["Todos"])
classes_opcoes = ["Todos"] + get_unique_values("classe")
classe = st.sidebar.multiselect("Classe", classes_opcoes, default=["Todos"])
id_equipamento = st.sidebar.text_input("IDs de Equipamento (separados por vírgula)")

filtros = {
    "data_referencia": date_range if date_range else None,
    "id_equipamento": [int(x) for x in id_equipamento.split(',')] if id_equipamento else None,
    "usuario": usuario if "Todos" not in usuario else None,
    "classe": classe if "Todos" not in classe else None,
}

# Carregar dados filtrados e dados adicionais para consulta à LLM
df = get_filtered_data(filtros)
additional_data = get_additional_data(filtros)

# Exibe aviso caso não haja dados
if df.empty:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")

# Se houver dados, exibe métricas e gráfico
if not df.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Total de Registros:** {len(df):,}")
    with col2:
        total_estimado = df["total_estimado"].sum() if "total_estimado" in df.columns else 0
        st.markdown(f"**Total Estimado:** R$ {total_estimado:,.0f}")
    
    # Preparação dos dados para o gráfico
    chart_data = df.copy()
    chart_data['Taxa Utilização Multiplicador'] = chart_data.apply(
        lambda row: row['custo_hora_realizado'] / row['custo_hora_estimado'] if row['custo_hora_estimado'] != 0 else 0,
        axis=1
    )
    chart_data['Consumo Multiplicador'] = chart_data.apply(
        lambda row: row['total_realizado'] / row['total_estimado'] if row['total_estimado'] != 0 else 0,
        axis=1
    )
    plot_data = pd.DataFrame({
        'Equipamento': chart_data['id_equipamento'].astype(str),
        'Uso vs Planejado': chart_data['Taxa Utilização Multiplicador'],
        'Consumo vs Planejado': chart_data['Consumo Multiplicador']
    })

    # Criação do gráfico com as atualizações
    fig = px.bar(
        plot_data.melt(id_vars='Equipamento', var_name='Métrica'),
        x='Equipamento',
        y='value',
        color='Métrica',
        barmode='group',
        title='Indicadores de Uso e Consumo por Equipamento',
        labels={'value': 'Valor (Escala Log)', 'Equipamento': 'Equipamento'},
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

    # Aplicar escala logarítmica no eixo Y
    fig.update_yaxes(type="log")

    # Linha horizontal tracejada em y=1 (referência ao planejado)
    fig.add_hline(
        y=1, 
        line_dash="dot", 
        line_color="red",
        annotation_text="Planejado (1.0)", 
        annotation_position="bottom right"
    )

    # Linha vertical tracejada vermelha em um equipamento específico (exemplo: equipamento "25")
    fig.add_shape(
        type="line",
        xref="x",     # Referência ao eixo X categórico
        yref="paper", # Para que a linha cubra toda a altura do gráfico
        x0="25",      # Altere "25" para a categoria desejada
        x1="25",
        y0=0,
        y1=1,
        line=dict(
            color="red",
            width=2,
            dash="dot"  # Estilo tracejado
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# Área para perguntas à LLM
st.subheader("Perguntas sobre os dados")
user_question = st.text_area("Digite sua pergunta:", height=100)
if st.button("Perguntar"):
    if user_question:
        # Combina os dados filtrados e adicionais para enviar à LLM
        combined_data = {"filtered_data": df.to_dict(orient='records'), "additional_data": additional_data}
        answer = query_groq(combined_data, user_question)
        st.markdown(answer)
    else:
        st.warning("Por favor, qual sua pergunta?")