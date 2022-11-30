import json


class ScoreDAO():
    def __init__(self, datasource = 'scores.json'):
        self.__datasource = datasource
        self.__objectCache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        json.dump(self.__objectCache, open(self.__datasource, 'w'))

    def __load(self):
        self.__objectCache = json.load(open(self.__datasource, 'r'))

    def add(self, level: int, nickname: str, time: float):
        level = str(level)
        if level in self.__objectCache: # Verifica se o level ja foi adicionado
            if nickname in self.__objectCache[level]: # Verifica se o nickname ja foi adicionado
                if time < self.__objectCache[level][nickname]: # Se o tempo for menor que o registrado armazena o novo tempo
                    self.__objectCache[level][nickname] = time
            else:
                if len(self.__objectCache[level]) == 50: # Se não tiver o nome e tiver 50 nomes
                    if time < max(self.__objectCache[level].values()): # Verifica se o tempo é menor do que o maior tempo do level
                        nickname_toremove = sorted(self.__objectCache[level], key = self.__objectCache[level].get)[-1]
                        self.__objectCache[level].pop(nickname_toremove) # Remove o nickname com o menor tempo
                        self.__objectCache[level][nickname] = time
                else:
                    self.__objectCache[level][nickname] = time
        else:
            self.__objectCache[level] = {nickname: time} # Se não, adiciona uma lista com a tupla com o dados

        self.__dump()


    def get_level(self, level: int):
        level = str(level)
        return self.__objectCache[level]

    def get_all(self):
        return self.__objectCache