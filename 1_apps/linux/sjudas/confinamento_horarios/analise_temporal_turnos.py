import pandas as pd
from datetime import time

# Função para determinar o turno com base no horário
# Manhã: 06:00 - 12:00
# Tarde: 12:00 - 18:00
# Noite: 18:00 - 06:00 (do próximo dia)

def determinar_turno(horario):
    """
    Função para determinar o turno de um horário específico.

    Args:
    - horario (datetime.time): O horário para o qual se quer identificar o turno.

    Returns:
    - str: O turno correspondente (manhã, tarde, noite).
    """
    if time(6, 0) <= horario < time(12, 0):
        return "Manhã"
    elif time(12, 0) <= horario < time(18, 0):
        return "Tarde"
    else:
        return "Noite"

# Função para adicionar a coluna de turno ao DataFrame
def adicionar_coluna_turno(df, coluna_fim):
    """
    Função para adicionar uma coluna de turno ao DataFrame com base nos horários de 'FIM'.

    Args:
    - df (DataFrame): DataFrame contendo os dados das batidas.
    - coluna_fim (str): Nome da coluna que contém os horários de 'FIM'.

    Returns:
    - DataFrame: DataFrame atualizado com uma nova coluna 'Turno'.
    """
    try:
        # Verificar se a coluna 'FIM' existe
        if coluna_fim not in df.columns:
            raise ValueError(f"A coluna '{coluna_fim}' não foi encontrada no DataFrame.")

        # Converter a coluna 'FIM' para datetime.time
        df[coluna_fim] = pd.to_datetime(df[coluna_fim], format='%H:%M:%S', errors='coerce').dt.time

        # Verificar se há valores nulos após a conversão (indicando problemas no formato)
        if df[coluna_fim].isnull().any():
            raise ValueError(f"Há valores nulos na coluna '{coluna_fim}' após tentativa de conversão. Verifique o formato dos dados.")

        # Adicionar a coluna 'Turno' ao DataFrame
        df['Turno'] = df[coluna_fim].apply(determinar_turno)

    except Exception as e:
        raise ValueError(f"Erro ao adicionar a coluna 'Turno': {e}")

    return df

# Função para realizar a análise temporal por turno
def analise_temporal_por_turno_ponderado(df):
    """
    Função para realizar a análise de variação dos turnos (manhã, tarde, noite) e calcular estatísticas relevantes.

    Args:
    - df (DataFrame): O DataFrame contendo as batidas e os turnos.

    Returns:
    - dict: Um dicionário contendo estatísticas por turno.
    """
    # Agrupar os dados pelo 'Turno'
    grupo_turno = df.groupby('Turno')

    # Calcular as estatísticas relevantes (ex.: média e desvio padrão das diferenças percentuais)
    estatisticas_por_turno = {
        turno: {
            'média_ponderada_diferença_percentual': grupo['MÉDIA PONDERADA (%)'].mean(),
            'desvio_padrao_diferença_percentual': grupo['MÉDIA PONDERADA (%)'].std(),
            'contagem_batidas': len(grupo)
        }
        for turno, grupo in grupo_turno
    }

    return estatisticas_por_turno
