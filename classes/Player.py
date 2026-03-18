class Player:
    def __init__(self, name):
        self.name = name
        self.properties = []
        self.money = 16
        self.position = 0

    def change_money(self, money):
        self.money += money

    def is_bankrupt(self):
        if self.money <= 0: return True
        return False

    def __repr__(self):
        return f"Player(name={self.name}, money={self.money}, position={self.position}, properties={self.properties})"