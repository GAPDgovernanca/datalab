import csv
import os
import json
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import PySimpleGUI as sg
import matplotlib

# Configuração do backend do Matplotlib para evitar problemas de renderização
matplotlib.use("TkAgg")


# Funções de conversão
def converter_valor_monetario(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if valor == "-" or not valor:
            return 0.0
        valor = valor.replace("R$ ", "")
        is_negative = False
        if valor.startswith("(") and valor.endswith(")"):
            is_negative = True
            valor = valor[1:-1]
        try:
            valor = float(valor.replace(".", "").replace(",", "."))
        except ValueError:
            return 0.0
        return -valor if is_negative else valor
    return valor


def converter_valor_numerico(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor or valor == "-":
            return 0.0
        try:
            return float(valor.replace(".", "").replace(",", "."))
        except ValueError:
            return 0.0
    return valor


# Funções auxiliares
def validar_celula(valor):
    if valor is None:
        return True
    if isinstance(valor, str):
        valor = valor.strip()
        return valor == "" or valor == "-" or valor.isspace()
    return False


def tratar_valor_ausente(valor, tipo="numerico"):
    if validar_celula(valor):
        return 0.0
    if tipo == "monetario":
        return converter_valor_monetario(valor)
    return converter_valor_numerico(valor)


# Classes e Funções de Processamento de Dados
class ProcessadorDados:
    def __init__(self):
        self.secoes = {
            "reformas": [],
            "motorizados": [],
            "implementos": [],
            "terceiros": [],
        }

    def identificar_secao(self, linha):
        linha_str = ",".join(linha).lower()
        if "equipamentos motorizados" in linha_str:
            return "motorizados"
        elif "implementos" in linha_str:
            return "implementos"
        elif "terceiros" in linha_str:
            return "terceiros"
        return None

    def eh_cabecalho(self, linha):
        cabecalhos_possiveis = [
            "orcado",
            "realizado",
            "frota",
            "modelo",
            "classe",
            "operacao",
        ]
        return any(
            cabecalho.lower() in linha[0].lower() for cabecalho in cabecalhos_possiveis
        )

    def normalizar_linha(self, linha, tipo_secao):
        if tipo_secao == "reformas":
            if len(linha) >= 5:
                return {
                    "id": linha[0].strip(),
                    "modelo": linha[1].strip(),
                    "orcado": tratar_valor_ausente(linha[2], "monetario"),
                    "realizado": tratar_valor_ausente(linha[3], "monetario"),
                    "diferenca": tratar_valor_ausente(linha[3], "monetario")
                    - tratar_valor_ausente(linha[2], "monetario"),
                }
        elif tipo_secao == "motorizados":
            if len(linha) >= 17:
                return {
                    "frota": linha[0].strip(),
                    "modelo": linha[1].strip(),
                    "classe": linha[2].strip(),
                    "orcado": tratar_valor_ausente(linha[3], "monetario"),
                    "realizado": tratar_valor_ausente(linha[4], "monetario"),
                    "diferenca": tratar_valor_ausente(linha[4], "monetario")
                    - tratar_valor_ausente(linha[3], "monetario"),
                    "horas_orcadas": tratar_valor_ausente(linha[12], "numerico"),
                    "horas_realizadas": tratar_valor_ausente(linha[13], "numerico"),
                }
        elif tipo_secao == "implementos":
            if len(linha) >= 12:
                return {
                    "frota": linha[0].strip(),
                    "modelo": linha[1].strip(),
                    "classe": linha[2].strip(),
                    "orcado": tratar_valor_ausente(linha[3], "monetario"),
                    "realizado": tratar_valor_ausente(linha[4], "monetario"),
                    "diferenca": tratar_valor_ausente(linha[4], "monetario")
                    - tratar_valor_ausente(linha[3], "monetario"),
                    "falta_realizar": tratar_valor_ausente(linha[5], "monetario"),
                }
        elif tipo_secao == "terceiros":
            if len(linha) >= 2:
                return {
                    "operacao": linha[0].strip(),
                    "valor": tratar_valor_ausente(linha[1], "monetario"),
                }
        return None

    def processar_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            secao_atual = "reformas"
            for linha in reader:
                nova_secao = self.identificar_secao(linha)
                if nova_secao:
                    secao_atual = nova_secao
                    continue
                if self.eh_cabecalho(linha):
                    continue
                dados = self.normalizar_linha(linha, secao_atual)
                if dados:
                    self.secoes[secao_atual].append(dados)

    def calcular_metricas(self):
        metricas = {}
        for secao, dados in self.secoes.items():
            metricas[secao] = {
                "total_orcado": sum(d.get("orcado", 0) for d in dados),
                "total_realizado": sum(d.get("realizado", 0) for d in dados),
                "total_diferenca": sum(d.get("diferenca", 0) for d in dados),
                "quantidade": len(dados),
            }
            if secao == "motorizados":
                metricas[secao].update(
                    {
                        "total_horas_orcadas": sum(
                            d.get("horas_orcadas", 0) for d in dados
                        ),
                        "total_horas_realizadas": sum(
                            d.get("horas_realizadas", 0) for d in dados
                        ),
                    }
                )
        return metricas

    def filtrar_por_classe(self, classe):
        dados_filtrados = []
        for dados in self.secoes["motorizados"]:
            if dados.get("classe") == classe:
                dados_filtrados.append(dados)
        return dados_filtrados

    def obter_categorias_classe(self):
        categorias = set()
        for dados in self.secoes["motorizados"]:
            categorias.add(dados.get("classe"))
        return list(categorias)


# Função para visualização de dados em 3D
def gerar_graficos_3d(
    metricas, coluna_explodir, classe_especifica=None, dados_filtrados=None
):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    cores = matplotlib.colormaps.get_cmap("viridis")

    if classe_especifica and dados_filtrados:
        x_labels = [classe_especifica]
        x_pos = np.arange(len(x_labels))
        y_labels = [
            label
            for label in dados_filtrados[0].keys()
            if label not in ["classe", "modelo", "frota"]
        ]
        if coluna_explodir and coluna_explodir in y_labels:
            y_labels = [coluna_explodir]
        y_pos = np.arange(len(y_labels))

        x, y = np.meshgrid(x_pos, y_pos)
        z = np.zeros_like(x)
        dz = np.array(
            [
                float(tratar_valor_ausente(dados_filtrados[0][label], "numerico"))
                for label in y_labels
            ]
        )

        for j in range(len(y_labels)):
            cor = (
                "red"
                if y_labels[j] == "diferenca" and dz[j] < 0
                else (
                    "green" if y_labels[j] == "diferenca" and dz[j] >= 0 else cores(0.5)
                )
            )
            ax.bar3d(
                x.flatten()[j],
                y.flatten()[j],
                z.flatten()[j],
                0.4,
                0.4,
                dz[j],
                shade=True,
                color=cor,
            )
            # Adiciona rótulo na parte superior da barra
            ax.text(
                x.flatten()[j],
                y.flatten()[j],
                dz[j],
                f"{dz[j]:.2f}",
                ha="center",
                va="bottom",
            )
    else:
        x_labels = list(metricas.keys())
        x_pos = np.arange(len(x_labels))

        for i, secao in enumerate(metricas.keys()):
            valores = metricas[secao]
            y_labels = list(valores.keys())[1:]  # Ignorando a chave 'quantidade'
            if coluna_explodir and coluna_explodir in y_labels:
                y_labels = [coluna_explodir]
            y_pos = np.arange(len(y_labels))

            x, y = np.meshgrid(x_pos[i : i + 1], y_pos)
            z = np.zeros_like(x)
            dz = np.array([float(valores[label]) for label in y_labels])

            for j in range(len(y_labels)):
                cor = (
                    "red"
                    if y_labels[j] == "total_diferenca" and dz[j] < 0
                    else (
                        "green"
                        if y_labels[j] == "total_diferenca" and dz[j] >= 0
                        else cores(i / len(metricas))
                    )
                )
                ax.bar3d(
                    x.flatten()[j],
                    y.flatten()[j],
                    z.flatten()[j],
                    0.4,
                    0.4,
                    dz[j],
                    shade=True,
                    color=cor,
                )
                # Adiciona rótulo na parte superior da barra
                ax.text(
                    x.flatten()[j],
                    y.flatten()[j],
                    dz[j],
                    f"{dz[j]:.2f}",
                    ha="center",
                    va="bottom",
                )

    ax.set_xlabel("Seções")
    ax.set_ylabel("Métricas")
    ax.set_zlabel("Valores")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels, rotation=45)
    plt.tight_layout()
    plt.show()


# Execução principal com interface interativa
def interface_usuario():
    layout = [
        [sg.Text("Selecione o arquivo CSV de dados:"), sg.Input(), sg.FileBrowse()],
        [
            sg.Text("Escolha a coluna para explodir:"),
            sg.Combo(
                [
                    "total_orcado",
                    "total_realizado",
                    "total_diferenca",
                    "quantidade",
                    "total_horas_orcadas",
                    "total_horas_realizadas",
                ],
                key="coluna_explodir",
            ),
        ],
        [
            sg.Text("Escolha uma classe para filtrar (opcional):"),
            sg.InputText(key="classe_filtrar"),
        ],
        [
            sg.Button("Processar Dados"),
            sg.Button("Listar Categorias de Classe"),
            sg.Button("Cancelar"),
        ],
    ]

    window = sg.Window("Análise de Gestão de Frotas", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            break
        if event == "Processar Dados":
            caminho_arquivo = values[0]
            coluna_explodir = values["coluna_explodir"]
            classe_especifica = values["classe_filtrar"]
            if os.path.exists(caminho_arquivo):
                processador = ProcessadorDados()
                processador.processar_arquivo(caminho_arquivo)
                metricas = processador.calcular_metricas()
                dados_filtrados = None
                if classe_especifica:
                    dados_filtrados = processador.filtrar_por_classe(classe_especifica)
                    if not dados_filtrados:
                        sg.popup(
                            f"Nenhum dado encontrado para a classe: {classe_especifica}"
                        )
                        continue
                with open("metricas.json", "w") as f:
                    json.dump(metricas, f, indent=4)
                gerar_graficos_3d(
                    metricas, coluna_explodir, classe_especifica, dados_filtrados
                )
            else:
                sg.popup(
                    "Arquivo não encontrado. Por favor, selecione um arquivo válido."
                )
        if event == "Listar Categorias de Classe":
            caminho_arquivo = values[0]
            if os.path.exists(caminho_arquivo):
                processador = ProcessadorDados()
                processador.processar_arquivo(caminho_arquivo)
                categorias = processador.obter_categorias_classe()
                sg.popup("Categorias de Classe:", ", ".join(categorias))
            else:
                sg.popup(
                    "Arquivo não encontrado. Por favor, selecione um arquivo válido."
                )

    window.close()


if __name__ == "__main__":
    interface_usuario()
