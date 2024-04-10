
import random
from game import Game
from turn import Turn
from position import Position


class DFS:
    def make_decision(self, game: Game) -> Turn:
        init_possible_moves = game.generate_possible_moves(game.current_player.position)
        bfsPath={}
        
        explored= [game.current_player.position]
        # for
        fortniter=[game.current_player.position]

        while len(fortniter) >0:
            current_cell = fortniter.pop()
            
            if current_cell == Position(6,0):
                break
            
            possible_moves = game.generate_possible_moves(current_cell)    
            # print(possible_moves)
            for possible_move in possible_moves:
                # possible_move 
                
                # current_cell = possible_move.end
                if possible_move.end in explored:
                   
                    continue

                child_cell = (possible_move.end.x,possible_move.end.y)
                bfsPath[current_cell.x,current_cell.y] = child_cell
                # print(possible_move.end)
                if possible_move.end in explored:
                   
                    continue

                fortniter.append(possible_move.end)
                explored.append(possible_move.end)  
        print(bfsPath)

        
        next_move =bfsPath[(game.current_player.position.x,game.current_player.position.y)]

        # print(init_possible_move)
        for init_possible_move in init_possible_moves:
            if init_possible_move.end.x == next_move[0] and init_possible_move.end.y == next_move[1]:
                return init_possible_move


                
    
