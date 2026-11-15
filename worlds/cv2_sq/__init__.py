import settings
import typing
import threading
from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld
from .Options import CV2Options, cv2_option_groups
from .Items import item_table, get_item_names_per_category
from .static_location_data import get_location_groups, location_ids
from .generator_main import (generate_early, create_items, create_item, get_filler_item_name,
                             create_regions, set_rules)


class CV2Web(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Castlevania II randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    option_groups = cv2_option_groups
    tutorials = [setup_en]


class CV2Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania II: Simon's Quest US ROM file."""
        description = "Castlevania II ROM File"
        copy_to = "CastlevaniaIISimonsQuest.nes"
        md5 = "87Dae73b0c4C8fdeba8cf4209df87e2c"

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CV2World(World):
    """Wuh oh! John Castlevania Castlevania'd too hard! Now he has to revive Dracula and
       kicc his ass before he dies of ligma"""
    game = "Castlevania II: Simon's Quest"
    option_definitions = CV2Options
    data_version = 1
    origin_region_name = "Town of Jova"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    web = CV2Web()
    settings: typing.ClassVar[CV2Settings]
    # topology_present = True
    ut_can_gen_without_yaml = True

    location_name_groups = get_location_groups()
    options_dataclass = CV2Options
    options: CV2Options
    generate_early = generate_early
    create_items = create_items
    create_item = create_item
    create_regions = create_regions
    #fill_slot_data = fill_slot_data
    #modify_multidata = modify_multidata
    #generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    set_rules = set_rules
    # connect_entrances = connect_entrances
    # write_spoiler_header = write_spoiler_header

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.location_cache = []
