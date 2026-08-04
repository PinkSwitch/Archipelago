from .Options import RandomizeVillagers


def create_conditional_items(world, pool):
    #  Remove the starting Glyph from the pool
    if world.create_item(world.starting_glyph) in pool:
        pool.remove(world.create_item(world.starting_glyph))

    if world.options.remove_large_cavern:
        pool.remove(world.create_item("Map: Large Cavern"))

    if world.options.remove_training_hall:
        pool.remove(world.create_item("Map: Training Hall"))

    if world.options.shuffle_dominus:
        pool.extend([world.create_item("Dominus Hatred"),
                     world.create_item("Dominus Anger"),
                     world.create_item("Dominus Agony")])

    if world.starting_area:
        pool.remove(world.create_item(f"Map: {world.starting_area}"))

    if world.options.randomize_villagers == RandomizeVillagers.option_anywhere:
        pool.extend([world.create_item("Nikolai"),
                     world.create_item("Jacob"),
                     world.create_item("Abram"),
                     world.create_item("Laura"),
                     world.create_item("Eugen"),
                     world.create_item("Aeon"),
                     world.create_item("Marcel"),
                     world.create_item("George"),
                     world.create_item("Serge"),
                     world.create_item("Anna"),
                     world.create_item("Monica"),
                     world.create_item("Irina"),
                     world.create_item("Daniela")])

        for villager in world.options.starting_villagers:
            pool.remove(world.create_item(villager))

    if world.options.start_with_glyph_sleeve:
        pool.remove(world.create_item("Glyph Sleeve"))

    if world.options.start_with_glyph_union:
        pool.remove(world.create_item("Glyph Union"))

    if world.options.start_with_lizard_tail:
        pool.remove(world.create_item("Lizard Tail"))

    if world.starting_glyph in world.glyph_filler_table:
        world.glyph_filler_table.remove(world.starting_glyph)


def generate_emergency_glyphs(world, pool):
    #  Generate Glyphs that need to be added here, if we didn't generate any via the pool or filler already
    from .game_data import villager_list
    from . import get_filler_item_name

    tin_man_glyphs = []
    generator_glyphs = []
    #  If we didn't generate any item capable of fighting Tin Man, add an emergency one here
    for item in world.can_kill_tin_man:
        if item not in villager_list:
            tin_man_glyphs.append(world.create_item(item))
    if len(set(tin_man_glyphs) & set(pool)) > 0 or "Torpor" in world.can_kill_tin_man or world.starting_glyph in world.can_kill_tin_man:  # Torpor can be gotten from villagers
        pool.append(world.create_item(get_filler_item_name(world)))  # If we don't need to do this, add a filler item
    else:
        pool.append(world.random.choice(tin_man_glyphs))

    for item in world.generator_logic_glyphs:
        generator_glyphs.append(world.create_item(item))

    if len(set(generator_glyphs) & set(pool)) > 0 or world.starting_glyph in world.generator_logic_glyphs:  # If we didn't already generate any of these
        pool.append(world.create_item(get_filler_item_name(world)))
    else:
        pool.append(world.random.choice(generator_glyphs))
