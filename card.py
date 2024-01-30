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
        elif rank == 11:
            rank = 'J'
        elif rank == 12:
            rank = 'Q'
        elif rank == 13:
            rank = 'K'
        elif rank == 0:
            rank = ''
        return f"{self.rank}{self.suit}"
