import sys
sys.path.append("..")  # Adjust as necessary
from cryptwalk import game  # Import game dict
import pygame
from enemies import create_enemy

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My RPG Battle")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Enemy load
enemy = game["enemy"]
if enemy:
    enemy_type = enemy.name.lower()  # e.g., "goblin"
else:
    enemy_type = "goblin"  # Fallback
    enemy = create_enemy(enemy_type)

enemy_image = pygame.image.load(f"assets/{enemy_type.capitalize()}/PNG/PNG Sequences/Idle/Idle_001.png")
enemy_image = pygame.transform.scale(enemy_image, (200, 200))
enemy_image = pygame.transform.flip(enemy_image, True, False)  # Face left
enemy_rect = enemy_image.get_rect()
enemy_rect.center = (SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2 + 50)  # Right side

enemy_name = enemy.name
enemy_hp = enemy.stats["hp"]
enemy_max_hp = enemy.stats["max_hp"]

# Player load
player_image = pygame.image.load(f"assets/ForrestRanger/Forest_Ranger_1/PNG/PNG Sequences/Idle/0_Forest_Ranger_Idle_000.png")
player_image = pygame.transform.scale(player_image, (200, 200))
player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50)  # Left side

player = game["player"]
player_name = player.name
player_hp = player.stats["hp"]
player_max_hp = player.stats["max_hp"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and player_turn:
            if event.key == pygame.K_a:  # 'A' for Attack
                damage = random.randint(5, 10)  # Example: 5-10 damage
                goblin_hp -= damage
                if goblin_hp < 0:
                    goblin_hp = 0
                player_turn = False  # Switch to enemy turn
        # Enemy turn logic (simple AI)
    if not player_turn and goblin_hp > 0:
        damage = random.randint(3, 8)
        hero_hp -= damage
        if hero_hp < 0:
            hero_hp = 0
        player_turn = True  # Back to player
        
    screen.fill(BLACK)
    screen.blit(enemy_image, enemy_rect)
    screen.blit(player_image, player_rect)

    font = pygame.font.SysFont("arial", 40)

    # Enemy name and HP
    name_text = font.render(enemy_name, True, WHITE)
    screen.blit(name_text, (SCREEN_WIDTH // 2 + 200 - name_text.get_width() // 2, 80))
    hp_bar_width = 400
    hp_bar_height = 40
    enemy_hp_ratio = enemy_hp / enemy_max_hp if enemy_max_hp > 0 else 0
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 + 200 - hp_bar_width // 2, 480, hp_bar_width, hp_bar_height))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 + 200 - hp_bar_width // 2, 480, hp_bar_width * enemy_hp_ratio, hp_bar_height))
    hp_text = font.render(f"HP: {enemy_hp}/{enemy_max_hp}", True, WHITE)
    screen.blit(hp_text, (SCREEN_WIDTH // 2 + 200 - hp_text.get_width() // 2, 530))

    # Player name and HP
    name_text = font.render(player_name, True, WHITE)
    screen.blit(name_text, (SCREEN_WIDTH // 4 - name_text.get_width() // 2, 80))
    player_hp_ratio = player_hp / player_max_hp if player_max_hp > 0 else 0
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 4 - hp_bar_width // 2, 480, hp_bar_width, hp_bar_height))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 4 - hp_bar_width // 2, 480, hp_bar_width * player_hp_ratio, hp_bar_height))
    hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, WHITE)
    screen.blit(hp_text, (SCREEN_WIDTH // 4 - hp_text.get_width() // 2, 530))

    # Check win/lose
    if hero_hp <= 0:
        lose_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(lose_text, (screen_width // 2 - 100, screen_height // 2))
        running = False  # Or handle restart
    elif goblin_hp <= 0:
        win_text = font.render("You Win!", True, (0, 255, 0))
        screen.blit(win_text, (screen_width // 2 - 100, screen_height // 2))
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()