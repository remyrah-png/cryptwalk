# items.py
class Item:
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type
        self.value = value

        def use(self, player):
            if self.type == "potion":
                healed = player.heal(self.value)
                print(f"You drink the {self.name} and heal {healed} HP.")
                return True
            else:
                print(f"The {self.name} cannot be used.")
                return False
            
# Example items (we'll use these later)
healing_potion = Item("Health Potion", "potion", 12)
iron_sword = Item("Iron Sword", "weapon", 5) # +5 stregnth
leather_armor = Item("Leather Armor", "armor", 3) # +3 defense

def use(self, player):
    if self.type == "potion":
        healed = player.heal(self.value)
        print(f"You drink {self.name} and recover {healed} HP!")
        return True  # used up
    elif self.type == "weapon":
        if player.weapon:
            print(f"You already have {player.weapon.name} equipped.")
            return False
        player.weapon = self
        player.stats["strength"] += self.value
        print(f"You equip {self.name} (+{self.value} strength)!")
        return False  # not consumed
    elif self.type == "armor":
        if player.armor:
            print(f"You already have {player.armor.name} equipped.")
            return False
        player.armor = self
        player.stats["defense"] += self.value
        print(f"You equip {self.name} (+{self.value} defense)!")
        return False
    else:
        print(f"You can't use {self.name}.")
        return False