import typing
import os
import pkgutil

from typing import Dict
from BaseClasses import Item, ItemClassification
from .Items import item_table
from .Options import RandomGlyphAttributes, RandomStolenGlyphs, RandomDropGlyphs
from .Rom import patch_rom, OoEProcPatch


class CVOoEItem(Item):
    game: str = "Castlevania: Order of Ecclesia"


def generate_early(world) -> None:
    from .setup_game import setup_game
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Order of Ecclesia" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Order of Ecclesia"]
        world.options.starting_glyph.value = passthrough["starting_glyph"]
        world.options.shuffle_dominus.value = passthrough["shuffle_dominus"]
        world.options.villagers_required.value = passthrough["villagers_required"]
        world.options.starting_area.value = passthrough["starting_area"]
        world.options.remove_large_cavern.value = passthrough["remove_large_cavern"]
        world.options.remove_training_hall.value = passthrough["remove_training_hall"]
        world.options.start_with_lizard_tail.value = passthrough["start_with_lizard_tail"]
        world.options.start_with_glyph_union.value = passthrough["start_with_glyph_union"]
        world.options.add_brown_chests.value = passthrough["add_brown_chests"]
        world.options.starting_villagers.value = passthrough["starting_villagers"]
        world.options.randomize_villagers.value = passthrough["randomize_villagers"]
        world.options.add_no_hit_chests.value = passthrough["add_medal_chests"]
        world.options.barlowe_required.value = passthrough["barlowe_required"]
        world.options.open_castle.value = passthrough["open_castle"]
        world.glyph_attributes = passthrough["glyph_attributes"]
        world.options.randomize_stolen_glyphs.value = passthrough["stolen_glyphs"]
        world.options.randomize_dropped_glyphs.value = passthrough["dropped_glyphs"]
        world.can_kill_tin_man = passthrough["tin_man_glyph_logic"]
        world.generator_logic_glyphs = passthrough["generator_logic"]
        world.connected_doors = passthrough["door_map"]

    setup_game(world)
    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)


def connect_entrances(world) -> None:
    from .modules.area_shuffle import shuffle_doors, set_ut_regions
    if world.connected_doors:
        set_ut_regions(world)

    if world.options.randomize_castle_doors and not world.connected_doors:
        shuffle_doors(world)


def create_items(world) -> None:
    from .generator_items import create_conditional_items, generate_emergency_glyphs
    pool = []
    for name, data in item_table.items():
        #  First we fill the base pool, all items as set in the Items file
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    for glyph in world.glyph_pool:  # Place all of the static glyphs here
        pool.append(set_classifications(world, glyph))

    create_conditional_items(world, pool)

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count - 2):  # Leave a couple spaces open for Emergency glyphs
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)
    generate_emergency_glyphs(world, pool)

    world.multiworld.itempool += pool


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def set_classifications(world, name) -> CVOoEItem:
    # Make quest items be prog, here.
    item_data = item_table[name]
    item = CVOoEItem(name, item_data.classification, item_data.code, world.player)
    if name in world.logical_regular_glyphs:
        item.classification = ItemClassification.progression  # If this is a Glyph with logic, make sure it's Progress!
    elif name in world.glyph_pool:
        item.classification = ItemClassification.useful  # If this is a Static Glyph, make it Useful as it's unique!

    return item


def create_item(world, name: str) -> CVOoEItem:
    data = set_classifications(world, name)
    return CVOoEItem(name, data.classification, data.code, world.player)


def create_progress_event(world, name: str) -> CVOoEItem:
    # Create item name [str] as a Progression Event item.
    return CVOoEItem(name, ItemClassification.progression, None, world.player)


def get_filler_item_name(world) -> str:
    from .Items import money_table, good_food_table, consumable_table, drops_table
    weights = {"drops": 3, "glyph": 10, "accessory": 10, "good_food": 8, "good_armor": 15, "money": 20,
               "armor": 40, "consumable": 60}

    weight_table = {
        "glyph": world.glyph_filler_table,
        "armor": world.armor_table,
        "good_armor": world.good_armor_table,
        "money": money_table,
        "consumable": consumable_table,
        "good_food": good_food_table,
        "accessory": world.accessory_table,
        "drops": drops_table
    }
    for fill_type, table in weight_table.items():
        if not table:  # Remove empty tables to prevent them from being chosen
            weights[fill_type] = 0

    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    filler_item = world.random.choice(weight_table[filler_type])
    if not world.has_tried_master_ring:
        world.has_tried_master_ring = True
        if world.random.randint(0, 101) <= 10:
            filler_item = "Master Ring"
            return filler_item

    if not world.has_tried_queen_of_hearts:
        world.has_tried_queen_of_hearts = True
        if world.random.randint(0, 101) <= 10:
            filler_item = "Queen of Hearts"
            return filler_item

    if filler_type not in ["consumable", "good_food", "money", "drops"]:
        # Remove equipment from the corresponding table so it doesn't gen again
        weight_table[filler_type].remove(filler_item)

    return filler_item


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "starting_glyph": world.options.starting_glyph.value,
        "shuffle_dominus": world.options.shuffle_dominus.value,
        "start_with_lizard_tail": world.options.start_with_lizard_tail.value,
        "start_with_glyph_union": world.options.start_with_glyph_union.value,
        "add_brown_chests": world.options.add_brown_chests.value,
        "villagers_required": world.options.villagers_required.value,
        "starting_villagers": world.options.starting_villagers.value,
        "randomize_villagers": world.options.randomize_villagers.value,
        "starting_area": world.options.starting_area.value,
        "remove_training_hall": world.options.remove_training_hall.value,
        "remove_large_cavern": world.options.remove_large_cavern.value,
        "add_medal_chests": world.options.add_no_hit_chests.value,
        "barlowe_required": world.options.barlowe_required.value,
        "open_castle": world.options.open_castle.value,
        "glyph_attributes": world.glyph_attributes,
        "stolen_glyphs": world.options.randomize_stolen_glyphs.value,
        "dropped_glyphs": world.options.randomize_dropped_glyphs.value,
        "tin_man_glyph_logic": world.can_kill_tin_man,
        "generator_logic": world.generator_logic_glyphs,
        "door_map": world.connected_doors
    }


def generate_output(world, output_directory: str) -> None:
    try:
        code_patch = pkgutil.get_data(__name__, "src/overlay_86.bin")
        patch = OoEProcPatch(player=world.player, player_name=world.multiworld.player_name[world.player])
        patch.write_file("ooe_base.bsdiff4", pkgutil.get_data(__name__, "src/ooe_base.bsdiff4"))
        patch_rom(world, patch, code_patch)

        world.rom_name = patch.name

        patch.write(os.path.join(output_directory,
                                 f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))
    except Exception:
        raise
    finally:
        world.rom_name_available_event.set()  # make sure threading continues and errors are collected


def write_spoiler_header(world, spoiler_handle: typing.TextIO) -> None:
    from .modules.area_shuffle import door_data
    if world.options.randomize_glyph_attributes:
        spoiler_handle.write("\nGlyph Attributes:\n")

        for index, glyph in enumerate(world.glyph_attributes):
            if world.options.randomize_glyph_attributes != RandomGlyphAttributes.option_chaotic:
                if any(x in glyph for x in ["Vol", "Melio"]) or index >= 47:
                    continue
            attributes = " + ".join(world.glyph_attributes[glyph])
            spoiler_handle.write(f"   {glyph}: {attributes}\n")

    if (world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_shuffled or
            world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_shuffled):
        spoiler_handle.write("\nEnemy Glyphs:")

        if world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_shuffled:
            for enemy in world.glyph_steals:
                spoiler_handle.write(f"\n   {enemy}: {world.glyph_steals[enemy]}")

        if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_shuffled:
            for enemy in world.glyph_drops:
                spoiler_handle.write(f"\n   {enemy}: {world.glyph_drops[enemy]}")
        spoiler_handle.write("\n")

    if world.options.randomize_castle_doors:
        spoiler_handle.write("\nCastle Entrances:")
        for door in world.connected_doors:
            if not door_data[door[0]].is_left_facing:
                continue
            spoiler_handle.write(f"\n   {door_data[door[0]].entrance_name} <=> {door_data[door[1]].entrance_name}")
    spoiler_handle.write("\n")


def modify_multidata(world, multidata: dict) -> None:
    # wait for self.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.player_name]
