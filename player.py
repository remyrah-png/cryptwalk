from entity import CombatEntity

class Player(CombatEntity):
    def __init__(self, name="Hero", hp=100, max_hp=100, strength=8, defense=4):
        super().__init__(name, hp, max_hp, strength, defense)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.inventory = []  # Potions, swords, etc. later

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.stats["max_hp"] += 20
        self.stats["hp"] = self.stats["max_hp"]
        self.stats["strength"] += 2
        self.stats["defense"] += 1
        print(f"{self.name} leveled up to level {self.level}!")