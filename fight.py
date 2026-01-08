import random
from combat import attack, apply_defend, apply_poison, apply_taunt, process_effects
from enemies import create_enemy

def run_battle(game):
    # Spawn random enemy
    enemy_types = ["goblin", "skeleton", "orc"]
    enemy_type = random.choice(enemy_types)
    game["enemy"] = create_enemy(enemy_type)
    game["combat_log"] = []
    game["turn"] = 1
    game["active_turn"] = "player"

    print(f"\nEncounter: A {game['enemy'].name} appears!")

    while game["player"].is_alive() and game["enemy"].is_alive():
        # Simple print display (we'll add Pygame later)
        print("\n======== Combat ======= ")
        print(f"Turn: {game['turn']} ({game['active_turn'].capitalize()}'s turn)")
        print(f"Player HP: {game['player'].stats['hp']}/{game['player'].stats['max_hp']}")
        print(f"Enemy HP: {game['enemy'].stats['hp']}/{game['enemy'].stats['max_hp']}")
        if game['combat_log']:
            print("\nLogs:")
            for log in game['combat_log'][-3:]:
                print(log)

        if game["active_turn"] == "player":
            while True:  # Validate input
                choice = input("\nChoose: 1) Attack 2) Defend 3) Poison 4) Taunt: ").strip()
                if choice == "1":
                    attack(game, "player", "enemy")
                    break
                elif choice == "2":
                    apply_defend(game["player"])
                    game["combat_log"].append("You defend!")
                    break
                elif choice == "3":
                    apply_poison(game["enemy"])
                    break
                elif choice == "4":
                    apply_taunt(game["enemy"])
                    break
                else:
                    print("Invalid! Choose 1-4.")
            process_effects(game, "player")
            game["active_turn"] = "enemy"
        else:
            # Enemy AI
            actions = ["attack", "defend", "poison", "taunt"]
            enemy_choice = random.choice(actions)
            if enemy_choice == "attack":
                attack(game, "enemy", "player")
            elif enemy_choice == "defend":
                apply_defend(game["enemy"])
                game["combat_log"].append(f"{game['enemy'].name} defends!")
            elif enemy_choice == "poison":
                apply_poison(game["player"])
            elif enemy_choice == "taunt":
                    apply_taunt(game["player"])
            process_effects(game, "enemy")
            game["active_turn"] = "player"
            game["turn"] += 1

    # Outcome
    if game["player"].is_alive():
        outcome = "win"
        gold = random.randint(10, 20)
        exp = random.randint(50, 100)
        print("You win!")
    else:
        outcome = "lose"
        gold = 0
        exp = 0
        print("Game over.")

    game["enemy"] = None
    return outcome, gold, exp