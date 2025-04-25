# README - Scraper de Ajustes da B3

## Descrição do Programa
Este programa é um web scraper desenvolvido em Python para extrair e processar dados da página de ajustes do pregão da B3 (Bolsa de Valores do Brasil). Ele utiliza a biblioteca Selenium para acessar, navegar e extrair informações diretamente da tabela contida no site da B3.

O objetivo é capturar os dados de ajustes do pregão, processá-los e salvá-los em um arquivo CSV para posterior análise.

## Estrutura e Fluxo do Programa

1. **Importação de bibliotecas**:
   - `re`, `time`, `csv`, `logging`: utilizadas para manipulação de strings, arquivos CSV e logging.
   - `selenium.webdriver` e seus módulos: usados para interagir com a página web da B3.

2. **Configuração do logging**:
   - O programa registra eventos importantes para facilitar o debug e monitoramento.

3. **Definição de funções auxiliares**:
   - `is_vencimento(text)`: Verifica se uma string representa um código de vencimento de contratos futuros.
   - `is_mercadoria(text)`: Determina se uma string representa uma mercadoria ou ativo financeiro.
   - `br_str_to_float(s)`: Converte valores numéricos do padrão brasileiro (com ponto como separador de milhar e vírgula como decimal) para float.
   - `format_float(value)`: Formata números float no padrão internacional, com separadores adequados.

4. **Função principal: `scrape_ajustes_b3(output_csv)`**:
   - Configura e inicia o driver do Selenium em modo headless (sem interface gráfica).
   - Acessa a URL da B3 e aguarda o carregamento do iframe que contém a tabela desejada.
   - Identifica e extrai o cabeçalho da tabela.
   - Processa as linhas da tabela, distinguindo entre mercadorias e vencimentos.
   - Converte e formata os valores monetários extraídos.
   - Salva os dados em um arquivo CSV com delimitador `;`.

5. **Finalização**:
   - Fecha o driver do Selenium e encerra o processo.

## Arquivo de Saída
O programa gera um arquivo CSV (padrão UTF-8) chamado `ajustes_b3.csv`, contendo as seguintes colunas:

- **Mercadoria**: Nome do ativo financeiro negociado.
- **Vencimento**: Código do vencimento do contrato.
- **Preço de ajuste anterior**: Preço do dia anterior.
- **Preço de ajuste atual**: Preço atualizado.
- **Variação**: Diferença entre o preço anterior e atual.
- **Valor do ajuste por contrato (R$)**: Ajuste financeiro por contrato.

## Dependências
Para executar o programa, é necessário instalar as seguintes bibliotecas:
```
pip install selenium
```

Além disso, é necessário ter o **Google Chrome** e o **Chromedriver** instalados e configurados corretamente.

## Execução
O programa pode ser executado diretamente via terminal:
```
python ajustes_b3.py
```
Ele irá gerar o arquivo `ajustes_b3.csv` com os dados extraídos da B3.

## Observações
- O scraper pode falhar caso a estrutura da página da B3 seja alterada.
- Ajustes podem ser necessários caso a formatação dos dados extraídos mude.

## Autor
Desenvolvido para coleta automática de dados financeiros na B3.