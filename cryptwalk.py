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
    player = game["player"]
    p_hp = player.stats["hp"]
    p_max = player.stats["max_hp"]
    print(f"HERO : {bar(p_hp, p_max)} {p_hp}/{p_max} HP   Gold: {player.gold}".center(50))

    if mode == "combat" and game["enemy"]:
        e = game["enemy"]
        e_hp = e.stats["hp"]
        e_max = e.stats["max_hp"]
        print(f"ENEMY: {bar(e_hp, e_max)} {e_hp}/{e_max} HP ({e.name})".center(50))

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
    game["combat_log"].append(f"{game['enemy'].name} attacks!")


def run_combat(game):
    pygame.init()  # Start Pygame
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cryptwalk Battle")
    clock = pygame.time.Clock()
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    
    font = pygame.font.SysFont("arial", 40)  # For text
    
    print("\n⚔ A Goblin ambushes you!")
    input("Press Enter to begin combat...")
    
    depth = game["world"]["depth"]
    scale = 1 + depth * .1  # +10% stats per level deeper
    game["enemy"] = CombatEntity("Goblin", 20, 20, 6, 2)
    game["combat_log"].clear()
    game["turn"] = 1
    
    running = True  # Pygame loop control
    while running and game["player"].is_alive() and game["enemy"] and game["enemy"].stats["hp"] > 0:
        # Process events (e.g., close window)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                game["running"] = False  # Exit game if window closed
        
        # Game logic (your original loop)
        process_effects(game, "enemy")
        process_effects(game, "player")
        
        if game["enemy"].stats["hp"] <= 0 or not game["player"].is_alive():
            break
        
        render_screen(game, mode="combat")  # Keep text render
        
        if game["active_turn"] == "player":
            player_turn(game)
            game["active_turn"] = "enemy"
        
        if game["active_turn"] == "enemy" and game["enemy"] and game["enemy"].stats["hp"] > 0:
            enemy_turn(game)
            game["active_turn"] = "player"
        
        game["turn"] += 1
        
        # Draw Pygame popup (simple HP bar, enemy name)
        screen.fill(BLACK)
        name_text = font.render(game["enemy"].name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 80))
        
        hp_bar_width = 400
        hp_bar_height = 40
        hp_ratio = game["enemy"].stats["hp"] / game["enemy"].stats["max_hp"] if game["enemy"].stats["max_hp"] > 0 else 0
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - hp_bar_width // 2, 480, hp_bar_width, hp_bar_height))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - hp_bar_width // 2, 480, hp_bar_width * hp_ratio, hp_bar_height))
        
        hp_text = font.render(f"HP: {game['enemy'].stats['hp']}/{game['enemy'].stats['max_hp']}", True, WHITE)
        screen.blit(hp_text, (SCREEN_WIDTH // 2 - hp_text.get_width() // 2, 530))
        
        pygame.display.flip()  # Update window
        clock.tick(30)  # 30 FPS, non-blocking
    
    # Victory/defeat (your code)
    if game["player"].is_alive():
        game["combat_log"].append("Goblin defeated!")
        render_screen(game, mode="combat")
        input("\nVictory! Press Enter...")
        game["player"].gold += 10
        print("\nSearching the body...")
        if random() < 0.6:
            loot = choice([healing_potion, iron_sword, leather_armor])
            game["player"].inventory.append(loot)
            print(f"You found a {loot.name}! Added to inventory.")
        else:
            print("Nothing useful found.")
    
    else:
        game["player"].is_alive = False
        render_screen(game, mode="combat")
        input("\nYou have been defeated...")
    
    game["enemy"] = None
    pygame.quit()  # Clean up Pygame

def roll_encounter():
    return random() < 0.5



def move_forward(game):
    # Increase depth — this is your "progress"
    game["world"]["depth"] += 1
    depth = game["world"]["depth"]

    # Procedural room generation
    adjectives = ["Echoing", "Moldy", "Bone-Lined", "Spider-Infested", "Blood-Stained",
                  "Collapsed", "Flickering", "Silent", "Damp", "Forgotten"]
    nouns = ["Chamber", "Hall", "Vault", "Passage", "Crypt", "Tomb", "Gallery"]

    adj = choice(adjectives)
    nouns = choice(nouns)
    room_name = f"The {adj} {nouns}"

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
    room_desc = choice(descriptions)

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

    if random() < encounter_chance:
        print("\nSomething stirs in the shadows...")
        input("Press Enter to fight...")
        run_combat(game)
    else:
        print("\n...The room is empty. For now.")

def rest(game):
    heal = 8
    before = game["player"].stats["hp"]
    game["player"].stats["hp"] = min(game["player"].stats["max_hp"], before + heal)
    gained = game["player"].stats["hp"] - before
    print(f"\nYou rest and recover {gained} HP.")


def use_inventory(game):
    inv = game["player"].inventory
    if not inv:
        print("\nYour inventory is empty.")
        input("Press Enter...")
        return

    print("\nInventory:")
    for i, item in enumerate(inv):
        equipped = ""
        if item is game["player"].weapon:
            equipped = " (equipped weapon)"
        elif item is game["player"].armor:
            equipped = " (equipped armor)"
        print(f"{i+1}) {item.name} ({item.type}{equipped})")

    choice = input("\nUse/equip item number (or Enter to cancel): ").strip()
    if not choice.isdigit():
        return

    idx = int(choice) - 1
    if not (0 <= idx < len(inv)):
        print("Invalid number.")
        input("Press Enter...")
        return

    item = inv[idx]

    if item.type == "potion":
        healed = game["player"].stats["hp"]
        game["player"].stats["hp"] = min(game["player"].stats["max_hp"], game["player"].stats["hp"] + item.value)
        healed = game["player"].stats["hp"] - healed
        print(f"\nYou drink {item.name} and recover {healed} HP!")
        inv.remove(item)  # consume potion
    elif item.type == "weapon":
        if game["player"].weapon == item:
            print(f"{item.name} is already equipped.")
        else:
            game["player"].weapon = item
            game["player"].stats["strength"] += item.value
            print(f"\nYou equip {item.name} (+{item.value} strength)!")
    elif item.type == "armor":
        if game["player"].armor == item:
            print(f"{item.name} is already equipped.")
        else:
            game["player"].armor = item
            game["player"].stats["defense"] += item.value
            print(f"\nYou equip {item.name} (+{item.value} defense)!")
    else:
        print("Can't use that item.")

    input("Press Enter...")


def main():
    print("Welcome to Cryptwalk")
    input("Press Enter to begin your descent...")

    # Give starting item for testing
    game["player"].inventory.append(healing_potion)
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