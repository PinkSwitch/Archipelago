import typing
import os
import pkgutil

from typing import Dict
from BaseClasses import Item, ItemClassification
from .Items import item_table
from .Options import SoulRandomizer, SoulsanityLevel
from .Rom import patch_rom, DoSProcPatch
from .setup_game import setup_game, place_souls


class CVDoSItem(Item):
    game: str = "Castlevania: Dawn of Sorrow"


def generate_early(world) -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Dawn of Sorrow" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Dawn of Sorrow"]
        world.options.goal = passthrough["goal"]
        world.options.soul_randomizer = passthrough["soul_randomizer"]
        world.options.soulsanity_level = passthrough["soulsanity_level"]
        world.starting_warp_room = passthrough["starting_warp"]
        world.options.open_drawbridge = passthrough["open_drawbridge"]
        world.options.boost_speed = passthrough["speed_boost"]
        world.red_soul_walls = passthrough["soul_walls"]
        world.options.gate_items = passthrough["buttonsanity"]
        world.magic_seal_table = passthrough["seals"]
        world.options.menace_condition.value = passthrough["menace_condition"]
        world.options.mine_condition.value = passthrough["mine_condition"]
        world.options.garden_condition.value = passthrough["garden_condition"]
    setup_game(world)

    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items, place_static_souls
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)
    if world.options.soul_randomizer != SoulRandomizer.option_soulsanity:
        place_static_souls(world)

    if ((world.options.soul_randomizer != SoulRandomizer.option_soulsanity) or
            world.options.soulsanity_level < SoulsanityLevel.option_medium):
        world.get_location("Imp Soul").place_locked_item(world.create_static_soul("Imp Soul"))


def create_items(world) -> None:
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    if world.options.gate_items:
        pool.extend([set_classifications(world, "West Lab Gate Key"),
                     set_classifications(world,"East Lab Gate Key"),
                     set_classifications(world, "Garden Gate Key"),
                     set_classifications(world, "Cavern Gate Key")])

    placed_seals = []

    for seal in world.magic_seal_table:
        if seal in ["Mine of Judgment", "The Abyss"] and world.mine_status == "Disabled":
            continue
        else:
            if world.magic_seal_table[seal] not in placed_seals:
                pool.append(set_classifications(world, world.magic_seal_table[seal]))  # Create the seal items if necessary)
                placed_seals.append(world.magic_seal_table[seal])

    place_souls(world)

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def set_classifications(world, name: str) -> CVDoSItem:
    data = item_table[name]
    item = CVDoSItem(name, data.classification, data.code, world.player)
    if name in world.important_souls:
        item.classification = ItemClassification.progression

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        if name == "Soul Eater Ring" and world.options.soulsanity_level == SoulsanityLevel.option_rare:
            item.classification = ItemClassification.progression

    return item


def create_item(world, name: str) -> CVDoSItem:
    data = set_classifications(world, name)
    return CVDoSItem(name, data.classification, data.code, world.player)


def get_filler_item_name(world) -> str:
    from .Items import consumable_table, money_table, soul_filler_table
    weights = {"soul": 10, "money": 20, "weapon": 30, "armor": 40, "consumable": 60}

    # If these pools have been exhausted, set their weights to 0
    if not world.weapon_table:
        weights["weapon"] = 0

    if not world.armor_table:
        weights["armor"] = 0

    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    weight_table = {
        "soul": soul_filler_table,
        "weapon": world.weapon_table,
        "armor": world.armor_table,
        "money": money_table,
        "consumable": consumable_table,
    }

    filler_item = world.random.choice(weight_table[filler_type])

    if filler_item in world.weapon_table:
        world.weapon_table.remove(filler_item)
    elif filler_item in world.armor_table:
        world.armor_table.remove(filler_item)

    if not world.has_tried_chaos_ring:
        world.has_tried_chaos_ring = True
        if world.random.randint(0, 101) <= 10:  # Chaos ring should have a single 10/100 chance to be placed
            filler_item = "Chaos Ring"

    return filler_item


def create_static_soul(world, soul):
    data = item_table[soul]
    item = Item(soul, ItemClassification.progression, None, world.player)  # Create an event item of the soul
    return item


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "goal": world.options.goal.value,
        "starting_warp": world.starting_warp_room,
        "soul_randomizer": world.options.soul_randomizer.value,
        "soulsanity_level": world.options.soulsanity_level.value,
        "open_drawbridge": world.options.open_drawbridge.value,
        "speed_boost": world.options.boost_speed.value,
        "soul_walls": world.red_soul_walls,
        "buttonsanity": world.options.gate_items.value,
        "seals": world.magic_seal_table,
        "menace_condition": world.options.menace_condition.value,
        "garden_condition": world.options.garden_condition.value,
        "mine_condition": world.options.mine_condition.value
    }