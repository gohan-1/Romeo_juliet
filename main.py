from game import Game
from  position import Position

from player import Player

def nominate_colors():
    black_player = {'name': 'Black', 'color': 'black'}
    red_player = {'name': 'Red', 'color': 'red'}
    return black_player, red_player


if __name__ == "__main__":
    game = Game()
    game.print_board()
    game.start_prompt()
    red_pl_name  = input('\nPlease enter  red Player  name ')
    p1 = Position(0,6)
    red_player =Player('RED',p1,red_pl_name)
    black_pl_name  = input('\nPlease enter black Player  name ')
    p2  = Position(6,0)
    Player('Black',p2,black_pl_name)
                
    game.move_prompt()
    game.choose_mv_option()
    
    
    # game.choose_option()
