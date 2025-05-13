import os
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Função para extrair texto de um arquivo Markdown
def extract_text_from_md(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            texto_completo = file.read()
        print(f"Processando {file_path}")

        if not texto_completo.strip():
            print(f"Nenhum texto extraído de {file_path}")
            return ""

        total_caracteres = len(texto_completo)
        total_caracteres_sem_espacos = len(texto_completo.replace(" ", "").replace("\n", ""))
        print(f"Total de caracteres (incluindo espaços e quebras de linha): {total_caracteres}")
        print(f"Total de caracteres (excluindo espaços e quebras de linha): {total_caracteres_sem_espacos}")

        return texto_completo

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return ""
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return ""

# Função para criar e persistir o vectorstore
def create_vectorstore():
    try:
        md_directory = "docs"  # Diretório onde os arquivos .md estão
        if not os.path.exists(md_directory):
            raise ValueError(f"Diretório {md_directory} não encontrado.")

        all_documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=500,
            add_start_index=True
        )

        md_files = [f for f in os.listdir(md_directory) if f.lower().endswith(".md")]
        if not md_files:
            raise ValueError(f"Nenhum arquivo Markdown encontrado em {md_directory}.")

        for md_file in md_files:
            file_path = os.path.join(md_directory, md_file)
            print(f"Processando: {md_file}")
            text = extract_text_from_md(file_path)
            if text:
                print(f"Texto extraído de {md_file}: {len(text)} caracteres")
                chunks = text_splitter.split_text(text)
                documents = [
                    Document(page_content=chunk, metadata={"source": md_file})
                    for chunk in chunks
                ]
                all_documents.extend(documents)
            else:
                print(f"Falha ao extrair texto de {md_file}")

        if not all_documents:
            raise ValueError("Nenhum texto válido extraído dos arquivos Markdown.")

        embeddings = OllamaEmbeddings(model="FloraFrilog:latest", base_url="http://192.168.100.247:11434")
        vectorstore = Chroma.from_documents(
            documents=all_documents,
            embedding=embeddings,
            collection_name="frilog_collection",
            persist_directory="chroma_db"
        )

        print("Vectorstore criado e persistido com sucesso!")
        return vectorstore

    except Exception as e:
        print(f"Erro ao criar vectorstore: {e}")
        return None

if __name__ == "__main__":
    create_vectorstore()