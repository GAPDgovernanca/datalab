## 1. Visão Geral

**Nome do Software:** Aplicativo de Análise de Sensibilidade para Negociação de Gado

**Objetivo:** Fornecer simulação de Monte Carlo e análise de sensibilidade para avaliação de riscos e oportunidades na compra e venda de gado, considerando variáveis de mercado, custos operacionais e crescimento dos animais.

**Usuários-Alvo:** Analistas financeiros do agronegócio, pecuaristas e traders de commodities agropecuárias.

## 2. Requisitos Funcionais

### 2.1 Entrada de Dados

- O sistema deve permitir a entrada manual de parâmetros via interface.
- O sistema deve obter automaticamente os preços futuros da arroba do boi via scraping da B3.
- O sistema deve permitir a importação de planilhas CSV contendo séries temporais de preços.

### 2.2 Processamento

- O sistema deve calcular a função lucro com base nos parâmetros inseridos.
- O sistema deve gerar distribuição empírica de por meio de Simulação de Monte Carlo com pelo menos 10.000 iterações.
- O sistema deve calcular derivadas parciais para cada variável de entrada e classificar impacto relativo no lucro.

### 2.3 Saída de Dados

- O sistema deve exibir histogramas da distribuição de .
- O sistema deve exibir scatter plots mostrando relações entre e variáveis de entrada.
- O sistema deve exportar os resultados em CSV, Excel e PDF.
- O sistema deve permitir o armazenamento de histórico de simulações em banco de dados.

## 3. Requisitos Não Funcionais

### 3.1 Performance

- O tempo de execução da simulação de Monte Carlo deve ser menor que 5 segundos para 10.000 iterações.
- O sistema deve suportar processamentos paralelos via multiprocessing.

### 3.2 Escalabilidade

- O banco de dados deve ser capaz de armazenar pelo menos 1 milhão de registros históricos sem degradação de performance.

### 3.3 Segurança

- O sistema deve permitir autenticação de usuários para acesso às funcionalidades.
- Os dados do usuário devem ser armazenados de forma segura e criptografada.

## 4. Arquitetura do Sistema

### 4.1 Tecnologias

- **Back-end:** Python com FastAPI/Flask
- **Front-end:** Streamlit/Dash
- **Banco de Dados:** PostgreSQL
- **Simulações:** NumPy, SciPy, multiprocessing
- **Scraping:** Selenium/API externa

### 4.2 Fluxo de Dados

1. Usuário insere dados ou realiza importação de preços futuros.
2. Sistema executa análise e gera simulações estocásticas.
3. Resultados são processados e apresentados graficamente.
4. Usuário pode exportar os resultados ou armazená-los no histórico.

## 5. Restrições e Dependências

- O scraping depende da disponibilidade dos dados da B3.
- A execução do cálculo deve garantir a consistência numérica da distribuição de .

## 6. Critérios de Aceitação

- O sistema deve calcular corretamente e exibir resultados estatisticamente coerentes.
- A interface deve ser responsiva e permitir a análise interativa dos dados.
- A exportação dos relatórios deve preservar a integridade dos cálculos.
