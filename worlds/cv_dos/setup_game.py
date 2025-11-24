import logging

def setup_game(world):
    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

def place_static_items(world):
    world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))
    world.get_location("Garden of Madness: Central Chamber").place_locked_item(world.create_item("Power of Darkness"))
    world.get_location("Abyss Center").place_locked_item(world.create_item("Menace Defeated"))

    if world.options.goal:
        world.get_location("The Pinnacle: Throne Room").place_locked_item(world.create_item("Aguni Defeated"))