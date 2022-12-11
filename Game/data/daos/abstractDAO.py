from abc import ABC
import json
class AbstractDAO(ABC):
    def __init__(self, cache: list or dict, datasource = ''):
        # O parâmetro cacha define se o DAO vai armazenar as informações em lista ou em dicionário
        # Deve ser passado ou um lista vazia [] ou um dicionário vazio {}
        self.datasource = datasource
        self._objectCache = cache

        try:
            self._load()
        except FileNotFoundError:
            self._dump()

    def _dump(self):
        json.dump(self._objectCache, open(self.datasource, 'w'))

    def _load(self):
        self._objectCache = json.load(open(self.datasource, 'r'))
