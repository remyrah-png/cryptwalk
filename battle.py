import sys
sys.path.append(".")

import pygame
import random
from enemies import create_enemy
from combat import calculate_damage  # Your damage function

def run_battle(player):
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crypt Encounter")
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
    enemy_image = enemy_image.subsurface((0, 0, 32, 32))  # Crop first frame
    enemy_image = pygame.transform.scale(enemy_image, (200, 200))
    enemy_rect = enemy_image.get_rect(center=(600, 300))

    enemy = create_enemy(enemy_type)

    # Player
    player_image = pygame.image.load("assets/player.png")
    player_image = player_image.subsurface((0, 0, 32, 32))
    player_image = pygame.transform.scale(player_image, (200, 200))
    player_rect = player_image.get_rect(center=(200, 300))

    # Menu
    font = pygame.font.SysFont("arial", 36)
    menu_options = ["Attack", "Defend", "Run"]
    selected = 0

    player_turn = True
    damage_text = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
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
                        player_turn = False
                    elif selected == 1:  # Defend
                        player.defending = True
                        player_turn = False
                    elif selected == 2:  # Run
                        pygame.quit()
                        return "run", 0, 0

        if not player_turn and enemy.is_alive():
            dmg = calculate_damage(enemy, player)
            player.take_damage(dmg)
            damage_text = f"Enemy hit for {dmg}!"
            player_turn = True

        if not enemy.is_alive():
            gold = enemy.gold_reward
            exp = random.randint(20, 50)
            pygame.quit()
            return "win", gold, exp
        if not player.is_alive():
            pygame.quit()
            return "lose", 0, 0

        screen.fill(BLACK)

        # Draw player left
        screen.blit(player_image, player_rect)
        player_name_text = font.render(player.name, True, WHITE)
        screen.blit(player_name_text, (player_rect.centerx - player_name_text.get_width() // 2, 50))
        player_ratio = player.stats["hp"] / player.stats["max_hp"]
        pygame.draw.rect(screen, RED, (player_rect.centerx - 120, 520, 240, 25))
        pygame.draw.rect(screen, GREEN, (player_rect.centerx - 120, 520, 240 * player_ratio, 25))
        player_hp_text = font.render(f"HP: {player.stats['hp']}/{player.stats['max_hp']}", True, WHITE)
        screen.blit(player_hp_text, (player_rect.centerx - player_hp_text.get_width() // 2, 555))

        # Draw enemy right
        screen.blit(enemy_image, enemy_rect)
        enemy_name_text = font.render(enemy.name, True, WHITE)
        screen.blit(enemy_name_text, (enemy_rect.centerx - enemy_name_text.get_width() // 2, 50))
        enemy_ratio = enemy.stats["hp"] / enemy.stats["max_hp"]
        pygame.draw.rect(screen, RED, (enemy_rect.centerx - 120, 520, 240, 25))
        pygame.draw.rect(screen, GREEN, (enemy_rect.centerx - 120, 520, 240 * enemy_ratio, 25))
        enemy_hp_text = font.render(f"HP: {enemy.stats['hp']}/{enemy.stats['max_hp']}", True, WHITE)
        screen.blit(enemy_hp_text, (enemy_rect.centerx - enemy_hp_text.get_width() // 2, 555))

        # Menu
        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 450 + i * 40))

        # Damage text
        if damage_text:
            dmg_text = font.render(damage_text, True, YELLOW)
            screen.blit(dmg_text, (SCREEN_WIDTH // 2 - dmg_text.get_width() // 2, 200))
            damage_text = ""  # Clear after one frame

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return "quit", 0, 0