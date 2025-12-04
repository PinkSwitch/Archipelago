import logging
from .Options import SoulsanityLevel, SoulRandomizer
from .Items import soul_filler_table, item_table
from BaseClasses import ItemClassification

def setup_game(world):
    soul_location_count = 0

    if world.options.goal:
        world.common_souls.update(["Slogra Soul", "Black Panther Soul"])
        world.uncommon_souls.update(["Ripper Soul", "Mud Demon Soul", "Gaibon Soul", "Malacoda Soul"])
        world.uncommon_souls.update(["Giant Slug Soul", "Stolas Soul", "Arc Demon Soul"])

    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.multiworld.itempool.append(world.create_item("Skeleton Soul"))
        world.multiworld.itempool.append(world.create_item("Axe Armor Soul"))
        world.multiworld.itempool.append(world.create_item("Killer Clown Soul"))
        world.multiworld.itempool.append(world.create_item("Ukoback Soul"))
        world.multiworld.itempool.append(world.create_item("Skeleton Ape Soul"))
        world.multiworld.itempool.append(world.create_item("Bone Ark Soul"))
        world.multiworld.itempool.append(world.create_item("Mandragora Soul"))
        world.multiworld.itempool.append(world.create_item("Rycuda Soul"))
        world.multiworld.itempool.append(world.create_item("Waiter Skeleton Soul"))
        soul_location_count += (len(world.common_souls) - 9)
        world.extra_item_count += 9

        if world.options.soulsanity_level:
            soul_location_count += len(world.uncommon_souls)

        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            world.armor_table.remove("Soul Eater Ring")  # Don't generate a filler copy since hard guarantees one
            world.multiworld.itempool.append(world.create_item("Soul Eater Ring"))
            world.multiworld.itempool.append(world.create_item("Imp Soul"))
            soul_location_count += (len(world.rare_souls) - 2)
            world.extra_item_count += 2

        for i in range(soul_location_count):
            world.multiworld.itempool.append(world.create_item(world.random.choice(soul_filler_table)))
            world.extra_item_count += 1

def place_static_items(world):
    world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))
    world.get_location("Garden of Madness: Central Chamber").place_locked_item(world.create_item("Power of Darkness"))
    world.get_location("Abyss Center").place_locked_item(world.create_item("Menace Defeated"))

    if world.options.goal:
        world.get_location("The Pinnacle: Throne Room").place_locked_item(world.create_item("Aguni Defeated"))