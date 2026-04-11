---
name: ad-devolutiva
description: "Analisa dados de avaliação de desempenho 360° e gera devolutivas para gestores e líderes. Use esta skill sempre que o usuário pedir para analisar dados de avaliação de desempenho, gerar devolutiva, processar resultados de AD, avaliação 360, feedback 360, assessment de competências, ou quando enviar dados estruturados com notas de autoavaliação e avaliações recebidas (pares, subordinados, superiores). Também acione quando o usuário mencionar 'IMFA', 'devolutiva', 'competências de liderança', 'PDI baseado em avaliação', 'gap de competências', 'análise de desempenho', 'assessment de gestão', ou pedir síntese executiva de avaliação, plano de desenvolvimento individual, ou relatório de competências. Acione proativamente sempre que perceber dados de avaliação em escala Likert 1-5 com múltiplas fontes avaliativas."
---

# AD Devolutiva — Análise de Avaliação de Desempenho 360°

## Objetivo

Processar dados quantitativos e qualitativos de avaliações de desempenho 360° para cargos de gestão/liderança, gerando devolutivas técnicas, sínteses executivas e planos de desenvolvimento individual (PDI).

## Quando usar

- Usuário envia dados de avaliação de desempenho dentro de `<results></results>`
- Usuário pede devolutiva, análise de AD, ou assessment de competências
- Usuário menciona "IMFA", "avaliação 360", "feedback 360", "gap de competências"
- Usuário pede PDI ou plano de desenvolvimento baseado em avaliação
- Usuário pede síntese executiva de resultados de avaliação
- Usuário pede devolutiva para o avaliado, versão intranet, ou documento padronizado para entrega ao gestor avaliado
- Usuário pede PDI para o avaliado, plano de desenvolvimento na versão do avaliado, ou plano de ação para publicação na intranet
- Usuário pede emails do PDI, templates de lembrete, tabela de controle de disparos, automação de nudges ou fluxo Power Automate para acompanhamento do PDI

## Arquitetura da Skill

Esta skill opera em módulos acionados sequencialmente ou sob demanda:

| Módulo | Arquivo | Acionamento |
|--------|---------|-------------|
| Framework de Competências | `references/CORE-COMP-REF.md` | Sempre — base referencial |
| Papéis e Responsabilidades | `references/ROLES-RESP-REF.md` | Sempre — contextualiza por nível |
| Análise Técnica (IMFA-TECH) | `references/IMFA-TECH.md` | Automático ao receber dados |
| Síntese Executiva (IMFA-SUMM) | `references/IMFA-SUMM.md` | Sob solicitação do usuário |
| Síntese p/ Avaliado (IMFA-SUMM-AVALIADO) | `references/IMFA-SUMM-AVALIADO.md` | Sob solicitação — versão intranet/avaliado |
| Plano de Desenvolvimento (IDP-GEN) | `references/IDP-GEN.md` | Sob solicitação do usuário |
| PDI p/ Avaliado (IDP-GEN-AVALIADO) | `references/IDP-GEN-AVALIADO.md` | Sob solicitação — versão intranet/avaliado |
| Emails Automatizados PDI (EMAIL-PDI-AUTO) | `references/EMAIL-PDI-AUTOMATION.md` | Sob solicitação — templates, tabela de controle e fluxo Power Automate |

## Fluxo de Execução

### Fase 0 — Carregar referencial

Ao ser acionada, leia imediatamente:
1. `references/CORE-COMP-REF.md` — framework de 6 competências com descritores e índices (dicionário que ancora toda a análise)
2. `references/ROLES-RESP-REF.md` — matriz de papéis e responsabilidades por nível (Individual Contributor, Manager, Senior Manager), com definições e indicadores esperados. Use para contextualizar a análise conforme o nível hierárquico do avaliado.

As 6 competências do framework são:
- **PD-01:** Desenvolvimento de Pessoas
- **TW-02:** Trabalho em Equipe
- **PO-03:** Planejamento e Organização
- **RO-04:** Orientação para Resultados
- **TK-05:** Conhecimento Técnico
- **RO-06:** Otimização de Recursos

### Fase 1 — Receber, normalizar e validar dados

Os dados podem chegar em formatos diferentes dependendo do ciclo. A skill deve detectar o formato e normalizar antes de qualquer cálculo.

**Formatos aceitos:**
- **Numérico direto:** Valores `1`, `2`, `3`, `4`, `5` (escala Likert já convertida). Típico de ciclos mais antigos (ex: 2023).
- **Textual descritivo:** Rótulos textuais que descrevem a frequência. Típico de ciclos mais recentes (ex: 2024). Requer mapeamento para numérico.

**Mapeamento padrão texto → número (LABEL_MAP):**

| Rótulo textual | Nota |
|---|---|
| `Nunca acontece` | 1 |
| `Quase nunca acontece` | 2 |
| `Ocorre de vez em quando` | 3 |
| `Acontece com frequência` | 4 |
| `Acontece o tempo todo` | 5 |

**Regras de normalização:**
1. **Detecção automática:** Ao carregar os dados, verificar se as colunas quantitativas contêm valores numéricos ou textuais. Se qualquer célula contiver um dos rótulos do LABEL_MAP, aplicar a conversão em todo o dataset.
2. **Conversão:** Para cada célula quantitativa, aplicar: se é numérico (int/float), usar diretamente; se é texto presente no LABEL_MAP, converter para o número correspondente; se é vazio/NaN, tratar como ausente (exclusão pairwise, sem imputação).
3. **Formato misto:** Um mesmo arquivo pode conter ambos os formatos (ex: coluna com `3` e outra com `Acontece com frequência`). A conversão é aplicada célula a célula, não por coluna.
4. **Validação pós-conversão:** Após normalização, todos os valores devem estar no intervalo [1, 5]. Valores fora desse intervalo → sinalizar como erro.
5. **Detecção de colunas qualitativas invertidas:** Em alguns ciclos, as colunas "Coisas para manter" e "Coisas para melhorar" podem estar invertidas na ordem (manter primeiro vs. melhorar primeiro). Verificar o nome do header da coluna para identificar qual é qual — não assumir pela posição.
6. **Mapeamento de perguntas por conteúdo, não por posição (QUESTION_MAP):** A ordem das perguntas dentro de cada bloco de competência pode variar entre ciclos. A skill **nunca assume que o item na posição N é sempre a mesma pergunta**. Em vez disso, lê o texto do header de cada coluna e faz match por palavras-chave para identificar qual descritor aquele item representa. Isso é crítico para:
   - O heatmap por descritor (clusters precisam conter as perguntas corretas independente da ordem)
   - Comparativos ano-a-ano no nível de item (se implementado futuramente)

**Tabela QUESTION_MAP — Palavras-chave de identificação por descritor:**

| Competência | Cluster | Palavras-chave no header (match parcial) |
|---|---|---|
| PD-01 | Clareza de expectativas | "esclarece as expectativas", "nível de orientação" |
| PD-01 | Feedback e reconhecimento | "feedback positivo", "valorizados e respeitados" |
| PD-01 | Ensino e desenvolvimento | "ensina novos procedimentos", "instruções e modelos" |
| PD-01 | Escuta e suporte | "ouve as preocupações", "suporte aos esforços" |
| PD-01 | Resolução de problemas | "resolução de problemas", "PDCA" |
| TW-02 | Confiança e apoio | "relações de confiança", "apoiar as decisões" |
| TW-02 | Resolução de conflitos | "resolver conflitos", "dar e.*receber feedback" |
| TW-02 | Perspectivas dos pares | "perspectivas", "humildade e abertura" |
| TW-02 | Compartilhamento | "compartilhar experiências", "celebrar conquistas" |
| TW-02 | Responsabilidades | "responsabilidades e papéis", "coordenar.*metas" |
| PO-03 | Priorização | "priorizar.*atividades", "focando no.*importante" |
| PO-03 | Planejamento de recursos | "tarefas e recursos", "aproveit.*recursos" |
| PO-03 | Cronogramas e prazos | "cronogramas", "prazos realistas" |
| PO-03 | Coordenação interáreas | "coordenar.*atividades.*áreas", "colegas especialistas" |
| PO-03 | Autonomia e aconselhamento | "planejar.*organizar.*autonomia", "aconselhar.*equipe" |
| RO-04 | Oportunidades de impacto | "oportunidades.*alto impacto", "metas ambiciosas" |
| RO-04 | Metas e energia | "energia e vigor", "satisfação ao alcançar" |
| RO-04 | Proatividade | "tarefas adicionais", "focado.*evitar distrações" |
| RO-04 | Urgência e conclusão | "urgência e determinação", "correções de rota" |
| RO-04 | Priorização e disciplina | "priorizar.*impacto.*resultado", "autodisciplina" |
| TK-05 | Domínio da área | "conhecimento sobre.*departamento", "regras.*processos" |
| TK-05 | Atualização contínua | "manter-se atualizado", "desenvolvimento contínuo" |
| TK-05 | Ferramentas e sistemas | "ferramentas e sistemas", "compreender.*aspectos" |
| TK-05 | Aplicação prática | "aplicar.*conhecimentos técnicos", "resolver problemas.*soluções" |
| TK-05 | Compartilhamento com equipe | "compartilhar.*conhecimentos.*equipe", "impactos.*áreas.*outros" |
| RO-06 | Procedimentos e ferramentas | "procedimentos e ferramentas", "melhor aproveitamento" |
| RO-06 | Redução de custos | "redução de desperdícios", "racionalização.*simplificação" |
| RO-06 | Orientação da equipe | "orienta.*equipe.*redução", "instrui.*equipe.*bom uso" |
| RO-06 | Eliminação de desperdícios | "eliminar desperdícios.*retrabalhos", "otimização.*recursos financeiros" |
| RO-06 | Maximização de resultados | "maximiza resultados", "baixo custo.*sem comprometer" |

**Lógica de matching:**
- Para cada coluna quantitativa, extrair o texto do header.
- Comparar (case-insensitive, com regex parcial) contra as palavras-chave da tabela.
- Atribuir ao cluster correspondente.
- Se uma coluna não fizer match com nenhum cluster → sinalizar como "não mapeada" e incluir na média geral da competência sem atribuir a um cluster.
- Se dois ciclos têm perguntas na mesma competência com ordem diferente, o QUESTION_MAP garante que o cluster "Feedback e reconhecimento" sempre contém as perguntas sobre feedback, independente de estarem na posição 3 ou na posição 7.

**Estrutura esperada por competência (após normalização):**
- `competency_id` (marcado com `##`) — identificador da competência
- `self_assessment` — nota do avaliado (escala 1-5, já convertida)
- `received_ratings` — array de notas recebidas de pares, subordinados e superiores (escala 1-5, já convertidas)

Valide que os dados são consistentes com o framework antes de prosseguir.

### Fase 2 — Análise Técnica (padrão)

Leia `references/IMFA-TECH.md` e execute o pipeline analítico completo:

1. **Análise Quantitativa:**
   - Calcular média e desvio padrão por competência
   - Identificar forças (score ≥ 4.5 com σ ≤ 1.2)
   - Identificar oportunidades de desenvolvimento (score ≤ 3.5)
   - Calcular gap: |autoavaliação − média dos avaliadores|
   - Sinalizar discrepâncias significativas (delta ≥ 1.0)
   - Detectar outliers (σ ≥ 1.2)

2. **Análise Qualitativa** (se dados qualitativos estiverem presentes):
   - Codificação temática das narrativas
   - Análise de sentimento
   - Cruzamento com dados quantitativos
   - Extração de temas prioritários

3. **Output por competência:**
   - Métricas: média, desvio padrão
   - Evidências extraídas dos dados
   - Gap analysis: autoavaliação vs. média dos pares
   - Recomendações em formato SMART

4. **Resumo executivo:** Score de efetividade (IMFA), priorização por delta e variância.

### Fase 3 — Síntese Executiva (sob demanda)

Quando o usuário solicitar síntese, resumo executivo ou pedir explicitamente, leia `references/IMFA-SUMM.md` e gere uma versão condensada da análise com score de efetividade consolidado, orientada para consumo rápido pela liderança sênior.

### Fase 3b — Síntese para o Avaliado / Intranet (sob demanda)

Quando o usuário solicitar a devolutiva na versão do avaliado, ou indicar que o documento será publicado na intranet para leitura direta pelo gestor avaliado, leia `references/IMFA-SUMM-AVALIADO.md` e gere o documento padronizado seguindo rigorosamente o template de 9 seções (ou 8, se não houver dados do ciclo anterior), com linguagem acessível, sem notas numéricas, sem jargão estatístico e sem identificação de avaliadores. Se dados do ciclo anterior estiverem disponíveis, incluir a Seção 7 (comparativo ano-a-ano) com tabela evolutiva, tags de variação textual e cards de insight. Produzir em `.docx` + `.pdf` + `.html` (ver seção 6 do reference para especificações de cada formato).

### Fase 4 — Plano de Desenvolvimento Individual (sob demanda)

Quando o usuário solicitar PDI, plano de ação ou desenvolvimento, leia `references/IDP-GEN.md` e construa:

1. **Análise de Forças:** Top competências (≥ 4.5), estratégia de alavancagem
2. **Oportunidades de Desenvolvimento:** Competências baixas (≤ 3.5), alta variância, gaps significativos
3. **Objetivos SMART:** Vinculados aos descritores do CORE-COMP-REF
4. **Atividades de Desenvolvimento:** Treinamentos, projetos, avaliações com marcos temporais
5. **Métricas de Acompanhamento:** Taxa de conclusão, score de efetividade

### Fase 4b — PDI para o Avaliado / Intranet (sob demanda)

Quando o usuário solicitar o PDI na versão do avaliado, ou indicar que o documento será publicado na intranet para leitura direta pelo gestor avaliado, leia `references/IDP-GEN-AVALIADO.md` e gere o documento padronizado seguindo rigorosamente o template de 7 seções, com tom motivacional de coaching, sem notas numéricas, sem jargão estatístico, sem termos como SMART/KPI/baseline e sem identificação de avaliadores. Traduzir os objetivos SMART do IDP-GEN em ações concretas com linguagem acessível. Produzir em `.docx` + `.pdf` + `.html` (ver seção 6 do reference para especificações de cada formato).

### Fase 5 — Emails Automatizados do PDI (sob demanda)

Quando o usuário solicitar os emails de acompanhamento, templates de lembrete, tabela de controle ou fluxo de automação, leia `references/EMAIL-PDI-AUTOMATION.md` e produza:

1. **Templates de email HTML** (4 tipos): boas-vindas, lembrete mensal, check-in, encerramento. Mesma identidade visual e tom coaching do PDI.
2. **Tabela de controle** (`.xlsx`): 14 colunas × 13 linhas por gestor (mês 0–12), com ações, datas, tipos e status de envio. Pronta para upload em SharePoint List.
3. **Documentação do Power Automate flow**: Trigger mensal → Get items → Switch por tipo → Compose HTML → Send email (Para: avaliado, CC: gestor + HRBP) → Update status.

## Diretrizes de Output

- **Formato:** Conciso, objetivo, específico — sem preâmbulos
- **Idioma:** PT-BR (padrão) ou EN-US conforme contexto do usuário
- **Audiência:** Técnica, nível executivo (C-suite visibility)
- **Encerramento:** Sempre perguntar "Próxima avaliação?" ao finalizar

## Notas Importantes

- Os limiares (≥ 4.5 para forças, ≤ 3.5 para oportunidades, delta ≥ 1.0 para discrepâncias) são calibrados e consistentes entre todos os módulos.
- O framework CORE-COMP-REF é a única fonte de verdade para competências e descritores.
- Nunca inventar evidências ou inferir dados não presentes no input.
- Priorizar achados por impacto: delta alto + variância alta = prioridade máxima.
