from calendar import c
from copy import deepcopy
from pygame import Color
from turtledemo.chaos import g
from game import Game
from turn import Turn


class AlphaBetaPruningPlayer:
    def make_decision(self, game: Game) -> Turn:

        _, move = self.alpha_beta_pruning(deepcopy(game), float('-inf'),
                                          float('inf'), 5, True, game.current_player.color)
        return move

    def alpha_beta_pruning(self, game: Game, alpha: float, beta: float, depth: int, is_maximizing: bool, current_player: Color):
        if depth == 0 or game.checking_winning_position():
            return self.evaluate(game, current_player), None
        move = None
        if is_maximizing:
            max_eval = float('-inf')
            possible_moves = game.generate_possible_moves()
            for move in possible_moves:
                print(game.current_player, move, 'is_maximizing', depth)
                game.make_move(move)
                eval, _ = self.alpha_beta_pruning(
                    game, alpha, beta, depth - 1, False, current_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                print('alpha', alpha,  move)
                game.undo_move()
                if alpha >= beta:
                    print('pruning', alpha, beta, eval, move)
                    # game.toggle_players()
                    break

            return max_eval, move
        else:
            min_eval = float('inf')
            possible_moves = game.generate_possible_moves()
            for move in possible_moves:
                print(game.current_player, move, 'is_minimizing', depth)

                game.make_move(move)
                eval, _ = self.alpha_beta_pruning(
                    game, alpha, beta, depth - 1, True, current_player)
                print(eval, 'eval')
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                print('beta', beta,  move)
                game.undo_move()

                if alpha >= beta:
                    print('pruning', alpha, beta, eval, move)
                    # game.toggle_players()
                    break
            return min_eval, move

    def evaluate(self, game: Game, current_player: Color) -> float:
        if game.checking_winning_position():
            # reversed as current player is toggled already
            if game.current_player.color == current_player:
                return -1
            else:
                return 1
        if game.red_player.color == current_player:
            print(game.red_player.position, game.BLACK_INITIAL_POSITION)
            return 1 - game.red_player.position.distance(game.RED_INITAL_POSTION)/72
        else:
            print(game.black_player.position, game.RED_INITAL_POSTION)
            return 1 - game.black_player.position.distance(game.RED_INITAL_POSTION)/72
