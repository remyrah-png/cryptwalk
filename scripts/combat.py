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

        
def apply_defend(entity):
    entity.defending = True  # No log here; add in caller

def apply_poison(game, target, dmg_per_turn=1, turns=3):
    target.effects.append({"type": "poison", "dmg": dmg_per_turn, "turns": turns})
    game["combat_log"].append(f"{target.name} is poisoned ({dmg_per_turn} dmg/turn for {turns} turns)!")

def apply_enrage(game, target, dmg_bonus=3, turns=2):  # Buffs enemy attack
    target.effects.append({"type": "enrage", "dmg": dmg_bonus, "turns": turns})
    game["combat_log"].append(f"{target.name} is enraged (+{dmg_bonus} dmg for {turns} turns)!")


    game["combat_log"].append(f"{attacker.name} is enraged for {turns} turns!")
def attack(game, attacker_key, defender_key, bonus_damage=0):
    attacker = game[attacker_key]
    defender = game[defender_key]

    base_dmg = calculate_damage(attacker, defender)
    bonus_damage = 0
    if attacker.weapon:
        bonus_damage = attacker.weapon.value
    dmg = base_dmg + bonus_damage
    print(f"Debug: {attacker.name}  dmg = {dmg}, defender HP = {defender.stats['hp']}")  # Debug

#Update attack() to handle "enrage":
# Add after taunt check (around line ~35):
    for i, eff in enumerate(attacker.effects[:]):
        if eff["type"] == "enrage" and eff["turns"] > 0:
            dmg += eff["dmg"]
            game["combat_log"].append(f"{attacker.name} is enraged! Extra damage!")
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
