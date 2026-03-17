from .Options import SoulsanityLevel, SoulRandomizer, MineCondition, GardenCondition
from .Items import soul_filler_table
from .in_game_data import warp_room_regions, warp_room_table
from .bullet_wall_randomizer import set_souls_for_walls
from .synthesis_randomizer import randomize_synthesis
from .boss_randomizer import randomize_bosses
from .seal_shuffle import set_seals
from BaseClasses import ItemClassification

def setup_game(world):

    world.mine_status = None
    if not world.options.goal:
        if world.options.mine_condition == MineCondition.option_throne_room or (
                    world.options.mine_condition == MineCondition.option_garden and 
                    world.options.garden_condition == GardenCondition.option_throne_room):
            world.mine_status = "Disabled"  # Make sure we don't generate Mine checks if the Mine is unreachable.

    if not world.mine_status:  # If we didn't just disable it, set the status here
        if world.options.mine_condition != MineCondition.option_none:
            world.mine_status == "Locked"
        else:
            world.mine_status == "Open"


    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

    if world.starting_warp_room is None:  # UT will have already grabbed it
        if world.options.shuffle_starting_warp_room:
            world.starting_warp_room = world.random.choice(warp_room_table)
        else:
            world.starting_warp_room = "Lost Village"

    world.starting_warp_region = warp_room_regions[world.starting_warp_room]

    if world.options.gate_items:
        world.multiworld.itempool.append(world.set_classifications("West Lab Gate Key"))
        world.multiworld.itempool.append(world.set_classifications("East Lab Gate Key"))
        world.multiworld.itempool.append(world.set_classifications("Garden Gate Key"))
        world.multiworld.itempool.append(world.set_classifications("Cavern Gate Key"))
        world.extra_item_count += 4

    set_seals(world)
    set_souls_for_walls(world)
    place_souls(world)
    randomize_synthesis(world)

    if world.options.boss_shuffle:
        randomize_bosses(world)

    menace_bosses = 13
    mine_bosses = 11
    garden_bosses = 13

    if world.mine_status == "Disabled":  # Remove the post-Mine bosses
        menace_bosses -= 2
        garden_bosses -= 2

    if not world.options.goal:  # Remove Aguni
        menace_bosses -= 1
        mine_bosses -= 1
        garden_bosses -= 1

    world.menace_triggers = {
        "throne_room": lambda state: state.has("Aguni Defeated", world.player),
        "garden": lambda state: state.has("Power of Darkness", world.player),
        "bosses": lambda state: state.has("Boss Defeated", menace_bosses, world.player)
    }

    world.mine_triggers = {
        "throne_room": lambda state: state.has("Aguni Defeated", world.player),
        "garden": lambda state: state.has("Power of Darkness", world.player),
        "bosses": lambda state: state.has("Boss Defeated", mine_bosses, world.player)
    }

    world.garden_triggers = {
        "throne_room": lambda state: state.has("Aguni Defeated", world.player),
        "bosses": lambda state: state.has("Boss Defeated", garden_bosses, world.player)
    }

def place_static_items(world):
    world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))
    world.get_location("Garden of Madness: Central Chamber").place_locked_item(world.create_item("Power of Darkness"))
    world.get_location("Abyss Center").place_locked_item(world.create_item("Menace Defeated"))

    world.get_location("Lost Village: Flying Armor").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Wizardry Lab: Balore").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Dark Chapel: Dimitrii").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Dark Chapel Inner: Malphas").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Garden of Madness: Dario").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Demon Guest House: Puppet Master").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Subterranean Hell: Rahab").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Condemned Tower: Gergoth").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Cursed Clock Tower: Zephyr").place_locked_item(world.create_item("Boss Defeated"))
    world.get_location("Silenced Ruins: Bat Company").place_locked_item(world.create_item("Boss Defeated"))

    if world.options.goal:
        world.get_location("The Pinnacle: Throne Room").place_locked_item(world.create_item("Aguni Defeated"))
        world.get_location("The Pinnacle: Aguni").place_locked_item(world.create_item("Boss Defeated"))

    if world.mine_status != "Disabled":
        world.get_location("The Abyss: Abaddon").place_locked_item(world.create_item("Boss Defeated"))
        world.get_location("Mine of Judgment: Death").place_locked_item(world.create_item("Boss Defeated"))


def place_souls(world):
    soul_location_count = 0
    extra_souls = 0

    world.important_souls.update(world.red_soul_walls)
    if world.options.soulsanity_level == SoulsanityLevel.option_rare and world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.important_souls.add("Imp Soul")

    if world.mine_status != "Disabled":
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
        if world.mine_status == "Disabled":
            goal_locked_enemies = {"Malacoda Soul", "Slogra Soul", "Ripper Soul"}  # These enemies are inacessible if Mine is removed
            world.excluded_static_souls.update(goal_locked_enemies)
            for soul in (item for item in world.red_soul_walls if item in goal_locked_enemies):
                world.multiworld.itempool.append(world.set_classifications(soul))
                world.extra_item_count += 1

def place_static_souls(world):
    for soul in world.important_souls:
        if soul not in world.excluded_static_souls:
            world.get_location(soul).place_locked_item(world.create_static_soul(soul))