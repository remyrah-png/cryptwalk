# combat.py - Combat system module
from items import healing_potion, iron_sword, leather_armor
from random import random, choice

def calculate_damage(attacker, defender):
    atk = attacker.stats["strength"]
    if attacker.weapon:
        atk += attacker.weapon.value

    defn = defender.stats["defense"]
    if defender.armor:
        defn += defender.armor.value

    dmg = max(1, atk - defn)
    return dmg  # <-- this line was missing

        
def apply_defend(game, entity):
    entity.defending = True
    game["combat_log"].append(f"{entity.name} is defending!")

def apply_poison(game, target, dmg_per_turn=1, turns=3):
    target.effects.append({
        "type": "poison",
        "dmg": dmg_per_turn,
        "turns": turns
    })
    game["combat_log"].append(f"{target.name} is poisoned for {turns} turns!")

def apply_taunt(game, attacker, dmg_reduction=-2, turns=1):
    attacker.effects.append({
        "type": "taunt",
        "dmg": dmg_reduction,  # negative
        "turns": turns
    })
    game["combat_log"].append(f"{attacker.name} is taunted for {turns} turns!")

def attack(game, attacker_key, defender_key, bonus_damage=0):
    attacker = game[attacker_key]
    defender = game[defender_key]

    base_dmg = calculate_damage(attacker, defender)
    bonus_damage = 0
    if attacker.weapon:
        bonus_damage = attacker.weapon.value
    dmg = base_dmg + bonus_damage

    # Apply taunt effect (reduces attacker's damage)
    for i, eff in enumerate(attacker.effects[:]):
        if eff["type"] == "taunt" and eff["turns"] > 0:
            dmg = max(1, dmg + eff["dmg"])  # dmg is negative
            game["combat_log"].append(f"{attacker.name} is taunted! Damage reduced!")
            eff["turns"] -= 1
            if eff["turns"] <= 0:
                attacker.effects.pop(i)
            break

    # Defending reduces damage
    if getattr(defender, "defending", False):
        dmg = max(1, dmg - 2)
        game["combat_log"].append(f"{defender.name} reduces the damage!")
        defender.defending = False

    defender.stats["hp"] = max(0, defender.stats["hp"] - dmg)
    game["combat_log"].append(f"{attacker.name} hits {defender.name} for {dmg} damage!")

    return dmg


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
