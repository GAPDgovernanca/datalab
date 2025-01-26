import streamlit as st
import pandas as pd

# Load consolidated data
data = pd.read_csv("consolidated_data.csv")

st.title("Dashboard de Dados Comerciais")

# Display a selection box to filter by "Cliente"
selected_cliente = st.selectbox(
    "Selecione o Cliente:", options=["Todos"] + list(data["CLIENTE"].dropna().unique())
)

# Filter the data based on the selected cliente
if selected_cliente != "Todos":
    filtered_data = data[data["CLIENTE"] == selected_cliente]

    if not filtered_data.empty:
        st.write("### Informações Detalhadas")

        # Display the details in a more readable layout
        for idx, row in filtered_data.iterrows():
            with st.expander("Clique para visualizar detalhes"):
                col1, col2 = st.columns(2)  # Split details into two columns
                with col1:
                    st.markdown(f"**CLIENTE:** {row['CLIENTE']}")
                    st.markdown(f"**N° DE LOJAS:** {row['N° DE LOJAS']}")
                    st.markdown(f"**REPRESENTANTE:** {row['REPRESENTANTE']}")
                    st.markdown(f"**NUMERO SKU'S:** {row.get('NUMERO SKU\'S ', 'N/A')}")
                with col2:
                    st.markdown(
                        f"**% CONTRATO:** {row['% CONTRATO'] if pd.notna(row['% CONTRATO']) else 'Não disponível'}"
                    )
                    st.markdown(
                        f"**FATURAMENTO/ENTREGA:** {row['FATURAMENTO/ENTREGA']}"
                    )
                    st.markdown(
                        f"**PERSPECTIVA FATURAR:** {row['PERSPECTIVA FATURAR']}"
                    )
                    status_color = (
                        "green" if "assinado" in str(row["STATUS"]).lower() else "red"
                    )
                    st.markdown(
                        f"<span style='color:{status_color};'><strong>STATUS:</strong> {row['STATUS']}</span>",
                        unsafe_allow_html=True,
                    )
    else:
        st.warning("Nenhum dado encontrado para o cliente selecionado.")
else:
    st.info("Selecione um cliente para visualizar os detalhes.")
