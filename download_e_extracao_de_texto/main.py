import requests
from bs4 import BeautifulSoup
import os

import re

def convert_to_snake_case(input_string):
    # Remove pontuação
    input_string = re.sub(r'[^\w\s]', '', input_string)
    # Converte para minúsculas e substitui espaços por underscores
    snake_case_string = re.sub(r'\s+', '_', input_string.lower())
    # Adiciona a extensão .pdf no final
    return snake_case_string + '.pdf'

# URL do site que você quer acessar
url = "https://proeg.ufam.edu.br/normas-academicas/57-proeg/146-legislacao-e-normas.html"

# Função para fazer o download de um arquivo
def download_file(url, folder, file_name):
  # if url != '/estagio-curricular.html':
    local_filename = os.path.join(folder, url.split('/')[-1])
    if url.split('.')[-1] == 'pdf':
      local_filename = os.path.join(folder, convert_to_snake_case(file_name))
    else:
      print(file_name)
      print(local_filename + '\n')
    # with requests.get(url, stream=True) as r:
    #   r.raise_for_status()
    #   with open(local_filename, 'wb') as f:
    #     for chunk in r.iter_content(chunk_size=8192):
    #       f.write(chunk)
    return local_filename

# Função principal para obter os links e baixar os documentos
def main(url, download_folder="downloads"):
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    response.raise_for_status()  # Verifica se houve algum erro na requisição

    # Cria a pasta de downloads, se não existir
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Faz o parsing do conteúdo HTML com BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os links dentro da hierarquia especificada
    for table in soup.find_all('table'):
        for tbody in table.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                for td in tr.find_all('td'):
                    for span in td.find_all('span'):
                        for a in span.find_all('a'):
                            link = a.get('href')
                            if link:  # Verifica se o link existe
                                # print(a.text)
                                # print(f"Baixando {link}...\n")
                                
                                download_file(link, download_folder, a.text)

if __name__ == "__main__":
    main(url=url)
