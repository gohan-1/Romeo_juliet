from enum import Enum
from card import Card
from deck import Deck
from helpers import get_int_input_option, green_text, purple_text, red_text, text_with_blue_background, text_with_red_background

from player import Player, PlayerType
from position import Position


class TurnType(Enum):
    MOVE = 1
    SWAP = 2


class Game:
    def __init__(self, deck: Deck = None) -> None:
        self.MATRIX_SIZE = 7
        self.RED_INITAL_POSTION = Position(6, 0)
        self.BLACK_INITIAL_POSITION = Position(0, 6)
        self.deck = deck or Deck()
        self.board = self.init_board()
        self.swap_queens()

        self.red_player = Player(
            PlayerType.RED, position=self.RED_INITAL_POSTION)
        self.black_player = Player(
            PlayerType.BLACK, position=self.BLACK_INITIAL_POSITION)
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
            name = text_with_red_background(
                self.current_player.name) if self.current_player.color == PlayerType.RED else text_with_blue_background(self.current_player.name)
            print(f'{name} turn')
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
        possible_moves = self.filter_possible_moves_for_current_player(
            possible_moves)
        for i, move in enumerate(possible_moves):
            print(f'{i+1}. {self.board[move.x][move.y]} {str(move)}')
        selected = get_int_input_option()
        while selected > len(possible_moves) or selected <= 0:
            print(red_text('Invalid input, please choose listed option'))
            selected = get_int_input_option()
        self.update_current_player_position(possible_moves[selected-1])
        self.evaluate_current_player_position()
        self.update_counter()

    def list_possible_moves_for_current_player(self) -> list[Position]:
        position = self.current_player.position
        current_card = self.board[position.x][position.y]
        if current_card.is_red_numeral():
            return self.get_valid_vertical_moves(current_card, position)
        elif current_card.is_black_numeral():
            return self.get_valid_horizontal_moves(current_card, position)
        elif current_card.is_joker():
            return self.get_valid_jocker_moves(position)
        elif current_card.is_jack():
            return self.get_valid_jack_moves(position)
        elif current_card.is_king():
            return self.get_valid_king_moves(position)
        elif current_card.is_queen():
            return self.get_valid_king_moves(position)
        return []

    def filter_possible_moves_for_current_player(self, possible_moves):
        # filter queen
        opponent = self.black_player if self.current_player == self.red_player else self.red_player
        queen_position = self.BLACK_INITIAL_POSITION if self.current_player == self.black_player else self.RED_INITAL_POSTION
        res = []
        for move in possible_moves:
            if move != queen_position and move != opponent.position:
                res.append(move)
        return res

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

    def get_valid_horizontal_moves(self, card, current_position) -> list[Position]:
        card_value = card.rank
        valid_moves = []
        if current_position.y + card_value < self.MATRIX_SIZE:
            valid_moves.append(Position(current_position.x,
                               current_position.y + card_value))
        if (current_position.y+1) - card_value > 0:
            valid_moves.append(Position(current_position.x,
                               current_position.y - card_value))
        if (current_position.y+1) + card_value > self.MATRIX_SIZE:

            reminder = card_value % self.MATRIX_SIZE

            padding = (current_position.y+1)

            value = (reminder + padding) % self.MATRIX_SIZE
            if value != 0:
                valid_moves.append(Position(current_position.x, (value - 1)))
            else:
                valid_moves.append(
                    Position(current_position.x, self.MATRIX_SIZE))

        if (current_position.y+1) - card_value <= 0:

            reminder = card_value % self.MATRIX_SIZE

            padding = current_position.y + 1

            value = abs(reminder - padding)
            if padding > reminder:

                valid_moves.append(
                    Position(current_position.x, current_position.y - (reminder)))
            else:
                value = abs(reminder - padding)
                valid_moves.append(
                    Position(current_position.x, self.MATRIX_SIZE - (value+1)))

        return valid_moves

    def get_valid_vertical_moves(self, card, current_position) -> list[Position]:
        card_value = card.rank
        valid_moves = []
        if current_position.x + card_value < self.MATRIX_SIZE:
            valid_moves.append(
                Position(current_position.x + card_value, current_position.y))
        if (current_position.x+1) - card_value > 0:
            valid_moves.append(
                Position(current_position.x - card_value, current_position.y))
        if (current_position.x+1) + card_value > self.MATRIX_SIZE:

            reminder = card_value % self.MATRIX_SIZE

            padding = (current_position.x+1)

            value = (reminder + padding) % self.MATRIX_SIZE

            if value != 0:
                valid_moves.append(Position((value - 1), current_position.y))
            else:
                valid_moves.append(
                    Position(self.MATRIX_SIZE, current_position.x))

        if (current_position.x+1) - card_value <= 0:

            reminder = card_value % self.MATRIX_SIZE

            padding = current_position.y + 1

            value = abs(reminder - padding)
            if padding > reminder:

                valid_moves.append(
                    Position(current_position.x - (reminder), current_position.y))
            else:
                value = abs(reminder - padding)
                valid_moves.append(
                    Position(self.MATRIX_SIZE - (value+1), current_position.y))
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
        while True:
            jokers = []
            for i in range(self.MATRIX_SIZE):
                for j in range(self.MATRIX_SIZE):
                    if (self.board[i][j].is_joker() and [i+1, j+1] not in self.previous_swap_index):
                        jokers.append([i+1, j+1])

            print(
                f'You have {len(jokers)} jokers to swap which are given below')
            # joker = [joker for joker in jokers]
            for index, value in enumerate(jokers):
                print(f'{index+1}. {value}')
            selected_joker = get_int_input_option()
            print('Now select the card')
            selected_joker_position = jokers[selected_joker - 1]

            selected_rank, selected_suit = self.select_card()

            for i in range(self.MATRIX_SIZE):
                for j in range(self.MATRIX_SIZE):
                    if self.board[i][j].suit == selected_suit and self.board[i][j].rank == selected_rank:
                        self.row_index = i
                        self.column_index = j

            # print(self.previous_swap_index[0])
            # print([selected_joker_position[0],selected_joker_position[1]])
            # print( self.previous_swap_index[0] == [selected_joker_position[0],selected_joker_position[1]] )

            print(self.row_index + 1, self.column_index+1)
            print(selected_joker_position[0], selected_joker_position[1])

            if (selected_joker_position[0] == self.row_index + 1 or selected_joker_position[1] == self.column_index+1):
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
                return
            else:
                print(
                    '************************************************************************')
                print(
                    '* selected card is not same row or column please select another one *')
                print(
                    '************************************************************************')

    def select_card(self):
        while True:
            print(purple_text('Choose the card you want to swap with'))
            selected_rank = input(
                'Rank {A, 2, 3, 4, 5, 6, 7, 8, 9, X, J, K}: ')

            if selected_rank == 'a' or selected_rank == 'A':
                card_value = 1
            elif selected_rank == 'k' or selected_rank == 'K':
                card_value = 13
            elif selected_rank == 'j' or selected_rank == 'J':
                card_value = 11
            elif selected_rank == 'x' or selected_rank == 'X':
                card_value = 10
            else:
                if type(selected_rank) != int and not selected_rank.isdigit():
                    print(red_text('Invalid rank'))
                    continue
                card_value = int(selected_rank)

            selected_suit = input(
                'Suit {Heart as H, Clubs as C, Spade as S, Diamond as D}: ').upper()

            if selected_suit not in ['H', 'C', 'S', 'D']:
                print(red_text('Invalid suit'))
                continue
            return card_value, selected_suit

    def turn_prompt(self) -> TurnType:
        while True:
            print(purple_text("What step would you take in this turn?"))
            print('1. Move my Romeo')
            print('2. Swap the Joker')
            choice = get_int_input_option()
            if choice == 1 or choice == 2:
                return TurnType(choice)

    def get_valid_jocker_moves(self, current_position):
        king_moves = self.get_valid_king_moves(current_position)
        jack_moves = self.get_valid_jack_moves(current_position)
        vertical_moves = []
        horizontal_moves = []
        for i in range(1, self.MATRIX_SIZE + 1):
            new_y1 = current_position.y + i
            new_y2 = current_position.y - i
            new_x1 = current_position.x + i
            new_x2 = current_position.x - i
            if new_y1 >= 0 and new_y1 < self.MATRIX_SIZE:
                horizontal_moves.append(Position(current_position.x, new_y1))
            if new_y2 >= 0 and new_y2 < self.MATRIX_SIZE:
                horizontal_moves.append(Position(current_position.x, new_y2))
            if new_x1 >= 0 and new_x1 < self.MATRIX_SIZE:
                vertical_moves.append(Position(new_x1, current_position.y))
            if new_x2 >= 0 and new_x2 < self.MATRIX_SIZE:
                vertical_moves.append(Position(new_x2, current_position.y))

        return vertical_moves + horizontal_moves + king_moves + jack_moves
