import os
import typing
import threading
import pkgutil
import json


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, filler_item_table, item_table
from .Locations import get_locations
from .Regions import init_areas
from .Options import FSAOptions, fsa_option_groups
from .Rules import set_location_rules
from .Rom import apply_patch
from .static_location_data import location_ids
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths

def run_client(*args):
    print("Running FSA Client")
    from .Client import launch
    launch_subprocess(launch, name="FSAdventuresClient", args=args)

components.append(
    Component("Four Swords Adventures Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apfsa"))
)


class FSAWeb(WebWorld):
    theme = "ocean"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the FSA randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Pink Switch"]
    )

    tutorials = [setup_en]

    option_groups = fsa_option_groups


class FSAdventuresWorld(World):
    """Bottom text"""
    
    game = "The Legend of Zelda: Four Swords Adventures"
    option_definitions = FSAOptions
    data_version = 1
    required_client_version = (0, 6, 1)
    origin_region_name = "Map"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()

    web = FSAWeb()
    # topology_present = True

    options_dataclass = FSAOptions
    options: FSAOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.world_version = "0.1"
        self.event_count = 0

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())
        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: True
        # self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Earth', self.player)

    def generate_early(self):
        self.maidens_required = json.dumps(self.options.maidens_required.value)


    def generate_output(self, output_directory: str) -> None:
        basepatch = pkgutil.get_data(__name__, "fsa.xml")
        base_str = basepatch.decode("utf-8")
        output_patch = apply_patch(self, base_str, output_directory)
        output_file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.xml")
        with open(output_file_path, "w") as file:
            file.write(output_patch)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:  # Todo: make this suck less
        return self.random.choice(filler_item_table)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.event_count):  # Change to fix event count
            item = self.set_classifications(self.get_filler_item_name())
            pool.append(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        return pool
