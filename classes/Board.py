import Player, Tile
import json

class Board: 
    def __init__(self):
        self.players = []
        self.tiles = []

    def owns_full_colour_set(self, player, colour):
        pass