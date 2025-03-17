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

def apply_flags(df: pd.DataFrame) -> pd.DataFrame:
    def flag_diferenca(row):
        # Caso especial: sem orçamento, mas com custo realizado
        if row['total_estimado'] == 0 and row['total_realizado'] > 0:
            return '🔶'
        if row['total_estimado'] != 0:
            percentual = (row['total_realizado'] - row['total_estimado']) / row['total_estimado'] * 100
            if percentual > 10:
                return '🟢'
            elif percentual < -10:
                return '🔴'
        return '⚪'
    df['Sinalizador'] = df.apply(flag_diferenca, axis=1)
    return df
