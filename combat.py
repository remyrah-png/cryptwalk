# combat.py - Combat system module

def calculate_damage(attacker, defender):
    atk = attacker["stats"]["strength"]
    weapon = attacker.get("weapon")
    if weapon:
        atk += weapon.get("strength", 0)

    defn = defender["stats"]["defense"]
    armor = defender.get("armor")
    if armor:
        defn += armor.get("defense", 0)

    dmg = atk - defn
    return max(1, dmg)


def apply_defend(entity):
    entity["defending"] = True


def apply_poison(target, dmg_per_turn=1, turns=3):
    target["effects"].append({
        "type": "poison",
        "dmg": dmg_per_turn,
        "turns": turns
    })


def apply_taunt(attacker, dmg_reduction=-2, turns=1):
    """Taunt reduces attacker's damage when they attack"""
    attacker["effects"].append({
        "type": "taunt",
        "dmg": dmg_reduction,  # negative value
        "turns": turns
    })


def attack(game, attacker_key, defender_key, bonus_damage=0):
    attacker = game[attacker_key]
    defender = game[defender_key]

    base_dmg = calculate_damage(attacker, defender)
    dmg = base_dmg + bonus_damage

    # Apply taunt effect (reduces attacker's damage)
    for i, eff in enumerate(attacker.get("effects", [])):
        if eff.get("type") == "taunt" and eff["turns"] > 0:
            dmg = max(1, dmg + eff["dmg"])  # dmg is negative
            game["combat_log"].append(f"{attacker['name']} is taunted! Damage reduced!")
            eff["turns"] -= 1
            if eff["turns"] <= 0:
                attacker["effects"].pop(i)
            break

    # Defending reduces damage
    if defender.get("defending", False):
        dmg = max(1, dmg - 2)
        game["combat_log"].append(f"{defender['name']} reduces the damage!")
        defender["defending"] = False

    defender["stats"]["hp"] = max(0, defender["stats"]["hp"] - dmg)
    game["combat_log"].append(f"{attacker['name']} hits {defender['name']} for {dmg} damage!")

    return dmg


def process_effects(game, target_key):
    target = game[target_key]
    effects = target.get("effects", [])
    new_effects = []

    for eff in effects[:]:  # copy to allow removal
        if eff["type"] == "poison" and eff["turns"] > 0:
            dmg = eff["dmg"]
            target["stats"]["hp"] = max(0, target["stats"]["hp"] - dmg)
            game["combat_log"].append(f"{target['name']} takes {dmg} poison damage!")
            eff["turns"] -= 1
            if eff["turns"] > 0:
                new_effects.append(eff)
            else:
                game["combat_log"].append(f"{target['name']} is no longer poisoned.")
        else:
            new_effects.append(eff)

    target["effects"] = new_effects


def is_alive(entity):
    return entity["stats"]["hp"] > 0
