from .Options import SoulsanityLevel, SoulRandomizer
from .Items import soul_filler_table
from .in_game_data import warp_room_regions, warp_room_table
from .bullet_wall_randomizer import set_souls_for_walls
from .synthesis_randomizer import randomize_synthesis
from BaseClasses import ItemClassification

def setup_game(world):
    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

    if world.starting_warp_room is None:  # UT will have already grabbed it
        if world.options.shuffle_starting_warp_room:
            world.starting_warp_room = world.random.choice(warp_room_table)
        else:
            world.starting_warp_room = "Lost Village"

    world.starting_warp_region = warp_room_regions[world.starting_warp_room]

    set_souls_for_walls(world)
    place_souls(world)
    randomize_synthesis(world)


def place_static_items(world):
    world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))
    world.get_location("Garden of Madness: Central Chamber").place_locked_item(world.create_item("Power of Darkness"))
    world.get_location("Abyss Center").place_locked_item(world.create_item("Menace Defeated"))

    if world.options.goal:
        world.get_location("The Pinnacle: Throne Room").place_locked_item(world.create_item("Aguni Defeated"))


def place_souls(world):
    soul_location_count = 0
    extra_souls = 0

    world.important_souls.update(world.red_soul_walls)
    if world.options.soulsanity_level == SoulsanityLevel.option_rare and world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.important_souls.add("Imp Soul")

    if world.options.goal:
        world.common_souls.update(["Slogra Soul", "Black Panther Soul"])
        world.uncommon_souls.update(["Ripper Soul", "Mud Demon Soul", "Gaibon Soul", "Malacoda Soul"])
        world.rare_souls.update(["Giant Slug Soul", "Stolas Soul", "Arc Demon Soul"])
    
    world.options.guaranteed_souls.value = {item.title() for item in world.options.guaranteed_souls.value}
    # Conver this to proper casing
    if "Common" in world.options.guaranteed_souls:
        for soul in world.common_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Common")

    if "Uncommon" in world.options.guaranteed_souls.value:
        for soul in world.uncommon_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Uncommon")

    if "Rare" in world.options.guaranteed_souls.value:
        for soul in world.rare_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Rare")

    for soul in world.options.guaranteed_souls:
        world.multiworld.itempool.append(world.set_classifications(soul))
        world.extra_item_count += 1

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        # These items are only important on Rare tier
        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            world.armor_table.remove("Soul Eater Ring")  # Don't generate a filler copy since hard guarantees one
            world.multiworld.itempool.append(world.set_classifications("Soul Eater Ring"))
            world.extra_item_count += 1

        for soul in world.important_souls:
            if soul not in world.options.guaranteed_souls:
                extra_souls += 1
                world.multiworld.itempool.append(world.set_classifications(soul))

        soul_location_count += (len(world.common_souls) - extra_souls)
        world.extra_item_count += extra_souls

        if world.options.soulsanity_level:
            soul_location_count += len(world.uncommon_souls)

        for i in range(soul_location_count):
            world.multiworld.itempool.append(world.set_classifications(world.random.choice(soul_filler_table)))
            world.extra_item_count += 1
    else:
        if not world.options.goal:
            goal_locked_enemies = {"Malacoda Soul", "Slogra Soul", "Ripper Soul"}  # These enemies are inacessible on Throne goal
            world.excluded_static_souls.update(goal_locked_enemies)
            for soul in (item for item in world.red_soul_walls if item in goal_locked_enemies):
                world.multiworld.itempool.append(world.set_classifications(soul))
                world.extra_item_count += 1

def place_static_souls(world):
    for soul in world.important_souls:
        if soul not in world.excluded_static_souls:
            world.get_location(soul).place_locked_item(world.create_static_soul(soul))