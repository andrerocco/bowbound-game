from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self._game = game
        self.__prev_state = None

    @abstractmethod
    def update(self, delta_time, actions) -> None:
        # Irá implementar as atualizações dos elementos do estado
        pass

    @abstractmethod
    def render(self, display_surface) -> None:
        # Irá renderizar na tela os elementos atualizados em update()
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.__prev_state = self.__game.state_stack[-1]
        self.__game.append_state(self)

    def exit_state(self):
        self.__game.pop_state()
