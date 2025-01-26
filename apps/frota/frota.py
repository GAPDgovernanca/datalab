import streamlit as st
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os

# Configurar página para modo wide
st.set_page_config(layout="wide", page_title="Indicadores da frota", page_icon="🚜")


# Adicionar CSS personalizado para ajustar o cabeçalho
st.markdown("""
    <style>
    h1 {
        font-size: 2.5rem; /* Ajusta o tamanho do texto do cabeçalho */
        margin-bottom: 20px; /* Adiciona espaçamento abaixo do cabeçalho */
        text-align: left; /* desloca o título para esquerda */
    }
    </style>
""", unsafe_allow_html=True)

   
# 1. Classe para carregar e validar dados
class DataLoader:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self.configuracoes = self.carregar_configuracoes()
        self.df = None
        # Adicionar mapeamento de colunas para fácil acesso
        self.colunas = {
            'classe': 'Classe',
            'equipamento': 'Equipamento',
            'medidor': 'Medidor',
            'modelo': 'Modelo/Versão',
            'usuario': 'Usuário'
        }

    def carregar_configuracoes(self):
        """
        Carrega as configurações do arquivo YAML com suporte a caminhos dinâmicos.
        """
        # Obter o diretório do script atual
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, self.yaml_path)

        try:
            with open(config_path, "r", encoding="utf-8") as arquivo:  # Forçar codificação UTF-8
                return yaml.safe_load(arquivo)
        except FileNotFoundError:
            st.error(f"O arquivo de configuração '{config_path}' não foi encontrado.")
            return None
        except yaml.YAMLError as e:
            st.error(f"Erro ao ler o arquivo de configuração: {e}")
            return None

    def carregar_arquivo(self):
        """
        Carrega o arquivo Excel enviado pelo usuário.
        """
        arquivo = st.file_uploader("Carregue um arquivo Excel", type=["xlsx"])
        if arquivo:
            self.df = pd.read_excel(arquivo, thousands=',', decimal='.')  # Trata números como "1,550.00"
            self.df.columns = [col.strip() for col in self.df.columns]  # Remove espaços extras dos nomes das colunas
            
            if not self.validar_colunas():
                st.error("O arquivo não contém as colunas necessárias.")
                return None
                
            self.preencher_nulos()
            st.success("Arquivo carregado com sucesso!")
            return self.df
        return None

    def validar_colunas(self):
        """
        Valida as colunas do DataFrame contra as configurações do YAML,
        com tratamento robusto para espaços.
        """
        colunas_yaml = []
        for categoria, valores in self.configuracoes.items():
            # Limpa e normaliza os nomes das colunas do YAML
            colunas_yaml.extend(key.strip() for key in valores.keys())
        
        # Adiciona as colunas do mapeamento
        colunas_yaml.extend(self.colunas.values())
        
        # Limpa e normaliza os nomes das colunas do DataFrame
        colunas_df = [col.strip() for col in self.df.columns]  # Remove espaços de ambos os lados        
        # Compara as colunas normalizadas
        colunas_ausentes = [
            coluna for coluna in colunas_yaml 
            if coluna not in colunas_df
        ]
        
        if colunas_ausentes:
            st.error(f"As seguintes colunas estão ausentes: {colunas_ausentes}")
            return False
        return True

    def preencher_nulos(self):
        """
        Preenche células vazias com 0 em colunas numéricas.
        """
        colunas_numericas = self.df.select_dtypes(include=[np.number]).columns
        self.df[colunas_numericas] = self.df[colunas_numericas].fillna(0)


# 2. Classe para gerar gráficos
class GraphGenerator:
    def __init__(self, df, configuracoes):
        self.df = df
        self.configuracoes = configuracoes

    def gerar_grafico_barras(self):
        """
        Gera um gráfico simplificado para os indicadores principais.
        """
        equipamentos = self.df["Equipamento"]
        indicadores = ["Uso vs Planejado", "Consumo vs Planejado"]
        multiplicadores = [
            self.df["Taxa Utilização Multiplicador"],
            self.df["Consumo Multiplicador"],
        ]

        x = range(len(equipamentos))
        width = 0.35  # Aumentado para melhor visualização

        cores = ["#1f77b4", "#ff7f0e"]  # Azul, laranja

        fig, ax = plt.subplots(figsize=(12, 6))
        for i, (label, values) in enumerate(zip(indicadores, multiplicadores)):
            ax.bar(
                [p + i * width for p in x],
                values,
                width,
                label=label,
                color=cores[i],
                edgecolor="black"
            )

        ax.axhline(y=1, color="red", linestyle="--", linewidth=1, label="Planejado (1.0)")
        ax.set_xlabel("Equipamento")
        ax.set_ylabel("Realizado vs Planejado")
        ax.set_title("Indicadores de Uso e Consumo por Equipamento")
        ax.set_xticks([p + width/2 for p in x])
        ax.set_xticklabels(equipamentos, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
        
        # Retornar a figura para exportação
        return fig

    def exibir_tabela_resumo(self):
        """
        Exibe uma tabela resumo com indicadores operacionais e financeiros.
        """
        # Criar dois DataFrames separados para melhor organização
        df_indicadores = self.df[[
            "Equipamento",
            "Taxa Utilização Multiplicador",
            "Consumo Multiplicador",
        ]].copy()
        
        df_proporcoes = self.df[[
            "Equipamento",
            "Lubrificantes Proporcao",
            "Filtros Proporcao",
            "Graxas Proporcao",
            "PSP Proporcao",
            "Reforma Proporcao",
            "Total Realizado"
        ]].copy()
        
        # Mesclar os DataFrames
        df_resumo = df_indicadores.merge(df_proporcoes, on="Equipamento")
        
        # Renomear as colunas para melhor visualização
        df_resumo.columns = [
            "Equipamento",
            "Util.%",
            "Cons.%",
            "Lub.%",
            "Filt.%",
            "Grax.%",
            "Peças%",
            "Reform%",
            "R$ Total"
        ]

        # Garantir que Equipamento seja tratado como string
        df_resumo["Equipamento"] = df_resumo["Equipamento"].astype(str)
        
        def format_percentage(x):
            """Formata percentuais com cores indicativas"""
            if pd.isna(x) or np.isinf(x):
                return "-"
            try:
                value = round(float(x * 100))
                # Valores muito altos também em vermelho
                if value > 999:
                    return f"🔴 >999%"
                elif value < -999:
                    return f"🔴 <-999%"
                
                # Usa cor vermelha para desvios acima de 20% e verde para economias
                if value > 120:
                    return f"🔴 {value}%"
                elif value < 80:
                    return f"🟢 {value}%"
                else:
                    return f"⚪ {value}%"
            except:
                return "-"
        
        def format_currency(x):
            """Formata valores monetários com notação brasileira"""
            try:
                rounded = round(float(x) / 100) * 100
                return f"R$ {rounded:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return "R$ 0"
        
        # Aplicar formatações
        for col in df_resumo.columns[1:]:
            if col == "R$ Total":
                df_resumo[col] = df_resumo[col].apply(format_currency)
            else:
                df_resumo[col] = df_resumo[col].apply(format_percentage)
        
        # Calcular e adicionar linha de total
        total_realizado = format_currency(self.df['Total Realizado'].sum())
        
        totais = {
            "Equipamento": "TOTAL",
            "Util.%": "",
            "Cons.%": "",
            "Lub.%": "",
            "Filt.%": "",
            "Grax.%": "",
            "Peças%": "",
            "Reform%": "",
            "R$ Total": total_realizado
        }
        
        # Adicionar linha de total ao DataFrame
        df_resumo.loc[len(df_resumo)] = totais
        
        st.markdown(
        """
        <style>
        [data-testid="stDataFrame"] {
            width: 100% !important;  /* Força a largura máxima */
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        
        # Exibir tabela com estilo
        st.write("### Análise por Equipamento")
        st.write("🔴 Acima do planejado/Crítico | 🟢 Abaixo do planejado | ⚪ Dentro do esperado (±20%)")
        st.dataframe(
            df_resumo,
            hide_index=True,
            use_container_width=True,  # Ajuste automático para ocupar todo o espaço do container
            column_config={
                "Equipamento": "Equip.",
                "Util.%": "Utilização",
                "Cons.%": "Consumo/h",
                "Lub.%": "Lubrif.",
                "Filt.%": "Filtros",
                "Grax.%": "Graxas",
                "Peças%": "Peças/Serv",
                "Reform%": "Reforma",
                "R$ Total": "Custo exc."
            }
        )

        # Adicionar seção de Downloads após a tabela
        st.markdown("### Downloads")
        st.markdown("---")  # Linha horizontal para separação visual

        # Criar três colunas para os botões
        col_df, col_chart, col_full = st.columns(3)

        # Botão 1: Exportar o DataFrame selecionado
        with col_df:
            if st.button("Exportar Tabela"):
                analise.df_filtrado.to_excel("analise_equipamentos_filtrado.xlsx", index=False)
                st.success("Tabela exportada como 'analise_equipamentos_filtrado.xlsx'.")

        # Botão 2: Exportar o gráfico de barras como PNG
        with col_chart:
            if st.button("Exportar Gráfico"):
                fig = graph_generator.gerar_grafico_barras()  # Obter o gráfico
                if fig is not None:
                    fig.savefig("grafico_barras.png", format="png")  # Salvar como PNG
                    st.success("Gráfico exportado como 'grafico_barras.png'.")
                else:
                    st.error("Erro ao gerar o gráfico para exportação.")

        # Botão 3: Exportar todos os dados originais (não filtrados)
        with col_full:
            if st.button("Exportar Todos os Dados"):
                analise.df.to_excel("analise_equipamentos_completo.xlsx", index=False)
                st.success("Todos os dados exportados como 'analise_equipamentos_completo.xlsx'.")


# 3. Classe principal para análise de indicadores
class AnaliseIndicadores:
    def __init__(self, yaml_path):
        self.data_loader = DataLoader(yaml_path)
        self.df = None
        self.df_filtrado = None
        self.meses_ajuste = 0

    def criar_interface(self):
        """
        Cria a interface com widgets de seleção no Streamlit,
        com layout melhorado e mais intuitivo.
        """
        if self.df is not None:
            st.markdown("#### Filtros de Seleção")
            
            # Container para os filtros principais
            with st.container():
                # 1. Seleção de Fazendas - Principal e mais proeminente
                st.markdown("##### 1. Selecione a Fazenda")
                usuarios = sorted(self.df["Usuário"].unique())
                col_check_fazenda, col_total_fazendas = st.columns([3, 1])
                with col_check_fazenda:
                    selecionar_todas_fazendas = st.checkbox(
                        "Selecionar todas as fazendas",
                        key="todas_fazendas"
                    )
                with col_total_fazendas:
                    st.markdown(f"Total: {len(usuarios)}")
                
                fazendas_selecionadas = st.multiselect(
                    "Fazendas disponíveis",
                    usuarios,
                    default=usuarios if selecionar_todas_fazendas else [],
                    key="fazendas"
                )

                if not fazendas_selecionadas:
                    st.warning("⚠️ Selecione pelo menos uma fazenda")
                    return [], [], [], []

                # 2. Filtrar DataFrame baseado nas fazendas selecionadas
                df_filtrado = self.df[self.df["Usuário"].isin(fazendas_selecionadas)]
                
                # 3. Classes de Equipamento
                st.markdown("##### 2. Filtre por Classe")
                tipos_equipamento = sorted(df_filtrado["Classe"].unique())
                col_check_classe, col_total_classes = st.columns([3, 1])
                with col_check_classe:
                    selecionar_todos_tipos = st.checkbox(
                        "Selecionar todas as classes",
                        key="todas_classes"
                    )
                with col_total_classes:
                    st.markdown(f"Total: {len(tipos_equipamento)}")

                tipo = st.multiselect(
                    "Classes de equipamento",
                    tipos_equipamento,
                    default=tipos_equipamento if selecionar_todos_tipos else [],
                    key="classes"
                )

                # 4. Equipamentos
                st.markdown("##### 3. Selecione os Equipamentos (opcional)")
                # Filtrar equipamentos baseado nas classes selecionadas
                df_filtrado = df_filtrado[df_filtrado["Classe"].isin(tipo)] if tipo else df_filtrado
                equipamentos = sorted(df_filtrado["Equipamento"].unique())
                
                col_check_equip, col_total_equip = st.columns([3, 1])
                with col_check_equip:
                    selecionar_todos_equip = st.checkbox(
                        "Selecionar todos os equipamentos",
                        key="todos_equip"
                    )
                with col_total_equip:
                    st.markdown(f"Total: {len(equipamentos)}")

                equipamentos_selecionados = st.multiselect(
                    "Equipamentos disponíveis",
                    equipamentos,
                    default=equipamentos if selecionar_todos_equip else [],
                    key="equipamentos"
                )

                # 5. Modelos
                df_filtrado = df_filtrado[df_filtrado["Equipamento"].isin(equipamentos_selecionados)] if equipamentos_selecionados else df_filtrado
                modelos = sorted(df_filtrado["Modelo/Versão"].unique())
                
                st.markdown("##### 4. Filtre por Modelo (opcional)")
                col_check_modelo, col_total_modelo = st.columns([3, 1])
                with col_check_modelo:
                    selecionar_todos_modelos = st.checkbox(
                        "Selecionar todos os modelos",
                        key="todos_modelos"
                    )
                with col_total_modelo:
                    st.markdown(f"Total: {len(modelos)}")

                modelos_selecionados = st.multiselect(
                    "Modelos disponíveis",
                    modelos,
                    default=modelos if selecionar_todos_modelos else [],
                    key="modelos"
                )
                
            # 6: Seleção do período em meses
            st.markdown("##### 5. Selecione o Período (Meses)")
            self.meses_ajuste = st.number_input(
                "Meses",
                min_value=1,
                max_value=12,
                value=6,
                step=1
            )

            # 7. Botão para limpar filtros
            if st.button("🔄 Limpar Todos os Filtros", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.rerun()

            return tipo, fazendas_selecionadas, equipamentos_selecionados, modelos_selecionados
        else:
            st.warning("Por favor, carregue os dados primeiro.")
            return [], [], [], []
                
    def filtrar_dados(self, tipo_selecionado, usuario_selecionado, equipamentos_selecionados, modelos_selecionados):
        """
        Filtra os dados com base nas seleções feitas pelo usuário.
        """
        mask = pd.Series(True, index=self.df.index)
        
        if tipo_selecionado:
            mask &= self.df["Classe"].isin(tipo_selecionado)
        if usuario_selecionado:
            mask &= self.df["Usuário"].isin(usuario_selecionado)
        if equipamentos_selecionados:
            mask &= self.df["Equipamento"].isin(equipamentos_selecionados)
        if modelos_selecionados:
            mask &= self.df["Modelo/Versão"].isin(modelos_selecionados)
        
        # Criar uma cópia explícita do DataFrame filtrado
        self.df_filtrado = self.df[mask].copy()

    def calcular_excedente(self, realizado, orcado, meses_ajuste):
        """
        Calcula o valor excedente entre realizado e orçado ajustado pelo período
        """
        orcado_ajustado = orcado / 12 * meses_ajuste
        return np.maximum(0, realizado - orcado_ajustado)

    def ajustar_valores(self):
        """
        Ajusta os valores planejados proporcionalmente ao período de ajuste.
        """

        # Validação do período
        if not self.meses_ajuste or self.meses_ajuste < 1:
            self.meses_ajuste = 6  # valor default

        # Ajuste do uso estimado
        self.df_filtrado["Uso Estimado Ajustado"] = (
            self.df_filtrado["Uso (km ou hora) Estimado"] / 12 * self.meses_ajuste
        )
        
        # Ajuste dos custos planejados (Peças/Serviços + Reforma)
        self.df_filtrado["Custo Planejado Ajustado"] = (
            (self.df_filtrado["Peças, Serviços e Pneus Orçado"] / 12 * self.meses_ajuste) + 
            (self.df_filtrado["Reforma Orçada"] / 12 * self.meses_ajuste)
        )
        
        # Cálculo do custo excedente total
        self.df_filtrado["Custo Excedente"] = (
            # INSUMOS
            self.calcular_excedente(self.df_filtrado["Lubrificantes Realizado"], 
                                self.df_filtrado["Lubrificantes Orçado"],
                                self.meses_ajuste) +
            self.calcular_excedente(self.df_filtrado["Filtros Realizado"],  # Use o nome exato da coluna após normalização
                                self.df_filtrado["Filtros Orçado"],
                                self.meses_ajuste) +
            self.calcular_excedente(self.df_filtrado["Graxas Realizado"],
                                self.df_filtrado["Graxas Orçado"],
                                self.meses_ajuste) +
            # MANUTENÇÃO
            self.calcular_excedente(self.df_filtrado["Peças, Serviços e Pneus Realizado"],
                                self.df_filtrado["Peças, Serviços e Pneus Orçado"],
                                self.meses_ajuste) +
            self.calcular_excedente(self.df_filtrado["Reforma Realizada"],
                                self.df_filtrado["Reforma Orçada"],
                                self.meses_ajuste)
        )

        self.df_filtrado["Total Realizado"] = self.df_filtrado["Custo Excedente"]

    def calcular_multiplicador(
        self, realizado, orcado_ajustado, uso_realizado_ajustado, uso_estimado_ajustado
    ):
        """
        Função auxiliar para calcular multiplicadores.
        """
        return np.divide(
            realizado / uso_realizado_ajustado,
            orcado_ajustado / uso_estimado_ajustado,
            out=np.zeros_like(realizado, dtype=float),
            where=(np.abs(uso_estimado_ajustado) > 1e-6) & (np.abs(uso_realizado_ajustado) > 1e-6),  # Evita divisão por zero
        )

    def calcular_indicadores(self):
        """
        Calcula os indicadores para os dados filtrados e ajustados.
        Inclui cálculos proporcionais de custos.
        """
        df = self.df_filtrado

        # 1. Cálculos de Uso (mantidos)
        # Ajustar unidades de uso conforme medidor
        df["Uso Realizado Ajustado"] = np.where(
            df["Medidor"] == "KM",
            df["Uso (km ou hora) Realizado"],
            df["Uso (km ou hora) Realizado"] * 1
        )

        # Ajustar valores planejados base período
        df["Uso Estimado Ajustado"] = (
            df["Uso (km ou hora) Estimado"] / 12 * self.meses_ajuste
        )

        # Taxa de Utilização
        df["Taxa Utilização Multiplicador"] = (
            df["Uso Realizado Ajustado"] / df["Uso Estimado Ajustado"]
        )

        # 2. Cálculos de Consumo (mantidos)
        # Ajuste combustível planejado
        df["Combustível Planejado Ajustado"] = (
            df["Combustíveis (l) Orçado"] / 12 * self.meses_ajuste
        )

        # Consumo por unidade
        df["Consumo Planejado por Unidade"] = (
            df["Combustível Planejado Ajustado"] / df["Uso Estimado Ajustado"]
        )

        df["Consumo Realizado por Unidade"] = (
            df["Combustíveis (l) Realizado"] / df["Uso Realizado Ajustado"]
        )

        df["Consumo Multiplicador"] = (
            df["Consumo Realizado por Unidade"] / df["Consumo Planejado por Unidade"]
        )

        # 3. NOVOS Cálculos Proporcionais
        # Função auxiliar para cálculo de proporção
        def calcular_proporcao(realizado, orcado, meses):
            orcado_ajustado = orcado / 12 * meses
            return np.where(orcado_ajustado > 0, 
                        realizado / orcado_ajustado, 
                        np.where(realizado > 0, np.inf, 0))

        # Insumos
        df["Lubrificantes Proporcao"] = calcular_proporcao(
            df["Lubrificantes Realizado"],
            df["Lubrificantes Orçado"],
            self.meses_ajuste
        )

        df["Filtros Proporcao"] = calcular_proporcao(
            df["Filtros Realizado"], 
            df["Filtros Orçado"],
            self.meses_ajuste
        )

        df["Graxas Proporcao"] = calcular_proporcao(
            df["Graxas Realizado"],
            df["Graxas Orçado"],
            self.meses_ajuste
        )

        # Manutenção
        df["PSP Proporcao"] = calcular_proporcao(
            df["Peças, Serviços e Pneus Realizado"],
            df["Peças, Serviços e Pneus Orçado"],
            self.meses_ajuste
        )

        df["Reforma Proporcao"] = calcular_proporcao(
            df["Reforma Realizada"],
            df["Reforma Orçada"],
            self.meses_ajuste
        )


# 4. Ponto de Entrada: Main
if __name__ == "__main__":

    st.title("Análise de Indicadores de Equipamentos")
    
    # Criar duas colunas principais com proporção ajustada
    col_filtros, col_resultados = st.columns([1, 3])  # Proporção 1:3 para melhor uso do espaço
    
    # Coluna da esquerda: Filtros
    with col_filtros:
        st.markdown("### Dados e Filtros")
        # Remover padding extra
        st.markdown("""
            <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
                .element-container {
                    margin-bottom: 0.5rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        yaml_path = "./frota_mapa.yaml"
        analise = AnaliseIndicadores(yaml_path)
        analise.df = analise.data_loader.carregar_arquivo()
        analise.meses_ajuste = 6  # valor default

    # Coluna da direita: Resultados
    with col_resultados:
        if analise.df is not None:
            # Voltar para coluna da esquerda para mostrar filtros
            with col_filtros:
                tipo, usuario, equipamentos, modelos = analise.criar_interface()
                if any([tipo, usuario, equipamentos, modelos]):
                    analise.filtrar_dados(tipo, usuario, equipamentos, modelos)
                    # Criar uma linha horizontal para separar
                    st.markdown("---")

            # Voltar para coluna da direita para mostrar resultados
            with col_resultados:
                if any([tipo, usuario, equipamentos, modelos]):
                    analise.ajustar_valores()
                    analise.calcular_indicadores()

                    # Gerar gráficos e tabela resumo
                    graph_generator = GraphGenerator(
                        analise.df_filtrado,
                        analise.data_loader.configuracoes
                    )
                    
                    # Ajustar tamanho do gráfico
                    st.markdown("""
                        <style>
                            .plotly-graph-div {
                                margin: 0 auto;
                                width: 100% !important;
                            }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    graph_generator.gerar_grafico_barras()
                    graph_generator.exibir_tabela_resumo()
                    