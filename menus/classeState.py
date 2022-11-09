class State:
    def __init__(self, game):
        self.__game = game
        self.__prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.__prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()
