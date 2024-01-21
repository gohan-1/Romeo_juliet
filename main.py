import random
import numpy as np

# Using NumPy
matrix = np.full((7, 7), '', dtype='<U2')  # Initialize with empty strings

def prepare_pack():
    suits = ['H', 'D', 'C', 'S']
    ranks = list(range(1, 14))

    # Create a list of dictionaries representing cards
    deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks * 4]

    # Remove specific cards from the deck
    deck = [card for card in deck if not (card['suit'] == 'D' and card['rank'] == 12) and not (card['suit'] == 'C' and card['rank'] == 12) and not (card['suit'] == 'S' and card['rank'] == 7)]

    return deck

def shuffle_pack(deck):
    random.shuffle(deck)
    return deck

def deal_cards(deck):
    for i in range(7):
        for j in range(7):
            # Pop a card from the deck and assign its string representation to the matrix element
            card = deck.pop(0)
            matrix[i, j] = f"{card['rank']}{card['suit']}"

# Example usage:
deck = prepare_pack()
shuffle_pack(deck)
deal_cards(deck)

# Print the matrix
print(matrix)
