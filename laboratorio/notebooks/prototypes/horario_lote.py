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

    # Agrupar por lote, curral e data
    df_daily = df.groupby(["LOTE", "CURRAL", "DATA_CONSUMO"]).agg(
        PRIMEIRO_TRATO=("HORA_INICIAL", "min"),
        ULTIMO_TRATO=("HORA_FINAL", "max")
    ).reset_index()

    # Converter horários para formato decimal e calcular duração
    df_daily["PRIMEIRO_TRATO_DECIMAL"] = df_daily["PRIMEIRO_TRATO"].dt.hour + df_daily["PRIMEIRO_TRATO"].dt.minute / 60
    df_daily["ULTIMO_TRATO_DECIMAL"] = df_daily["ULTIMO_TRATO"].dt.hour + df_daily["ULTIMO_TRATO"].dt.minute / 60
    df_daily["DURACAO"] = df_daily["ULTIMO_TRATO_DECIMAL"] - df_daily["PRIMEIRO_TRATO_DECIMAL"]

    return df_daily


# Função para extrair número do lote
def extrair_numero(lote):
    num = re.search(r'\d+', str(lote))  # Garantir que lote seja string
    return int(num.group()) if num else float('inf')


# Função para criar a abreviação dos lotes (pegar apenas os 3 últimos dígitos)
def abreviar_lote(lote):
    return str(lote)[-3:]  # Mantém os últimos 3 dígitos


# =========================================================
# 2) Configuração inicial
# =========================================================
df_daily = carregar_dados()

# Ordenar lotes e criar abreviações
lotes_originais = sorted(set(df_daily["LOTE"].unique()), key=extrair_numero)  # Ordem alfanumérica
lotes_abreviados = {l: abreviar_lote(l) for l in lotes_originais}  # 11157 → 157
df_daily["LOTE_ABREV"] = df_daily["LOTE"].map(lotes_abreviados)

# Range de datas
data_min = df_daily["DATA_CONSUMO"].min()
data_max = df_daily["DATA_CONSUMO"].max()

# =========================================================
# 3) Interface do Streamlit
# =========================================================
st.title("Análise da Duração dos Tratos por Lote")
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

# Filtro de lotes (ordenado alfanumericamente)
st.sidebar.write("Selecione os Lotes:")
lotes_selecionados = st.sidebar.multiselect(
    "Lotes:",
    options=lotes_originais,
    default=lotes_originais[:5],
    format_func=lambda x: lotes_abreviados[x]  # Exibe apenas os últimos 3 dígitos no dropdown
)

# =========================================================
# 4) Processar dados filtrados
# =========================================================
# Garantir que data_inicio e data_fim estejam no mesmo formato que DATA_CONSUMO
data_inicio = pd.to_datetime(data_inicio).tz_localize(None)
data_fim = pd.to_datetime(data_fim).tz_localize(None)

# Filtrar dados
df_filtrado = df_daily[
    (df_daily["DATA_CONSUMO"] >= data_inicio) &
    (df_daily["DATA_CONSUMO"] <= data_fim) &
    (df_daily["LOTE"].isin(lotes_selecionados))
]

# =========================================================
# 5) Exibir o gráfico
# =========================================================
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para o período ou lotes selecionados.")
else:
    # Criar gráfico com dados filtrados
    fig = px.line(
        df_filtrado,
        x="DATA_CONSUMO",
        y="DURACAO",
        color="LOTE_ABREV",
        line_shape="spline",  # Suavizar linhas
        title="Duração dos Tratos no Período Selecionado",
        hover_data={
            "DURACAO": ":.2f",  # Duração com duas casas decimais
            "CURRAL": True,     # Adiciona o CURRAL ao tooltip
            "DATA_CONSUMO": "|%d/%m/%Y"  # Formato da data
        }
    )
    fig.update_xaxes(tickformat="%d/%m")  # Exibe datas no formato DD/MM

    # Adicionar faixa visual de 8h-10h no gráfico
    fig.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, x1=1,
        y0=8, y1=10,
        fillcolor="rgba(50,205,50,0.3)",
        layer="below",
        line_width=0
    )

    # Configurar layout do gráfico
    fig.update_layout(
        yaxis_title="Duração (horas)",
        hovermode="x unified",
        height=700,  # Altura do gráfico
        margin=dict(l=10, r=10, t=50, b=10)  # Margens reduzidas
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
