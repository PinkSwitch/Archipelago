import os
import typing
import threading
import pkgutil


from typing import List, Set, Dict, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from Options import OptionGroup
import settings
from .Items import get_item_names_per_category, item_table
from .Locations import get_locations
from .Regions import init_areas
from .Options import EBOptions, eb_option_groups, StartingCharacter
from .setup_game import setup_gamevars, place_static_items
from .modules.enemy_data import initialize_enemies
from .modules.flavor_data import create_flavors
from .game_data.local_data import item_id_table, world_version
from .modules.hint_data import setup_hints
from .game_data.text_data import spoiler_psi, spoiler_starts, spoiler_badges
from .Client import EarthBoundClient
from .Rules import set_location_rules
from .Rom import patch_rom, get_base_rom_path, EBProcPatch, valid_hashes
from .game_data.static_location_data import location_ids, location_groups
from .modules.equipamizer import EBArmor, EBWeapon
from worlds.generic.Rules import add_item_rule, forbid_items_for_player
from Options import OptionError


class EBSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the EarthBound US ROM"""
        description = "EarthBound ROM File"
        copy_to = "EarthBound.sfc"
        md5s = valid_hashes

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

    option_groups = eb_option_groups


class EarthBoundWorld(World):
    """EarthBound is a contemporary-themed JRPG. Take four psychically-endowed children
       across the world in search of 8 Melodies to defeat Giygas, the cosmic evil."""
    
    game = "EarthBound"
    option_definitions = EBOptions
    data_version = 1
    required_client_version = (0, 5, 0)

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    location_name_groups = location_groups

    web = EBWeb()
    settings: typing.ClassVar[EBSettings]
    # topology_present = True

    options_dataclass = EBOptions
    options: EBOptions

    locked_locations: List[str]
    location_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.event_count = 8
        self.world_version = world_version
        self.removed_teleports = []
        self.armor_list: Dict[str, EBArmor]
        self.weapon_list: Dict[str, EBWeapon]

    def generate_early(self):  # Todo: place locked items in generate_early
        self.starting_character = self.options.starting_character.current_key.capitalize()
        self.locals = []
        local_space_count = 0
        max_counts = {
            "Ness": 12,
            "Paula": 11,
            "Jeff": 9,
            "Poo": 99
        }
        max_count = max_counts[self.starting_character]
        for item_name, amount in self.options.start_inventory.items():
            if item_name in item_id_table:
                local_space_count += amount
                if local_space_count > max_count and not self.options.remote_items:
                    player = self.multiworld.get_player_name(self.player)
                    raise OptionError(f"{player}: starting inventory cannot place more than {max_count} items into 'Goods' for {self.starting_character}. Attempted to place {local_space_count} Goods items.")

        for item_name, amount in self.options.start_inventory_from_pool.items():
            if item_name in item_id_table:
                local_space_count += amount
                if local_space_count > max_count and not self.options.remote_items:
                    player = self.multiworld.get_player_name(self.player)
                    raise OptionError(f"{player}: starting inventory cannot place more than {max_count} items into 'Goods' for {self.starting_character}. Attempted to place {local_space_count} Goods items.")
        setup_gamevars(self)
        create_flavors(self)
        initialize_enemies(self)
        if self.options.shuffle_teleports == 0:
            self.options.local_items.value |= self.item_name_groups["PSI"]
            self.event_count += 12
            if self.options.magicant_mode != 0:
                self.event_count -= 1

        if self.options.character_shuffle == 0:
            self.options.local_items.value.update(["Paula", "Jeff", "Poo", "Flying Man"])
            self.event_count += 6

    def create_regions(self) -> None:
        init_areas(self, get_locations(self))
        place_static_items(self)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())
        self.generate_filler(pool)

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_location_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Saved Earth', self.player)

    def pre_fill(self) -> None:
        prefill_locations = []
        prefill_items = []
        
        if self.options.magicant_mode == 3:
            removable_teleports = 6
        else:
            removable_teleports = 5

        if self.options.shuffle_teleports == 0:
            prefill_locations.extend([
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
                self.multiworld.get_location("Dalaam - Trial of Mu", self.player)
            ])

            if self.options.magicant_mode == 0:
                prefill_locations.append(self.multiworld.get_location("Magicant - Ness's Nightmare", self.player))

            prefill_items.extend([
                self.create_item("Onett Teleport"),
                self.create_item("Twoson Teleport"),
                self.create_item("Happy-Happy Village Teleport"),
                self.create_item("Threed Teleport"),
                self.create_item("Saturn Valley Teleport"),
                self.create_item("Dusty Dunes Teleport"),
                self.create_item("Fourside Teleport"),
                self.create_item("Winters Teleport"),
                self.create_item("Scaraba Teleport"),
                self.create_item("Deep Darkness Teleport"),
                self.create_item("Tenda Village Teleport"),
                self.create_item("Lost Underworld Teleport")

            ])
            self.random.shuffle(prefill_items)
            self.removed_teleports.extend(prefill_items[0:removable_teleports])
            del prefill_items[0:removable_teleports]
            prefill_items.extend([
                self.create_item("Dalaam Teleport"),
                self.create_item("Summers Teleport"),
                self.create_item("Progressive Poo PSI"),
                self.create_item("Progressive Poo PSI")
            ])

            if self.options.magicant_mode in [0, 3]:
                prefill_items.append(self.create_item("Magicant Teleport"))
            self.random.shuffle(prefill_items)
            add_item_rule(self.multiworld.get_location("Onett - Buzz Buzz", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Onett - Mani Mani Statue", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Saturn Valley - Saturn Coffee", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Monkey Caves - Monkey Power", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Summers - Magic Cake", self.player), lambda item: item.name in self.item_name_groups["PSI"] and item.name != "Summers Teleport")
            add_item_rule(self.multiworld.get_location("Scaraba - Star Master", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Tenda Village - Tenda Tea", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Lost Underworld - Talking Rock", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Fourside - Department Store Blackout", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Cave of the Present - Star Master", self.player), lambda item: item.name in self.item_name_groups["PSI"])
            add_item_rule(self.multiworld.get_location("Dalaam - Trial of Mu", self.player), lambda item: (item.name in self.item_name_groups["PSI"] and item.name != "Dalaam Teleport"))
            
            if self.options.magicant_mode == 0:
                add_item_rule(self.multiworld.get_location("Magicant - Ness's Nightmare", self.player), lambda item: (item.name in self.item_name_groups["PSI"] and item.name != "Magicant Teleport"))

        if self.options.character_shuffle == 0:
            main_characters = ["Ness", "Paula", "Jeff", "Poo"]
            for character in main_characters:
                if character != self.starting_character:
                    prefill_items.append(self.create_item(character))

            prefill_items.extend([
                self.create_item("Flying Man"),
                self.create_item("Teddy Bear"),
                self.create_item("Super Plush Bear")
            ])

            prefill_locations.extend([
                self.multiworld.get_location("Happy-Happy Village - Prisoner", self.player),
                self.multiworld.get_location("Threed - Zombie Prisoner", self.player),
                self.multiworld.get_location("Snow Wood - Bedroom", self.player),
                self.multiworld.get_location("Monotoli Building - Monotoli Character", self.player),
                self.multiworld.get_location("Dalaam - Throne Character", self.player),
                self.multiworld.get_location("Deep Darkness - Barf Character", self.player),
            ])
            self.random.shuffle(prefill_locations)
            add_item_rule(self.multiworld.get_location("Happy-Happy Village - Prisoner", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Threed - Zombie Prisoner", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Snow Wood - Bedroom", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Monotoli Building - Monotoli Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Dalaam - Throne Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])
            add_item_rule(self.multiworld.get_location("Deep Darkness - Barf Character", self.player), lambda item: item.name in self.item_name_groups["Characters"])

            if (self.start_location == 9 and self.starting_teleport == "Winters Teleport") or (self.start_location == 7 and self.starting_teleport == "Dalaam Teleport"):
                if self.starting_character != "Poo":
                    forced_poo = self.random.choice(["Dalaam - Throne Character", "Snow Wood - Bedroom"])
                    add_item_rule(self.multiworld.get_location(forced_poo, self.player), lambda item: item.name == "Poo")
                forbid_items_for_player(self.multiworld.get_location("Dalaam - Trial of Mu", self.player), {"Winters Teleport"}, self.player)
                forbid_items_for_player(self.multiworld.get_location("Dalaam - Trial of Mu", self.player), {"Progressive Poo PSI"}, self.player)

        fill_restrictive(self.multiworld, self.multiworld.get_all_state(False), prefill_locations, prefill_items, True, True)
        setup_hints(self)

    def generate_output(self, output_directory: str):
        try:
            patch = EBProcPatch()
            patch.write_file("earthbound_basepatch.bsdiff4", pkgutil.get_data(__name__, "earthbound_basepatch.bsdiff4"))
            patch_rom(self, patch, self.player)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def fill_slot_data(self) -> Dict[str, List[int]]:
        return {
            "starting_area": self.start_location,
            "pizza_logic": self.options.monkey_caves_mode.value,
            "free_sancs": self.options.no_free_sanctuaries.value,
            "shopsanity": self.options.shop_randomizer.value
        }

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nStarting Location:    {spoiler_starts[self.start_location]}\n")
        spoiler_handle.write(f"Franklin Badge Protection:    {spoiler_badges[self.franklin_protection]}\n")
        if self.options.psi_shuffle:
            spoiler_handle.write("\nPSI Shuffle:\n")
            spoiler_handle.write(f"Favorite Thing PSI Slot:    {spoiler_psi[self.offensive_psi_slots[0]]}\n")
            spoiler_handle.write(f"Ness Offensive PSI Middle Slot:    {spoiler_psi[self.offensive_psi_slots[1]]}\n")
            spoiler_handle.write(f"Paula Offensive PSI Top Slot:    {spoiler_psi[self.offensive_psi_slots[2]]}\n")
            spoiler_handle.write(f"Paula/Poo Offensive PSI Middle Slot:    {spoiler_psi[self.offensive_psi_slots[3]]}\n")
            spoiler_handle.write(f"Paula/Poo Offensive PSI Bottom Slot:    {spoiler_psi[self.offensive_psi_slots[4]]}\n")
            spoiler_handle.write(f"Poo Progressive PSI Slot:    {spoiler_psi[self.offensive_psi_slots[5]]}\n")

            spoiler_handle.write(f"Ness/Poo Shield Slot:    {spoiler_psi[self.shield_slots[0]]}\n")
            spoiler_handle.write(f"Paula Shield Slot:    {spoiler_psi[self.shield_slots[1]]}\n")

            spoiler_handle.write(f"Ness Assist PSI Middle Slot:    {spoiler_psi[self.assist_psi_slots[0]]}\n")
            spoiler_handle.write(f"Ness Assist PSI Bottom Slot:    {spoiler_psi[self.assist_psi_slots[1]]}\n")
            spoiler_handle.write(f"Paula Assist PSI Middle Slot:    {spoiler_psi[self.assist_psi_slots[2]]}\n")
            spoiler_handle.write(f"Paula Assist PSI Bottom Slot:    {spoiler_psi[self.assist_psi_slots[3]]}\n")
            spoiler_handle.write(f"Poo Assist PSI Slot:    {spoiler_psi[self.assist_psi_slots[4]]}\n")
        if self.options.psi_shuffle == 2:
            spoiler_handle.write(f"Bomb/Bazooka Slot:    {spoiler_psi[self.jeff_offense_items[0]]}\n")
            spoiler_handle.write(f"Bottle Rocket Slot:    {spoiler_psi[self.jeff_offense_items[1]]}\n")

            spoiler_handle.write(f"Spray Can Slot:    {spoiler_psi[self.jeff_assist_items[0]]}\n")
            spoiler_handle.write(f"Multi-Level Gadget Slot 1:    {spoiler_psi[self.jeff_assist_items[1]]}\n")
            spoiler_handle.write(f"Single-Level Gadget Slot 1:    {spoiler_psi[self.jeff_assist_items[2]]}\n")
            spoiler_handle.write(f"Single-Level Gadget Slot 2:    {spoiler_psi[self.jeff_assist_items[3]]}\n")
            spoiler_handle.write(f"Multi-Level Gadget Slot 2:    {spoiler_psi[self.jeff_assist_items[4]]}\n")

        if self.options.boss_shuffle:
            spoiler_handle.write("\nBoss Randomization:\n" + 
                                 f" Frank => {self.boss_list[0]}\n" +
                                 f" Frankystein Mark II => {self.boss_list[1]}\n" +
                                 f" Titanic Ant => {self.boss_list[2]}\n" +
                                 f" Captain Strong => {self.boss_list[3]}\n" +
                                 f" Everdred => {self.boss_list[4]}\n" +
                                 f" Mr. Carpainter => {self.boss_list[5]}\n" +
                                 f" Mondo Mole => {self.boss_list[6]}\n" +
                                 f" Boogey Tent => {self.boss_list[7]}\n" +
                                 f" Mini Barf => {self.boss_list[8]}\n" +
                                 f" Master Belch => {self.boss_list[9]}\n" +
                                 f" Trillionage Sprout => {self.boss_list[10]}\n" +
                                 f" Guardian Digger => {self.boss_list[11]}\n" +
                                 f" Dept. Store Spook => {self.boss_list[12]}\n" +
                                 f" Evil Mani-Mani => {self.boss_list[13]}\n" +
                                 f" Clumsy Robot => {self.boss_list[14]}\n" +
                                 f" Shrooom! => {self.boss_list[15]}\n" +
                                 f" Plague Rat of Doom => {self.boss_list[16]}\n" +
                                 f" Thunder and Storm => {self.boss_list[17]}\n" +
                                 f" Kraken => {self.boss_list[18]}\n" +
                                 f" Guardian General => {self.boss_list[19]}\n" +
                                 f" Master Barf => {self.boss_list[20]}\n" +
                                 f" Starman Deluxe => {self.boss_list[21]}\n" +
                                 f" Electro Specter => {self.boss_list[22]}\n" +
                                 f" Carbon Dog => {self.boss_list[23]}\n" +
                                 f" Ness's Nightmare => {self.boss_list[24]}\n" +
                                 f" Heavily Armed Pokey => {self.boss_list[25]}\n" +
                                 f" Starman Junior => {self.boss_list[26]}\n" +
                                 f" Diamond Dog => {self.boss_list[27]}\n" +
                                 f" Giygas (Phase 2) => {self.boss_list[28]}\n")

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:  # Todo: make this suck less
        weights = {"rare": self.options.rare_filler_weight.value, "uncommon": self.options.uncommon_filler_weight.value, "common": self.options.common_filler_weight.value,
                   "rare_gear": int(self.options.rare_filler_weight.value * 0.5), "uncommon_gear": int(self.options.uncommon_filler_weight.value * 0.5),
                   "common_gear": int(self.options.common_filler_weight.value * 0.5)}
        choices = self.random.choices(list(weights), weights=list(weights.values()), k=len(self.multiworld.get_unfilled_locations(self.player)))
        filler_type = self.random.choice(choices)
        weight_table = {
            "common": self.common_items,
            "common_gear": self.common_gear,
            "uncommon": self.uncommon_items,
            "uncommon_gear": self.uncommon_gear,
            "rare": self.rare_items,
            "rare_gear": self.rare_gear
        }
        return self.random.choice(weight_table[filler_type])

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add(self.starting_character)

        if self.options.shuffle_teleports == 0:
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
        elif self.options.magicant_mode not in [0, 3]:
            excluded_items.add("Magicant Teleport")

        if self.options.character_shuffle == 0:
            excluded_items.add("Ness")
            excluded_items.add("Paula")
            excluded_items.add("Jeff")
            excluded_items.add("Poo")
            excluded_items.add("Flying Man")

        if self.options.progressive_weapons:
            excluded_items.add("Magicant Bat")
            excluded_items.add("Legendary Bat")
            excluded_items.add("Pop Gun")
            excluded_items.add("Stun Gun")
            excluded_items.add("Death Ray")
            excluded_items.add("Moon Beam Gun")

        if self.options.progressive_armor:
            excluded_items.add("Platinum Band")
            excluded_items.add("Diamond Band")
            excluded_items.add("Pixie's Bracelet")
            excluded_items.add("Cherub's Band")
            excluded_items.add("Goddess Band")
            excluded_items.add("Coin of Slumber")
            excluded_items.add("Souvenir Coin")
            excluded_items.add("Mr. Saturn Coin")

        if not self.options.no_free_sanctuaries:
            excluded_items.add("Tiny Key")
            excluded_items.add("Tenda Lavapants")

        return excluded_items

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        if name == "Magicant Teleport" and self.options.magicant_mode == 3:
            item.classification = ItemClassification.useful
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
        
        if self.options.progressive_weapons:
            for i in range(2):
                pool.append(self.set_classifications("Progressive Bat"))
            for i in range(4):
                pool.append(self.set_classifications("Progressive Gun"))

        if self.options.progressive_armor:
            for i in range(5):
                pool.append(self.set_classifications("Progressive Bracelet"))
            for i in range(3):
                pool.append(self.set_classifications("Progressive Other"))

        return pool
