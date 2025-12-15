# GAPDgovernanca/datalab

GAPD é um repositório dedicado a ferramentas, laboratórios e prompts para processamento automatizado de dados e geração de dashboards.

## Estrutura do Repositório

<details>
.
├── 1_apps
│   ├── linux
│   │   ├── 5S_librecalc_macros
│   │   │   ├── GAPD_5S2025_respostas_macroBASIC_processamento.bas
│   │   │   └── GAPD_confinamento_leitura_noturna_cocho.bas
│   │   ├── frota
│   │   │   ├── frota_mapa.yaml
│   │   │   ├── frota.py
│   │   │   └── requirements_frota.txt
│   │   ├── frota_etl
│   │   │   ├── database
│   │   │   │   ├── esquema.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── operacoes.py
│   │   │   ├── logger.py
│   │   │   ├── main.py
│   │   │   ├── relacionamentos.py
│   │   │   ├── relationships.txt
│   │   │   ├── requirements_frota_etl.txt
│   │   │   └── transformador
│   │   │   │   ├── excel.py
│   │   │   │   └── __init__.py
│   │   ├── frota_llm
│   │   │   ├── backup
│   │   │   │   ├── frota_llm.py
│   │   │   │   └── requirements.txt
│   │   │   ├── dashboard.py
│   │   │   ├── db_access.py
│   │   │   ├── db_filters.py
│   │   │   ├── KNIME - Prompt Completo para Query Consolidada.md
│   │   │   ├── list_frota_db.py
│   │   │   ├── llm_session.py
│   │   │   └── README.md
│   │   ├── mindpub
│   │   │   ├── CUMBUCA - plano de trabalho.md
│   │   │   ├── mindpub.py
│   │   │   └── README.txt
│   │   └── sjudas
│   │       ├── confinamento_batidas_histogramas
│   │       │   ├── batidas.py
│   │       │   ├── config.yaml
│   │       │   ├── instructions
│   │       │   │   ├── Entendendo os Pesos Relativos no Controle de Dietas.html
│   │       │   │   ├── formula_calculo.tex
│   │       │   │   ├── instructions_for_app_batidas.md
│   │       │   │   ├── ### Lista de Comandos para Commit.md
│   │       │   │   ├── pseudocode.md
│   │       │   │   └── requirements.md
│   │       │   ├── requirements.txt
│   │       │   └── sjudas - app batidas - prompt para refatorar o programa.md
│   │       ├── confinamento_horarios
│   │       │   ├── analise temporal turnos.md
│   │       │   ├── analise_temporal_turnos.py
│   │       │   ├── horario_curral.py
│   │       │   ├── horario_hex_periodo.py
│   │       │   ├── horario_hex.py
│   │       │   ├── horario_lote.py
│   │       │   └── hora.txt
│   │       └── confinamento_resources
│   └── win
│       ├── AD_excel_macros
│       │   └── GAPD_AD202425_respostas_macroVBA_processamento.bas
│       └── heatmap
│           ├── package.json
│           ├── package-lock.json
│           ├── postcss.config.js
│           ├── public
│           │   └── index.html
│           ├── src
│           │   ├── App.jsx
│           │   ├── components
│           │   │   └── Heatmap.jsx
│           │   ├── index.css
│           │   └── index.js
│           ├── tailwind.config.js
│           └── webpack.config.js
├── 2_labs
│   ├── gerenciamento do fluxo de versionamento
│   ├── linux
│   │   ├── 5S
│   │   │   ├── correlacao.py
│   │   │   ├── matriz_correlacao_5S.png
│   │   │   └── perguntas.yaml
│   │   ├── ad_analysis
│   │   │   └── EQassessment.ipynb
│   │   ├── ajustes_b3
│   │   │   ├── ajustes_b3.py
│   │   │   ├── endpoint.py
│   │   │   ├── main.py
│   │   │   ├── README.txt
│   │   │   └── requirements.txt
│   │   ├── analise-sensibilidade-gado
│   │   │   ├── package.json
│   │   │   ├── package-lock.json
│   │   │   ├── postcss.config.js
│   │   │   ├── public
│   │   │   │   ├── favicon.ico
│   │   │   │   ├── index.html
│   │   │   │   ├── logo192.png
│   │   │   │   ├── logo512.png
│   │   │   │   ├── manifest.json
│   │   │   │   └── robots.txt
│   │   │   ├── README.md
│   │   │   ├── src
│   │   │   │   ├── App.css
│   │   │   │   ├── App.js
│   │   │   │   ├── App.test.js
│   │   │   │   ├── components
│   │   │   │   │   └── CattleAnalysisApp.js
│   │   │   │   ├── index.css
│   │   │   │   ├── index.js
│   │   │   │   ├── logo.svg
│   │   │   │   ├── reportWebVitals.js
│   │   │   │   └── setupTests.js
│   │   │   └── tailwind.config.js
│   │   ├── api_groq
│   │   ├── biblioteca.html
│   │   ├── conselho_atas_de_reuniao
│   │   │   ├── 20240215 - ata de reunião.md
│   │   │   ├── 20240321 - ata de reunião.md
│   │   │   ├── 20240416 - ata de reunião.md
│   │   │   ├── gemini.py
│   │   │   └── mindmap.mmd
│   │   ├── dash
│   │   │   ├── 20241102 - dash do raizes do futuro.html
│   │   │   ├── dash_automotivo.py
│   │   │   ├── sjudas - dash da avaliacao 5S - guia do usuario.md
│   │   │   ├── sjudas - dash da avaliacao 5s - modelo bimestral.html
│   │   │   └── sjudas - dash da avaliacao 5s - modelo mensal.html
│   │   ├── Especificação de Requisitos de Software - Aplicativo de Análise de Sensibilidade.md
│   │   ├── Especificações Funcionais - Aplicativo de Análise de Sensibilidade.md
│   │   ├── frota_llm_versao_v2
│   │   │   ├── db.py
│   │   │   ├── documentacao
│   │   │   │   ├── Guideline para Desenvolvimento do Dashboard de Gestão de Frota Agrícola.md
│   │   │   │   ├── Guideline para o Módulo db_py.md
│   │   │   │   ├── Guideline para o Módulo filters_py.md
│   │   │   │   ├── Guideline para o Módulo ia_integration_py.md
│   │   │   │   ├── Guideline para o Módulo main_py.md
│   │   │   │   ├── Guideline para o Módulo processing_py.md
│   │   │   │   └── Guideline para o Módulo ui_py.md
│   │   │   └── test_database.py
│   │   ├── GAPD - pecuaria - resultados.md
│   │   ├── langchain_extrator_modelo.py
│   │   ├── mosaico_confinamento
│   │   │   ├── manual.md
│   │   │   ├── mosaico_qrcode.png
│   │   │   ├── package.json
│   │   │   ├── package-lock.json
│   │   │   ├── postcss.config.js
│   │   │   ├── public
│   │   │   │   ├── favicon.ico
│   │   │   │   ├── index.html
│   │   │   │   ├── logo192.png
│   │   │   │   ├── logo512.png
│   │   │   │   ├── manifest.json
│   │   │   │   └── robots.txt
│   │   │   ├── README.md
│   │   │   ├── src
│   │   │   │   ├── App.css
│   │   │   │   ├── App.test.tsx
│   │   │   │   ├── App.tsx
│   │   │   │   ├── components
│   │   │   │   │   ├── mosaico
│   │   │   │   │   │   └── imspv-mosaico-drill.tsx
│   │   │   │   │   └── ui
│   │   │   │   │   │   └── card.tsx
│   │   │   │   ├── globals.css
│   │   │   │   ├── index.css
│   │   │   │   ├── index.tsx
│   │   │   │   ├── logo.svg
│   │   │   │   ├── react-app-env.d.ts
│   │   │   │   ├── reportWebVitals.ts
│   │   │   │   └── setupTests.ts
│   │   │   ├── tailwind.config.js
│   │   │   └── tsconfig.json
│   │   └── yaml_files
│   └── win
│       ├── hedge_pec
│       │   ├── payoff_opcoes_base_app.py
│       │   └── requirements.txt
│       ├── mec
│       │   ├── analisar_dados.py
│       │   ├── automotive_analysis.py
│       │   ├── base MEC.md
│       │   ├── conector.py
│       │   ├── consultasimples.py
│       │   ├── listar_tabelas.py
│       │   ├── maintenance_predictor.py
│       │   ├── MEC_relacionamentos.csv
│       │   ├── modelo_preditivo.py
│       │   ├── predictive_analytics.py
│       │   ├── predictive_analytics_v2.py
│       │   ├── predictive_analytics_v3.py
│       │   ├── relacionamentos.xlsx
│       │   ├── RelatorioAnomaliasManutencao.pdf
│       │   ├── RelatorioDesviosManutencao.pdf
│       │   ├── RelatorioManutencao.pdf
│       │   ├── RelatorioManutencaoPrioritaria.pdf
│       │   └── sqlopenai.py
│       ├── mec_der
│       │   ├── lib
│       │   │   ├── bindings
│       │   │   │   └── utils.js
│       │   │   ├── tom-select
│       │   │   │   ├── tom-select.complete.min.js
│       │   │   │   └── tom-select.css
│       │   │   └── vis-9.1.2
│       │   │   │   ├── vis-network.css
│       │   │   │   └── vis-network.min.js
│       │   ├── mec_der_geral_lista.html
│       │   ├── mec_der_geral_lista.py
│       │   └── mec_der_seletor.py
│       ├── mec_sql_queries
│       │   ├── Criacao_Tabela_Mineracao_OS.sql
│       │   ├── SQLQuery4Insercao_Dados_Mineracao_OS.sql
│       │   ├── VW_FK_Tabelas_Agendamento_OS.sql
│       │   ├── VW_Mineração_Dados_OS_Completa.sql
│       │   └── VW_OS_EQUIPAMENTOS_2021_2024_EMP_21.sql
│       └── mosaico_sjudas
│           ├── DER.md
│           ├── mosaico.py
│           └── requirements.txt
├── 3_prompts
│   ├── 20241102 - dash do raizes do futuro.md
│   ├── formulario - relatorio de ocorrencias.md
│   ├── GPT - Governança.md
│   ├── knowledge - PEC indicadores - Objetivo Geral do Projeto.md
│   ├── processamento das respostas do questionario de lideranca.md
│   ├── prompt - analise dados de frotas.md
│   ├── prompt - analise de programa em python.md
│   ├── prompt - relatorio de ocorrencias.md
│   ├── sjudas - dash da avaliacao do 5S.md
│   ├── sjudas - dash da avaliacao do 5S - tabela de notas - versao 1.md
│   ├── sjudas - dash da avaliacao do 5S - tabela de notas - versao 2.md
│   ├── sjudas - dash do relatorio de batidas - trendline.md
│   └── virtualenvwrapper.md
├── 4_gpt_devolutiva
│   ├── CORE-COMP-REF.md
│   ├── GPT - AD devolutiva - config.md
│   ├── IDP-GEN.md
│   ├── IMFA-SUMM.md
│   ├── IMFA-TECH.md
│   └── knowledge - Roles and Responsibilities.md
├── lib
│   ├── bindings
│   │   └── utils.js
│   ├── tom-select
│   │   ├── tom-select.complete.min.js
│   │   └── tom-select.css
│   └── vis-9.1.2
│       ├── vis-network.css
│       └── vis-network.min.js
├── README.md
└── requirements.txt
</details>

## Componentes Principais

    1_apps: Aplicações desenvolvidas para ambientes Linux e Windows.

    2_labs: Laboratórios de experimentação, testes de conceito e scripts de análise.

    3_prompts: Biblioteca de prompts otimizados para uso com LLMs em tarefas de análise de dados.

    4_gpt_devolutiva: Base de conhecimento estruturada para geração de devolutivas via GPT.

    lib: Bibliotecas auxiliares e dependências de front-end/visualização.