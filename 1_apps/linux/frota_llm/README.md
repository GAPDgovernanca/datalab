```markdown
# Módulo de Filtros e Cálculos do Dashboard

Este módulo realiza consultas ao banco de dados, calcula multiplicadores e aplica sinalizadores (flags) aos registros com base nos desvios entre os valores orçados e realizados. Toda a configuração dos sinalizadores está centralizada em um arquivo YAML (**db_config.yaml**), o que facilita futuras alterações sem a necessidade de modificar o código. Essa abordagem, juntamente com o uso de caminho absoluto para carregar o arquivo de configuração, garante que o módulo funcione corretamente no ambiente do Streamlit Cloud.

---

## Arquivos Principais

- **db_filters.py**  
  Contém as funções:
  - `build_filters(filtros: Dict, alias: str = 'fc')`: Constrói uma string SQL de condições a partir dos filtros fornecidos.
  - `calcular_multiplicadores(df: pd.DataFrame)`: Calcula multiplicadores (Taxa Utilização e Consumo) com base nos custos e totais orçados e realizados.
  - `apply_flags(df)`: Aplica sinalizadores aos registros do DataFrame com base no desvio percentual entre o orçamento e o realizado.
  
  Essa implementação utiliza um caminho absoluto para localizar o arquivo **db_config.yaml** no mesmo diretório deste módulo, garantindo que o arquivo seja encontrado corretamente, mesmo no Streamlit Cloud.

- **db_config.yaml**  
  Arquivo de configuração que centraliza todos os parâmetros relativos aos sinalizadores.  
  Qualquer ajuste futuro relativo aos limites ou aos ícones dos sinalizadores deverá ser feito apenas neste arquivo.

---

## Exemplo de Configuração (db_config.yaml)

```yaml
threshold_percentage: 10
flag_over_threshold: "🔴"
flag_under_threshold: "🟢"
flag_neutral: "⚪"
flag_no_budget: "🔶"
```

- **threshold_percentage**: Define o limite percentual para identificar desvios críticos.
- **flag_over_threshold**: Sinalizador aplicado quando o percentual calculado é superior ao limite (indicando, conforme o cálculo, que o realizado ficou abaixo do orçado).
- **flag_under_threshold**: Sinalizador aplicado quando o percentual calculado é inferior ao limite negativo (indicando que o realizado excedeu o orçado).
- **flag_neutral**: Sinalizador aplicado quando o desvio está dentro do intervalo aceitável (entre -threshold e +threshold).
- **flag_no_budget**: Sinalizador especial para situações onde não há orçamento definido, mas há custo realizado.

---

## Dependências

Para o correto funcionamento deste módulo, além das bibliotecas que já fazem parte da sua instalação, é necessário ter instalado:

- **pandas** (para manipulação dos DataFrames)
- **PyYAML** (para carregar o arquivo YAML de configuração)

Para instalar o PyYAML, execute:

```bash
pip install pyyaml
```

---

## Considerações para o Ambiente Streamlit Cloud

No Streamlit Cloud, o diretório de execução pode ser diferente do diretório onde os arquivos do projeto estão localizados. Para evitar problemas de localização do arquivo **db_config.yaml**, o módulo **db_filters.py** utiliza o caminho absoluto baseado na sua própria localização:

```python
import os
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_config.yaml")
```

**Certifique-se de que o arquivo db_config.yaml esteja no mesmo diretório que db_filters.py.**

---

## Instruções de Uso

1. **Configuração:**  
   - Coloque os arquivos `db_filters.py` e `db_config.yaml` juntos no mesmo diretório do seu projeto.
   - Ajuste os parâmetros dos sinalizadores, se necessário, editando apenas o arquivo **db_config.yaml**.

2. **Integração no Projeto:**  
   Importe e utilize as funções no seu aplicativo, por exemplo, no seu dashboard:

   ```python
   from db_filters import build_filters, calcular_multiplicadores, apply_flags

   # Exemplo de uso:
   df = get_filtered_data(filtros)
   df = calcular_multiplicadores(df)
   df = apply_flags(df)
   ```

3. **Execução no Streamlit Cloud:**  
   Como o caminho absoluto é utilizado para carregar o arquivo de configuração, o módulo funcionará corretamente independentemente do diretório de execução.

---

## Contribuição e Manutenção

- **Centralização da Configuração:**  
  Faça todos os ajustes relativos aos sinalizadores exclusivamente no arquivo **db_config.yaml**. Isso ajuda a manter a consistência e evita que alterações acidentais no código quebrem a integração com o restante do sistema.

- **Documentação:**  
  A docstring e os comentários no código explicam a lógica e os critérios usados para aplicar os sinalizadores. Esses comentários devem ser mantidos atualizados à medida que a lógica evoluir.

---