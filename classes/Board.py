from Player import Player
from Tile import Tile
import json

class Board: 
    def __init__(self):
        # Load players onto board
        players = ["Peter", "Billy", "Charlotte", "Sweedal"]
        self.players = [Player(name) for name in players]
        
        # Load board tiles from json
        self.tiles = []
        try:
            with open("jsons/board.json", "r") as file:
                data = json.load(file)
            
            for i in data:
                name = i['name']
                colour = i.get("colour", None)
                price = i.get("price", None)
                type = i.get("type", None)
                self.tiles.append(Tile(name, colour, price, type))

        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Failed to decode JSON: {e}")

    def owns_full_colour_set(self, player, colour):
        # TODO: Check functionality
        # Check for matching pair within player's properties
        p_count = 0
        for property in player.properties:
            if property.colour == colour: p_count += 1
            
        return p_count == 2

if __name__ == "__main__":
    board = Board()
    print([player for player in board.players])
    print([tile for tile in board.tiles])