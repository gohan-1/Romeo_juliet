from deck import Deck
from helpers import green_text, text_with_blue_background, text_with_red_background
import sys

from  position import Position

from player import Player
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



        


    def move_prompt(self):
        print(' \n\n Choose the  option ')
        print('\n1 for swap ')
        print(' \n2 for move ')

    def start_prompt(self):
        self.flag = True
        while self.flag:

            print('\n\nPlaying Romeo game')

            print(" \n\n1. play")
            print(" \n2. Reset Game")
            print(" \n3. Quit")
            choice =int(input("Enter your choice (1/2/3): "))

            if choice == 1:
                self.print_board()
                # board = self.move_prompt()
                red_pl_name  = input('\nPlease enter  red Player  name ')
                p1 = Position(0,6)
                red_player =Player('RED',p1,red_pl_name)
                black_pl_name  = input('\nPlease enter black Player  name ')
                p2  = Position(6,0)
                Player('Black',p2,black_pl_name)
                
                self.move_prompt()
                self.flag=False
            elif choice == 2:
                self.deck = Deck()
                self.board = self.init_board()
                self.swap_queens()
                self.print_board()
            
            elif choice == 3:
                print("Exiting the game. Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                sys.exit()


    def choose_option(self):
        option = int(input(' Please Enter the choice '))
        if (option == 1 ):
            self.swap()
        else:
            self.move()
        
