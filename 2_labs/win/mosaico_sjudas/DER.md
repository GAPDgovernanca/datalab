# Documento de Especificação e Requisitos: Mosaico de Gestão IMS/PV

**Versão:** 1.0 (Baseado no protótipo Streamlit)

**Data:** 15/12/2025

**Contexto:** Gestão de Pecuária de Precisão (Confinamento)

## 1. Visão Geral do Produto

O **Mosaico IMS/PV** é uma ferramenta de visualização analítica e apoio à tomada de decisão para gestores de confinamento de gado. O objetivo central é permitir o monitoramento rápido e visual do desempenho nutricional e zootécnico de múltiplos currais simultaneamente.

A métrica principal é a **IMS/PV** (Ingestão de Matéria Seca em relação ao Peso Vivo), um indicador crucial de apetite, saúde e desempenho animal. O sistema classifica os currais estatisticamente e permite uma análise detalhada ("drill-down") para projetar datas de abate e eficiência alimentar.

## 2. Regras de Negócio e Cálculos

O sistema opera sobre as seguintes lógicas matemáticas e zootécnicas identificadas no protótipo:

### 2.1. Classificação Estatística (Curva de Gauss)

A classificação dos currais não é fixa, mas dinâmica baseada na distribuição da população atual (Média e Desvio Padrão - $\sigma$).

- **Muito Alto (Azul):** $> \text{Média} + 2\sigma$

- **Alto (Verde):** Entre $\text{Média} + 1\sigma$ e $\text{Média} + 2\sigma$

- **Acima da Média (Amarelo):** Entre $\text{Média}$ e $\text{Média} + 1\sigma$

- **Abaixo da Média (Laranja):** Entre $\text{Média} - 1\sigma$ e $\text{Média}$

- **Alerta (Vermelho):** Entre $\text{Média} - 2\sigma$ e $\text{Média} - 1\sigma$

- **Crítico (Cinza Escuro):** $< \text{Média} - 2\sigma$

### 2.2. Indicadores de Desempenho (KPIs)

- **Consumo de Matéria Seca (CMS):** Dado de entrada (kg/dia).

- **Ganho Médio Diário (GMD):**
  
  $$GMD = \frac{\text{Peso Atual} - \text{Peso Entrada}}{\text{Dias de Confinamento}}$$

- **Conversão Alimentar (CA):**
  
  $$CA = \frac{\text{Consumo MS}}{GMD}$$
  
  *Regra de exceção:* Se $GMD < 0.1$, considerar CA zerada ou tratada para evitar divisão por zero/infinito.

### 2.3. Projeção de Abate

- **Meta de Peso:** Definida estaticamente em **560 kg** (configurável futuramente).

- **Dias Restantes:**
  
  $$\text{Dias} = \frac{\text{Meta} - \text{Peso Atual}}{GMD}$$

- **Data Prevista:** Data Atual + Dias Restantes.

## 3. Requisitos Funcionais (RF)

### RF01 - Painel Mosaico (Visão Geral)

- O sistema deve exibir uma grade (grid) representando todos os currais ativos.

- Cada célula do grid deve conter: Código do Curral e % IMS/PV.

- A cor de fundo da célula deve refletir automaticamente o status estatístico (vide 2.1).

- A visualização deve ser compacta, permitindo ver dezenas de currais em uma única tela ("One Screen View").

### RF02 - Interatividade e Seleção

- O usuário deve poder clicar diretamente em qualquer bloco do mosaico.

- Ao clicar, o sistema deve atualizar a seção de detalhes sem recarregar a página inteira (preservando o contexto).

- O sistema deve fornecer feedback visual (cursor ou realce) ao passar o mouse sobre os currais.

### RF03 - Detalhamento do Curral (Drill-Down)

Ao selecionar um curral, o sistema deve exibir:

1. **Cabeçalho:** Identificação, Status Classificatório e valor exato do IMS/PV.

2. **Cartões Métricos:** Consumo MS (kg), Dias de Confinamento, Tipo de Ração Atual (Adaptação, Crescimento, Terminação) e Dias na Ração.

3. **Análise Econômica/Zootécnica:** GMD Atual e Conversão Alimentar.

### RF04 - Visualização Gráfica de Evolução

- Deve ser exibido um gráfico de barras comparativo para o curral selecionado contendo:
  
  - Peso de Entrada (Verde).
  
  - Peso Atual (Azul).
  
  - Meta de Peso (Roxo).

### RF05 - Planejamento de Saída

- O sistema deve calcular e exibir quantos dias faltam para o abate baseando-se no GMD atual.

- O sistema deve exibir a data estimada de abate.

- Se a meta já foi atingida, exibir mensagem de conclusão ("Status Meta: Atingida").

## 4. Requisitos Não-Funcionais (RNF)

### RNF01 - Interface e Usabilidade (UI/UX)

- **Tecnologia:** Python com framework Streamlit.

- **Biblioteca Gráfica:** Plotly (Graph Objects) para renderização do Mosaico (Heatmap + Scatter) visando precisão de layout e performance.

- **Responsividade:** O grid deve se ajustar à largura do container (`width="stretch"`).

- **Tema:** O sistema deve suportar Modo Claro e Escuro, mas garantir contraste forçado nos cartões de métricas (Fundo Branco, Texto Escuro) para legibilidade crítica.

### RNF02 - Desempenho

- O cálculo estatístico (média/desvio) deve ser realizado no *frontend* (ou camada de aplicação) em tempo real após o carregamento dos dados.

### RNF03 - Estética do Mosaico

- O mosaico não deve apresentar espaçamentos excessivos ("gaps") entre as colunas. Deve assemelhar-se a um "Waffle Chart" ou tabela densa.

## 5. Arquitetura de Dados (Simulação vs. Produção)

### 5.1. Estado Atual (Protótipo)

- Dados gerados via algoritmo randômico (`numpy`) simulando 88 currais (C13 a C100) + 12 currais estáticos.

- Não há persistência de dados.

### 5.2. Requisitos para Produção (Roadmap)

Para transformar o sketch em produto, é necessário implementar:

- **Fonte de Dados:** Conexão com banco de dados SQL (PostgreSQL/SQL Server) ou API do sistema de gestão pecuária (ERP).

- **Schema Sugerido (Tabela `LeiturasDiarias`):**
  
  - `id_curral` (VARCHAR)
  
  - `data_leitura` (DATE)
  
  - `consumo_ms` (FLOAT)
  
  - `peso_medio` (FLOAT)
  
  - `cabecas` (INT)
  
  - `fase_nutricional` (VARCHAR)

## 6. Inventário de Componentes de Interface

1. **Header:** Título centralizado com subtítulo explicativo.

2. **Mosaico Principal:** `plotly.graph_objects.Figure` combinando `Heatmap` (cores) e `Scatter` (texto) em layout de grid cartesiano.

3. **Legenda:** Barra horizontal estática explicando as 6 faixas de cores e seus intervalos numéricos.

4. **Painel de Detalhes:** Container condicional que exibe dados apenas se um curral estiver selecionado (ou padrão C01).

5. **Gráfico de Barras (Evolução):** `plotly.express.bar` minimalista sem legendas redundantes.

6. **KPI Cards:** `st.metric` customizados via CSS injetado.

## 7. Considerações Finais

O pipeline atual demonstra maturidade na lógica de visualização e regras de negócio. O maior esforço para a versão de produção reside na **substituição da função `generate_data()`** por conectores de dados reais e na implementação de filtros temporais (ex: visualizar histórico vs. dados de hoje).
