import random
import numpy as np

import colorama
from colorama import Fore, Back, Style

# Using NumPy
matrix = np.full((7, 7), '', dtype='<U3')  # Initialize with empty strings
black_rome = [0,6]
red_romeo = [6,0]

def prepare_pack():
    deck = []
    suits = ['H', 'D', 'C', 'S']
    ranks = list(range(1, 14))
    for i in suits:
        for j in range(1,14):
           deck.append({'suit' : i , 'rank' : j})

    # Create a list of dictionaries representing cards
    # deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks * 4]

    # Remove specific cards from the deck
    deck = [card for card in deck if not (card['suit'] == 'D' and card['rank'] == 12) and not (card['suit'] == 'C' and card['rank'] == 12) and not (card['suit'] == 'S' and card['rank'] == 7)]

    return deck

def shuffle_matrix():
    flat_matrix = matrix.flatten()

    # Shuffle the flattened matrix
    random.shuffle(flat_matrix)

    # Reshape the flattened matrix back to the original shape
    shuffle_matrix= flat_matrix.reshape(matrix.shape)
    return shuffle_matrix

    # Print the shuffled matrix



def deal_cards(deck):
    for i in range(7):
        for j in range(7):
            # Pop a card from the deck and assign its string representation to the matrix element
            card = deck.pop(0)
            if card['rank'] == 1:
                card['rank'] =  'A'
            elif card['rank'] == 11:
                card['rank'] = 'J'
            elif card['rank'] == 12:
                 card['rank'] = 'Q'
            elif card['rank'] == 13:
                 card['rank'] = 'K' 
            if card['rank'] == 10:
                matrix[i, j] = str(card['rank'])+str(card['suit'])
            elif card['rank'] == 7:
                matrix[i,j] = 'JOK'
            else:
                matrix[i, j] = '0'+str(card['rank'])+str(card['suit']) 
            

def swap_queens(matrix):
    for i in range(7):
        for j in range(7):
            if matrix[i,j] == '0QS':
                a=matrix[i,j]
                matrix[i,j]=matrix[6,0]
                matrix[6,0]=a
            elif matrix[i,j] == '0QH':
                a=matrix[i,j]
                matrix[i,j]=matrix[0,6]
                matrix[0,6]=a

def turn_down_sevens(matrix):
    for _ in range(3):
        row = random.randint(0, 6)
        col = random.randint(0, 6)
        grid[row][col] = 'Joker'
    return grid

def nominate_colors():
    black_player = {'name': 'Black', 'color': 'black'}
    red_player = {'name': 'Red', 'color': 'red'}
    return black_player, red_player

def initiate_counters():
    black_counter = 0
    red_counter = 0
    return black_counter, red_counter

def highlight_element(element, position):
    
    if position  == red_romeo:
        return f"{Back.RED}{Fore.BLACK}{element}{Style.RESET_ALL}"
    elif  position  == black_rome:
        return f"{Back.YELLOW}{Fore.BLACK}{element}{Style.RESET_ALL}"
    else:
        return element

# # Example usage:
deck = prepare_pack()

deal_cards(deck)
shuffle_matrix = shuffle_matrix()
matrix =shuffle_matrix
# Print the matrix
swap_queens(matrix)
for i, row in enumerate(matrix):
    for j, cell in enumerate(row):
        print(highlight_element(cell, [i, j]), end=' ')
    print()

# for row in highlighted_matrix:
#     print(' '.join(row))

