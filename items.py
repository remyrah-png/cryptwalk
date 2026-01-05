# items.py

class Item:
    def __init__(self, name, type_, value):
        self.name = name
        self.type = type_  # "potion", "weapon", "armor"
        self.value = value  # heal amount or stat bonus

    def use(self, player):
        if self.type == "potion":
            healed = player.heal(self.value)
            print(f"You drink {self.name} and recover {healed} HP!")
            return True  # consumed
        elif self.type == "weapon":
            if player.weapon == self:
                print(f"{self.name} is already equipped.")
                return False
            player.weapon = self
            player.stats["strength"] += self.value
            print(f"You equip {self.name} (+{self.value} strength)!")
            return False
        elif self.type == "armor":
            if player.armor == self:
                print(f"{self.name} is already equipped.")
                return False
            player.armor = self
            player.stats["defense"] += self.value
            print(f"You equip {self.name} (+{self.value} defense)!")
            return False
        else:
            print("Can't use that.")
            return False

# Example items
healing_potion = Item("Healing Potion", "potion", 12)
iron_sword = Item("Iron Sword", "weapon", 5)
leather_armor = Item("Leather Armor", "armor", 3)
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