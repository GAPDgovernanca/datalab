# Guideline Geral para o Desenvolvimento do Dashboard de Gestão de Frota Agrícola

---

#### IMPORTANTE:

TODOS OS CODIGOS FORNECIDOS A SEGUIR SÃO APENAS EXEMPLOS OU REFERENCIAS. Você foi contratado para escrever códigos e programas originais e completos, baseado nos guidelines que está recebendo. Portanto, TODOS OS CODIGOS são apenas bibliotecas de referência e de consulta e como tal devem ser tratados.

## 1. Introdução

**Objetivo:**  
Desenvolver um dashboard interativo em Python para a gestão de frota agrícola, que integre dados operacionais e financeiros dos equipamentos, forneça visualizações dinâmicas e permita consultas analíticas via uma API de inteligência artificial (IA).

**Escopo:**  
O sistema deverá:

- Conectar-se a um banco de dados SQLite que já contém os ajustes necessários em suas tabelas.
- Permitir a aplicação de filtros customizados para seleção de períodos, equipamentos, classes e usuários.
- Exibir dados em formatos diversos, como cards, gráficos interativos e tabelas.
- Integrar uma API de IA para responder a perguntas e fornecer análises baseadas nos dados apresentados.

---

## 2. Arquitetura e Estrutura do Projeto

### 2.1. Organização de Código e Pastas

- **Código Fonte:**  
  Organizar os scripts em módulos que separem claramente as responsabilidades, por exemplo:
  
  - **db.py:** Conexão e operações com o banco de dados.
  - **filters.py:** Construção e validação dos filtros SQL.
  - **processing.py:** Cálculos de métricas, multiplicadores e sinalizadores.
  - **ia_integration.py:** Integração com a API de IA (GROQ).
  - **ui.py:** Componentes da interface, layout e customizações com CSS.
  - **main.py:** Integração de todos os módulos e definição do fluxo principal do dashboard.

- **Documentação:**  
  Manter comentários e uma documentação interna clara para cada função e módulo, facilitando a manutenção e evolução do código.

### 2.2. Ferramentas e Bibliotecas

- **Framework Principal:**  
  Utilizar o **Streamlit** para criação do dashboard.
- **Manipulação de Dados:**  
  Empregar o **pandas** para carregamento e transformação dos dados.
- **Banco de Dados:**  
  Utilizar o **sqlite3** para conexão com o banco de dados `frota.db`.
- **Visualizações:**  
  Usar o **Plotly Express** para criação de gráficos interativos.
- **Integração com IA:**  
  Configurar a API de IA (GROQ) utilizando uma biblioteca cliente adequada e ler a chave de API de uma variável de ambiente.
- **Customização de Interface:**  
  Incluir estilos CSS customizados via `st.markdown` com a flag `unsafe_allow_html=True`.

---

## 3. Funcionalidades Principais

### 3.1. Integração com o Banco de Dados

- **Conexão:**
  
  - Implementar a função `get_db_connection()` para estabelecer a conexão com o SQLite.
  - Configurar o `row_factory` para que os resultados sejam retornados em formato de dicionário.

- **Consultas:**
  
  - Desenvolver funções para obter datas padrão (mínimas e máximas) e as datas mais recentes dos registros.
  - Realizar consultas em múltiplas tabelas (fato_custo, fato_combustivel, fato_manutencao, fato_reforma, fato_uso) e unir dados com a tabela `dim_equipamento`.

### 3.2. Filtragem e Processamento dos Dados

- **Filtros Customizados:**
  
  - Permitir seleção interativa de intervalo de datas, IDs de equipamentos (entrada de texto, separados por vírgula), e filtros de “Classe” e “Unidade/Usuário” (multiseleção com opção “Todos”).
  - Desenvolver a função `build_filters()` para construir as cláusulas SQL dinamicamente com base nos filtros selecionados.

- **Carregamento dos Dados:**
  
  - Implementar `get_filtered_data()` para a consulta principal, realizando junção entre as tabelas necessárias e aplicando os filtros.
  - Implementar `get_additional_data()` para extrair informações complementares de outras tabelas, enriquecendo a base de dados para análises.

### 3.3. Cálculo de Métricas e Indicadores

- **Multiplicadores e Indicadores:**
  
  - Desenvolver a função `calcular_multiplicadores()` para calcular métricas como a “Taxa de Utilização Multiplicador” e o “Consumo Multiplicador” com base nos valores já ajustados no banco.

- **Sinalizadores Visuais:**
  
  - Criar a função `apply_flags()` para identificar e sinalizar visualmente, por meio de ícones (por exemplo, 🟢, 🔴, ⚪), os desvios significativos entre os valores realizados e os estimados.

### 3.4. Integração com a API de Inteligência Artificial

- **Configuração:**
  
  - Configurar a API utilizando a variável de ambiente `GROQ_API_KEY` e a classe cliente apropriada.

- **Processamento de Perguntas:**
  
  - Implementar `query_groq(data_json, question, model_name="deepseek-r1-distill-llama-70b")` para:
    - Combinar os dados filtrados e complementares em um objeto JSON.
    - Construir um prompt detalhado com regras de arredondamento e definições técnicas.
    - Enviar a consulta à API e processar a resposta, removendo partes desnecessárias, se necessário.

### 3.5. Interface do Usuário e Visualizações

- **Layout e Customização:**
  
  - Configurar a página com `st.set_page_config(layout="wide")`.
  - Inserir CSS customizado para definir o estilo dos containers, cards, tabelas e componentes interativos.

- **Componentes Interativos:**
  
  - Desenvolver uma sidebar com filtros (datas, IDs, usuário e classe) e carregamento dinâmico dos valores únicos.
  - Exibir métricas em cards customizados (por exemplo, total de registros, valor total estimado).
  - Gerar gráficos interativos com Plotly Express que comparem indicadores como “Uso vs Planejado” e “Consumo vs Planejado”, incluindo linhas de referência.
  - Apresentar os dados em tabelas formatadas, com ênfase na formatação monetária e na aplicação de sinalizadores visuais.

- **Seção de Perguntas à IA:**
  
  - Incluir uma área de texto para que o usuário insira perguntas sobre os dados.
  - Conectar essa entrada à função de integração com a IA para retornar análises detalhadas e insights.

---

## 4. Fluxo de Dados e Lógica de Processamento

1. **Entrada dos Filtros:**
   - Os filtros são configurados na sidebar e armazenados em um dicionário.
2. **Consulta ao Banco de Dados:**
   - As funções `get_filtered_data()` e `get_additional_data()` são chamadas para extrair os dados conforme os filtros selecionados.
3. **Processamento dos Dados:**
   - Os indicadores e multiplicadores são calculados a partir dos dados já ajustados.
   - Sinalizadores visuais são aplicados para destacar desvios relevantes.
4. **Exibição dos Resultados:**
   - Os dados processados são exibidos em cards, gráficos interativos e tabelas estilizadas.
5. **Integração com a IA:**
   - Ao enviar uma pergunta, os dados e a questão do usuário são combinados e enviados à API, retornando uma resposta estruturada para análise.

---

## 5. Considerações Técnicas e Boas Práticas

### 5.1. Segurança e Validação

- **Variáveis de Ambiente:**
  
  - Utilizar variáveis de ambiente para armazenar a chave da API, evitando expor informações sensíveis.

- **SQL e Validação:**
  
  - Considerar o uso de parâmetros preparados nas consultas SQL para mitigar riscos de injeção de código.

- **Validação de Entradas:**
  
  - Implementar verificações robustas para garantir que os dados inseridos pelo usuário (especialmente IDs) estejam no formato correto.

### 5.2. Performance e Escalabilidade

- **Consultas Otimizadas:**
  
  - Garantir que o banco de dados esteja indexado adequadamente para otimizar as consultas.

- **Cache de Dados:**
  
  - Avaliar a implementação de cache (por exemplo, com `@st.cache_data`) para melhorar a performance em cenários de alta demanda.

### 5.3. Documentação e Manutenção

- **Comentários e Documentação:**
  
  - Documentar todas as funções e módulos, facilitando futuras manutenções e a incorporação de novas funcionalidades.

- **Modularidade:**
  
  - Manter o código modularizado, permitindo a escalabilidade e a fácil integração de novos componentes.

---

## 6. Conclusão e Próximos Passos

Este guideline estabelece as bases para o desenvolvimento de um dashboard de gestão de frota agrícola robusto, integrando dados do SQLite e funcionalidades avançadas de visualização e análise por meio de uma API de IA.

**Próximos passos sugeridos:**

- Definir a estrutura do repositório e as responsabilidades de cada módulo.
- Elaborar um protótipo inicial da interface e validar com os stakeholders.
- Implementar os módulos seguindo as boas práticas de segurança, performance e documentação.
- Realizar testes integrados para garantir a consistência dos dados e a correta exibição das informações.
