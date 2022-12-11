from daos.abstractDAO import AbstractDAO
from daos.exceptions.NivelJaExisteException import NivelJaExisteException
from daos.exceptions.NivelNaoExisteException import NivelNaoExisteException
from utility.staticTileMapUtility import TileMapUtility
import os
from utility.finder import find_file


class LevelDAO(AbstractDAO):
    def __init__(self, filename):
        try:
            datasource = find_file(filename) # Verifica se o arquivo com o nome passado existe
        except:
            # Volta duas pastas (daos, data) e acessa a pasta maps para criar o arquivo
            datasource = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'maps', filename)
        
        super().__init__(cache=[], datasource=datasource)

    def add_level(self, level_dict: dict):
        # Confere se level_dict tem uma chave 'level_name'
        if 'level_name' not in level_dict:
            raise Exception("The key 'level_name' containing the level name was not found in the 'level_dict' parameter.")

        # Confere se já existe algum nível com o nome 'level_name' 
        existing_level_names = [level['level_name'] for level in self._objectCache]
        if level_dict['level_name'] in existing_level_names:
            raise NivelJaExisteException("A level with the name '{}' already exists in the selected datasource.".format(level_dict['level_name']))

        # Tenta fazer a conversão do nível (a validação das informações específicas de criação de nível são conferidas)
        try:
            converted_dict = TileMapUtility.convert(level_dict)
        except Exception as error:
            raise error

        self._objectCache.append(converted_dict)
        self._dump()

    def remove_level_by_name(self, level_name: str) -> dict:
        # Busca o nível com o nome passado e, se encontrado, o remove do cache e do arquivo
        # Se for encontrado, retorna o nível removido
        for i, level in enumerate(self._objectCache, start=0):
            if level['level_name'] == level_name:
                removed_level = self._objectCache.pop(i)
                self._dump()
                return removed_level
        
        raise NivelNaoExisteException(f"Level with name {level_name} doesn't exist.")

    # Getters
    def get_level_names(self):
        return [x['level_name'] for x in self._objectCache]

    def get_level(self, level_name):
        for i, level in enumerate(self._objectCache, start=0):
            if level['level_name'] == level_name:
                return self._objectCache[i]
        
        raise NivelNaoExisteException(f"Level with name {level_name} doesn't exist.")
