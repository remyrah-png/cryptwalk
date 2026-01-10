# combat.py - Combat system module

from random import random, choice

def calculate_damage(attacker, defender):
    atk = attacker.stats["strength"]
    if attacker.weapon:
        atk += attacker.weapon.value

    defn = defender.stats["defense"]
    if defender.armor:
        defn += defender.armor.value

    dmg = max(1, atk - defn)
    return dmg

def apply_defend(entity):
    entity.defending = True

def apply_poison(game, target, dmg_per_turn=1, turns=3):
    target.effects.append({
        "type": "poison",
        "dmg": dmg_per_turn,
        "turns": turns
    })
    game["combat_log"].append(f"{target.name} is poisoned for {turns} turns!")

def apply_taunt(game, target, dmg_reduction=-2, turns=1):
    target.effects.append({
        "type": "taunt",
        "dmg": dmg_reduction,  # negative, reduces target's damage output
        "turns": turns
    })
    game["combat_log"].append(f"{target.name} is taunted for {turns} turns! (Damage reduced)")

def attack(game, attacker_key, defender_key):
    attacker = game[attacker_key]
    defender = game[defender_key]

    dmg = calculate_damage(attacker, defender)

    # Apply taunt effect (reduces attacker's damage if taunted)
    for eff in attacker.effects[:]:
        if eff["type"] == "taunt" and eff["turns"] > 0:
            dmg = max(1, dmg + eff["dmg"])  # dmg_reduction is negative
            game["combat_log"].append(f"{attacker.name} is taunted! Damage reduced!")
            eff["turns"] -= 1
            if eff["turns"] <= 0:
                attacker.effects.remove(eff)

    # Defending reduces damage
    if defender.defending:
        dmg = max(1, dmg - 2)
        game["combat_log"].append(f"{defender.name} reduces the damage!")
        defender.defending = False

    defender.stats["hp"] = max(0, defender.stats["hp"] - dmg)
    game["combat_log"].append(f"{attacker.name} hits {defender.name} for {dmg} damage!")

    return dmg

def process_effects(game, target_key):
    target = game[target_key]
    new_effects = []

    for eff in target.effects[:]:
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