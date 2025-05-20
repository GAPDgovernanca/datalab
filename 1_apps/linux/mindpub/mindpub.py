import warnings
import streamlit as st
import openai
import os
from ebooklib import epub
from bs4 import BeautifulSoup

# Suprime os warnings do ebooklib
warnings.filterwarnings("ignore", message="In the future version we will turn default option ignore_ncx to True.", module="ebooklib.epub")
warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib.epub")

# Define a chave de API da OpenAI a partir da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- FUNÇÕES AUXILIARES ---

def extrair_texto_capitulo(epub_path, chapter_id):
    """Extrai o texto de um capítulo de um arquivo EPUB."""
    try:
        book = epub.read_epub(epub_path)
        chapter = book.get_item_with_id(chapter_id)
        if chapter:
            soup = BeautifulSoup(chapter.get_content(), 'html.parser')
            return soup.get_text()
        return "Capítulo não encontrado."
    except Exception as e:
        return f"Erro: {e}"

def resumir_e_formatar(texto, formato_saida="markdown"):
    """
    Resume o texto, gera um mapa mental e formata a saída.
    Para cada parágrafo, envia uma requisição à API da OpenAI.
    """
    paragrafos = [p.strip() for p in texto.split('\n\n') if p.strip()]
    resumos_paragrafos = []
    max_chars = 3000  # Limite de caracteres para evitar requisições muito grandes

    for paragrafo in paragrafos:
        # Trunca parágrafos muito longos
        if len(paragrafo) > max_chars:
            paragrafo = paragrafo[:max_chars]
        try:
            prompt = f"""
Você é um assistente especialista em criar mapas mentais claros, concisos e bem organizados.
Sua tarefa é resumir o parágrafo abaixo e estruturar as informações em um mapa mental hierárquico.

Instruções:
- Seja breve e direto, destacando os pontos principais.
- Utilize cabeçalhos Markdown para indicar a hierarquia (use '##', '###', '####', etc.; não utilize '#').
- Destaque takeaways, insights e conclusões de forma sucinta.
- Formate a saída em {formato_saida}.

Parágrafo:
{paragrafo}
            """
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um assistente prestativo."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=768,
                temperature=0.5,
                top_p=0.9,
            )
            resumo = response.choices[0].message.content
            resumos_paragrafos.append(resumo)
        except Exception as e:
            resumos_paragrafos.append(f"Erro ao processar o parágrafo: {e}")

    if formato_saida == "markdown":
        return "\n\n".join(resumos_paragrafos)
    else:
        texto_puro = ""
        for resumo in resumos_paragrafos:
            for linha in resumo.splitlines():
                linha = linha.lstrip('# ')
                nivel = linha.count('#')
                linha = linha.lstrip('#')
                indentacao = "    " * nivel
                texto_puro += indentacao + linha.strip() + "\n"
        return texto_puro

# --- INTERFACE STREAMLIT ---

st.sidebar.title("Menu")
modo = st.sidebar.radio("Selecione o modo:", ("Sumarizador de Livros EPUB com Mapa Mental", "Janela de Conversação"))

if modo == "Sumarizador de Livros EPUB com Mapa Mental":
    st.title("Sumarizador de Livros EPUB com Mapa Mental")
    
    uploaded_file = st.file_uploader("Escolha um arquivo EPUB", type="epub")
    
    if uploaded_file:
        epub_path = uploaded_file.name
        with open(epub_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
        if openai.api_key:
            try:
                book = epub.read_epub(epub_path)
                chapter_items = []
    
                def add_items(item):
                    # Tipo 9: capítulo
                    if item.get_type() == 9:
                        title = item.get_name()
                        if title.endswith(".xhtml") or title.endswith(".html"):
                            soup = BeautifulSoup(item.get_content(), 'html.parser')
                            heading = soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                            if heading:
                                title = heading.get_text()
                            else:
                                title = title.split('/')[-1].split('.')[0]
                        chapter_items.append((title, item.get_id()))
                    # Tipo 11: grupo de itens
                    if item.get_type() == 11:
                        for subitem in item.get_subitems():
                            add_items(subitem)
    
                for item in book.get_items():
                    add_items(item)
    
                chapter_options = [title for title, _ in chapter_items]
                selected_chapter_title = st.selectbox("Selecione o capítulo:", chapter_options)
                selected_chapter_id = next(chapter_id for title, chapter_id in chapter_items if title == selected_chapter_title)
    
                formato_saida = st.radio("Escolha o formato de saída:", ("markdown", "texto puro"), index=0)
    
                if st.button("Gerar Resumo e Mapa Mental"):
                    with st.spinner("Extraindo o capítulo..."):
                        texto_capitulo = extrair_texto_capitulo(epub_path, selected_chapter_id)
                    if texto_capitulo.startswith("Erro"):
                        st.error(texto_capitulo)
                    else:
                        with st.spinner("Resumindo e formatando..."):
                            resultado = resumir_e_formatar(texto_capitulo, formato_saida)
                        if resultado.startswith("Erro"):
                            st.error(resultado)
                        else:
                            st.subheader(f"Mapa Mental do Capítulo: {selected_chapter_title}")
                            if formato_saida == "markdown":
                                st.markdown(resultado)
                                st.subheader("Código Markdown:")
                                st.code(resultado, language="markdown")
                            else:
                                st.text(resultado)
                            # Armazena o resumo na sessão para usar no chat
                            st.session_state.summary = resultado
    
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.error("Defina a variável de ambiente OPENAI_API_KEY.")

elif modo == "Janela de Conversação":
    st.title("Janela de Conversação")
    
    # Inicializa o histórico com o resumo, se disponível
    if 'summary' in st.session_state and 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Você é um assistente prestativo."},
            {"role": "assistant", "content": st.session_state.summary}
        ]
    elif 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Você é um assistente prestativo."}]
    
    # Formulário para envio de mensagem
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Digite sua mensagem:")
        submit_button = st.form_submit_button(label="Enviar")
    
    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                max_tokens=150,
                temperature=0.7,
            )
            assistant_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Erro ao chamar a API: {e}"})
    
    # Exibe o histórico de mensagens
    st.markdown("### Histórico de Conversa")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Você:** {msg['content']}")
        else:
            st.markdown(f"**Assistente:** {msg['content']}")
