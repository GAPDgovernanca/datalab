# Guideline – Módulo db.py

## IMPORTANTE:

TODOS OS CODIGOS FORNECIDOS A SEGUIR SÃO APENAS EXEMPLOS OU REFERENCIAS. Seu papel deve ser escrever códigos e programas originais e completos, baseado nos guidelines que está recebendo. Portanto, TODOS OS CODIGOS são apenas bibliotecas de estudo, leitura e de consulta e como tal devem ser tratados. Evite copiar:

## 1. Objetivo do Módulo

O módulo **db.py** deverá centralizar todas as operações de conexão, consulta e manipulação de dados do banco SQLite, garantindo:

- **Robustez:** Tratamento adequado de erros e fechamento seguro das conexões.
- **Segurança:** Uso de parâmetros em queries para mitigar riscos de SQL injection.
- **Manutenibilidade:** Código modular, documentado e organizado em classes/métodos.
- **Facilidade de Testes:** Estrutura que permita a criação de testes unitários para cada função.

---

## 2. Mapeamento do Banco de Dados

Este projeto utilizará o seguinte esquema do banco de dados:

### Tabela: `dim_equipamento`

- **Colunas:**
  - `id_equipamento`
  - `modelo`
  - `usuario`
  - `classe`
  - `data_criacao`

### Tabela: `fato_uso`

- **Colunas:**
  - `id`
  - `id_equipamento`
  - `tipo_medidor`
  - `uso_estimado`
  - `uso_realizado`
  - `uso_diferenca`
  - `data_referencia`
  - `data_processamento`

### Tabela: `sqlite_sequence`

- **Colunas:**
  - `name`
  - `seq`

### Tabela: `fato_custo`

- **Colunas:**
  - `id`
  - `id_equipamento`
  - `custo_hora_estimado`
  - `custo_hora_realizado`
  - `custo_hora_diferenca`
  - `total_estimado`
  - `total_realizado`
  - `total_diferenca`
  - `data_referencia`
  - `data_processamento`

### Tabela: `fato_combustivel`

- **Colunas:**
  - `id`
  - `id_equipamento`
  - `comb_litros_estimado`
  - `comb_litros_realizado`
  - `comb_litros_diferenca`
  - `comb_valor_unitario_estimado`
  - `comb_valor_unitario_realizado`
  - `comb_valor_unitario_diferenca`
  - `comb_total_estimado`
  - `comb_total_realizado`
  - `comb_total_diferenca`
  - `data_referencia`
  - `data_processamento`

### Tabela: `fato_manutencao`

- **Colunas:**
  - `id`
  - `id_equipamento`
  - `lubrificantes_estimado`
  - `lubrificantes_realizado`
  - `lubrificantes_diferenca`
  - `filtros_estimado`
  - `filtros_realizado`
  - `filtros_diferenca`
  - `graxas_estimado`
  - `graxas_realizado`
  - `graxas_diferenca`
  - `pecas_servicos_estimado`
  - `pecas_servicos_realizado`
  - `pecas_servicos_diferenca`
  - `data_referencia`
  - `data_processamento`

### Tabela: `fato_reforma`

- **Colunas:**
  - `id`
  - `id_equipamento`
  - `reforma_estimado`
  - `reforma_realizado`
  - `reforma_diferenca`
  - `data_referencia`
  - `data_processamento`

### Relacionamentos

- **fato_uso:** `id_equipamento` → `dim_equipamento.id_equipamento`
- **fato_custo:** `id_equipamento` → `dim_equipamento.id_equipamento`
- **fato_combustivel:** `id_equipamento` → `dim_equipamento.id_equipamento`
- **fato_manutencao:** `id_equipamento` → `dim_equipamento.id_equipamento`
- **fato_reforma:** `id_equipamento` → `dim_equipamento.id_equipamento`

---

## 3. Recomendações e Boas Práticas

### 3.1. Uso de Classes e Modularidade

- **Encapsulamento:**  
  Crie uma classe (por exemplo, `Database`) que centralize a lógica de conexão e execução de queries. Essa abordagem melhora a organização do código e facilita a manutenção e extensão futura.
- **Divisão de Responsabilidades:**  
  Separe métodos para diferentes operações: conexão, execução de query, recuperação de resultados, etc.

### 3.2. Gerenciamento de Conexões

- **Context Managers:**  
  Utilize o `with` statement (através do módulo `contextlib`) para garantir que a conexão seja fechada corretamente, mesmo em casos de erro.
- **Row Factory:**  
  Configure a propriedade `row_factory` para `sqlite3.Row` para facilitar o acesso aos dados retornados como dicionários.

### 3.3. Tratamento de Erros e Logging

- **Exceções:**  
  Implemente tratamento de exceções para capturar e logar erros durante a conexão e execução de queries.
- **Logging:**  
  Configure um logger para registrar erros e eventos importantes, auxiliando na depuração e manutenção.

### 3.4. Segurança e SQL Injection

- **Parâmetros em Queries:**  
  Sempre utilize placeholders (`?`) e passe os parâmetros separadamente para evitar vulnerabilidades de SQL injection.

### 3.5. Documentação

- **Docstrings e Comentários:**  
  Documente cada método e classe com docstrings, explicando a funcionalidade, os parâmetros esperados e os retornos. Isso facilitará a compreensão e a manutenção do código por novos desenvolvedores.

### 3.6. Testabilidade

- **Testes Unitários:**  
  Estruture o código de forma que seja possível escrever testes unitários para os métodos da classe, garantindo que as operações de banco estejam funcionando conforme o esperado.

---

## 4. Exemplo de Estrutura e Código do db.py

## IMPORTANTE:

TODOS OS CODIGOS FORNECIDOS A SEGUIR SÃO APENAS EXEMPLOS OU REFERENCIAS. Seu papel deve ser escrever códigos e programas originais e completos, baseado nos guidelines que está recebendo. Portanto, TODOS OS CODIGOS são apenas bibliotecas de estudo, leitura e de consulta e como tal devem ser tratados. Evite copiar:
<exemplo de código>

```python
import sqlite3
import logging
from contextlib import contextmanager

class Database:
    """
    Classe para gerenciamento da conexão e execução de operações no banco de dados SQLite.

    Esquema do Banco de Dados:

    Tabela: dim_equipamento
    - id_equipamento, modelo, usuario, classe, data_criacao

    Tabela: fato_uso
    - id, id_equipamento, tipo_medidor, uso_estimado, uso_realizado, uso_diferenca, data_referencia, data_processamento

    Tabela: sqlite_sequence
    - name, seq

    Tabela: fato_custo
    - id, id_equipamento, custo_hora_estimado, custo_hora_realizado, custo_hora_diferenca, total_estimado, total_realizado, total_diferenca, data_referencia, data_processamento

    Tabela: fato_combustivel
    - id, id_equipamento, comb_litros_estimado, comb_litros_realizado, comb_litros_diferenca, comb_valor_unitario_estimado, comb_valor_unitario_realizado, comb_valor_unitario_diferenca, comb_total_estimado, comb_total_realizado, comb_total_diferenca, data_referencia, data_processamento

    Tabela: fato_manutencao
    - id, id_equipamento, lubrificantes_estimado, lubrificantes_realizado, lubrificantes_diferenca, filtros_estimado, filtros_realizado, filtros_diferenca, graxas_estimado, graxas_realizado, graxas_diferenca, pecas_servicos_estimado, pecas_servicos_realizado, pecas_servicos_diferenca, data_referencia, data_processamento

    Tabela: fato_reforma
    - id, id_equipamento, reforma_estimado, reforma_realizado, reforma_diferenca, data_referencia, data_processamento

    Relacionamentos:
    - fato_uso.id_equipamento -> dim_equipamento.id_equipamento
    - fato_custo.id_equipamento -> dim_equipamento.id_equipamento
    - fato_combustivel.id_equipamento -> dim_equipamento.id_equipamento
    - fato_manutencao.id_equipamento -> dim_equipamento.id_equipamento
    - fato_reforma.id_equipamento -> dim_equipamento.id_equipamento
    """

    def __init__(self, db_path: str):
        """
        Inicializa a classe Database com o caminho para o banco de dados.

        :param db_path: Caminho para o arquivo SQLite.
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @contextmanager
    def get_connection(self):
        """
        Context manager para gerenciar a conexão com o banco de dados.
        Garante que a conexão seja fechada após o uso.

        :yield: Objeto de conexão do SQLite.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao conectar com o banco: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: tuple = None):
        """
        Executa uma query no banco de dados.

        :param query: String com a instrução SQL.
        :param params: Tupla com os parâmetros a serem passados para a query.
        :return: Cursor com os resultados da execução.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
            except sqlite3.Error as e:
                self.logger.error(f"Erro na execução da query: {e}")
                raise

    def fetch_all(self, query: str, params: tuple = None):
        """
        Executa uma query e retorna todos os resultados.

        :param query: Instrução SQL.
        :param params: Parâmetros para a query.
        :return: Lista de linhas (como objetos sqlite3.Row).
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = None):
        """
        Executa uma query e retorna apenas uma linha de resultado.

        :param query: Instrução SQL.
        :param params: Parâmetros para a query.
        :return: Uma linha (como objeto sqlite3.Row) ou None.
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchone()

    # Exemplo de método específico para obter datas padrão
    def get_date_defaults(self):
        """
        Recupera as datas mínimas e máximas (data_referencia e data_processamento)
        combinadas de todas as tabelas de fato.

        :return: Objeto com os valores mínimo e máximo.
        """
        query = """
            SELECT MIN(data_referencia) AS min_data_referencia, 
                   MAX(data_referencia) AS max_data_referencia, 
                   MIN(data_processamento) AS min_data_processamento, 
                   MAX(data_processamento) AS max_data_processamento
            FROM (
                SELECT data_referencia, data_processamento FROM fato_custo
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_combustivel
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_manutencao
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_reforma
                UNION ALL
                SELECT data_referencia, data_processamento FROM fato_uso
            )
        """
        return self.fetch_one(query)

# Outras funções ou classes relacionadas ao acesso ao DB podem ser adicionadas aqui.
```

</exemplo de código>

## 5. Considerações Finais e Próximos Passos

- **Testes Unitários:**  
  Desenvolver testes que cubram os métodos da classe `Database`, verificando a conectividade, execução de queries e o correto fechamento das conexões.
