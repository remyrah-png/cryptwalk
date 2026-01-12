from player import Player
from enemies import create_enemy
from cryptwalk import game
def main():
    print("Game starting...")
    player = Player()
    enemy = create_enemy("goblin")
    
    # Simple combat loop (text-based for now)
    while player.is_alive() and enemy.is_alive():
        print(dir(Player))
        player.attack(enemy, game)  # Player turn
        if enemy.is_alive():
            enemy.attack(player)  # Enemy turn
    
    if player.is_alive():
        print("You win!")
    else:
        print("Game over.")

if __name__ == "__main__":
    main()