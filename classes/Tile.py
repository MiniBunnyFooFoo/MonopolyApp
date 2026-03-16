class Tile:
    def __init__(self, name, colour, price, type):
        self.name = name
        self.owner = None
        self.colour = colour
        self.price = price
        self.type = type

    def is_owned(self):
        return bool(self.owner)