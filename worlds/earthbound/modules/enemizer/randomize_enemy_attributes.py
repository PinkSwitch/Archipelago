from .enemy_attributes import enemy_species, enemy_adjectives, battle_sprites, field_sprites, excluded_enemies
from ...game_data.text_data import calc_pixel_width

enemy_explosions = {
    "Power Robot": 0x40,
    "Reactor Robot": 0x40,
    "Sphere": 0x40,
    "Oak": 0x41,
}

def randomize_enemy_attributes(world, rom):
    taken_names = []
    for enemy in world.enemies:
        if enemy not in excluded_enemies and " (" not in enemy:
            # print(enemy)
            new_name = "FFFFFFFFFFFFFFFFFFFFFFFFFF"
            pixel_width = calc_pixel_width(new_name)
            while len(new_name) > 25 and new_name not in taken_names and pixel_width > 95:
                species = world.random.choice(enemy_species)
                adjective = world.random.choice(enemy_adjectives)
                new_name = adjective + species
                pixel_width = calc_pixel_width(new_name)
            taken_names.append(new_name)
            sprite = world.random.choice(battle_sprites[species])
             # field_sprite = field_sprites[species]
            palette = world.random.randint(1,31)
            gender = world.random.randint(1,3)