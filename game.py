from deck import Deck
from helpers import green_text, text_with_blue_background, text_with_red_background


class Game:
    def __init__(self, deck: Deck = None) -> None:
        self.MATRIX_SIZE = 7
        self.deck = deck or Deck()
        self.board = self.init_board()
        self.swap_queens()
       
        

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

    def move(self):
        pass

    def swap(self):
        print('started')
        previous_swap_index = [[0,6],[6,0]]
        jokers=[]
        for i in range(self.MATRIX_SIZE):
            for j in range(self.MATRIX_SIZE):
                if (self.board[i][j].is_joker() and [i, j] not in previous_swap_index):
                    jokers.append([i,j])
        
        print(f'You have {len(jokers)} jokers to swap whicher ')
        # joker = [joker for joker in jokers]
        for index,value in enumerate(jokers):
            print(f' {index} with position {value} ')
        selected = int(input('choose one of the joker'))
        print('choose teh card')
        selected = int(input(' choose the row value'))
        selected = int(input('choose the coumn value'))



        


    def create_prompt(self):
        print(' \n Choose the move ')
        print(' 1 for swap ')
        print(' 2 for move ')

    def choose_option(self):
        option = int(input(' Please Enter the choice '))
        if (option == 1 ):
            self.swap()
        else:
            self.move()