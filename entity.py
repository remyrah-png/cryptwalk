class CombatEntity:
    def __init__(self, name, hp, max_hp, strength, defense):
        self.name = name
        self.stats = {
            "hp": hp,
            "max_hp": max_hp,
            "strength": strength,
            "defense": defense
        }
        self.defending = False
        self.effects = []
        self.weapon = None
        self.armor = None

    def heal(self, amount):
        before = self.stats["hp"]
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"] + amount)
        return self.stats["hp"] - before

    def is_alive(self):
        return self.stats["hp"] > 0