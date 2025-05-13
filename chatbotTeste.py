import streamlit as st
import fitz
from PIL import Image
import pytesseract
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
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

# Função para extrair texto de um PDF com PyMuPDF
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        st.write(f"Processando {file_path} ({len(doc)} páginas)")
        for i, page in enumerate(doc, 1):
            page_text = page.get_text()
            if page_text:
                text += page_text
                st.write(f"Página {i}: Texto extraído ({len(page_text)} caracteres)")
            else:
                st.warning(f"Página {i}: Nenhum texto extraível, tentando OCR")
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_text = pytesseract.image_to_string(img, lang="por")
                text += ocr_text
                st.write(f"Página {i}: OCR aplicado ({len(ocr_text)} caracteres)")
        doc.close()
        if not text:
            st.error(f"Nenhum texto extraído de {file_path}")
        return text
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
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

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
   Resposta: Conforme o documento NGR - TJ4.pdf, o prazo de entrega é de 3 a 5 dias úteis.
2. Pergunta: Como consultar o estoque?
   Resposta: Consulte o sistema interno na seção "Estoque" ou contate o supervisor (fonte: Manual Operacional.pdf).

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