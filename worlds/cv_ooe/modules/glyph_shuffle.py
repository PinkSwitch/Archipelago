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

    for enemy in glyph_steals:
        if glyph_steals[enemy] != "Arma Machina":  # Arma Machina is a 100% key item, so we can't Fillerize it
            enemy_glyph_pool.add(glyph_steals[enemy])

    for enemy in glyph_drops:
        if glyph_drops[enemy] != "Arma Machina":
            enemy_glyph_pool.add(glyph_drops[enemy])
        
    world.glyph_filler_table.extend(enemy_glyph_pool)
    print(world.glyph_filler_table)