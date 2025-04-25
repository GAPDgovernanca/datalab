"""
Módulo de filtros e cálculos para o dashboard.

Este módulo mantém a estrutura original para consultas ao banco de dados,
os cálculos de multiplicadores e a aplicação de sinalizadores (flags).

Importante:
- Nenhum nome de variável ou assinatura de função foi alterado, garantindo a compatibilidade com o restante do sistema.
- A configuração dos sinalizadores está centralizada no arquivo db_config.yaml, que agora é carregado utilizando
  um caminho absoluto baseado no local deste arquivo, para funcionar corretamente no Streamlit Cloud.
"""

import os
import yaml
from typing import Dict
import pandas as pd
import sqlite3

# Define o caminho absoluto para o arquivo db_config.yaml (localizado no mesmo diretório deste módulo)
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_config.yaml")

# Lista das chaves obrigatórias que devem estar definidas no arquivo YAML.
REQUIRED_CONFIG_KEYS = [
    "threshold_percentage",
    "flag_over_threshold",
    "flag_under_threshold",
    "flag_neutral",
    "flag_no_budget"
]

def load_config():
    """
    Carrega a configuração do arquivo YAML.
    
    Lança um FileNotFoundError se o arquivo não for encontrado
    e um KeyError se alguma chave obrigatória estiver ausente.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Arquivo {CONFIG_FILE} não encontrado. Por favor, verifique se 'db_config.yaml' está no mesmo diretório de 'db_filters.py'."
        )
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}
    
    # Verifica se todas as chaves obrigatórias estão presentes
    for key in REQUIRED_CONFIG_KEYS:
        if key not in config:
            raise KeyError(
                f"A chave '{key}' está ausente na configuração ({CONFIG_FILE}). Adicione essa chave para continuar."
            )
    return config

# Carrega as configurações de sinalizadores utilizando o caminho absoluto para o arquivo YAML.
CONFIG = load_config()

def build_filters(filtros: Dict, alias: str = 'fc') -> str:
    """
    Constrói uma string de condições SQL a partir dos filtros fornecidos.
    
    Mantém a compatibilidade com as demais partes do sistema.
    """
    conditions = []
    data_referencia = filtros.get("data_referencia")
    if data_referencia and len(data_referencia) == 2:
        start_date, end_date = data_referencia
        conditions.append(f"{alias}.data_referencia BETWEEN '{start_date}' AND '{end_date}'")
    if filtros.get("id_equipamento"):
        ids = ",".join(map(str, filtros["id_equipamento"]))
        conditions.append(f"{alias}.id_equipamento IN ({ids})")
    if filtros.get("usuario") and "Todos" not in filtros["usuario"]:
        usuarios = "', '".join(filtros["usuario"])
        conditions.append(f"de.usuario IN ('{usuarios}')")
    if filtros.get("classe") and "Todos" not in filtros["classe"]:
        classes = "', '".join(filtros["classe"])
        conditions.append(f"de.classe IN ('{classes}')")
    return " AND ".join(conditions)

def calcular_multiplicadores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula dois multiplicadores:
      - Taxa Utilização Multiplicador: custo_hora_realizado / custo_hora_estimado
      - Consumo Multiplicador: total_realizado / total_estimado

    A divisão por zero é evitada (retorna 0.0 nesses casos).
    """
    if df.empty:
        return df
    df['Taxa Utilização Multiplicador'] = df.apply(
        lambda row: row['custo_hora_realizado'] / row['custo_hora_estimado']
        if row['custo_hora_estimado'] != 0 else 0.0,
        axis=1
    )
    df['Consumo Multiplicador'] = df.apply(
        lambda row: row['total_realizado'] / row['total_estimado']
        if row['total_estimado'] != 0 else 0.0,
        axis=1
    )
    return df

def apply_flags(df):
    """
    Aplica sinalizadores (flags) aos registros do DataFrame com base no desvio percentual entre o orçamento e o realizado.

    Critérios:
      - Se total_estimado == 0 e total_realizado > 0, retorna CONFIG["flag_no_budget"].
      - Se total_estimado != 0, calcula:
            percentual = (total_diferenca / total_estimado) * 100
        (Espera-se que total_diferenca seja calculado como: total_orçado - total_realizado)
      - Se percentual < -CONFIG["threshold_percentage"], retorna CONFIG["flag_under_threshold"].
      - Se percentual > CONFIG["threshold_percentage"], retorna CONFIG["flag_over_threshold"].
      - Para desvios entre -CONFIG["threshold_percentage"] e CONFIG["threshold_percentage"], retorna CONFIG["flag_neutral"].

    OBSERVAÇÃO:
      A configuração dos sinalizadores está centralizada no arquivo db_config.yaml.
    """
    def flag_diferenca(row):
        # Caso especial: orçamento zero mas custo realizado > 0.
        if row['total_estimado'] == 0 and row['total_realizado'] > 0:
            return CONFIG["flag_no_budget"]

        if row['total_estimado'] != 0:
            percentual = (row['total_diferenca'] / row['total_estimado']) * 100
            if percentual < -CONFIG["threshold_percentage"]:
                return CONFIG["flag_under_threshold"]
            elif percentual > CONFIG["threshold_percentage"]:
                return CONFIG["flag_over_threshold"]

        return CONFIG["flag_neutral"]

    df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df
