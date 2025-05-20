**Prompt Completo para Produzir a Análise a Partir do Arquivo CSV Compartilhado**

1. **Carregar o Arquivo CSV**
   - Carregar o arquivo CSV fornecido usando a codificação UTF-8 para lidar com caracteres especiais.
   - Assumir que o arquivo contém várias colunas, incluindo o nome do avaliador, data, área avaliada e várias perguntas relacionadas ao programa 5S.

2. **Limpeza e Pré-processamento dos Dados**
   1. **Selecionar Colunas Relevantes**:
      - Extrair colunas relacionadas à área avaliada (`area avaliada:`), data da avaliação (`Start Date (UTC)`), e as respostas para perguntas específicas, como:
        - Equipamentos de limpeza (`Existem equipamentos de limpeza adequados e acessíveis...`)
        - Limpeza (`As áreas de trabalho do local que você está avaliando...`)
        - Frequência de limpeza (`A limpeza é realizada de forma frequente...`)
        - Identificação de itens (`Cada item tem um lugar designado e está claramente identificado?`)
        - Condição de armazenamento (`Os locais de armazenamento são adequados...`)
        - Necessidade dos itens (`Todos os itens presentes na área são necessários para os trabalhos realizados no local?`)
        - Comprometimento (`Você viu exemplos específicos de boas práticas?`)
   
   2. **Renomear Colunas**:
      - Renomear estas colunas para nomes simplificados, como: `area`, `date`, `cleaning_equipment`, `cleanliness`, `cleaning_frequency`, `item_identification`, `storage_condition`, `item_necessity`, e `commitment`.

3. **Transformação dos Dados**
   1. **Converter o Formato da Data**:
      - Converter a coluna `date` para o formato datetime.
      - Extrair o número da semana da coluna `date` para permitir a análise temporal.

   2. **Extrair Respostas Numéricas**:
      - Extrair valores numéricos das respostas do questionário. As respostas geralmente estão formatadas com um prefixo como `"3: Maioria dos equipamentos necessários disponíveis"`.
      - Implementar uma função para extrair o prefixo numérico (`extract_numeric`). A função deve:
        - Lidar com diferentes formatos usando um padrão regex para identificar prefixos numéricos seguidos de dois pontos.
        - Garantir que valores como `None` sejam atribuídos corretamente para respostas não numéricas.
      - Aplicar `extract_numeric` nas colunas `cleaning_equipment`, `cleanliness`, `cleaning_frequency`, `item_identification`, `storage_condition`, `item_necessity`, e `commitment`.

   3. **Converter Escalas de Avaliação**:
      - As respostas do CSV usam uma escala de `0-4`, que deve ser convertida:
        - Converter a escala original `0-4` para uma escala `1-5`. Para isso, somar `1` ao valor inteiro de cada valor extraído das respostas.
        - Converter a escala `1-5` para uma escala `1-10` usando a fórmula:
          \[
          \text{nota\_10} = \left(\frac{(\text{nota\_5} - 1) \times (10-1)}{5-1}\right) + 1
          \]
      - Aplicar essas transformações nas colunas `cleaning_equipment`, `cleanliness`, `cleaning_frequency`, `item_identification`, `storage_condition`, `item_necessity`, e `commitment`.

4. **Agrupamento das Perguntas em Categorias**
   1. **Agrupar as Perguntas nas Categorias Seiri, Seiton, e Seiso**:
      - Agrupar as perguntas nas seguintes categorias para uma análise mais direcionada:
        - **Seiri (Utilização)**: perguntas relacionadas à necessidade e identificação de itens (`item_necessity` e `item_identification`).
        - **Seiton (Organização)**: perguntas relacionadas à organização dos itens (`item_identification` e `storage_condition`).
        - **Seiso (Limpeza)**: perguntas relacionadas à limpeza e frequência de limpeza (`cleaning_equipment`, `cleanliness`, e `cleaning_frequency`).

5. **Análise dos Dados**
   1. **Calcular Médias Semanais**:
      - Agrupar os dados por `week` e `area` para calcular as médias semanais de todas as colunas relevantes.
      - Gerar tabelas separadas para `Complexo Barracão` e `Complexo Oficina`.

   2. **Calcular Médias por Categoria**:
      - **Seiri (Utilização)**: Calcular as médias de todas as perguntas do grupo Seiri para cada área.
      - **Seiton (Organização)**: Calcular as médias de todas as perguntas do grupo Seiton para cada área.
      - **Seiso (Limpeza)**: Calcular as médias de todas as perguntas do grupo Seiso para cada área.

6. **Identificar Pontos Críticos e Pontos Fortes**
   1. **Calcular Pontos Críticos e Pontos Fortes**:
      - Identificar os **5 menores valores** (pontos críticos) para cada área, incluindo o nome da coluna e o valor.
      - Identificar os **5 maiores valores** (pontos fortes) para cada área, incluindo o nome da coluna e o valor.

7. **Gerar Saída em Markdown**
   1. **Preparar Tabelas em Markdown**:
      - Gerar uma tabela Markdown para **Médias Gerais por Área**.
      - Gerar tabelas Markdown para **Médias por Categoria** (Seiri, Seiton, Seiso).
      - Gerar tabelas Markdown para **Pontos Críticos (5 Menores Valores)** e **Pontos Fortes (5 Maiores Valores)** para ambas as áreas.
      - Incluir uma tabela Markdown para **Evolução Semanal** das pontuações, detalhando as médias semanais para ambas as áreas.

**Exemplo de Saída em Markdown**:
- Estruturar as tabelas como no exemplo abaixo:

```markdown
**Médias Gerais por Área:**

| Área              | Nota Média (Escala de 10) |
|-------------------|---------------------------|
| Complexo Barracão | 7.38                      |
| Complexo Oficina  | 6.91                      |

**Médias por Categoria:**

| Categoria             | Complexo Barracão | Complexo Oficina |
|-----------------------|-------------------|------------------|
| **Seiri (Utilização)** | 7.75              | 7.00             |
| **Seiton (Organização)** | 7.75              | 7.00             |
| **Seiso (Limpeza)**    | 7.00              | 6.81             |

**Pontos Críticos (5 Menores Valores):**

| Área               | Aspecto             | Nota |
|--------------------|---------------------|------|
| Complexo Barracão  | Frequência Limpeza  | 3.25 |
| Complexo Oficina   | Equipamento Limpeza | 3.25 |

**Pontos Fortes (5 Maiores Valores):**

| Área               | Aspecto             | Nota |
|--------------------|---------------------|------|
| Complexo Oficina   | Equipamento Limpeza | 10.00 |
| Complexo Barracão  | Necessidade de Itens| 10.00 |

**Evolução Semanal das Notas:**

| Semana | Área               | Equipamento Limpeza | Limpeza | Frequência Limpeza | Identificação Itens | Condição Armazenamento | Necessidade de Itens | Comprometimento |
|--------|--------------------|---------------------|---------|--------------------|---------------------|------------------------|----------------------|-----------------|
| 44     | Complexo Barracão  | 7.25                | 8.00    | 7.50               | 7.00                | 7.75                   | 7.50                 | 8.00            |
| 44     | Complexo Oficina   | 6.50                | 7.00    | 6.75               | 6.25                | 7.00                   | 7.00                 | 7.25            |
```
