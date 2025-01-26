**Instruções para Processamento dos Dados da Planilha**

Você receberá uma planilha contendo um questionário com respostas de vários participantes. Sua tarefa é processar esses dados seguindo os passos abaixo:

1. **Extração das Notas:**

   - **Identifique as perguntas e as respostas correspondentes na planilha.**
   - **Para cada resposta, extraia a nota que está no prefixo.**
     - As notas estão no início de cada resposta, no formato "**n**: descrição", onde "**n**" é a nota na escala original de 0 a 4.
     - **Exemplo:** "3: Maioria dos equipamentos necessários disponíveis" significa que a nota é 3.
   - **Anote essas notas para uso posterior.**

2. **Construção da Tabela Inicial:**

   - **Crie uma tabela em formato markdown** para organizar as notas extraídas.
   - **As colunas devem representar os participantes, incluindo o nome e o complexo avaliado (Barracão ou Oficina).**
     - **Exemplo de cabeçalho de coluna:** "Júlio Cezar (Barracão)"
   - **As linhas devem representar as perguntas do questionário.**
   - **Insira as notas extraídas nas células correspondentes, mantendo a organização por pergunta e por participante.**

3. **Conversão das Notas para Escalas Superiores:**

   - **Converta as notas da escala original de 0-4 para uma escala de 1-5.**
     - **Método:** Adicione 1 a cada nota original.
     - **Fórmula:** `nota_5 = nota_original + 1`
   - **Converta as notas da escala de 1-5 para uma escala de 1-10 usando a seguinte fórmula:**
     - **Fórmula:** `nota_10 = ((nota_5 - 1) * (10 - 1)) / (5 - 1) + 1`
     - **Simplificando:** `nota_10 = ((nota_5 - 1) * 9) / 4 + 1`
   - **Aplique essa conversão para cada nota individualmente.**
     - **Exemplo de cálculo:**
       - Nota original: 3
       - Conversão para escala 1-5: `nota_5 = 3 + 1 = 4`
       - Conversão para escala 1-10:
         - `nota_10 = ((4 - 1) * 9) / 4 + 1`
         - `nota_10 = (3 * 9) / 4 + 1`
         - `nota_10 = 6,75 + 1 = 7,75`

4. **Atualização da Tabela com Notas Convertidas:**

   - **Atualize a tabela inicial substituindo as notas originais pelas notas convertidas para a escala de 1-10.**
   - **Mantenha o formato da tabela em markdown e certifique-se de que todas as notas estejam corretamente posicionadas.**

5. **Cálculo das Médias por Pergunta e por Complexo:**

   - **Para cada pergunta, calcule a média das notas dos participantes que avaliaram o mesmo complexo.**
     - **Separe os cálculos para os complexos Barracão e Oficina.**
     - **Método:**
       - **Some todas as notas dos participantes do mesmo complexo para a pergunta específica.**
       - **Divida essa soma pelo número de participantes que avaliaram esse complexo.**
     - **Exemplo de cálculo:**
       - Notas dos participantes do Barracão para a Pergunta 1: 7,75; 7,75; 7,75; 7,75
       - Soma: 7,75 + 7,75 + 7,75 + 7,75 = 31,00
       - Número de participantes: 4
       - Média: 31,00 / 4 = 7,75
   - **Registre essas médias em uma nova tabela, com colunas para "Média Barracão" e "Média Oficina".**

6. **Cálculo das Médias Gerais por Complexo:**

   - **Calcule a média geral de cada complexo considerando todas as perguntas e todos os participantes que avaliaram esse complexo.**
     - **Método:**
       - **Some todas as notas dos participantes do complexo em questão (somando todas as perguntas).**
       - **Divida essa soma pelo número total de respostas (número de participantes multiplicado pelo número de perguntas).**
     - **Exemplo de cálculo:**
       - Soma total das notas do Barracão: 132,50
       - Número total de respostas: 4 participantes × 5 perguntas = 20
       - Média geral: 132,50 / 20 = 6,625
   - **Apresente as médias gerais de forma clara, preferencialmente em uma tabela ou lista.**

7. **Detalhamento dos Cálculos:**

   - **Forneça detalhes dos cálculos realizados, incluindo:**
     - **Notas individuais utilizadas em cada média.**
     - **Somas intermediárias.**
     - **Número de participantes considerados em cada cálculo.**
   - **Isso garantirá transparência e verificabilidade dos resultados.**

8. **Interpretação dos Resultados:**

   - **Inclua uma legenda para interpretar as notas na escala de 1-10:**
     - **1 a 3,25:** Baixo desempenho
     - **3,26 a 6,5:** Desempenho médio
     - **6,51 a 10:** Alto desempenho
   - **Analise os resultados obtidos, destacando pontos fortes e áreas que necessitam de melhoria em cada complexo.**

9. **Apresentação Final:**

   - **Organize todas as tabelas e cálculos de forma clara e lógica.**
   - **Utilize títulos e subtítulos para separar as seções (por exemplo, "Tabela de Notas Convertidas", "Médias por Pergunta", "Médias Gerais por Complexo").**
   - **Certifique-se de que o documento final seja fácil de ler e entender.**

10. **Verificação dos Cálculos:**

    - **Revise todos os cálculos para garantir que não haja erros.**
    - **Verifique se todas as notas foram corretamente extraídas, convertidas e incluídas nos cálculos das médias.**

**Resumo das Fórmulas Utilizadas:**

- **Conversão de notas da escala 0-4 para 1-5:**
  - `nota_5 = nota_original + 1`

- **Conversão de notas da escala 1-5 para 1-10:**
  - `nota_10 = ((nota_5 - 1) * (10 - 1)) / (5 - 1) + 1`
  - Simplificada: `nota_10 = ((nota_5 - 1) * 9) / 4 + 1`

- **Cálculo da média por pergunta e por complexo:**
  - `média_pergunta_complexo = soma_das_notas / número_de_participantes`

- **Cálculo da média geral por complexo:**
  - `média_geral_complexo = soma_total_das_notas / número_total_de_respostas`

**Notas Importantes:**

- **Mantenha consistência nas casas decimais ao apresentar as notas e médias.** Utilize duas casas decimais para maior precisão, caso necessário.
- **Ao lidar com números decimais, certifique-se de usar a vírgula como separador decimal, conforme a convenção em português.** Por exemplo, use "7,75" em vez de "7.75".
- **Se houver participantes que avaliaram mais de um complexo, certifique-se de separar corretamente suas respostas para cada complexo.**