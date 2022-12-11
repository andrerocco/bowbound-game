from daos.abstractDAO import AbstractDAO

class ScoreDAO(AbstractDAO):
    def __init__(self, datasource='scores.json'):
        super().__init__(cache={}, datasource=datasource)

    def add(self, level_name: str, player_name: str, time: float):
        if level_name in self._objectCache.keys(): 
            if player_name in self._objectCache[level_name]:
                if time < self._objectCache[level_name][player_name]:
                    self._objectCache[level_name][player_name] = time
            else: # Se o nome do jogador não estiver no dicionário
                if len(self._objectCache[level_name]) >= 25: # Se o dicionário tiver com o máximo de nomes (25)
                    if time < max(self._objectCache[level_name].values()): # Se o tempo for menor do que o maior pior tempo do dicionário
                        player_name_to_remove = sorted(self._objectCache[level_name], key=self._objectCache[level_name].get)[-1] # Pega o nome do jogador com o maior tempo
                        self._objectCache[level_name].pop(player_name_to_remove) # Remove o nome do jogador com o maior tempo
                        self._objectCache[level_name][player_name] = time # Adiciona o novo nome do jogador com o novo tempo
                else:
                    self._objectCache[level_name][player_name] = time
        else:
            self._objectCache[level_name] = {player_name: time}

        self._dump()

    def get_level_scores(self, level_name):
        try:
            return self._objectCache[str(level_name)]
        except KeyError:
            return {}

    def get_all_scores(self):
        return self._objectCache