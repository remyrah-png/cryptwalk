import pygame
import random
import sys
sys.path.append(".")  # For local imports

from cryptwalk import game  # For fallback testing
from combat import attack, apply_defend, apply_poison, apply_enrage, process_effects
from enemies import create_enemy
from entity import CombatEntity

def run_pygame_battle(game):
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cryptwalk Battle")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Load images (fallback if missing)
    try:
        enemy_type = game["enemy"].name.lower() if game["enemy"] else "goblin"
        enemy_image = pygame.image.load(f"assets/{enemy_type.capitalize()}/PNG/PNG Sequences/Idle/Idle_001.png")
        enemy_image = pygame.transform.scale(enemy_image, (200, 200))
        enemy_image = pygame.transform.flip(enemy_image, True, False)
    except:
        enemy_image = pygame.Surface((200, 200))
        enemy_image.fill((0, 255, 0))
    enemy_rect = enemy_image.get_rect(center=(SCREEN_WIDTH//2 + 250, SCREEN_HEIGHT//2))

    try:
        player_image = pygame.image.load("assets/ForrestRanger/Forest_Ranger_1/PNG/PNG Sequences/Idle/0_Forest_Ranger_Idle_000.png")
        player_image = pygame.transform.scale(player_image, (200, 200))
    except:
        player_image = pygame.Surface((200, 200))
        player_image.fill((0, 128, 255))
    player_rect = player_image.get_rect(center=(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2))

    font = pygame.font.SysFont("arial", 40)
    small_font = pygame.font.SysFont("arial", 28)

    player_turn = True
    running = True
    while running and game["player"].is_alive() and game["enemy"] and game["enemy"].is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and player_turn:
                if event.key == pygame.K_a:  # Attack
                    attack(game, "player", "enemy")
                    process_effects(game, "enemy")
                    player_turn = False
                elif event.key == pygame.K_d:  # Defend
                    apply_defend(game["player"])
                    game["combat_log"].append("You defend!")
                    player_turn = False
                elif event.key == pygame.K_p:  # Poison
                    apply_poison(game, game["enemy"])
                    player_turn = False
                elif event.key == pygame.K_e:  # Enrage (taunt enemy)
                    apply_enrage(game, game["enemy"])
                    player_turn = False
                elif event.key == pygame.K_i:  # Inventory (simple: use first potion if any)
                    if game["player"].inventory:
                        item = game["player"].inventory[0]
                        if item.use(game["player"]):
                            game["player"].inventory.pop(0)
                        game["combat_log"].append(f"Used {item.name}!")
                    else:
                        game["combat_log"].append("No items!")
                    player_turn = False

        # Enemy AI (simple: random action)
        if not player_turn:
            actions = [pygame.K_a, pygame.K_d, pygame.K_p]  # Enemy attacks/defends/poisons
            ai_action = random.choice(actions)
            if ai_action == pygame.K_a:
                attack(game, "enemy", "player")
            elif ai_action == pygame.K_d:
                apply_defend(game["enemy"])
                game["combat_log"].append("Enemy defends!")
            else:
                apply_poison(game, game["player"])
            process_effects(game, "player")
            player_turn = True

        # Render
        screen.fill(BLACK)
        screen.blit(player_image, player_rect)
        screen.blit(enemy_image, enemy_rect)

        player = game["player"]
        enemy = game["enemy"]
        # Player HP bar/name
        name_text = font.render(player.name, True, WHITE)
        screen.blit(name_text, (150 - name_text.get_width()//2, 50))
        p_ratio = player.stats["hp"] / player.stats["max_hp"]
        pygame.draw.rect(screen, RED, (100, 450, 200, 30))
        pygame.draw.rect(screen, GREEN, (100, 450, 200 * p_ratio, 30))
        hp_text = small_font.render(f"HP: {player.stats['hp']}/{player.stats['max_hp']}", True, WHITE)
        screen.blit(hp_text, (100, 485))

        # Enemy HP bar/name
        name_text = font.render(enemy.name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH - 350 + name_text.get_width()//2, 50))
        e_ratio = enemy.stats["hp"] / enemy.stats["max_hp"]
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 300, 450, 200, 30))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 300, 450, 200 * e_ratio, 30))
        hp_text = small_font.render(f"HP: {enemy.stats['hp']}/{enemy.stats['max_hp']}", True, WHITE)
        screen.blit(hp_text, (SCREEN_WIDTH - 300, 485))

        # Controls & Log
        ctrl_text = small_font.render("A:Attack D:Defend P:Poison E:Enrage I:Item  (Your turn!)" if player_turn else "--- Enemy Turn ---", True, WHITE)
        screen.blit(ctrl_text, (20, 20))
        for i, log in enumerate(game["combat_log"][-3:]):
            log_text = small_font.render(log, True, WHITE)
            screen.blit(log_text, (20, SCREEN_HEIGHT - 120 + i * 25))

        pygame.display.flip()
        clock.tick(60)

    # Post-battle
    if game["player"].is_alive():
        game["player"].gold += random.randint(8, 15) + game["world"]["depth"]
        game["combat_log"].append("Victory! Gained gold.")
        game["enemy"] = None
    else:
        game["combat_log"].append("Defeat!")
        game["enemy"] = None
        # Optional: game["running"] = False

    pygame.quit()

# Standalone test: if __name__ == "__main__": run_pygame_battle(game)