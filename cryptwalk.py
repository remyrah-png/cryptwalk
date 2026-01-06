# cryptwalk.py - Main game file
import os
import random
from random import random, choice # Added import
from items import healing_potion, iron_sword, leather_armor # Added import
from player import Player
from entity import CombatEntity 
from combat import (
    attack, apply_defend, apply_poison, apply_taunt,
    process_effects, calculate_damage
)
from battle import run_battle  # Added for graphical pop-up

TEST_MODE = True

game = {
    "turn": 1,
    "combat_log": [],
    "active_turn": "player",
    "running": True,

    "player": Player(),

"world":{
    "depth": 0,
    "current_room": {
    "name": "Crypt Entrance",
    "desc": "Cold air spills from a cracked stone doorway. The adventure begins."
        }
    },

    "enemy": None,
}

def bar(current, maximum, width=20):
    filled = int((current / maximum) * width) if maximum > 0 else 0
    filled_bar = '#' * filled
    empty_bar = '-' * (width - filled)
    return f"[{filled_bar}{empty_bar}] {current}/{maximum}"

def render_screen(game, mode="explore"):
    if mode == "explore":
        print("============== Cryptwalk ==============")
        print(f"Depth: {game['world']['depth']}")
        print(f"Room: {game['world']['current_room']['name']}")
        print(game['world']['current_room']['desc'])
        print(f"\nPlayer HP: {bar(game['player'].stats['hp'], game['player'].stats['max_hp'])}")
        print(f"Gold: {game['player'].gold} | EXP: {game['player'].exp} | Level: {game['player'].level}")

    elif mode == "combat":
        print("============== Combat ==============")
        print(f"Turn: {game['turn']} ({game['active_turn'].capitalize()}'s turn)")
        print("\nPlayer:")
        print(f"HP: {bar(game['player'].stats['hp'], game['player'].stats['max_hp'])}")
        print(f"Strength: {game['player'].stats['strength']} | Defense: {game['player'].stats['defense']}")
        print(f"Effects: {game['player'].effects}")

        print("\nEnemy:")
        print(f"Name: {game['enemy'].name}")
        print(f"HP: {bar(game['enemy'].stats['hp'], game['enemy'].stats['max_hp'])}")
        print(f"Strength: {game['enemy'].stats['strength']} | Defense: {game['enemy'].stats['defense']}")
        print(f"Effects: {game['enemy'].effects}")

        if game['combat_log']:
            print("\nCombat Log:")
            for log in game['combat_log'][-3:]:  # Last 3 logs
                print(log)

def generate_room(game):
    depth = game['world']['depth']
    rooms = [
        "Dusty Chamber",
        "Flooded Hallway",
        "Skeleton Room",
        "Treasure Vault",
        "Dark Altar"
    ]
    descs = [
        "Cobwebs hang from the ceiling.",
        "Water drips from cracks in the walls.",
        "Bones scatter the floor.",
        "Glimmering gold catches your eye.",
        "An ominous altar stands in the center."
    ]
    game['world']['current_room'] = {
        "name": random.choice(rooms),
        "desc": random.choice(descs)
    }

def move_forward(game):
    game['world']['depth'] += 1
    generate_room(game)
    encounter_chance = 0.6 + (game['world']['depth'] * 0.05)
    if random() < encounter_chance:
        print("\nSomething stirs in the shadows...")
        input("Press Enter to fight...")
        outcome, gold, exp = run_battle()
        if outcome == "win":
            game["player"].gold += gold
            game["player"].gain_exp(exp)
            print(f"\nVictory! Gained {gold} gold and {exp} EXP!")
        elif outcome == "run":
            print("\nYou ran away!")
        elif outcome == "lose":
            print("\nYou were defeated...")
            game["running"] = False
    else:
        print("\n...The room is empty. For now.")

def rest(game):
    heal_amount = 8
    game["player"].heal(heal_amount)
    print(f"You rest and recover {heal_amount} HP.")

def use_inventory(game):
    print("\nInventory:")
    for i, item in enumerate(game["player"].inventory, 1):
        print(f"{i} ) {item.name}")

    choice = input("\nUse item (number) or Enter to cancel: ").strip()

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(game["player"].inventory):
            item = game["player"].inventory.pop(idx)
            item.use(game["player"])
            print(f"Used {item.name}.")

def main():
    if TEST_MODE:
        # Test mode: Start with items
        game["player"].inventory = [healing_potion, iron_sword, leather_armor]

    while game["running"] and game["player"].is_alive():
        render_screen(game, mode="explore")

        print("\nWhat do you do?")
        print("1) Move forward")
        print("2) Rest (+8 HP)")
        print("3) Inventory")
        print("4) Status")
        print("5) Quit")

        choice = input("\n> ").strip()

        if choice == "1":
            move_forward(game)
        elif choice == "2":
            rest(game)
        elif choice == "3":
            use_inventory(game)
        elif choice == "4":
            render_screen(game, mode="explore")
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("\nYou escape the crypt alive...")
            game["running"] = False

    if not game["player"].is_alive():
        print("\nGame Over")

if __name__ == "__main__":
    main()