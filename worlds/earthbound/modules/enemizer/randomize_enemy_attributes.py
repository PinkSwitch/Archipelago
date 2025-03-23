from .enemy_attributes import enemy_species, enemy_adjectives, battle_sprites, field_sprites

def randomize_enemy_attributes(world, rom):
    for enemy in world.enemies:
        new_name = "FFFFFFFFFFFFFFFFFFFFFFFFFF"
        while len(new_name) > 25:
            species = world.random.choice(enemy_species)
            adjective = world.random.choice(enemy_adjectives)
            new_name = adjective + species
        sprite = battle_sprites[species]
        # sprite = world.random.choice(battle_sprites[species])
        # field_sprite = field_sprites[species]
        print(new_name)