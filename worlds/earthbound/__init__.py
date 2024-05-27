import base64
import os
import typing
import threading
import pkgutil


from typing import List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from Fill import fill_restrictive
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

class EBSettings(settings.Group):
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
    settings: typing.ClassVar[EBSettings]
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
        self.event_count = 0

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
        if self.options.psi_shuffle == 0:
            self.event_count += 12

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Earth', self.player)


    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        if self.options.psi_shuffle == 0:
            excluded_items.add("Onett Teleport")
            excluded_items.add("Twoson Teleport")
            excluded_items.add("Happy-Happy Village Teleport")
            excluded_items.add("Threed Teleport")
            excluded_items.add("Saturn Valley Teleport")
            excluded_items.add("Dusty Dunes Teleport")
            excluded_items.add("Fourside Teleport")
            excluded_items.add("Winters Teleport")
            excluded_items.add("Summers Teleport")
            excluded_items.add("Scaraba Teleport")
            excluded_items.add("Deep Darkness Teleport")
            excluded_items.add("Tenda Village Teleport")
            excluded_items.add("Lost Underworld Teleport")
            excluded_items.add("Magicant Teleport")
            excluded_items.add("Progressive Poo PSI")
            excluded_items.add("Dalaam Teleport")

        if self.options.character_shuffle == 0:
            excluded_items.add("Paula")
            excluded_items.add("Jeff")
            excluded_items.add("Poo")
            excluded_items.add("Flying Man")
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.event_count): #Change to fix event count
            item = self.set_classifications(self.roll_filler())
            pool.append(item)

    def pre_fill(self) -> None:
        if self.options.psi_shuffle == 0:
            psi_locations = [
                self.multiworld.get_location("Onett - Buzz Buzz", self.player),
                self.multiworld.get_location("Onett - Mani Mani Statue", self.player),
                self.multiworld.get_location("Saturn Valley - Saturn Coffee", self.player),
                self.multiworld.get_location("Monkey Caves - Monkey Power", self.player),
                self.multiworld.get_location("Summers - Magic Cake", self.player),
                self.multiworld.get_location("Scaraba - Star Master", self.player),
                self.multiworld.get_location("Tenda Village - Tenda Tea", self.player),
                self.multiworld.get_location("Lost Underworld - Talking Rock", self.player),
                self.multiworld.get_location("Fourside - Department Store Blackout", self.player),
                self.multiworld.get_location("Cave of the Present - Star Master", self.player),
                self.multiworld.get_location("Dalaam - Trial of Mu", self.player),
                self.multiworld.get_location("Magicant - Ness's Nightmare", self.player),
            ]
            
            
            psi_items = [
                self.create_item("Onett Teleport"),
                self.create_item("Twoson Teleport"),
                self.create_item("Happy-Happy Village Teleport"),
                self.create_item("Threed Teleport"),
                self.create_item("Saturn Valley Teleport"),
                self.create_item("Dusty Dunes Teleport"),
                self.create_item("Fourside Teleport"),
                self.create_item("Winters Teleport"),
                self.create_item("Summers Teleport"),
                self.create_item("Scaraba Teleport"),
                self.create_item("Deep Darkness Teleport"),
                self.create_item("Tenda Village Teleport"),
                self.create_item("Lost Underworld Teleport"),
                self.create_item("Dalaam Teleport"),
                self.create_item("Magicant Teleport"),]

            self.random.shuffle(psi_locations) #Fix dalaam, winters, and magicant
            
            fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), psi_locations, psi_items, True, True)

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
            patch.write_file("earthbound_basepatch.bsdiff4", pkgutil.get_data(__name__, "earthbound_basepatch.bsdiff4"))
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