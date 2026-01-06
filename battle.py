import sys
sys.path.append(".")

import pygame
from enemies import create_enemy

def run_battle():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My RPG Battle")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 0, 0)

    enemy_type = "goblin"  # Change to "skeleton" or "orc" to test!

    enemy_image = pygame.image.load(f"assets/{enemy_type}.png")
    enemy_image = pygame.transform.scale(enemy_image, (300, 300))

    enemy_rect = enemy_image.get_rect()
    enemy_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

    enemy = create_enemy(enemy_type)
    enemy_name = enemy.name
    enemy_hp = enemy.stats["hp"]
    enemy_max_hp = enemy.stats["max_hp"]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill(BLACK)
        screen.blit(enemy_image, enemy_rect)

        font = pygame.font.SysFont("arial", 40)
        name_text = font.render(enemy_name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 80))

        hp_bar_width = 400
        hp_bar_height = 40
        hp_ratio = enemy_hp / enemy_max_hp if enemy_max_hp > 0 else 0
        pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - hp_bar_width // 2, 480, hp_bar_width, hp_bar_height))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - hp_bar_width // 2, 480, hp_bar_width * hp_ratio, hp_bar_height))
    
        hp_text = font.render(f"HP: {enemy_hp}/{enemy_max_hp}", True, WHITE)
        screen.blit(hp_text, (SCREEN_WIDTH // 2 - hp_text.get_width() // 2, 530))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return "win", 10, 20  # Return outcome, gold, exp - adjust as needed

if __name__ == "__main__":
    run_battle()