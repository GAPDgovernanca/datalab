import streamlit as st
import pandas as pd
import plotly.express as px
import re

# =========================================================
# 1) Ler e preparar dados
# =========================================================
@st.cache_data
def carregar_dados():
    # Carregar o arquivo
    df = pd.read_csv("horarios.csv", encoding="utf-8", delimiter=";")
    df.columns = df.columns.str.strip()

    # Converter datas e horários
    df["DATA_CONSUMO"] = pd.to_datetime(df["DATA_CONSUMO"], format="%d/%m/%Y")
    df["HORA_INICIAL"] = pd.to_datetime(df["HORA_INICIAL"], format="%H:%M:%S")
    df["HORA_FINAL"] = pd.to_datetime(df["HORA_FINAL"], format="%H:%M:%S")

    # Agrupar por curral e data
    df_daily = df.groupby(["CURRAL", "DATA_CONSUMO"]).agg(
        PRIMEIRO_TRATO=("HORA_INICIAL", "min"),
        ULTIMO_TRATO=("HORA_FINAL", "max")
    ).reset_index()

    # Converter horários para formato decimal e calcular duração
    df_daily["PRIMEIRO_TRATO_DECIMAL"] = df_daily["PRIMEIRO_TRATO"].dt.hour + df_daily["PRIMEIRO_TRATO"].dt.minute / 60
    df_daily["ULTIMO_TRATO_DECIMAL"] = df_daily["ULTIMO_TRATO"].dt.hour + df_daily["ULTIMO_TRATO"].dt.minute / 60
    df_daily["DURACAO"] = df_daily["ULTIMO_TRATO_DECIMAL"] - df_daily["PRIMEIRO_TRATO_DECIMAL"]

    # Adicionar colunas adicionais para detalhes no clique
    df_daily["HORARIO_INICIAL"] = df_daily["PRIMEIRO_TRATO"].dt.strftime("%H:%M:%S")
    df_daily["HORARIO_FINAL"] = df_daily["ULTIMO_TRATO"].dt.strftime("%H:%M:%S")

    return df_daily


# Função para extrair número do curral
def extrair_numero(curral):
    num = re.search(r'\d+', curral)
    return int(num.group()) if num else float('inf')


# Função para criar a abreviação correta
def criar_abreviacao(curral):
    match = re.match(r'([A-Z]+)-(\d+)', curral)  # Captura o prefixo e o número
    if match:
        prefixo, numero = match.groups()
        return f"{prefixo[0]}{numero}"  # Usa apenas a primeira letra do prefixo e o número
    return curral  # Se não corresponder ao padrão, retorna o curral original


# =========================================================
# 2) Configuração inicial
# =========================================================
df_daily = carregar_dados()

# Ordenar currais e criar abreviações
currais_originais = sorted(set(df_daily["CURRAL"].unique()), key=extrair_numero)  # Ordem alfanumérica
currais_abreviados = {c: criar_abreviacao(c) for c in currais_originais}
df_daily["CURRAL_ABREV"] = df_daily["CURRAL"].map(currais_abreviados)

# Range de datas
data_min = df_daily["DATA_CONSUMO"].min()
data_max = df_daily["DATA_CONSUMO"].max()

# =========================================================
# 3) Interface do Streamlit
# =========================================================
st.title("Análise da Duração dos Tratos")
st.sidebar.header("Filtros")

# Filtro de período (evita erro de valores insuficientes)
date_range = st.sidebar.date_input(
    "Selecione o Período:",
    value=[data_min, data_max],  # Sempre inicia com duas datas
    min_value=data_min,
    max_value=data_max,
    key="date_range"
)

# Verifica se a seleção retornou apenas uma data ou um intervalo
if isinstance(date_range, tuple) or isinstance(date_range, list):  # Verifica se é uma lista ou tupla
    if len(date_range) == 2:
        data_inicio, data_fim = date_range
    else:
        data_inicio = data_fim = date_range[0]  # Se só uma data for selecionada, usamos a mesma para início e fim
else:
    data_inicio = data_fim = date_range  # Se for um único valor, aplica para início e fim


# Filtro de currais (ordenado alfanumericamente)
st.sidebar.write("Selecione os Currais:")
currais_selecionados = st.sidebar.multiselect(
    "Currais:",
    options=currais_originais,
    default=currais_originais[:5],
    format_func=lambda x: currais_abreviados[x]  # Exibe abreviações no dropdown
)

# =========================================================
# 4) Processar dados filtrados
# =========================================================
# Converter para pandas datetime
data_inicio = pd.to_datetime(data_inicio)
data_fim = pd.to_datetime(data_fim)

# Filtrar dados
df_filtrado = df_daily[
    (df_daily["DATA_CONSUMO"] >= data_inicio) &
    (df_daily["DATA_CONSUMO"] <= data_fim) &
    (df_daily["CURRAL"].isin(currais_selecionados))
]

# =========================================================
# 5) Exibir o gráfico
# =========================================================
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para o período ou currais selecionados.")
else:
    # Criar gráfico com dados filtrados
    fig = px.line(
        df_filtrado,
        x="DATA_CONSUMO",
        y="DURACAO",
        color="CURRAL_ABREV",
        line_shape="spline",  # Suavizar linhas
        title="Duração dos Tratos no Período Selecionado",
        hover_data={"DURACAO": ":.2f"}  # Duração com duas casas decimais
    )
    fig.update_xaxes(tickformat="%d/%m")

    # Adicionar faixa 8-10h
    fig.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1,
        y0=8, y1=10,
        fillcolor="rgba(50,205,50,0.3)",
        layer="below",
        line_width=0
    )

    # Configurar layout para ocupar o máximo de espaço
    fig.update_layout(
        yaxis_title="Duração (horas)",
        hovermode="x unified",
        height=700,  # Altura do gráfico
        margin=dict(l=10, r=10, t=50, b=10)  # Margens reduzidas
    )

    st.plotly_chart(fig, use_container_width=True)  # Expandir até o limite disponível