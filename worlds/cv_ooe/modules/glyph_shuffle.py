import struct
from ..Options import RandomStolenGlyphs, RandomDropGlyphs


def shuffle_glyphs(world) -> None:
    enemy_glyph_pool = set()
    world.glyph_drops = {
        "Bone Scimitar": "Secare",
        "Axe Knight": "Ascia",
        "Bone Archer": "Arcus",
        "Spear Guard": "Hasta",
        "Werebat": "Arma Chiroptera",
        "Skull Spider": "Fidelis Aranea",
        "Owl": "Fidelis Noctua",
        "Spectral Sword": "Melio Secare",
        "Automaton ZX27": "Arma Machina",
        "Gorgon Head": "Fidelis Medusa",
        "Black Panther": "Arma Felix",
        "Polkir": "Fidelis Polkir",
        "Red Smasher": "Vol Culter",
        "Hammer Shaker": "Melio Macir",
        "Great Knight": "Melio Ascia",
        "Winged Skeleton": "Fidelis Alate",
        "Dullahan": "Vol Confodere",
        "Miss Murder": "Vol Falcis",
        "Lizardman": "Vol Scutum",
    }

    world.glyph_steals = {
        "Necromancer": "Fidelis Caries",
        "Sea Demon": "Grando",
        "Fire Demon": "Ignis",
        "Black Fomor": "Umbra",
        "Thunder Demon": "Fulgur",
        "White Fomor": "Vol Luminatio",
        "Nova Skeleton": "Nitesco",
        "Jiang Shi": "Fidelis Mortus",
        "Demon Lord": "Globus",
        "Albus": "Acerbatus",
        "Barlowe": "Globus"
    }

    if world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_shuffled:
        for enemy in world.glyph_steals:
            new_glyph = world.random.choice(world.glyph_pool)
            world.glyph_pool.remove(new_glyph)
            world.glyph_steals[enemy] = new_glyph

    if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_shuffled:
        for enemy in world.glyph_drops:
            new_glyph = world.random.choice(world.glyph_pool)
            world.glyph_pool.remove(new_glyph)
            world.glyph_drops[enemy] = new_glyph

    # Assign Enemy glyphs to the Filler generation pool
    if world.options.randomize_stolen_glyphs != RandomStolenGlyphs.option_glyphsanity:
        for enemy in world.glyph_steals:
            glyph = world.glyph_steals[enemy]
            if glyph != "Arma Machina":  # Arma Machina is a 100% key item, so we can't Fillerize it
                enemy_glyph_pool.add(glyph)
                if glyph in world.glyph_pool:
                    world.glyph_pool.remove(glyph)
    else:
        #  If Glyphsanity, ignore the shuffling logic and instead add the relevant glyphs to the static pool
        world.glyph_pool.extend(["Fidelis Caries", "Grando", "Ignis", "Umbra", "Fulgur", "Vol Luminatio", "Nitesco",
                                 "Fidelis Mortus", "Globus", "Acerbatus", "Globus"])

    if world.options.randomize_dropped_glyphs != RandomDropGlyphs.option_glyphsanity:
        for enemy in world.glyph_drops:
            glyph = world.glyph_drops[enemy]
            if glyph != "Arma Machina":
                enemy_glyph_pool.add(glyph)
                if glyph in world.glyph_pool:
                    world.glyph_pool.remove(glyph)
    else:
        world.glyph_pool.extend(["Secare", "Ascia", "Arcus", "Hasta", "Arma Chiroptera", "Fidelis Aranea",
                                 "Fidelis Noctua", "Melio Secare", "Fidelis Medusa", "Arma Felix", "Fidelis Polkir",
                                 "Vol Culter", "Melio Macir", "Melio Ascia", "Fidelis Alate", "Vol Confodere",
                                 "Vol Falcis", "Vol Scutum"])
        
    world.glyph_filler_table.extend(enemy_glyph_pool)


def write_shuffled_glyphs(world, rom) -> None:
    from ..game_data import enemy_table
    from ..Items import item_table
    if world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_shuffled:
        for enemy in world.glyph_steals:
            glyph = world.glyph_steals[enemy]
            glyph_id = item_table[glyph].code
            index = enemy_table.index(enemy)
            rom.write_to_file(0x020B6364 + (index * 0x24) + 0x14, "arm9", struct.pack("H", glyph_id))

    if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_shuffled:
        for enemy in world.glyph_drops:
            glyph = world.glyph_drops[enemy]
            glyph_id = item_table[glyph].code
            index = enemy_table.index(enemy)
            rom.write_to_file(0x020B6364 + (index * 0x24) + 0x14, "arm9", struct.pack("H", glyph_id))
