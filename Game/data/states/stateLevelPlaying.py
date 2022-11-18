from states.abstractState import State


class LevelPlaying(State):
    def __init__(self, game):
        super().__init__(game)
        


    def update(self):
        ...

    def render(self):
        ...

    def set_level_score(self):
        ...

    def next_level(self):
        ...

    def restart_level(self):
        ...