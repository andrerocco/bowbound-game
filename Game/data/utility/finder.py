# Esse módulo deve ser usado para buscar arquivos cujo local não é fixo
# Sua implementação evita a necessidade de alterar o código caso o local do arquivo seja alterado

import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def find_file(filename: str, initial_path: str = PROJECT_ROOT):
    """ 
    Args:
        filename (str): Nome do arquivo a ser procurado
        initial_path (str, optional): Diretório a ser procurado. Padrão: diretório atual

    Returns:
        str: Caminho completo do arquivo encontrado
        None: Caso o arquivo não seja encontrado
    """
    for root, dirs, files in os.walk(initial_path): # Percorre o diretório especificado em path e seus subdiretórios
        if filename in files:
            return os.path.join(root, filename) # Retorna o caminho completo do arquivo encontrado

    raise Exception(f"No file named {filename} found") # Caso o arquivo não seja encontrado


def path_list_from_folder(subdir: str, initial_path: str = PROJECT_ROOT, file_extension: str = '.*') -> list:
    """ 
    Args:
        subdir (str): Nome do subdiretório do qual os arquivos serão listados
        initial_path (str, optional): Diretório a ser procurado. Padrão: diretório atual
        file_extension (str, optional): Extensão dos arquivos a serem listados. Padrão: todos os arquivos

    Returns:
        list: Lista de caminhos completos dos arquivos encontrados
    """

    if initial_path is not os.getcwd():
        path = os.path.join(os.getcwd(), initial_path) # Conecta o diretório atual ao diretório passado como argumento
    else:
        path = initial_path

    for root, dirs, files in os.walk(path):
        if subdir in dirs:
            subdir_path = os.path.join(root, subdir)
    if not subdir_path:
        raise Exception(f"No folder named {subdir} found")
    
    files_in_subdir = [] # Armazenará os paths completos de todos os arquivos

    if file_extension != '.*':
        for file in os.listdir(subdir_path):
            if file.endswith(file_extension):
                files_in_subdir.append(os.path.join(subdir_path, file))
    else:
        for file in os.listdir(subdir_path):
            files_in_subdir.append(os.path.join(subdir_path, file))
    
    return files_in_subdir