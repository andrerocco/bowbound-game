from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game, actions_dict: dict):
        self._game = game
        self.__prev_state = None

        self._actions = actions_dict

    @abstractmethod
    def update_actions(self, event):
        # Deve conferir o evento e possivelmente atualizar um atributo de ações
        pass

    @abstractmethod
    def update(self) -> None:
        # Irá implementar as atualizações dos elementos do estado
        # É possível entrar em outro estado dentro deste método
        # Deve-se importart o estado desejado, instanciar e chamar o método enter_state()
        pass

    @abstractmethod
    def render(self, display_surface) -> None:
        # Irá renderizar na tela os elementos atualizados em update()
        # Na maioria dos casos, deve-se limpar no início do método usando display_surface.fill((0, 0, 0)) 
        pass

    def restart_actions(self):
        # Essa função é chamada quando há uma troca estados (para não gerar conflitos) de inputs antigos
        # Reinicia o dicionário salvo em actions para False em todos seus valores
        for key in self._actions:
            self._actions[key] = False

    def enter_state(self):
        if len(self._game.state_stack) > 1:
            self.__prev_state = self._game.state_stack[-1] # Salva o estado anterior em prev_state
        
        self._game.append_state(self) # Adiciona o estado atual na pilha de estados

    def exit_state(self):
        self._game.pop_state()
