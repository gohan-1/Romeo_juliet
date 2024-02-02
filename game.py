from enum import Enum
from deck import Deck
from helpers import green_text, text_with_blue_background, text_with_red_background
import sys

from player import Player, PlayerType
from position import Position


class TurnType(Enum):
    MOVE = 1
    SWAP = 2


class Game:
    def __init__(self, deck: Deck = None) -> None:
        self.MATRIX_SIZE = 7
        self.deck = deck or Deck()
        self.board = self.init_board()
        self.swap_queens()

        self.red_player = Player(PlayerType.RED, position=Position(6, 0))
        self.black_player = Player(PlayerType.BLACK, position=Position(0, 6))
        self.current_player = self.red_player

    def init_board(self):
        board = [[None]*self.MATRIX_SIZE for _ in range(self.MATRIX_SIZE)]
        x = 0
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                board[i][j] = self.deck.cards[x]
                x += 1
        return board

    def swap_queens(self):
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if self.board[i][j].is_heart_queen():
                    temp = self.board[0][self.MATRIX_SIZE-1]
                    self.board[0][self.MATRIX_SIZE-1] = self.board[i][j]
                    self.board[i][j] = temp
                elif self.board[i][j].is_spade_queen():
                    temp = self.board[self.MATRIX_SIZE-1][0]
                    self.board[self.MATRIX_SIZE-1][0] = self.board[i][j]
                    self.board[i][j] = temp

    def print_board(self):
        WIDTH = 3
        print("".center(WIDTH), end='')
        for i in range(self.MATRIX_SIZE):
            print(str(i+1).center(WIDTH), end='')
        for i in range(self.MATRIX_SIZE):
            print("\n")
            print(str(i+1).center(WIDTH), end='')
            for j in range(self.MATRIX_SIZE):
                card = self.board[i][j]
                card_text: str = str(self.board[i][j]).center(WIDTH)
                if card.is_joker():
                    card_text = green_text(card_text)
                elif card.is_heart_queen():
                    card_text = text_with_red_background(
                        card_text)
                elif card.is_spade_queen():
                    card_text = text_with_blue_background(
                        card_text)
                print(card_text, end='')
        print("\n")

    def play(self):
        while True:
            print(f'{self.current_player.name} turn')
            self.print_board()
            option = self.turn_prompt()
            if option == TurnType.MOVE:
                self.move()
            elif option == TurnType.SWAP:
                self.swap()

    def move(self):
        print('Please choose your desire position')
        possible_moves = self.list_possible_moves_for_current_player()
        for i, move in enumerate(possible_moves):
            print(f'{i+1}. {str(move)}')
        selected = int(input('Your option: '))
        self.update_current_player_position(possible_moves[selected-1])
        self.evaluate_current_player_position()
        self.update_counter()

    def list_possible_moves_for_current_player(self) -> list[Position]:
        position = self.current_player.position
        current_card = self.board[position.x][position.y]
        if current_card.is_red_numeral():
            pass
        elif current_card.is_black_numeral():
            pass
        elif current_card.is_joker():
            pass
        elif current_card.is_jack():
            pass
        elif current_card.is_king():
            pass
        return []

    def update_current_player_position(self, new_position):
        self.current_player.position = new_position

    def evaluate_current_player_position(self):
        # check if current player in winning position
        pass

    def update_counter(self):
        pass

    def setup_players(self):
        red_name = input("Red player's name: ")
        self.red_player.name = red_name
        black_name = input("Black player's name: ")
        self.black_player.name = black_name

    def swap(self):
        previous_swap_index = [[0, 6], [6, 0]]
        jokers = []
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if (self.board[i][j].is_joker() and [i, j] not in previous_swap_index):
                    jokers.append([i+1, j+1])

        print(f'You have {len(jokers)} jokers to swap whicher ')
        # joker = [joker for joker in jokers]
        for index, value in enumerate(jokers):
            print(f' {index+1} with position {value} ')
        selected_joker = int(input('choose one of the joker'))
        print('choose teh card')
        selected_joker_position = jokers[selected_joker - 1]

        selected_row = int(input(' choose the row value'))
        selected_column = int(input('choose the coumn value'))

        self.board[selected_joker_position[0] - 1][selected_joker_position[1] - 1], \
            self.board[selected_row - 1][selected_column - 1] = \
            self.board[selected_row - 1][selected_column - 1], \
            self.board[selected_joker_position[0] -
                       1][selected_joker_position[1] - 1]

        previous_swap_index = [[selected_row, selected_column], [
            selected_joker_position[0], [selected_joker_position[1]]]]

        print(previous_swap_index)

    def turn_prompt(self) -> TurnType:
        while True:
            print("What step would you take in this turn?")
            print('1. Move my Romeo')
            print('2. Swap the Joker')
            choice = int(input('Your choice: '))
            if choice == 1 or choice == 2:
                return TurnType(choice)
