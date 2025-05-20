MINDPUB.PY

# Descrição do Programa

Este programa é uma aplicação web desenvolvida em Python utilizando o framework Streamlit, a biblioteca EbookLib para manipulação de arquivos EPUB, BeautifulSoup para análise e extração de conteúdo HTML, e a API GPT-4 da OpenAI para realizar sumarização avançada e geração de mapas mentais estruturados.

# Objetivo do Programa

O objetivo principal do programa é permitir que o usuário faça o upload de livros no formato EPUB, selecione um capítulo específico e obtenha automaticamente um resumo detalhado em formato de mapa mental estruturado. Esse resumo é gerado por meio de inteligência artificial utilizando o modelo GPT-4 da OpenAI.

# Funcionalidades

- Upload de livros EPUB através da interface.
- Identificação automática e seleção dos capítulos disponíveis no livro.
- Extração e processamento do texto do capítulo selecionado.
- Geração de resumos organizados em formato markdown ou texto puro, estruturados como mapas mentais.
- Interface interativa para visualização dos resumos.
- Janela de conversação integrada, permitindo ao usuário interagir com a IA para discussões adicionais sobre o conteúdo resumido.

# Dependências

- Streamlit
- EbookLib
- BeautifulSoup4
- OpenAI

# Configuração necessária

- Uma chave API válida da OpenAI configurada como variável de ambiente (`OPENAI_API_KEY`).

# Instruções de Uso

1. Execute o aplicativo com o comando `streamlit run mindpub.py`.
2. Utilize o menu lateral para selecionar entre o modo de sumarização ou a janela de conversação.
3. No modo sumarizador, faça upload do arquivo EPUB e escolha o capítulo desejado.
4. Clique em "Gerar Resumo e Mapa Mental" para obter o resultado.

Este programa é especialmente útil para leitores que buscam otimizar seu aprendizado e compreensão através da rápida absorção de conteúdos complexos de livros.