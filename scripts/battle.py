import sys
sys.path.append("..")  # Adjust as necessary
from cryptwalk import game  # Import game dict
import pygame
import random
from enemies import create_enemy
from items import Item  # For inventory handling

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

# Turn and state
player_turn = True
running = True
message = ""  # For displaying actions/results

font = pygame.font.SysFont("arial", 40)
small_font = pygame.font.SysFont("arial", 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and player_turn:
            if event.key == pygame.K_a:  # Attack
                damage = random.randint(player.stats["strength"] - enemy.stats["defense"], player.stats["strength"])
                if damage < 1: damage = 1
                if enemy.defending:
                    damage = max(1, damage // 2)
                    enemy.defending = False
                    message += " Enemy defended!"
                enemy_hp -= damage
                if enemy_hp < 0: enemy_hp = 0
                message = f"You attack for {damage} damage!" + message
                player_turn = False
            elif event.key == pygame.K_d:  # Defend
                player.defending = True
                message = "You defend!"
                player_turn = False
            elif event.key == pygame.K_i:  # Inventory
                if not player.inventory:
                    message = "Inventory empty!"
                else:
                    # Simple text list for selection (use numbers 1-9 for items)
                    inv_text = "Inventory: "
                    for i, item in enumerate(player.inventory[:9]):  # Limit to 9 for keys
                        inv_text += f"{i+1}: {item.name} "
                    message = inv_text + "\nPress number to use."
                    # Wait for number key
                    selected = None
                    while selected is None:
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.KEYDOWN:
                                if pygame.K_1 <= sub_event.key <= pygame.K_9:
                                    idx = sub_event.key - pygame.K_1
                                    if idx < len(player.inventory):
                                        item = player.inventory[idx]
                                        if item.use(player):  # If returns True, consume
                                            player.inventory.pop(idx)
                                        # Update HP/stats if changed
                                        player_hp = player.stats["hp"]
                                        message = f"Used {item.name}!"
                                        selected = True
                            elif sub_event.type == pygame.QUIT:
                                running = False
                                selected = True
                        clock.tick(60)
                    player_turn = False  # End turn after use

    # Enemy turn
    if not player_turn and enemy_hp > 0 and running:
        # Simple AI: 70% attack, 30% defend
        if random.random() < 0.7:
            damage = random.randint(enemy.stats["strength"] - player.stats["defense"], enemy.stats["strength"])
            if damage < 1: damage = 1
            if player.defending:
                damage = max(1, damage // 2)
                player.defending = False
                message += " You defended!"
            player_hp -= damage
            if player_hp < 0: player_hp = 0
            message += f"\nEnemy attacks for {damage} damage!" + message
        else:
            enemy.defending = True
            message += "\nEnemy defends!"
        player_turn = True

    # Draw
    screen.fill(BLACK)
    screen.blit(enemy_image, enemy_rect)
    screen.blit(player_image, player_rect)

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

    # Action message
    msg_lines = message.split("\n")
    for i, line in enumerate(msg_lines[-3:]):  # Last 3 lines
        msg_text = small_font.render(line, True, WHITE)
        screen.blit(msg_text, (20, SCREEN_HEIGHT - 100 - i * 30))

    # Check win/lose
    if player_hp <= 0:
        lose_text = font.render("Game Over", True, RED)
        screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
    elif enemy_hp <= 0:
        win_text = font.render("You Win!", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()