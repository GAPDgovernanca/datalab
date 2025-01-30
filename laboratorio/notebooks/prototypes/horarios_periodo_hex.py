import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import numpy as np

# =========================================================
# 1. Ler e preparar os dados
# =========================================================
df = pd.read_csv("horarios.csv", encoding="utf-8", delimiter=";")
df.columns = df.columns.str.strip()

# Converter horários para formato decimal
df["HORA_INICIAL"] = pd.to_datetime(df["HORA_INICIAL"], format="%H:%M:%S")
df["HORA_FINAL"] = pd.to_datetime(df["HORA_FINAL"], format="%H:%M:%S")
df["HORARIO_INICIO_DECIMAL"] = df["HORA_INICIAL"].dt.hour + df["HORA_INICIAL"].dt.minute / 60
df["HORARIO_FINAL_DECIMAL"] = df["HORA_FINAL"].dt.hour + df["HORA_FINAL"].dt.minute / 60
df["DIFERENCA_HORAS"] = (df["HORA_FINAL"] - df["HORA_INICIAL"]).dt.total_seconds() / 3600

# Determinar valores MÍNIMO e MÁXIMO de horário inicial para o slider
horario_min = df["HORARIO_INICIO_DECIMAL"].min()
horario_max = df["HORARIO_INICIO_DECIMAL"].max()

# Criar os ticks do eixo Y (somente números inteiros com uma casa decimal)
yticks = np.round(np.arange(df["DIFERENCA_HORAS"].min(), df["DIFERENCA_HORAS"].max(), 0.5), 1)

# =========================================================
# 2. Criar a aplicação Dash
# =========================================================
app = Dash(__name__)
app.title = "Densidade Horária - Joinplot Hexbin"

app.layout = html.Div([
    html.H1("Gráfico de Densidade: Horário Inicial x Duração (Hexbin)"),
    
    # Intervalo de filtro para horários iniciais
    html.Div([
        html.Label("Filtrar por Horário Inicial:"),
        dcc.RangeSlider(
            id="horario-slider",
            min=horario_min,
            max=horario_max,
            step=0.5,
            value=[horario_min, horario_max],  # Começa no intervalo completo
            marks={i: f"{i:.1f}" for i in np.arange(horario_min, horario_max + 0.5, 1)}  # Exibe ticks a cada 1h
        ),
    ], style={"margin-bottom": "20px"}),

    # Gráfico de densidade
    dcc.Graph(id="grafico-hexbin"),
])

# =========================================================
# 3. Callback para atualizar o gráfico
# =========================================================
@app.callback(
    Output("grafico-hexbin", "figure"),
    Input("horario-slider", "value")
)
def atualizar_grafico(horario_range):
    """Filtra os dados e gera o gráfico Hexbin atualizado"""
    horario_min_sel, horario_max_sel = horario_range

    df_filtrado = df[
        (df["HORARIO_INICIO_DECIMAL"] >= horario_min_sel) & 
        (df["HORARIO_INICIO_DECIMAL"] <= horario_max_sel)
    ]

    if df_filtrado.empty:
        return px.line(title="Sem dados no período selecionado.")

    # Criar gráfico Hexbin com Plotly
    fig = px.density_heatmap(
        df_filtrado,
        x="HORARIO_INICIO_DECIMAL",
        y="DIFERENCA_HORAS",
        nbinsx=30,
        nbinsy=30,
        color_continuous_scale="Blues",
        title="Densidade de Duração x Horário Inicial",
    )

    # Ajustar rótulos e formatação
    fig.update_layout(
        xaxis_title="Horário Inicial (h)",
        yaxis_title="Duração (h)",
        coloraxis_colorbar=dict(title="Densidade"),
        height=700,
        hovermode="closest",
        yaxis=dict(tickmode="array", tickvals=yticks, tickformat=".1f")  # Definir escala do eixo Y
    )
    fig.update_traces(opacity=0.8)

    return fig

# =========================================================
# 4. Executar a aplicação
# =========================================================
if __name__ == "__main__":
    app.run_server(debug=True)
