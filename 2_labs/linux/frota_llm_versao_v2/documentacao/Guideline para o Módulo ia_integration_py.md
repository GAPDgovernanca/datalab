# Guideline – Módulo ia_integration.py

## 1. Objetivo do Módulo

O módulo **ia_integration.py** deve centralizar toda a lógica de comunicação com a API de inteligência artificial (IA). Suas responsabilidades incluem:

- **Envio de Prompts:** Construir e enviar prompts estruturados para a API, incorporando informações dos dados do sistema e das perguntas dos usuários.
- **Tratamento de Respostas:** Processar e limpar as respostas recebidas da API, removendo, por exemplo, quaisquer tags ou seções desnecessárias.
- **Configuração e Autenticação:** Gerenciar a leitura da chave de API a partir de variáveis de ambiente e configurar o cliente da API.
- **Modularidade:** Permitir a customização de parâmetros, como o nome do modelo e ajustes na formatação do prompt, para facilitar a manutenção e a extensão futura.

---

## 2. Escopo e Funcionalidades

### 2.1. Funcionalidades Principais

- **Envio de Solicitações à API:**
  
  - Construir um prompt detalhado que inclua instruções, regras, e dados relevantes.
  - Enviar a consulta à API de IA usando a biblioteca cliente (por exemplo, `groq`).
  - Permitir a especificação de parâmetros, como o modelo a ser utilizado (ex.: `"deepseek-r1-distill-llama-70b"`).

- **Tratamento e Limpeza da Resposta:**
  
  - Remover partes desnecessárias da resposta (por exemplo, tags `<think>` caso existam).
  - Retornar uma resposta formatada e pronta para exibição na interface do usuário.

- **Configuração da API:**
  
  - Ler a chave de API a partir de uma variável de ambiente (ex.: `GROQ_API_KEY`).
  - Configurar o cliente da API de forma segura e encapsulada.

### 2.2. Entrada e Saída

- **Entradas:**
  
  - **Dados JSON:** Dados combinados do sistema (por exemplo, dados filtrados e dados adicionais) para incorporar no prompt.
  - **Pergunta do Usuário:** A consulta textual que o usuário deseja enviar para a API.
  - **Parâmetros Opcionais:** Nome do modelo, ajustes na formatação do prompt, etc.

- **Saída:**
  
  - A resposta processada e limpa da API, pronta para ser exibida na interface.

---

## 3. Estrutura e Organização do Código

### 3.1. Uso de Classes

- **Encapsulamento:**  
  Recomenda-se criar uma classe, por exemplo, `AIIntegration`, que centralize toda a comunicação com a API. Essa abordagem torna o código mais modular e facilita testes e manutenção.

- **Métodos de Responsabilidade Única:**  
  Cada método dentro da classe deve ter uma responsabilidade clara:
  
  - Um método para construir o prompt.
  - Um método para enviar a solicitação à API.
  - Um método para tratar/limpar a resposta.

### 3.2. Organização dos Métodos

- **Construtor (`__init__`):**
  
  - Configura a chave de API e instancia o cliente da API.
  - Pode receber parâmetros opcionais para configurações padrão (ex.: modelo padrão).

- **Método `build_prompt`:**
  
  - Constrói o prompt incorporando dados do sistema e a pergunta do usuário.
  - Deve ser flexível e permitir a alteração da estrutura do prompt conforme a necessidade.

- **Método `query`:**
  
  - Envia a mensagem à API utilizando o cliente configurado.
  - Trata exceções e garante que erros sejam logados e, se necessário, repassados à camada superior.

- **Método `clean_response`:**
  
  - Processa a resposta recebida para remover tags ou seções desnecessárias (por exemplo, eliminando partes entre `<think>` e `</think>`).

---

## 4. Boas Práticas e Considerações

- **Documentação e Type Hints:**  
  Cada método deve ser documentado com docstrings explicando os parâmetros, retorno e lógica. Utilize type hints para melhorar a clareza e facilitar a manutenção.

- **Tratamento de Exceções e Logging:**  
  Envolva as chamadas à API em blocos `try/except` para capturar erros e registrar mensagens de log úteis para depuração. Certifique-se de que falhas não interrompam a aplicação de forma inesperada.

- **Modularidade e Testabilidade:**  
  Estruture o código para que seja fácil escrever testes unitários para cada método. Por exemplo, teste a construção do prompt, a limpeza da resposta e a gestão de exceções.

- **Configuração Segura:**  
  Leia a chave de API a partir de uma variável de ambiente e nunca a exponha diretamente no código. Considere a possibilidade de criar um wrapper de configuração que facilite a atualização dos parâmetros da API.

- **Flexibilidade para Ajustes:**  
  Permita que a estrutura do prompt e os parâmetros (como o nome do modelo) sejam facilmente configuráveis, seja via parâmetros do construtor ou métodos setter.

---

## 5. Exemplo de Estrutura e Código do ia_integration.py

```python
import os
import logging
import re
from typing import Any, Dict

# Supondo que a biblioteca 'groq' esteja instalada e configurada.
from groq import Groq

class AIIntegration:
    """
    Classe para integração com a API de inteligência artificial.

    Responsabilidades:
    - Construir e enviar prompts à API.
    - Tratar e limpar as respostas recebidas.
    """

    def __init__(self, model_name: str = "deepseek-r1-distill-llama-70b"):
        """
        Inicializa a integração com a API de IA.

        :param model_name: Nome do modelo a ser utilizado na consulta.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Chave de API não encontrada na variável de ambiente 'GROQ_API_KEY'.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def build_prompt(self, data_json: Dict[str, Any], question: str) -> str:
        """
        Constrói o prompt que será enviado para a API.

        O prompt deve incluir informações relevantes sobre os dados e as regras de formatação, além da pergunta do usuário.

        :param data_json: Dados do sistema em formato JSON.
        :param question: Pergunta do usuário.
        :return: Prompt completo como uma string.
        """
        # Exemplo de prompt estruturado. Ajuste conforme necessário.
        prompt = f"""
        Você é um especialista em gestão de frota agrícola, focado em análise operacional e financeira.

        Regras de Formatação:
        - Utilize regras de arredondamento apropriadas.
        - Mantenha consistência em tabelas e formatação numérica.

        Dados do Sistema:
        {data_json}

        Pergunta do Usuário:
        {question}
        """
        return prompt.strip()

    def clean_response(self, response: str) -> str:
        """
        Limpa a resposta da API, removendo seções indesejadas, como tags de pensamento (<think>...</think>).

        :param response: Resposta bruta da API.
        :return: Resposta limpa.
        """
        # Remover conteúdo entre <think> e </think>, se presente.
        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        return cleaned_response.strip()

    def query(self, data_json: Dict[str, Any], question: str) -> str:
        """
        Envia a consulta à API de IA e retorna a resposta processada.

        :param data_json: Dados do sistema em formato JSON.
        :param question: Pergunta do usuário.
        :return: Resposta da IA, processada e limpa.
        """
        try:
            prompt = self.build_prompt(data_json, question)
            self.logger.debug(f"Prompt enviado para a API: {prompt}")

            # Envia a consulta à API usando o cliente
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a highly specialized assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name
            )

            # Obter a resposta da API
            response = chat_completion.choices[0].message.content
            self.logger.debug(f"Resposta bruta da API: {response}")

            # Limpar e retornar a resposta
            return self.clean_response(response)
        except Exception as e:
            self.logger.error(f"Erro ao consultar a API de IA: {e}")
            raise

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de dados JSON e pergunta
    example_data = {
        "filtered_data": [{"id_equipamento": 101, "total_estimado": 1000, "total_realizado": 950}],
        "additional_data": {"fato_combustivel": [], "fato_manutencao": []}
    }
    example_question = "Quais são os principais indicadores de desempenho da frota?"

    ai_integration = AIIntegration()
    resposta = ai_integration.query(example_data, example_question)
    print("Resposta da IA:", resposta)
```

---

## 6. Considerações Finais e Próximos Passos

- **Testes Unitários:**  
  Desenvolver testes que validem:
  
  - A construção correta do prompt.
  - O tratamento adequado das respostas (limpeza de tags indesejadas).
  - A gestão de exceções e o comportamento da função `query` em caso de falhas.

- **Documentação:**  
  Mantenha a documentação atualizada e detalhada, garantindo que novos desenvolvedores possam entender e modificar a integração sem dificuldades.

- **Refatoração e Melhorias:**  
  Após a implementação inicial, revise o código para incorporar melhorias baseadas no feedback dos testes e na experiência de uso, garantindo a robustez e flexibilidade da integração.
