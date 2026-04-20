from BaseClasses import Region, Location
from typing import List, TYPE_CHECKING, Dict
from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation
from .Locations import LocationData, get_locations
from .Options import StartWithChangeCube
if TYPE_CHECKING:
    from . import PoRWorld


def init_areas(world: "PoRWorld", locations: List[LocationData]) -> None:
    has_change_cube = Has("Change Cube", options=[OptionFilter(StartWithChangeCube, 0)], filtered_resolution=True)

    can_cast_spell = Has("Call Cube") | has_change_cube
    small_uppies = HasAny("Stone of Flight", "Griffon Wing") | HasAll("Call Cube", "Acrobat Cube") | (can_cast_spell & Has("Owl Morph"))
    medium_uppies = HasAny("Stone of Flight", "Griffon Wing") | (can_cast_spell & Has("Owl Morph"))
    big_uppies = Has("Griffon Wing") | (can_cast_spell & Has("Owl Morph"))
    is_smol = Has("Lizard Tail") | (can_cast_spell & Has("Owl Morph")) | (can_cast_spell & Has("Toad Morph"))

    locations_per_region = get_locations_per_region(locations)

    region_list = [
        "Entrance - Wind's Room",  # Used for quests/shops
        "Entrance - Hub",  # The entire starting area up through the hub
        "Entrance - Behemoth Area",  # The area past the first jump check, Behemoth's boss room
        "Entrance - Underground Passage",  # The tunnel leading to the Nest of Evil portrait
        "Entrance - Hub Painting Room",  # The City of Haze portrait
        "Entrance - Upper Area",  # The upper route from the statue room

        "Buried Chamber",  # The ENTIRE buried Chamber, since it all falls under the same logic

        "Great Stairway - Lower",  # Ground level up to Keremet and the check afterwards
        "Great Stairway - Staircases",  # The big stairs rooms and surrounding areas
        "Great Stairway - Entrance Connector",  # The part that connects to the entrance and the wall switch. There's an awkward jump to the upper level that can't be made with acrobat.
        "Great Stairway - Upper",  # The towers to the left of the staircase rooms
        "Great Stairway - Central Painting Area",  # The painting but also the secret room with the nun robes
        "Great Stairway - Underground Painting",  # The sandy graves portrait room
        "Great Stairway - Central Staircases",

        "Tower of Death - Bottom",
        "Tower of Death - Motorcycles",
        "Tower of Death - Belt Area",
        "Tower of Death - Painting Room",
        "Tower of Death - Elevator Room",
        "Tower of Death - First Gear Room",
        "Tower of Death - Ascent",
        "Tower of Death - Second Gear Room",
        "Tower of Death - Top of the Tower",
        
        "Master's Keep - Bridge",
        "Master's Keep - Lower",
        "Master's Keep - Main",
        "Master's Keep - Upper Quarters",
        "Master's Keep - Portrait Room",

        "City of Haze",
        "City of Haze - East",

        "13th Street",
        "13th Street - Main",

        "Sandy Grave",
        "Sandy Grave - Pyramid Top",

        "Forgotten City",
        "Forgotten City - Inner",

        "Nation of Fools",
        "Nation of Fools - Right Lower",
        "Nation of Fools - Main",

        "Forest of Doom",
        "Forest of Doom - Main",
        "Forest of Doom - Cave",

        "Dark Academy",
        "Dark Academy - Right Building",
        "Dark Academy - Main",

        "Burnt Paradise",
        "Burnt Paradise - Bottom",
        "Nest of Evil"

    ]

    if world.options.goal:
        regions.append("Throne Room")

    regions = []

    for area in region_list:
        regions.append(create_region(world, world.player, locations_per_region, area))

    world.multiworld.regions += regions

    world.get_region("Entrance - Hub").add_exits(["Entrance - Wind's Room", "Entrance - Behemoth Area", "Entrance - Hub Painting Room", "Entrance - Upper Area", "Entrance - Underground Passage"],
                                                 {"Entrance - Behemoth Area": small_uppies,
                                                 "Entrance - Hub Painting Room": is_smol,
                                                  "Entrance - Upper Area": HasAll("Acrobat Cube", "Call Cube", "Stone of Flight") | big_uppies,
                                                  "Entrance - Underground Passage": Has("Portrait Clear", world.options.nest_portraits.value)})

    world.get_region("Entrance - Hub Painting Room").add_exits(["Entrance - Hub", world.portrait_connections["City of Haze"]],
                                                              {"Entrance - Hub": is_smol})

    world.get_region("Entrance - Underground Passage").add_exits(["Entrance - Hub", world.portrait_connections["Nest of Evil"]],
                                                                 {"Entrance - Hub": small_uppies})

    world.get_region("Entrance - Upper Area").add_exits(["Entrance - Hub", "Great Stairway - Entrance Connector"])  # Stairway connector

    world.get_region("Entrance - Behemoth Area").add_exits(["Entrance - Hub", "Great Stairway - Lower", "Buried Chamber"],
                                                              {"Great Stairway - Lower": HasAll("Strength Glove", "Push Cube", "Call Cube")})

    world.get_region("Buried Chamber").add_exits(["Entrance - Hub", "Great Stairway - Lower"])

    world.get_region("Great Stairway - Lower").add_exits(["Entrance - Hub", "Great Stairway - Central Staircases", "Buried Chamber"],
                                                          {"Great Stairway - Central Staircases": Has("Stone of Flight") | big_uppies})

    world.get_region("Great Stairway - Staircases").add_exits(["Great Stairway - Lower", "Great Stairway - Underground Painting", "Tower of Death - Bottom", "Great Stairway - Upper"],
                                                          {"Great Stairway - Central Staircases": Has("Stone of Flight") | big_uppies,
                                                           "Tower of Death - Bottom": HasAll("Strength Glove", "Push Cube", "Call Cube"),
                                                           "Great Stairway - Upper": small_uppies | Has("Puppet Master")})

    world.get_region("Great Stairway - Underground Painting").add_exits(["Great Stairway - Staircases", world.portrait_connections["Sandy Grave"]])

    world.get_region("Great Stairway - Entrance Connector").add_exits(["Great Stairway - Staircases", "Entrance - Upper Area", "Great Stairway - Upper"],
                                                          {"Great Stairway - Upper": (HasAll("Call Cube", "Acrobat Cube", "Puppet Master")) | medium_uppies})

    world.get_region("Great Stairway - Upper").add_exits(["Great Stairway - Staircases", "Great Stairway - Entrance Connector", "Tower of Death - Belt Area", "Great Stairway - Central Painting Area"],
                                                          {"Tower of Death - Belt Area": can_cast_spell & HasAny("Owl Morph", "Toad Morph"),
                                                           "Great Stairway - Central Painting Area": small_uppies})

    world.get_region("Great Stairway - Central Painting Area").add_exits([world.portrait_connections["Nation of Fools"], "Great Stairway - Upper"])

    world.get_region("Tower of Death - Bottom").add_exits(["Tower of Death - Ascent", "Tower of Death - First Gear Room", "Tower of Death - Motorcycles"],
                                                          {"Tower of Death - Motorcycles": Has("Cog"),
                                                           "Tower of Death - First Gear Room": small_uppies})

    world.get_region("Tower of Death - Motorcycles").add_exits(["Tower of Death - Bottom", "Tower of Death - Belt Area"],
                                                          {"Tower of Death - Belt Area": HasAll("Wait Cube", "Call Cube") & has_change_cube})

    world.get_region("Tower of Death - Belt Area").add_exits(["Tower of Death - Painting Room", "Great Stairway - Upper", "Master's Keep - Bridge"],
                                                          {"Great Stairway - Upper": can_cast_spell & HasAny("Owl Morph", "Toad Morph")})

    world.get_region("Tower of Death - Painting Room").add_exits(["Tower of Death - Belt Area", world.portrait_connections["Forest of Doom"]])

    world.get_region("Tower of Death - Elevator Room").add_exits(["Master's Keep - Bridge", "Tower of Death - Top of the Tower", "Tower of Death - First Gear Room", "Master's Keep - Lower"],
                                                                  {"Master's Keep - Lower": small_uppies & Has("Tower Elevator Active")})

    world.get_region("Tower of Death - First Gear Room").add_exits(["Tower of Death - Bottom", "Tower of Death - Ascent"],
                                                                   {"Tower of Death - Ascent": can_cast_spell & HasAny("Owl Morph", "Toad Morph")})


    world.get_region("Tower of Death - Ascent").add_exits(["Tower of Death - First Gear Room", "Tower of Death - Second Gear Room"],
                                                          {"Tower of Death - First Gear Room": can_cast_spell & HasAny("Owl Morph", "Toad Morph"),
                                                           "Tower of Death - Second Gear Room": medium_uppies})

    world.get_region("Tower of Death - Second Gear Room").add_exits(["Tower of Death - Ascent", "Tower of Death - Top of the Tower"])

    world.get_region("Tower of Death - Top of the Tower").add_exits(["Tower of Death - Second Gear Room", "Tower of Death - Elevator Room"])


    world.get_region("Master's Keep - Bridge").add_exits(["Tower of Death - Belt Area", "Tower of Death - Elevator Room"])

    world.get_region("Master's Keep - Lower").add_exits(["Tower of Death - Elevator Room", "Master's Keep - Bridge", "Master's Keep - Main"],
                                                         {"Tower of Death - Elevator Room": Has("Tower Elevator Active"),
                                                          "Master's Keep - Main": medium_uppies | (small_uppies & Has("Puppet Master"))})

    world.get_region("Master's Keep - Main").add_exits(["Master's Keep - Lower", "Master's Keep - Upper Quarters"],
                                                         {"Master's Keep - Upper Quarters": medium_uppies | (small_uppies & Has("Puppet Master"))})

    world.get_region("Master's Keep - Upper Quarters").add_exits(["Master's Keep - Portrait Room", "Master's Keep - Main"],
                                                         {"Master's Keep - Portrait Room": can_cast_spell & Has("Sanctuary")})

    world.get_region("Master's Keep - Portrait Room").add_exits([world.portrait_connections["Forgotten City"], world.portrait_connections["Burnt Paradise"], world.portrait_connections["Dark Academy"], world.portrait_connections["13th Street"]],
                                                         {world.portrait_connections["13th Street"]: CanReachLocation("Forgotten City - Boss Room"),
                                                         world.portrait_connections["Burnt Paradise"]: CanReachLocation("13th Street - Boss Room")})
                                                         
    world.get_region("City of Haze").add_exits(["City of Haze - East"],
                                                         {"City of Haze - East": Has("Puppet Master") | (has_change_cube & Has("Call Cube"))})

    world.get_region("Sandy Grave").add_exits(["Sandy Grave - Upper Pyramid"],
                                                         {"Sandy Grave - Upper Pyramid": small_uppies})

    world.get_region("Nation of Fools").add_exits(["Nation of Fools - Right Lower", "Nation of Fools - Main"],
                                                         {"Nation of Fools - Right Lower": small_uppies | Has("Puppet Master"),
                                                          "Nation of Fools - Main": medium_uppies})

    world.get_region("Sandy Grave - Upper Pyramid").add_exits(["Sandy Grave - Pyramid Top"],
                                                         {"Sandy Grave - Pyramid Top": medium_uppies})

    world.get_region("Forest of Doom").add_exits(["Forest of Doom - Main"],
                                                         {"Forest of Doom - Main": small_uppies})

    world.get_region("Forest of Doom - Main").add_exits(["Forest of Doom - Cave"],
                                                         {"Forest of Doom - Cave": HasAll("Strength Glove", "Push Cube", "Call Cube")})

    world.get_region("Dark Academy").add_exits(["Dark Academy - Right Building"],
                                                         {"Dark Academy - Right Building": small_uppies | Has("Puppet Master")})

    world.get_region("Dark Academy - Right Building").add_exits(["Dark Academy - Main"],
                                                         {"Dark Academy - Main": big_uppies})

    world.get_region("Forgotten City").add_exits(["Forgotten City - Inner"],
                                                         {"Forgotten City - Inner": medium_uppies | Has("Puppet Master")})

    world.get_region("13th Street").add_exits(["13th Street - Main"],
                                                         {"13th Street - Main": HasAll("Strength Glove", "Push Cube", "Call Cube")})

    world.get_region("Burnt Paradise").add_exits(["Burnt Paradise - Entrance"],
                                                         {"Burnt Paradise - Entrance": small_uppies | Has("Puppet Master")})

    world.get_region("Burnt Paradise - Entrance").add_exits(["Burnt Paradise - Bottom"],
                                                         {"Burnt Paradise - Bottom": big_uppies})

    if world.options.goal:
        # Add a connection to the throne room if necessary
        world.get_region("Master's Keep - Upper Quarters").connect(world.get_region("Throne Room"), "Throne Barrier", Has("Brauner Defeated"))

def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = PoRLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location

def create_region(world: "PoRWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
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