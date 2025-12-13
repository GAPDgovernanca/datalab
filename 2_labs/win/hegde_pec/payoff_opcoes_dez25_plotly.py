import numpy as np
from openpyxl import load_workbook
import plotly.graph_objects as go

# =====================================
# CONFIGURAÇÃO
# =====================================
EXCEL_FILE = "Planilha Hedge.xlsx"
SHEET = "Base"
N_POINTS = 400

# =====================================
# FUNÇÕES
# =====================================
def read(ws, cell):
    return float(ws[cell].value)

def payoff(S, K, premium, opt_type, position):
    if opt_type == "call":
        intrinsic = max(S - K, 0)
    else:
        intrinsic = max(K - S, 0)

    if position == "short":
        return premium - intrinsic
    else:
        return intrinsic - premium

def payoff_curve(S, K, premium, opt_type, position):
    return [payoff(s, K, premium, opt_type, position) for s in S]

def weighted_avg(curves, weights):
    weights = np.abs(np.array(weights))
    curves = np.array(curves)
    return (curves.T @ weights) / weights.sum()

# =====================================
# LEITURA DA PLANILHA
# =====================================
wb = load_workbook(EXCEL_FILE, data_only=True)
ws = wb[SHEET]

# PUT Dez/25
put_legs = [
    ("Put EB", read(ws,"EB1"), read(ws,"EB14"), read(ws,"EB7")),
    ("Put EH", read(ws,"EH1"), read(ws,"EH14"), read(ws,"EH7")),
]

# CALL Dez/25
call_legs = [
    ("Call EE", read(ws,"EE1"), read(ws,"EE14"), read(ws,"EE7")),
    ("Call EK", read(ws,"EK1"), read(ws,"EK14"), read(ws,"EK7")),
]

spot = read(ws,"AV2")
strikes = [l[1] for l in put_legs + call_legs]

# =====================================
# DOMÍNIO DE PREÇO
# =====================================
S_min = min(strikes + [spot]) - 80
S_max = max(strikes + [spot]) + 80
S = np.linspace(S_min, S_max, N_POINTS)

# =====================================
# CURVAS
# =====================================
put_curves = []
put_weights = []

for name, K, prem, cts in put_legs:
    pos = "short" if cts < 0 else "long"
    put_curves.append(payoff_curve(S, K, prem, "put", pos))
    put_weights.append(cts)

call_curves = []
call_weights = []

for name, K, prem, cts in call_legs:
    pos = "short" if cts < 0 else "long"
    call_curves.append(payoff_curve(S, K, prem, "call", pos))
    call_weights.append(cts)

put_agg = weighted_avg(put_curves, put_weights)
call_agg = weighted_avg(call_curves, call_weights)
net_agg = put_agg + call_agg

# =====================================
# GRÁFICO BASE
# =====================================
fig = go.Figure()

for i, leg in enumerate(put_legs):
    fig.add_trace(go.Scatter(
        x=S, y=put_curves[i],
        name=leg[0],
        visible=True
    ))

for i, leg in enumerate(call_legs):
    fig.add_trace(go.Scatter(
        x=S, y=call_curves[i],
        name=leg[0],
        visible=True
    ))

fig.add_trace(go.Scatter(
    x=S, y=put_agg,
    name="PUT agregado",
    line=dict(width=4)
))

fig.add_trace(go.Scatter(
    x=S, y=call_agg,
    name="CALL agregado",
    line=dict(width=4)
))

fig.add_trace(go.Scatter(
    x=S, y=net_agg,
    name="NET (PUT + CALL)",
    line=dict(width=5)
))

# =====================================
# SLIDER (linha vertical móvel)
# =====================================
steps = []
for s in S:
    steps.append({
        "method": "update",
        "args": [
            {},
            {"shapes": [{
                "type": "line",
                "x0": s, "x1": s,
                "y0": min(net_agg) - 5,
                "y1": max(net_agg) + 5,
                "line": {"color": "red", "width": 2}
            }]}
        ],
        "label": f"{round(s,1)}"
    })

fig.update_layout(
    sliders=[{
        "active": int(len(steps)/2),
        "currentvalue": {"prefix": "Preço (R$/@): "},
        "pad": {"t": 50},
        "steps": steps
    }],
    title="Payoff por @ – Opções Dez/25 (Put + Call)",
    xaxis_title="Preço do boi (R$/@)",
    yaxis_title="Payoff (R$/@)",
    hovermode="x unified"
)

# Linhas de strike
for k in strikes:
    fig.add_vline(x=k, line_dash="dash", opacity=0.4)

fig.add_hline(y=0, line_dash="dash")

fig.show()
