from enum import Enum
from card import Card
from deck import Deck
from helpers import get_int_input_option, green_text, purple_text, red_text, text_with_blue_background, text_with_red_background, yellow_text

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
        self.previous_swap_index = [Position(0, 6), Position(6, 0)]

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

        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if self.board[i][j].is_spade_queen():
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
                if not self.move():
                    continue
            elif option == TurnType.SWAP:
                if not self.swap():
                    continue

            check_win = self.checking_winning_position()
            if check_win == True:
                return False

    def move(self) -> bool:
        print('Please choose your desired position')
        possible_moves = self.list_possible_moves_for_current_player()
        if len(possible_moves) == 0:
            print(red_text('No possible moves for this card'))
            return False
        for i, move in enumerate(possible_moves):
            print(
                f'{self.board[move.x][move.y]} {str(move)} >>> Press {i + 1} ')
        selected = get_int_input_option()
        while selected > len(possible_moves) or selected <= 0:
            print(red_text('Invalid input, please choose listed option'))
            selected = get_int_input_option()
        return self.perform_move(possible_moves[selected-1])

    def perform_move(self, move):
        self.update_current_player_position(move)
        self.toggle_players()
        self.update_counter()
        return True

    def list_possible_moves_for_current_player(self) -> list[Position]:
        position = self.current_player.position
        current_card = self.board[position.x][position.y]
        possible_moves = []
        if current_card.is_red_numeral():
            possible_moves = self.get_valid_vertical_moves(
                current_card, position)
        elif current_card.is_black_numeral():
            possible_moves = self.get_valid_horizontal_moves(
                current_card, position)
        elif current_card.is_joker():
            all_moves = self.get_valid_joker_moves(position)
            unique_list = []
            for item in all_moves:
                if item not in unique_list:
                    unique_list.append(item)
            possible_moves = unique_list
        elif current_card.is_jack():
            possible_moves = self.get_valid_jack_moves(position)
        elif current_card.is_king():
            possible_moves = self.get_valid_king_moves(position)
        elif current_card.is_queen():
            possible_moves = self.get_valid_king_moves(position)
        return self.filter_possible_moves_for_current_player(possible_moves)

    def filter_possible_moves_for_current_player(self, possible_moves):
        # filter queen
        opponent = self.black_player if self.current_player == self.red_player else self.red_player
        queen_position = self.BLACK_INITIAL_POSITION if self.current_player == self.black_player else self.RED_INITAL_POSTION
        res = []
        for move in possible_moves:
            if move != queen_position and move != opponent.position:
                res.append(move)
        return res

    def filter_possible_swap(self, possible_moves):
        res = []
        for move in possible_moves:
            if move not in self.previous_swap_index and not self.is_occuiped(move) and move != self.RED_INITAL_POSTION and move != self.BLACK_INITIAL_POSITION:
                res.append(move)
        return res

    def checking_winning_position(self):
        if self.black_player.position == self.RED_INITAL_POSTION:
            print(yellow_text('BLACK WINS'))
            return True
        elif self.red_player.position == self.BLACK_INITIAL_POSITION:
            print(yellow_text('RED WINS'))
            return True
        else:
            return False

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

    def check_right(self, cur, opp, value):
        if cur > opp and cur + value > self.MATRIX_SIZE + opp:
            return False
        if cur < opp and cur + value > opp:
            return False
        return True

    def check_left(self, cur, opp, value):
        if cur < opp and self.MATRIX_SIZE + cur - value < opp:
            return False
        if cur > opp and cur - value < opp:
            return False
        return True

    def get_valid_horizontal_moves(self, card, current_position) -> list[Position]:
        card_value = card.rank
        valid_moves = []
        new_y1 = (current_position.y + card_value) % self.MATRIX_SIZE
        new_y2 = (self.MATRIX_SIZE + current_position.y -
                  card_value) % self.MATRIX_SIZE
        new_ys = [new_y1, new_y2]
        opponent = self.black_player if self.current_player == self.red_player else self.red_player
        opponent_position = opponent.position
        if current_position.x == opponent_position.x:
            if not self.check_right(current_position.y, opponent_position.y, card_value):
                new_ys.remove(new_y1)
            if not self.check_left(current_position.y, opponent_position.y, card_value):
                new_ys.remove(new_y2)

        for new_y in new_ys:
            valid_moves.append(Position(current_position.x, new_y))

        return valid_moves

    def get_valid_vertical_moves(self, card, current_position) -> list[Position]:
        card_value = card.rank
        valid_moves = []
        new_x1 = (current_position.x + card_value) % self.MATRIX_SIZE
        new_x2 = (self.MATRIX_SIZE + current_position.x -
                  card_value) % self.MATRIX_SIZE
        new_xs = [new_x1, new_x2]
        opponent = self.black_player if self.current_player == self.red_player else self.red_player
        opponent_position = opponent.position
        if opponent_position.y == current_position.y:
            if not self.check_right(current_position.x, opponent_position.x, card_value):
                new_xs.remove(new_x1)
            if not self.check_left(current_position.x, opponent_position.x, card_value):
                new_xs.remove(new_x2)
        for new_x in new_xs:
            valid_moves.append(Position(new_x, current_position.y))

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

    def get_swappable_jokers(self):
        jokers = []
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if (self.board[i][j].is_joker() and Position(i, j) not in self.previous_swap_index and not self.is_occuiped(Position(i, j))):
                    jokers.append(Position(i, j))
        return jokers

    def swap(self):
        while True:
            jokers = self.get_swappable_jokers()
            if len(jokers) == 0:
                print(red_text('No jokers available to swap'))
                return False
            print(
                f'You have {len(jokers)} jokers to swap which are given below: ')
            # joker = [joker for joker in jokers]
            for index, value in enumerate(jokers):
                print(f'{value} >>> Press {index + 1}')
            selected_joker = get_int_input_option()
            while selected_joker > len(jokers) or selected_joker <= 0:
                print(red_text('Invalid input, please choose listed option'))
                selected_joker = get_int_input_option()
            # list_posible
            print('Now select the card the card you want to swap.')
            selected_joker_position = jokers[selected_joker - 1]

            swap_positions = self.list_possible_swaps(selected_joker_position)

            for i, move in enumerate(swap_positions):
                print(
                    f'{self.board[move.x][move.y]} {str(move)} >>> Press {i + 1} ')
            selected = get_int_input_option()
            self.perform_swap(selected_joker_position,
                              swap_positions[selected-1])
            return True

    def perform_swap(self, joker_position, swap_position):
        self.board[joker_position.x][joker_position.y], \
            self.board[swap_position.x][swap_position.y] = \
            self.board[swap_position.x][swap_position.y], \
            self.board[joker_position.x][joker_position.y]
        self.previous_swap_index = [swap_position, joker_position]
        self.toggle_players()

    def list_possible_swaps(self, joker_position):
        list_of_positions = []
        for i in range(self.MATRIX_SIZE):
            if (joker_position.x) != i:
                list_of_positions.append(Position(i, joker_position.y))
        for j in range(self.MATRIX_SIZE):
            if ((joker_position.y) != j):
                list_of_positions.append(Position(joker_position.x, j))
        return self.filter_possible_swap(list_of_positions)

    def is_occuiped(self, position):
        return self.red_player.position == position or self.black_player.position == position

    def turn_prompt(self) -> TurnType:
        while True:
            print(purple_text("What step would you take in this turn?"))
            print('Move my Romeo >>> Press 1')
            print('Swap the Joker >>> Press 2')
            choice = get_int_input_option()
            if choice == 1 or choice == 2:
                return TurnType(choice)

    def get_valid_joker_moves(self, current_position):
        king_moves = self.get_valid_king_moves(current_position)
        filtered_king_moves = []
        for king_move in king_moves:
            card = self.board[king_move.x][king_move.y]
            if card.is_king():
                filtered_king_moves.append(king_move)
        jack_moves = self.get_valid_jack_moves(current_position)
        filtered_jack_moves = []
        for jack_move in jack_moves:
            card = self.board[jack_move.x][jack_move.y]
            if card.is_jack():
                filtered_jack_moves.append(jack_move)
        vertical_moves = []
        horizontal_moves = []
        for i in range(0, self.MATRIX_SIZE):
            vertical_card = self.board[i][current_position.y]
            if vertical_card.is_red_numeral():
                valid_cards = self.get_valid_vertical_moves(
                    vertical_card, Position(i, current_position.y))
                for valid_card in valid_cards:
                    if valid_card.y == current_position.y and valid_card.x == current_position.x:
                        vertical_moves.append(
                            Position(i, current_position.y))
            if vertical_card.is_joker() and i != current_position.x:
                vertical_moves.append(Position(i, current_position.y))
            horizontal_card = self.board[current_position.x][i]
            if horizontal_card.is_black_numeral():
                valid_cards = self.get_valid_horizontal_moves(
                    horizontal_card, Position(current_position.x, i))

                for valid_card in valid_cards:
                    print(valid_card.x, valid_card.y)
                    if valid_card.x == current_position.x and valid_card.y == current_position.y:
                        horizontal_moves.append(
                            Position(current_position.x, i))
            if horizontal_card.is_joker() and i != current_position.y:
                horizontal_moves.append(Position(current_position.x, i))

        return vertical_moves + horizontal_moves + filtered_king_moves + filtered_jack_moves
