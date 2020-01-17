from enum import Enum

# состояния
class State(Enum):
    MENU = 0,
    START = 1,
    CONTINUE = 2,
    QUIT = 3


class GameState:
    def __init__(self):
        self.state = State.MENU

    def change(self, state):
        self.state = state

    def check(self, state):
        if self.state == state:
            return True
        return False
