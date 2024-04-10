from queue import PriorityQueue
from typing import Optional

from pygame import Color
from game import Game
from position import Position
from turn import Turn


class AStarPlayer:
    def make_decision(self, game: Game) -> Turn:
        frontier = PriorityQueue()
        start = game.current_player.position
        goal = game.get_winning_position()
        frontier.put(start, 0)
        came_from: dict[Position, Optional[Position]] = {}
        cost_so_far: dict[Position, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            possible_moves = game.generate_possible_moves()

            for move in possible_moves:
                new_cost = cost_so_far[current] + 1
                if move not in cost_so_far or new_cost < cost_so_far[move]:
                    cost_so_far[move] = new_cost
                    priority = new_cost + self.heuristic(move, goal)
                    frontier.put(move, priority)
                    came_from[move] = current

        return came_from, cost_so_far

    def heuristic(self, game: Game, current_player: Color) -> float:
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
