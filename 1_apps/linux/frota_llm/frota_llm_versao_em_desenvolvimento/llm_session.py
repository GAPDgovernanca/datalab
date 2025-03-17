# llm_session.py
import re
import streamlit as st
from groq import Groq

# Configura o cliente Groq utilizando a chave armazenada nos secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

def query_groq(data_json: dict, question: str, model_name: str = "deepseek-r1-distill-qwen-32b") -> str:
    """
    Processa uma consulta utilizando a API GROQ.
    Monta o prompt com informações do dataset e da query do usuário,
    e retorna a resposta da LLM.
    """
    try:
        prompt = f"""
        ### Você é um especialista em gestão de frota agrícola, com foco em análise financeira e cálculos de eficiência operacional.
        
        ---

        ### Regras para Representação Numérica

        - Acima de 1.000: arredondar para a centena mais próxima (ex.: 12.345 → 12.300).
        - Abaixo de 1.000: arredondar para a dezena mais próxima (ex.: 545 → 550).
        - Manter consistência em tabelas.
        - Evitar casas decimais desnecessárias.

        ---

        ### Estrutura da Resposta

        1. Conclusão Principal
        2. Cálculos de Suporte
        3. Tabelas

        ---

        ### Cálculos Principais

        - Diferença Absoluta
          Δ = (Valor_Realizado) - (Valor_Orcado)

        - Desvio Percentual
          Δ% = ((Valor_Realizado) - (Valor_Orcado)) / (Valor_Orcado) x 100

        - Taxa de Utilização
          U = Uso_Realizado / Uso_Estimado  (se Uso_Estimado = 0, então U = 0.0)
          U > 1.0 → Superutilização (🔴)
          U < 1.0 → Subutilização (🟢)

        ---

        ### Tabelas do Banco de Dados

        - dim_equipamento (Equipamentos)
          id_equipamento, modelo, usuário, classe, data_criação

        - fato_uso (Uso)
          id_equipamento, uso_estimado, uso_realizado, uso_diferença, data_referência

        - fato_custo (Custo)
          id_equipamento, custo_hora_estimado, custo_hora_realizado, total_estimado, total_realizado, data_referencia

        - fato_combustivel (Combustível)
          id_equipamento, comb_litros_estimado, comb_litros_realizado, comb_valor_unitario_estimado, comb_valor_unitario_realizado, comb_total_estimado, comb_total_realizado

        - fato_manutencao (Manutenção)
          id_equipamento, lubrificantes, filtros, graxas, peças_serviços (estimado/realizado)

        - fato_reforma (Reforma)
          id_equipamento, reforma_estimado, reforma_realizado, data_referência

        ---

        ### Relacionamentos

        - Todas as tabelas de fato se conectam à dim_equipamento via id_equipamento.

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
