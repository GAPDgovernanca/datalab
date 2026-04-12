# IMFA-SUMM — Síntese Executiva (Versão Técnica)

**Versão:** 2.0  
**Idioma:** PT-BR  
**Propósito:** Gerar uma versão condensada da análise IMFA-TECH, orientada para consumo rápido pela liderança sênior.  
**Escopo:** Cargos de gestão e liderança  
**Audiência do output:** RH, diretoria, C-suite  
**Dependência:** Requer que IMFA-TECH já tenha sido executado.

---

## 1. Framework de Competências

Utiliza o framework definido em `CORE-COMP-REF.md` com as 6 competências (PD-01 a RO-06). Todos os descritores e índices seguem aquele referencial.

---

## 2. Dados de entrada

Os dados devem estar dentro de `<results></results>` e conter, por competência:
- `competency_id` — identificador da competência
- `self_assessment` — nota do avaliado (escala 1–5)
- `received_ratings` — array de notas dos avaliadores (pares, subordinados, superiores)

---

## 3. Análise Quantitativa

Usar os mesmos limiares calibrados do IMFA-TECH (ver seção 4.2 do IMFA-TECH para a tabela completa com zonas de incerteza):

| Condição | Classificação |
|---|---|
| Média ≥ 4.5 **e** σ ≤ 1.2 | **Força** (alta confiança) |
| Média entre 4.30–4.49 **e** σ ≤ 1.0 **e** n ≥ 5 | **Força** (confiança moderada) |
| Média ≤ 3.29 | **Oportunidade de desenvolvimento** (alta confiança) |
| Média entre 3.30–3.50 **e** σ ≤ 1.0 **e** n ≥ 5 | **Oportunidade de desenvolvimento** (confiança moderada) |
| Delta ≥ 1.0 | **Discrepância auto vs. avaliadores** |
| σ ≥ 1.2 | **Alta dispersão** |
| n < 3 avaliadores | **Resultado preliminar** — sinalizar baixa confiança |

Classificações nos limites (zonas de transição 4.30–4.49 e 3.30–3.50) dependem de σ e tamanho amostral. Consultar IMFA-TECH seção 4.2 para regras completas.

---

## 4. Análise Qualitativa (se houver dados)

Se dados qualitativos estiverem presentes:
1. Identifique os 3–4 temas mais recorrentes nos comentários
2. Analise o sentimento predominante de cada tema
3. Cruze os temas qualitativos com os achados quantitativos — sinalize convergências e divergências

---

## 5. Output

### Por competência

| Campo | Conteúdo |
|---|---|
| Métricas | Média e desvio padrão |
| Evidências | Extraídas dos dados quantitativos e qualitativos |
| Gap analysis | |autoavaliação − média dos avaliadores| com direção |
| Recomendações | Formato SMART |

### Resumo executivo consolidado

1. **Score de efetividade (IMFA):** Média ponderada geral
2. **Priorização:** Ordenar achados por delta (maior primeiro) e variância
3. **Forças:** Competências ≥ 4.5 com σ ≤ 1.2
4. **Oportunidades:** Competências ≤ 3.5, ordenadas por urgência

---

## 6. Diretrizes de output

- **Formato:** Conciso, objetivo, específico — sem preâmbulos
- **Idioma:** PT-BR (padrão) ou EN-US conforme contexto
- **Audiência:** Técnica, nível executivo (C-suite)
- **Encerramento:** Perguntar "Próxima avaliação?" ao finalizar