# fight.py - Pygame battle pop-up

import pygame
from pygame.locals import *
from combat import attack, apply_defend, apply_poison, apply_taunt, process_effects

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("arial", 30)

def draw_text(screen, text, color, x, y):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pygame_battle(game):
    print("Attempting to open Pygame window...")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cryptwalk Battle")
    clock = pygame.time.Clock()

    player = game["player"]
    enemy = game["enemy"]

    # Load enemy image (assume assets/goblin.png exists; add more for other types)
    enemy_type = enemy.name.lower()
    try:
        enemy_image = pygame.image.load(f"assets/{enemy_type}.png")
        enemy_image = pygame.transform.scale(enemy_image, (300, 300))
    except:
        enemy_image = None  # Fallback if no image

    enemy_rect = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 150, 300, 300) if enemy_image else None

    # For player sprite (use uploaded blue character sprite sheet later; static for now)
    # Placeholder: No image yet, just stats

    message = ""
    player_turn = True
    running = True

    while running and player.is_alive() and enemy.is_alive():
        screen.fill(BLACK)

        # Draw enemy
        if enemy_image:
            screen.blit(enemy_image, enemy_rect)

        # Draw stats
        draw_text(screen, f"{player.name} HP: {player.stats['hp']}/{player.stats['max_hp']}", WHITE, 50, 50)
        draw_text(screen, f"{enemy.name} HP: {enemy.stats['hp']}/{enemy.stats['max_hp']}", WHITE, SCREEN_WIDTH - 300, 50)
        draw_text(screen, message, RED, 50, 100)

        # HP bars
        hp_bar_width = 200
        hp_bar_height = 20

        # Player HP bar
        pygame.draw.rect(screen, RED, (50, 80, hp_bar_width, hp_bar_height))
        player_hp_ratio = player.stats["hp"] / player.stats["max_hp"] if player.stats["max_hp"] > 0 else 0
        pygame.draw.rect(screen, GREEN, (50, 80, hp_bar_width * player_hp_ratio, hp_bar_height))

        # Enemy HP bar
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 250, 80, hp_bar_width, hp_bar_height))
        enemy_hp_ratio = enemy.stats["hp"] / enemy.stats["max_hp"] if enemy.stats["max_hp"] > 0 else 0
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 250, 80, hp_bar_width * enemy_hp_ratio, hp_bar_height))

        # Instructions
        draw_text(screen, "Press 1: Attack | 2: Defend | 3: Poison | 4: Taunt | ESC: Quit", WHITE, 50, SCREEN_HEIGHT - 50)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            elif event.type == KEYDOWN and player_turn:
                if event.key == K_1:
                    attack(game, "player", "enemy")
                    message = game["combat_log"][-1]
                elif event.key == K_2:
                    apply_defend(player)
                    message = "You brace for impact!"
                    game["combat_log"].append(message)
                elif event.key == K_3:
                    apply_poison(game, enemy)
                    message = game["combat_log"][-1]
                elif event.key == K_4:
                    apply_taunt(game, enemy)
                    message = game["combat_log"][-1]
                player_turn = False

        if not player_turn and enemy.is_alive():
            # Enemy turn
            attack(game, "enemy", "player")
            message = game["combat_log"][-1]
            process_effects(game, "player")  # Apply effects to player
            process_effects(game, "enemy")   # Apply effects to enemy
            player_turn = True

    # End battle screen
    screen.fill(BLACK)
    if player.is_alive():
        draw_text(screen, "Victory!", GREEN, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    else:
        draw_text(screen, "Defeat...", RED, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)  # Show for 2 seconds

    pygame.quit()
    print("Pygame window closed.")
# No standalone run here—called from cryptwalk.py