import PyPDF2
import pandas as pd
import re
import os
import glob

def clean_text(text):
    return ''.join(c for c in text if c.isprintable())

def extract_references(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            references_text = ""
            found_references = False

            for page_num in range(num_pages - 1, -1, -1):
                page = reader.pages[page_num]
                text = page.extract_text()

                if "Referências" in text or "References" in text:
                    found_references = True
                    references_text = text.strip() + "\n" + references_text

                    for next_page_num in range(page_num + 1, num_pages):
                        page = reader.pages[next_page_num]
                        text = page.extract_text()
                        references_text += "\n" + text.strip()
                    break

            if not found_references:
                return f"Seção de referências não encontrada em {pdf_path}."

            lines = references_text.split("\n")
            references = []
            current_reference = ""

            for line in lines:
                line = line.strip()
                if re.match(r"^[A-Za-z]+,.*\(\d{4}\)", line):
                    if current_reference:
                        references.append(clean_text(current_reference.strip()))
                    current_reference = line
                elif re.match(r"^[A-Z]+,", line):
                    if current_reference:
                        references.append(clean_text(current_reference.strip()))
                    current_reference = line
                else:
                    current_reference += " " + line

            if current_reference:
                references.append(clean_text(current_reference.strip()))

            return references
    except Exception as e:
        return [f"Erro ao processar {pdf_path}: {str(e)}"]

def save_references_to_excel(references, pdf_path):
    try:
        df = pd.DataFrame({"Referências": references})
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_excel = f"Referencias-{base_name}.xlsx"
        counter = 1
        
        while os.path.exists(output_excel):
            output_excel = f"Referencias-{base_name}_{counter}.xlsx"
            counter += 1
        
        df.to_excel(output_excel, index=False)
        return f"Referências salvas em {output_excel}"
    except Exception as e:
        return f"Erro ao salvar referências no Excel: {str(e)}"

def listar_referencias(folder_path):
    messages = []
    try:
        pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
        for pdf_path in pdf_files:
            try:
                references = extract_references(pdf_path)
                if isinstance(references, list) and references:
                    message = save_references_to_excel(references, pdf_path)
                    messages.append(message)
                else:
                    messages.append(references)
            except Exception as e:
                messages.append(f"Erro ao processar {pdf_path}: {str(e)}")
    except Exception as e:
        messages.append(f"Erro ao acessar a pasta: {str(e)}")
    return messages
