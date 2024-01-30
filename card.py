class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank = self.rank
        suit = self.suit
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

    def is_heart_queen(self):
        return self.suit == 'H' and self.rank == 12

    def is_spade_queen(self):
        return self.suit == 'S' and self.rank == 12

    def is_joker(self):
        return self.suit == 'Joker'
