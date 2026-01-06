from player import Player
from enemies import create_enemy

def main():
    print("Starting Cryptwalk...")
    player = Player()
    print(f'Welcome, {player.name}! Health: {player.stats["hp"]}/{player.stats["max_hp"]}')

    enemies = create_enemy("goblin")
    print(f'Encountered an enemy: {enemies.name} with HP: {enemies.stats["hp"]}/{enemies.stats["max_hp"]}')
if __name__ == "__main__":
    main()