# IMFA-SUMM-AVALIADO — Síntese Executiva (Versão Avaliado / Intranet)

**PROTOCOL_ID:** IMFA-SUMM-AVALIADO-01  
**VERSION:** 1.7  
**OBJECTIVE:** Gerar devolutiva padronizada para o avaliado, publicável na intranet  
**LANG:** PT-BR  
**AUDIÊNCIA:** O próprio avaliado (gestor/líder avaliado no ciclo 360°)

---

## 1. Contexto e Propósito

Este módulo produz a versão da Síntese Executiva destinada ao **avaliado**. Diferente do IMFA-SUMM (orientado à liderança sênior), este documento é escrito **para** a pessoa avaliada, com linguagem acessível, tom de desenvolvimento e formato padronizado replicável para todos os gestores do ciclo.

**Acionamento:** Quando o usuário solicitar a síntese/devolutiva na versão do avaliado, ou quando indicar que o documento será publicado na intranet para leitura direta pelo avaliado.

**Dependências:** Requer que IMFA-TECH já tenha sido executado (dados quantitativos e qualitativos processados).

---

## 2. Estilo

### Tom
Devolutiva de desenvolvimento — não avaliativo, não punitivo. O texto fala **com** o avaliado, não **sobre** ele. Honesto, respeitoso, encorajador sem ser condescendente.

### Pessoa verbal
Segunda pessoa ("você") ao longo de todo o documento.

### Vocabulário
Linguagem corporativa acessível, sem jargão estatístico.

**Termos proibidos:** desvio padrão, threshold, outlier, sigma, score, gap analysis, IMFA, delta, variância, framework, Likert, z-score, cluster, pipeline, decile.

**Substituições padronizadas:**

| Termo técnico (uso interno) | Versão avaliado |
|---|---|
| Score ≥ 4.5 (com σ ≤ 1.2) | **Ponto forte reconhecido** |
| Score 3.51 – 4.49 | **Dentro do esperado** |
| Score ≤ 3.50 | **Ponto para desenvolver** |
| Gap: auto > avaliadores | "Você se avalia acima do que os avaliadores percebem" |
| Gap: auto < avaliadores | "As pessoas ao seu redor reconhecem mais essa competência do que você mesmo" |
| Discrepância alta (delta ≥ 1.0) | "Diferença significativa entre sua visão e a dos avaliadores" |
| Competência / competency_id | "Tema avaliado" |
| Escala Likert 1-5 | "Escala de 1 a 5, onde 1 significa 'raramente' e 5 significa 'quase sempre'" |

### Redação
- Frases curtas (máximo ~25 palavras).
- Parágrafos de no máximo 3–4 linhas.
- Voz ativa.
- Sem siglas do framework (PD-01, TW-02, etc.) — usar apenas nomes por extenso dos temas.

---

## 3. Forma

### Estrutura fixa (9 seções, sempre nesta ordem e com estes títulos exatos)

| # | Título padronizado | Tipo |
|---|---|---|
| 1 | **Resultado da Avaliação de Desempenho [Ano]** | Cabeçalho (dados variáveis) |
| 2 | **Como funciona esta avaliação** | Abertura (texto fixo/institucional) |
| 3 | **Seus resultados por tema** | Painel de competências (dados variáveis) |
| 4 | **O que as pessoas reconhecem em você** | Destaques positivos (dados variáveis) |
| 5 | **Onde você pode crescer** | Pontos para desenvolver (dados variáveis) |
| 6 | **Como você se vê vs. como os outros te veem** | Autopercepção / gap (dados variáveis) |
| 7 | **Sua evolução em relação ao ano anterior** | Comparativo ano-a-ano (dados variáveis, requer dados do ciclo anterior) |
| 8 | **Principais temas dos comentários** | Qualitativo sintético (dados variáveis) |
| 9 | **E agora?** | Próximos passos (texto fixo/institucional) |

**Nota:** A Seção 7 só é incluída quando existem dados do ciclo imediatamente anterior para o mesmo avaliado. Se for a primeira avaliação do gestor, o documento mantém 8 seções (sem a Seção 7) e a numeração se ajusta automaticamente.

### Layout
- Orientado para leitura em tela (intranet).
- Blocos curtos com espaçamento visual generoso entre seções.
- Extensão máxima: ~1000–1200 palavras (~2–3 páginas-tela). Com a seção comparativa, o documento pode ser levemente mais longo.
- Divisores visuais entre seções.

### Ícones padronizados para o Painel (Seção 3)

| Faixa | Ícone | Cor de fundo |
|---|---|---|
| Ponto forte reconhecido | 🟢 | Verde claro (#E8F5E9) |
| Dentro do esperado | 🟡 | Amarelo claro (#FFF8E1) |
| Ponto para desenvolver | 🔴 | Vermelho claro (#FFEBEE) |

---

## 4. Conteúdo por Seção

### Seção 1 — Cabeçalho
Dados do avaliado em formato tabular simples:
- Nome do avaliado
- Cargo/função
- Ciclo avaliativo (ano)
- Participantes: quantidade e tipos de avaliadores (ex: "4 liderados, 4 colegas gestores, 2 diretores + autoavaliação"). **Nunca** incluir nomes de avaliadores.

### Seção 2 — Como funciona esta avaliação
**Texto institucional fixo (idêntico para todos os avaliados):**

> Na avaliação 360°, pessoas que trabalham diretamente com você — liderados, colegas gestores e diretores — respondem a um questionário sobre seis temas ligados à sua atuação como gestor. Você também se avalia nos mesmos temas.
>
> Cada pergunta usa uma escala de 1 a 5, onde 1 significa "raramente" e 5 significa "quase sempre". Os resultados são agrupados por tema, e a média das respostas define o seu resultado em cada um deles.
>
> O objetivo desta devolutiva não é premiar ou punir — é ajudar você a enxergar com clareza o que já funciona bem e onde existem espaços para crescer. A partir desses resultados, será construído junto com sua liderança um plano de desenvolvimento individual.

### Seção 3 — Seus resultados por tema
Tabela com 3 colunas:

| Coluna | Conteúdo |
|---|---|
| Tema avaliado | Nome por extenso da competência (sem código) |
| Resultado | Faixa descritiva + ícone (🟢/🟡/🔴). **Sem nota numérica.** |
| Comentário | 1 frase descritiva, específica ao avaliado |

**Regras:**
- Sempre listar as 6 competências, mesmo que todas estejam na mesma faixa.
- Ordenar da maior para a menor média (internamente calculada, não exibida).
- A classificação em faixas segue os thresholds do IMFA-TECH (seção 4.2), incluindo as zonas de transição: classificações nos limites (4.30–4.49 e 3.30–3.50) dependem de σ e tamanho amostral.
- A faixa exibida ao avaliado é sempre uma das 3 (🟢🟡🔴) — a confiança (alta/moderada) é metadado interno, não aparece no documento.
- Se o número total de avaliadores for < 3, adicionar nota visível no cabeçalho: "Resultado preliminar — número reduzido de participantes" com ícone ⚠️.

**Heatmap por descritor (componente visual abaixo da tabela-resumo):**

Após a tabela-resumo, incluir um heatmap interativo em formato accordion que detalha cada competência nos seus descritores (itens do questionário agrupados em 5 clusters temáticos). Esse componente responde à pergunta: "Dentro de cada tema, o que exatamente preciso melhorar ou manter?"

**Estrutura:**
- 6 blocos clicáveis (1 por competência), ordenados da maior para a menor média.
- Cada bloco mostra: seta de expansão (▶), nome da competência, badge de faixa global.
- Ao clicar, o bloco expande para revelar 5 descritores com:
  - Nome do descritor (linguagem acessível, sem código)
  - Barra de progresso colorida (`.hm-bar-fill` com classe `.forte`, `.esperado` ou `.desenvolver`)
  - Badge de faixa do descritor (pill com a mesma classificação 3 faixas)
- O primeiro bloco abre expandido por padrão.
- Apenas 1 bloco aberto por vez (accordion behavior).

**Agrupamento dos itens do questionário em descritores:**

Cada competência tem 10 itens no questionário. Agrupar em 5 clusters temáticos de 2 itens cada, calculando a média do cluster para classificar na faixa. **O agrupamento é feito por conteúdo do header (QUESTION_MAP), nunca por posição da coluna** — ver tabela QUESTION_MAP na Fase 1 do SKILL.md. Isso garante que o cluster "Feedback e reconhecimento" sempre contém as perguntas sobre feedback, mesmo que elas mudem de posição entre ciclos.

Os nomes dos clusters devem ser descritivos e acessíveis (ex: "Feedback positivo e reconhecimento", não "PD-01.3").

| Competência | Cluster 1 | Cluster 2 | Cluster 3 | Cluster 4 | Cluster 5 |
|---|---|---|---|---|---|
| Desenv. Pessoas | Clareza de expectativas | Feedback e reconhecimento | Ensino e desenvolvimento | Escuta e suporte | Resolução de problemas |
| Trabalho em Equipe | Confiança e apoio | Resolução de conflitos | Perspectivas dos pares | Compartilhamento | Responsabilidades |
| Planej. e Organização | Priorização | Planejamento de recursos | Cronogramas e prazos | Coordenação interáreas | Autonomia e aconselhamento |
| Orient. Resultados | Oportunidades de impacto | Metas e energia | Proatividade | Urgência e conclusão | Priorização e disciplina |
| Conhec. Técnico | Domínio da área | Atualização contínua | Ferramentas e sistemas | Aplicação prática | Compartilhamento com equipe |
| Otimiz. Recursos | Procedimentos e ferramentas | Redução de custos | Orientação da equipe | Eliminação de desperdícios | Maximização de resultados |

**Regras do heatmap:**
- **Sem nota numérica** — apenas faixa de cor e barra de progresso proporcional.
- A barra de progresso usa largura proporcional (internamente calculada como % de 1–5, não exibida).
- Mesmas 3 faixas de cor do painel: verde (Ponto forte), âmbar (Dentro do esperado), vermelho (Ponto para desenvolver).
- Mesmos thresholds do IMFA-TECH: ≥4.5 = forte; 3.51–4.49 = esperado; ≤3.50 = desenvolver.
- Legenda de cores no topo do heatmap.
- Texto introdutório antes do heatmap: "Clique em cada tema para ver o detalhamento. Isso mostra onde exatamente, dentro de cada tema, você pode focar seus esforços."

**CSS classes do heatmap:**
- `.hm-comp` — container de cada competência
- `.hm-comp-header` — linha clicável com seta + nome + badge
- `.hm-comp-header.open` — seta rotacionada 90°
- `.hm-desc-list` — container dos descritores (oculto por padrão, `max-height: 0`)
- `.hm-desc-list.open` — expandido (`max-height: 500px`, transição suave)
- `.hm-desc-row` — linha de cada descritor
- `.hm-bar-track` — trilha da barra de progresso (fundo cinza claro)
- `.hm-bar-fill.forte` / `.esperado` / `.desenvolver` — preenchimento colorido
- `.hm-desc-badge.forte` / `.esperado` / `.desenvolver` — pill de classificação

**JavaScript:** Função accordion no `<script>` que fecha todos os blocos antes de abrir o clicado.

### Seção 4 — O que as pessoas reconhecem em você
- Selecionar os **2–3 temas com melhor resultado**.
- Para cada tema: subtítulo em negrito + parágrafo narrativo de 2–3 frases.
- Linguagem concreta, ancorada nos descritores do CORE-COMP-REF, mas sem usar termos técnicos.
- Foco em **comportamentos observáveis** reconhecidos pelos avaliadores, não em traços de personalidade.

### Seção 5 — Onde você pode crescer
- Selecionar os **1–2 temas com menor resultado** ou maior necessidade de desenvolvimento.
- Mesmo formato da Seção 4: subtítulo + parágrafo narrativo.
- Tom construtivo e propositivo — descrever o espaço de crescimento, não o déficit.
- Incluir o tema transversal (se identificado no IMFA-TECH) como ponto de atenção.
- Foco em **comportamentos observáveis**, não em personalidade.

### Seção 6 — Como você se vê vs. como os outros te veem
**Abertura fixa (idêntica para todos):**

> Nesta avaliação, comparamos como você se avaliou com as notas que recebeu dos outros participantes. Essa comparação ajuda a entender como a sua visão sobre si mesmo se alinha com a percepção das pessoas ao seu redor.

**Depois, conteúdo variável:**
- Descrever o padrão de gap identificado no IMFA-TECH (subestimação, superestimação ou alinhamento).
- Citar os temas onde o gap é mais relevante, sem expor números.
- Tom neutro e construtivo: se subestima → "Reconhecer suas próprias forças é tão importante quanto trabalhar os pontos de melhoria"; se superestima → "Buscar mais feedback pode ajudar a calibrar a sua percepção com a dos colegas".

### Seção 7 — Sua evolução em relação ao ano anterior
**Condição:** Só incluir quando existem dados IMFA-TECH do ciclo imediatamente anterior para o mesmo avaliado. Se for a primeira avaliação, omitir esta seção inteira.

**Abertura fixa:**

> A tabela abaixo compara os seus resultados de [Ano atual] com os de [Ano anterior]. Isso permite que você veja onde houve progresso, onde os resultados se mantiveram e se algum tema precisa de mais atenção.

**Componente 1 — Tabela evolutiva:**
Tabela com 4 colunas: *Tema avaliado*, *[Ano anterior]* (faixa + ícone), *[Ano atual]* (faixa + ícone), *Variação* (tag descritiva).

**Vocabulário padronizado para a coluna "Variação":**

| Condição (baseada no Δ da média de avaliadores) | Tag | Estilo visual |
|---|---|---|
| Δ ≥ +0.30 | **↑ Melhorou de forma expressiva** | Verde (tag `.up`) |
| Δ entre +0.15 e +0.29 | **↑ Melhorou levemente** | Verde (tag `.up`) |
| Δ entre −0.14 e +0.14 | **→ Se manteve estável** | Azul (tag `.stable`) |
| Δ entre −0.29 e −0.15 | **↓ Recuou levemente** | Vermelho (tag `.down`) |
| Δ ≤ −0.30 | **↓ Recuou de forma expressiva** | Vermelho escuro (tag `.down-faixa`) |

**Nota sobre mudança de faixa:** Se a competência mudou de faixa (ex: de "Ponto forte" para "Dentro do esperado"), usar a tag `.down-faixa` (vermelho escuro) mesmo que o Δ numérico seja leve, para sinalizar visualmente que a classificação mudou.

**Componente 2 — Cards de insight (3 blocos narrativos):**
Após a tabela, incluir 3 cards visuais:

1. **"O que melhorou"** (card verde): Listar os temas que subiram ou se consolidaram. Mencionar evolução na autopercepção se relevante. Tom positivo e reforçador.
2. **"O que precisa de atenção"** (card vermelho): Listar temas que recuaram ou que permanecem como pontos para desenvolver pelo segundo ciclo consecutivo. Destacar se os comentários qualitativos repetem os mesmos temas do ano anterior (indicando que o desenvolvimento ainda não produziu mudança percebida). Tom construtivo, não punitivo.
3. **"O que se manteve estável"** (card azul): Listar temas que não variaram significativamente. Diferenciar entre estabilidade positiva (forças mantidas) e estabilidade que merece atenção (fragilidades crônicas).

**Regras:**
- **Nunca** mostrar notas numéricas nem deltas numéricos — usar apenas faixas descritivas e tags de variação textual.
- Cada card tem 2–4 frases, máximo.
- Se uma competência permanece como "Ponto para desenvolver" por 2+ ciclos, usar a expressão "pelo segundo ano consecutivo" para sinalizar persistência sem soar punitivo.
- A análise da variação usa os dados internos do IMFA-TECH (médias, deltas), mas o output para o avaliado é sempre em linguagem descritiva.

### Seção 8 — Principais temas dos comentários
Dividir em 2 blocos: **"O que manter"** e **"O que melhorar"**.

**Regras:**
- Cada bloco com 2–4 itens em bullet points.
- Cada item = 1 frase síntese, agrupada por tema (ex: "comunicação", "presença no campo").
- **Nunca** transcrever comentários literalmente.
- **Nunca** identificar a fonte (não dizer "um liderado disse", "o diretor mencionou").
- Se não houver dados qualitativos para uma competência, não inventar.

### Seção 9 — E agora?
**Texto institucional fixo (idêntico para todos os avaliados):**

> A partir destes resultados, será construído um Plano de Desenvolvimento Individual (PDI) em conjunto com a sua liderança direta. Esse plano vai definir ações concretas, prazos e metas para trabalhar os pontos identificados nesta avaliação.
>
> Você receberá uma conversa individual com o seu gestor para discutir esses resultados, tirar dúvidas e alinhar as prioridades de desenvolvimento. Esse é um momento de diálogo — aproveite para trazer a sua perspectiva.
>
> O acompanhamento será feito ao longo dos próximos meses, com revisões periódicas para verificar o progresso e ajustar o plano conforme necessário.

---

## 5. Regras de Padronização

1. **Todos os avaliados** recebem exatamente as mesmas seções, na mesma ordem, com os mesmos títulos.
2. O que varia é o conteúdo dentro de cada seção (seções 1, 3, 4, 5, 6, 7, 8).
3. As **seções 2 e 9** são textos institucionais fixos, idênticos para todos.
4. A **seção 7 (comparativo)** só é incluída quando existem dados do ciclo anterior. Se for a primeira avaliação, o documento tem 8 seções (sem a 7) e a numeração se ajusta.
5. O **painel (seção 3)** sempre mostra as 6 competências, mesmo que todas estejam na mesma faixa.
6. **Nenhum avaliado** recebe nota numérica — nem no painel, nem no comparativo, nem em qualquer outra seção.
7. **Nenhum comentário** é transcrito literalmente.
8. **Nenhum avaliador** é identificável direta ou indiretamente.
9. O documento é **confidencial** — uso exclusivo do avaliado e sua liderança direta.
10. A seção comparativa (7) usa **apenas faixas descritivas e tags de variação textual**, nunca deltas numéricos.

---

## 6. Formatos de Saída

Três formatos disponíveis. O usuário pode solicitar um ou mais:

### 6a. Formato `.docx` (Word)
- **Uso:** Entrega direta, arquivamento, impressão.
- **Fonte:** Arial.
- **Tamanho base:** 11pt corpo, 16pt título principal, 13pt subtítulos.
- **Cabeçalho:** "Avaliação de Desempenho 360° — Ciclo [Ano]" (alinhado à direita, itálico).
- **Rodapé:** "Documento confidencial — uso exclusivo do avaliado e sua liderança direta" (centralizado, itálico).
- **Paleta de cores:** Azul escuro (#1F4E79) para títulos, verde (#2E7D32) para positivos, vermelho (#C62828) para pontos de atenção, cinza (#424242) para corpo de texto.
- **Fluxo de geração (ordem de preferência):**
  1. **Pandoc (preferencial):** Gerar o HTML primeiro (6c), depois converter:
     ```bash
     pandoc SE_AD_2025_Nome.html -o SE_AD_2025_Nome.docx --reference-doc=template_ad.docx
     ```
     Se `template_ad.docx` não estiver disponível, omitir `--reference-doc` (pandoc usará estilos padrão).
  2. **python-docx (alternativa):** Se pandoc não estiver instalado, gerar via Python:
     ```python
     from docx import Document
     doc = Document()
     # ... montar seções programaticamente
     doc.save('SE_AD_2025_Nome.docx')
     ```
  3. **Fallback manual:** Entregar apenas o .html e instruir o usuário a abrir no Word e salvar como .docx.

### 6b. Formato `.pdf`
- **Uso:** Visualização, distribuição somente-leitura.
- **Fluxo de geração (ordem de preferência):**
  1. **weasyprint (preferencial):** Converter diretamente do HTML (preserva CSS fielmente):
     ```bash
     weasyprint SE_AD_2025_Nome.html SE_AD_2025_Nome.pdf
     ```
  2. **LibreOffice headless (alternativa):** Se weasyprint não estiver disponível:
     ```bash
     soffice --headless --convert-to pdf SE_AD_2025_Nome.html
     ```
  3. **Fallback manual:** Instruir o usuário a abrir o .html no navegador e imprimir como PDF (Ctrl+P → Salvar como PDF).
- **Nota:** O `@media print` do HTML já garante que todas as abas sejam expandidas e o bloco de confirmação seja ocultado na versão impressa/PDF.

### 6c. Formato `.html` (Intranet)
- **Uso:** Publicação direta na intranet corporativa, acesso pelo navegador do avaliado.
- **Arquivo:** HTML único, autocontido (`<style>` inline, sem arquivos externos além de fontes do Google Fonts).
- **Fonte:** `Source Sans 3` (Google Fonts), com fallback para `Segoe UI, Arial, sans-serif`.
- **Paleta de cores (CSS variables):** Mesma paleta do `.docx` — `--primary: #1F4E79`, `--accent: #2E75B6`, `--green: #2E7D32`, `--yellow: #F9A825`, `--red: #C62828`, `--body-text: #424242`.
- **Layout:** `max-width: 780px`, centralizado, fundo branco com sombra sutil. Responsivo (adapta a telas < 600px).
- **Barra superior:** Fundo azul escuro (--primary), com "Avaliação de Desempenho 360°" à esquerda e "Ciclo [Ano]" à direita.
- **Barra inferior (footer):** Fundo azul escuro, texto "Documento confidencial — uso exclusivo do avaliado e sua liderança direta".
- **Painel de competências (Seção 3):** Tabela HTML com badges em formato pill (border-radius arredondado):
  - 🟢 Ponto forte reconhecido → fundo verde claro (#E8F5E9), texto verde (#2E7D32)
  - 🟡 Dentro do esperado → fundo amarelo claro (#FFF8E1), texto âmbar (#E6A000)
  - 🔴 Ponto para desenvolver → fundo vermelho claro (#FFEBEE), texto vermelho (#C62828)
- **Heatmap por descritor (Seção 3, abaixo da tabela):** Componente accordion interativo dentro da aba "Resultados". Cada competência é um bloco `.hm-comp` clicável que expande para mostrar 5 descritores com barra de progresso colorida + badge de faixa. Classes: `.hm-comp-header` (com `.open`), `.hm-desc-list` (com `.open`), `.hm-desc-row`, `.hm-bar-track`, `.hm-bar-fill` (`.forte`/`.esperado`/`.desenvolver`), `.hm-desc-badge`. Barras: verde `#97C459`, âmbar `#EF9F27`, vermelho `#E24B4A`. Legenda de cores no topo. Primeiro bloco aberto por padrão. Accordion behavior (1 aberto por vez) via JS.
- **Seção de autopercepção (Seção 6):** Caixa destacada com borda esquerda azul (highlight-box).
- **Tabela evolutiva (Seção 7):** Tabela `.evo-table` com badges de faixa (mesmo estilo do painel) + tags de variação `.evo-tag` em formato pill:
  - `.up` → fundo verde claro (#E8F5E9), texto verde (#2E7D32) — para melhorias
  - `.stable` → fundo azul claro (#E3F2FD), texto azul (#1565C0) — para estabilidade
  - `.down` → fundo vermelho claro (#FFEBEE), texto vermelho (#C62828) — para recuos leves
  - `.down-faixa` → fundo vermelho médio (#FFCDD2), texto vermelho escuro (#B71C1C) — para recuos com mudança de faixa
- **Cards de insight (Seção 7):** 3 cards `.insight-card` com borda esquerda colorida:
  - `.positive` → fundo verde claro, borda verde
  - `.attention` → fundo vermelho claro, borda vermelha
  - `.neutral` → fundo azul claro, borda azul
- **Temas dos comentários (Seção 8):** Listas com bullet points coloridos (verde para manter, vermelho para melhorar), fundo cinza claro por item.
- **Navegação por abas coloridas (obrigatório):** O HTML usa estrutura de tabs com etiquetas coloridas para facilitar navegabilidade. Implementação:
  - **CSS variables de cor por aba:** Definir no `:root` uma variável por aba:
    - `--tab-visao: #2E75B6` (azul — contexto/introdução)
    - `--tab-resultados: #F9A825` (âmbar — painel de dados)
    - `--tab-destaques: #2E7D32` (verde — pontos fortes e crescimento)
    - `--tab-evolucao: #7B61A6` (roxo — análise temporal)
    - `--tab-comentarios: #1D9E75` (teal — voz dos avaliadores)
  - **CSS de `.nav-btn`:** Cada botão contém um `.dot` (span circular 8px com `border-radius: 50%`) cuja cor de fundo é a variável da aba correspondente. O botão usa `opacity: 0.65` no estado inativo e `opacity: 1` no ativo/hover. O atributo `data-tab` no botão vincula a cor via seletor CSS: `.nav-btn[data-tab="visao-geral"] .dot { background: var(--tab-visao); }`. No estado `.active`, o botão recebe `color` e `border-bottom-color` na cor da aba, e o `.dot` recebe `transform: scale(1.25)`.
  - **CSS de `.nav-tabs`:** Flex container com scroll horizontal oculto (`scrollbar-width: none`, `overflow-x: auto`).
  - **CSS de `.tab-pane`:** Oculto com `display: none`; `.tab-pane.active` com `display: block` e animação `fadeIn` (0.35s, translateY 6px→0 + opacity 0→1).
  - **HTML:** A div `.nav-tabs` fica logo abaixo da `.header-bar`, com 5 botões (cada um com `data-tab` e `<span class="dot"></span>` antes do texto): **Visão Geral** (ativa por padrão), **Resultados**, **Destaques**, **Evolução**, **Comentários**.
  - **Agrupamento das seções em tabs:**
    - *Visão Geral:* Seção 1 (Cabeçalho) + Seção 2 (Como funciona)
    - *Resultados:* Seção 3 (Painel de competências)
    - *Destaques:* Seção 4 (O que reconhecem) + Seção 5 (Onde crescer)
    - *Evolução:* Seção 6 (Autopercepção) + Seção 7 (Comparativo ano-a-ano)
    - *Comentários:* Seção 8 (Temas dos comentários) + Seção 9 (E agora?)
  - **JavaScript:** Função `openTab(tabId, btn)` no final do `<body>` que remove `.active` de todos os painéis e botões, e adiciona ao clicado e ao painel correspondente.
  - **Regra de impressão:** `@media print` oculta `.nav-tabs` (`display: none !important`) e força exibição de todos os `.tab-pane` (`display: block !important`), garantindo impressão/PDF do documento inteiro.
  - **Nota:** Se a Seção 7 (comparativo) não existir (primeira avaliação), a aba "Evolução" contém apenas a Seção 6 (autopercepção).
- **Print-friendly:** Inclui `@media print` para impressão limpa, com todas as abas expandidas. O bloco de confirmação é ocultado na impressão.
- **Confirmação de leitura (obrigatório no HTML):** Bloco `.read-confirmation` fixo após as tabs (fora das abas, visível em qualquer aba). Componentes:
  - Título "Confirmação de leitura" + texto explicativo
  - Checkbox com label: "Confirmo que li e compreendi os resultados da minha Avaliação de Desempenho 360° — Ciclo [Ano]."
  - Sublabel: "Ao confirmar, o RH e sua liderança serão notificados automaticamente."
  - Botão "Enviar confirmação" (desabilitado até o checkbox ser marcado)
  - 3 estados visuais: `.sending` (spinner), `.success` (check verde + timestamp), `.error` (mensagem vermelha)
  - **JavaScript:** 5 variáveis de configuração no `<script>` (`GESTOR_NOME`, `GESTOR_EMAIL`, `DOCUMENTO`, `CICLO`, `DOC_TOKEN`) + `WEBHOOK_URL` (URL do Power Automate). A variável `DOC_TOKEN` é um token HMAC-SHA256 gerado no momento da criação do HTML (ver nota no SKILL.md). Função `enviarConfirmacao()` faz `fetch(WEBHOOK_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...payload, token: DOC_TOKEN }) })` com os dados do gestor + timestamp + token.
  - **Backend:** Power Automate flow com trigger "When a HTTP request is received" → **Validar token** (Compose: recalcular HMAC com a mesma chave secreta e comparar com `triggerBody()?['token']`; se inválido → Response 403) → **Verificar duplicidade** (Get items no SharePoint filtrando por `gestor_email + documento + ciclo`; se já confirmado → Response 409) → Create item no SharePoint (lista `PDI_Confirmacoes_Leitura`) → Send email ao HRBP (opcional) → Response 200. Ver `references/EMAIL-PDI-AUTOMATION.md` para detalhes.
  - **Regra de impressão:** `.read-confirmation { display: none; }` no `@media print`.
- **Nomenclatura do arquivo:** `SE_AD_[ANO]_[NOME].html`

### Regra de consistência entre formatos
Os três formatos devem conter **exatamente o mesmo conteúdo textual** — mesmas 9 seções (ou 8, se sem comparativo), mesmos textos fixos, mesmos dados variáveis. A diferença é apenas de apresentação visual. Se o conteúdo for alterado em um formato, deve ser refletido nos demais.

---

## 7. Checklist de Validação (antes de entregar)

### Conteúdo (todos os formatos)
- [ ] Todas as 9 seções presentes (ou 8 se primeira avaliação), na ordem correta, com títulos exatos?
- [ ] Seções 2 e 9 são os textos fixos, sem alteração?
- [ ] Painel mostra as 6 competências com faixa descritiva + ícone, sem nota numérica?
- [ ] Competências ordenadas da maior para a menor?
- [ ] Nenhum jargão técnico-estatístico presente?
- [ ] Linguagem em segunda pessoa ("você") consistente?
- [ ] Nenhum avaliador identificável?
- [ ] Nenhum comentário transcrito literalmente?
- [ ] Seção de autopercepção inclui explicação acessível do conceito de gap?
- [ ] Documento ≤ ~1200 palavras?
- [ ] Cabeçalho e rodapé presentes?
- [ ] Conteúdo textual idêntico entre .docx, .pdf e .html?

### Seção comparativa (checklist adicional — Seção 7)
- [ ] Tabela evolutiva mostra as 6 competências com faixa do ano anterior + faixa do ano atual + tag de variação?
- [ ] Nenhuma nota numérica nem delta numérico presente?
- [ ] Tags de variação usam o vocabulário padronizado (6 opções da tabela)?
- [ ] Mudança de faixa sinalizada com tag `.down-faixa` (vermelho escuro)?
- [ ] 3 cards de insight presentes: "O que melhorou", "O que precisa de atenção", "O que se manteve estável"?
- [ ] Competências crônicas (2+ ciclos como "Ponto para desenvolver") mencionadas com a expressão "pelo segundo ano consecutivo"?

### HTML (checklist adicional)
- [ ] Arquivo único autocontido (CSS inline, sem dependências externas além de Google Fonts)?
- [ ] CSS variables com a paleta padrão definida na seção 6c?
- [ ] Layout responsivo funcional (testar mentalmente para < 600px)?
- [ ] **Navegação por abas com etiquetas coloridas implementada?** (`.nav-btn` com `.dot` colorido + `data-tab` + 5 CSS variables `--tab-*`)
- [ ] **Cada botão tem `data-tab` e `<span class="dot"></span>` antes do texto?**
- [ ] **Aba ativa mostra cor temática na borda inferior, no texto e no dot ampliado (`scale(1.25)`)?**
- [ ] **Abas inativas com `opacity: 0.65`, ativas/hover com `opacity: 1`?**
- [ ] **Função `openTab()` presente no `<script>` ao final do `<body>`?**
- [ ] **`@media print` oculta `.nav-tabs` e força `display: block !important` em todos os `.tab-pane`?**
- [ ] Badges com faixa descritiva usando as classes corretas (`.forte`, `.esperado`, `.desenvolver`)?
- [ ] **Heatmap por descritor presente na aba "Resultados", abaixo da tabela-resumo?**
- [ ] **6 blocos accordion (1 por competência) com 5 descritores cada?**
- [ ] **Barras de progresso coloridas (verde/âmbar/vermelho) + badge de faixa por descritor?**
- [ ] **Accordion behavior (1 bloco aberto por vez, primeiro aberto por padrão)?**
- [ ] **Legenda de cores no topo do heatmap?**
- [ ] **Nenhuma nota numérica visível nos descritores (apenas barra + faixa)?**
- [ ] Tabela evolutiva com classes `.evo-table`, `.evo-tag` (`.up`, `.stable`, `.down`, `.down-faixa`)?
- [ ] Cards de insight com classes `.insight-card` (`.positive`, `.attention`, `.neutral`)?
- [ ] Highlight-box presente na seção de autopercepção?
- [ ] Listas de temas qualitativos com bullet colorido (verde/vermelho)?
- [ ] Nomenclatura: `SE_AD_[ANO]_[NOME].html`?

### Confirmação de leitura (checklist adicional)
- [ ] Bloco `.read-confirmation` presente após as tabs (fora do `.content`, antes do `.footer-bar`)?
- [ ] Checkbox com label completa + sublabel sobre notificação automática?
- [ ] Botão "Enviar confirmação" desabilitado até checkbox ser marcado?
- [ ] 3 estados visuais implementados: `.sending` (spinner), `.success` (check verde + timestamp), `.error`?
- [ ] 4 variáveis de configuração preenchidas no `<script>`: `GESTOR_NOME`, `GESTOR_EMAIL`, `DOCUMENTO`, `CICLO`?
- [ ] `DOC_TOKEN` preenchido (HMAC-SHA256 gerado na criação do HTML)?
- [ ] `WEBHOOK_URL` definida (placeholder ou URL real)?
- [ ] Função `enviarConfirmacao()` com `fetch()` POST incluindo `token: DOC_TOKEN` no payload?
- [ ] `@media print` oculta `.read-confirmation`?

---

## Exemplo de Referência — Síntese para Avaliado (Caso 1: Carlos Mendes)

> **Nota:** Este exemplo serve como calibração de formato, tom e nível de detalhe. Use como referência ao gerar sínteses reais. Os dados vêm do `VALIDATION-CASES.md`, Caso 1.

---

### Seção 1 — Cabeçalho

| Campo | Valor |
|---|---|
| Nome | Carlos Mendes |
| Cargo | Gerente de Operações |
| Ciclo | 2025 |
| Participantes | 4 liderados, 3 colegas gestores, 1 diretor + autoavaliação |

### Seção 2 — Como funciona esta avaliação

> Na avaliação 360°, pessoas que trabalham diretamente com você — liderados, colegas gestores e diretores — respondem a um questionário sobre seis temas ligados à sua atuação como gestor. Você também se avalia nos mesmos temas.
>
> Cada pergunta usa uma escala de 1 a 5, onde 1 significa "raramente" e 5 significa "quase sempre". Os resultados são agrupados por tema, e a média das respostas define o seu resultado em cada um deles.
>
> O objetivo desta devolutiva não é premiar ou punir — é ajudar você a enxergar com clareza o que já funciona bem e onde existem espaços para crescer. A partir desses resultados, será construído junto com sua liderança um plano de desenvolvimento individual.

### Seção 3 — Seus resultados por tema

| Tema avaliado | Resultado | Comentário |
|---|---|---|
| Conhecimento Técnico | 🟢 Ponto forte reconhecido | Você é referência técnica para a equipe e para outras áreas |
| Orientação para Resultados | 🟢 Ponto forte reconhecido | Sua energia e determinação para alcançar metas são reconhecidas por todos |
| Planejamento e Organização | 🟡 Dentro do esperado | Você organiza bem as atividades e cumpre prazos, com espaço para envolver mais a equipe |
| Otimização de Recursos | 🟡 Dentro do esperado | Há boas práticas de uso de recursos, com oportunidade de ampliar para toda a equipe |
| Trabalho em Equipe | 🟡 Dentro do esperado | A colaboração funciona, mas a equipe gostaria de mais momentos de troca e escuta |
| Desenvolvimento de Pessoas | 🔴 Ponto para desenvolver | A equipe sente falta de mais orientação, feedback e acompanhamento individual |

*(Abaixo da tabela: heatmap accordion com 6 blocos × 5 descritores cada — ver spec completa na seção 3)*

### Seção 4 — O que as pessoas reconhecem em você

**Conhecimento Técnico**
Você domina os processos e ferramentas da área com profundidade. As pessoas recorrem a você quando há dúvidas técnicas complexas, e reconhecem que você se mantém atualizado. Essa competência é consistente — todos os avaliadores convergem nessa percepção.

**Orientação para Resultados**
Sua determinação em alcançar metas é visível. Você mantém o foco mesmo diante de obstáculos e transmite um senso de urgência produtivo para a equipe. Os avaliadores reconhecem sua capacidade de priorizar o que realmente importa.

### Seção 5 — Onde você pode crescer

**Desenvolvimento de Pessoas**
Sua equipe valoriza sua experiência técnica, mas sente falta de mais proximidade no dia a dia. Há espaço para investir em orientações mais frequentes, feedbacks estruturados e acompanhamento do crescimento individual. Essa é a principal oportunidade de desenvolvimento deste ciclo.

### Seção 6 — Como você se vê vs. como os outros te veem

> Nesta avaliação, comparamos como você se avaliou com as notas que recebeu dos outros participantes. Essa comparação ajuda a entender como a sua visão sobre si mesmo se alinha com a percepção das pessoas ao seu redor.

No tema Desenvolvimento de Pessoas, existe uma diferença significativa entre sua visão e a dos avaliadores. Você se avalia acima do que os avaliadores percebem. Isso não significa que sua percepção esteja errada — mas indica que há uma lacuna entre a sua intenção e o que a equipe vivencia no dia a dia. Buscar mais feedback nesse tema pode ajudar a calibrar essa percepção.

Nos demais temas, sua autoavaliação está alinhada com a visão dos avaliadores.

### Seção 8 — Principais temas dos comentários

**O que manter:**
- Disponibilidade para tirar dúvidas técnicas e resolver problemas complexos
- Foco e disciplina na entrega de resultados

**O que melhorar:**
- Frequência e qualidade do feedback individual aos liderados
- Mais momentos de escuta ativa e acompanhamento do desenvolvimento da equipe

### Seção 9 — E agora?

> A partir destes resultados, será construído um Plano de Desenvolvimento Individual (PDI) em conjunto com a sua liderança direta. Esse plano vai definir ações concretas, prazos e metas para trabalhar os pontos identificados nesta avaliação.
>
> Você receberá uma conversa individual com o seu gestor para discutir esses resultados, tirar dúvidas e alinhar as prioridades de desenvolvimento. Esse é um momento de diálogo — aproveite para trazer a sua perspectiva.
>
> O acompanhamento será feito ao longo dos próximos meses, com revisões periódicas para verificar o progresso e ajustar o plano conforme necessário.

**END_PROTOCOL**
