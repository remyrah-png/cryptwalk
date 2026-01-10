# player.py

from entity import CombatEntity

class Player(CombatEntity):
    def __init__(self):
        super().__init__("Hero", 35, 35, 10, 5)
        self.inventory = []
        self.gold = 0