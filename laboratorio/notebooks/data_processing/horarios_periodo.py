import pandas as pd
import plotly.express as px

# =========================================================
# 1) Ler e normalizar colunas
# =========================================================
df = pd.read_csv("horarios_periodo.csv", encoding="utf-8", delimiter=";")
df.columns = df.columns.str.strip()

# =========================================================
# 2) Converter datas e horários
#    -> DATA_CONSUMO no formato DD/MM/YYYY
#    -> HORA_INICIAL e HORA_FINAL no formato HH:MM:SS
# =========================================================
df["DATA_CONSUMO"] = pd.to_datetime(df["DATA_CONSUMO"], format="%d/%m/%Y")
df["HORA_INICIAL"] = pd.to_datetime(df["HORA_INICIAL"], format="%H:%M:%S")
df["HORA_FINAL"]   = pd.to_datetime(df["HORA_FINAL"],   format="%H:%M:%S")

# =========================================================
# 3) Agrupar por (CURRAL, DATA_CONSUMO) e calcular a duração
# =========================================================
df_daily = df.groupby(["CURRAL", "DATA_CONSUMO"]).agg(
    PRIMEIRO_TRATO=("HORA_INICIAL", "min"),
    ULTIMO_TRATO=("HORA_FINAL",   "max")
).reset_index()

# Converte para horas decimais e calcula a diferença
df_daily["PRIMEIRO_TRATO_DECIMAL"] = (
    df_daily["PRIMEIRO_TRATO"].dt.hour 
    + df_daily["PRIMEIRO_TRATO"].dt.minute / 60
)
df_daily["ULTIMO_TRATO_DECIMAL"] = (
    df_daily["ULTIMO_TRATO"].dt.hour 
    + df_daily["ULTIMO_TRATO"].dt.minute / 60
)
df_daily["DURACAO"] = (
    df_daily["ULTIMO_TRATO_DECIMAL"] 
    - df_daily["PRIMEIRO_TRATO_DECIMAL"]
)

# =========================================================
# 4) Gráfico facetado e ordenação dos currais
# =========================================================
currais_ordenados = sorted(df_daily["CURRAL"].unique())

fig = px.line(
    df_daily,
    x="DATA_CONSUMO",
    y="DURACAO",
    color="CURRAL",
    facet_col="CURRAL",
    facet_col_wrap=4,
    category_orders={"CURRAL": currais_ordenados},
    title="Variação da Duração dos Tratos por Curral (Faixa Ideal: 8h a 10h)"
)

# Unificar o eixo X e formatar rótulos das datas (DD/MM) com fonte menor
fig.update_xaxes(
    matches='x', 
    tickformat='%d/%m', 
    tickfont=dict(size=10)
)

# =========================================================
# 5) Destacar faixa de 8 a 10 horas em cada subplot
# =========================================================
min_data = df_daily["DATA_CONSUMO"].min()
max_data = df_daily["DATA_CONSUMO"].max()

for i, curral in enumerate(currais_ordenados, start=1):
    xref = "x" if i == 1 else f"x{i}"
    yref = "y" if i == 1 else f"y{i}"
    fig.add_shape(
        type="rect",
        xref=xref, yref=yref,
        x0=min_data, x1=max_data,
        y0=8,        y1=10,
        fillcolor="rgba(50,205,50,0.3)",  # verde claro
        line_width=0,
        layer="below"
    )

# Ajustes finais
fig.update_layout(
    hovermode="x unified",
    height=900,
    showlegend=False
)

# Rotular melhor o eixo Y
fig.update_yaxes(title_text="Duração (horas)")

# Mostrar o gráfico
fig.show()
