import typing
import os
import pkgutil

from typing import Dict
from BaseClasses import Item, ItemClassification
from .Items import item_table
from .Options import RandomizeVillagers
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
        world.options.starting_villagers.value = passthrough["add_brown_chests"]
        world.options.randomize_villagers.value = passthrough["randomize_villagers"]

    setup_game(world)
    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)


def create_items(world) -> None:
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    if set_classifications(world, world.starting_glyph) in pool:
        pool.remove(set_classifications(world, world.starting_glyph))

    if world.options.remove_large_cavern:
        pool.remove(set_classifications(world, "Map: Large Cavern"))

    if world.options.remove_training_hall:
        pool.remove(set_classifications(world, "Map: Training Hall"))

    if world.options.shuffle_dominus:
        pool.extend([set_classifications(world, "Dominus Hatred"),
                     set_classifications(world, "Dominus Anger"),
                     set_classifications(world, "Dominus Agony")])

    if world.starting_area:
        pool.remove(set_classifications(world, f"Map: {world.starting_area}"))

    if world.options.randomize_villagers == RandomizeVillagers.option_anywhere:
        pool.extend([set_classifications(world, "Nikolai"),
                     set_classifications(world, "Jacob"),
                     set_classifications(world, "Abram"),
                     set_classifications(world, "Laura"),
                     set_classifications(world, "Eugen"),
                     set_classifications(world, "Aeon"),
                     set_classifications(world, "Marcel"),
                     set_classifications(world, "George"),
                     set_classifications(world, "Serge"),
                     set_classifications(world, "Anna"),
                     set_classifications(world, "Monica"),
                     set_classifications(world, "Irina"),
                     set_classifications(world, "Daniela")])

        for villager in world.options.starting_villagers:
            pool.remove(set_classifications(world, villager))

    if world.options.start_with_glyph_sleeve:
        pool.remove(set_classifications(world, "Glyph Sleeve"))

    if world.options.start_with_glyph_union:
        pool.remove(set_classifications(world, "Glyph Union"))

    if world.options.start_with_lizard_tail:
        pool.remove(set_classifications(world, "Lizard Tail"))

    if world.starting_glyph in world.glyph_filler_table:
        world.glyph_filler_table.remove(world.starting_glyph)

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def set_classifications(world, name) -> CVOoEItem:
    # Make quest items be prog, here.
    item_data = item_table[name]
    item = CVOoEItem(name, item_data.classification, item_data.code, world.player)
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
               "armor": 40, "consumable": 60}  # TODO; tweak

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
        weight_table[filler_type].remove(filler_item)  # Remove equipment from the corresponding table so it doesn't gen again

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
        "remove_large_cavern": world.options.remove_large_cavern.value
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


def modify_multidata(world, multidata: dict) -> None:
    # wait for self.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.multiworld.player_name[world.player]]
