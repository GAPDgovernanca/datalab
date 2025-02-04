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
    .block-container { padding-top: 2rem; } /* Ajuste do espaço acima do cabeçalho */
    .custom-card {
        background-color: #2c3e50;  /* Fundo mais escuro para contraste */
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #34495e;  /* Cor da borda combinando */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);  /* Sombra para destaque */
        text-align: center;
        margin-bottom: 10px;
        color: #ecf0f1;  /* Texto claro para contraste */
    }
    .custom-card p {
        font-size: 28px; /* Aumento da fonte dos dados */
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
        color: #ecf0f1;  /* Cor clara para contraste */
    }
    .custom-header {
        color: #ecf0f1; /* Contraste claro */
        font-size: 28px;
        font-weight: bold;
    }
    .custom-subheader {
        color: #bdc3c7; /* Texto mais suave para subcabeçalhos */
        font-size: 20px;
    }
    .stDataFrame div[data-testid="stHorizontalBlock"] {
        width: auto !important;
        min-width: 150px !important; /* Ajuste para largura adequada */
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
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Função para conectar ao banco SQLite
def get_db_connection():
    try:
        conn = sqlite3.connect("./frota.db")
        conn.row_factory = sqlite3.Row  # Garante que os dados retornem como dicionário
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter os valores mínimos e máximos das datas
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

def clean_date(date_str):
    """Remove a parte da hora e converte para YYYY-MM-DD."""
    return date_str.split()[0] if date_str else None

def get_latest_reference_date():
    """Obtém a data de referência mais recente no banco de dados e remove a hora."""
    conn = get_db_connection()
    if not conn:
        return "unknown_date"

    query = "SELECT MAX(data_referencia) FROM fato_custo"
    
    try:
        result = conn.execute(query).fetchone()
        conn.close()
        return clean_date(result[0]) if result and result[0] else "unknown_date"
    except Exception as e:
        st.error(f"Erro ao obter a última data de referência: {e}")
        return "unknown_date"

def get_latest_processing_date():
    """Obtém a data de processamento mais recente no banco de dados e remove a hora."""
    conn = get_db_connection()
    if not conn:
        return "unknown_date"

    query = "SELECT MAX(data_processamento) FROM fato_custo"
    
    try:
        result = conn.execute(query).fetchone()
        conn.close()
        return clean_date(result[0]) if result and result[0] else "unknown_date"
    except Exception as e:
        st.error(f"Erro ao obter a última data de processamento: {e}")
        return "unknown_date"

def calculate_proportion_factor(latest_reference_date, latest_date):
    """
    Calcula o fator de proporção com base no período disponível dos dados.

    Parâmetros:
    - latest_reference_date (str): Data de referência inicial no formato 'YYYY-MM-DD'.
    - latest_date (str): Data final do período de análise no formato 'YYYY-MM-DD'.

    Retorna:
    - float: Fator de proporção ajustado (entre 0 e 1).
    """
    try:
        ref_date = datetime.strptime(latest_reference_date, "%Y-%m-%d")
        last_date = datetime.strptime(latest_date, "%Y-%m-%d")
        
        # Calcula os meses decorridos entre a data de referência e a data mais recente
        months_elapsed = (last_date.year - ref_date.year) * 12 + (last_date.month - ref_date.month)

        # Ajusta o fator para ficar no intervalo de 0 a 1 (máximo de 12 meses)
        proportion_factor = min(months_elapsed / 12, 1.0) if months_elapsed > 0 else 1.0

        return round(proportion_factor, 4)  # Retorna com 4 casas decimais para precisão
    except Exception as e:
        print(f"Erro ao calcular fator de proporção: {e}")
        return 1.0  # Fallback para evitar erros

# Função para processar perguntas usando GROQ AI

def query_groq(data_json, question, model_name="deepseek-r1-distill-llama-70b"):
    try:
        # Obtém a data mais recente de processamento antes de definir o prompt
        latest_date = get_latest_processing_date()
        latest_reference_date = get_latest_reference_date()
        proportion_factor = calculate_proportion_factor(latest_reference_date, latest_date)

        prompt = f"""
        Você é um especialista em gestão de frota agrícola, com foco em análise financeira e cálculos de eficiência operacional.

        Regras para Representação Numérica:

        - Acima de 1.000: arredondar para a centena mais próxima (12.345 → 12.300)
        - Abaixo de 1.000: arredondar para a dezena mais próxima (545 → 550)
        - Manter consistência em tabelas
        - Evitar casas decimais desnecessárias

        Estrutura da Resposta:

        1. Iniciar com a principal conclusão
        2. Apresentar cálculos de suporte
        3. Utilizar indicadores (🟢, 🔴, ⚠️) para destaque
        4. Usar tabelas para múltiplos pontos de dados

        5. Definições Temporais:

            - **Valores Estimados (B_anual)**: Representa a soma total estimada para um ciclo completo de safra (abril a abril).
            - **Valores Estimados Ajustados (B_escalado)**: Todo valor estimado deve ser ajustado proporcionalmente ao período analisado ({latest_reference_date} até {latest_date}), aplicando o fator de proporção:  
                B_escalado = B_anual * {proportion_factor}
                Esse ajuste é **obrigatório** para garantir comparabilidade.
            - **Uso Estimado na tabela fato_uso**: O campo **uso_estimado** deve ser ajustado proporcionalmente ao período analisado ({latest_reference_date} até {latest_date}), aplicando o fator de proporção:  
                B_escalado = B_anual * {proportion_factor}
                Esse ajuste é **obrigatório** para garantir comparabilidade.
            - **Valores Reais (A_realizado)**: Representa os valores efetivamente registrados entre abril e {latest_date}. **Os valores realizados devem ser usados diretamente, sem qualquer ajuste ou modificação.**

        6. Cálculos Principais:

            - **Diferença Absoluta**:  
            Delta = A_realizado - B_escalado  

            - **Desvio Percentual**:  
            Delta% = ((A_realizado - B_escalado) / B_escalado) * 100  

            - **Taxa de Utilização**:  
            U = Uso_Realizado / Uso_Estimado  
            Se Uso_Estimado = 0, então U = 0.0  
            - U > 1.0 → Superutilização 🟢  
            - U < 1.0 → Subutilização 🔴  

        7. Tabelas do Banco de Dados:

        - **dim_equipamento (Equipamentos)**  
        - id_equipamento, modelo, usuário, classe, data_criação  

        - **fato_uso (Uso)**  
        - id_equipamento, uso_estimado, uso_realizado, uso_diferença, data_referência  

        - **fato_custo (Custo)**  
        - id_equipamento, custo_hora_estimado/realizado, total_estimado/realizado, data_referência  

        - **fato_combustivel (Combustível)**  
        - id_equipamento, comb_litros_estimado/realizado, comb_valor_unitario_estimado/realizado, comb_total_estimado/realizado  

        - **fato_manutencao (Manutenção)**  
        - id_equipamento, lubrificantes, filtros, graxas, peças_serviços (estimado/realizado para cada)  

        - **fato_reforma (Reforma)**  
        - id_equipamento, reforma_estimado, reforma_realizado, data_referência  

        8. Relacionamentos:

        - Todas as tabelas fato se conectam à **dim_equipamento** via **id_equipamento**

        9. Diretrizes:

        - Escrever em português brasileiro
        - Focar em insights baseados em dados
        - Maximizar a densidade informacional

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

        # Removendo tokens desnecessários da resposta (somente se necessário)
        if "<think>" in response and "</think>" in response:
            cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        else:
            cleaned_response = response

        # Ajuste para garantir que a resposta sempre comece com um relatório de conclusões sem cabeçalhos
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
        return sorted(df[column_name].dropna().tolist())  # Ordenar os valores alfabeticamente
    except Exception as e:
        st.error(f"Erro ao carregar valores únicos para {column_name}: {e}")
        return []

# Função para aplicar sinalizadores visuais
def apply_flags(df):
    def flag_diferenca(row):
        percentual = (row['total_diferenca'] / row['total_estimado'] * 100) if row['total_estimado'] != 0 else 0
        
        if percentual > 10:  # Agora um percentual positivo é algo bom
            return '🟢'  # Verde = Economia
        elif percentual < -10:  # Um percentual negativo significa prejuízo
            return '🔴'  # Vermelho = Prejuízo
        else:
            return '⚪'

    if 'total_diferenca' in df.columns:
        df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df

def calcular_multiplicadores(df, proportion_factor):
    """
    Calcula os multiplicadores apenas se os dados necessários estiverem disponíveis.
    """
    try:
        # Create a connection to get uso data
        conn = get_db_connection()
        if conn:
            # Get uso data for the same equipments in df
            uso_query = """
                SELECT id_equipamento, uso_estimado, uso_realizado 
                FROM fato_uso 
                WHERE id_equipamento IN ({})
            """.format(','.join(map(str, df['id_equipamento'].unique())))
            
            uso_df = pd.read_sql_query(uso_query, conn)
            conn.close()
            
            # Merge uso data with main df
            df = df.merge(uso_df, left_on='id_equipamento', right_on='id_equipamento', how='left')
        
        # Calculate only if we have the required columns
        if 'uso_estimado' in df.columns and 'uso_realizado' in df.columns:
            df['uso_estimado_ajustado'] = df['uso_estimado'] * proportion_factor
            df['Taxa Utilização Multiplicador'] = df.apply(
                lambda row: row['uso_realizado'] / row['uso_estimado_ajustado']
                if row['uso_estimado_ajustado'] != 0 else 0.0,
                axis=1
            )
        
        if 'Total Orçado' in df.columns and 'Total Realizado' in df.columns:
            df['total_estimado_ajustado'] = df['Total Orçado'] * proportion_factor
            df['Consumo Multiplicador'] = df.apply(
                lambda row: row['Total Realizado'] / row['total_estimado_ajustado']
                if row['total_estimado_ajustado'] != 0 else 0.0,
                axis=1
            )
        
        return df
        
    except Exception as e:
        print(f"Erro ao calcular multiplicadores: {e}")
        return df

# Título principal
st.markdown('<h1 class="centered-title">Frota - Dashboard Operacional</h1>', unsafe_allow_html=True)

# Obter datas padrão para inicialização
default_min_date, default_max_date = get_date_defaults()

# Sidebar - Filtros
date_range = st.sidebar.date_input("Data de Referência", [default_min_date, default_max_date])
usuarios_opcoes = ["Todos"] + get_unique_values("usuario")  # Adiciona "Todos" às opções
usuario = st.sidebar.multiselect("Unidade", usuarios_opcoes, default=["Todos"])

classes_opcoes = ["Todos"] + get_unique_values("classe")  # Adiciona "Todos" às opções
classe = st.sidebar.multiselect("Classe", classes_opcoes, default=["Todos"])

id_equipamento = st.sidebar.text_input("IDs de Equipamento (separados por vírgula)")

# Montar filtros
filtros = {
    "data_referencia": date_range if date_range else None,
    "id_equipamento": [int(x) for x in id_equipamento.split(',')] if id_equipamento else None,
    "classe": classe if classe != "Todos" else None,
    "usuario": usuario if usuario != "Todos" else None,
}

# Carregar dados filtrados
df = get_filtered_data(filtros)

# Carregar dados adicionais para IA
additional_data = get_additional_data(filtros)

# Verificar se os dados retornaram resultados
if df.empty:
    st.warning("Nenhum dado encontrado para os filtros aplicados. Verifique os parâmetros.")

# Obter as datas de referência ANTES de calcular o fator de proporção
latest_reference_date = get_latest_reference_date()
latest_date = get_latest_processing_date()

# Calcular o fator de proporção
proportion_factor = calculate_proportion_factor(latest_reference_date, latest_date)

# Exibir métricas
st.markdown('<div class="card-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="custom-card"><h3>Total de Registros</h3><p>{len(df):,}</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="custom-card"><h3>Total Estimado</h3><p>R$ {df["total_estimado"].sum() if "total_estimado" in df.columns else 0:,.0f}</p></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if not df.empty:
    # Preparar dados para o gráfico
    chart_data = df.copy()
    
    # Tratar divisões por zero nos cálculos
    chart_data['Taxa Utilização Multiplicador'] = chart_data.apply(
        lambda row: row['custo_hora_realizado'] / row['custo_hora_estimado'] if row['custo_hora_estimado'] != 0 else 0,
        axis=1
    )
    chart_data['Consumo Multiplicador'] = chart_data.apply(
        lambda row: row['total_realizado'] / row['total_estimado'] if row['total_estimado'] != 0 else 0,
        axis=1
    )
    
    # Criar DataFrame para plotagem
    plot_data = pd.DataFrame({
        'equipamento': chart_data['id_equipamento'].astype(str),  # Garante que seja tratado como string
        'Uso vs Planejado': chart_data['Taxa Utilização Multiplicador'],
        'Consumo vs Planejado': chart_data['Consumo Multiplicador']
    })

    # Criar gráfico interativo com Plotly
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
    
    # Aqui o layout do gráfico é atualizado para tratar ID_EQUIPAMENTO como nome próprio
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_type='category',  # Força o eixo X como categórico
        legend_title_text='Indicadores',
        yaxis_title="Multiplicador (Realizado/Planejado)",
        hovermode="x unified"
    )
    
    # Adicionar linha de referência e ajustar layout
    fig.add_hline(
        y=1, 
        line_dash="dot", 
        line_color="red",
        annotation_text="Planejado (1.0)", 
        annotation_position="bottom right"
    )
    
    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    try:
        from streamlit.components.v1 import html
        # html(chart_component, height=400)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader("Dados filtrados")
if not df.empty:
    df = apply_flags(df)
    # Aplicar sinalizadores visuais e calcular multiplicadores com o proportion_factor correto
    df = calcular_multiplicadores(df, proportion_factor)



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

    # Inverter sinais na apresentação final (se necessário)
    df['Custo Dif'] = df['Custo Dif']
    df['Total Dif'] = df['Total Dif']

    df = df[['Fazenda', 'Classe', 'Equip', 'Custo Orçado', 'Custo Realizado', 'Custo Dif', 
             'Total Orçado', 'Total Realizado', 'Total Dif', 'Sinalizador']]

    # Formatar os valores monetários e ajustar o estilo da tabela
    df.update(df.select_dtypes(include=['float', 'int']).round(0))
    styled_df = df.style.format({
        'Custo Orçado': 'R$ {:,.0f}',
        'Custo Realizado': 'R$ {:,.0f}',
        'Custo Dif': 'R$ {:,.0f}',
        'Total Orçado': 'R$ {:,.0f}',
        'Total Realizado': 'R$ {:,.0f}',
        'Total Dif': 'R$ {:,.0f}'
    }).set_table_styles([
        # Layout fixo e estilos gerais
        {'selector': 'table', 'props': [('table-layout', 'fixed'), ('width', '150%')]},
        {'selector': 'th, td', 'props': [('text-align', 'center'), ('padding', '10px')]},

        # Larguras específicas para cada coluna (cabeçalho + dados)
        {'selector': 'th:nth-child(1), td:nth-child(1)', 'props': [('width', '150px')]},  # Fazenda
        {'selector': 'th:nth-child(2), td:nth-child(2)', 'props': [('width', '120px')]},  # Classe
        {'selector': 'th:nth-child(3), td:nth-child(3)', 'props': [('width', '100px')]},  # Equip
        {'selector': 'th:nth-child(n+4), td:nth-child(n+4)', 'props': [('width', '300px')]},  # Colunas numéricas
        {'selector': 'th:last-child, td:last-child', 'props': [('width', '60px')]}  # Sinalizador
    ])

    st.dataframe(styled_df)

# Seção para perguntas ao modelo AI
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
