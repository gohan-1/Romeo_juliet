from game import Game


def nominate_colors():
    black_player = {'name': 'Black', 'color': 'black'}
    red_player = {'name': 'Red', 'color': 'red'}
    return black_player, red_player


if __name__ == "__main__":
    game = Game()
    game.print_board()
    game.create_prompt()
    game.choose_option()
