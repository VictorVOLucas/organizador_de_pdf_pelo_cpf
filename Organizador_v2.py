import re
import PyPDF2
import os

def extract_cpf(text):
    cpf_pattern = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
    matches = cpf_pattern.findall(text)
    return matches

def identify_header(page):
    text = page.extract_text().lower()
    if 'aviso ferias' in text:
        return 'Aviso Ferias'
    elif 'aviso de férias' in text:
        return 'Aviso de Férias'
    else:
        return None

def organize_and_save_pdf(input_pdf_path):
    with open(input_pdf_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        cpf_mapping = {}  # Mapeia CPF para uma lista de páginas

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            cpf_list = extract_cpf(text)
            for cpf in cpf_list:
                if cpf in cpf_mapping:
                    cpf_mapping[cpf].append(page_num)
                else:
                    cpf_mapping[cpf] = [page_num]

        not_added_pages = set(range(len(pdf_reader.pages)))

        for cpf, pages in cpf_mapping.items():
            for page_num in pages:
                pdf_writer.add_page(pdf_reader.pages[page_num])
                not_added_pages.discard(page_num)

        output_pdf_path = os.path.splitext(input_pdf_path)[0]+".pdf"

        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        print("Páginas não adicionadas ao PDF organizado:")
        print(not_added_pages)

# Exemplo de uso
# input_pdf_path = 'Ferias Barricas  - ORIGINAL - Copia.pdf'
# organize_and_save_pdf(input_pdf_path)
