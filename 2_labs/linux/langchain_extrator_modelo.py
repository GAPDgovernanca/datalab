import os
import json

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def main():
    # Lê a chave a partir da variável de ambiente
    chave_groq = os.environ.get("GROQ_API_KEY")

    # Caso a variável não esteja definida, avisamos e encerramos
    if not chave_groq:
        print("Erro: A variável de ambiente GROQ_API_KEY não está definida.")
        print("Por favor, defina GROQ_API_KEY antes de executar este script.")
        return

    # Inicializa o ChatGroq usando a chave obtida do ambiente
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

    # Define o parser de saída em JSON
    parser = JsonOutputParser(
        pydantic_object={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "features": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    )

    # Prompt com chaves escapadas
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Extraia os detalhes de um produto em formato JSON:
{{
  "name": "...",
  "price": 1234,
  "features": ["...", "...", "..."]
}}"""),
        ("user", "{input}")
    ])

    # Criação da "chain" (cadeia de execução)
    chain = prompt | llm | parser

    # Usuário digita a descrição do produto
    descricao = input("Descreva o produto: ").strip()
    try:
        resultado = chain.invoke({"input": descricao})
        print("\nResposta em JSON:")
        # ensure_ascii=False para manter acentuação legível
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro ao processar o texto com langchain-groq: {e}")

if __name__ == "__main__":
    main()
