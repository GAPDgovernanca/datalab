import re
import time
import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_vencimento(text):
    """
    Verifica se 'text' segue o padrão típico de vencimento da B3 (ex.: H25, J25, K25...).
    Ajuste conforme sua lista de códigos válidos.
    Exemplos:
      - H25, J25, K25, M25, N25, Q25, U25, V25, X25, Z25...
    """
    text = text.strip().upper()
    # Regex simples: 1 letra (entre H, J, K, M, N, Q, U, V, X, Z) + 2 dígitos
    return bool(re.match(r'^[HJKMNQUVXZ]\d{2}$', text))

def is_mercadoria(text):
    """
    Heurística simples para saber se o texto é (provavelmente) uma mercadoria.
    - Se contiver ' - ' (ex.: 'ABEVO - Contrato Futuro de ABEV3'), consideramos mercadoria
    - Se tiver mais de 5 caracteres e não for um vencimento, provavelmente é mercadoria
    - Ajuste conforme a realidade da B3 (alguns nomes podem ter números).
    """
    text = text.strip()
    if not text:
        return False
    if " - " in text:
        return True
    if len(text) > 5 and not is_vencimento(text):
        return True
    return False

def br_str_to_float(s):
    """
    Converte uma string numérica em notação pt-BR (ex.: "18.372,90") para float (ex.: 18372.90).
    Caso a string esteja vazia ou não seja possível converter, retorna None.
    """
    if not s:
        return None
    try:
        # Remove o separador de milhar (ponto) e substitui a vírgula pelo ponto decimal
        return float(s.replace('.', '').replace(',', '.'))
    except Exception as e:
        logging.error(f"Erro ao converter '{s}': {e}")
        return None

def format_float(value):
    """
    Recebe um valor float (ou None) e retorna string no formato en-US,
    com duas casas decimais e separador de milhar em vírgula. Ex.: 1107510.4 -> '1,107,510.40'
    Se for None ou string vazia, retorna string vazia.
    """
    if value is None or value == "":
        return ""
    try:
        val_float = float(value)
        return f"{val_float:,.2f}"
    except ValueError:
        # Se não conseguir converter, devolve como string original
        return str(value)

def scrape_ajustes_b3(output_csv="ajustes_b3.csv"):
    logging.info("Iniciando o scraper de ajustes da B3")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # Ajuste conforme seu sistema
    options.binary_location = "/usr/bin/chromium-browser"

    try:
        logging.info("Iniciando o driver do Selenium")
        driver = webdriver.Chrome(options=options)
        
        url = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/derivativos/ajustes-do-pregao/"
        logging.info(f"Acessando a URL: {url}")
        driver.get(url)
        
        logging.info("Aguardando o carregamento do iframe")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        logging.info("Iframe encontrado. Mudando para o contexto do iframe")
        driver.switch_to.frame(iframe)
        
        logging.info("Aguardando a presença da tabela dentro do iframe")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        table = driver.find_element(By.TAG_NAME, "table")
        logging.info("Tabela encontrada. Extraindo linhas")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        logging.info("Extraindo cabeçalho da tabela")
        header_cols = []
        thead = table.find_elements(By.TAG_NAME, "thead")
        if thead:
            header_row = thead[0].find_elements(By.TAG_NAME, "tr")[0]
            header_cols = [col.text.strip() for col in header_row.find_elements(By.TAG_NAME, "th")]
        else:
            header_cols = [col.text.strip() for col in rows[0].find_elements(By.TAG_NAME, "th")]
            if not header_cols:
                header_cols = [col.text.strip() for col in rows[0].find_elements(By.TAG_NAME, "td")]

        # Se não achou cabeçalho ou não é confiável, define manualmente
        if not header_cols or len(header_cols) < 6:
            logging.info("Cabeçalho insuficiente encontrado. Definindo cabeçalho padrão.")
            header_cols = [
                "Mercadoria",
                "Vencimento",
                "Preço de ajuste anterior",
                "Preço de ajuste atual",
                "Variação",
                "Valor do ajuste por contrato (R$)"
            ]
        logging.info(f"Cabeçalho definido: {header_cols}")
        
        table_data = []
        current_mercadoria = None

        # Iniciamos a leitura a partir da segunda linha, caso a primeira seja cabeçalho
        start_index = 1 if len(rows) > 1 else 0
        logging.info("Iniciando extração das linhas de dados")

        for idx, row in enumerate(rows[start_index:], start=start_index):
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 2:
                logging.debug(f"Linha {idx} ignorada por ter colunas insuficientes")
                continue

            col0 = cols[0].text.strip()
            col1 = cols[1].text.strip() if len(cols) > 1 else ""
            col2 = cols[2].text.strip() if len(cols) > 2 else ""
            col3 = cols[3].text.strip() if len(cols) > 3 else ""
            col4 = cols[4].text.strip() if len(cols) > 4 else ""
            col5 = cols[5].text.strip() if len(cols) > 5 else ""

            # Decidir se col0 é mercadoria ou vencimento
            if is_mercadoria(col0):
                # col0 = mercadoria, col1 = vencimento
                current_mercadoria = col0
                mercadoria_text = col0
                vencimento_text = col1
                preco_ajuste_anterior = col2
                preco_ajuste_atual = col3
                variacao = col4
                ajuste_por_contrato = col5

            elif is_vencimento(col0):
                # col0 = vencimento, col1 = preco_ajuste_anterior...
                mercadoria_text = current_mercadoria
                vencimento_text = col0
                preco_ajuste_anterior = col1
                preco_ajuste_atual = col2
                variacao = col3
                ajuste_por_contrato = col4

            else:
                # Pode ser que col0 esteja vazio (por conta de rowspan) ou algo não detectado
                # Verificamos se col1 é um vencimento
                if not col0 and is_vencimento(col1):
                    # Então col1 = vencimento
                    mercadoria_text = current_mercadoria
                    vencimento_text = col1
                    preco_ajuste_anterior = col2
                    preco_ajuste_atual = col3
                    variacao = col4
                    ajuste_por_contrato = col5
                else:
                    # Caso especial: se não for mercadoria nem vencimento, provavelmente é lixo ou separador
                    logging.debug(f"Linha {idx} não se enquadra nos padrões de Mercadoria/Vencimento. Ignorada.")
                    continue

            # Converte e formata
            preco_ant_float = br_str_to_float(preco_ajuste_anterior)
            preco_at_float  = br_str_to_float(preco_ajuste_atual)
            variacao_float  = br_str_to_float(variacao)
            ajuste_float    = br_str_to_float(ajuste_por_contrato)

            preco_ant_str = format_float(preco_ant_float)
            preco_at_str  = format_float(preco_at_float)
            variacao_str  = format_float(variacao_float)
            ajuste_str    = format_float(ajuste_float)

            row_data = {
                header_cols[0]: mercadoria_text,
                header_cols[1]: vencimento_text,
                header_cols[2]: preco_ant_str,
                header_cols[3]: preco_at_str,
                header_cols[4]: variacao_str,
                header_cols[5]: ajuste_str
            }
            logging.info(f"Linha {idx} extraída: {row_data}")
            table_data.append(row_data)
        
        logging.info("Salvando os dados extraídos em CSV com delimitador ';'")
        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header_cols, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for row in table_data:
                writer.writerow(row)
        
        logging.info(f"Dados salvos com sucesso em: {output_csv}")

    except Exception as e:
        logging.error("Ocorreu um erro ao fazer o scraping", exc_info=True)
    finally:
        driver.quit()
        logging.info("Driver encerrado")

if __name__ == "__main__":
    scrape_ajustes_b3("ajustes_b3.csv")
