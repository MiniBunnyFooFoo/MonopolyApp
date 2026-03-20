from backend.Board import Board
from backend.utils import load_jsons
import json

class Game:
    def __init__(self):
        self.board = Board()
    
    def _snapshot(self, log, extra=None):
        players = []
        for p in self.board.players:
            players.append({
                "name": p.name,
                "money": p.money,
                "position": p.position,
                "properties": [t.name for t in p.properties],
            })
        tiles = []
        for t in self.board.tiles:
            tiles.append({
                "name": t.name,
                "colour": t.colour,
                "price": t.price,
                "type": t.type,
                "owner": t.owner,
            })
        snap = {"players": players, "tiles": tiles, "log": log}
        if extra:
            snap.update(extra)
        return snap
    
    def run(self, dice_rolls):
        # Reset the board and players
        for player in self.board.players:
            player.reset()

        for tile in self.board.tiles:
            tile.reset()
        
        snapshots = []
        snapshots.append(self._snapshot(f"Game started!"))

        board_len = len(self.board.tiles)
        player_count = len(self.board.players)
        turn_count = 0
        
        for roll in dice_rolls:
            player_no = turn_count % player_count
            
            # set player's turn
            player = self.board.players[player_no]
            log_lines = [f"🎲 **{player.name}** rolled a **{roll}**"]
            
            # increment player's position
            player.position += roll

            # Add money for passing go
            if player.position >= board_len:
                player.change_money(1)      
                player.position %= board_len
                log_lines.append(f"⭐ {player.name} passed GO! +$1 → ${player.money}")
                
            
            # buy property or pay rent
            tile = self.board.tiles[player.position]
            log_lines.append(f"📍 Landed on **{tile.name}**")

            
            # Check for GO
            if tile.type == "go":
                snapshots.append(self._snapshot("\n".join(log_lines)))
                turn_count += 1
                continue

            
            # buy property
            if not tile.is_owned():
                tile.owner = player_no
                player.properties.append(tile)
                price = tile.price
                player.change_money(-price)
                log_lines.append(f"🏠 {player.name} bought **{tile.name}** for ${tile.price} → ${player.money}")
                                
            # pay rent
            elif tile.owner != player_no:
                pay_id = tile.owner
                paid_player = self.board.players[pay_id]
                
                rent = tile.price
                
                # check for double rent
                if self.board.owns_full_colour_set(paid_player, tile.colour): 
                    log_lines.append(f"🎯 Double rent! {paid_player.name} owns the full set.")
                    rent*=2
                
                # players pay each other
                paid_player.change_money(rent)
                player.change_money(-rent)
                log_lines.append(f"💸 {player.name} paid ${rent} rent to {paid_player.name}")

            snapshots.append(self._snapshot("\n".join(log_lines)))

            # check bankruptcy for player
            if player.is_bankrupt():
                snapshots[-1]["log"] += f"\n💀 **{player.name} is bankrupt!** Game over."
                break

            # increment turn counter
            turn_count += 1
            

        # Finish simulation       
        winning_money = 0
        winner_id = ""

        # Calculate each player's net worth
        for i in self.board.players:
            money = i.money
            for j in i.properties:
                money += j.price
                        
            if money > winning_money:
                winning_money = money
                winner_id = i.name
        
        snapshots.append(self._snapshot(
            f"🏆 **GAME OVER** — **{winner_id}** wins with a net worth of **${winning_money}**!",
            {"game_over": True, "winner": winner_id}
        ))
        
        return snapshots
    
if __name__ == "__main__":
    try:
        data1 = load_jsons("rolls_1")
        data2 = load_jsons("rolls_2")
                        
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("Failed to decode JSON: {e}")

    game = Game()
    
    # Rolls 1
    game.run(data1)
    
    # Rolls 2
    game.run(data2)