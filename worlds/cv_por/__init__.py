from .Items import item_table
from .Options import PoROptions, por_option_groups
from .generator_main import generate_game

class PoRWeb(WebWorld):
    theme = "ocean"
    
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Portrait of Ruin randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    option_groups = por_option_groups
    tutorials = [setup_en]

class CVPoRItem(Item):
    game: str = "Castlevania: Portrait of Ruin"

class PoRSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania: Portrait of Ruin US ROM file."""
        description = "Portrait of Ruin ROM File"
        copy_to = "CASTLEVANIA2_ACBEA4_00.nds"
        md5 = "2edd57540cae45842fbd19c45a4214f9"

class PoRWorld(World):
    """Placeholder text"""
    game = "Castlevania: Portrait of Ruin"
    option_definitions = PoROptions
    data_version = 1
    origin_region_name = "Dracula's Castle: Entrance"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()

    web = PoRWeb
    settings: typing.ClassVar[PoRSettings]
    # topology_present = True
    ut_can_gen_without_yaml = True

    options_dataclass = PoROptions
    options: PoROptions

    #locked_locations: List[str]
    #ocation_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.extra_item_count = 0
        generate_game(self)