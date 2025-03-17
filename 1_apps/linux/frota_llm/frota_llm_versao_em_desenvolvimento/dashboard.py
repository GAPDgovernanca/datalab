import streamlit as st

# A chamada para set_page_config deve ser a primeira instrução do Streamlit
st.set_page_config(layout="wide")

import pandas as pd
import plotly.express as px
from db_access import (
    get_date_defaults,
    get_filtered_data,
    get_additional_data,
    get_unique_values
)
from llm_session import query_groq
from db_filters import apply_flags, calcular_multiplicadores

# CSS para personalização (igual ao do programa original)
st.markdown("""
    <style>
    .reportview-container { background-color: #f0f0f0; }
    .sidebar .sidebar-content { padding-top: 0px; }
    .block-container { padding-top: 2rem; }
    .custom-card {
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #34495e;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 10px;
        color: #ecf0f1;
    }
    .custom-card p {
        font-size: 28px;
        font-weight: bold;
    }
    .card-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        gap: 10px;
    }
    .centered-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #ecf0f1;
    }
    .custom-header {
        color: #ecf0f1;
        font-size: 28px;
        font-weight: bold;
    }
    .custom-subheader {
        color: #bdc3c7;
        font-size: 20px;
    }
    .stDataFrame div[data-testid="stHorizontalBlock"] {
        width: auto !important;
        min-width: 150px !important;
    }
    .ai-response {
        font-size: 18px;
        font-family: Arial, sans-serif;
        line-height: 1.5;
        color: #ecf0f1;
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #34495e;
    }
    .down-green {
        color: #50C878 !important;
    }
    .stTextArea textarea {
        min-height: 100px;
        max-height: 500px;
        resize: vertical;
        overflow: auto;
        line-height: 1.5;
        padding: 8px;
        font-size: 16px;
        font-family: Arial, sans-serif;
    }
    textarea {
        height: auto !important;
        min-height: 100px !important;
        transition: height 0.1s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração da página com cabeçalho formatado
st.markdown('<h1 class="centered-title">Frota - Dashboard Operacional</h1>', unsafe_allow_html=True)

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
        st.markdown(f'<div class="custom-card"><h3>Total de Registros</h3><p>{len(df):,}</p></div>', unsafe_allow_html=True)
    with col2:
        total_estimado = df["total_estimado"].sum() if "total_estimado" in df.columns else 0
        st.markdown(f'<div class="custom-card"><h3>Total Estimado</h3><p>R$ {total_estimado:,.0f}</p></div>', unsafe_allow_html=True)
    
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
        hovermode="x unified",
        bargap=0.0,          # Remove o espaço entre grupos de barras
        bargroupgap=0.0,     # Remove o espaço entre as barras dentro do mesmo grupo
        margin=dict(l=0, r=0, t=30, b=0)  # Ajusta margens do gráfico (opcional)
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

    # Exibição da tabela exatamente igual ao programa original
    st.subheader("Dados filtrados")
    if not df.empty:
        # Aplica os sinalizadores (com a lógica ajustada) e calcula multiplicadores
        df = apply_flags(df)
        df = calcular_multiplicadores(df)
        
        # Renomeia colunas para exibição
        df = df.rename(columns={
            'usuario': 'Fazenda',
            'classe': 'Classe',
            'id_equipamento': 'Equip',
            'custo_hora_estimado': 'Custo Orçado',
            'custo_hora_realizado': 'Custo Realizado',
            'custo_hora_diferenca': 'Custo Dif',
            'total_estimado': 'Total Orçado',
            'total_realizado': 'Total Realizado',
            'total_diferenca': 'Total Dif',
        })

        # Ajusta a ordem das colunas para exibição
        df = df[['Fazenda', 'Classe', 'Equip', 'Custo Orçado', 'Custo Realizado', 'Custo Dif', 
                'Total Orçado', 'Total Realizado', 'Total Dif', 'Sinalizador']]

        # Arredonda os valores numéricos para facilitar a visualização
        df.update(df.select_dtypes(include=['float', 'int']).round(0))
        
        # Formata a tabela com estilos personalizados
        styled_df = df.style.format({
            'Custo Orçado': 'R$ {:,.0f}',
            'Custo Realizado': 'R$ {:,.0f}',
            'Custo Dif': 'R$ {:,.0f}',
            'Total Orçado': 'R$ {:,.0f}',
            'Total Realizado': 'R$ {:,.0f}',
            'Total Dif': 'R$ {:,.0f}'
        }).set_table_styles([
            {'selector': 'table', 'props': [('table-layout', 'fixed'), ('width', '150%')]},
            {'selector': 'th, td', 'props': [('text-align', 'center'), ('padding', '10px')]},
            {'selector': 'th:nth-child(1), td:nth-child(1)', 'props': [('width', '150px')]},
            {'selector': 'th:nth-child(2), td:nth-child(2)', 'props': [('width', '120px')]},
            {'selector': 'th:nth-child(3), td:nth-child(3)', 'props': [('width', '100px')]},
            {'selector': 'th:nth-child(n+4), td:nth-child(n+4)', 'props': [('width', '300px')]},
            {'selector': 'th:last-child, td:last-child', 'props': [('width', '60px')]}
        ])

        st.dataframe(styled_df)

# Área para perguntas à LLM
st.subheader("Perguntas sobre os dados")
user_question = st.text_area("Digite sua pergunta:", height=100, key="auto_expanding_textarea", max_chars=None)
if st.button("Perguntar ao GROQ"):
    if user_question:
        # Combina os dados filtrados e adicionais para enviar à LLM
        combined_data = {"filtered_data": df.to_dict(orient='records'), "additional_data": additional_data}
        answer = query_groq(combined_data, user_question)
        st.markdown(answer)
    else:
        st.warning("Por favor, insira uma pergunta.")
