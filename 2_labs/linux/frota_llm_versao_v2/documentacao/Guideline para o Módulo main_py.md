# Guideline – Módulo main.py

## 1. Objetivo do Módulo

O módulo **main.py** deve:

- Ser o ponto de entrada da aplicação, iniciando a execução do dashboard.
- Coordenar a inicialização e a integração de todos os módulos do projeto:
  - **db.py**: Gerenciamento de conexões e operações com o banco de dados.
  - **filters.py**: Construção dinâmica dos filtros SQL.
  - **processing.py**: Processamento dos dados e cálculo de indicadores.
  - **ia_integration.py**: Comunicação com a API de inteligência artificial.
  - **ui.py**: Renderização da interface e interatividade do dashboard.
- Gerenciar a configuração geral da aplicação (por exemplo, logging, variáveis de ambiente e configurações de layout do Streamlit).
- Organizar o fluxo de execução, desde a captura dos filtros e consulta aos dados até a apresentação final na interface.

---

## 2. Estrutura e Organização do Código

### 2.1. Organização Geral

- **Ponto de Entrada:**  
  Utilize a construção padrão do Python com `if __name__ == "__main__":` para garantir que o módulo seja executado como programa principal.

- **Importação dos Módulos:**  
  Importe os módulos desenvolvidos anteriormente (db, filters, processing, ia_integration, ui) e quaisquer bibliotecas externas necessárias (por exemplo, Streamlit, logging, etc.).

- **Configuração Inicial:**  
  Configure o ambiente da aplicação:
  
  - Configuração do layout do Streamlit com `st.set_page_config()`.
  - Configuração de logging para registrar eventos e erros.
  - Carregamento de variáveis de ambiente (por exemplo, chave de API).

- **Orquestração do Fluxo de Dados:**  
  Organize as etapas do fluxo da aplicação, que podem incluir:
  
  1. Inicialização dos módulos e leitura dos filtros do usuário.
  2. Consulta ao banco de dados e aplicação dos filtros (utilizando os módulos *db.py* e *filters.py*).
  3. Processamento dos dados (via *processing.py*).
  4. Integração com a API de IA (via *ia_integration.py*), se aplicável.
  5. Renderização da interface e dos componentes visuais (via *ui.py*).

### 2.2. Uso de Funções e Classes

- **Função Principal:**  
  Crie uma função principal (por exemplo, `main()`) que encapsule a lógica de inicialização e orquestração do sistema. Isso facilita a leitura e a manutenção do código e possibilita a reutilização ou testes desta função.

- **Modularidade:**  
  Delegue as responsabilidades específicas a funções e métodos dos módulos importados. O `main.py` deve se preocupar com a coordenação geral e a passagem de dados entre os módulos.

- **Tratamento de Exceções e Logging:**  
  Utilize blocos `try/except` para capturar erros durante a execução e registrar mensagens úteis com o módulo `logging`. Isso ajudará a identificar e resolver problemas sem interromper a execução da aplicação.

---

## 3. Boas Práticas e Considerações

- **Clareza e Documentação:**  
  Documente a função `main()` e as seções críticas do código com docstrings, explicando o fluxo de execução e a finalidade de cada etapa.

- **Separação de Responsabilidades:**  
  O `main.py` deve apenas coordenar o fluxo de execução, deixando a lógica de negócios (consulta, processamento, integração com IA e renderização) a cargo dos módulos especializados.

- **Testabilidade:**  
  Estruture o código de forma que a função `main()` e os métodos auxiliares possam ser testados individualmente. Isso pode incluir a criação de funções de inicialização que possam ser chamadas em ambientes de teste sem iniciar toda a interface.

- **Configuração de Ambiente:**  
  Centralize a leitura de variáveis de ambiente e as configurações iniciais para facilitar a alteração de parâmetros e a adaptação a diferentes ambientes (desenvolvimento, teste, produção).

---

## 4. Exemplo de Estrutura e Código do main.py

```python
import os
import logging
import streamlit as st

# Importação dos módulos desenvolvidos
from db import Database
from filters import FilterBuilder
from processing import DataProcessor
from ia_integration import AIIntegration
from ui import main_ui

def configure_logging() -> None:
    """
    Configura o sistema de logging para a aplicação.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def configure_environment() -> None:
    """
    Configura o ambiente da aplicação, como variáveis de ambiente e layout do Streamlit.
    """
    st.set_page_config(layout="wide")
    # Outras configurações de ambiente podem ser adicionadas aqui, se necessário

def main():
    """
    Função principal que orquestra o fluxo de execução do dashboard.
    """
    # Configura logging e ambiente
    configure_logging()
    configure_environment()

    logger = logging.getLogger(__name__)
    logger.debug("Iniciando o dashboard de gestão de frota agrícola.")

    try:
        # Renderiza a interface do usuário e captura filtros
        main_ui()

        # Caso seja necessário, integre a lógica para obter dados do banco e processá-los.
        # Exemplo:
        # db_instance = Database("./frota.db")
        # filtros = ...  # Capturados via UI ou processados via FilterBuilder
        # data_raw = db_instance.fetch_all("SELECT * FROM fato_custo")
        # processor = DataProcessor(data_raw)
        # processed_data = processor.process_all()
        # ui.render_table(processed_data)

        # A integração com a API de IA também pode ser realizada, se necessário,
        # quando o usuário submeter uma pergunta.
        # Exemplo:
        # ai_integration = AIIntegration()
        # resposta = ai_integration.query(data_json, user_question)
        # st.markdown(resposta)

    except Exception as e:
        logger.error(f"Erro na execução do dashboard: {e}")
        st.error("Ocorreu um erro ao executar o dashboard. Por favor, verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()
```

---

## 5. Considerações Finais e Próximos Passos

- **Testes e Validação:**  
  Desenvolver testes que validem o fluxo de execução coordenado pelo `main.py`, simulando a passagem de dados entre os módulos e a resposta da interface.

- **Feedback e Iteração:**  
  Após a implementação inicial, colete feedback dos usuários e da equipe de desenvolvimento para ajustar a orquestração e melhorar a robustez do fluxo.

- **Documentação Contínua:**  
  Mantenha a documentação do `main.py` atualizada, garantindo que novas alterações e integrações sejam refletidas nas docstrings e comentários.
