import random
from card import Card


class Deck:
    def __init__(self):

        self.cards: list[Card] = self.prepare_pack()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def prepare_pack(self):
        cards = [Card(suit, rank) for suit in ['H', 'D', 'C', 'S']
                 for rank in range(1, 14)]
        cards = [card for card in cards if not (card.suit == 'D' and card.rank == 12)
                 and not (card.suit == 'C' and card.rank == 12)
                 and not (card.rank == 7)]
        cards.append(Card('Joker', 0))
        cards.append(Card('Joker', 0))
        cards.append(Card('Joker', 0))
        return cards
