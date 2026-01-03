# player.py

class Player:
    def __init__(self):
        self.name = "Hero"
        self.stats = {
            "hp": 35,
            "max_hp": 35,
            "strength": 10,
            "defense": 5
        }
        self.alive = True
        self.effects = []
        self.weapon = None
        self.armor= None
        self.inventory = []
        self.gold = 0

    def heal(self, amount):
        before = self.stats["hp"]
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)
        return self.stats["hp"] - before

    def is_alive(self):
        return self.stats["hp"] > 0

