Analise o arquivo CSV compartilhado que contém avaliações do programa 5S e produza um relatório HTML abrangente. Siga estas etapas específicas:

1. Leitura e Processamento:
    1. Utilize UTF-8 para lidar com caracteres especiais
2. Para COMPLEXO BARRACÃO:
    1. Converta as notas da escala original (0-4 nos prefixos das respostas) para escala 1-5
    2. Depois converta para escala 1-10 usando: nota_10 = ((nota_5 - 1) * (10-1))/(5-1) + 1
3. Para COMPLEXO OFICINA:
    1. Converta as notas da escala original (0-4 nos prefixos das respostas) para escala 1-5
    2. Depois converta para escala 1-10 usando: nota_10 = ((nota_5 - 1) * (10-1))/(5-1) + 1
4. Análises Requeridas:
    1. Média geral por área (Barracão em base 10, Oficina em base 10)
    2. Médias por categoria (Utilização, Organização, Limpeza) mantendo as respectivas bases
    3. Evolução temporal (comparativo semana a semana ) respeitando as bases.
    4. Pontos críticos (5 menores notas) e pontos fortes (5 maiores notas) em suas respectivas bases
    5. URLs das fotos disponíveis por área e categoria
5. Relatório HTML:
    1. Use CSS interno (sem dependências externas)
    2. Estruture em seções: Visão Geral, Evolução Temporal, Pontos Críticos, Galeria de Fotos, Recomendações
    3. Inclua cards métricos, tabelas comparativas e links para fotos
    4. Use cores para indicar variações (vermelho para quedas, verde para melhorias)
    5. IMPORTANTE: Indique claramente as bases diferentes (/10.0 para Barracão e /10.0 para Oficina)
    6. IMPORTANTE: Divida o relatorio em partes administráveis. Lembre-se que você tem limites de tokens que precisam ser respeitados.
6. Agrupamento das Questões:
    1. Seiri (Utilização): questões 9, 10, 11, 12
    2. Seiton (Organização): questões 15, 16, 17, 18, 19
    3. Seiso (Limpeza): questões 3, 4, 5, 6, 7
7. Layout do Relatório:
    1. Cabeçalho com título e período
    2. Cards para médias gerais (indicando as bases diferentes)
    3. Tabelas comparativas (com notas em suas respectivas bases)
    4. Gráficos de evolução (indicando escalas diferentes para cada área)
    5. Seção de pontos críticos e fortes (mantendo bases distintas)
    6. Galeria de fotos com links
    7. Recomendações finais
8. Observações de Visualização:
    1. Adicione notas explicativas sobre as bases utilizadas
    2. Em comparações diretas, indique claramente a base de cada métrica
    3. Use elementos visuais (cores, ícones ou labels) para diferenciar as bases
    4. Mantenha a clareza na apresentação das métricas
9. Forneça o código HTML completo, incluindo os estilos CSS internos necessários para reproduzir o relatório sem dependências externas. Precisamos que o seu relatorio tenha exatamente a mesma estrutura de apresentação que o codigo HTML compartilhado