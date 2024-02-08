import sys
from game import Game
from helpers import get_int_input_option, purple_text


if __name__ == "__main__":
    print('Welcome to Romeo and Juliet Game')

    while True:
        try:
            print(purple_text('Please choose the mode you want to start the game'))
            print('1. Play in turn')
            print('2. Play with AI')
            print('3. Quit')
            choice = get_int_input_option()
            if choice == 1:
                game = Game()
                option = input(purple_text(
                    "Do you want to update players' info? (y/N)"))
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
        except Exception as e:
            print('There is error. Restarting the game...')
