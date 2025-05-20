import re
import streamlit as st
from groq import Groq

# Configura o cliente Groq utilizando a chave armazenada nos secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

def query_groq(data_json: dict, question: str, model_name: str = "deepseek-r1-distill-llama-70b") -> str:
    """
    Processa uma consulta utilizando a API GROQ.
    Monta o prompt com informações do dataset e da query do usuário,
    e retorna a resposta da LLM.
    """
    try:
        prompt = f"""
        # Você é um especialista em gestão de frota de maquinário agrícola, com foco em análise financeira dos valores dos orçamentos e custos realizados e cálculos de eficiência operacional.
        ## Sua única habilidade é explicar as relações existentes entre valores orçados e valores realizados, apresentando os resulatdos dos seus cálculos de forma clara e objetiva.
        
        ---

        # Regras para Representação Numérica

        1. Acima de 1.000: arredondar para a centena mais próxima (ex.: 12.345 → 12.300)
        2. Abaixo de 1.000: arredondar para a dezena mais próxima (ex.: 545 → 550)
        3. Manter consistência em tabelas
        4. Evitar casas decimais desnecessárias

        ---

        # Estrutura da Resposta

        1. Conclusão Principal
        2. Cálculos de Suporte
        3. Tabelas

        ---

        # Cálculos Principais

        1. Diferença Absoluta
          Δ = (Valor_Orcado) - (Valor_Realizado)

        2. Desvio Percentual
          Δ% = ((Valor_Orcado) - (Valor_Realizado)) / (Valor_Orcado) x 100

        3. Taxa de Utilização
          U = Uso_Realizado / Uso_Estimado  (se Uso_Estimado = 0, então U = 0.0)
          U > 1.0 → Superutilização
          U < 1.0 → Subutilização

        ---

        # Tabelas do Banco de Dados

        1. dim_equipamento (Equipamentos)
          id_equipamento, modelo, usuario, classe, data_criacao

        2. fato_uso (Uso)
          id_equipamento, uso_estimado, uso_realizado, uso_diferenca, data_referencia

        3. fato_custo (Custo)
          id_equipamento, custo_hora_estimado, custo_hora_realizado, total_estimado, total_realizado, data_referencia

        4. fato_combustivel (Combustível)
          id_equipamento, comb_litros_estimado, comb_litros_realizado, comb_valor_unitario_estimado, comb_valor_unitario_realizado, comb_total_estimado, comb_total_realizado

        5. fato_manutencao (Manutenção)
          id_equipamento, lubrificantes, filtros, graxas, pecas_servicos (estimado/realizado)

        6. fato_reforma (Reforma)
          id_equipamento, reforma_estimado, reforma_realizado, data_referencia

        ---

        # Relacionamentos

        - Todas as tabelas de fatos do Banco de Dados se conectam à tabela dim_equipamento via id_equipamento.

        ---

        **Dataset Provided:**
        ```json
        {data_json}
        ```

        **User Query:**
        ```text
        {question}
        ```
        """
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly specialized assistant."},
                {"role": "user", "content": prompt}
            ],
            model=model_name,
        )
        response = chat_completion.choices[0].message.content

        # Remove trechos de raciocínio interno (ex.: <think>...</think>)
        if "<think>" in response and "</think>" in response:
            cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        else:
            cleaned_response = response

        return cleaned_response
    except Exception as e:
        st.error(f"Erro ao comunicar com a API GROQ: {e}")
        return "Erro ao processar a consulta."
