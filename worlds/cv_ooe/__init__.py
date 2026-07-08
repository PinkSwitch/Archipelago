import typing
import settings
import threading

from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld

from .Items import item_table, get_item_names_per_category
from .static_location_data import location_ids, get_location_groups
from .Options import OoEOptions, ooe_option_groups
from .generator_main import (generate_early, create_regions, create_items, create_item, get_filler_item_name)


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

    location_name_groups = get_location_groups()
    options_dataclass = OoEOptions
    options: OoEOptions
    generate_early = generate_early
    create_items = create_items
    create_item = create_item
    create_regions = create_regions
    #fill_slot_data = fill_slot_data
    #modify_multidata = modify_multidata
    #generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    #set_rules = set_rules
    #write_spoiler_header = write_spoiler_header

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.location_cache = []
        self.has_tried_master_ring = False
        self.has_tried_queen_of_hearts = False
        self.has_generated_output = False
        self.starting_glyph = None

        self.glyph_filler_table = [
            "Vol Confodere",
            "Secare",
            "Melio Secare",
            "Hasta",
            "Melio Macir",
            "Arcus",
            "Ascia",
            "Vol Falcis",
            "Vol Culter",
            "Vol Scutum",
            "Torpor",
            "Ignis",
            "Grando",
            "Fulgur",
            "Vol Luminatio",
            "Nitesco",
            "Acerbatus",
            "Globus",
            "Arma Felix",
            "Arma Chiroptera",
            "Fidelis Caries",
            "Fidelis Alate",
            "Fidelis Polkir",
            "Fidelis Noctua",
            "Fidelis Medusa",
            "Fidelis Aranea",
            "Fidelis Mortus"]
            
        self.armor_table = []

        self.good_armor_table = []

        self.accessory_table = [
            "Protect Ring",
            "Resist Ring",
            "Archer Ring",
            "Blow Ring",
            "Wind Ring",
            "Ruby Ring",
            "Sapphire Ring",
            "Emerald Ring",
            "Diamond Ring",
            "Onyx Ring",
            "Heart Earrings",
            "Gold Ring",
            "Miser Ring",
            "Lucky Clover",
            "Thief Ring"]
