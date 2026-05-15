import settings
import typing
import threading

from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld

from .Items import item_table, get_item_names_per_category
from .Options import PoROptions, por_option_groups
from .static_location_data import location_ids, get_location_groups
from .generator_main import (CVPoRItem, generate_early, create_regions, fill_slot_data,
                             modify_multidata, generate_output, create_items, get_filler_item_name, set_rules,
                             write_spoiler_header, extend_hint_information)
from .Client import PoRClient

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


class PoRSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania: Portrait of Ruin US ROM file."""
        description = "Portrait of Ruin ROM File"
        copy_to = "CASTLEVANIA2_ACBEA4_00.nds"
        md5 = "2edd57540cae45842fbd19c45a4214f9"

    rom_file: RomFile = RomFile(RomFile.copy_to)


class PoRWorld(World):
    """The year is 1944. Dracula's castle has reappeared, and it's been taken over
       by the mad vampire artist, Brauner, and his two twin daughters. Explore the
       castle and Brauner's magical portraits with two characters and put a stop to him!"""
    game = "Castlevania: Portrait of Ruin"
    option_definitions = PoROptions
    data_version = 1
    origin_region_name = "Entrance - Hub"

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_ids
    item_name_groups = get_item_names_per_category()
    portrait_connections = {}

    web = PoRWeb()
    settings: typing.ClassVar[PoRSettings]
    # topology_present = True
    ut_can_gen_without_yaml = True

    location_name_groups = get_location_groups()
    options_dataclass = PoROptions
    options: PoROptions
    generate_early = generate_early
    create_items = create_items
    create_regions = create_regions
    fill_slot_data = fill_slot_data
    modify_multidata = modify_multidata
    generate_output = generate_output
    get_filler_item_name = get_filler_item_name
    set_rules = set_rules
    write_spoiler_header = write_spoiler_header
    extend_hint_information = extend_hint_information

    # locked_locations: List[str]
    # ocation_cache: List[Location]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

        self.locked_locations = []
        self.location_cache = []
        self.has_tried_magus_ring = False
        self.has_generated_output = False

        self.subweapon_filler_table = [
            "Axe Subweapon",
            "Javelin",
            "Ricochet Rock",
            "Boomerang",
            "Shuriken",
            "Yagyu Shuriken",
            "Kunimitsu",
            "Kunai",
            "Crossbow",
            "Dart",
            "Defensive Form",
            "Wrecking Ball",
            "Rampage",
            "Berserker",
            "Cure Curse",
            "Rock Riot",
            "Spirit of Light",
            "Dark Rift",
            "Stone Circle",
            "Ice Needle",
            "Explosion",
            "Chain Lightning",
            "Nightmare",
            "Summon Medusa",
            "Acidic Bubbles",
            "Hex",
            "Salamander",
            "Thor's Bellow",
            "Summon Crow",
            "Summon Skeleton",
            "Summon Ghost",
            "Summon Gunman",
            "Summon Frog"
        ]

        self.weapon_table = [
            "Leather Whip",
            "Steel Whip",
            "Rose Stem Whip",
            "Blank Book",
            "Knife",
            "Combat Knife",
            "Baselard",
            "Short Sword",
            "Cutlass",
            "Gladius",
            "Rahab's Frost",
            "Agni's Flame",
            "Claymore",
            "Falchion",
            "Great Sword",
            "Zweihander",
            "Spear",
            "Partisan",
            "Lance",
            "Trident",
            "Long Spear",
            "Couse",
            "Axe",
            "Mace",
            "Battle Axe",
            "Morning Star",
            "Bhuj",
            "Brass Knuckles",
            "Cestus"
        ]
        
        self.good_weapon_table = [
            "Medusa Whip",
            "Katar",
            "Cinquedea",
            "Heaven's Sword",
            "Jagdplaute",
            "Damascus Sword",
            "Dragon Slayer",
            "Final Sword",
            "Holy Claymore",
            "Sarissa",
            "Voulge",
            "Bullova",
            "Golden Axe",
            "Illusion Fist"
        ]

        self.armor_table = [
            "Casual Clothes",
            "Hobo's Clothes",
            "Houppelande",
            "Poncho",
            "Combat Fatigues",
            "Adrenaline Gear",
            "Kalasiris",
            "Tailcoat",
            "Biker's Jacket",
            "Justaucorps",
            "Tuxedo Coat",
            "Battle Jacket",
            "Surcoat",
            "Leather Cuirass",
            "Copper Plate",
            "Iron Plate",
            "Silver Plate",
            "Gold Plate",
            "Holy Mail",
            "Mirror Cuirass",
            "Spiked Mail",
            "Leather Corset",
            "Jade Corset",
            "Amethyst Corset",
            "Emerald Corset",
            "Ruby Corset",
            "Sapphire Corset",
            "Lilith Corset",
            "Diamond Corset",
            "Kirtle",
            "Cotton Apron",
            "Silk Negligee",
            "Bathrobe",
            "Frilly Camisole",
            "Sequined Dress",
            "Clown Shirt",
            "Cocktail Dress",
            "Dancer's Blouse",
            "Cotehardie",
            "Eye for Decay",
            "Sunglasses",
            "Thick Glasses",
            "Glasses",
            "Monocle",
            "Goggles",
            "Uraeus",
            "Royal Crown",
            "Head Guard",
            "Iron Helmet",
            "Stone Mask",
            "Viking Helmet",
            "Ballroom Masque",
            "Fedora",
            "Porkpie Hat",
            "Silk Hat",
            "Traveler's Hat",
            "Skull Mask",
            "Witch's Hat",
            "Pearl Tiara",
            "Diamond Tiara",
            "Midnight Tiara",
            "Sandals",
            "Engineer Boots",
            "Royal Sandals",
            "Combat Boots",
            "Slick Boots",
            "Hiking Boots",
            "Oxfords",
            "Wingtips",
            "Iron Leggings",
            "Silver Leggings",
            "Enamel Pinheels",
            "Inuit Boots",
            "Glass Shoes",
            "Diamond Shoes"
        ]

        self.good_armor_table = [
            "Feather Gear",
            "Lorica",
            "Platinum Plate",
            "Samurai Plate",
            "Berserker Mail",
            "Ancient Armor",
            "Scout Armor",
            "Heavy Armor",
            "Impervious Mail",
            "Diamond Corset",
            "Miko Dress",
            "Europa's Dress",
            "Dalmatica",
            "Princess Coat",
            "Wedding Dress",
            "Samurai Helmet",
            "Mourning Veil",
            "Open Veil",
            "Holy Veil",
            "Arachne Hennin",
            "Muse's Tiara",
            "Gold Leggings",
            "Platinum Lggngs",
            "Succubus Boots",
            "Prima Shoes",
            "Silent Sandals"
        ]

        self.accessory_table = [
            "Studded Choker",
            "Astral Ring",
            "Gold Ring",
            "Cape",
            "Blue Cape",
            "Pearl Ring",
            "Tough Ring",
            "Master Ring",
            "Skull Ring",
            "Hercules Ring",
            "Hero's Cape",
            "Elven Cape",
            "Invisible Cape",
            "Holy Mantle",
            "Paludamentum",
            "Blessed Ankh",
            "Orchid Corsage",
            "Rose Corsage",
            "Forget-Me-Not",
            "Platinum Chain",
            "Heart Brooch",
            "Astral Brooch",
            "Abalone Brooch",
            "Moon Brooch"

        ]

    def create_item(self, name: str) -> CVPoRItem:
        from .generator_main import set_classifications
        data = set_classifications(self, name)
        return CVPoRItem(name, data.classification, data.code, self.player)
        
