### Passos para Criar e Gerenciar um Ambiente Virtual com `virtualenvwrapper`

#### 1. **Criar um Novo Ambiente Virtual**

Para criar um novo ambiente virtual com o **`virtualenvwrapper`**, você pode usar o comando **`mkvirtualenv`**. Este comando cria o ambiente e já o ativa automaticamente. Além disso, o ambiente fica salvo na pasta **`~/.virtualenvs`**, onde todos os ambientes são gerenciados.

```bash
mkvirtualenv nome_do_ambiente
```

- **Exemplo**: Se precisar criar um ambiente virtual para um projeto chamado "projeto_novo":
  ```bash
  mkvirtualenv projeto_novo_env
  ```
- Isso cria um ambiente chamado **`projeto_novo_env`**.

#### 2. **Ativar um Ambiente Virtual Existente**

Para ativar um ambiente virtual que já foi criado e está na pasta **`~/.virtualenvs`**, você pode usar o comando **`workon`**:

```bash
workon nome_do_ambiente
```

- **Exemplo**: Se quiser ativar o ambiente **`projeto_novo_env`**:
  ```bash
  workon projeto_novo_env
  ```
- Isso ativará o ambiente e você verá o nome do ambiente entre parênteses no terminal, como `(projeto_novo_env)`.

#### 3. **Instalar Dependências no Ambiente Virtual Ativo**

Depois de ativar o ambiente virtual, você pode instalar as dependências necessárias usando o **`pip`**:

```bash
pip install nome_da_dependencia
```

- **Exemplo**: Para instalar **`requests`**:
  ```bash
  pip install requests
  ```

Se você tem um arquivo **`requirements.txt`** com todas as dependências do projeto, pode usar:

```bash
pip install -r requirements.txt
```

#### 4. **Desativar o Ambiente Virtual**

Quando terminar de trabalhar no ambiente virtual, você pode desativá-lo para retornar ao ambiente Python global do sistema:

```bash
deactivate
```

- Isso desativará o ambiente e removerá o nome do ambiente do seu prompt.

#### 5. **Remover um Ambiente Virtual Que Não Precisa Mais**

Se em algum momento você decidir que não precisa mais de um ambiente virtual, pode removê-lo com o comando **`rmvirtualenv`**:

```bash
rmvirtualenv nome_do_ambiente
```

- **Exemplo**: Para remover o ambiente **`projeto_novo_env`**:
  ```bash
  rmvirtualenv projeto_novo_env
  ```
- Isso apagará o ambiente completamente do diretório **`~/.virtualenvs`**.

#### 6. **Listar Todos os Ambientes Virtuais Disponíveis**

Para listar todos os ambientes virtuais que você tem disponíveis, use:

```bash
workon
```

- Isso mostrará uma lista com o nome de todos os ambientes que estão em **`~/.virtualenvs`**, facilitando para escolher qual você deseja ativar.

### Resumo dos Comandos

| **Comando**                   | **Função**                                  |
|-------------------------------|--------------------------------------------|
| `mkvirtualenv nome_do_ambiente` | Cria um novo ambiente virtual.             |
| `workon nome_do_ambiente`       | Ativa um ambiente virtual existente.       |
| `deactivate`                   | Desativa o ambiente virtual ativo.         |
| `rmvirtualenv nome_do_ambiente` | Remove um ambiente virtual que não é mais necessário. |
| `workon`                       | Lista todos os ambientes virtuais disponíveis. |

### Exemplo de Fluxo Completo

1. **Criar um Novo Ambiente** para um novo projeto:
   ```bash
   mkvirtualenv novo_projeto_env
   ```
2. **Instalar as Dependências** do projeto:
   ```bash
   pip install -r requirements.txt
   ```
3. **Trabalhar no Projeto** (editar código, executar testes, etc.).
4. **Desativar o Ambiente** quando terminar:
   ```bash
   deactivate
   ```
5. **Remover o Ambiente** se ele não for mais necessário:
   ```bash
   rmvirtualenv novo_projeto_env
   ```

### Benefícios do `virtualenvwrapper`

- **Centralização dos Ambientes**: Todos os ambientes ficam em **`~/.virtualenvs`**, o que facilita o gerenciamento.
- **Facilidade de Ativação**: Com o comando **`workon`**, você não precisa lembrar o caminho exato dos ambientes.
- **Organização**: Menos ambiente espalhado pelo sistema, facilitando a manutenção e evitando duplicidades.