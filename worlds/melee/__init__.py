import os
import typing
import threading
import pkgutil
import json
import base64
import logger


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
import settings
from .Items import get_item_names_per_category, filler_item_table, item_table
from .Locations import get_locations
from .Regions import init_areas
from .Options import SSBMOptions, ssbm_option_groups
from .Rules import set_location_rules
from .Rom import apply_patch
from .static_location_data import location_ids
from .setup_game import setup_gamevars, place_static_items, calculate_trophy_based_locations
from .in_game_data import global_trophy_table
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths

def run_client(*args):
    print("Running SSBM Client")
    from .Client import launch
    launch_subprocess(launch, name="SSBMClient", args=args)

components.append(
    Component("Super Smash Bros. Melee Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apssbm"))
)


class SSBMWeb(WebWorld):
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

    option_groups = ssbm_option_groups


class SSBMWorld(World):
    """Bottom text"""
    
    game = "Super Smash Bros. Melee"
    option_definitions = SSBMOptions
    data_version = 1
    required_client_version = (0, 6, 1)
    origin_region_name = "Game Base"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()

    web = SSBMWeb()
    # topology_present = True

    options_dataclass = SSBMOptions
    options: SSBMOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.world_version = "0.1"
        self.extra_item_count = 0
        self.goal_count = 1
        self.picked_trophies = set()
        self.all_trophies = global_trophy_table.copy()
        self.all_adventure_trophies = False
        self.all_classic_trophies = False
        self.all_allstar_trophies = False
        self.location_count = 282
        self.required_item_count = 54

    def create_regions(self) -> None:
        for item in self.multiworld.precollected_items[self.player]: #First add starting inventories to the Trophy Pool
            if item.name in global_trophy_table:
                self.picked_trophies.add(item.name)

        calculate_trophy_based_locations(self) #Check if the current Trophy Pool will affect the location pool
        excess_trophies = len(self.picked_trophies) - (self.location_count - self.required_item_count)

        if excess_trophies > 0:
            logger.warning(f"""Warning: {world.multiworld.get_player_name(world.player)}'s generated Trophy Count is higher than the number of locations and required items.
                    Your Trophy counts have automatically been lowered as necessary.""")
        for i in range(excess_trophies):
            self.removed_list = list(self.picked_trophies)
            self.picked_trophies.remove(self.random.choice(self.removed_list))
            if self.options.extra_trophies:
                self.options.extra_trophies.value -= 1
            else:
                self.options.trophies_required.value -= 1


        calculate_trophy_based_locations(self) # If the Trophy Pool was adjusted, recalculate this to remove the locations

        for trophy in self.picked_trophies:
            if trophy not in self.multiworld.precollected_items[self.player]: #Don't create any extra trophies
                self.multiworld.itempool.append(self.create_item(trophy))
            self.extra_item_count += 1

        init_areas(self, get_locations(self))
        place_static_items(self)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())
        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Sense of Accomplishment', self.player, self.goal_count)

    def generate_early(self):
        setup_gamevars(self)
        
        self.authentication_id = self.random.getrandbits(32)
        #self.maidens_required = json.dumps(self.options.maidens_required.value)

    def generate_output(self, output_directory: str) -> None:
        basepatch = pkgutil.get_data(__name__, "melee_base.xml")
        base_str = basepatch.decode("utf-8")
        self.game_name = f"SSBM_{self.player}{self.player_name}{self.authentication_id}".encode("utf-8")
        self.game_name = base64.b64encode(self.game_name).decode("utf-8")
        self.game_name = self.game_name.encode("utf-8")
        
        self.encoded_slot_name = self.player_name.encode("utf-8")
        self.encoded_slot_name = base64.b64encode(self.encoded_slot_name).decode("utf-8")
        output_patch = apply_patch(self, base_str, output_directory)
        output_file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.xml")
        with open(output_file_path, "w") as file:
            file.write(output_patch)



    def fill_slot_data(self) -> Dict[str, typing.Any]:
        return {
            "authentication_id": self.authentication_id
        }

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:  # Todo: make this suck less
        return self.random.choice(filler_item_table)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(self.starting_character)
        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)
        return item

    def generate_filler(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool) - self.extra_item_count):  # Change to fix event count
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
