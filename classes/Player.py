class Player:
    def __init__(self, name):
        self.name = name
        self.properties = []
        self.money = 16
        self.position = 0

    def pay(self):
        pass

    def add_money(self, money):
        pass

    def is_bankrupt(self):
        pass

    def __repr__(self):
        return f"Player(name={self.name}, money={self.money})"