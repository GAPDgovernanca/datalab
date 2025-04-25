## 1. Definição Formal do Problema

Seja um lote de animais comprado a um preço unitário por arroba (@), com peso inicial e crescimento projetado de acordo com uma função de ganho de peso . O objetivo é estimar a função lucro , dada por:

aonde:

- , peso final estimado com base na função de ganho de peso;
- representa o preço de venda por arroba no momento ;
- , custos operacionais acumulados;
- pode ser um modelo linear ou não-linear com ruído estocástico.

A simulação deve ser realizada para um número de iterações , a fim de obter a distribuição .

## 2. Variáveis de Entrada

### Dados de Compra:

- : Preço de compra unitário por arroba (R$/@)
- : Peso médio inicial (arrobas)
- : Ágio/desconto relativo ao mercado (%),

### Função de Crescimento:

- : Taxa de ganho de peso, podendo assumir distribuição normal
- : Tempo de confinamento

### Custos Operacionais:

- , custo financeiro sobre capital investido

### Preço Futuro:

- obtido via scraping de dados futuros e análise histórica
- : Correlação entre preços passados e futuros usada para ajuste estocástico

## 3. Modelagem Matemática

### Simulação de Monte Carlo

Para iterações:

1. Amostragem de para evolução do peso.
2. Amostragem de , onde é uma distribuição ajustada aos preços futuros.
3. Cálculo de por iteração.
4. Construção da distribuição empírica de .

### Análise de Sensibilidade

Derivar para cada variável , identificando as que mais impactam o resultado.

## 4. Implementação Computacional

### Stack Tecnológica:

- **Back-end:** Python (FastAPI ou Flask), Pandas, NumPy, Scipy
- **Simulações:** SciPy.stats, NumPy.random, multiprocessing para paralelismo
- **Front-end:** Streamlit ou Dash
- **Banco de Dados:** PostgreSQL para armazenar simulações passadas
- **Scraping de Preços:** Selenium ou API de terceiros

### Algoritmo Principal:

1. **Entrada de Dados:** Receber parâmetros via API.
2. **Scraping de Preços Futuros:** Obter e ajustar distribuição .
3. **Execução da Simulação:** Monte Carlo para obtenção da distribuição de .
4. **Análise de Sensibilidade:** Cálculo das derivadas parciais .
5. **Renderização Gráfica:** Histogramas de , scatter plots .
6. **Exportação de Resultados:** Geração de relatórios em CSV, Excel, PDF.

## 5. Requisitos de Performance

- Tempo de simulação inferior a **5s para 10.000 iterações**.
- Uso de **paralelismo** via multiprocessing para otimização computacional.
- Interface responsiva adaptada para desktop e mobile.
