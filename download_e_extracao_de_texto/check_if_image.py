import fitz
import pytesseract
from PIL import Image
import io
import os
import pickle
from tqdm import tqdm
import pandas as pd

def load_pickle(path):
  with open(path, 'rb') as handle:
    data = pickle.load(handle)
  return data

def save_data_to_pickle(data, path):
  with open (path, 'wb') as file:
    pickle.dump(data, file)

def extract_text_from_image_page(pdf_path, page_num):
    # Abre o arquivo PDF usando PyMuPDF
    pdf_document = fitz.open(pdf_path)
    
    # Carrega a página específica
    page = pdf_document.load_page(page_num)
    
    # Extrai a imagem da página
    pix = page.get_pixmap()
    
    # Converte a imagem para um objeto PIL
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    # Usa pytesseract para realizar OCR na imagem
    config = '--tessdata-dir assets/tessdata'
    # text = pytesseract.image_to_string(img, lang='por', config=config)
    text = pytesseract.image_to_string(img)
    
    return text


def extract_text(path):
  doc = fitz.open(path)
  text = ''
  for i, page in enumerate(doc):
    page_text = page.get_text()
    text += page_text
    
    if len(page_text) == 0:
      text += extract_text_from_image_page(path, i)
  return text

def generate_file_list(directory):
  file_list = []
  total_files = sum(len(files) for _, _, files in os.walk(directory))
  
  with tqdm(total=total_files, desc="Processing files") as pbar:
    for root, dirs, files in os.walk(directory):
      for file_name in files:
        file_path = os.path.join(root, file_name)
        subject = os.path.splitext(file_name)[0]  # Remove a extensão .pdf
        
        # Se o arquivo está diretamente em 'downloads', o assunto é o nome do arquivo sem extensão
        if root == directory:
          text = extract_text(file_path)
          file_list.append({'assunto': subject, 'text': text})
        # Se o arquivo está em uma subpasta, o assunto é o nome da pasta
        else:
          folder_name = os.path.basename(root)
          text = extract_text(file_path)
          file_list.append({'assunto': folder_name, 'text': text})
        
        pbar.update(1)

  return file_list

# extracted_text = generate_file_list('./downloads')
# df = pd.DataFrame(extracted_text)
# df.to_pickle('./pickles/data.pkl')


# print(df.head())

# data = load_pickle('./pickles/data.pkl')
# print(df.head())

print(extract_text('./downloads/aluna_gestante.pdf'))

# './downloads/aproveitamento_de_estudos.pdf'
# path = './downloads/aceleração_de_estudos.pdf'

