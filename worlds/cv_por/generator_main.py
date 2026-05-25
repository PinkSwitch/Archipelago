import os
import typing
import pkgutil

from BaseClasses import Item, ItemClassification
from typing import Dict, TextIO
from .Items import item_table
from .Options import PortraitShuffle, NestofEvil
from .modules.portrait_shuffle import portrait_data
from .modules.quest_data import quest_data


class CVPoRItem(Item):
    game: str = "Castlevania: Portrait of Ruin"


def generate_early(world) -> None:
    from .setup_game import setup_game
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Portrait of Ruin" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Portrait of Ruin"]
        world.options.goal.value = passthrough["goal"]
        world.options.start_with_change_cube.value = passthrough["start_with_change_cube"]
        world.options.brauner_portraits.value = passthrough["brauner_portraits"]
        world.options.dracula_portraits.value = passthrough["dracula_portraits"]
        world.options.nest_portraits.value = passthrough["nest_portraits"]
        world.options.nest_of_evil_state.value = passthrough["nest_of_evil"]
        world.options.brauner_required.value = passthrough["brauner_required"]
        world.options.stronger_glove.value = passthrough["stronger_glove"]
        world.options.randomized_quests.value = passthrough["active_quests"]
        world.options.excluded_quests.value = passthrough["excluded_quests"]
        world.options.start_with_call_cube = passthrough["start_with_call_cube"]

        world.portrait_connections["City of Haze"] = passthrough["hub_portrait"]
        world.portrait_connections["Sandy Grave"] = passthrough["underground_portrait"]
        world.portrait_connections["Nation of Fools"] = passthrough["stairs_portrait"]
        world.portrait_connections["Forest of Doom"] = passthrough["tower_portrait"]
        world.portrait_connections["Forgotten City"] = passthrough["brauner_portrait_1"]
        world.portrait_connections["13th Street"] = passthrough["brauner_portrait_2"]
        world.portrait_connections["Burnt Paradise"] = passthrough["brauner_portrait_3"]
        world.portrait_connections["Dark Academy"] = passthrough["brauner_portrait_4"]
        world.portrait_connections["Nest of Evil"] = passthrough["passage_portrait"]
    setup_game(world)
    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)

def create_items(world) -> None:
    from .modules.quest_data import cakes_notforsale
    force_create_blacklist = ["Gold Ring", "Knife Subweapon", "Cross", "Holy Water", "Bible",
                              "Bwaka Knife", "Paper Airplane", "Cream Pie", "Grenade", "Steel Ball",
                              "Stonewall", "Offensive Form", "Taunt", "Knee Strike", "Aura Blast",
                              "Rocket Slash", "Toad Morph", "Owl Morph", "Sanctuary", "Speed Up", "Eye for an Eye",
                              "Clear Skies", "Time Stop", "Heal", "Cure Poison", "STR Boost",
                              "CON Boost", "INT Boost", "MIND Boost", "LUCK Boost", "ALL Boost", "Gale Force",
                              "Raging Fire", "Ice Fang", "Thunderbolt", "Tempest", "Piercing Beam", "Cocytus",
                              "Nun's Habit", "Nun's Robes", "Nun's Shoes", "Long Sword", "Birthday Cake",]  # We want to specifically NEVER forcibly create these.

    if world.options.nest_of_evil_state == NestofEvil.option_removed:
        force_create_blacklist.remove("Cocytus")

    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    if world.options.shuffle_whip:
        pool.append(set_classifications(world, "True Vampire Killer"))

    if world.options.add_extra_items:
        pool.extend([
            set_classifications(world, "Puppet Master"),
            set_classifications(world, "Tori"),
            set_classifications(world, "Seiryu"),
            set_classifications(world, "Suzaku"),
            set_classifications(world, "Byakko"),
            set_classifications(world, "Gnebu"),
        ])

    if not world.options.exclude_owl_morph:
        pool.append(set_classifications(world, "Owl Morph"))

    if not world.options.start_with_call_cube:
        pool.append(set_classifications(world, "Call Cube"))

    if not world.options.start_with_change_cube:
        pool.append(set_classifications(world, "Change Cube"))

    if world.options.nest_of_evil_state:
        pool.extend([
            set_classifications(world, "Greatest Five"),
            set_classifications(world, "Tome of Arms p1"),
            set_classifications(world, "Tome of Arms p2"),
        ])
        
    for item in world.quest_reward_pool:
        pool.append(set_classifications(world, item))
        
    for quest in world.important_quests:
        if quest in world.vanilla_quests and quest not in world.important_quests:
            continue

        if quest == "Quest: Build Your Strength 3":
            pool.append(set_classifications(world, world.random.choice(cakes_notforsale)))
            
        if quest_data[quest].requires_filler_items:
            for item in quest_data[quest].required_items:
                #  We don't want to regenerate any of these as filler because we know we need them here
                if item in world.subweapon_filler_table:
                    world.subweapon_filler_table.remove(item)

                if item in world.good_weapon_table:
                    world.good_weapon_table.remove(item)

                if item in world.weapon_table:
                    world.weapon_table.remove(item)

                if item in world.armor_table:
                    world.armor_table.remove(item)

                if item in world.good_armor_table:
                    world.good_armor_table.remove(item)

                if item in world.accessory_table:
                    world.accessory_table.remove(item)
                    
                if item not in pool and item not in force_create_blacklist:
                    pool.append(set_classifications(world, item))


    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def set_classifications(world, name) -> CVPoRItem:
    # Make quest items be prog, here.
    item_data = item_table[name]
    item = CVPoRItem(name, item_data.classification, item_data.code, world.player)
    if item.name in world.quest_requirements:
        if ItemClassification.trap in item.classification:
            item.classification |= ItemClassification.progression  # Traps should be ProgTrap
        else:
            item.classification = ItemClassification.progression

    return item


def generate_output(world, output_directory: str) -> None:
    from .Rom import PoRProcPatch, patch_rom
    try:
        code_patch = pkgutil.get_data(__name__, "src/overlay_119.bin")
        patch = PoRProcPatch(player=world.player, player_name=world.multiworld.player_name[world.player])
        patch.write_file("por_base.bsdiff4", pkgutil.get_data(__name__, "src/por_base.bsdiff4"))
        patch_rom(world, patch, code_patch)

        world.rom_name = patch.name

        patch.write(os.path.join(output_directory,
                                 f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))
    except Exception:
        raise
    finally:
        world.rom_name_available_event.set()  # make sure threading continues and errors are collected


def write_spoiler_header(world, spoiler_handle: TextIO) -> None:
    if world.options.portrait_shuffle:
        spoiler_handle.write("""
Portraits:
""")
        for connection in world.portrait_connections:
            if connection != "Nest of Evil":
                spoiler_handle.write(f""" {portrait_data[connection].spoiler_map_name}: {world.portrait_connections[connection]}
""")

        if world.options.portrait_shuffle == PortraitShuffle.option_add_nest_of_evil:
            spoiler_handle.write(f""" {portrait_data["Nest of Evil"].spoiler_map_name}: {world.portrait_connections["Nest of Evil"]}
""")


def modify_multidata(world, multidata: dict) -> None:
    # wait for self.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.multiworld.player_name[world.player]]


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "goal": world.options.goal.value,
        "start_with_change_cube": world.options.start_with_change_cube.value,
        "brauner_portraits": world.options.brauner_portraits.value,
        "dracula_portraits": world.options.dracula_portraits.value,
        "nest_portraits": world.options.nest_portraits.value,
        "nest_of_evil": world.options.nest_of_evil_state.value,
        "brauner_required": world.options.brauner_required.value,
        "stronger_glove": world.options.stronger_glove.value,
        "active_quests": world.options.randomized_quests.value,
        "excluded_quests": world.options.excluded_quests.value,
        "start_with_call_cube": world.options.start_with_call_cube.value,

        "hub_portrait": world.portrait_connections["City of Haze"],
        "underground_portrait": world.portrait_connections["Sandy Grave"],
        "stairs_portrait": world.portrait_connections["Nation of Fools"],
        "tower_portrait": world.portrait_connections["Forest of Doom"],
        "brauner_portrait_1": world.portrait_connections["Forgotten City"],
        "brauner_portrait_2": world.portrait_connections["13th Street"],
        "brauner_portrait_3": world.portrait_connections["Burnt Paradise"],
        "brauner_portrait_4": world.portrait_connections["Dark Academy"],
        "passage_portrait": world.portrait_connections["Nest of Evil"]

    }

def extend_hint_information(world, hint_data: Dict[int, Dict]) -> None:
    from .static_location_data import location_ids
    hint_struct = {
    }
    if world.options.portrait_shuffle:
        for connection in world.portrait_connections:
            locations_per_region = []
            room = portrait_data[connection].spoiler_map_name
            destination = world.portrait_connections[connection]
            region = world.location_name_groups[destination]
            for location in region:
                hint_struct[location_ids[location]] = room
        
        hint_data[world.player] = hint_struct


def get_filler_item_name(world) -> str:
    from .Items import money_table, good_food_table, consumable_table
    weights = {"subweapon": 5, "good_weapon": 7, "accessory": 8, "good_food": 10, "good_armor": 15, "money": 20,
               "weapon": 30, "armor": 40, "consumable": 60}

    weight_table = {
        "subweapon": world.subweapon_filler_table,
        "good_weapon": world.good_weapon_table,
        "weapon": world.weapon_table,
        "armor": world.armor_table,
        "good_armor": world.good_armor_table,
        "money": money_table,
        "consumable": consumable_table,
        "good_food": good_food_table,
        "accessory": world.accessory_table
    }
    for fill_type, table in weight_table.items():
        if not table:  # Remove empty tables to prevent them from being chosen
            weights[fill_type] = 0

    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    filler_item = world.random.choice(weight_table[filler_type])
    if not world.has_tried_magus_ring:
        world.has_tried_magus_ring = True
        if world.random.randint(0, 101) <= 10:  # Magus ring should have a single 10/100 chance to be placed
            filler_item = "Magus Ring"
            return filler_item

    if filler_type not in ["consumable", "good_food", "money"]:
        weight_table[filler_type].remove(filler_item)  # Remove equipment from the corresponding table so it doesn't gen again

    return filler_item


def create_item(world, name: str) -> CVPoRItem:
    data = set_classifications(world, name)
    return CVPoRItem(name, data.classification, data.code, world.player)

def create_item_as_event(world, name: str) -> CVPoRItem:
    # The same as create item, but forces the code to None instead. This lets us create pseudochecks for inactive quests
    data = set_classifications(world, name)
    return CVPoRItem(name, data.classification, None, world.player)
