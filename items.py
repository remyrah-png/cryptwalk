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
health_potion = Item("Health Potion", "potion", 12)
iron_sword = Item("Iron Sword", "weapon", 5) # +5 stregnth
leather_armor = Item("Leather Armor", "armor", 3) # +3 defense