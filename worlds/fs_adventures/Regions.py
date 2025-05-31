from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
if TYPE_CHECKING:
    from . import FSAdventuresWorld


class FSALocation(Location):
    game: str = "The Legend of Zelda: Four Swords Adventures"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "FSAdventuresWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Map"),
        create_region(world, player, locations_per_region, "Whereabouts of the Wind"),
        create_region(world, player, locations_per_region, "Eastern Hyrule"),
        create_region(world, player, locations_per_region, "Death Mountain"),
        create_region(world, player, locations_per_region, "Near the Fields"),
        create_region(world, player, locations_per_region, "The Dark World"),
        create_region(world, player, locations_per_region, "The Desert of Doubt"),
        create_region(world, player, locations_per_region, "Frozen Hyrule"),
        create_region(world, player, locations_per_region, "Realm of the Heavens"),
        # World 1
        create_region(world, player, locations_per_region, "Lake Hylia"),
        create_region(world, player, locations_per_region, "Cave of No Return"),
        create_region(world, player, locations_per_region, "Hyrule Castle"),
        # World 2
        create_region(world, player, locations_per_region, "The Coast"),
        create_region(world, player, locations_per_region, "Village of the Blue Maiden"),
        create_region(world, player, locations_per_region, "Eastern Temple"),
        # World 3
        create_region(world, player, locations_per_region, "Death Mountain Foothills"),
        create_region(world, player, locations_per_region, "The Mountain Path"),
        create_region(world, player, locations_per_region, "Tower of Flames"),
        # World 4
        create_region(world, player, locations_per_region, "The Field"),
        create_region(world, player, locations_per_region, "The Swamp"),
        create_region(world, player, locations_per_region, "Infiltration of Hyrule Castle"),
        # World 5
        create_region(world, player, locations_per_region, "Lost Woods"),
        create_region(world, player, locations_per_region, "Kakariko Village"),
        create_region(world, player, locations_per_region, "Temple of Darkness"),
        # World 6
        create_region(world, player, locations_per_region, "Desert of Doubt"),
        create_region(world, player, locations_per_region, "Desert Temple"),
        create_region(world, player, locations_per_region, "Pyramid"),
        # World 7
        create_region(world, player, locations_per_region, "Frozen Hyrule (Stage)"),
        create_region(world, player, locations_per_region, "Ice Temple"),
        create_region(world, player, locations_per_region, "Tower of Winds"),
        # World 8
        create_region(world, player, locations_per_region, "Realm of the Heavens (Stage)"),
        create_region(world, player, locations_per_region, "The Dark Cloud"),
        create_region(world, player, locations_per_region, "Palace of Winds"),

    ]
    
    multiworld.regions += regions

    multiworld.get_region("Map", player).add_exits(["Whereabouts of the Wind", "Eastern Hyrule", "Death Mountain",
                                                    "Near the Fields", "The Dark World", "The Desert of Doubt",
                                                    "Frozen Hyrule", "Realm of the Heavens"])

    multiworld.get_region("Whereabouts of the Wind", player).add_exits(["Lake Hylia", "Cave of No Return", "Hyrule Castle"])
    multiworld.get_region("Eastern Hyrule", player).add_exits(["The Coast", "Village of the Blue Maiden", "Eastern Temple"])
    multiworld.get_region("Death Mountain", player).add_exits(["Death Mountain Foothills", "The Mountain Path", "Tower of Flames"])
    multiworld.get_region("Near the Fields", player).add_exits(["The Field", "The Swamp", "Infiltration of Hyrule Castle"])
    multiworld.get_region("The Dark World", player).add_exits(["Lost Woods", "Kakariko Village", "Temple of Darkness"])
    multiworld.get_region("The Desert of Doubt", player).add_exits(["Desert of Doubt", "Desert Temple", "Pyramid"])
    multiworld.get_region("Frozen Hyrule", player).add_exits(["Frozen Hyrule (Stage)", "Ice Temple", "Tower of Winds"])
    multiworld.get_region("Realm of the Heavens", player).add_exits(["Realm of the Heavens (Stage)", "The Dark Cloud", "Palace of Winds"])


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = FSALocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "FSAdventuresWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
    