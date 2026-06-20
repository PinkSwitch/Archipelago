import typing
import settings

from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld

from .Options import OoEOptions, ooe_option_groups


class OoEWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Order of Ecclesia randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    option_groups = ooe_option_groups
    tutorials = [setup_en]


class OoESettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania: Order of Ecclesia US ROM file."""
        description = "Order of Ecclesia ROM File"
        copy_to = "CASTLEVANIA3_YR9EA4_00.nds"
        md5 = "e13bdcf706989486df939556eeb42ece"

    rom_file: RomFile = RomFile(RomFile.copy_to)


class OoEWorld(World):
    """placeholder"""
    game = "Castlevania: Order of Ecclesia"
    option_definitions = OoEOptions
    data_version = 1
    origin_region_name = "Ecclesia"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    web = OoEWeb()
    settings: typing.ClassVar[OoESettings]
    # topology_present = True
    ut_can_gen_without_yaml = True