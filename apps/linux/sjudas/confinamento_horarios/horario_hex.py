import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Nome do arquivo CSV
arquivo_dados = "horario_hex.csv"

# 1. Carregar os dados corretamente
df = pd.read_csv(arquivo_dados, encoding="utf-8", delimiter=";")
df.columns = df.columns.str.strip()  # Remover espaços extras nos nomes das colunas

# 2. Converter colunas de horário para formato datetime
df["HORA_INICIAL"] = pd.to_datetime(df["HORA_INICIAL"], format="%H:%M:%S")
df["HORA_FINAL"] = pd.to_datetime(df["HORA_FINAL"], format="%H:%M:%S")

# 3. Calcular a diferença entre o primeiro e o último trato para cada LOTE
df_diff = df.groupby("LOTE").agg(
    HORARIO_INICIO=("HORA_INICIAL", "first"),
    HORARIO_FINAL=("HORA_FINAL", "last")
).reset_index()

df_diff["DIFERENCA_HORAS"] = (df_diff["HORARIO_FINAL"] - df_diff["HORARIO_INICIO"]).dt.total_seconds() / 3600  # Converter para horas
df_diff["HORARIO_INICIO_DECIMAL"] = df_diff["HORARIO_INICIO"].dt.hour + df_diff["HORARIO_INICIO"].dt.minute / 60

# 4. Remover outliers usando o método do IQR (Intervalo Interquartil)
Q1 = df_diff["DIFERENCA_HORAS"].quantile(0.25)
Q3 = df_diff["DIFERENCA_HORAS"].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
df_diff = df_diff[(df_diff["DIFERENCA_HORAS"] >= limite_inferior) & (df_diff["DIFERENCA_HORAS"] <= limite_superior)]

# 5. Criar JointPlot com estilo Hexbin
sns.set_theme(style="whitegrid")
g = sns.jointplot(
    data=df_diff,
    x="HORARIO_INICIO_DECIMAL",
    y="DIFERENCA_HORAS",
    kind="hex",  # Tipo Hexbin
    height=8,
    marginal_kws=dict(bins=30, fill=True, kde=False),  # Configurar marginais
    space=0.1,  # Ajustar o espaço entre os gráficos
    color="blue"  # Cor do hexbin
)

# 6. Ajustar rótulos dos eixos
g.set_axis_labels("Horário Inicial (h)", "Duração (h)", fontsize=12)

# 7. Melhorar granularidade e exibir apenas uma casa decimal nos eixos X e Y
g.ax_joint.set_xticks(np.round(np.linspace(df_diff["HORARIO_INICIO_DECIMAL"].min(), df_diff["HORARIO_INICIO_DECIMAL"].max(), 10), 1))  # 10 divisões no eixo X
g.ax_joint.set_yticks(np.round(np.linspace(df_diff["DIFERENCA_HORAS"].min(), df_diff["DIFERENCA_HORAS"].max(), 10), 1))  # Eixo Y com 1 casa decimal

# 8. Criar manualmente a barra de cores para o Hexbin
hexbin = g.ax_joint.collections[0]  # Recuperar o objeto Hexbin
cb = plt.colorbar(hexbin, ax=g.ax_joint, pad=0.02)  # Criar barra de cor ao lado do gráfico
cb.set_label("Densidade", fontsize=12)   # Adicionar legenda da densidade
cb.ax.tick_params(labelsize=10)          # Ajustar tamanho dos rótulos

# 9. Melhorar histogramas marginais com cores diferentes
g.plot_marginals(sns.histplot, bins=30, kde=True, color="orange")  # Histogramas marginais em laranja

# 10. Ajustar transparência para evitar sobreposição no Hexbin
g.ax_joint.collections[0].set_alpha(0.8)

# 11. Adicionar linha de tendência
x_vals = df_diff["HORARIO_INICIO_DECIMAL"]
y_vals = df_diff["DIFERENCA_HORAS"]
slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
g.ax_joint.plot(x_vals, slope * x_vals + intercept, color="red", linestyle="--", linewidth=2, label="Tendência")
g.ax_joint.legend()

# 12. Exibir o gráfico
plt.show()
