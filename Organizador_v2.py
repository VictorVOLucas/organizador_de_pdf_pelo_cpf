import re
import PyPDF2
import os

def extract_cpf(text):
    # Define um padrão regex para identificar CPFs no texto
    cpf_pattern = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
    # Encontra todas as correspondências no texto
    matches = cpf_pattern.findall(text)
    return matches

def identify_header(page):
    # Extrai o texto da página e converte para minúsculas
    text = page.extract_text().lower()
    # Verifica se o texto contém a expressão 'aviso ferias'
    if 'aviso ferias' in text:
        return 'Aviso Ferias'
    # Verifica se o texto contém a expressão 'aviso de férias'
    elif 'aviso de férias' in text:
        return 'Aviso de Férias'
    else:
        return None

def organize_and_save_pdf(input_pdf_path):
    # Abre o arquivo PDF de entrada no modo de leitura binária
    with open(input_pdf_path, 'rb') as input_file:
        # Cria um leitor de PDF
        pdf_reader = PyPDF2.PdfReader(input_file)
        # Cria um escritor de PDF
        pdf_writer = PyPDF2.PdfWriter()

        # Dicionário para mapear CPFs para uma lista de páginas
        cpf_mapping = {}

        # Itera sobre as páginas do PDF
        for page_num in range(len(pdf_reader.pages)):
            # Obtém a página atual
            page = pdf_reader.pages[page_num]
            # Extrai o texto da página
            text = page.extract_text()
            # Encontra CPFs no texto
            cpf_list = extract_cpf(text)
            # Atualiza o mapeamento de CPFs para páginas
            for cpf in cpf_list:
                if cpf in cpf_mapping:
                    cpf_mapping[cpf].append(page_num)
                else:
                    cpf_mapping[cpf] = [page_num]

        # Conjunto de páginas não adicionadas ao PDF organizado
        not_added_pages = set(range(len(pdf_reader.pages)))

        # Adiciona as páginas organizadas ao escritor de PDF
        for cpf, pages in cpf_mapping.items():
            for page_num in pages:
                pdf_writer.add_page(pdf_reader.pages[page_num])
                not_added_pages.discard(page_num)

        # Define o caminho do arquivo de saída com base no nome do arquivo de entrada
        output_pdf_path = os.path.splitext(input_pdf_path)[0] + ".pdf"

        # Abre o arquivo de saída no modo de escrita binária
        with open(output_pdf_path, 'wb') as output_file:
            # Escreve o PDF organizado no arquivo de saída
            pdf_writer.write(output_file)

        # Exibe as páginas não adicionadas ao PDF organizado
        print("Páginas não adicionadas ao PDF organizado:")
        print(not_added_pages)

# Exemplo de uso
# Caminho do arquivo PDF de entrada
input_pdf_path = 'INSIRA AQUI O CAMINHO DO PDF'
# Organiza e salva o PDF
organize_and_save_pdf(input_pdf_path)
