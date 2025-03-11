import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import math

# Log library version for debugging
import sys
print(f"Python version: {sys.version}")
print(f"Dash Bootstrap Components version: {dbc.__version__}")

# Functions for option calculations
def sigma_ef(xi):
    """
    Calculate effective volatility (σef) from the distance parameter (ξ)
    Formula: σef = sqrt(2*sqrt(1 + ξ²) - 2)
    """
    return np.sqrt(2 * np.sqrt(1 + xi**2) - 2)

def time_threshold(sigma_ef_pct, sigma_daily_pct):
    """
    Calculate time threshold (tr) in days
    tr = (σef / σdaily)²
    """
    # Convert percentages to decimals for calculation
    sigma_ef_decimal = sigma_ef_pct / 100.0
    sigma_daily_decimal = sigma_daily_pct / 100.0
    
    # Avoid division by zero
    if sigma_daily_decimal == 0:
        return float('inf')
    
    # Calculate tr
    return (sigma_ef_decimal / sigma_daily_decimal)**2

def calculate_xi(S, K, r, t):
    """
    Calculate ξ parameter based on distance from at-the-money
    """
    VP_K = K * np.exp(-r * t)
    # The value is normalized for better intuition
    xi = (S - VP_K) / ((S + VP_K)/2)
    return xi

# Initialize the Dash app with a modern Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}]
               )

# App title
app.title = "Option Horizon of Indecision Calculator"

# Define default values
S_default = 50
K_default = 50
r_default = 5.0  # percentage
t_default = 0.2  # years
sigma_daily_default = 2.37  # percentage

# App layout with Bootstrap components for a cleaner interface
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Option Horizon of Indecision Calculator", 
                   className="text-center my-4"),
            html.H4("Based on the formula: σef = √(2√(1+ξ²) - 2)", 
                   className="text-center mb-4 text-muted"),
        ], width=12)
    ]),
    
    # Main content area with graphs and controls
    dbc.Row([
        # Left side: Controls
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Option Parameters", className="text-center")),
                dbc.CardBody([
                    # Stock price - Using dbc.Row and dbc.Col instead of FormGroup
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Stock Price (S)", html_for="stock-price-slider"),
                            dcc.Slider(
                                id="stock-price-slider",
                                min=30,
                                max=70,
                                step=0.5,
                                value=S_default,
                                marks={i: str(i) for i in range(30, 71, 10)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Div(id="stock-price-display", className="text-muted text-center mt-1"),
                        ])
                    ], className="mb-3"),
                    
                    # Strike price - Using dbc.Row and dbc.Col instead of FormGroup
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Strike Price (K)", html_for="strike-price-slider"),
                            dcc.Slider(
                                id="strike-price-slider",
                                min=30,
                                max=70,
                                step=0.5,
                                value=K_default,
                                marks={i: str(i) for i in range(30, 71, 10)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Div(id="strike-price-display", className="text-muted text-center mt-1"),
                        ])
                    ], className="mb-3"),
                    
                    # Daily volatility - Using dbc.Row and dbc.Col instead of FormGroup
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Daily Volatility (%)", html_for="volatility-slider"),
                            dcc.Slider(
                                id="volatility-slider",
                                min=0.5,
                                max=5.0,
                                step=0.1,
                                value=sigma_daily_default,
                                marks={i: str(i) for i in range(1, 6)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            html.Div(id="volatility-display", className="text-muted text-center mt-1"),
                        ])
                    ], className="mb-3"),
                    
                    # Interest rate and Time to expiration
                    dbc.Row([
                        dbc.Col([
                            # Using dbc.Row and dbc.Col instead of FormGroup
                            dbc.Label("Risk-free Rate (%)"),
                            dbc.Input(
                                id="risk-free-rate-input",
                                type="number",
                                value=r_default,
                                min=0,
                                max=20,
                                step=0.1
                            ),
                        ], width=6),
                        dbc.Col([
                            # Using dbc.Row and dbc.Col instead of FormGroup
                            dbc.Label("Time to Expiration (years)"),
                            dbc.Input(
                                id="time-to-expiration-input",
                                type="number",
                                value=t_default,
                                min=0.01,
                                max=2,
                                step=0.01
                            ),
                        ], width=6),
                    ], className="mb-3"),
                    
                    # Reset button
                    dbc.Button(
                        "Reset to Defaults",
                        id="reset-button",
                        color="secondary",
                        className="mt-3 w-100"
                    ),
                ]),
            ], className="mb-4"),
            
            # Adicionar um switch para controlar a visibilidade da legenda
            dbc.Row([
                dbc.Col([
                    dbc.Label("Legend Visibility:"),
                    dbc.Switch(
                        id="legend-toggle",
                        label="Show Legend",
                        value=True,  # Inicialmente ligado
                        className="mt-1",
                    ),
                ], className="text-center mt-3"),
            ]),

            # Results Card
            dbc.Card([
                dbc.CardHeader(html.H4("Option Results", className="text-center")),
                dbc.CardBody([
                    html.Div(id="results-display"),
                    html.Hr(),
                    dbc.Alert([
                        html.H5("Glossary", className="alert-heading"),
                        html.P([
                            html.Strong("Horizon of Indecision (tr): "),
                            "The number of days before expiration when an option's behavior begins to differentiate."
                        ]),
                        html.P([
                            html.Strong("Distance parameter (ξ): "),
                            "Measures how far an option is from being at-the-money."
                        ]),
                        html.P([
                            html.Strong("Effective volatility (σef): "),
                            "Volatility needed for the option to differentiate its behavior."
                        ]),
                    ], color="info"),
                ]),
            ]),
        ], md=4, className="mb-4"),
        
        # Right side: Graphs
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Option Analysis Graphs", className="text-center")),
                dbc.CardBody([
                    dcc.Graph(
                        id="option-graphs",
                        config={"displayModeBar": True, "scrollZoom": True},
                        style={"height": "700px"},
                    ),
                ]),
            ]),
        ], md=8),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P(
                "This calculation follows the methodology from Chapter 4 of 'Options: Trading Volatility' discussing the characteristics of options near expiration.",
                className="text-center text-muted"
            ),
        ], width=12)
    ])
], fluid=True, className="p-3")

# Define callback to update the graphs and results
@app.callback(
    [Output("option-graphs", "figure"),
     Output("results-display", "children"),
     Output("stock-price-display", "children"),
     Output("strike-price-display", "children"),
     Output("volatility-display", "children")],
    [Input("stock-price-slider", "value"),
     Input("strike-price-slider", "value"),
     Input("volatility-slider", "value"),
     Input("risk-free-rate-input", "value"),
     Input("time-to-expiration-input", "value"),
     Input("legend-toggle", "value")]  # Novo input para o switch
)
def update_graphs_and_results(S, K, sigma_daily, r, t, show_legend):  # Adicionar parâmetro
    # Convert percentage to decimal for calculations
    r_decimal = r / 100.0
    
    # Calculate xi based on inputs
    xi = calculate_xi(S, K, r_decimal, t)
    
    # Calculate effective volatility and time threshold
    sigma_ef_val = sigma_ef(xi) * 100  # Convert to percentage
    tr_val = time_threshold(sigma_ef_val, sigma_daily)
    
    # Calculate present value of K for annotations
    PV_K = K * np.exp(-r_decimal * t)
    
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"colspan": 1}, {"colspan": 1}],
               [{"colspan": 2}, None]],
        subplot_titles=(
            "ξ vs Effective Volatility (σef)",
            "Effective Volatility vs Time Threshold (tr)",
            "Horizon of Indecision vs Strike Price"
        ),
        vertical_spacing=0.1,
    )
    
    # Plot 1: ξ vs σef
    xi_range = np.linspace(-0.3, 0.3, 500)
    sigma_ef_values = [sigma_ef(x) * 100 for x in xi_range]  # Convert to percentage
    
    fig.add_trace(
        go.Scatter(
            x=xi_range,
            y=sigma_ef_values,
            mode="lines",
            name="σef",
            line=dict(color="blue", width=3),
        ),
        row=1, col=1
    )
    
    # Add current point
    fig.add_trace(
        go.Scatter(
            x=[xi],
            y=[sigma_ef_val],
            mode="markers",
            name="Current Value",
            marker=dict(color="red", size=12, symbol="circle"),
            text=f"ξ = {xi:.4f}, σef = {sigma_ef_val:.2f}%",
            hoverinfo="text"
        ),
        row=1, col=1
    )
    
    # Plot 2: σef vs Time Threshold (tr)
    sigma_ef_range = np.linspace(0.1, 20, 500)
    tr_values = [time_threshold(s, sigma_daily) for s in sigma_ef_range]
    
    fig.add_trace(
        go.Scatter(
            x=sigma_ef_range,
            y=tr_values,
            mode="lines",
            name="Time Threshold",
            line=dict(color="green", width=3),
        ),
        row=1, col=2
    )
    
    # Add current point
    fig.add_trace(
        go.Scatter(
            x=[sigma_ef_val],
            y=[tr_val],
            mode="markers",
            marker=dict(color="red", size=12, symbol="circle"),
            text=f"σef = {sigma_ef_val:.2f}%, tr = {tr_val:.2f} days",
            hoverinfo="text",
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Plot 3: Moneyness visualization
    # Generate a range of K values around S
    K_range = np.linspace(0.6 * S, 1.4 * S, 500)
    
    # Calculate xi for each K
    xi_values = [calculate_xi(S, k, r_decimal, t) for k in K_range]
    
    # Calculate sigma_ef for each xi
    sigma_ef_values = [sigma_ef(x) * 100 for x in xi_values]
    
    # Calculate tr for each sigma_ef
    tr_values = [time_threshold(s, sigma_daily) for s in sigma_ef_values]
    
    # Plot tr vs K
    fig.add_trace(
        go.Scatter(
            x=K_range,
            y=tr_values,
            mode="lines",
            name="Horizon of Indecision",
            line=dict(color="purple", width=3),
        ),
        row=2, col=1
    )
    
    # Add vertical lines for S and K
    fig.add_vline(
        x=S, line_width=2, line_dash="solid", line_color="green",
        row=2, col=1
    )
    fig.add_vline(
        x=K, line_width=2, line_dash="dash", line_color="red",
        row=2, col=1
    )
    
    # Add shaded areas for in/out/at-the-money
    atm_range = 0.01  # Define what we consider "at-the-money" (±1%)
    
    # In-the-money area (green)
    fig.add_trace(
        go.Scatter(
            x=K_range[K_range < S],
            y=tr_values[:len(K_range[K_range < S])],
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.1)',
            line=dict(width=0),
            name="In-the-money",
            showlegend=True,
        ),
        row=2, col=1
    )
    
    # Out-of-the-money area (red)
    fig.add_trace(
        go.Scatter(
            x=K_range[K_range > S],
            y=tr_values[-len(K_range[K_range > S]):],
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.1)',
            line=dict(width=0),
            name="Out-of-the-money",
            showlegend=True,
        ),
        row=2, col=1
    )
    
    # At-the-money area (blue)
    atm_indices = np.where(np.abs(K_range/S - 1) < atm_range)
    if len(atm_indices[0]) > 0:
        atm_K = K_range[atm_indices]
        atm_tr = [tr_values[i] for i in atm_indices[0]]
        
        fig.add_trace(
            go.Scatter(
                x=atm_K,
                y=atm_tr,
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(width=0),
                name="At-the-money",
                showlegend=True,
            ),
            row=2, col=1
        )
    
    # Melhorar as anotações para S e K
    fig.add_annotation(
        x=S, y=0,
        text=f"S = {S:.2f}",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="green",
        ax=0, ay=-40,
        font=dict(size=12, color="green"),
        bgcolor="rgba(255, 255, 255, 0.85)",
        bordercolor="green",
        borderwidth=1,
        borderpad=4,
        row=2, col=1
    )

    fig.add_annotation(
        x=K, y=0,
        text=f"K = {K:.2f}\nPV(K) = {PV_K:.2f}",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=0, ay=-80,
        font=dict(size=12, color="darkred"),
        bgcolor="rgba(255, 255, 255, 0.85)",
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
        row=2, col=1
    )
    
    # Update x-axis labels for moneyness
    fig.update_xaxes(
        title_text="Strike Price (K)",
        row=2, col=1
    )
    
    # Add a secondary x-axis for moneyness
    fig.update_layout(
        xaxis3=dict(
            title="Strike Price (K)",
            showgrid=True,
        ),
        xaxis4=dict(
            title="Moneyness (K/S)",
            overlaying="x3",
            side="top",
            tickvals=[S * m for m in np.arange(0.6, 1.5, 0.1)],
            ticktext=[f"{m:.1f}" for m in np.arange(0.6, 1.5, 0.1)],
            showgrid=False,
        ),
    )
    
    # Update axis labels and formatting
    fig.update_xaxes(title_text="Distance Parameter (ξ)", row=1, col=1)
    fig.update_yaxes(title_text="Effective Volatility (%)", row=1, col=1)
    
    fig.update_xaxes(title_text="Effective Volatility (%)", row=1, col=2)
    fig.update_yaxes(title_text="Time Threshold (tr) in days", row=1, col=2)
    
    fig.update_yaxes(title_text="Time Threshold (tr) in days", row=2, col=1)

    # Melhoria na legenda - separando em grupos lógicos e melhorando o posicionamento
    # Definir legendas personalizadas para cada grupo
    legend_groups = {
        "curves": {
            "names": ["Horizon of Indecision", "σef", "Time Threshold"],
            "title": "Curve Analysis"
        },
        "markers": {
            "names": ["Current Value"],
            "title": "Current Position"
        },
        "areas": {
            "names": ["In-the-money", "Out-of-the-money", "At-the-money"],
            "title": "Option Zones"
        }
    }

    # Atribuir grupo apropriado para cada trace
    for i in range(len(fig.data)):
        trace_name = fig.data[i].name
        for group, info in legend_groups.items():
            if trace_name in info["names"]:
                fig.data[i].legendgroup = group
                fig.data[i].legendgrouptitle = dict(text=info["title"])
                break

    # Melhorar a apresentação e posicionamento da legenda
    fig.update_layout(
        template="plotly_white",
        showlegend=show_legend,  # Usar o valor do switch para controlar a visibilidade
        legend=dict(
            # resto das configurações permanece igual...
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="rgba(0, 0, 0, 0.2)",
            borderwidth=1,
            font=dict(size=11),
            itemsizing="constant",
            groupclick="toggleitem",
            tracegroupgap=8,
        ),
        # Ajustar margens com base na visibilidade da legenda
        margin=dict(l=40, r=60 if show_legend else 40, t=50, b=30),
        hovermode="closest",
    )
    
    # Create results display as Bootstrap components
    # Determine option status
    if np.abs(S/K - 1) < atm_range:
        status = "At-the-money"
        status_color = "info"
    elif S > K:
        status = "In-the-money (Call) / Out-of-the-money (Put)"
        status_color = "success"
    else:
        status = "Out-of-the-money (Call) / In-the-money (Put)"
        status_color = "danger"
    
    results_display = [
        dbc.Alert(
            f"Current Option Status: {status}",
            color=status_color,
            className="text-center mb-3"
        ),
        html.Div([
            dbc.Row([
                dbc.Col([html.Strong("Distance Parameter (ξ):")], width=6),
                dbc.Col([f"{xi:.4f}"], width=6),
            ], className="mb-2"),
            dbc.Row([
                dbc.Col([html.Strong("Effective Volatility (σef):")], width=6),
                dbc.Col([f"{sigma_ef_val:.2f}%"], width=6),
            ], className="mb-2"),
            dbc.Row([
                dbc.Col([html.Strong("Time Threshold (tr):")], width=6),
                dbc.Col([f"{tr_val:.2f} days"], width=6),
            ], className="mb-2"),
            dbc.Row([
                dbc.Col([html.Strong("Present Value of K:")], width=6),
                dbc.Col([f"{PV_K:.2f}"], width=6),
            ], className="mb-2"),
        ]),
    ]
    
    # Create formatted displays for sliders
    stock_price_display = f"Current value: ${S:.2f}"
    strike_price_display = f"Current value: ${K:.2f}"
    volatility_display = f"Current value: {sigma_daily:.2f}%"
    
    return fig, results_display, stock_price_display, strike_price_display, volatility_display

# Callback for reset button
@app.callback(
    [Output("stock-price-slider", "value"),
     Output("strike-price-slider", "value"),
     Output("volatility-slider", "value"),
     Output("risk-free-rate-input", "value"),
     Output("time-to-expiration-input", "value")],
    [Input("reset-button", "n_clicks")],
    [State("stock-price-slider", "value"),
     State("strike-price-slider", "value"),
     State("volatility-slider", "value"),
     State("risk-free-rate-input", "value"),
     State("time-to-expiration-input", "value")]
)
def reset_values(n_clicks, current_s, current_k, current_vol, current_r, current_t):
    # Only reset if button is clicked
    if n_clicks is None:
        return current_s, current_k, current_vol, current_r, current_t
    return S_default, K_default, sigma_daily_default, r_default, t_default

# Main entry point
if __name__ == "__main__":
    print("Option Horizon of Indecision Calculator - Interactive Dashboard")
    print("------------------------------------------------------------")
    print("Starting the interactive dashboard. Please wait...")
    print("Once started, open your web browser to http://127.0.0.1:8050/")
    app.run_server(debug=True)