# Manual do Usuário - Mosaico IMS_PV

## Visão Geral

O Mosaico IMS_PV é uma ferramenta de visualização para monitoramento do índice de Ingestão de Matéria Seca por Peso Vivo (IMS_PV) em confinamentos de gado. Este dashboard permite identificar rapidamente a situação nutricional dos animais através de um mosaico colorido.

## Como Usar

### Tela Principal

1. **Mosaico Colorido**: Cada quadrado colorido representa um curral, com o código do curral e seu valor de IMS_PV (%).
   - As cores indicam diferentes níveis de IMS_PV em relação à média:
     - **Azul**: Muito Alto
     - **Verde**: Alto
     - **Amarelo**: Acima da média
     - **Laranja**: Abaixo da média
     - **Vermelho**: Alerta
     - **Cinza escuro**: Crítico

2. **Legenda**: Na parte inferior do mosaico, encontra-se a legenda explicando o significado de cada cor e seus respectivos intervalos de valores.

### Detalhes do Curral

Para visualizar informações detalhadas de um curral:

1. **Clique em qualquer quadrado** do mosaico para exibir os detalhes daquele curral.

2. **Painel de Informações**: Mostra dados importantes como:
   - Consumo de Matéria Seca (kg/dia)
   - Dias de confinamento
   - Tipo de ração
   - Dias na ração atual

3. **Gráfico de Peso**: Compara visualmente o peso de entrada (verde) e o peso atual (azul) dos animais.

4. **Indicadores de Desempenho**: Apresenta métricas importantes:
   - Ganho de peso total (kg)
   - Variação percentual (%)
   - Ganho diário de peso (kg/dia)

## Dicas de Uso

- **Priorize currais em alerta**: Currais em vermelho ou cinza escuro podem precisar de atenção imediata.
- **Compare a evolução**: Monitore regularmente os currais para avaliar o progresso ao longo do tempo.
- **Analise por fase**: Animais em diferentes fases (adaptação, crescimento, terminação) devem ter padrões diferentes de IMS_PV.

## Compatibilidade

O dashboard funciona em desktops, tablets e smartphones, com interface otimizada para cada dispositivo.

## Execução
> npm start