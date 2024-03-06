SUIT_MAP = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣', 'Joker': '🃟'}
SUIT_MAP_FILE = {'S': 'spades', 'H': 'hearts',
                 'D': 'diamonds', 'C': 'clubs', 'Joker': 'joker'}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank = self.rank
        suit = SUIT_MAP[self.suit]

        if suit == 'Joker':
            suit = 'JK'
        if rank == 1:
            rank = 'A'
        elif rank == 10:
            rank = 'X'
        elif rank == 11:
            rank = 'J'
        elif rank == 12:
            rank = 'Q'
        elif rank == 13:
            rank = 'K'
        elif rank == 0:
            rank = ''
        return f"{rank}{suit}"

    def get_image_path(self, folder_path='assets/cards'):
        if self.suit == 'Joker':
            return f'{folder_path}/joker.png'
        rank = self.rank
        if rank == 1:
            rank = 'ace'
        elif rank == 11:
            rank = 'jack'
        elif rank == 12:
            rank = 'queen'
        elif rank == 13:
            rank = 'king'
        elif rank == 0:
            rank = ''
        suit = SUIT_MAP_FILE[self.suit]
        return f'{folder_path}/{rank}_of_{suit}.png'

    def is_heart_queen(self):
        return self.suit == 'H' and self.rank == 12

    def is_spade_queen(self):
        return self.suit == 'S' and self.rank == 12

    def is_joker(self):
        return self.suit == 'Joker'

    def is_red_numeral(self):
        return self.suit in ['H', 'D'] and self.rank <= 10

    def is_black_numeral(self):
        return self.suit in ['S', 'C'] and self.rank <= 10

    def is_king(self):
        return self.rank == 13

    def is_jack(self):
        return self.rank == 11

    def is_queen(self):
        return self.rank == 12
