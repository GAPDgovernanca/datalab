# GAPDgovernanca/datalab

## Estrutura do Repositório

```
└───datalab
    ├───.devcontainer
    ├───1_apps
    │   ├───linux
    │   │   ├───5S_librecalc_macros
    │   │   ├───frota
    │   │   ├───frota_etl
    │   │   │   ├───database
    │   │   │   └───transformador
    │   │   ├───frota_llm
    │   │   │   └───backup
    │   │   ├───mindpub
    │   │   └───sjudas
    │   │       ├───confinamento_batidas_histogramas
    │   │       │   ├───.ipynb_checkpoints
    │   │       │   └───instructions
    │   │       ├───confinamento_batidas_trendline
    │   │       ├───confinamento_horarios
    │   │       └───confinamento_resources
    │   └───win
    │       ├───AD_excel_macros
    │       └───heatmap
    │           ├───public
    │           └───src
    │               └───components
    ├───2_labs
    │   ├───linux
    │   │   ├───ad_analysis
    │   │   ├───ajustes_b3
    │   │   ├───analise-sensibilidade-gado
    │   │   │   ├───public
    │   │   │   └───src
    │   │   │       └───components
    │   │   ├───conselho_atas_de_reuniao
    │   │   ├───dash
    │   │   ├───frota_llm_versao_v2
    │   │   │   └───documentacao
    │   │   ├───mosaico_confinamento
    │   │   │   ├───public
    │   │   │   └───src
    │   │   │       └───components
    │   │   │           ├───mosaico
    │   │   │           └───ui
    │   │   └───yaml_files
    │   └───win
    │       ├───mec
    │       ├───mec_der
    │       │   └───lib
    │       │       ├───bindings
    │       │       ├───tom-select
    │       │       └───vis-9.1.2
    │       └───mec_sql_queries
    ├───3_prompts
    ├───4_gpt_devolutiva
    └───lib
        ├───bindings
        ├───tom-select
        └───vis-9.1.2
```

## Descrição

GAPD é um repositório dedicado a ferramentas, laboratórios e prompts para processamento automatizado de dados e geração de dashboards.

## Componentes Principais

- **1_apps**: Aplicações para sistemas Linux e Windows
- **2_labs**: Laboratórios de desenvolvimento para diferentes sistemas operacionais
- **3_prompts**: Coleção de prompts para análise de dados, geração de dashboards e outras tarefas
- **4_GPT_base_de_conhecimento_devolutiva**: Base de conhecimento para GPT com foco em devolutivas
- **lib**: Bibliotecas e dependências do projeto

## Requisitos

Para instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

Última atualização: 11 de março de 2025
