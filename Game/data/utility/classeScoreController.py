from utility.abstractScoreDAO import ScoreDAO

class ScoreController():
    def __init__(self):
        self.__scoreDAO = ScoreDAO()

    def add_score(self, level: int, nickname: str, time: float):
        self.__scoreDAO.add(level, nickname, time)

    def get_level_scores(self, level: int):
        scores = self.__scoreDAO.get_level(level)
        scores = self.__converte_tempo(sorted(scores.items(), key=lambda x:x[1]))
        return scores

    def get_all_scores(self):
        scores = {}
        for chave, valor in self.__scoreDAO.get_all().items():
            scores_level = self.__converte_tempo(sorted(valor.items(), key=lambda x:x[1]))
            scores[int(chave)] = scores_level
        
        return scores

    def __converte_tempo(self, scores_level: list):
        novo_tempos = []
        for score_level in scores_level:
            seg = score_level[1]
            miliseg = (seg - int(seg)) * 100
            min = 0
            while seg >= 60:
                seg -= 60
                min += 1

            if min <= 10:
                novo_tempos.append((score_level[0],f"0{min}:{int(seg)}:{miliseg:.0f}"))
            else:
                novo_tempos.append((score_level[0],f"{min}:{int(seg)}:{miliseg:.0f}"))

        return novo_tempos
