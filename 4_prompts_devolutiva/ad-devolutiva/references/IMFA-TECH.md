# IMFA-TECH — Análise Técnica de Avaliação 360°

**Versão:** 2.0  
**Idioma:** PT-BR  
**Propósito:** Pipeline analítico principal. Processa dados quantitativos e qualitativos, produz métricas por competência, identifica forças, oportunidades e discrepâncias.  
**Escopo:** Cargos de gestão e liderança  
**Audiência do output:** Técnica (RH, diretoria, C-suite)

---

## 1. Framework de Competências

Este módulo utiliza o framework definido em `CORE-COMP-REF.md`:

| ID | Competência |
|---|---|
| PD-01 | Desenvolvimento de Pessoas |
| TW-02 | Trabalho em Equipe |
| PO-03 | Planejamento e Organização |
| RO-04 | Orientação para Resultados |
| TK-05 | Conhecimento Técnico |
| RO-06 | Otimização de Recursos |

Verifique que cada item do dataset esteja alinhado ao framework antes de prosseguir.

---

## 2. Pré-processamento dos Dados

Antes de qualquer cálculo, normalize o formato dos dados.

### 2.1 Mapeamento texto → número (LABEL_MAP)

| Rótulo textual | Nota |
|---|---|
| Nunca acontece | 1 |
| Quase nunca acontece | 2 |
| Ocorre de vez em quando | 3 |
| Acontece com frequência | 4 |
| Acontece o tempo todo | 5 |

### 2.2 Detecção de formato

- Escaneie as colunas quantitativas.
- Se qualquer célula contiver um dos rótulos do LABEL_MAP, trate o dataset como formato textual e aplique a conversão.
- Se os valores já forem numéricos (1–5), use diretamente.
- Se o formato não for reconhecido, sinalize erro.

### 2.3 Conversão célula a célula

Para cada célula nas colunas quantitativas:
1. Se é numérica (int/float) → usar diretamente
2. Se é texto presente no LABEL_MAP → converter para o número correspondente
3. Se é vazia/NaN → excluir do cálculo (exclusão pairwise, sem imputação)
4. Se é outro valor → sinalizar como erro

### 2.4 Detecção de colunas qualitativas

Verifique o **nome do header** de cada coluna para identificar se é "Coisas para manter" ou "Coisas para melhorar". Nunca assuma pela posição da coluna — a ordem pode variar entre ciclos.

### 2.5 Mapeamento de perguntas por conteúdo (QUESTION_MAP)

A ordem das perguntas dentro de cada bloco de competência pode variar entre ciclos. O mapeamento é feito por **conteúdo do header**, nunca por posição.

Para cada coluna quantitativa:
1. Extraia o texto do header
2. Compare (case-insensitive, regex parcial) contra as palavras-chave da tabela abaixo
3. Atribua ao cluster correspondente (competência + descritor)

**Regras:**
- Cada cluster deve conter exatamente 2 itens mapeados
- Se uma coluna não fizer match → sinalizar como "não mapeada" e incluir na média geral da competência sem atribuir a um cluster
- Nunca assuma que a posição do item = identidade do descritor

**Tabela QUESTION_MAP:**

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

### 2.6 Validação pós-conversão

Após normalizar todos os dados:
- Verifique que todos os valores estão no intervalo [1, 5]
- Registre: formato detectado, quantidade de linhas convertidas, nulos excluídos

---

## 3. Estrutura dos dados por competência

Após o pré-processamento, os dados devem estar nesta estrutura para cada competência:

- `competency_id` — identificador da competência (PD-01, TW-02, etc.)
- `self_assessment` — nota do avaliado (escala 1–5, já normalizada)
- `received_ratings` — array de notas recebidas de pares, subordinados e superiores (escala 1–5, já normalizadas)

---

## 4. Análise Quantitativa

**Fonte:** Dados normalizados da etapa de pré-processamento.

### 4.1 Cálculos obrigatórios

Para cada competência e para cada cluster:
1. **Média** das notas dos avaliadores (excluindo autoavaliação)
2. **Desvio padrão** das notas dos avaliadores
3. **Delta (gap):** |autoavaliação − média dos avaliadores|

### 4.2 Classificação

| Condição | Classificação |
|---|---|
| Média ≥ 4.5 **e** σ ≤ 1.2 | **Força** (alta confiança) |
| Média entre 4.30–4.49 **e** σ ≤ 1.0 **e** n ≥ 5 | **Força** (confiança moderada) |
| Média entre 4.30–4.49 **e** (σ > 1.0 **ou** n < 5) | **Dentro do esperado** |
| Média entre 3.51–4.29 | **Dentro do esperado** |
| Média entre 3.30–3.50 **e** σ ≤ 1.0 **e** n ≥ 5 | **Oportunidade de desenvolvimento** (confiança moderada) |
| Média entre 3.30–3.50 **e** (σ > 1.0 **ou** n < 5) | **Dentro do esperado** |
| Média ≤ 3.29 | **Oportunidade de desenvolvimento** (alta confiança) |
| Delta ≥ 1.0 | **Discrepância significativa** (auto vs. avaliadores) |
| σ ≥ 1.2 | **Alta dispersão** |

**Nota sobre confiança amostral:**
- Se o número total de avaliadores (excluindo autoavaliação) for < 3, sinalizar que o resultado é **preliminar** e que a classificação tem baixa confiança.
- A confiança (alta/moderada/preliminar) é um metadado interno: usado para decidir classificações nos limites e disponível no output técnico (IMFA-TECH, IMFA-SUMM), mas **não aparece** na versão para avaliado (IMFA-SUMM-AVALIADO), que exibe apenas as 3 faixas (🟢🟡🔴).

### 4.3 Priorização

Ordenar os achados por impacto: **delta alto + variância alta = prioridade máxima**.

---

## 5. Análise Qualitativa

**Condição:** Executar apenas se houver dados qualitativos (comentários "manter" e "melhorar").

### 5.1 O que fazer

1. **Identificar temas recorrentes:** Agrupe os comentários por tema (ex: comunicação, presença no campo, delegação). Nomeie cada tema de forma descritiva.
2. **Analisar o sentimento predominante:** Para cada tema, identifique se o tom geral é positivo, neutro ou negativo.
3. **Cruzar com os dados quantitativos:** Verifique se os temas qualitativos corroboram ou contradizem os achados numéricos. Sinalizar divergências.
4. **Extrair temas prioritários:** Selecione os 3–4 temas mais mencionados ou que mais convergem com os dados quantitativos.

### 5.2 Regras

- Nunca transcreva comentários literalmente
- Nunca identifique a fonte de um comentário
- Se não houver comentários para uma competência, não invente

---

## 6. Output por Competência

Para cada competência, produza:

| Campo | Conteúdo |
|---|---|
| Métricas | Média e desvio padrão dos avaliadores |
| Evidências | Extraídas dos dados quantitativos e qualitativos |
| Gap analysis | Autoavaliação vs. média dos avaliadores, com indicação de direção (super/subestimação) |
| Recomendações | Em formato SMART (Específica, Mensurável, Atingível, Relevante, Com prazo) |

---

## 7. Resumo executivo

Ao final da análise, produza:
1. **Score de efetividade (IMFA):** Média ponderada geral das 6 competências
2. **Ranking de competências:** Da melhor para a pior média
3. **Forças consolidadas:** Competências classificadas como força
4. **Oportunidades priorizadas:** Competências classificadas como oportunidade, ordenadas por urgência (delta + variância)
5. **Padrão de gap:** Superestimação, subestimação ou alinhamento geral

---

## 8. Diretrizes de output

- **Formato:** Conciso, objetivo, específico — sem preâmbulos
- **Idioma:** PT-BR (padrão) ou EN-US conforme contexto
- **Audiência:** Técnica, nível executivo (C-suite)
- **Encerramento:** Perguntar "Próxima avaliação?" ao finalizar

---

## 9. Execução Computacional (OBRIGATÓRIO)

**Regra:** Todos os cálculos quantitativos (médias, desvios padrão, deltas, classificação por faixa, identificação de forças/oportunidades) **devem** ser realizados via execução de código Python. Não calcule mentalmente.

### Fluxo

1. Receba os dados do usuário
2. Gere um script Python (pandas) que:
   - Carrega os dados em um DataFrame
   - Aplica o LABEL_MAP se necessário (seção 2.1)
   - Mapeia colunas a clusters via QUESTION_MAP com regex no header (seção 2.5)
   - Calcula: média por competência, média por cluster, σ, delta (auto − peers), classificação por faixa
   - Exporta um dicionário/JSON com a estrutura de resultados
3. Execute o script via terminal
4. Use o output resultante como base para todas as fases subsequentes (análise qualitativa, sínteses, PDI)

**Nunca** escreva médias, desvios ou classificações sem tê-los obtido da saída do script.

### Template de script Python

Adaptar este template aos dados recebidos:

```python
import pandas as pd
import json
import re

# ── Configuração ──
LABEL_MAP = {
    'Nunca acontece': 1,
    'Quase nunca acontece': 2,
    'Ocorre de vez em quando': 3,
    'Acontece com frequência': 4,
    'Acontece o tempo todo': 5
}

THRESHOLDS = {
    'forca_media': 4.5,
    'forca_sigma_max': 1.2,
    'oportunidade_media': 3.5,
    'discrepancia_delta': 1.0,
    'outlier_sigma': 1.2,
    'forca_moderada_min': 4.3,
    'forca_moderada_sigma_max': 1.0,
    'oportunidade_moderada_max': 3.5,
    'oportunidade_moderada_min': 3.3,
    'n_minimo_confiavel': 5,
    'n_minimo_absoluto': 3
}

# QUESTION_MAP: competencia -> cluster -> [keywords]
QUESTION_MAP = {
    'PD-01': {
        'Clareza de expectativas': ['esclarece as expectativas', 'nível de orientação'],
        'Feedback e reconhecimento': ['feedback positivo', 'valorizados e respeitados'],
        'Ensino e desenvolvimento': ['ensina novos procedimentos', 'instruções e modelos'],
        'Escuta e suporte': ['ouve as preocupações', 'suporte aos esforços'],
        'Resolução de problemas': ['resolução de problemas', 'PDCA'],
    },
    'TW-02': {
        'Confiança e apoio': ['relações de confiança', 'apoiar as decisões'],
        'Resolução de conflitos': ['resolver conflitos', 'dar e.*receber feedback'],
        'Perspectivas dos pares': ['perspectivas', 'humildade e abertura'],
        'Compartilhamento': ['compartilhar experiências', 'celebrar conquistas'],
        'Responsabilidades': ['responsabilidades e papéis', 'coordenar.*metas'],
    },
    'PO-03': {
        'Priorização': ['priorizar.*atividades', 'focando no.*importante'],
        'Planejamento de recursos': ['tarefas e recursos', 'aproveit.*recursos'],
        'Cronogramas e prazos': ['cronogramas', 'prazos realistas'],
        'Coordenação interáreas': ['coordenar.*atividades.*áreas', 'colegas especialistas'],
        'Autonomia e aconselhamento': ['planejar.*organizar.*autonomia', 'aconselhar.*equipe'],
    },
    'RO-04': {
        'Oportunidades de impacto': ['oportunidades.*alto impacto', 'metas ambiciosas'],
        'Metas e energia': ['energia e vigor', 'satisfação ao alcançar'],
        'Proatividade': ['tarefas adicionais', 'focado.*evitar distrações'],
        'Urgência e conclusão': ['urgência e determinação', 'correções de rota'],
        'Priorização e disciplina': ['priorizar.*impacto.*resultado', 'autodisciplina'],
    },
    'TK-05': {
        'Domínio da área': ['conhecimento sobre.*departamento', 'regras.*processos'],
        'Atualização contínua': ['manter-se atualizado', 'desenvolvimento contínuo'],
        'Ferramentas e sistemas': ['ferramentas e sistemas', 'compreender.*aspectos'],
        'Aplicação prática': ['aplicar.*conhecimentos técnicos', 'resolver problemas.*soluções'],
        'Compartilhamento com equipe': ['compartilhar.*conhecimentos.*equipe', 'impactos.*áreas.*outros'],
    },
    'RO-06': {
        'Procedimentos e ferramentas': ['procedimentos e ferramentas', 'melhor aproveitamento'],
        'Redução de custos': ['redução de desperdícios', 'racionalização.*simplificação'],
        'Orientação da equipe': ['orienta.*equipe.*redução', 'instrui.*equipe.*bom uso'],
        'Eliminação de desperdícios': ['eliminar desperdícios.*retrabalhos', 'otimização.*recursos financeiros'],
        'Maximização de resultados': ['maximiza resultados', 'baixo custo.*sem comprometer'],
    },
}


def normalizar_valor(val):
    """Converte célula para numérico usando LABEL_MAP."""
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip()
    if val_str in LABEL_MAP:
        return float(LABEL_MAP[val_str])
    try:
        return float(val_str)
    except ValueError:
        return None


def mapear_coluna(header_text):
    """Mapeia header de coluna a (competencia, cluster) via regex."""
    for comp_id, clusters in QUESTION_MAP.items():
        for cluster_name, keywords in clusters.items():
            for kw in keywords:
                if re.search(kw, header_text, re.IGNORECASE):
                    return comp_id, cluster_name
    return None, None


def classificar(media, sigma, n_avaliadores):
    """Classifica por faixa com zona de incerteza e confiança amostral."""
    T = THRESHOLDS
    if n_avaliadores < T['n_minimo_absoluto']:
        return 'Resultado preliminar (amostra insuficiente)'
    if media >= T['forca_media'] and sigma <= T['forca_sigma_max']:
        return 'Força (alta confiança)'
    if media >= T['forca_moderada_min'] and media < T['forca_media'] and sigma <= T['forca_moderada_sigma_max']:
        if n_avaliadores >= T['n_minimo_confiavel']:
            return 'Força (confiança moderada)'
        else:
            return 'Dentro do esperado'
    if media <= T['oportunidade_moderada_min']:
        return 'Oportunidade de desenvolvimento (alta confiança)'
    if media > T['oportunidade_moderada_min'] and media <= T['oportunidade_media'] and sigma <= T['forca_moderada_sigma_max']:
        if n_avaliadores >= T['n_minimo_confiavel']:
            return 'Oportunidade de desenvolvimento (confiança moderada)'
        else:
            return 'Dentro do esperado'
    return 'Dentro do esperado'


# ── Carregar dados ──
# Substituir pelo carregamento real dos dados do usuário:
# df = pd.read_csv('dados_avaliacao.csv') ou construir DataFrame do input
# ...

# ── Pipeline de análise ──
# 1. Normalizar valores: df[colunas_quant] = df[colunas_quant].applymap(normalizar_valor)
# 2. Mapear colunas: col_map = {col: mapear_coluna(col) for col in colunas_quant}
# 3. Calcular métricas por competência e por cluster
# 4. Classificar cada competência/cluster
# 5. Calcular deltas (auto - peers) e sinalizar discrepâncias
# 6. Exportar resultados como JSON

# ── Output esperado (estrutura do JSON) ──
# {
#   "avaliado": {"nome": "...", "cargo": "...", "ciclo": "..."},
#   "n_avaliadores": N,
#   "competencias": {
#     "PD-01": {
#       "nome": "Desenvolvimento de Pessoas",
#       "media_avaliadores": X.XX,
#       "sigma": X.XX,
#       "autoavaliacao": X.XX,
#       "delta": X.XX,
#       "classificacao": "Força / Dentro do esperado / Oportunidade",
#       "clusters": {
#         "Clareza de expectativas": {"media": X.XX, "sigma": X.XX, "classificacao": "..."},
#         ...
#       }
#     },
#     ...
#   }
# }
```

### Regras de uso

- Adaptar o template aos dados reais recebidos do usuário (formato CSV, tabela colada, etc.)
- O script deve ser executado via terminal antes de produzir qualquer output narrativo
- Se o terminal não estiver disponível, informar o usuário e pedir que execute o script manualmente
- O JSON de saída é a base para IMFA-SUMM, IMFA-SUMM-AVALIADO, IDP-GEN e IDP-GEN-AVALIADO