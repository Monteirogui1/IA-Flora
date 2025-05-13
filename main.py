import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from functools import lru_cache

# Configuração do título da aplicação
st.title("Frilog Chat - Flora")

# Inicialização do estado da sessão
if "model" not in st.session_state:
    st.session_state["model"] = "FloraTest:latest"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Carregamento do vectorstore persistido
@st.cache_resource
def load_vectorstore():
    try:
        embeddings = OllamaEmbeddings(model="FloraTest:latest")
        vectorstore = Chroma(
            collection_name="frilog_collection",
            embedding_function=embeddings,
            persist_directory="chroma_db"
        )
        return vectorstore
    except Exception as e:
        st.error(f"Erro ao carregar vectorstore: {e}")
        return None

vectorstore = load_vectorstore()
if vectorstore is None:
    st.stop()

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chain.invoke(prompt)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})