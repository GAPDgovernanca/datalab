import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Configuração da Página ---
st.set_page_config(
    page_title="Mosaico IMS_PV - Confinamento",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Estilos CSS Customizados ---
st.markdown("""
    <style>
    /* Estiliza o container da métrica (Cards) */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Força a cor do Rótulo (Título do Card) para cinza escuro */
    /* Usamos seletores múltiplos para garantir que o Streamlit não sobrescreva */
    [data-testid="stMetricLabel"], 
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] > label,
    [data-testid="stMetricLabel"] p {
        color: #6c757d !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Força a cor do Valor numérico para preto */
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div {
        color: #212529 !important;
    }

    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Remove margens extras do gráfico plotly para encaixar melhor */
    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. Geração de Dados ---
@st.cache_data
def generate_data():
    # Dados base
    data = [
        {'CURRAL': 'C01', 'IMS_PV': 3.25, 'CONSUMO_MS': 14.6, 'PESO_ENTRADA': 380, 'PESO_MEDIO_ATUAL': 520, 'DIAS_CONF': 75, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 30},
        {'CURRAL': 'C02', 'IMS_PV': 2.85, 'CONSUMO_MS': 12.8, 'PESO_ENTRADA': 410, 'PESO_MEDIO_ATUAL': 490, 'DIAS_CONF': 42, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 22},
        {'CURRAL': 'C03', 'IMS_PV': 3.45, 'CONSUMO_MS': 15.1, 'PESO_ENTRADA': 370, 'PESO_MEDIO_ATUAL': 530, 'DIAS_CONF': 80, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 35},
        {'CURRAL': 'C04', 'IMS_PV': 2.05, 'CONSUMO_MS': 9.2, 'PESO_ENTRADA': 390, 'PESO_MEDIO_ATUAL': 435, 'DIAS_CONF': 25, 'TIPO_RACAO_ATUAL': 'Crescimento', 'TIPO_DIAS_RACAO': 25},
        {'CURRAL': 'C05', 'IMS_PV': 1.85, 'CONSUMO_MS': 8.5, 'PESO_ENTRADA': 450, 'PESO_MEDIO_ATUAL': 465, 'DIAS_CONF': 20, 'TIPO_RACAO_ATUAL': 'Adaptação', 'TIPO_DIAS_RACAO': 20},
        {'CURRAL': 'C06', 'IMS_PV': 1.65, 'CONSUMO_MS': 7.2, 'PESO_ENTRADA': 420, 'PESO_MEDIO_ATUAL': 440, 'DIAS_CONF': 15, 'TIPO_RACAO_ATUAL': 'Adaptação', 'TIPO_DIAS_RACAO': 15},
        {'CURRAL': 'C07', 'IMS_PV': 2.95, 'CONSUMO_MS': 13.0, 'PESO_ENTRADA': 400, 'PESO_MEDIO_ATUAL': 505, 'DIAS_CONF': 60, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 25},
        {'CURRAL': 'C08', 'IMS_PV': 3.15, 'CONSUMO_MS': 14.0, 'PESO_ENTRADA': 380, 'PESO_MEDIO_ATUAL': 525, 'DIAS_CONF': 70, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 30},
        {'CURRAL': 'C09', 'IMS_PV': 2.15, 'CONSUMO_MS': 9.8, 'PESO_ENTRADA': 430, 'PESO_MEDIO_ATUAL': 465, 'DIAS_CONF': 22, 'TIPO_RACAO_ATUAL': 'Crescimento', 'TIPO_DIAS_RACAO': 22},
        {'CURRAL': 'C10', 'IMS_PV': 3.55, 'CONSUMO_MS': 15.5, 'PESO_ENTRADA': 365, 'PESO_MEDIO_ATUAL': 535, 'DIAS_CONF': 85, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 40},
        {'CURRAL': 'C11', 'IMS_PV': 2.25, 'CONSUMO_MS': 10.5, 'PESO_ENTRADA': 425, 'PESO_MEDIO_ATUAL': 470, 'DIAS_CONF': 28, 'TIPO_RACAO_ATUAL': 'Crescimento', 'TIPO_DIAS_RACAO': 28},
        {'CURRAL': 'C12', 'IMS_PV': 3.35, 'CONSUMO_MS': 14.8, 'PESO_ENTRADA': 375, 'PESO_MEDIO_ATUAL': 515, 'DIAS_CONF': 72, 'TIPO_RACAO_ATUAL': 'Terminação', 'TIPO_DIAS_RACAO': 32},
    ]

    np.random.seed(42)
    for i in range(13, 101):
        imspv = 1.5 + np.random.random() * 2.3
        peso_entrada = 350 + np.random.random() * 100
        ganho = 30 + np.random.random() * 150
        peso_atual = peso_entrada + ganho
        dias_conf = int(10 + np.random.random() * 80)

        tipo_racao = 'Adaptação'
        if dias_conf > 25: tipo_racao = 'Crescimento'
        if dias_conf > 40: tipo_racao = 'Terminação'

        dias_racao = min(dias_conf, 40 if tipo_racao == 'Terminação' else (30 if tipo_racao == 'Crescimento' else 15))

        data.append({
            'CURRAL': f'C{i:02d}',
            'IMS_PV': imspv,
            'CONSUMO_MS': (imspv * peso_atual / 100),
            'PESO_ENTRADA': peso_entrada,
            'PESO_MEDIO_ATUAL': peso_atual,
            'DIAS_CONF': dias_conf,
            'TIPO_RACAO_ATUAL': tipo_racao,
            'TIPO_DIAS_RACAO': dias_racao
        })
    
    return pd.DataFrame(data)

# --- 2. Lógica de Negócio e Classificação ---
def calculate_stats(df):
    media = df['IMS_PV'].mean()
    desvio = df['IMS_PV'].std()
    return media, desvio

def classify_imspv_data(val, media, desvio):
    # Retorna: (Label, Cor Hex, Índice, Cor do Texto)
    # Ajustamos a cor do texto para garantir contraste (preto no amarelo/laranja)
    if val > media + 2 * desvio: return ('Muito Alto', '#3b82f6', 5, 'white')
    if val > media + desvio: return ('Alto', '#22c55e', 4, 'white')
    if val > media: return ('Acima média', '#eab308', 3, '#1f2937') # Texto escuro no Amarelo
    if val > media - desvio: return ('Abaixo média', '#fb923c', 2, 'white')
    if val > media - 2 * desvio: return ('Alerta', '#ef4444', 1, 'white')
    return ('Crítico', '#1f2937', 0, 'white')

# --- 3. Componentes de UI ---

def main():
    st.markdown("<div class='main-header'><h1>Mosaico IMS_PV - Confinamento</h1><p style='color:gray'>Ingestão de Matéria Seca / Peso Vivo (%)</p></div>", unsafe_allow_html=True)

    df = generate_data()
    media, desvio = calculate_stats(df)
    
    # Aplica classificação expandida
    classification_results = df['IMS_PV'].apply(lambda x: classify_imspv_data(x, media, desvio))
    df['Status'] = [x[0] for x in classification_results]
    df['Color'] = [x[1] for x in classification_results]
    df['Color_Index'] = [x[2] for x in classification_results] 
    df['Text_Color'] = [x[3] for x in classification_results] # Nova coluna de cor do texto
    
    # Ordenar
    df = df.sort_values('IMS_PV', ascending=False).reset_index(drop=True)

    # Grid Coordinates
    cols_per_row = 10
    df['X_Grid'] = df.index % cols_per_row
    df['Y_Grid'] = df.index // cols_per_row
    df['Y_Grid'] = df['Y_Grid'].max() - df['Y_Grid']

    # --- Visualização: Heatmap (Fundo) + Scatter (Texto/Interação) ---
    fig_grid = go.Figure()

    # 1. Camada de Fundo (Heatmap)
    colors_map = [
        [0.0, '#1f2937'], [0.166, '#1f2937'], # Crítico
        [0.166, '#ef4444'], [0.333, '#ef4444'], # Alerta
        [0.333, '#fb923c'], [0.5, '#fb923c'],   # Abaixo
        [0.5, '#eab308'], [0.666, '#eab308'],   # Acima
        [0.666, '#22c55e'], [0.833, '#22c55e'], # Alto
        [0.833, '#3b82f6'], [1.0, '#3b82f6']    # Muito Alto
    ]
    
    fig_grid.add_trace(go.Heatmap(
        x=df['X_Grid'],
        y=df['Y_Grid'],
        z=df['Color_Index'],
        colorscale=colors_map,
        showscale=False,
        xgap=2, 
        ygap=2,
        hoverinfo='skip'
    ))

    # 2. Camada de Texto e Interação (Scatter)
    fig_grid.add_trace(go.Scatter(
        x=df['X_Grid'],
        y=df['Y_Grid'],
        mode='text',
        text=df['CURRAL'] + "<br>" + df['IMS_PV'].apply(lambda x: f"{x:.2f}%"),
        # Aqui usamos a lista de cores calculada para cada ponto individualmente
        textfont=dict(color=df['Text_Color'], size=11, family="Arial Black"),
        hoverinfo='text',
        hovertext=df['CURRAL'] + "<br>Status: " + df['Status'] + "<br>IMS_PV: " + df['IMS_PV'].apply(lambda x: f"{x:.2f}%"),
        customdata=df[['CURRAL', 'Status', 'IMS_PV']]
    ))

    fig_grid.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False, fixedrange=True),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False, fixedrange=True),
        margin=dict(t=10, l=10, r=10, b=10),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        clickmode='event+select',
        dragmode=False
    )

    st.markdown("##### 🖱️ Clique em um bloco do mosaico para ver os detalhes")
    
    # Atualizado para width="stretch" conforme o warning do Streamlit
    event = st.plotly_chart(fig_grid, width="stretch", on_select="rerun", selection_mode="points", key="mosaico_final")

    # --- Lógica de Seleção ---
    selected_curral_id = None
    if event and event.selection and len(event.selection.points) > 0:
        point = event.selection.points[0]
        if "customdata" in point:
            selected_curral_id = point["customdata"][0]

    if not selected_curral_id:
        selected_curral_id = df.iloc[0]['CURRAL']

    # Legenda
    cols = st.columns(6)
    legends = [
        ("Muito Alto", "#3b82f6", f"> {(media + 2*desvio):.2f}%"),
        ("Alto", "#22c55e", f"{(media + desvio):.2f} - {(media + 2*desvio):.2f}%"),
        ("Acima média", "#eab308", f"{media:.2f} - {(media + desvio):.2f}%"),
        ("Abaixo média", "#fb923c", f"{(media - desvio):.2f} - {media:.2f}%"),
        ("Alerta", "#ef4444", f"{(media - 2*desvio):.2f} - {(media - desvio):.2f}%"),
        ("Crítico", "#1f2937", f"< {(media - 2*desvio):.2f}%"),
    ]
    
    for col, (label, color, range_val) in zip(cols, legends):
        with col:
            st.markdown(f"<div style='display:flex;align-items:center;font-size:12px'><div style='width:12px;height:12px;background-color:{color};border-radius:2px;margin-right:5px'></div><div><b>{label}</b><br>{range_val}</div></div>", unsafe_allow_html=True)

    st.divider()

    # --- Área de Detalhes ---
    selected_row = df[df['CURRAL'] == selected_curral_id]
    
    if not selected_row.empty:
        selected_data = selected_row.iloc[0]
        
        st.markdown(f"### 📊 Detalhes: {selected_data['CURRAL']}")
        st.caption(f"Status: {selected_data['Status']} | IMS_PV: {selected_data['IMS_PV']:.2f}%")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Consumo MS", f"{selected_data['CONSUMO_MS']:.2f} kg/dia")
        c2.metric("Dias Confinamento", f"{int(selected_data['DIAS_CONF'])} dias")
        c3.metric("Tipo Ração", selected_data['TIPO_RACAO_ATUAL'])
        c4.metric("Dias na Ração", f"{int(selected_data['TIPO_DIAS_RACAO'])} dias")

        st.markdown("---")
        
        ganho_total = selected_data['PESO_MEDIO_ATUAL'] - selected_data['PESO_ENTRADA']
        gmd = ganho_total / selected_data['DIAS_CONF'] if selected_data['DIAS_CONF'] > 0 else 0
        conversao_alimentar = selected_data['CONSUMO_MS'] / gmd if gmd > 0.1 else 0

        peso_meta = 560
        peso_restante = peso_meta - selected_data['PESO_MEDIO_ATUAL']
        dias_para_abate = int(peso_restante / gmd) if (gmd > 0 and peso_restante > 0) else 0
        data_prevista = datetime.now() + timedelta(days=dias_para_abate) if dias_para_abate > 0 else datetime.now()
        
        col_chart, col_projection = st.columns([1, 1])

        with col_chart:
            st.markdown("#### ⚖️ Evolução de Peso")
            peso_df = pd.DataFrame([
                {'Tipo': 'Entrada', 'Valor': selected_data['PESO_ENTRADA'], 'Cor': '#16a34a'},
                {'Tipo': 'Atual', 'Valor': selected_data['PESO_MEDIO_ATUAL'], 'Cor': '#2563eb'},
                {'Tipo': 'Meta', 'Valor': peso_meta, 'Cor': '#9333ea'}
            ])
            
            fig_bar = px.bar(
                peso_df, 
                x='Tipo', 
                y='Valor', 
                color='Tipo',
                color_discrete_map={'Entrada': '#16a34a', 'Atual': '#2563eb', 'Meta': '#9333ea'},
                text_auto='.0f'
            )
            fig_bar.update_layout(
                showlegend=False, 
                height=250,
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis_title="Peso (kg)",
                xaxis_title=None
            )
            # Atualizado para width="stretch" conforme o warning do Streamlit
            st.plotly_chart(fig_bar, width="stretch")

        with col_projection:
            st.markdown("#### 🚀 Performance e Planejamento")
            
            kp1, kp2 = st.columns(2)
            with kp1:
                st.info(f"**GMD Atual**\n\n{gmd:.2f} kg/dia")
                st.warning(f"**Conversão (CA)**\n\n{conversao_alimentar:.2f}")

            with kp2:
                if peso_restante > 0:
                    st.success(f"**Dias p/ Abate**\n\n{dias_para_abate} dias")
                    st.caption(f"Data Est.: {data_prevista.strftime('%d/%m/%Y')}")
                else:
                    st.success(f"**Status Meta**\n\nAtingida! 🎉")
            
            st.markdown("---")
            st.markdown(f"<small>Meta de Peso definida em: <b>{peso_meta} kg</b></small>", unsafe_allow_html=True)
    else:
        st.error("Erro ao carregar dados do curral selecionado.")

if __name__ == "__main__":
    main()