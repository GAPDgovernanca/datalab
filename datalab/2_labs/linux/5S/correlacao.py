#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# Carregar mapeamento YAML das perguntas
def carregar_mapeamento(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Processar CSV para formato analítico adequado
def processar_csv(csv_path, yaml_path, incluir_dimensoes=True):
    df_raw = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')

    mapeamento = carregar_mapeamento(yaml_path)
    perguntas_dict = {k: v for d in mapeamento['dimensoes'].values() for k, v in d.items()}

    perguntas_originais = df_raw.iloc[:, 0].tolist()

    dados = {}
    for col in df_raw.columns[1:]:
        notas = pd.to_numeric(df_raw[col][1:], errors='coerce')
        dados[col] = notas.values

    df_processado = pd.DataFrame(dados, index=perguntas_originais[1:])
    df_processado = df_processado.rename(index=perguntas_dict)

    # Remover itens não desejados, mantendo dimensões principais opcionalmente
    itens_descartar = ['FOTOGRAFIAS', 'Response Type', 'DATAS', 'Submit Date (UTC)']
    if not incluir_dimensoes:
        itens_descartar += ['DIMENSÃO LIMPEZA', 'DIMENSÃO ORGANIZAÇÃO', 'DIMENSÃO ARRUMAÇÃO']

    df_processado = df_processado.drop(itens_descartar, errors='ignore')

    return df_processado.transpose()

# Gerar diagrama de correlação
def gerar_diagrama_correlacao(df):
    plt.figure(figsize=(15, 12))
    sns.heatmap(
        df.corr(),
        annot=True,
        cmap='RdYlGn',
        fmt='.2f',
        linewidths=0.5,
        center=0,
        annot_kws={"size":10},
        xticklabels=df.columns,
        yticklabels=df.columns
    )
    plt.title('Matriz de Correlação entre Perguntas (Escala Invertida)', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    plt.savefig('matriz_correlacao_5S.png', dpi=300)
    plt.show()

# Função principal
if __name__ == "__main__":
    # Altere aqui para True ou False para incluir ou não as dimensões no diagrama
    df = processar_csv('silos.csv', 'perguntas.yaml', incluir_dimensoes=True)
    gerar_diagrama_correlacao(df)

# Para dar permissão ao arquivo no Ubuntu, execute no terminal:
# chmod +x correlacao.py
# ./correlacao.py