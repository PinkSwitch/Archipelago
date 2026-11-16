import typing
import os
import pkgutil
from typing import Dict
from BaseClasses import Item
from .Items import item_table
from .Rom import patch_rom, CV2ProcPatch


class CV2Item(Item):
    game: str = "Castlevania II: Simon's Quest"


def generate_early(world) -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania II: Simon's Quest" not in world.multiworld.re_gen_passthrough:
            return

        passthrough = world.multiworld.re_gen_passthrough["Castlevania II: Simon's Quest"]
        world.options.dracula_parts_required.value = passthrough["drac_parts"]
        world.options.orbs_required.value = passthrough["orbs_required"]
        world.options.poison_proof_ring.value = passthrough["poison_ring"]
        world.options.inclusive_white_crystal.value = passthrough["white_crystal"]

    world.auth_id = world.random.getrandbits(32)


def create_items(world) -> None:
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def create_item(world, name: str) -> CV2Item:
    data = set_classifications(world, name)
    return CV2Item(name, data.classification, data.code, world.player)


def get_filler_item_name(world) -> str:
    return world.random.choice(["Heart", "Half Heart", "Big Heart"])


def set_classifications(world, name) -> CV2Item:
    item_data = item_table[name]
    item = CV2Item(name, item_data.classification, item_data.code, world.player)

    return item


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "drac_parts": world.options.dracula_parts_required.value,
        "orbs_required": world.options.orbs_required.value,
        "poison_ring": world.options.poison_proof_ring.value,
        "white_crystal": world.options.inclusive_white_crystal.value,
    }


def generate_output(world, output_directory: str) -> None:
    try:
        patch = CV2ProcPatch(player=world.player, player_name=world.multiworld.player_name[world.player])
        patch.write_file("cv2_base.bsdiff4", pkgutil.get_data(__name__, "src/cv2_base.bsdiff4"))
        patch_rom(world, patch)

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
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.player_name]
