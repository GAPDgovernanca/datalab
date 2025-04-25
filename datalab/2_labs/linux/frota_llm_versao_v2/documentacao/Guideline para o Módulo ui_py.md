# Guideline – Módulo ui.py

## 1. Objetivo do Módulo

O módulo **ui.py** deverá centralizar a lógica de apresentação e interação do usuário com o dashboard de gestão de frota agrícola. Suas responsabilidades incluem:

- **Configuração do Layout:** Definir o layout da página (por exemplo, utilizar o modo "wide") e organizar a distribuição dos componentes (cabeçalho, sidebar, área de conteúdo).
- **Exibição de Componentes:** Renderizar componentes interativos, como filtros, cards de métricas, gráficos, tabelas e áreas para inserção de perguntas.
- **Customização Visual:** Aplicar estilos via CSS customizado para garantir uma interface agradável e consistente.
- **Integração com Outros Módulos:** Integrar os dados e resultados processados pelos módulos *db*, *filters*, *processing* e *ia_integration* para exibição e interação com o usuário.
- **Interatividade e Feedback:** Prover mensagens de erro, alertas e feedback visual (por exemplo, utilizando `st.error()`, `st.warning()`, etc.) para melhorar a experiência do usuário.

---

## 2. Escopo e Funcionalidades

### 2.1. Componentes Principais da Interface

- **Configuração Inicial e Layout:**
  - Configurar a página com `st.set_page_config(layout="wide")`.
  - Definir o cabeçalho principal, por exemplo, utilizando `st.markdown()` com estilos customizados.
- **Sidebar de Filtros:**
  - Criar uma sidebar que permita a seleção interativa de filtros (datas, IDs, usuário, classe).
  - Utilizar componentes como `st.date_input()`, `st.multiselect()` e `st.text_input()`.
- **Área de Conteúdo Principal:**
  - Exibir cards de métricas (usando HTML customizado via `st.markdown()`).
  - Renderizar gráficos interativos (por exemplo, com `st.plotly_chart()`).
  - Exibir tabelas de dados processados (usando `st.dataframe()` ou `st.table()`).
  - Incluir uma seção para perguntas à IA (usando `st.text_area()` e botões de ação).

### 2.2. Interação e Atualização dos Componentes

- **Reatividade:**
  - Atualizar os componentes conforme a seleção de filtros ou inserção de perguntas, garantindo que a interface responda dinamicamente às alterações.
- **Mensagens de Feedback:**
  - Exibir mensagens informativas, de erro ou alertas para o usuário, utilizando `st.info()`, `st.error()` ou `st.warning()` conforme o contexto.
- **Integração com Dados Processados:**
  - Integrar os dados oriundos dos módulos de processamento para exibição em gráficos e tabelas.

---

## 3. Estrutura e Organização do Código

### 3.1. Separação de Responsabilidades

- **Divisão em Funções e Classes:**
  - Separe a lógica de construção da interface em funções específicas, como:
    - `render_header()`: para exibir o cabeçalho e título principal.
    - `render_sidebar()`: para configurar e renderizar os filtros e outros controles na sidebar.
    - `render_cards()`: para exibir os cards com métricas chave.
    - `render_graphs()`: para a criação e exibição dos gráficos interativos.
    - `render_table()`: para exibir os dados em formato tabular.
    - `render_ia_section()`: para a área de perguntas à IA e exibição das respostas.
- **Utilização de Classes (Opcional):**
  - Se o projeto se beneficiar de uma organização orientada a objetos, considere encapsular a construção da interface em uma classe (por exemplo, `DashboardUI`). Essa abordagem permite agrupar funções relacionadas e compartilhar estado entre as funções de renderização.

### 3.2. Organização do Código

- **Docstrings e Type Hints:**
  
  - Documente cada função com docstrings explicando os parâmetros, a lógica e os retornos.
  - Utilize type hints para melhorar a legibilidade e auxiliar na manutenção.

- **Modularidade e Reusabilidade:**
  
  - Garanta que cada função tenha uma responsabilidade bem definida e possa ser testada de forma independente.
  - Evite misturar lógica de negócios (processamento de dados) com a lógica de apresentação.

---

## 4. Boas Práticas e Considerações

- **Estilos e Customizações:**
  
  - Centralize os estilos CSS em um bloco único, aplicável via `st.markdown(css_code, unsafe_allow_html=True)`, para manter a consistência visual.

- **Responsividade:**
  
  - Utilize componentes como `st.columns()` e `st.container()` para garantir que a interface se ajuste bem a diferentes tamanhos de tela.

- **Tratamento de Erros e Feedback:**
  
  - Utilize blocos try/except quando necessário e forneça feedback visual ao usuário em caso de erros na renderização dos componentes.

- **Integração com Módulos de Dados:**
  
  - A lógica de obtenção de dados e processamento deve ser realizada por módulos externos (como *db.py*, *filters.py*, *processing.py* e *ia_integration.py*), e a UI deve apenas invocar esses módulos para obter os dados a serem exibidos.

- **Testabilidade:**
  
  - Estruture a interface de modo que partes dela possam ser testadas individualmente (por exemplo, simulação de entrada de filtros ou validação de atualizações na tabela).

---

## 5. Exemplo de Estrutura e Código do ui.py

A seguir, um exemplo simplificado demonstrando a organização sugerida para o módulo **ui.py**:

```python
import streamlit as st
import pandas as pd
from typing import Tuple

# Suponha que os módulos de processamento e integração já estejam implementados
# from db import Database
# from filters import FilterBuilder
# from processing import DataProcessor
# from ia_integration import AIIntegration

def render_header():
    """
    Renderiza o cabeçalho do dashboard.
    """
    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #ecf0f1;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown('<h1 class="centered-title">Dashboard de Gestão de Frota Agrícola</h1>', unsafe_allow_html=True)

def render_sidebar() -> dict:
    """
    Renderiza a sidebar com filtros e retorna um dicionário com os valores selecionados.

    :return: Dicionário contendo os filtros aplicados.
    """
    st.sidebar.header("Filtros de Consulta")

    # Exemplo: Seleção de intervalo de datas
    date_range = st.sidebar.date_input("Data de Referência", [])

    # Exemplo: Seleção de IDs de equipamentos
    id_input = st.sidebar.text_input("IDs de Equipamento (separados por vírgula)")
    ids = [int(id.strip()) for id in id_input.split(",") if id.strip().isdigit()] if id_input else []

    # Exemplo: Seleção de usuário e classe
    usuario = st.sidebar.multiselect("Unidade", ["Todos", "Fazenda A", "Fazenda B"], default=["Todos"])
    classe = st.sidebar.multiselect("Classe", ["Todos", "Trator", "Colheitadeira"], default=["Todos"])

    return {
        "data_referencia": date_range,
        "id_equipamento": ids,
        "usuario": usuario,
        "classe": classe
    }

def render_cards(total_registros: int, total_estimado: float):
    """
    Renderiza os cards de métricas no topo do dashboard.

    :param total_registros: Número total de registros.
    :param total_estimado: Valor total estimado (ex.: em R$).
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div style="background-color:#2c3e50;padding:10px;border-radius:10px;color:#ecf0f1;text-align:center;margin-bottom:10px;">'
            f'<h3>Total de Registros</h3><p>{total_registros:,}</p></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div style="background-color:#2c3e50;padding:10px;border-radius:10px;color:#ecf0f1;text-align:center;margin-bottom:10px;">'
            f'<h3>Total Estimado</h3><p>R$ {total_estimado:,.0f}</p></div>',
            unsafe_allow_html=True
        )

def render_graphs(processed_df: pd.DataFrame):
    """
    Renderiza os gráficos interativos com base nos dados processados.

    :param processed_df: DataFrame com os dados processados para visualização.
    """
    # Exemplo: gráfico de barras utilizando Plotly Express
    try:
        import plotly.express as px
        # Prepare os dados para o gráfico
        plot_data = processed_df.copy()
        # Exemplo: Cria um gráfico de barras comparando indicadores
        fig = px.bar(plot_data, x='id_equipamento', y='Taxa Utilização Multiplicador', 
                     title='Indicadores de Utilização por Equipamento')
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao renderizar o gráfico: {e}")

def render_table(processed_df: pd.DataFrame):
    """
    Exibe os dados processados em uma tabela interativa.

    :param processed_df: DataFrame com os dados prontos para exibição.
    """
    st.subheader("Dados Filtrados")
    st.dataframe(processed_df)

def render_ia_section():
    """
    Renderiza a seção de perguntas à IA, permitindo a entrada do usuário e exibindo a resposta.
    """
    st.subheader("Perguntas sobre os Dados")
    user_question = st.text_area("Digite sua pergunta:", height=100)

    if st.button("Perguntar à IA"):
        if user_question:
            # Exemplo: Invocar a integração com IA (supondo que o módulo ia_integration esteja configurado)
            # ai_integration = AIIntegration()
            # resposta = ai_integration.query(data_json, user_question)
            resposta = "Resposta simulada da IA para a pergunta: " + user_question  # Simulação
            st.markdown(resposta)
        else:
            st.warning("Por favor, insira uma pergunta.")

def main_ui():
    """
    Função principal que integra todos os componentes da interface.
    """
    render_header()
    filtros = render_sidebar()

    # Simulação: Obter dados do banco e processá-los (os módulos db, filters e processing devem ser integrados)
    total_registros = 1500  # Exemplo estático
    total_estimado = 1250000.0  # Exemplo estático
    render_cards(total_registros, total_estimado)

    # Simulação: DataFrame de dados processados
    sample_data = {
        'id_equipamento': [101, 102, 103],
        'Taxa Utilização Multiplicador': [1.1, 0.9, 1.0],
        'Consumo Multiplicador': [0.95, 1.05, 1.00]
    }
    processed_df = pd.DataFrame(sample_data)
    render_graphs(processed_df)
    render_table(processed_df)
    render_ia_section()

# Execução do dashboard
if __name__ == "__main__":
    main_ui()
```

---

## 6. Considerações Finais e Próximos Passos

- **Testes e Validação:**  
  Desenvolver testes manuais e unitários para validar cada componente da interface. Verifique se os filtros, gráficos e tabelas são atualizados conforme esperado.

- **Feedback do Usuário:**  
  Após um protótipo inicial, colete feedback dos usuários para ajustar a usabilidade e os elementos visuais da interface.

- **Melhoria Contínua:**  
  Revise periodicamente o código da UI para incorporar melhorias, novos estilos ou componentes, mantendo a separação clara entre a lógica de apresentação e a lógica de negócios.
