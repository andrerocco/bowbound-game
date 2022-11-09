# Esse módulo deve ser usado para buscar arquivos cujo local não é fixo
# Sua implementação evita a necessidade de alterar o código caso o local do arquivo seja alterado

import os


""" 
Args:
    filename (str): Nome do arquivo a ser procurado
    path (str, optional): Diretório a ser procurado. Padrão: diretório atual

Returns:
    str: Caminho completo do arquivo encontrado
    None: Caso o arquivo não seja encontrado
"""

def find_file(filename: str, path: str = os.getcwd()):
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)

    return None
