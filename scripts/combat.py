# combat.py - Combat system module

from items import healing_potion, iron_sword, leather_armor
from random import random, choice

def attack(game, attacker_key, defender_key):
    attacker = game[attacker_key]
    defender = game[defender_key]

    dmg = calculate_damage(attacker, defender)

    # Critical hit check
    if random() < attacker.stats.get("crit_chance", 0):
        dmg *= 2
        game["combat_log"].append(f"Critical hit by {attacker.name}!")

    # Apply damage
    defender.stats["hp"] = max(0, defender.stats["hp"] - dmg)
    game["combat_log"].append(f"{attacker.name} attacks {defender.name} for {dmg} damage!")

    return dmg

def calculate_damage(attacker, defender):
    atk = attacker.stats["strength"]
    if attacker.weapon:
        atk += attacker.weapon.value

    defn = defender.stats["defense"]
    if defender.armor:
        defn += defender.armor.value

    dmg = max(1, atk - defn)
    return dmg  # <-- this line was missing

        
def apply_defend(entity):
    entity.defending = True  # No log here; add in caller

def apply_poison(game, target, dmg_per_turn=1, turns=3):
    target.effects.append({"type": "poison", "dmg": dmg_per_turn, "turns": turns})
    game["combat_log"].append(f"{target.name} is poisoned ({dmg_per_turn} dmg/turn for {turns} turns)!")

def apply_enrage(game, target, turns=3):
    target.effects.append({"type": "enrage", "turns": turns})
    game["combat_log"].append(f"{target.name} is enraged for {turns} turns!")  # Fixed: use target.name instead of attacker

def process_effects(game, target_key):
    target = game[target_key]
    effects = target.effects[:]
    new_effects = []

    for eff in effects[:]:  # copy to allow removal
        if eff["type"] == "poison" and eff["turns"] > 0:
            dmg = eff["dmg"]
            target.stats["hp"] = max(0, target.stats["hp"] - dmg)
            game["combat_log"].append(f"{target.name} takes {dmg} poison damage!")
            eff["turns"] -= 1
            if eff["turns"] > 0:
                new_effects.append(eff)
            else:
                game["combat_log"].append(f"{target.name} is no longer poisoned.")
        else:
            new_effects.append(eff)

    target.effects = new_effects


def is_alive(entity):
    return entity.stats["hp"] > 0
