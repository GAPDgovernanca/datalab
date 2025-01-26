# GAPD - Data Analysis Project

Este repositório contém os componentes principais do projeto GAPD, incluindo aplicações de análise de dados, notebooks, scripts de automação e documentação.

## Estrutura de Pastas

A estrutura de pastas atual do projeto é a seguinte:

```
GAPD
├── apps                # Aplicações principais do projeto
│   ├── ADheatmap       # Aplicação de heatmap
│   ├── frota           # Aplicação de gerenciamento de frotas
│   └── sjudas          # Aplicação de análise de batidas
├── laboratorio         # Scripts experimentais e protótipos
│   ├── config          # Arquivos de configuração
│   ├── dash            # Dashboards e relatórios
│   ├── data            # Dados brutos e processados
│   ├── docs            # Documentação adicional
│   └── notebooks       # Notebooks Jupyter para análise
├── GAPD.code-workspace # Arquivo de configuração do workspace do VSCode
├── README.md           # Documentação principal do repositório
└── requirements.txt    # Dependências do projeto
```

## Configuração do ambiente

1. Certifique-se de ter o Python 3.8+ instalado.

2. Crie um ambiente virtual usando o `virtualenvwrapper` e o comando `workon`:
   
   ```bash
   mkvirtualenv nome_do_ambiente
   workon nome_do_ambiente
   ```

3. Instale as dependências do projeto:
   
   ```bash
   pip install -r requirements.txt
   ```

## Como contribuir

1. Faça um fork do repositório.

2. Crie uma branch para suas mudanças:
   
   ```bash
   git checkout -b minha-nova-feature
   ```

3. Faça o commit das suas alterações:
   
   ```bash
   git commit -m "Descrição da nova feature"
   ```

4. Envie suas alterações:
   
   ```bash
   git push origin minha-nova-feature
   ```

5. Crie um Pull Request no repositório principal.

## Licença

Este projeto está licenciado sob a licença MIT.
# Testing credentials storage - successful
