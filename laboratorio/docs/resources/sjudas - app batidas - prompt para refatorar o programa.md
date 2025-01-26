# Instruções para Refatoração do Código em Estrutura Modular

Você é uma LLM especializada em desenvolvimento Python. Sua tarefa é refatorar um programa Streamlit de análise de dados em uma estrutura modular. O trabalho será dividido em etapas, e você deve aguardar feedback após cada uma.

## Estrutura de Arquivos Final Desejada
```plaintext
app/
├── config.yaml              # Arquivo de configuração existente
├── __init__.py             # Torna o diretório um pacote Python
├── main.py                 # Novo arquivo principal
├── utils/
│   ├── __init__.py        # Torna utils um pacote
│   ├── config.py          # Gerenciamento de configuração
│   └── helpers.py         # Funções auxiliares
├── modules/
│   ├── __init__.py        # Torna modules um pacote
│   ├── data_processor.py  # Processamento de dados
│   ├── filter_manager.py  # Gerenciamento de filtros
│   └── visualizer.py      # Visualização e exportação
```

## Etapa 1: Setup Inicial e Módulo de Configuração

### 1.1 Criar Estrutura de Diretórios
```bash
mkdir -p app/utils app/modules
touch app/__init__.py
touch app/utils/__init__.py
touch app/modules/__init__.py
```

### 1.2 Implementar utils/config.py
Desenvolver gerenciador de configuração que:
- Carrega config.yaml
- Fornece acesso global à configuração
- Valida estrutura da configuração

Exemplo esperado:
```python
# app/utils/config.py
import yaml
import os
from typing import Dict, Any

class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self) -> None:
        """Carrega configurações do YAML"""
        pass  # Implementar carregamento
    
    @property
    def config(self) -> Dict[str, Any]:
        return self._config
```

### 1.3 Implementar utils/helpers.py
Mover funções auxiliares que são usadas em múltiplos módulos.

Entregáveis da Etapa 1:
- Estrutura de diretórios completa
- utils/config.py implementado
- utils/helpers.py com funções auxiliares
- Testes de configuração

## Etapa 2: Módulo de Processamento de Dados

### 2.1 Implementar modules/data_processor.py
```python
# app/modules/data_processor.py
import pandas as pd
from typing import Optional, Tuple
from ..utils.config import ConfigManager

class DataProcessor:
    def __init__(self):
        self.config = ConfigManager().config
        
    def load_data(self, file) -> Optional[pd.DataFrame]:
        """Carrega e processa dados"""
        pass
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pré-processa dados"""
        pass
    
    def calculate_weighted_average(self, df: pd.DataFrame, weights: dict) -> pd.DataFrame:
        """Calcula médias ponderadas"""
        pass
```

Entregáveis da Etapa 2:
- Implementação completa de DataProcessor
- Testes unitários
- Documentação de uso
- Exemplos de processamento

## Etapa 3: Módulo de Gerenciamento de Filtros

### 3.1 Implementar modules/filter_manager.py
```python
# app/modules/filter_manager.py
import streamlit as st
import pandas as pd
from typing import Dict, List
from ..utils.config import ConfigManager

class FilterManager:
    def __init__(self):
        self.config = ConfigManager().config
        self.initialize_session_state()
    
    def initialize_session_state(self) -> None:
        """Inicializa estado do Streamlit"""
        pass
    
    def create_filters(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Cria filtros interativos"""
        pass
```

Entregáveis da Etapa 3:
- Implementação completa de FilterManager
- Gerenciamento de estado do Streamlit
- Documentação dos filtros
- Exemplos de uso

## Etapa 4: Módulo de Visualização

### 4.1 Implementar modules/visualizer.py
```python
# app/modules/visualizer.py
import streamlit as st
import matplotlib.pyplot as plt
from typing import Any, Dict
from ..utils.config import ConfigManager

class Visualizer:
    def __init__(self):
        self.config = ConfigManager().config
    
    def create_histogram(self, data: Dict[str, Any]) -> plt.Figure:
        """Cria histograma"""
        pass
    
    def save_outputs(self, data: Dict[str, Any]) -> None:
        """Prepara downloads"""
        pass
```

Entregáveis da Etapa 4:
- Implementação completa de Visualizer
- Funções de exportação
- Documentação de estilos
- Exemplos de visualizações

## Etapa 5: Integração e Arquivo Principal

### 5.1 Implementar main.py
```python
# app/main.py
import streamlit as st
from utils.config import ConfigManager
from modules.data_processor import DataProcessor
from modules.filter_manager import FilterManager
from modules.visualizer import Visualizer

def main():
    """Função principal da aplicação"""
    config = ConfigManager().config
    
    # Inicializar componentes
    data_processor = DataProcessor()
    filter_manager = FilterManager()
    visualizer = Visualizer()
    
    # Interface principal
    st.title(config["ui"]["page_title"])
    
    # ... resto da implementação
```

Entregáveis da Etapa 5:
- Implementação completa de main.py
- Integração de todos os módulos
- Testes de integração
- Documentação do fluxo completo

## Para Cada Etapa

1. **Antes de Implementar**:
   - Revise o código atual
   - Identifique dependências
   - Liste funções a mover
   - Planeje testes

2. **Durante a Implementação**:
   - Siga PEP 8
   - Use type hints
   - Adicione docstrings
   - Mantenha funcionalidade

3. **Após Implementar**:
   - Teste funcionalidade
   - Verifique integração
   - Documente uso
   - Liste melhorias

## Formato de Resposta para Cada Etapa

```markdown
# Implementação da Etapa X

## Análise
- Funções identificadas
- Dependências necessárias
- Pontos de integração

## Implementação
[código completo dos arquivos]

## Documentação
- Explicação das mudanças
- Exemplos de uso
- Decisões de design

## Testes
- Testes implementados
- Resultados obtidos
- Pontos de atenção

## Próximos Passos
- Sugestões de melhoria
- Dependências para próxima etapa
```

Aguarde feedback após cada etapa antes de prosseguir. Está pronto para começar com a Etapa 1?