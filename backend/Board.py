from backend.Player import Player
from backend.Tile import Tile
from backend.utils import load_jsons
import json

class Board: 
    def __init__(self):
        # Load players onto board
        players = ["Peter", "Billy", "Charlotte", "Sweedal"]
        self.players = [Player(name) for name in players]
        
        # Load board tiles from json       
        self.tiles = []
        try:

            data = load_jsons("board")
            
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
        # Check for matching pair within player's properties
        p_count = 0
        for property in player.properties:
            if property.colour == colour: p_count += 1
            
        return p_count == 2