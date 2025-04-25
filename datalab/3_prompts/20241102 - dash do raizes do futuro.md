### CONTEXTO
Você terá acesso a três arquivos CSV contendo avaliações de um programa corporativo de mentoria:
1. mentorados.csv - Avaliação dos mentorados pelos mentores
2. mentor.csv - Avaliação dos mentores pelos mentorados
3. mentor senior.csv - Avaliação geral do programa

### OBJETIVO
Realizar uma análise completa e estruturada do programa de mentoria, oferecendo insights quantitativos e qualitativos, além de recomendações práticas para melhoria.

### INSTRUÇÕES DE PROCESSAMENTO

#### 1. Preparação dos Dados
1. Carregue os três arquivos CSV utilizando a biblioteca Papa Parse
2. Configure o parsing com as seguintes opções:
   - header: true
   - skipEmptyLines: true
   - dynamicTyping: true
3. Utilize o encoding UTF-8 para garantir a correta leitura de caracteres especiais
4. Trate campos vazios como "Não Respondeu" para preservar a consistência da análise

#### 2. Análise Quantitativa
Execute as seguintes análises usando lodash para agregação:

a) Para mentorados.csv:
- Contagem de progresso por categoria
- Análise de iniciativa e engajamento
- Padrões de receptividade ao aprendizado

b) Para mentor.csv:
- Níveis de satisfação geral
- Clareza nas orientações
- Disponibilidade e acessibilidade
- Qualidade do feedback

c) Para mentor senior.csv:
- Satisfação com aspectos organizacionais
- Percepção de mudanças positivas
- Efetividade dos encontros

#### 3. Análise Qualitativa
1. Extraia e categorize comentários subjetivos em:
   - Pontos fortes
   - Áreas de melhoria
   - Sugestões construtivas

2. Identifique padrões em respostas abertas sobre:
   - Comunicação
   - Desenvolvimento
   - Engajamento
   - Metodologia

### ESTRUTURA DE APRESENTAÇÃO

#### 1. Dashboard Visual (React Component)
Crie um componente React com:

a) Estrutura base:
```javascript
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { BarChart, PieChart, /* outros componentes */ } from 'recharts';
```

b) Seções obrigatórias:
1. Visão Geral do Programa
   - Total de perguntas por avaliação (7, 10, 10)
   - Foco de cada questionário
   - Métricas principais

2. Visualizações de Dados
   - Gráfico de pizza para progresso dos mentorados
   - Gráfico de barras para satisfação com reuniões
   - Indicadores de satisfação geral

3. Análise Detalhada
   - Desenvolvimento dos mentorados
   - Efetividade da mentoria
   - Impactos observados

4. Depoimentos e Percepções
   - Excertos corrigidos de feedback
   - Categorizados por perspectiva

5. Plano de Ação
   - Recomendações imediatas (30 dias)
   - Ações de médio prazo (90 dias)
   - Objetivos de longo prazo (180 dias)

#### 2. Formatação Visual
- Use cores consistentes:
  - Azul (#0088FE) para mentorados
  - Verde (#00C49F) para mentores
  - Amarelo (#FFBB28) para programa
- Mantenha espaçamento uniforme (gap-4, gap-6)
- Use Tailwind apenas com classes predefinidas

### RECOMENDAÇÕES DE ANÁLISE

1. Foque em números absolutos em vez de percentuais
   - "3 em 6 mentorados" em vez de "50%"
   - Use proporções claras e compreensíveis

2. Estruture recomendações em três níveis:
   - Ações imediatas
   - Melhorias estruturais
   - Desenvolvimento contínuo

3. Apresente métricas de sucesso:
   - Quantitativas (frequência, cumprimento de metas)
   - Qualitativas (evolução, impacto)

4. Ao corrigir depoimentos:
   - Mantenha o significado original
   - Ajuste apenas gramática e clareza
   - Preserve o tom pessoal

### OUTPUTS ESPERADOS

1. Dashboard interativo mostrando:
   - Distribuição de respostas
   - Tendências principais
   - Áreas de melhoria

2. Análise detalhada com:
   - Insights quantitativos
   - Feedback qualitativo
   - Recomendações práticas

3. Plano de ação estruturado:
   - Objetivos claros
   - Prazos definidos
   - Métricas de acompanhamento

### CONSIDERAÇÕES IMPORTANTES

1. Mantenha o foco no desenvolvimento:
   - Individual (mentorados)
   - Profissional (mentores)
   - Organizacional (programa)

2. Priorize recomendações:
   - Acionáveis
   - Mensuráveis
   - Relevantes ao contexto

3. Preserve a confidencialidade:
   - Não identifique indivíduos
   - Use agregações apropriadas
   - Mantenha o profissionalismo