import streamlit as st
import pandas as pd
import sqlite3
import os
from PIL import Image
from groq import Groq
from streamlit.components.v1 import html
import plotly.express as px
from datetime import datetime
import re

# Configuração do layout do Streamlit
st.set_page_config(layout="wide")

# CSS para personalização
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

# Configuração da API GROQ
api_key = st.secrets["GROQ_API_KEY"]  # Chave lida do secrets
client = Groq(api_key=api_key)

# Função para conectar ao banco SQLite (agora com caminho ajustado)
def get_db_connection():
    try:
        db_path = os.path.join(os.path.dirname(__file__), "frota.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter os valores mínimos e máximos das datas (para filtros)
def get_date_defaults():
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

# Função para processar perguntas usando GROQ AI
def query_groq(data_json, question, model_name="deepseek-r1-distill-llama-70b"):
    try:
        # Montar prompt sem cálculos de proporcionalidade, pois o DB já está configurado corretamente.
        prompt = f"""
        ### Você é um especialista em gestão de frota agrícola, com foco em análise financeira e cálculos de eficiência operacional.

        ---

        ### Regras para Representação Numérica

        - Acima de 1.000: arredondar para a centena mais próxima (ex.: 12.345 → 12.300).
        - Abaixo de 1.000: arredondar para a dezena mais próxima (ex.: 545 → 550).
        - Manter consistência em tabelas.
        - Evitar casas decimais desnecessárias.

        ---

        ### Estrutura da Resposta

        1. Conclusão Principal
        2. Cálculos de Suporte
        3. Tabelas

        ---

        ### Cálculos Principais

        - Diferença Absoluta
          Δ = (Valor_Realizado) - (Valor_Orcado)

        - Desvio Percentual
          Δ% = ((Valor_Realizado) - (Valor_Orcado)) / (Valor_Orcado) x 100

        - Taxa de Utilização
          U = Uso_Realizado / Uso_Estimado  (se Uso_Estimado = 0, então U = 0.0)
          U > 1.0 → Superutilização (🔴)
          U < 1.0 → Subutilização (🟢)

        ---

        ### Tabelas do Banco de Dados

        - dim_equipamento (Equipamentos)
          id_equipamento, modelo, usuário, classe, data_criação

        - fato_uso (Uso)
          id_equipamento, uso_estimado, uso_realizado, uso_diferença, data_referência

        - fato_custo (Custo)
          id_equipamento, custo_hora_estimado, custo_hora_realizado, total_estimado, total_realizado, data_referencia

        - fato_combustivel (Combustível)
          id_equipamento, comb_litros_estimado, comb_litros_realizado, comb_valor_unitario_estimado, comb_valor_unitario_realizado, comb_total_estimado, comb_total_realizado

        - fato_manutencao (Manutenção)
          id_equipamento, lubrificantes, filtros, graxas, peças_serviços (estimado/realizado)

        - fato_reforma (Reforma)
          id_equipamento, reforma_estimado, reforma_realizado, data_referência

        ---

        ### Relacionamentos

        - Todas as tabelas de fato se conectam à dim_equipamento via id_equipamento.

        ---

        ### Diretrizes

        - Linguagem: português brasileiro.
        - Não formatar fontes em negrito ou itálico.
        - Fornecer insights objetivos, baseados diretamente nos valores do banco.
        - Não aplicar ajustes de datas.

        **Dataset Provided:**
        ```json
        {data_json}
        ```

        **User Query:**
        ```text
        {question}
        ```
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly specialized assistant."},
                {"role": "user", "content": prompt}
            ],
            model=model_name,
        )
        response = chat_completion.choices[0].message.content

        if "<think>" in response and "</think>" in response:
            cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        else:
            cleaned_response = response

        return cleaned_response

    except Exception as e:
        st.error(f"Erro ao comunicar com a API GROQ: {e}")
        return "Erro ao processar a consulta."

# Função para validar e construir filtros SQL
def build_filters(filtros, alias='fc'):
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

# Função para carregar dados com filtros
def get_filtered_data(filtros):
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

# Função para carregar dados adicionais para a IA
def get_additional_data(filtros):
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
        filters = build_filters(filtros, alias='t')
        if filters:
            query += f" AND {filters}"
        try:
            additional_data[table] = pd.read_sql_query(query, conn).to_dict(orient='records')
        except Exception as e:
            st.error(f"Erro ao carregar dados da tabela {table}: {e}")

    conn.close()
    return additional_data

# Função para carregar valores únicos para filtros dimensionais
def get_unique_values(column_name):
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

# FUNÇÃO COM O AJUSTE SOLICITADO
def apply_flags(df):
    def flag_diferenca(row):
        # Caso especial: não havia orçamento (0), mas houve custo realizado > 0
        if row['total_estimado'] == 0 and row['total_realizado'] > 0:
            return '🔶'  # <-- Sinalizador para "uso sem orçamento"

        # Se houve orçamento, aplica a lógica normal:
        if row['total_estimado'] != 0:
            percentual = (row['total_diferenca'] / row['total_estimado'] * 100)
            if percentual > 10:
                return '🟢'
            elif percentual < -10:
                return '🔴'
            else:
                return '⚪'
        else:
            # Se total_estimado == 0 e total_realizado == 0, mantém branco
            return '⚪'

    if 'total_diferenca' in df.columns:
        df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df

def calcular_multiplicadores(df):
    """
    Calcula os multiplicadores utilizando os valores originais, sem ajuste proporcional.
    """
    try:
        conn = get_db_connection()
        if conn:
            uso_query = """
                SELECT id_equipamento, uso_estimado, uso_realizado 
                FROM fato_uso 
                WHERE id_equipamento IN ({})
            """.format(','.join(map(str, df['id_equipamento'].unique())))
            
            uso_df = pd.read_sql_query(uso_query, conn)
            conn.close()
            
            df = df.merge(uso_df, on='id_equipamento', how='left')
        
        if 'uso_estimado' in df.columns and 'uso_realizado' in df.columns:
            df['Taxa Utilização Multiplicador'] = df.apply(
                lambda row: row['uso_realizado'] / row['uso_estimado']
                if row['uso_estimado'] != 0 else 0.0,
                axis=1
            )
        
        if 'Total Orçado' in df.columns and 'Total Realizado' in df.columns:
            df['Consumo Multiplicador'] = df.apply(
                lambda row: row['Total Realizado'] / row['Total Orçado']
                if row['Total Orçado'] != 0 else 0.0,
                axis=1
            )
        
        return df
        
    except Exception as e:
        print(f"Erro ao calcular multiplicadores: {e}")
        return df

# Título principal
st.markdown('<h1 class="centered-title">Frota - Dashboard Operacional</h1>', unsafe_allow_html=True)

# Obter datas padrão para inicialização (usado apenas para filtro)
default_min_date, default_max_date = get_date_defaults()

# Sidebar - Filtros
date_range = st.sidebar.date_input("Data de Referência", [default_min_date, default_max_date])
usuarios_opcoes = ["Todos"] + get_unique_values("usuario")
usuario = st.sidebar.multiselect("Unidade", usuarios_opcoes, default=["Todos"])

classes_opcoes = ["Todos"] + get_unique_values("classe")
classe = st.sidebar.multiselect("Classe", classes_opcoes, default=["Todos"])

id_equipamento = st.sidebar.text_input("IDs de Equipamento (separados por vírgula)")

filtros = {
    "data_referencia": date_range if date_range else None,
    "id_equipamento": [int(x) for x in id_equipamento.split(',')] if id_equipamento else None,
    "classe": classe if classe != "Todos" else None,
    "usuario": usuario if usuario != "Todos" else None,
}

df = get_filtered_data(filtros)
additional_data = get_additional_data(filtros)

if df.empty:
    st.warning("Nenhum dado encontrado para os filtros aplicados. Verifique os parâmetros.")

# Exibir métricas
st.markdown('<div class="card-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="custom-card"><h3>Total de Registros</h3><p>{len(df):,}</p></div>', unsafe_allow_html=True)

with col2:
    total_estimado_soma = df["total_estimado"].sum() if "total_estimado" in df.columns else 0
    st.markdown(f'<div class="custom-card"><h3>Total Estimado</h3><p>R$ {total_estimado_soma:,.0f}</p></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if not df.empty:
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
        'equipamento': chart_data['id_equipamento'].astype(str),
        'Uso vs Planejado': chart_data['Taxa Utilização Multiplicador'],
        'Consumo vs Planejado': chart_data['Consumo Multiplicador']
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
    
    st.markdown('<div style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    try:
        from streamlit.components.v1 import html
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Dados filtrados")
if not df.empty:
    # Aplica os sinalizadores (já com o ajuste)
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

    # Ajusta as colunas para exibição
    df = df[['Fazenda', 'Classe', 'Equip', 'Custo Orçado', 'Custo Realizado', 'Custo Dif', 
             'Total Orçado', 'Total Realizado', 'Total Dif', 'Sinalizador']]

    # Arredonda valores numéricos
    df.update(df.select_dtypes(include=['float', 'int']).round(0))
    
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

st.subheader("Perguntas sobre os dados apresentados")
user_question = st.text_area("Digite sua pergunta:", height=100, key="auto_expanding_textarea", max_chars=None)
if st.button("Perguntar ao GROQ"):
    if user_question:
        combined_data = {"filtered_data": df.to_dict(orient='records'), "additional_data": additional_data}
        answer = query_groq(combined_data, user_question)
        st.subheader("")
        st.markdown(answer, unsafe_allow_html=False)
    else:
        st.warning("Por favor, insira uma pergunta.")
