from enum import Enum
from deck import Deck
from helpers import green_text, text_with_blue_background, text_with_red_background

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
        self.previous_swap_index = [[0, 6], [6, 0]]

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

    def is_red(self):
        if self.current_player == self.red_player:
            return True
        else:
            return False

    def toggle_players(self):
        if (self.is_red()):
            self.current_player = self.black_player
        else:
            self.current_player = self.red_player

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
                if i == self.red_player.position.x and j == self.red_player.position.y:
                    card_text = text_with_red_background(card_text)
                elif i == self.black_player.position.x and j == self.black_player.position.y:
                    card_text = text_with_blue_background(card_text)
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
            self.toggle_players()

    def move(self):
        print('Please choose your desire position')
        possible_moves = self.list_possible_moves_for_current_player()
        for i, move in enumerate(possible_moves):
            print(f'{i+1}. {str(move)}')
        selected = int(input('Your option: '))
        while selected >= len(possible_moves):
            print('Invalid input, please choose listed option')
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
            return self.get_valid_jack_moves(position)
        elif current_card.is_king():
            return self.get_valid_king_moves(position)
        elif current_card.is_queen():
            return self.get_valid_king_moves(position)
        return []

    def get_valid_jack_moves(self, current_position) -> list[Position]:
        jack_moves = [(-1, 2), (1, 2), (2, 1), (2, -1),
                      (1, -2), (-1, -2), (-2, -1), (-2, 1)]
        valid_moves = []
        for move in jack_moves:
            new_x = current_position.x + move[0]
            new_y = current_position.y + move[1]
            if new_x >= 0 and new_x < self.MATRIX_SIZE and new_y >= 0 and new_y < self.MATRIX_SIZE:
                valid_moves.append(Position(new_x, new_y))
        return valid_moves

    def get_valid_king_moves(self, current_position) -> list[Position]:
        king_moves = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                      (1, 0), (1, -1), (0, -1), (-1, -1)]
        valid_moves = []
        for move in king_moves:
            new_x = current_position.x + move[0]
            new_y = current_position.y + move[1]
            if new_x >= 0 and new_x < self.MATRIX_SIZE and new_y >= 0 and new_y < self.MATRIX_SIZE:
                valid_moves.append(Position(new_x, new_y))
        return valid_moves

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
        jokers = []
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if (self.board[i][j].is_joker() and [i, j]):
                    jokers.append([i+1, j+1])

        print(f'You have {len(jokers)} jokers to swap which are given below  ')
        # joker = [joker for joker in jokers]
        for index, value in enumerate(jokers):
            print(f' {index+1} with position {value} ')
        selected_joker = int(input(' \n choose one of the joker'))
        print('Now select the card')
        selected_joker_position = jokers[selected_joker - 1]

        selected_value = input(
            ' \n please Enter the card value you want swap with: ')

        selected_suit = input(
            ' \n please Enter the suit you want swap with :').upper()

        if selected_value == 'a' or selected_value == 'A':
            card_value = 1
        elif selected_value == 'k' or selected_value == 'K':
            card_value = 13
        elif selected_value == 'j' or selected_value == 'J':
            card_value = 11
        elif 0 < int(selected_value) < 11:
            card_value = int(selected_value)
        else:
            print('Invalid card given please recheck it')

        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if self.board[i][j].suit == selected_suit and self.board[i][j].rank == card_value:
                    self.row_index = i
                    self.column_index = j

        # print(self.previous_swap_index[0])
        # print([selected_joker_position[0],selected_joker_position[1]])
        # print( self.previous_swap_index[0] == [selected_joker_position[0],selected_joker_position[1]] )

        print(self.row_index + 1, self.column_index+1)
        print(selected_joker_position[0], selected_joker_position[1])

        if [selected_joker_position[0], selected_joker_position[1]] in self.previous_swap_index or [self.row_index + 1, self.column_index + 1] in self.previous_swap_index:
            print(
                '************************************************************************')
            print(
                '* cards are used in previous swap, Please choose another cards to swap *')
            print(
                '************************************************************************')

        else:
            self.board[selected_joker_position[0] - 1][selected_joker_position[1] - 1], \
                self.board[self.row_index][self.column_index] = \
                self.board[self.row_index][self.column_index], \
                self.board[selected_joker_position[0] -
                           1][selected_joker_position[1] - 1]

        self.previous_swap_index = [[self.row_index + 1, self.column_index+1], [
            selected_joker_position[0], selected_joker_position[1]]]

    def turn_prompt(self) -> TurnType:
        while True:
            print("What step would you take in this turn?")
            print('1. Move my Romeo')
            print('2. Swap the Joker')
            choice = int(input('Your choice: '))
            if choice == 1 or choice == 2:
                return TurnType(choice)
