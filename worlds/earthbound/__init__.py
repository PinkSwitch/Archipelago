import base64
import os
import typing
import threading

from typing import List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, item_table, common_items, uncommon_items, rare_items
from .Locations import get_locations
from .Regions import init_areas
from .Options import EBOptions
from .setup_game import setup_gamevars, place_static_items
from .Client import EarthBoundClient
from .Rules import set_location_rules
from .Rom import LocalRom, patch_rom, get_base_rom_path, EBProcPatch, USHASH

class ESettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the EarthBound US ROM"""
        description = "EarthBound ROM File"
        copy_to = "EarthBound.sfc"
        md5s = [USHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class EBWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the EarthBound randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

class EarthBoundWorld(World):
    """EarthBound is a contemporary-themed JRPG. Take four psychically-endowed children
       across the world in search of 8 Melodies to defeat Giygas, the cosmic evil."""
    game = "EarthBound"
    option_definitions = EBOptions
    data_version = 1
    required_client_version = (0, 4, 6)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for
                           location in get_locations(None)}
    item_name_groups = get_item_names_per_category()

    web = EBWeb()
    settings: typing.ClassVar[EBOptions]
    #topology_present = True

    options_dataclass = EBOptions
    options: EBOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

        self.locked_locations= []
        self.location_cache= []

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))
        place_static_items(self)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def roll_filler(self) -> str: #Todo: make this suck less
        weights = {"rare": self.options.rare_filler_weight.value, "uncommon": self.options.uncommon_filler_weight.value, "common": self.options.common_filler_weight.value}
        choices = self.random.choices(list(weights), weights=list(weights.values()), k=len(self.multiworld.get_unfilled_locations(self.player)))
        filler_type = self.random.choice(choices)
        weight_table = {
            "common": common_items,
            "uncommon": uncommon_items,
            "rare": rare_items
        }
        return self.random.choice(weight_table[filler_type])

    def generate_early(self):#Todo: place locked items in generate_early
        self.locals = []
        setup_gamevars(self)

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Earth', self.player)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.set_classifications(self.roll_filler())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        return pool

    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player
            patch = EBProcPatch()
            patch_rom(self, patch, self.player, self.multiworld)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]