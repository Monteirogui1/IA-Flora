import streamlit as st
import fitz
from PIL import Image
import pytesseract
import os
import io
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from functools import lru_cache

pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Configuração do título da aplicação
st.title("Frilog Chat - Flora")

# Inicialização do estado da sessão
if "model" not in st.session_state:
    st.session_state["model"] = "FloraTest:latest"

if "messages" not in st.session_state:
    st.session_state.messages = []


# Função para extrair texto de um PDF usando somente PyTesseract (baseada no código fornecido)
def extract_text_from_pdf(file_path):
    try:
        # Abrir o arquivo PDF
        documento = fitz.open(file_path)
        texto_completo = ""
        st.write(f"Processando {file_path} ({documento.page_count} páginas)")

        # Processar cada página
        for pagina_num in range(documento.page_count):
            st.write(f"Processando página {pagina_num + 1}...")
            # Carregar a página
            pagina = documento.load_page(pagina_num)

            # Converter a página em imagem com resolução ajustada
            pix = pagina.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72))
            img_data = pix.tobytes("png")

            # Converter pixmap para imagem PIL
            imagem = Image.open(io.BytesIO(img_data))

            # Converter para escala de cinza
            imagem_cinza = imagem.convert("L")

            # Extrair texto da imagem usando OCR
            texto_pagina = pytesseract.image_to_string(imagem_cinza, lang="por")
            texto_completo += f"\n--- Página {pagina_num + 1} ---\n{texto_pagina}\n"

        # Fechar o documento
        documento.close()

        if not texto_completo.strip():
            st.error(f"Nenhum texto extraído de {file_path}")
            return ""

        # Contar caracteres para depuração
        total_caracteres = len(texto_completo)
        total_caracteres_sem_espacos = len(texto_completo.replace(" ", "").replace("\n", ""))
        st.write(f"Total de caracteres (incluindo espaços e quebras de linha): {total_caracteres}")
        st.write(f"Total de caracteres (excluindo espaços e quebras de linha): {total_caracteres_sem_espacos}")

        return texto_completo

    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {file_path}")
        return ""
    except Exception as e:
        st.error(f"Erro ao processar {file_path}: {e}")
        return ""


# Carregamento de todos os PDFs no diretório e configuração do retriever
@st.cache_resource
def load_vectorstore():
    try:
        pdf_directory = "pdfs"  # Diretório contendo os PDFs
        if not os.path.exists(pdf_directory):
            raise ValueError(f"Diretório {pdf_directory} não encontrado.")

        # Lista para armazenar todos os documentos
        all_documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Tamanho otimizado do chunk
            chunk_overlap=200,  # Sobreposição para contexto
            add_start_index=True
        )

        # Iterar sobre todos os arquivos PDF no diretório
        pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith(".pdf")]
        if not pdf_files:
            raise ValueError(f"Nenhum arquivo PDF encontrado em {pdf_directory}.")

        for pdf_file in pdf_files:
            file_path = os.path.join(pdf_directory, pdf_file)
            st.write(f"Processando: {pdf_file}")  # Log para depuração
            text = extract_text_from_pdf(file_path)
            if text:
                st.write(f"Texto extraído de {pdf_file}: {len(text)} caracteres")
                chunks = text_splitter.split_text(text)
                documents = [
                    Document(page_content=chunk, metadata={"source": pdf_file})
                    for chunk in chunks
                ]
                all_documents.extend(documents)
            else:
                st.error(f"Falha ao extrair texto de {pdf_file}")

        if not all_documents:
            raise ValueError("Nenhum texto válido extraído dos PDFs.")

        # Criar vectorstore com ChromaDB
        embeddings = OllamaEmbeddings(model="FloraTest:latest")
        vectorstore = Chroma.from_documents(
            documents=all_documents,
            embedding=embeddings,
            collection_name="frilog_collection",  # Nome da coleção no ChromaDB
            persist_directory="chroma_db"  # Diretório para persistência (opcional)
        )
        # Persistir os dados (opcional, se quiser salvar no disco)
        vectorstore.persist()
        return vectorstore
    except Exception as e:
        st.error(f"Erro ao criar vectorstore: {e}")
        return None


vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_type="mmr")

# Configuração do modelo e cadeia LangChain
llm = ChatOllama(model="FloraTest:latest", temperature=0.1)


# Cache para respostas frequentes
@lru_cache(maxsize=100)
def cached_chain_invoke(question):
    return chain.invoke(question).content


# Prompt aprimorado com few-shot prompting
rag_template = """
Você é Flora, atendente da empresa Frilog. Sua tarefa é responder às perguntas dos funcionários de forma clara, concisa, foque em ser natural e humanizado, como um diálogo comum entre duas pessoas e baseada exclusivamente no contexto fornecido. 
Se a resposta não estiver no contexto, diga: "Não tenho informações suficientes para responder." Não Mencione o nome do arquivo PDF (disponível nos metadados) na resposta.
Leve em consideração também o histórico de mensagens da conversa com o usuário.
Responda sempre em português brasileiro.

Contexto Atual: {context}

Pergunta do Funcionário: {question}

Exemplos:
1. Pergunta: Qual é o prazo de entrega?
   Resposta: O prazo de entrega é de 3 a 5 dias úteis.
2. Pergunta: Como consultar o estoque?
   Resposta: Consulte o sistema interno na seção "Estoque" ou contate o supervisor.

Sua resposta:
"""

prompt = ChatPromptTemplate.from_template(rag_template)

chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
)

# Exibição do histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Como posso ajudar você hoje?"):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta da Flora
    with st.chat_message("assistant"):
        response = chain.invoke(prompt)
        st.markdown(response.content)
        # Adicionar resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response.content})