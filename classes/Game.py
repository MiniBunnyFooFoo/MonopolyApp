from Board import Board
import json

class Game:
    def __init__(self):
        self.board = Board()
    
    def run(self, dice_rolls):
        # TODO: Reset the board
        board_len = len(self.board.tiles)
        player_count = len(self.board.players)
        turn_count = 0
        for roll in dice_rolls:
            player_no = turn_count % player_count
            
            # set player's turn
            player = self.board.players[player_no]
            print(f"Player {player_no}: {player.name}, rolled: {roll}")
            
            # increment player's position
            player.position += roll

            # Add money for passing go
            if player.position >= board_len:
                player.change_money(1)      
                player.position %= board_len
                print(f"{player.name} + 1 -> {player.money}")
                
            
            # buy property or pay rent
            tile = self.board.tiles[player.position]
            print(tile)

            
            # Check for GO
            if tile.type == "go":
                continue

            
            # buy property
            if not tile.is_owned():
                tile.owner = player_no
                player.properties.append(tile)
                price = tile.price
                player.change_money(-price)
                print(f"{player.name} bought {tile.name}!")
                                
            # pay rent
            elif tile.owner != player_no:
                pay_id = tile.owner
                paid_player = self.board.players[pay_id]
                
                rent = tile.price
                
                # TODO: check for double rent (see TODO)
                if self.board.owns_full_colour_set(paid_player, tile.colour): 
                    print(f"{paid_player.name}")
                    rent*=2
                
                # players pay each other
                paid_player.change_money(rent)
                player.change_money(-rent)
                print(f"{paid_player.name} + {rent} -> {paid_player.money}")
                print(f"{player.name} - {rent} -> {player.money}")

            # TODO: check bankruptcy for player
            if player.is_bankrupt():
                print("Someone's a broke boy")
                break

            # increment turn counter
            turn_count += 1
            print(player)
            input("Turn done: ")

        # TODO: Finish simulation
        print("game end")
        print("============================== RESULTS =============================")
        winning_money = -1
        winners = []
        for i in self.board.players:
            if i.money >= winning_money:
                winners.append(i)
        
        print(f"WINNERS: {winners}")
            
    
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
    
    # # Rolls 2
    # game.run(data2)