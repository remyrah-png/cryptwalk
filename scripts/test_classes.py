# test_classes.py

from player import Player
from items import Item, healing_potion, iron_sword, leather_armor

# Create a player
player = Player()
player.stats["hp"] = 20  # take some damage for testing

print(f"Player HP: {player.stats['hp']}/{player.stats['max_hp']}")

# Use the potion
healed = healing_potion.use(player)
if healed:
    print(f"New HP: {player.stats['hp']}/{player.stats['max_hp']}")

print("\n--- Testing equipment ---")
iron_sword.use(player)
print(f"Strength: {player.stats['strength']}")

leather_armor.use(player)
print(f"Defense: {player.stats['defense']}")