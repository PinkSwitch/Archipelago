def set_seals(world):
    seals = [
        "Magic Seal 1",
        "Magic Seal 2",
        "Magic Seal 3",
        "Magic Seal 4",
        "Magic Seal 5"
    ]

    placed_seals = []

    world.magic_seal_table = {
        "Lost Village": "Magic Seal 1",
        "Wizardry Lab": "Magic Seal 1",
        "Dark Chapel": "Magic Seal 2",
        "Dark Chapel Inner": "Magic Seal 2",
        "Garden of Madness": "Magic Seal 2",  # Dario
        "Demon Guest House": "Magic Seal 3",
        "Subterranean Hell": "Magic Seal 3",
        "Condemned Tower": "Magic Seal 3",
        "Cursed Clock Tower": "Magic Seal 4",
        "Silenced Ruins": "Magic Seal 4",
        "Demon Guest House Upper": "Magic Seal 4",
        "The Pinnacle": "Magic Seal 4",
        "Castle Center": "Magic Seal 5"
    }

    if world.options.goal:
        world.magic_seal_table["Mine of Judgment"] = "Magic Seal 5"
        world.magic_seal_table["The Abyss"] = "Magic Seal 5"


    if world.options.seal_shuffle:
        for seal in world.magic_seal_table:
            world.magic_seal_table[seal] = world.random.choice(seals) # Randomize the list

        if world.options.early_seal_1:
            world.magic_seal_table["Lost Village"] = "Magic Seal 1"  # We still want to set this early so the player doesn't get stuck

    for seal in world.magic_seal_table:
        if world.magic_seal_table[seal] not in placed_seals:
            world.multiworld.itempool.append(world.set_classifications(world.magic_seal_table[seal]))  # Create the seal items if necessary
            world.extra_item_count += 1
            placed_seals.append(world.magic_seal_table[seal])
    

def write_seals(world, rom):
    print("AAAAAAAAAAAA")