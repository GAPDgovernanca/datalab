# Guideline – Módulo filters.py

## IMPORTANTE:

TODOS OS CODIGOS FORNECIDOS A SEGUIR SÃO APENAS EXEMPLOS OU REFERENCIAS. Você foi contratado para escrever códigos e programas originais e completos, baseado nos guidelines que está recebendo. Portanto, TODOS OS CODIGOS são apenas bibliotecas de referência e de consulta e como tal devem ser tratados.

## 1. Objetivo do Módulo

O módulo **filters.py** será responsável por:

- Receber os filtros definidos pelo usuário (por exemplo, intervalo de datas, IDs de equipamentos, seleção de classe e usuário).
- Construir dinamicamente as cláusulas `WHERE` das queries SQL a partir desses filtros.
- Garantir que os filtros sejam aplicados de forma consistente e segura, colaborando para a execução correta das consultas no banco de dados.

---

## 2. Escopo e Funcionalidades

### 2.1. Funcionalidades Principais

- **Construção Dinâmica de Filtros:**  
  Gerar uma string com as condições SQL baseadas em um dicionário de filtros. Exemplos:
  
  - **Data de Referência:** Verificar se o filtro contém um intervalo e construir uma condição `BETWEEN`.
  - **ID de Equipamento:** Se informado, criar uma cláusula `IN` para os IDs.
  - **Usuário e Classe:** Quando selecionado, criar condições para os respectivos campos, com tratamento para a opção “Todos”.

- **Flexibilidade:**  
  Permitir a reutilização da função ou classe para diferentes alias de tabelas (por exemplo, utilizando alias "fc" para a tabela principal ou "t" para tabelas adicionais).

- **Validação:**  
  Validar as entradas para garantir que os dados estejam no formato esperado e evitar erros de formatação ou vulnerabilidades (por exemplo, SQL injection).

---

## 3. Estrutura e Organização do Código

### 3.1. Definição de Classes

- **Encapsulamento:**  
  Recomenda-se encapsular a lógica de construção dos filtros em uma classe (por exemplo, `FilterBuilder`). Essa abordagem melhora a organização do código e facilita a extensão futura.

- **Métodos de Responsabilidade Única:**  
  Cada método dentro da classe deve ser responsável por construir uma parte específica do filtro (ex.: método para datas, método para IDs, método para campos de seleção).

### 3.2. Exemplos de Métodos e Funções

- **build_date_filter:**  
  Receber um intervalo de datas e retornar uma condição SQL (ex.: `alias.data_referencia BETWEEN ? AND ?`) juntamente com os parâmetros.

- **build_in_filter:**  
  Construir condições para filtros que envolvem listas, como IDs ou listas de usuários/classe, utilizando placeholders.

- **build_filters:**  
  Método principal que junta as condições individuais, concatenando-as com `AND`, e retorna a cláusula completa, juntamente com uma tupla com os parâmetros.

### 3.3. Uso de Docstrings e Type Hints

- Cada classe e método deve ser documentado com docstrings explicando os parâmetros, o funcionamento interno e o retorno.
- Utilizar type hints para melhorar a legibilidade e facilitar a manutenção do código.

---

## 4. Boas Práticas e Considerações

- **Modularidade:**  
  Mantenha a lógica de construção dos filtros isolada do restante do código. Isso facilita testes unitários e futuras alterações.

- **Segurança:**  
  Ao montar a query, evite a concatenação direta de valores. Sempre utilize placeholders (`?`) e passe os valores como parâmetros, minimizando os riscos de SQL injection.

- **Validação de Entradas:**  
  Verifique se os dados recebidos (como datas e listas) estão no formato correto. Implemente funções auxiliares para limpar ou converter esses valores se necessário.

- **Testabilidade:**  
  Estruture a classe de forma que seja possível escrever testes unitários para cada método, verificando se as condições SQL e os parâmetros retornados estão corretos conforme os filtros aplicados.

- **Flexibilidade para Aliases:**  
  Permita que a classe receba um parâmetro opcional para o alias da tabela, possibilitando a construção de filtros para diferentes contextos (por exemplo, quando a mesma lógica precisa ser aplicada a tabelas com alias distintos).

---

## 5. Exemplo de Implementação do Módulo filters.py

A seguir, um exemplo simplificado que demonstra a estrutura sugerida para o módulo:

```python
from typing import Dict, List, Tuple, Optional

class FilterBuilder:
    """
    Classe para construção dinâmica de cláusulas SQL a partir de filtros do usuário.

    Métodos:
        - build_date_filter: Gera condição para intervalo de datas.
        - build_in_filter: Gera condição para filtros de lista (ex.: IDs, usuário, classe).
        - build_filters: Concatena todas as condições e retorna a cláusula completa e os parâmetros.
    """

    def __init__(self, filters: Dict, alias: str = 'fc'):
        """
        Inicializa a classe com os filtros e o alias da tabela.

        :param filters: Dicionário com os filtros aplicados.
        :param alias: Alias da tabela a ser usado nas condições SQL.
        """
        self.filters = filters
        self.alias = alias

    def build_date_filter(self, field: str) -> Tuple[Optional[str], Tuple]:
        """
        Constrói uma condição SQL para um intervalo de datas.

        :param field: Nome do campo de data.
        :return: Uma tupla contendo a condição SQL (ou None) e os parâmetros.
        """
        date_range = self.filters.get("data_referencia")
        if date_range and isinstance(date_range, list) and len(date_range) == 2:
            condition = f"{self.alias}.{field} BETWEEN ? AND ?"
            params = (date_range[0], date_range[1])
            return condition, params
        return None, ()

    def build_in_filter(self, field: str, filter_key: str) -> Tuple[Optional[str], Tuple]:
        """
        Constrói uma condição SQL para filtros que envolvem listas (por exemplo, IDs, usuário, classe).

        :param field: Nome do campo na tabela.
        :param filter_key: Chave do dicionário de filtros.
        :return: Uma tupla contendo a condição SQL (ou None) e os parâmetros.
        """
        value = self.filters.get(filter_key)
        if value and not (isinstance(value, list) and "Todos" in value):
            placeholders = ', '.join(['?'] * len(value))
            condition = f"{self.alias}.{field} IN ({placeholders})"
            return condition, tuple(value)
        return None, ()

    def build_filters(self) -> Tuple[str, Tuple]:
        """
        Constrói a cláusula completa WHERE a partir dos filtros aplicados.

        :return: Uma tupla contendo a cláusula SQL completa e os parâmetros.
        """
        conditions: List[str] = []
        parameters: List = []

        # Filtro de data_referencia
        date_condition, date_params = self.build_date_filter("data_referencia")
        if date_condition:
            conditions.append(date_condition)
            parameters.extend(date_params)

        # Filtro de id_equipamento (exemplo para IDs)
        id_condition, id_params = self.build_in_filter("id_equipamento", "id_equipamento")
        if id_condition:
            conditions.append(id_condition)
            parameters.extend(id_params)

        # Filtro para usuário (campo 'usuario')
        user_condition, user_params = self.build_in_filter("usuario", "usuario")
        if user_condition:
            conditions.append(user_condition)
            parameters.extend(user_params)

        # Filtro para classe
        class_condition, class_params = self.build_in_filter("classe", "classe")
        if class_condition:
            conditions.append(class_condition)
            parameters.extend(class_params)

        # Concatena todas as condições usando 'AND'
        where_clause = " AND ".join(conditions) if conditions else ""
        return where_clause, tuple(parameters)

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de dicionário de filtros
    filtros = {
        "data_referencia": ["2023-01-01", "2023-12-31"],
        "id_equipamento": [101, 102, 103],
        "usuario": ["Fazenda A"],
        "classe": ["Trator"]
    }

    builder = FilterBuilder(filtros, alias='fc')
    clause, params = builder.build_filters()
    print("Cláusula WHERE:", clause)
    print("Parâmetros:", params)
```

---

## 6. Considerações Finais e Próximos Passos

- **Testes:**  
  Desenvolver testes unitários para cada método da classe `FilterBuilder`, verificando se as condições e os parâmetros são gerados corretamente para diferentes cenários de entrada.

- **Documentação:**  
  Mantenha a documentação atualizada e acrescente comentários onde a lógica seja mais complexa. Isso facilitará a manutenção e a evolução do módulo.

- **Refatoração:**  
  Revise periodicamente o código para incorporar melhorias e novas funcionalidades conforme a necessidade do projeto.
