import fitz
import pytesseract
from PIL import Image
from PIL import ImageEnhance
import io
import os


def ler_pdf_com_ocr(caminho_arquivo):
    try:
        # Abrir o arquivo PDF
        documento = fitz.open(caminho_arquivo)
        num_paginas = documento.page_count
        print(f"O PDF tem {num_paginas} páginas.")

        texto_completo = ""
        # Processar cada página
        for pagina_num in range(num_paginas):
            print(f"Processando página {pagina_num + 1}...")
            # Carregar a página
            pagina = documento.load_page(pagina_num)

            # Converter a página em imagem (pixmap)
            pix = pagina.get_pixmap(matrix=fitz.Matrix(600/72, 600/72))
            img_data = pix.tobytes("png")

            # Converter pixmap para imagem PIL
            imagem = Image.open(io.BytesIO(img_data))

            # Converter para escala de cinza
            imagem_cinza = imagem.convert("L")



            # Extrair texto da imagem usando OCR com PSM
            texto_pagina = pytesseract.image_to_string(imagem_cinza, lang='por')
            texto_completo += f"\n--- Página {pagina_num + 1} ---\n{texto_pagina}\n"

        # Fechar o documento
        documento.close()

        # Contar caracteres
        total_caracteres = len(texto_completo)  # Inclui espaços e quebras de linha
        total_caracteres_sem_espacos = len(texto_completo.replace(" ", "").replace("\n", ""))

        print(f"Total de caracteres (incluindo espaços e quebras de linha): {total_caracteres}")
        print(f"Total de caracteres (excluindo espaços e quebras de linha): {total_caracteres_sem_espacos}")

        return texto_completo

    except FileNotFoundError:
        return "Arquivo não encontrado."
    except Exception as e:
        return f"Erro ao processar o PDF: {str(e)}"



# Exemplo de uso
caminho = "pdfs/NGR - TJ4.pdf"  # Substitua pelo caminho do seu PDF
texto = ler_pdf_com_ocr(caminho)
print(texto)

# Opcional: Salvar o texto em um arquivo
with open("saida_texto.txt", "w", encoding="utf-8") as arquivo_saida:
    arquivo_saida.write(texto)



# Total de caracteres (incluindo espaços e quebras de linha): 33432
# Total de caracteres (excluindo espaços e quebras de linha): 28231

# Total de caracteres (incluindo espaços e quebras de linha): 32378
# Total de caracteres (excluindo espaços e quebras de linha): 27089