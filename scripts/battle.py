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
    SCREEN_WIDTH = 1200  # Increased for better layout
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cryptwalk Battle")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BG_COLOR = (20, 20, 20)  # Dark background

    font = pygame.font.SysFont("arial", 40)
    small_font = pygame.font.SysFont("arial", 24)

    # Player animation (using combined sheet)
    player_idle_path = "assets/ForestRanger/Forest_Ranger_1/PNG/PNG Sequences/Idle/Idle.png"
    try:
        player_sheet = pygame.image.load(player_idle_path)
        player_frame_width = 128  # From your assets
        player_frame_height = 96
        player_frame_count = player_sheet.get_width() // player_frame_width  # Auto-detect
        player_frames = [player_sheet.subsurface((i * player_frame_width, 0, player_frame_width, player_frame_height)) for i in range(player_frame_count)]
        player_frames = [pygame.transform.scale(frame, (250, 250)) for frame in player_frames]  # Scale up
    except Exception as e:
        print(f"Player load error: {e}")
        player_frames = [pygame.Surface((250, 250)).convert()] * 4
        player_frames[0].fill((0, 128, 255))  # Blue placeholder
    player_rect = player_frames[0].get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))
    player_frame_index = 0
    player_anim_timer = 0
    player_anim_speed = 100  # ms per frame

    # Enemy animation
    enemy = game["enemy"]
    enemy_type = enemy.name.lower()
    enemy_idle_path = f"assets/{enemy_type.capitalize()}/PNG/PNG Sequences/Idle/Idle.png"  # Assume similar structure
    try:
        enemy_sheet = pygame.image.load(enemy_idle_path)
        enemy_frame_width = 128  # Adjust if different
        enemy_frame_height = 96
        enemy_frame_count = enemy_sheet.get_width() // enemy_frame_width
        enemy_frames = [enemy_sheet.subsurface((i * enemy_frame_width, 0, enemy_frame_width, enemy_frame_height)) for i in range(enemy_frame_count)]
        enemy_frames = [pygame.transform.scale(frame, (250, 250)) for frame in enemy_frames]
        enemy_frames = [pygame.transform.flip(frame, True, False) for frame in enemy_frames]  # Face left
    except Exception as e:
        print(f"Enemy load error: {e}")
        enemy_frames = [pygame.Surface((250, 250)).convert()] * 4
        enemy_frames[0].fill((0, 255, 0))  # Green placeholder
    enemy_rect = enemy_frames[0].get_rect(center=(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2 + 50))
    enemy_frame_index = 0
    enemy_anim_timer = 0
    enemy_anim_speed = 100

    player_turn = game["active_turn"] == "player"

    running = True
    while running and enemy.is_alive() and game["player"].is_alive():
        current_time = pygame.time.get_ticks()

        # Animate player
        if current_time - player_anim_timer > player_anim_speed:
            player_anim_timer = current_time
            player_frame_index = (player_frame_index + 1) % len(player_frames)

        # Animate enemy
        if current_time - enemy_anim_timer > enemy_anim_speed:
            enemy_anim_timer = current_time
            enemy_frame_index = (enemy_frame_index + 1) % len(enemy_frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and player_turn:
                if event.key == pygame.K_a:
                    dmg = attack(game, "player", "enemy")
                    print(f"Debug: Player attack dmg = {dmg}")  # Debug
                    player_turn = False
                elif event.key == pygame.K_d:
                    apply_defend(game["player"])
                    game["combat_log"].append("You defend!")
                    player_turn = False
                elif event.key == pygame.K_p:
                    apply_poison(game, game["enemy"])
                    player_turn = False
                elif event.key == pygame.K_e:
                    apply_enrage(game, game["player"])  # Or enemy, depending on intent
                    player_turn = False
                elif event.key == pygame.K_i:
                    # Item logic (e.g., heal)
                    if healing_potion in game["player"].inventory:
                        healing_potion.use(game["player"])
                        game["player"].inventory.remove(healing_potion)
                    player_turn = False

        if not player_turn:
            # Enemy turn
            enemy_action = random.choice(["attack", "defend", "poison"])
            if enemy_action == "attack":
                dmg = attack(game, "enemy", "player")
                print(f"Debug: Enemy attack dmg = {dmg}")  # Debug
            elif enemy_action == "defend":
                apply_defend(enemy)
                game["combat_log"].append(f"{enemy.name} defends!")
            elif enemy_action == "poison":
                apply_poison(game, game["player"])
            process_effects(game, "player")
            player_turn = True

        process_effects(game, "enemy")

        # Render
        screen.fill(BG_COLOR)

        # Player
        screen.blit(player_frames[player_frame_index], player_rect)
        p_name = font.render("Hero", True, WHITE)
        screen.blit(p_name, (player_rect.centerx - p_name.get_width() // 2, player_rect.top - 50))
        p_ratio = max(0, game["player"].stats["hp"] / game["player"].stats["max_hp"])
        pygame.draw.rect(screen, RED, (player_rect.left, player_rect.bottom + 20, 250, 30))
        pygame.draw.rect(screen, GREEN, (player_rect.left, player_rect.bottom + 20, 250 * p_ratio, 30))
        hp_text = small_font.render(f"HP: {game['player'].stats['hp']}/{game['player'].stats['max_hp']}", True, WHITE)
        screen.blit(hp_text, (player_rect.centerx - hp_text.get_width() // 2, player_rect.bottom + 55))

        # Enemy
        screen.blit(enemy_frames[enemy_frame_index], enemy_rect)
        e_name = font.render(enemy.name, True, WHITE)
        screen.blit(e_name, (enemy_rect.centerx - e_name.get_width() // 2, enemy_rect.top - 50))
        e_ratio = max(0, enemy.stats["hp"] / enemy.stats["max_hp"])
        pygame.draw.rect(screen, RED, (enemy_rect.left, enemy_rect.bottom + 20, 250, 30))
        pygame.draw.rect(screen, GREEN, (enemy_rect.left, enemy_rect.bottom + 20, 250 * e_ratio, 30))
        hp_text = small_font.render(f"HP: {enemy.stats['hp']}/{enemy.stats['max_hp']}", True, WHITE)
        screen.blit(hp_text, (enemy_rect.centerx - hp_text.get_width() // 2, enemy_rect.bottom + 55))

        # Controls
        ctrl_text = small_font.render("A:Attack D:Defend P:Poison E:Enrage I:Item  (Your turn!)" if player_turn else "--- Enemy Turn ---", True, WHITE)
        screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, 20))

        # Combat log (last 5 lines)
        for i, log in enumerate(game["combat_log"][-5:]):
            log_text = small_font.render(log, True, WHITE)
            screen.blit(log_text, (20, SCREEN_HEIGHT - 150 + i * 25))

        pygame.display.flip()
        clock.tick(60)

    # Post-battle
    if game["player"].is_alive():
        game["player"].gold += random.randint(8, 15) + game["world"]["depth"]
        game["combat_log"].append("Victory! Gained gold.")
    else:
        game["combat_log"].append("Defeat!")
    game["enemy"] = None
    pygame.quit()

# Standalone test
if __name__ == "__main__":
    # Mock game for testing
    game["enemy"] = create_enemy("goblin")
    run_pygame_battle(game)