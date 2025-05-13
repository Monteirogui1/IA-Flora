import os
from docling.document_converter import DocumentConverter

# Diretórios de entrada e saída
source_dir = "pdfs"
output_dir = "docs"

# Criar o diretório de saída, se não existir
os.makedirs(output_dir, exist_ok=True)

# Inicializa o conversor
converter = DocumentConverter()

# Percorre os PDFs
for filename in os.listdir(source_dir):
    if filename.lower().endswith(".pdf"):
        source_path = os.path.join(source_dir, filename)
        output_filename = os.path.splitext(filename)[0] + ".md"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Convertendo: {filename}")
        try:
            result = converter.convert(source_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.document.export_to_markdown())
            print(f"✅ Salvo em: {output_path}")
        except Exception as e:
            print(f"❌ Erro ao converter {filename}: {e}")
