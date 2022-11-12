from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self._game = game
        self.__prev_state = None

    @abstractmethod
    def update(self, delta_time, actions) -> None:
        # Irá implementar as atualizações dos elementos do estado
        # É possível entrar em outro estado dentro deste método
        # Deve-se importart o estado desejado, instanciar e chamar o método enter_state()
        pass

    @abstractmethod
    def render(self, display_surface) -> None:
        # Irá renderizar na tela os elementos atualizados em update()
        # Na maioria dos casos, deve-se limpar no início do método usando display_surface.fill((0, 0, 0)) 
        pass

    def enter_state(self):
        if len(self._game.state_stack) > 1:
            self.__prev_state = self.__game.state_stack[-1] # Salva o estado anterior em prev_state
        
        self._game.append_state(self) # Adiciona o estado atual na pilha de estados

    def exit_state(self):
        self._game.pop_state()
