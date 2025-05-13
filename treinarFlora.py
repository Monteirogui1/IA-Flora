import fitz
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
import io
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Configuração do Tesseract
pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
TESSDATA_PATH = r'C:\Program Files\Tesseract-OCR\tessdata'
config_pytesseract = '--tessdata-dir tessdata -l por --oem 3 --psm 6'

# Função para extrair texto de um PDF usando PyTesseract
def extract_text_from_pdf(file_path):
    try:
        documento = fitz.open(file_path)
        texto_completo = ""
        print(f"Processando {file_path} ({documento.page_count} páginas)")

        for pagina_num in range(documento.page_count):
            print(f"Processando página {pagina_num + 1}...")
            pagina = documento.load_page(pagina_num)
            pix = pagina.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72))
            img_data = pix.tobytes("png")
            imagem = Image.open(io.BytesIO(img_data))
            imagem_cinza = imagem.convert("L")
            texto_pagina = pytesseract.image_to_string(imagem_cinza)
            texto_completo += f"\n--- Página {pagina_num + 1} ---\n{texto_pagina}\n"

        documento.close()

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
        pdf_directory = "pdfs"
        if not os.path.exists(pdf_directory):
            raise ValueError(f"Diretório {pdf_directory} não encontrado.")

        all_documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=500,
            add_start_index=True
        )

        pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith(".pdf")]
        if not pdf_files:
            raise ValueError(f"Nenhum arquivo PDF encontrado em {pdf_directory}.")

        for pdf_file in pdf_files:
            file_path = os.path.join(pdf_directory, pdf_file)
            print(f"Processando: {pdf_file}")
            text = extract_text_from_pdf(file_path)
            if text:
                print(f"Texto extraído de {pdf_file}: {len(text)} caracteres")
                chunks = text_splitter.split_text(text)
                documents = [
                    Document(page_content=chunk, metadata={"source": pdf_file})
                    for chunk in chunks
                ]
                all_documents.extend(documents)
            else:
                print(f"Falha ao extrair texto de {pdf_file}")

        if not all_documents:
            raise ValueError("Nenhum texto válido extraído dos PDFs.")

        embeddings = OllamaEmbeddings(model="FloraTest:latest")
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