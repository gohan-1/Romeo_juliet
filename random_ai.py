
import random
from game import Game
from turn import Turn


class RandomAIPlayer:
    def make_decision(self, game: Game) -> Turn:
        possible_moves = game.generate_possible_moves()
        choice = random.randint(0, len(possible_moves)-1)
        return possible_moves[choice]
