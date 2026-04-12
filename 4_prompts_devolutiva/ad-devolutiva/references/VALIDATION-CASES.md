# VALIDATION-CASES — Casos de Teste para Calibração

**Versão:** 1.0  
**Propósito:** Avaliados fictícios com dados completos e output esperado. Usar para verificar se o pipeline produz resultados consistentes entre execuções.  
**Uso:** Após cada execução do pipeline, compare o output gerado contra o esperado abaixo.

---

## Caso 1 — Perfil "Forte técnico, fraco em pessoas"

### Dados do avaliado
- **Nome:** Carlos Mendes (fictício)
- **Cargo:** Gerente de Operações
- **Ciclo:** 2025
- **Avaliadores:** 4 liderados, 3 pares, 1 diretor (n=8) + autoavaliação

### Input quantitativo (notas dos avaliadores — excluindo auto)

| Competência | Auto | Av.1 | Av.2 | Av.3 | Av.4 | Av.5 | Av.6 | Av.7 | Av.8 |
|---|---|---|---|---|---|---|---|---|---|
| Desenv. Pessoas (PD-01) | 4.0 | 2.5 | 3.0 | 2.5 | 3.0 | 2.0 | 3.0 | 2.5 | 2.5 |
| Trabalho em Equipe (TW-02) | 4.0 | 3.5 | 4.0 | 3.5 | 3.0 | 4.0 | 3.5 | 3.5 | 3.0 |
| Planej. e Organização (PO-03) | 4.5 | 4.0 | 4.5 | 4.0 | 4.5 | 4.0 | 4.5 | 4.0 | 4.5 |
| Orient. Resultados (RO-04) | 5.0 | 4.5 | 5.0 | 4.5 | 4.5 | 5.0 | 4.5 | 5.0 | 4.5 |
| Conhec. Técnico (TK-05) | 5.0 | 5.0 | 4.5 | 5.0 | 4.5 | 5.0 | 4.5 | 5.0 | 5.0 |
| Otimiz. Recursos (RO-06) | 4.0 | 4.0 | 4.5 | 4.0 | 3.5 | 4.0 | 4.5 | 4.0 | 4.0 |

### Output esperado

| Competência | Média avaliadores | σ | Auto | Delta | Classificação |
|---|---|---|---|---|---|
| TK-05 | 4.81 | 0.26 | 5.0 | 0.19 | 🟢 Força (alta confiança) |
| RO-04 | 4.69 | 0.26 | 5.0 | 0.31 | 🟢 Força (alta confiança) |
| PO-03 | 4.25 | 0.27 | 4.5 | 0.25 | 🟡 Dentro do esperado |
| RO-06 | 4.06 | 0.32 | 4.0 | 0.06 | 🟡 Dentro do esperado |
| TW-02 | 3.50 | 0.38 | 4.0 | 0.50 | 🟡 Dentro do esperado |
| PD-01 | 2.63 | 0.32 | 4.0 | 1.38 | 🔴 Oportunidade (alta confiança) |

### Verificações obrigatórias

- [ ] PD-01 classificado como Oportunidade (média 2.63 ≤ 3.29)?
- [ ] PD-01 com discrepância significativa (delta 1.38 ≥ 1.0)?
- [ ] TK-05 e RO-04 classificados como Força (médias ≥ 4.5, σ ≤ 1.2)?
- [ ] PO-03 classificado como Dentro do esperado (média 4.25, na zona de transição mas σ ≤ 1.0 e n=8 → poderia ser Força moderada)?
- [ ] Padrão de gap = **superestimação** em PD-01 (auto=4.0 >> pares=2.63)?
- [ ] Seção 4 (destaques positivos) menciona Conhecimento Técnico e/ou Orientação para Resultados?
- [ ] Seção 5 (onde crescer) menciona Desenvolvimento de Pessoas como foco principal?
- [ ] Seção 6 (autopercepção) identifica superestimação em PD-01?
- [ ] PDI prioriza PD-01 como foco #1, com ações de feedback e escuta?

---

## Caso 2 — Perfil "Subestimador alinhado"

### Dados do avaliado
- **Nome:** Ana Ferreira (fictício)
- **Cargo:** Gerente Administrativa
- **Ciclo:** 2025
- **Avaliadores:** 3 liderados, 2 pares, 1 diretor (n=6) + autoavaliação

### Input quantitativo

| Competência | Auto | Av.1 | Av.2 | Av.3 | Av.4 | Av.5 | Av.6 |
|---|---|---|---|---|---|---|---|
| Desenv. Pessoas (PD-01) | 3.5 | 4.5 | 4.0 | 4.5 | 4.0 | 4.5 | 4.0 |
| Trabalho em Equipe (TW-02) | 3.0 | 4.5 | 4.5 | 5.0 | 4.5 | 4.5 | 5.0 |
| Planej. e Organização (PO-03) | 3.0 | 4.0 | 4.5 | 4.0 | 4.0 | 4.5 | 4.0 |
| Orient. Resultados (RO-04) | 3.5 | 3.5 | 3.0 | 3.5 | 3.0 | 3.5 | 3.0 |
| Conhec. Técnico (TK-05) | 3.0 | 3.5 | 3.0 | 3.5 | 3.0 | 3.5 | 3.0 |
| Otimiz. Recursos (RO-06) | 3.0 | 3.0 | 3.5 | 2.5 | 3.0 | 3.5 | 3.0 |

### Output esperado

| Competência | Média avaliadores | σ | Auto | Delta | Classificação |
|---|---|---|---|---|---|
| TW-02 | 4.67 | 0.26 | 3.0 | 1.67 | 🟢 Força (alta confiança) |
| PD-01 | 4.25 | 0.27 | 3.5 | 0.75 | 🟡 Dentro do esperado |
| PO-03 | 4.17 | 0.26 | 3.0 | 1.17 | 🟡 Dentro do esperado |
| RO-04 | 3.25 | 0.27 | 3.5 | 0.25 | 🔴 Oportunidade (alta confiança) |
| TK-05 | 3.25 | 0.27 | 3.0 | 0.25 | 🔴 Oportunidade (alta confiança) |
| RO-06 | 3.08 | 0.31 | 3.0 | 0.08 | 🔴 Oportunidade (alta confiança) |

### Verificações obrigatórias

- [ ] TW-02 classificado como Força (média 4.67 ≥ 4.5, σ ≤ 1.2)?
- [ ] TW-02 com discrepância significativa (delta 1.67 ≥ 1.0)? Direção = **subestimação**
- [ ] PO-03 com discrepância significativa (delta 1.17 ≥ 1.0)? Direção = **subestimação**
- [ ] RO-04, TK-05 e RO-06 classificados como Oportunidade (médias ≤ 3.29)?
- [ ] Padrão de gap = **subestimação generalizada** (auto < pares em 5 de 6 competências)?
- [ ] Seção 4 (destaques) menciona Trabalho em Equipe como ponto reconhecido?
- [ ] Seção 5 (onde crescer) menciona Otimização de Recursos e/ou Orientação para Resultados?
- [ ] Seção 6 (autopercepção) identifica subestimação — "As pessoas reconhecem mais essas competências do que você"?
- [ ] PDI usa as forças (TW-02) como alavanca para desenvolver as oportunidades?

---

## Caso 3 — Perfil "Amostra pequena" (teste de confiança)

### Dados do avaliado
- **Nome:** Roberto Lima (fictício)
- **Cargo:** Coordenador de Projetos
- **Ciclo:** 2025
- **Avaliadores:** 1 liderado, 1 par (n=2) + autoavaliação

### Input quantitativo

| Competência | Auto | Av.1 | Av.2 |
|---|---|---|---|
| Desenv. Pessoas (PD-01) | 4.0 | 4.5 | 4.5 |
| Trabalho em Equipe (TW-02) | 4.0 | 4.0 | 3.5 |
| Planej. e Organização (PO-03) | 4.0 | 3.0 | 3.5 |
| Orient. Resultados (RO-04) | 4.5 | 4.5 | 5.0 |
| Conhec. Técnico (TK-05) | 4.0 | 4.0 | 4.0 |
| Otimiz. Recursos (RO-06) | 3.5 | 3.0 | 3.0 |

### Output esperado

| Competência | Média avaliadores | σ | Auto | Delta | Classificação |
|---|---|---|---|---|---|
| RO-04 | 4.75 | 0.35 | 4.5 | 0.25 | ⚠️ Resultado preliminar (n < 3) |
| PD-01 | 4.50 | 0.00 | 4.0 | 0.50 | ⚠️ Resultado preliminar (n < 3) |
| TK-05 | 4.00 | 0.00 | 4.0 | 0.00 | ⚠️ Resultado preliminar (n < 3) |
| TW-02 | 3.75 | 0.35 | 4.0 | 0.25 | ⚠️ Resultado preliminar (n < 3) |
| PO-03 | 3.25 | 0.35 | 4.0 | 0.75 | ⚠️ Resultado preliminar (n < 3) |
| RO-06 | 3.00 | 0.00 | 3.5 | 0.50 | ⚠️ Resultado preliminar (n < 3) |

### Verificações obrigatórias

- [ ] **Todas** as competências classificadas como "Resultado preliminar" (n=2 < 3)?
- [ ] Nenhuma competência classificada como Força ou Oportunidade com confiança?
- [ ] Documento do avaliado inclui aviso ⚠️ "Resultado preliminar — número reduzido de participantes"?
- [ ] Análise prossegue normalmente (produz síntese e PDI), mas sinaliza a limitação?
- [ ] PDI inclui nota de que as ações são baseadas em amostra limitada e devem ser recalibradas no próximo ciclo?
