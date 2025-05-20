# Guideline – Módulo processing.py

## IMPORTANTE:

TODOS OS CODIGOS FORNECIDOS A SEGUIR SÃO APENAS EXEMPLOS OU REFERENCIAS. Você foi contratado para escrever códigos e programas originais e completos, baseado nos guidelines que está recebendo. Portanto, TODOS OS CODIGOS são apenas bibliotecas de referência e de consulta e como tal devem ser tratados.

## 1. Objetivo do Módulo

O módulo **processing.py** será responsável por:

- **Cálculo de Métricas e Indicadores:**  
  Processar os dados recebidos (normalmente em forma de DataFrame do Pandas) para calcular indicadores importantes, como:
  
  - **Taxa de Utilização Multiplicador:** Relação entre os valores realizados e os valores estimados (por exemplo, `uso_realizado` dividido por `uso_estimado`).
  - **Consumo Multiplicador:** Relação entre valores realizados e estimados para os custos, se aplicável.

- **Aplicação de Sinalizadores Visuais:**  
  Analisar as diferenças entre os valores realizados e estimados e aplicar ícones (por exemplo, 🟢, 🔴 ou ⚪) para destacar situações de economia, prejuízo ou neutralidade.

- **Preparação dos Dados para Visualizações:**  
  Ajustar os DataFrames para que fiquem prontos para serem exibidos em componentes da interface (como gráficos e tabelas).

---

## 2. Escopo e Funcionalidades

### 2.1. Funcionalidades Principais

- **Cálculo de Multiplicadores/Indicadores:**  
  Implementar funções que, a partir dos dados do DataFrame, calculem:
  
  - A **Taxa de Utilização Multiplicador**, garantindo a prevenção de divisões por zero.
  - O **Consumo Multiplicador** ou outros indicadores relevantes, utilizando os valores já ajustados no banco.

- **Aplicação de Sinalizadores:**  
  Implementar a função `apply_flags()` que, com base na diferença percentual entre valores realizados e estimados, atribua um sinalizador visual (por exemplo, 🟢 para economia, 🔴 para prejuízo e ⚪ para casos neutros).

- **Modularidade e Reutilização:**  
  Estruturar a lógica de processamento de forma que seja facilmente reutilizável e extensível, por exemplo, encapsulando os cálculos dentro de uma classe (como `DataProcessor`).

### 2.2. Requisitos e Considerações

- **Entrada:**  
  O módulo deve receber dados em forma de DataFrame (obtidos após as consultas ao banco), com colunas padronizadas (por exemplo, `uso_estimado`, `uso_realizado`, `total_estimado`, `total_realizado`, etc.).

- **Saída:**  
  Os dados processados devem estar prontos para a exibição, com novas colunas para os indicadores e sinalizadores, e com formatação apropriada para utilização em visualizações (gráficos, tabelas, etc.).

---

## 3. Estrutura e Organização do Código

### 3.1. Uso de Classes

- **Encapsulamento:**  
  Recomenda-se criar uma classe (por exemplo, `DataProcessor`) que contenha métodos específicos para:
  
  - Calcular os multiplicadores.
  - Aplicar sinalizadores aos dados.
  - Realizar outros processamentos que possam ser necessários para preparar os dados para visualização.

- **Métodos com Responsabilidade Única:**  
  Cada método deve ter uma responsabilidade clara, facilitando testes unitários e a manutenção do código.

### 3.2. Funções e Métodos

- **calculate_usage_multiplier:**  
  Método que calcula a taxa de utilização, assegurando a verificação de divisões por zero.

- **calculate_consumption_multiplier:**  
  Método (ou parte de um método) para calcular indicadores relacionados ao consumo ou custos.

- **apply_flags:**  
  Método que, com base em regras definidas (por exemplo, diferenças percentuais maiores que 10% ou menores que -10%), atribui sinalizadores visuais aos registros.

- **Outros Processamentos:**  
  Métodos para transformar ou preparar os dados (como renomear colunas, arredondar valores, etc.) podem ser incluídos conforme necessário.

---

## 4. Boas Práticas e Considerações

- **Uso de Docstrings e Type Hints:**  
  Documentar cada função e método com docstrings explicando os parâmetros, retornos e a lógica implementada. Utilize type hints para melhorar a clareza do código.

- **Tratamento de Exceções:**  
  Incluir blocos try/except para capturar e logar possíveis erros durante os cálculos, garantindo que a aplicação não interrompa a execução em caso de dados inesperados.

- **Modularidade e Testabilidade:**  
  Separe a lógica de processamento em funções/métodos pequenos e específicos, facilitando a criação de testes unitários para cada parte do processamento.

- **Reutilização e Extensibilidade:**  
  Estruture o código de forma que seja simples adicionar novos indicadores ou alterar as regras de sinalização sem impactar toda a lógica do processamento.

- **Consistência na Formatação dos Dados:**  
  Certifique-se de que os valores numéricos são formatados (por exemplo, arredondamento) conforme necessário para a visualização, e que as colunas dos DataFrames tenham nomes claros e padronizados.

---

## 5. Exemplo de Estrutura e Código do processing.py

A seguir, um exemplo simplificado demonstrando a estrutura sugerida para o módulo **processing.py**:

```python
import pandas as pd
from typing import Optional

class DataProcessor:
    """
    Classe responsável por processar os dados do dashboard, calculando métricas e aplicando sinalizadores visuais.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o DataProcessor com um DataFrame contendo os dados extraídos do banco.

        :param df: DataFrame com os dados brutos.
        """
        self.df = df.copy()

    def calculate_usage_multiplier(self) -> pd.DataFrame:
        """
        Calcula a Taxa de Utilização Multiplicador para cada registro.
        A fórmula utilizada é: uso_realizado / uso_estimado, com verificação para evitar divisão por zero.

        :return: DataFrame com uma nova coluna 'Taxa Utilização Multiplicador'.
        """
        def compute(row):
            try:
                if row['uso_estimado'] != 0:
                    return row['uso_realizado'] / row['uso_estimado']
                return 0.0
            except Exception as e:
                # Log ou tratamento específico podem ser adicionados aqui
                return 0.0

        self.df['Taxa Utilização Multiplicador'] = self.df.apply(compute, axis=1)
        return self.df

    def calculate_consumption_multiplier(self) -> pd.DataFrame:
        """
        Calcula o Consumo Multiplicador, definido como a razão entre o valor realizado e o estimado para custos.
        Adapte a fórmula conforme os nomes das colunas existentes no DataFrame.

        :return: DataFrame com uma nova coluna 'Consumo Multiplicador'.
        """
        def compute(row):
            try:
                if row.get('total_estimado', 0) != 0:
                    return row.get('total_realizado', 0) / row.get('total_estimado', 0)
                return 0.0
            except Exception as e:
                return 0.0

        self.df['Consumo Multiplicador'] = self.df.apply(compute, axis=1)
        return self.df

    def apply_flags(self, threshold: float = 10.0) -> pd.DataFrame:
        """
        Aplica sinalizadores visuais aos registros com base na diferença percentual entre os valores realizados e estimados.
        Exemplos de sinalizadores:
          - 🟢: Desvio percentual > threshold (indicando economia).
          - 🔴: Desvio percentual < -threshold (indicando prejuízo).
          - ⚪: Casos em que o desvio está dentro do limite.

        :param threshold: Valor percentual para definir os limites dos sinalizadores.
        :return: DataFrame com uma nova coluna 'Sinalizador'.
        """
        def flag(row):
            try:
                # Supondo que a coluna 'total_diferenca' e 'total_estimado' estejam presentes
                if row['total_estimado'] != 0:
                    percentual = (row['total_diferenca'] / row['total_estimado']) * 100
                    if percentual > threshold:
                        return '🟢'
                    elif percentual < -threshold:
                        return '🔴'
                return '⚪'
            except Exception:
                return '⚪'

        self.df['Sinalizador'] = self.df.apply(flag, axis=1)
        return self.df

    def process_all(self) -> pd.DataFrame:
        """
        Método que encadeia todas as etapas de processamento:
        - Calcula os multiplicadores.
        - Aplica os sinalizadores.
        - Realiza outras transformações necessárias.

        :return: DataFrame final processado e pronto para visualização.
        """
        self.calculate_usage_multiplier()
        self.calculate_consumption_multiplier()
        self.apply_flags()
        # Outras transformações podem ser adicionadas aqui (por exemplo, renomeação de colunas, arredondamentos, etc.)
        return self.df

# Exemplo de uso:
if __name__ == "__main__":
    # Supondo que exista um DataFrame 'df' com as colunas necessárias, obtido a partir das consultas
    sample_data = {
        'uso_estimado': [100, 0, 200],
        'uso_realizado': [110, 0, 180],
        'total_estimado': [1000, 1500, 2000],
        'total_realizado': [950, 1600, 2100],
        'total_diferenca': [-50, 100, 100]
    }
    df = pd.DataFrame(sample_data)

    processor = DataProcessor(df)
    processed_df = processor.process_all()
    print(processed_df)
```

---

## 6. Considerações Finais e Próximos Passos

- **Testes Unitários:**  
  Desenvolver testes que validem individualmente cada método (cálculo dos multiplicadores e aplicação dos sinalizadores), garantindo que as regras de negócio estejam corretas para diferentes cenários.

- **Refatoração e Melhoria Contínua:**  
  Revisar periodicamente a lógica de processamento, especialmente quando novas métricas ou regras forem adicionadas, para manter o código limpo e eficiente.

- **Documentação e Comentários:**  
  Manter a documentação atualizada e detalhada, explicando a lógica de cada método, para facilitar a compreensão por novos desenvolvedores e a manutenção futura.
