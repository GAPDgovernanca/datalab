import requests
import json
import matplotlib.pyplot as plt  # Opcional, para gráficos

API_KEY = "C4KAOTSAGOL2Y1DF"  # Sua chave da API
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol):
    """
    Busca os dados diários do ativo.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao acessar a API:", response.status_code)
        return None

def exibir_dados(data, num_dias=5):
    """
    Exibe os dados dos últimos num_dias.
    """
    time_series = data.get("Time Series (Daily)")
    if not time_series:
        print("Dados de 'Time Series (Daily)' não encontrados.")
        return

    # Ordena as datas de forma decrescente
    datas = sorted(time_series.keys(), reverse=True)
    print(f"Exibindo os dados dos últimos {num_dias} dias:")
    for date in datas[:num_dias]:
        dia = time_series[date]
        print(f"Data: {date}")
        print(f"  Abertura: {dia['1. open']}")
        print(f"  Máximo:   {dia['2. high']}")
        print(f"  Mínimo:   {dia['3. low']}")
        print(f"  Fechamento: {dia['4. close']}")
        print("-" * 30)

def plot_closing_prices(data):
    """
    Plota os preços de fechamento dos dados retornados pela API.
    """
    time_series = data.get("Time Series (Daily)")
    if not time_series:
        print("Dados de 'Time Series (Daily)' não encontrados.")
        return

    # Ordena as datas de forma crescente
    datas = sorted(time_series.keys())
    closing_prices = [float(time_series[date]['4. close']) for date in datas]

    plt.figure(figsize=(10, 5))
    plt.plot(datas, closing_prices, marker='o')
    plt.title("Preço de Fechamento Diário")
    plt.xlabel("Data")
    plt.ylabel("Preço")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Exemplo: Cotação da PETR4
    ativo = "PETR4.SA"  # Lembre de incluir o sufixo .SA para ativos brasileiros
    dados = get_stock_data(ativo)
    if dados:
        exibir_dados(dados)
        # Opcional: gerar gráfico
        plot_closing_prices(dados)
