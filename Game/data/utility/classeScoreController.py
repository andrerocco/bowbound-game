from daos.ScoreDAO import ScoreDAO
from typing import List

class ScoreController():
    def __init__(self):
        self.__scoreDAO = ScoreDAO()

    def add_score(self, level_name: str, player_name: str, time: float):
        self.__scoreDAO.add(level_name, player_name, time)

    def get_all_level_scores_sorted(self, level_name) -> List[tuple]:
        scores_level = self.__scoreDAO.get_level_scores(level_name)
        scores_level = sorted(scores_level.items(), key=lambda x:x[1])

        return self.__convert_time_format(scores_level) # Lista ordenada de tuplas do tipo (nome do jogador, tempo formatado), ordenada pelos tempos
    
    def get_best_level_score(self, level_name) -> tuple:
        scores_level = self.__scoreDAO.get_level_scores(level_name)
        best_score = min(scores_level.items(), key=lambda x:x[1])
        best_score = self.__convert_time_format([best_score])[0]
        
        return best_score # Tupla do tipo (nome do jogador, tempo formatado)

    def get_all_best_scores(self) -> dict:
        best_scores = {}
        for level_name, scores_dict in self.__scoreDAO.get_all_scores().items():
            best_scores[level_name] = self.get_best_level_score(level_name)
        
        return best_scores # Dicionario que tem como chave o nome dos níveis e como valor uma tupla do tipo (nome do jogador, tempo formatado)

    def __convert_time_format(self, scores_level: list):
        # Converte os floats com os segundos para uma string no formato min:seg.miliseg
        # Retorna uma lista de tuplas com os nomes dos jogadores e seus tempos convertidos

        formated_scores = []
        for name, time in scores_level:
            minutes, seconds = divmod(time, 60)
            formated_scores.append((name, "{:0>2}:{:05.2f}".format(int(minutes),seconds)))
        
        return formated_scores
