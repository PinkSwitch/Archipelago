from ..Options import RandomStolenGlyphs, RandomDropGlyphs


def shuffle_glyphs(world) -> None:
    enemy_glyph_pool = set()
    glyph_drops = {
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

    glyph_steals = {
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
        for enemy in glyph_steals:
            new_glyph = world.random.choice(world.glyph_pool)
            world.glyph_pool.remove(new_glyph)
            glyph_steals[enemy] = new_glyph

    if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_shuffled:
        for enemy in glyph_drops:
            new_glyph = world.random.choice(world.glyph_pool)
            glyph_drops[enemy] = new_glyph

    # Assign Enemy glyphs to the Filler generation pool
    for enemy in glyph_steals:
        glyph = glyph_steals[enemy]
        if glyph != "Arma Machina":  # Arma Machina is a 100% key item, so we can't Fillerize it
            enemy_glyph_pool.add(glyph)
            if glyph in world.glyph_pool:
                world.glyph_pool.remove(glyph)

    for enemy in glyph_drops:
        glyph = glyph_drops[enemy]
        if glyph != "Arma Machina":
            enemy_glyph_pool.add(glyph)
            world.glyph_pool.remove(glyph)
        
    world.glyph_filler_table.extend(enemy_glyph_pool)
    print(world.glyph_pool)