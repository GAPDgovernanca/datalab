# EMAIL-PDI-AUTOMATION — Sistema de Emails Automatizados do PDI

**PROTOCOL_ID:** EMAIL-PDI-AUTO-01  
**VERSION:** 1.0  
**OBJECTIVE:** Gerar templates de email e tabela de controle para nudges automatizados do PDI via Power Automate  
**LANG:** PT-BR  
**PLATAFORMA:** Microsoft 365 / Power Automate / SharePoint

---

## 1. Contexto e Propósito

Este módulo produz os artefatos necessários para automatizar o envio de emails de acompanhamento do PDI ao longo dos 12 meses do ciclo. O objetivo é transformar o PDI em ferramenta viva, com lembretes mensais que reforçam as ações e preparam o avaliado para os check-ins com a liderança.

**Acionamento:** Quando o usuário solicitar os emails do PDI, os templates de nudge, a tabela de controle de disparos, ou o fluxo de automação.

**Dependências:** Requer que IDP-GEN e/ou IDP-GEN-AVALIADO já tenham sido executados (ações, prazos, competências e marcos definidos).

---

## 2. Arquitetura da Solução

### 3 Camadas

| Camada | Artefato | Descrição |
|---|---|---|
| **1 — Templates** | 4 modelos de email HTML | Boas-vindas, lembrete mensal, check-in, encerramento |
| **2 — Dados** | Tabela de controle (SharePoint List ou Excel) | 1 linha por gestor por mês (13 linhas por gestor: mês 0–12) |
| **3 — Motor** | Power Automate flow | Recorrência mensal, lê tabela, renderiza template, envia email, atualiza status |

### Destinatários de cada email

| Campo | Destinatário |
|---|---|
| **Para:** | Avaliado (`gestor_email`) |
| **CC:** | Gestor direto (`gestor_direto_email`) + HRBP (`hrbp_email`) |

---

## 3. Templates de Email (Camada 1)

### Tom e estilo
Mesmo tom motivacional de coaching do IDP-GEN-AVALIADO. Segunda pessoa ("você"). Sem jargão. Frases curtas. Cada email deve ser lido em menos de 2 minutos.

### Identidade visual
Mesma paleta do PDI e da Síntese: `--primary: #1F4E79`, `--accent: #2E75B6`, `--green: #2E7D32`, `--red: #C62828`, `--light-gray: #F5F5F5`. Fonte: `Source Sans 3` com fallback `Segoe UI, Arial, sans-serif`.

### Estrutura comum a todos os templates

| Elemento | Descrição |
|---|---|
| **Header** | Barra azul escuro com título à esquerda e "Ciclo [Ano]" ou "Mês X de 12" à direita |
| **Body** | Saudação com nome, subtítulo em caixa alta, conteúdo variável por tipo |
| **CTA** | Botão "Acessar meu PDI na intranet" (link para o HTML do PDI na intranet) |
| **Footer** | Texto explicativo + link para RH |

### 4 Tipos de template

#### Template 1 — Boas-vindas (mês 0)
- **Quando:** Dia da entrega do PDI ao avaliado.
- **Assunto:** `PDI [Ciclo] | Seu plano de desenvolvimento está pronto, [Nome]`
- **Conteúdo:** Saudação, explicação do que é o PDI e o que esperar dos emails mensais, citação motivacional (quote-box), 2 cards resumindo os focos prioritários do ciclo (ação_titulo + ação_detalhe + comp-tag), CTA.

#### Template 2 — Lembrete mensal (meses 1–11)
- **Quando:** Dia 1 de cada mês em que há ação programada.
- **Assunto:** `PDI | Mês [N] de 12 — Suas ações deste mês, [Nome]`
- **Conteúdo:** Saudação, barra de progresso (% do ciclo), 1–2 cards com as ações do mês (month-tag + action-title + action-detail + comp-tag), citação motivacional, CTA.
- **Barra de progresso:** Track cinza com fill azul, label "Mês X de 12" e "Y% do ciclo".

#### Template 3 — Check-in (meses 3, 6, 9)
- **Quando:** Meses de check-in (substitui o lembrete mensal nesses meses).
- **Assunto:** `PDI | Mês [N] — Hora de fazer um balanço, [Nome]`
- **Conteúdo:** Saudação, barra de progresso (fill verde nos check-ins), explicação do check-in, caixa verde com perguntas de reflexão (checkin-box), tracker de marcos com status (done/current/upcoming via dots coloridos), CTA.
- **Perguntas de reflexão:** Extraídas do campo `perguntas_checkin` da tabela de controle. Personalizadas por gestor.
- **Tracker de marcos:** Tabela visual com 3 colunas (número do mês, nome do objetivo, status com dot colorido):
  - `.done` (verde) = marco já passado
  - `.current` (azul) = marco atual
  - `.upcoming` (cinza) = marco futuro

#### Template 4 — Encerramento (mês 12)
- **Quando:** Último mês do ciclo.
- **Assunto:** `PDI | Ciclo completo — Parabéns, [Nome]`
- **Conteúdo:** Saudação, barra de progresso 100% (fill verde), caixa de celebração (celebration-box com frase de impacto), menção ao novo ciclo de avaliação 360°, tracker com todos os marcos como "Concluído" (exceto mês 12 = "Agora"), citação, CTA.

---

## 4. Tabela de Controle (Camada 2)

### Estrutura — 14 colunas

| Coluna | Tipo | Descrição |
|---|---|---|
| `gestor_nome` | Texto | Nome do avaliado |
| `gestor_email` | Email | Destinatário principal (Para:) |
| `gestor_direto_email` | Email | Gestor direto (CC:) |
| `hrbp_email` | Email | HR Business Partner (CC:) |
| `ciclo` | Texto | Ex: "2024-2025" |
| `mes` | Número (0–12) | Mês do ciclo (0 = boas-vindas) |
| `tipo_email` | Texto | `boas-vindas` / `acao` / `checkin` / `encerramento` |
| `acao_titulo` | Texto | Título(s) da(s) ação(ões) do mês (separados por `;`) |
| `acao_detalhe` | Texto | Descrição prática da(s) ação(ões) (separadas por `|`) |
| `competencia_tag` | Texto | Tag(s) de competência (separadas por `;`) |
| `perguntas_checkin` | Texto | Perguntas de reflexão para check-ins (separadas por `|`). Vazio nos meses de ação. |
| `data_programada` | Data | Data programada para envio (dia 1 do mês correspondente) |
| `data_envio` | Data | Preenchido pelo Power Automate após envio |
| `status` | Texto | `pendente` / `enviado` |

### Regras de preenchimento
- **13 linhas por gestor** (mês 0 a 12).
- Meses sem ação específica no PDI recebem `tipo_email = acao` com `acao_titulo = "Manter rotina de [práticas do PDI]"`.
- Meses de check-in (3, 6, 9) recebem `tipo_email = checkin` e as ações do mês + perguntas de reflexão.
- O campo `perguntas_checkin` é personalizado por gestor com base nos focos do PDI.
- Highlight visual nas linhas de check-in (fundo azul claro) e status pendente (fundo amarelo claro) / enviado (fundo verde claro).

### Formato de entrega
- `.xlsx` (Excel) como template para upload em SharePoint List.
- Freezar primeira linha (headers). Auto-filtro ativo. Colunas com largura otimizada.

---

## 5. Power Automate Flow (Camada 3)

### Trigger
**Recurrence:** Dia 1 de cada mês, 08:00 (fuso horário local).

### Passos do fluxo

| # | Ação | Detalhe |
|---|---|---|
| 1 | **Get items** | SharePoint List → filtrar `data_programada = mês atual` AND `status = 'pendente'` |
| 2 | **Apply to each** | Iterar sobre cada registro encontrado |
| 3 | **Condition / Switch** | Avaliar campo `tipo_email` → selecionar bloco HTML correspondente |
| 4 | **Compose** | Renderizar o template HTML substituindo variáveis: `{{gestor_nome}}`, `{{mes}}`, `{{acao_titulo}}`, `{{acao_detalhe}}`, `{{competencia_tag}}`, `{{perguntas_checkin}}` |
| 5 | **Send an email (V2)** | Para: `gestor_email`, CC: `gestor_direto_email; hrbp_email`, Assunto: dinâmico por tipo, Corpo: HTML renderizado, Importância: Normal |
| 6 | **Update item** | `status = 'enviado'`, `data_envio = utcNow()` |

### Assuntos por tipo

| Tipo | Assunto |
|---|---|
| `boas-vindas` | `PDI {{ciclo}} \| Seu plano de desenvolvimento está pronto, {{gestor_nome}}` |
| `acao` | `PDI \| Mês {{mes}} de 12 — Suas ações deste mês, {{gestor_nome}}` |
| `checkin` | `PDI \| Mês {{mes}} — Hora de fazer um balanço, {{gestor_nome}}` |
| `encerramento` | `PDI \| Ciclo completo — Parabéns, {{gestor_nome}}` |

### Variáveis dinâmicas no HTML
As variáveis são substituídas via expressão do Power Automate no passo Compose:
- `{{gestor_nome}}` → `items('Apply_to_each')?['gestor_nome']`
- `{{mes}}` → `items('Apply_to_each')?['mes']`
- `{{acao_titulo}}` → split por `;` e renderizar 1 card por ação
- `{{acao_detalhe}}` → split por `|` e associar ao card correspondente
- `{{competencia_tag}}` → split por `;` e renderizar pill colorida por tag
- `{{perguntas_checkin}}` → split por `|` e renderizar lista no checkin-box
- `{{progresso_pct}}` → `int(items('Apply_to_each')?['mes']) * 100 / 12` (arredondado)

---

## 6. Regras de Padronização

1. **Todos os gestores** recebem exatamente os mesmos templates, com conteúdo variável.
2. Os emails de check-in (meses 3, 6, 9) **substituem** o lembrete mensal — não se acumulam.
3. **Nenhum email** contém nota numérica, score ou dado estatístico.
4. **Nenhum avaliador** é identificável nos emails.
5. O tom é **motivacional de coaching** — apoio, não cobrança.
6. O CTA sempre aponta para o PDI do avaliado na intranet.
7. A barra de progresso é calculada automaticamente: `(mês / 12) * 100%`.

---

## 7. Checklist de Validação

### Templates de email
- [ ] 4 templates presentes (boas-vindas, ação, check-in, encerramento)?
- [ ] Header com barra azul escuro + título + indicador de mês/ciclo?
- [ ] Barra de progresso nos templates 2, 3 e 4?
- [ ] Cards de ação com month-tag + título + detalhe + comp-tag?
- [ ] Caixa de perguntas (verde) no template de check-in?
- [ ] Tracker de marcos com dots de status no template de check-in e encerramento?
- [ ] Caixa de celebração no template de encerramento?
- [ ] CTA "Acessar meu PDI na intranet" em todos os templates?
- [ ] Footer com texto explicativo em todos?
- [ ] Tom motivacional, sem jargão, sem notas numéricas?
- [ ] HTML responsivo (testável em 320px–600px)?

### Tabela de controle
- [ ] 14 colunas conforme spec?
- [ ] 13 linhas por gestor (mês 0–12)?
- [ ] Tipos corretos: boas-vindas (mês 0), acao (meses regulares), checkin (3/6/9), encerramento (12)?
- [ ] Perguntas de checkin preenchidas apenas nos meses 3, 6, 9?
- [ ] Datas programadas corretas (dia 1 de cada mês)?
- [ ] Status inicial = "pendente" para todos?
- [ ] Highlight visual nas linhas de check-in?

### Power Automate flow
- [ ] Trigger: Recurrence mensal, dia 1, 08:00?
- [ ] Filtro: data_programada = mês atual AND status = pendente?
- [ ] Switch por tipo_email com 4 branches?
- [ ] Variáveis substituídas corretamente no Compose?
- [ ] Destinatários: Para = avaliado, CC = gestor + HRBP?
- [ ] Update item: status = enviado + data_envio = now?
- [ ] Assuntos dinâmicos por tipo?

---

**END_PROTOCOL**
