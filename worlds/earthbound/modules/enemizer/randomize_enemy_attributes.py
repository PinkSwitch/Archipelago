import struct
from .enemy_attributes import (enemy_species, enemy_adjectives, battle_sprites, field_sprites, excluded_enemies, insects, robots, movement_patterns,
start_texts, death_texts)
from ..music_rando import battle_songs
from ...game_data.text_data import calc_pixel_width, text_encoder

shield_statuses = [
    "phys_1",
    "phys_2",
    "psi_1",
    "psi_2"
]

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
            field_sprite = field_sprites[sprite]
            movement_pattern = movement_patterns[field_sprite]
            palette = world.random.randint(1,31)
            gender = world.random.randint(1,3)
            if species in robots:
                enemy_type = 2
            elif species in insects:
                enemy_type = 1
            else:
                enemy_type = 0
            row = world.random.randint(0,1)
            mirror_chance = world.random.randint(0,100)
            start_text = world.random.choice(start_texts)
            #death_text = ????
            if species in ["Power Robot", "Reactor Robot", "Sphere"]:
                death_action = 0x0040
            elif species == "Oak":
                death_action = 0x0041
            else:
                death_action = 0x0000
            music = world.random.choice(battle_songs)
            drop_rate = world.random.randint(0,7)
            base_drop = world.random.choice(world.filler_drops)
            if world.random.randint(1,100) < 6:
                status = world.random.randint(1,7)
                if status < 5:
                    world.enemies[enemy].has_shield = shield_statuses[status - 1]
            else:
                status = 0
            address = world.enemies[enemy].address
            print(f"{new_name} using {palette}")
            new_name = text_encoder(new_name, 0x18)
            if len(new_name) < 0x18:
                new_name.extend([0x00])
            rom.write_bytes(address, bytearray([0x01]))
            rom.write_bytes(address + 1, new_name)
            rom.write_bytes(address + 0x1A, bytearray([gender]))
            rom.write_bytes(address + 0x1B, bytearray([enemy_type]))
            rom.write_bytes(address + 0x1C, struct.pack("H", sprite))
            rom.write_bytes(address + 0x1E, struct.pack("H", field_sprite))
            rom.write_bytes(address + 0x2B, struct.pack("H", movement_pattern))
            rom.write_bytes(address + 0x2B, struct.pack("H", movement_pattern))
            rom.write_bytes(address + 0x2D, struct.pack("I", start_text))
            #rom.write_bytes(address + 0x31, struct.pack("I", death_text))
            rom.write_bytes(address + 0x35, bytearray([palette]))
            rom.write_bytes(address + 0x37, bytearray([music]))
            # Miss rate?
            rom.write_bytes(address + 0x4E, struct.pack("H", death_action))
            rom.write_bytes(address + 0x57, bytearray([drop_rate]))
            rom.write_bytes(address + 0x58, bytearray([base_drop]))
            rom.write_bytes(address + 0x59, bytearray([status]))
            rom.write_bytes(address + 0x5B, bytearray([row]))
            rom.write_bytes(address + 0x5D, bytearray([mirror_chance]))
            
            #fire_weakness =

            #freeze_weakness = 

            #flash_weakness =

            #paralyz_weankess = 

            #hypnosis_weakness = 