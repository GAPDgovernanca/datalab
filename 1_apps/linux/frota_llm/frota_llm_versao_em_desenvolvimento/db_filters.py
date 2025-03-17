from typing import Dict
import pandas as pd
import sqlite3

def build_filters(filtros: Dict, alias: str = 'fc') -> str:
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
    Marca em vermelho (🔴) quando o total_diferenca < 0 e for maior que 10% em magnitude
    (ou seja, quando houve um estouro significativo de orçamento).
    Marca em verde (🟢) quando há sobra de orçamento acima de 10%.
    Sinal neutro (⚪) quando estiver dentro da faixa de -10% a +10%.
    🔶 se não havia orçamento (0) mas houve custo > 0.
    """
    def flag_diferenca(row):
        # Caso especial: não havia orçamento (0), mas houve custo realizado > 0
        if row['total_estimado'] == 0 and row['total_realizado'] > 0:
            return '🔶'

        # Se havia orçamento, analisamos o 'total_diferenca' (estimado - realizado)
        if row['total_estimado'] != 0:
            # Calcula o desvio percentual com base em total_diferenca
            percentual = (row['total_diferenca'] / row['total_estimado']) * 100

            # Se o valor for menor que -10%, significa que realizamos bem mais do que o estimado
            # (houve estouro de orçamento) => vermelho (🔴)
            if percentual < -10:
                return '🔴'

            # Se o valor for maior que +10%, significa que gastamos bem menos do que o estimado
            # (houve sobra de orçamento) => verde (🟢)
            elif percentual > 10:
                return '🟢'

        # Caso contrário, fica neutro (⚪)
        return '⚪'

    df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df

