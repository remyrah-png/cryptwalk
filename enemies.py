from entity import CombatEntity

def create_enemy(enemy_type):
    if enemy_type == "goblin":
        return CombatEntity(
            name="Goblin",
            hp=30,
            max_hp=30,
            strength=5,
            defense=2
        )
    elif enemy_type == "Orc":
        return CombatEntity(
            name="Orc",
            hp=40,
            max_hp=40,
            strength=7,
            defense=3
        )
    elif enemy_type == "Ogre":
        return CombatEntity(
            name="Ogre",
            hp=60,
            max_hp=60,
            strength=10,
            defense=5
        )
    else:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
