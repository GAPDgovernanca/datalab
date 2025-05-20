import requests

# Sua chave API (substitua se necessário)
API_KEY = "C4KAOTSAGOL2Y1DF"
BASE_URL = "https://www.alphavantage.co/query"

def symbol_search(keywords):
    """
    Realiza uma busca de ativos com base no termo informado.
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro na requisição:", response.status_code)
        return None

if __name__ == "__main__":
    termo_busca = input("Digite o termo de busca para o ativo: ")
    resultado = symbol_search(termo_busca)
    
    if resultado:
        print("\nResultados da busca:")
        # A resposta vem com a chave "bestMatches"
        for match in resultado.get("bestMatches", []):
            simbolo = match.get("1. symbol", "N/A")
            nome = match.get("2. name", "N/A")
            tipo = match.get("3. type", "N/A")
            regiao = match.get("4. region", "N/A")
            moeda = match.get("8. currency", "N/A")
            print(f"Símbolo: {simbolo} | Nome: {nome} | Tipo: {tipo} | Região: {regiao} | Moeda: {moeda}")
