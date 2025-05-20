### Prompt Completo para Query Consolidada

**Contexto:**  
Você possui um banco de dados com as seguintes tabelas e campos:

- **dim_equipamento**  
  
  - `id_equipamento`, `modelo`, `usuario`, `classe`, `data_criacao`

- **fato_uso**  
  
  - `id`, `id_equipamento`, `tipo_medidor`, `uso_estimado`, `uso_realizado`, `uso_diferenca`, `data_referencia`, `data_processamento`

- **fato_custo**  
  
  - `id`, `id_equipamento`, `custo_hora_estimado`, `custo_hora_realizado`, `custo_hora_diferenca`, `total_estimado`, `total_realizado`, `total_diferenca`, `data_referencia`, `data_processamento`

- **fato_combustivel**  
  
  - `id`, `id_equipamento`, `comb_litros_estimado`, `comb_litros_realizado`, `comb_litros_diferenca`, `comb_valor_unitario_estimado`, `comb_valor_unitario_realizado`, `comb_valor_unitario_diferenca`, `comb_total_estimado`, `comb_total_realizado`, `comb_total_diferenca`, `data_referencia`, `data_processamento`

- **fato_manutencao**  
  
  - `id`, `id_equipamento`, `lubrificantes_estimado`, `lubrificantes_realizado`, `lubrificantes_diferenca`, `filtros_estimado`, `filtros_realizado`, `filtros_diferenca`, `graxas_estimado`, `graxas_realizado`, `graxas_diferenca`, `pecas_servicos_estimado`, `pecas_servicos_realizado`, `pecas_servicos_diferenca`, `data_referencia`, `data_processamento`

- **fato_reforma**  
  
  - `id`, `id_equipamento`, `reforma_estimado`, `reforma_realizado`, `reforma_diferenca`, `data_referencia`, `data_processamento`

**Objetivo:**  
Construir uma query SQL que reúna os dados de todas essas tabelas, relacionando-as por `id_equipamento` e filtrando para um equipamento específico (por exemplo, onde `id_equipamento = 3721`), consolidando os registros para que seja retornada apenas uma linha por equipamento.

**Abordagens Disponíveis (Escolha uma conforme a necessidade):**

---

#### **Abordagem 1 – Consolidação com Agregação (GROUP BY)**

Esta abordagem utiliza funções de agregação para resumir os dados de cada tabela fato e agrupa pelo equipamento. Exemplo:

```sql
SELECT
    de.id_equipamento,
    de.modelo,
    de.usuario,
    de.classe,
    de.data_criacao,

    -- Para campos que podem ser agregados numericamente
    MAX(fu.tipo_medidor) AS tipo_medidor,
    SUM(fu.uso_estimado) AS uso_estimado,
    SUM(fu.uso_realizado) AS uso_realizado,
    SUM(fu.uso_diferenca) AS uso_diferenca,

    SUM(fc.total_estimado) AS total_estimado,
    SUM(fc.total_realizado) AS total_realizado,
    SUM(fc.total_diferenca) AS total_diferenca,

    SUM(fco.comb_litros_estimado) AS comb_litros_estimado,
    SUM(fco.comb_litros_realizado) AS comb_litros_realizado,
    SUM(fco.comb_litros_diferenca) AS comb_litros_diferenca,

    SUM(fm.lubrificantes_estimado) AS lubrificantes_estimado,
    SUM(fm.lubrificantes_realizado) AS lubrificantes_realizado,
    SUM(fm.lubrificantes_diferenca) AS lubrificantes_diferenca,

    SUM(fr.reforma_estimado) AS reforma_estimado,
    SUM(fr.reforma_realizado) AS reforma_realizado,
    SUM(fr.reforma_diferenca) AS reforma_diferenca

FROM
    dim_equipamento AS de
LEFT JOIN
    fato_uso AS fu ON de.id_equipamento = fu.id_equipamento
LEFT JOIN
    fato_custo AS fc ON de.id_equipamento = fc.id_equipamento
LEFT JOIN
    fato_combustivel AS fco ON de.id_equipamento = fco.id_equipamento
LEFT JOIN
    fato_manutencao AS fm ON de.id_equipamento = fm.id_equipamento
LEFT JOIN
    fato_reforma AS fr ON de.id_equipamento = fr.id_equipamento
WHERE
    de.id_equipamento = 3721
GROUP BY
    de.id_equipamento, de.modelo, de.usuario, de.classe, de.data_criacao;
```

*Observação:* Use funções de agregação (como MAX, SUM, etc.) conforme o que faz sentido para cada campo. Essa query retorna uma única linha por equipamento.

---

#### **Abordagem 2 – Subconsultas Correlacionadas**

Essa abordagem usa subconsultas para selecionar somente um registro “mais relevante” de cada tabela fato. Por exemplo, considerando o registro mais recente (baseado em `data_referencia`):

```sql
SELECT
    de.id_equipamento,
    de.modelo,
    de.usuario,
    de.classe,
    de.data_criacao,

    (SELECT fu.tipo_medidor
     FROM fato_uso fu
     WHERE fu.id_equipamento = de.id_equipamento
     ORDER BY fu.data_referencia DESC
     LIMIT 1) AS tipo_medidor,

    (SELECT fu.uso_estimado
     FROM fato_uso fu
     WHERE fu.id_equipamento = de.id_equipamento
     ORDER BY fu.data_referencia DESC
     LIMIT 1) AS uso_estimado,

    (SELECT fc.total_estimado
     FROM fato_custo fc
     WHERE fc.id_equipamento = de.id_equipamento
     ORDER BY fc.data_referencia DESC
     LIMIT 1) AS total_estimado,

    (SELECT fco.comb_total_estimado
     FROM fato_combustivel fco
     WHERE fco.id_equipamento = de.id_equipamento
     ORDER BY fco.data_referencia DESC
     LIMIT 1) AS comb_total_estimado,

    (SELECT fm.lubrificantes_estimado
     FROM fato_manutencao fm
     WHERE fm.id_equipamento = de.id_equipamento
     ORDER BY fm.data_referencia DESC
     LIMIT 1) AS lubrificantes_estimado,

    (SELECT fr.reforma_estimado
     FROM fato_reforma fr
     WHERE fr.id_equipamento = de.id_equipamento
     ORDER BY fr.data_referencia DESC
     LIMIT 1) AS reforma_estimado

FROM
    dim_equipamento de
WHERE
    de.id_equipamento = 3721;
```

*Observação:* Cada subconsulta retorna o registro mais recente de sua respectiva tabela para aquele equipamento. Essa abordagem evita a multiplicação de linhas sem precisar usar agregação de vários registros.

---

#### **Abordagem 3 – CTEs com Funções de Janela**

Caso o seu banco de dados suporte Common Table Expressions (CTEs) e funções de janela, você pode usar essa abordagem para filtrar o registro “mais relevante” de cada tabela. Por exemplo:

```sql
WITH uso_cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_equipamento ORDER BY data_referencia DESC) AS rn
  FROM fato_uso
),
custo_cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_equipamento ORDER BY data_referencia DESC) AS rn
  FROM fato_custo
),
comb_cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_equipamento ORDER BY data_referencia DESC) AS rn
  FROM fato_combustivel
),
manut_cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_equipamento ORDER BY data_referencia DESC) AS rn
  FROM fato_manutencao
),
reforma_cte AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_equipamento ORDER BY data_referencia DESC) AS rn
  FROM fato_reforma
)
SELECT
    de.id_equipamento,
    de.modelo,
    de.usuario,
    de.classe,
    de.data_criacao,
    u.tipo_medidor,
    u.uso_estimado,
    c.total_estimado,
    cb.comb_total_estimado,
    m.lubrificantes_estimado,
    r.reforma_estimado
FROM
    dim_equipamento de
LEFT JOIN
    uso_cte u ON de.id_equipamento = u.id_equipamento AND u.rn = 1
LEFT JOIN
    custo_cte c ON de.id_equipamento = c.id_equipamento AND c.rn = 1
LEFT JOIN
    comb_cte cb ON de.id_equipamento = cb.id_equipamento AND cb.rn = 1
LEFT JOIN
    manut_cte m ON de.id_equipamento = m.id_equipamento AND m.rn = 1
LEFT JOIN
    reforma_cte r ON de.id_equipamento = r.id_equipamento AND r.rn = 1
WHERE
    de.id_equipamento = 3721;
```

*Observação:* Cada CTE atribui um número de linha para os registros de cada tabela fato, e os JOINs selecionam apenas o registro com `rn = 1` (por exemplo, o mais recente).

---

### Instrução Final

Utilize o template acima conforme a necessidade do seu relatório. Escolha uma das abordagens (Abordagem 1, 2 ou 3) de acordo com os seguintes critérios:

- **Abordagem 1 (GROUP BY e agregação):**  
  Use quando os dados puderem ser consolidados por meio de funções agregadas e uma única linha por equipamento for suficiente para seu relatório.

- **Abordagem 2 (Subconsultas Correlacionadas):**  
  Ideal para quando você deseja retornar somente o registro “mais relevante” (como o mais recente) de cada tabela fato, sem agregar os valores de múltiplos registros.

- **Abordagem 3 (CTEs e Funções de Janela):**  
  Indicado se o seu banco de dados suporta essas funcionalidades e você prefere uma solução performática para selecionar um registro específico de cada tabela fato.
