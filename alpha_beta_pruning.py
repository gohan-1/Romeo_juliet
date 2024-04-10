from copy import deepcopy
from game import Game
from player import PlayerType
from turn import Turn


class AlphaBetaPruningPlayer:
    def make_decision(self, game: Game) -> Turn:

        _, move = self.alpha_beta_pruning(deepcopy(game), float('-inf'),
                                          float('inf'), 5, True, game.current_player.color)
        return move

    def alpha_beta_pruning(self, game: Game, alpha: float, beta: float, depth: int, is_maximizing: bool, current_player: PlayerType):
        if depth == 0 or game.checking_winning_position():
            return self.evaluate(game, current_player), None
        move = None
        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            possible_moves = game.generate_possible_moves()
            for move in possible_moves:
                game.make_move(move)
                eval, _ = self.alpha_beta_pruning(
                    game, alpha, beta, depth - 1, False, current_player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                game.undo_move()
                if alpha >= beta:
                    break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            possible_moves = game.generate_possible_moves()
            for move in possible_moves:
                game.make_move(move)
                eval, _ = self.alpha_beta_pruning(
                    game, alpha, beta, depth - 1, True, current_player)
                if eval < min_eval:
                    best_move = move
                    min_eval = eval
                beta = min(beta, eval)
                game.undo_move()
                if alpha >= beta:
                    break
            return min_eval, best_move

    def evaluate(self, game: Game, current_player: PlayerType) -> float:
        if game.checking_winning_position():
            # reversed as current player is toggled already
            if game.current_player.color == current_player:
                return -1
            else:
                return 1
        if game.red_player.color == current_player:
            return 1 - game.red_player.position.distance(game.BLACK_INITIAL_POSITION)/72
        else:
            return 1 - game.black_player.position.distance(game.RED_INITAL_POSTION)/72
