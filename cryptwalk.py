# cryptwalk.py - Main game file
import os
import random
from combat import (
    attack, apply_defend, apply_poison, apply_taunt,
    process_effects, calculate_damage
)

TEST_MODE = True

game = {
    "turn": 1,
    "combat_log": [],
    "active_turn": "player",
    "running": True,

    "player": {
        "name": "Hero",
        "stats": {"hp": 35, "max_hp": 35, "strength": 10, "defense": 5},
        "alive": True,
        "effects": [],
        "weapon": None,
        "armor": None,
        "inventory": [],
        "gold": 0,
    },

    "world": {
        "depth": 0,
        "current_room": {
            "name": "Crypt Entrance",
            "desc": "Cold air spills from a cracked stone doorway. The adventure begins."
        }
    },   # ← COMMA HERE

    "enemy": None,
}








def bar(current, maximum, width=20):
    filled = int((current / maximum) * width) if maximum > 0 else 0
    filled = max(0, min(width, filled))
    return "#" * filled + "_" * (width - filled)


def clear_screen():
    os.system("clear")


def render_screen(game, mode="explore"):
    clear_screen()
    player = game["player"]
    room = game["world"]["current_room"]

    print("=" * 50)
    print(f" {room['name']}".center(50))
    print("=" * 50)
    print(f"{room['desc']}".center(50))
    print()

    if mode == "combat" and game["enemy"]:
        turn_text = ">>> YOUR TURN <<<" if game["active_turn"] == "player" else "--- ENEMY TURN ---"
        print(f"{turn_text.center(50)}")
        print()

    # HUD
    p_hp = player["stats"]["hp"]
    p_max = player["stats"]["max_hp"]
    print(f"HERO : {bar(p_hp, p_max)} {p_hp}/{p_max} HP   Gold: {player['gold']}".center(50))

    if mode == "combat" and game["enemy"]:
        e = game["enemy"]
        e_hp = e["stats"]["hp"]
        e_max = e["stats"]["max_hp"]
        print(f"ENEMY: {bar(e_hp, e_max)} {e_hp}/{e_max} HP ({e['name']})".center(50))

    print("-" * 50)

    # Recent events
    log = game["combat_log"]
    if log:
        print("Recent events:".center(50))
        for line in log[-3:]:
            print(f"  • {line}".center(50))
    print("=" * 50)

    if mode == "combat":
        print("Actions:".center(50))
        print("  1) Attack    2) Defend".center(50))
        print("  3) Poison    4) Taunt".center(50))
        print("-" * 50)


def player_turn(game):
    while True:
        choice = input("\nChoose action (1-4): ").strip()
        if choice == "1":
            attack(game, "player", "enemy")
            return
        elif choice == "2":
            apply_defend(game["player"])
            game["combat_log"].append("You brace for impact!")
            return
        elif choice == "3":
            apply_poison(game["enemy"], dmg_per_turn=1, turns=3)
            game["combat_log"].append("You poison the enemy!")
            return
        elif choice == "4":
            apply_taunt(game["player"], dmg_reduction=-2, turns=1)  # taunt self? Wait — actually you want enemy to taunt player?
            game["combat_log"].append("You taunt the enemy — it enrages and strikes harder? Wait, logic flip!")
            return
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


def enemy_turn(game):
    attack(game, "enemy", "player")
    game["combat_log"].append(f"{game['enemy']['name']} attacks!")


def run_combat(game):
    print("\n⚔ A Goblin ambushes you!")
    input("Press Enter to begin combat...")

    depth = game["world"]["depth"]
    scale = 1 + depth * .1 # +10% stats per level deeper

    game["enemy"] = {
        "name": "Goblin",
        "stats": {"hp": 20, "max_hp": 20, "strength": 6, "defense": 3},
        "defending": False,
        "effects": []
    }
    game["combat_log"].clear()
    game["turn"] = 1

    while game["player"]["alive"] and game["enemy"] and game["enemy"]["stats"]["hp"] > 0:
        render_screen(game, mode="combat")

        if game["active_turn"] == "player":
            player_turn(game)
            process_effects(game, "enemy")
            if game["enemy"]["stats"]["hp"] <= 0:
                game["combat_log"].append("Goblin defeated!")
                render_screen(game, mode="combat")
                input("\nVictory! Press Enter...")
                game["player"]["gold"] += 10
                game["enemy"] = None
                return

            game["active_turn"] = "enemy"

        if game["active_turn"] == "enemy":
            enemy_turn(game)
            process_effects(game, "player")
            if game["player"]["stats"]["hp"] <= 0:
                game["player"]["alive"] = False
                render_screen(game, mode="combat")
                input("\nYou have been defeated...")
                return

            game["active_turn"] = "player"
            game["turn"] += 1


def roll_encounter():
    return random.random() < 0.5



def move_forward(game):
    # Increase depth — this is your "progress"
    game["world"]["depth"] += 1
    depth = game["world"]["depth"]

    # Procedural room generation
    adjectives = ["Echoing", "Moldy", "Bone-Lined", "Spider-Infested", "Blood-Stained",
                  "Collapsed", "Flickering", "Silent", "Damp", "Forgotten"]
    nouns = ["Chamber", "Hall", "Vault", "Passage", "Crypt", "Tomb", "Gallery"]

    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    room_name = f"The {adj} {noun}"

    descriptions = [
        "The air tastes old and stale.",
        "Water drips from cracks overhead.",
        "Bones crunch beneath your boots.",
        "Cobwebs drape everything like funeral curtains.",
        "Faint scratching echoes from the walls.",
        "Torchlight reveals ancient carvings.",
        "A cold wind blows from deeper within.",
        "The floor is slick with moisture."
    ]
    room_desc = random.choice(descriptions)

    # Update current room
    game["world"]["current_room"] = {
        "name": room_name,
        "desc": room_desc
    }

    # Show the new room
    print(f"\nYou descend deeper... (Depth {depth})")
    print(f"You enter: {room_name}")
    print(room_desc)

    # Higher chance of encounter the deeper you go (optional scaling)
    encounter_chance = min(0.8, 0.4 + depth * 0.05)  # starts ~40%, maxes at 80%

    if random.random() < encounter_chance:
        print("\nSomething stirs in the shadows...")
        input("Press Enter to fight...")
        run_combat(game)
    else:
        print("\n...The room is empty. For now.")

def rest(game):
    heal = 8
    before = game["player"]["stats"]["hp"]
    game["player"]["stats"]["hp"] = min(game["player"]["stats"]["max_hp"], before + heal)
    gained = game["player"]["stats"]["hp"] - before
    print(f"\nYou rest and recover {gained} HP.")


def use_inventory(game):
    inv = game["player"]["inventory"]
    if not inv:
        print("\nYour inventory is empty.")
        input("Press Enter...")
        return

    print("\nInventory:")
    for i, item in enumerate(inv):
        print(f"{i+1}) {item['name']}")

    # Simple: use first potion or equip first weapon/armor
    for item in inv[:]:
        if item["type"] == "potion" and game["player"]["stats"]["hp"] < game["player"]["stats"]["max_hp"]:
            heal = item["heal"]
            before = game["player"]["stats"]["hp"]
            game["player"]["stats"]["hp"] = min(game["player"]["stats"]["max_hp"], before + heal)
            print(f"\nYou use {item['name']} (+{heal} HP)")
            inv.remove(item)
            input("Press Enter...")
            return
        elif item["type"] == "weapon" and not game["player"]["weapon"]:
            game["player"]["weapon"] = item
            inv.remove(item)
            print(f"\nEquipped {item['name']} (+{item['strength']} STR)")
            input("Press Enter...")
            return
        elif item["type"] == "armor" and not game["player"]["armor"]:
            game["player"]["armor"] = item
            inv.remove(item)
            print(f"\nEquipped {item['name']} (+{item['defense']} DEF)")
            input("Press Enter...")
            return

    print("\nNothing to use or equip right now.")
    input("Press Enter...")


def main():
    print("Welcome to Cryptwalk")
    input("Press Enter to begin your descent...")

    # Give starting item for testing
    game["player"]["inventory"].append({"type": "potion", "name": "Healing Potion", "heal": 12})

    while game["running"] and game["player"]["alive"]:
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

    if not game["player"]["alive"]:
        print("\nGame Over")

if __name__ == "__main__":
    main()
