from Board import Board
import json

class Game:
    def __init__(self):
        self.board = Board()
    
    def run(self, dice_rolls):
        board_len = len(self.board.tiles)
        player_count = len(self.board.players)
        turn_count = 0
        print(board_len)
        for roll in dice_rolls:
            player_no = turn_count % player_count
            
            # set player's turn
            player = self.board.players[player_no]
            
            # increment player's position
            player.position += roll
            print(player)
            if player.position >= board_len:
                player.position %= board_len
                print(f"new pos: {player.position}")
                
            
            # buy property or pay rent
            tile = self.board.tiles[player.position]
            
            # TODO: pay rent
            if tile.is_owned():
                pay_id = tile.owner
                paid_player = self.board.players[pay_id]
                
                rent = tile.price
                
                # check for double rent (see TODO)
                if self.board.owns_full_colour_set(paid_player, tile.colour): 
                    rent*=2
                
                
                                
            # TODO: buy property
            else:
                pass
            
            # TODO: check bankruptcy for player
            
    
if __name__ == "__main__":
    try:
        with open("jsons/rolls_1.json", "r") as file:
            data1 = json.load(file)

        with open("jsons/rolls_2.json", "r") as file1:
            data2 = json.load(file1)
                        
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("Failed to decode JSON: {e}")

    game = Game()
    
    # Rolls 1
    game.run(data1)
    
    # Rolls 2
    game.run(data2)