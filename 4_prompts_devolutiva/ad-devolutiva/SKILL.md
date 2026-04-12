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

Os dados podem chegar em formatos diferentes dependendo do ciclo (numérico direto ou rótulos textuais). O módulo IMFA-TECH contém todas as regras de normalização, incluindo:

- **LABEL_MAP:** Mapeamento de rótulos textuais para notas 1–5 (ver `references/IMFA-TECH.md`, seção 2.1)
- **QUESTION_MAP:** Mapeamento de perguntas a clusters por conteúdo do header, não por posição (ver `references/IMFA-TECH.md`, seção 2.5)
- **Regras de detecção:** Formato misto, colunas qualitativas invertidas, validação pós-conversão (ver `references/IMFA-TECH.md`, seções 2.2–2.6)

**Ação:** Ao receber dados, leia `references/IMFA-TECH.md` e execute o pré-processamento completo (seções 2.1 a 2.6) antes de qualquer cálculo.

**Estrutura esperada por competência (após normalização):**
- `competency_id` — identificador da competência
- `self_assessment` — nota do avaliado (escala 1–5, já convertida)
- `received_ratings` — array de notas recebidas de pares, subordinados e superiores (escala 1–5, já convertidas)

Valide que os dados são consistentes com o framework antes de prosseguir.

### Fase 2 — Análise Técnica (padrão)

Leia `references/IMFA-TECH.md` e execute o pipeline analítico completo.

**Regra obrigatória:** Todos os cálculos quantitativos devem ser realizados via execução de código Python (ver IMFA-TECH, seção "Execução Computacional"). O JSON resultante é o artefato de entrada para todas as fases seguintes.

O pipeline inclui:
1. **Análise Quantitativa** (via código Python): média, desvio padrão, delta, classificação por faixa
2. **Análise Qualitativa** (se houver comentários): identificação de temas, sentimento, cruzamento com dados quantitativos
3. **Output por competência:** métricas + evidências + gap analysis + recomendações SMART
4. **Resumo executivo:** Score IMFA, priorização por delta e variância

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

- Os limiares (≥ 4.5 para forças, ≤ 3.5 para oportunidades, delta ≥ 1.0 para discrepâncias) são calibrados e consistentes entre todos os módulos. Zonas de transição (4.30–4.49 e 3.30–3.50) dependem de σ e tamanho amostral — ver IMFA-TECH seção 4.2 para regras completas.
- Se o número total de avaliadores (excluindo auto) for < 3, o resultado é **preliminar** com baixa confiança.
- O framework CORE-COMP-REF é a única fonte de verdade para competências e descritores.
- Nunca inventar evidências ou inferir dados não presentes no input.
- Priorizar achados por impacto: delta alto + variância alta = prioridade máxima.
- **Segurança do webhook:** Ao gerar HTMLs com confirmação de leitura (Fases 3 e 4), incluir a variável `DOC_TOKEN` (HMAC-SHA256 de `gestor_email|documento|ciclo` com chave secreta compartilhada). O token é enviado junto ao payload do webhook e validado no Power Automate antes de gravar no SharePoint. Ver `EMAIL-PDI-AUTOMATION.md` seção 5.1 para o fluxo completo de validação.
