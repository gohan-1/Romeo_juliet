import sys
from game import Game
from position import Position

from player import Player


def nominate_colors():
    black_player = {'name': 'Black', 'color': 'black'}
    red_player = {'name': 'Red', 'color': 'red'}
    return black_player, red_player


if __name__ == "__main__":
    print('Welcome to Romeo and Juliet Game')
    while True:
        print('Please choose the mode you want to start the game')
        print('1. Play in turn')
        print('2. Play with AI')
        print('3. Quit')
        choice = int(input('Your choice: '))
        if choice == 1:
            game = Game()
            option = input("Do you want to update players' info? (y/N)")
            if option == 'y' or option == 'Y':
                game.setup_players()
            game.play()

        elif choice == 2:
            print('This mode is not supported yet. Please choose another one')
        elif choice == 3:
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
