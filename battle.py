import sys
sys.path.append(".")

import pygame
import random
from enemies import create_enemy
from combat import calculate_damage

def run_battle(player):
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Battle: Hero vs Enemy")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

    # Random enemy
    possible_enemies = ["goblin", "skeleton", "orc"]
    enemy_type = random.choice(possible_enemies)
    enemy_image = pygame.image.load(f"assets/{enemy_type}.png")
    enemy_image = pygame.transform.scale(enemy_image, (200, 200))
    enemy_rect = enemy_image.get_rect(center=(600, 300))

    enemy = create_enemy(enemy_type)
    enemy_name = enemy.name
    enemy_hp = enemy.stats["hp"]
    enemy_max_hp = enemy.stats["max_hp"]

    # Player sprite
    player_image = pygame.image.load("assets/player.png")
    player_image = pygame.transform.scale(player_image, (200, 200))
    player_rect = player_image.get_rect(center=(200, 300))

    player_name = player.name
    player_hp = player.stats["hp"]
    player_max_hp = player.stats["max_hp"]

    # Menu
    font = pygame.font.SysFont("arial", 36)
    menu_options = ["Attack", "Defend", "Item", "Run"]
    selected = 0

    player_turn = True
    damage_text = ""
    damage_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return "quit", 0, 0
            if player_turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    if event.key == pygame.K_RETURN:
                        if selected == 0:  # Attack
                            dmg = calculate_damage(player, enemy)
                            enemy.take_damage(dmg)
                            damage_text = f"Hit for {dmg}!"
                            damage_timer = 60
                            player_turn = False
                        elif selected == 1:  # Defend
                            player.apply_defend()
                            damage_text = "Defending!"
                            damage_timer = 60
                            player_turn = False
                        elif selected == 2:  # Item
                            # Simple potion use for now (expand later)
                            if player.inventory:
                                item = player.inventory[0]
                                item.use(player)
                                damage_text = f"Used {item.name}!"
                                player.inventory.pop(0)
                            else:
                                damage_text = "No items!"
                            damage_timer = 60
                            player_turn = False
                        elif selected == 2:  # Run
                            if random.random() < 0.6:
                                pygame.quit()
                                return "run", 0, 0
                            else:
                                damage_text = "Failed to run!"
                                damage_timer = 60
                                player_turn = False

        # Enemy turn
        if not player_turn and enemy.is_alive():
            dmg = calculate_damage(enemy, player)
            player.take_damage(dmg)
            damage_text = f"Enemy hit for {dmg}!"
            damage_timer = 60
            player_turn = True

        # Check win/lose
        if not enemy.is_alive():
            gold = enemy.gold_reward
            exp = random.randint(20, 50)
            pygame.quit()
            return "win", gold, exp
        if not player.is_alive():
            pygame.quit()
            return "lose", 0, 0

        screen.fill(BLACK)

        # Player
        screen.blit(player_image, player_rect)
        player_name_text = font.render(player_name, True, WHITE)
        screen.blit(player_name_text, (player_rect.centerx - player_name_text.get_width() // 2, 50))
        player_ratio = player_hp / player_max_hp
        pygame.draw.rect(screen, RED, (player_rect.centerx - 120, 520, 240, 25))
        pygame.draw.rect(screen, GREEN, (player_rect.centerx - 120, 520, 240 * player_ratio, 25))
        player_hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, WHITE)
        screen.blit(player_hp_text, (player_rect.centerx - player_hp_text.get_width() // 2, 555))

        # Enemy
        screen.blit(enemy_image, enemy_rect)
        enemy_name_text = font.render(enemy_name, True, WHITE)
        screen.blit(enemy_name_text, (enemy_rect.centerx - enemy_name_text.get_width() // 2, 50))
        enemy_ratio = enemy_hp / enemy_max_hp
        pygame.draw.rect(screen, RED, (enemy_rect.centerx - 120, 520, 240, 25))
        pygame.draw.rect(screen, GREEN, (enemy_rect.centerx - 120, 520, 240 * enemy_ratio, 25))
        enemy_hp_text = font.render(f"HP: {enemy_hp}/{enemy_max_hp}", True, WHITE)
        screen.blit(enemy_hp_text, (enemy_rect.centerx - enemy_hp_text.get_width() // 2, 555))

        # Menu
        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected else WHITE
            menu_text = font.render(option, True, color)
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 450 + i * 40))

        # Damage text
        if damage_timer > 0:
            dmg_text = font.render(damage_text, True, YELLOW)
            screen.blit(dmg_text, (SCREEN_WIDTH // 2 - dmg_text.get_width() // 2, 200))
            damage_timer -= 1

        pygame.display.flip()
        clock.tick(60)

### Updated cryptwalk.py (Full File)```python
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
from battle import run_battle  # Added import for graphical battle

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
        outcome, gold, exp = run_battle(game["player"])
        if outcome == "win":
            game["player"].gold += gold
            game["player"].gain_exp(exp)
            print(f"\nVictory! Gained {gold} gold and {exp} EXP!")
        elif outcome == "run":
            print("\nYou ran away!")
        elif outcome == "lose":
            print("\nYou were defeated...")
            game["running"] = False  # Game over
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