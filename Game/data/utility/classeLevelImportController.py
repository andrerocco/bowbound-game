from tkinter.filedialog import askopenfilename

from utility.staticTileMapUtility import TileMapUtility
from daos.LevelDAO import LevelDAO


class LevelImportController:
    def __init__(self, destination_json_name: str):
        self.__level_dao = LevelDAO(destination_json_name)
        
    def import_from_file_picker(self):
        file_path = askopenfilename(filetypes=[("Map Files", ".ods")])
        if file_path == '': # Quando o file picker é fechado sem selecionar um arquivos
            return False # Irá retornar False
        else:
            try:
                tile_map = TileMapUtility.import_map_from_ods(file_path)
                self.__level_dao.add_level(tile_map)
                return True # Se conseguiu importar, irá retornar True
            except Exception as e:
                raise e # Se houve erro ao importar, irá levantar a exceção
