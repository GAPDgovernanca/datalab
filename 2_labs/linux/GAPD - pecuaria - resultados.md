| Campo                       | Descrição                                                        | Fórmula                                                |
| --------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------ |
| Giro                        | Ciclo de produção dos animais                                    | *Preenchido manualmente*                               |
| Data Abate                  | Data em que os animais foram abatidos                            | *Preenchido manualmente*                               |
| Tipo                        | Raça ou classificação genética dos animais                       | *Preenchido manualmente*                               |
| Sexo                        | Gênero dos animais                                               | *Preenchido manualmente*                               |
| QTD                         | Quantidade de animais em cada lote                               | *Preenchido manualmente*                               |
| Dias                        | Período de permanência dos animais no confinamento               | *Preenchido manualmente*                               |
| PV entrada                  | Peso vivo médio dos animais na entrada do confinamento (kg)      | *Preenchido manualmente*                               |
| PV entrada (@)              | Peso vivo na entrada convertido em arrobas                       | `PV entrada / 30`                                      |
| PV saída                    | Peso vivo médio dos animais na saída do confinamento (kg)        | *Preenchido manualmente*                               |
| GPD Vivo                    | Ganho de peso diário vivo (kg/dia)                               | `(PV saída - PV entrada) / Dias`                       |
| Carcaça                     | Peso da carcaça após o abate (kg)                                | *Preenchido manualmente*                               |
| PM em @                     | Peso médio em arrobas da carcaça                                 | `Carcaça / 15`                                         |
| REND.                       | Rendimento de carcaça                                            | `Carcaça / PV saída`                                   |
| GMD carcaça                 | Ganho médio diário em peso de carcaça (kg/dia)                   | `(Carcaça - (PV entrada * 0.5)) / Dias`                |
| Rend ganho                  | Rendimento do ganho                                              | `GMD carcaça / GPD Vivo`                               |
| Ganho @                     | Ganho total em arrobas durante o período de confinamento         | `PM em @ - PV entrada (@)`                             |
| Ganho@ Mês                  | Ganho em arrobas por mês                                         | `Ganho @ / (Dias / 30)`                                |
| CMS (Kg)                    | Consumo de matéria seca em quilogramas por animal por dia        | *Preenchido manualmente*                               |
| CMS%PV                      | Consumo de matéria seca como percentual do peso vivo médio       | `CMS (Kg) / ((PV saída + PV entrada) / 2)`             |
| CA                          | Conversão alimentar (kg alimento/kg ganho)                       | `CMS (Kg) / GPD Vivo`                                  |
| Conv @                      | Conversão em arrobas (kg alimento/@ ganho)                       | `CMS (Kg) * Dias / Ganho @`                            |
| Custo alimentar @           | Custo da alimentação por arroba produzida (R$)                   | `(Diária alimentar * Dias) / Ganho @`                  |
| Diária total                | Custo diário total por animal (R$)                               | `Operacional + Diária alimentar`                       |
| Operacional                 | Custo operacional diário por animal (R$)                         | *Preenchido manualmente*                               |
| Diária alimentar            | Custo diário com alimentação por animal (R$)                     | *Preenchido manualmente*                               |
| R$/kg MS                    | Custo por quilograma de matéria seca (R$)                        | `Diária alimentar / CMS (Kg)`                          |
| Custo da @ produzida        | Custo total para produzir uma arroba (R$)                        | `Custo alimentar @ + ((Operacional * Dias) / Ganho @)` |
| Valor da @ vendida          | Preço de venda da arroba (R$)                                    | *Preenchido manualmente*                               |
| Resultado Cabeça            | Resultado financeiro por animal (R$)                             | *Preenchido manualmente*                               |
| Resultado Total             | Resultado financeiro total do lote (R$)                          | `Resultado Cabeça * QTD`                               |
| BMF/Cabeça                  | Valor de hedge na Bolsa de Mercadorias e Futuros por animal (R$) | *Preenchido manualmente*                               |
| Resultado Frigorífico       | Resultado financeiro obtido na venda para o frigorífico (R$)     | *Preenchido manualmente*                               |
| BMF/Total                   | Valor total de hedge na BMF para o lote (R$)                     | `BMF/Cabeça * QTD`                                     |
| Resultado Frigorífico Hedge | Resultado financeiro total considerando o hedge (R$)             | `Resultado Frigorífico + BMF/Total`                    |
| Valor @ com Hedge           | Valor da arroba considerando a operação de hedge (R$)            | `Resultado Frigorífico Hedge / QTD / PM em @`          |
| Valor Venda Cabeça          | Valor de venda por animal (R$)                                   | `Resultado Frigorífico / QTD`                          |
