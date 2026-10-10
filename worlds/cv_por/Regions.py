from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation
from rule_builder.field_resolvers import FromOption
from .Locations import get_locations
from .Options import (NestofEvil, DraculaPortraits, BraunerRequired, StrongerGlove, NestPortraits,
                      AddBossKeys, ExcludedBossKeys, EarlyOpenCastle)

if TYPE_CHECKING:
    from . import PoRWorld


class PoRLocation(Location):
    game: str = "Castlevania: Portrait of Ruin"


region_list = [
    "Entrance - Wind's Room",  # Used for quests/shops
    "Entrance - Hub",  # The entire starting area up through the hub
    "Entrance - Behemoth Area",  # The area past the first jump check, Behemoth's boss room
    "Entrance - Post Behemoth",  # The area right of behemoth, for boss keys
    "Entrance - Underground Passage",  # The tunnel leading to the Nest of Evil portrait
    "Entrance - Hub Painting Room",  # The City of Haze portrait
    "Entrance - Upper Area",  # The upper route from the statue room
    "Entrance - Iron Block Door",  # Region for the iron pusblock door

    "Buried Chamber",  # The ENTIRE buried Chamber, since it all falls under the same logic

    "Great Stairway - Lower",  # Ground level up to Keremet and the check afterwards
    "Great Stairway - Staircases",  # The big stairs rooms and surrounding areas
    "Great Stairway - Post Keremet",  # The item after Keremt, for boss keys
    "Great Stairway - Entrance Connector",  # The part that connects to the entrance and the wall switch. There's an awkward jump to the upper level that can't be made with acrobat.
    "Great Stairway - Upper",  # The towers to the left of the staircase rooms
    "Great Stairway - Central Painting Area",  # The painting but also the secret room with the nun robes
    "Great Stairway - Underground Painting",  # The sandy graves portrait room
    "Great Stairway - Pipe Door",
    "Great Stairway - Push Block Door",
    "Great Stairway - Underground",

    "Tower of Death - Bottom",
    "Tower of Death - Motorcycles",
    "Tower of Death - Belt Area",
    "Tower of Death - Painting Room",
    "Tower of Death - Elevator Room",
    "Tower of Death - First Gear Room",
    "Tower of Death - Ascent",
    "Tower of Death - Second Gear Room",
    "Tower of Death - Top of the Tower",
    "Tower of Death - Elevator Exit",
    
    "Master's Keep - Bridge",
    "Master's Keep - Lower",
    "Master's Keep - Main",
    "Master's Keep - Upper Quarters",
    "Master's Keep - Portrait Room",

    "The Throne Room",

    "City of Haze",
    "City of Haze - East",
    "City of Haze - Post-Boss",

    "13th Street",
    "13th Street - Main",

    "Sandy Grave",
    "Sandy Grave - Upper Pyramid",
    "Sandy Grave - Pyramid Top",

    "Forgotten City",
    "Forgotten City - Inner",
    "Forgotten City - Inner Upper",

    "Nation of Fools",
    "Nation of Fools - Right Lower",
    "Nation of Fools - Right Lower Medium Room",
    "Nation of Fools - Main",

    "Forest of Doom",
    "Forest of Doom - Main",
    "Forest of Doom - Cave",

    "Dark Academy",
    "Dark Academy - Right Building",
    "Dark Academy - Main",

    "Burnt Paradise",
    "Burnt Paradise - Entrance",
    "Nest of Evil"
]

strongies = Has("Strength Glove") & (HasAll("Push Cube", "Call Cube") | OptionFilter(StrongerGlove, 1))

can_cast_spell = HasAny("Change Cube", "Skill Cube")
small_uppies = HasAny("Stone of Flight", "Griffon Wing") | (HasAll("Acrobat Cube", "Call Cube")) | (can_cast_spell & Has("Owl Morph"))
medium_uppies = HasAny("Stone of Flight", "Griffon Wing") | (can_cast_spell & Has("Owl Morph"))
big_uppies = Has("Griffon Wing") | (can_cast_spell & Has("Owl Morph"))
is_smol = Has("Lizard Tail") | (can_cast_spell & Has("Owl Morph")) | (can_cast_spell & Has("Toad Morph"))


def init_areas(world: "PoRWorld") -> None:
    regions = []
    active_regions = region_list.copy()

    if not (world.options.goal or world.options.open_throne):
        active_regions.remove("The Throne Room")

    for area in active_regions:
        regions.append(Region(area, world.player, world.multiworld))

    world.multiworld.regions += regions
    create_locations(world)
    connect_regions(world)


def create_locations(world):
    from .static_location_data import location_ids
    all_locations = get_locations(world)

    for location in all_locations:
        if location.region not in region_list:
            raise ValueError(f"Error: Region {location.region} is invalid for location {location.name}.")
        region = world.get_region(location.region)
        region.locations.append(PoRLocation(world.player, location.name, None if location.is_event else location_ids[location.name], region))


def connect_regions(world):
    world.get_region("Entrance - Hub").add_exits(["Entrance - Wind's Room", "Entrance - Behemoth Area", "Entrance - Hub Painting Room", "Entrance - Upper Area", "Entrance - Underground Passage"],
                                                 {"Entrance - Behemoth Area": small_uppies | OptionFilter(EarlyOpenCastle, 1),
                                                 "Entrance - Hub Painting Room": is_smol | Has("Puppet Master"),
                                                  "Entrance - Upper Area": HasAll("Acrobat Cube", "Stone of Flight", "Call Cube") | big_uppies,
                                                  "Entrance - Underground Passage": Has("Portrait Clear", FromOption(NestPortraits))})

    world.get_region("Entrance - Hub Painting Room").add_exits(["Entrance - Hub", world.portrait_connections["City of Haze"]],
                                                               {"Entrance - Hub": is_smol})

    world.get_region("Entrance - Underground Passage").add_exits(["Entrance - Hub", world.portrait_connections["Nest of Evil"]],
                                                                 {"Entrance - Hub": small_uppies})

    world.get_region("Entrance - Upper Area").add_exits({"Entrance - Hub": None, "Great Stairway - Entrance Connector": "Sec01Rm14"})  # Stairway connector

    world.get_region("Entrance - Behemoth Area").add_exits(["Entrance - Hub", "Entrance - Post Behemoth"],
                                                           {"Entrance - Post Behemoth": (Has("Colosseum Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Colosseum Key", "contains"))})

    world.get_region("Entrance - Post Behemoth").add_exits({"Entrance - Behemoth Area": None, "Entrance - Iron Block Door": None, "Buried Chamber": "Sec00Rm0A"},
                                                           {"Entrance - Iron Block Door": strongies,
                                                            "Entrance - Behemoth Area": (Has("Colosseum Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Colosseum Key", "contains"))})

    world.get_region("Entrance - Iron Block Door").add_exits({"Entrance - Post Behemoth": None, "Great Stairway - Lower": "Sec00Rm0B"},
                                                             {"Entrance - Post Behemoth": strongies})

    world.get_region("Buried Chamber").add_exits({"Entrance - Post Behemoth": "Sec02Rm03", "Great Stairway - Lower": "Sec02Rm1C"})

    world.get_region("Great Stairway - Lower").add_exits({"Entrance - Iron Block Door": "Sec03Rm00", "Great Stairway - Staircases": None, "Buried Chamber": "Sec03Rm06", "Great Stairway - Post Keremet": None},
                                                         {"Great Stairway - Staircases": Has("Stone of Flight") | big_uppies,
                                                          "Great Stairway - Post Keremet": (Has("Cavern Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Cavern Key", "contains"))})

    world.get_region("Great Stairway - Post Keremet").add_exits(["Great Stairway - Lower", "Great Stairway - Staircases"],
                                                                {"Great Stairway - Lower": (Has("Cavern Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Cavern Key", "contains")),
                                                                 "Great Stairway - Staircases": (Has("Stone of Flight") | big_uppies) | (OptionFilter(EarlyOpenCastle, 1) & small_uppies)})

    world.get_region("Great Stairway - Staircases").add_exits(["Great Stairway - Lower", "Great Stairway - Underground", "Great Stairway - Push Block Door", "Great Stairway - Upper"],
                                                              {"Great Stairway - Push Block Door": strongies,
                                                               "Great Stairway - Upper": small_uppies | Has("Puppet Master")})

    world.get_region("Great Stairway - Underground").add_exits(["Great Stairway - Staircases", "Great Stairway - Underground Painting", "Great Stairway - Post Keremet"],
                                                               {"Great Stairway - Staircases": OptionFilter(EarlyOpenCastle, 0) | HasAny("Stone of Flight", "Uppet Master") | small_uppies})

    world.get_region("Great Stairway - Push Block Door").connect(world.get_region("Tower of Death - Bottom"), "Sec03Rm0C")

    world.get_region("Great Stairway - Underground Painting").add_exits(["Great Stairway - Staircases", world.portrait_connections["Sandy Grave"]])

    world.get_region("Great Stairway - Entrance Connector").add_exits({"Great Stairway - Staircases": None, "Entrance - Upper Area": "Sec06Rm00", "Great Stairway - Upper": None},
                                                                      {"Great Stairway - Upper": HasAll("Acrobat Cube", "Puppet Master", "Call Cube") | medium_uppies | HasAll("Acrobat Cube", "Speed Up", "Call Cube")})

    world.get_region("Great Stairway - Upper").add_exits(["Great Stairway - Staircases", "Great Stairway - Entrance Connector", "Great Stairway - Pipe Door", "Great Stairway - Central Painting Area"],
                                                         {"Great Stairway - Pipe Door": can_cast_spell & HasAny("Owl Morph", "Toad Morph"),
                                                          "Great Stairway - Central Painting Area": small_uppies})

    world.get_region("Great Stairway - Pipe Door").add_exits({"Great Stairway - Upper": None, "Tower of Death - Belt Area": "Sec06Rm0C"},
                                                             {"Great Stairway - Upper": can_cast_spell & HasAny("Owl Morph", "Toad Morph")})

    world.get_region("Great Stairway - Central Painting Area").add_exits([world.portrait_connections["Nation of Fools"], "Great Stairway - Upper"])

    world.get_region("Tower of Death - Bottom").add_exits({"Tower of Death - First Gear Room": None, "Tower of Death - Motorcycles": None, "Great Stairway - Push Block Door": "Sec07Rm17"},
                                                          {"Tower of Death - Motorcycles": Has("Cog") & (Has("Tower Base Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Tower Base Key", "contains")),
                                                           "Tower of Death - First Gear Room": small_uppies})

    world.get_region("Tower of Death - Motorcycles").add_exits(["Tower of Death - Bottom", "Tower of Death - Belt Area"],
                                                               {"Tower of Death - Belt Area": HasAll("Wait Cube", "Call Cube", "Change Cube")})

    world.get_region("Tower of Death - Belt Area").add_exits({"Tower of Death - Painting Room": None, "Great Stairway - Pipe Door": "Sec08Rm0A", "Master's Keep - Bridge": "Sec08Rm07"})

    world.get_region("Tower of Death - Painting Room").add_exits(["Tower of Death - Belt Area", world.portrait_connections["Forest of Doom"]], {
                                                                  world.portrait_connections["Forest of Doom"]: Has("Stella's Locket")
    })

    world.get_region("Tower of Death - Elevator Room").add_exits({"Master's Keep - Bridge": "Sec07Rm1B", "Tower of Death - Top of the Tower": None, "Tower of Death - First Gear Room": None, "Tower of Death - Elevator Exit": None},
                                                                 {"Tower of Death - Elevator Exit": small_uppies & Has("Tower Elevator Active"),
                                                                  "Tower of Death - Top of the Tower": big_uppies})

    world.get_region("Tower of Death - Elevator Exit").add_exits({"Master's Keep - Lower": "Sec07Rm19", "Tower of Death - Elevator Room": None},
                                                                 {"Tower of Death - Elevator Room": Has("Tower Elevator Active")})

    world.get_region("Tower of Death - First Gear Room").add_exits(["Tower of Death - Bottom", "Tower of Death - Ascent"],
                                                                   {"Tower of Death - Ascent": can_cast_spell & HasAny("Owl Morph", "Toad Morph")})

    world.get_region("Tower of Death - Ascent").add_exits(["Tower of Death - First Gear Room", "Tower of Death - Second Gear Room"],
                                                          {"Tower of Death - First Gear Room": can_cast_spell & HasAny("Owl Morph", "Toad Morph"),
                                                           "Tower of Death - Second Gear Room": medium_uppies})

    world.get_region("Tower of Death - Second Gear Room").add_exits(["Tower of Death - Ascent", "Tower of Death - Top of the Tower"],
                                                                    {"Tower of Death - Top of the Tower": (Has("Clock Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Clock Key", "contains"))})

    world.get_region("Tower of Death - Top of the Tower").add_exits(["Tower of Death - Second Gear Room", "Tower of Death - Elevator Room"],
                                                                    {"Tower of Death - Second Gear Room": (Has("Clock Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Clock Key", "contains"))})


    world.get_region("Master's Keep - Bridge").add_exits({"Tower of Death - Belt Area": "Sec0BRm03", "Tower of Death - Elevator Room": "Sec0BRm05"})

    world.get_region("Master's Keep - Lower").add_exits({"Tower of Death - Elevator Exit": "Sec0ARm13", "Master's Keep - Bridge": None, "Master's Keep - Main": None},
                                                        {"Master's Keep - Main": medium_uppies | (small_uppies & Has("Puppet Master"))})

    world.get_region("Master's Keep - Main").add_exits(["Master's Keep - Lower", "Master's Keep - Upper Quarters"],
                                                       {"Master's Keep - Upper Quarters": medium_uppies | (small_uppies & Has("Puppet Master"))})

    world.get_region("Master's Keep - Upper Quarters").add_exits(["Master's Keep - Portrait Room", "Master's Keep - Main"],
                                                                 {"Master's Keep - Portrait Room": (Has("Sanctuary") & (Has("Skill Cube") | HasAll("Call Cube", "Change Cube"))) & (
                                                                         Has("Gallery Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "Gallery Key", "contains")
                                                                 )})

    world.get_region("Master's Keep - Portrait Room").add_exits([world.portrait_connections["Forgotten City"], world.portrait_connections["Burnt Paradise"], world.portrait_connections["Dark Academy"], world.portrait_connections["13th Street"]],
                                                         {world.portrait_connections["13th Street"]: CanReachLocation(f'{world.portrait_connections["Forgotten City"]}: Boss Room'),
                                                         world.portrait_connections["Burnt Paradise"]: CanReachLocation(f'{world.portrait_connections["Dark Academy"]}: Boss Room')})
                                                         
    world.get_region("City of Haze").add_exits(["City of Haze - East"],
                                                         {"City of Haze - East": Has("Puppet Master") | HasAll("Change Cube", "Call Cube")})

    world.get_region("City of Haze - East").add_exits(["City of Haze - Post-Boss"],
                                                      {"City of Haze - Post-Boss": (Has("City Key") | OptionFilter(AddBossKeys, 0) | OptionFilter(ExcludedBossKeys, "City Key", "contains"))})

    world.get_region("Sandy Grave").add_exits(["Sandy Grave - Upper Pyramid"],
                                                         {"Sandy Grave - Upper Pyramid": (small_uppies & Has("Puppet Master")) | medium_uppies})

    world.get_region("Nation of Fools").add_exits(["Nation of Fools - Right Lower", "Nation of Fools - Main"],
                                                         {"Nation of Fools - Right Lower": small_uppies | Has("Puppet Master"),
                                                          "Nation of Fools - Main": medium_uppies | HasAll("Acrobat Cube", "Puppet Master", "Call Cube")})

    world.get_region("Nation of Fools - Right Lower").add_exits(["Nation of Fools - Right Lower Medium Room"],
                                                         {"Nation of Fools - Right Lower Medium Room": small_uppies})

    world.get_region("Sandy Grave - Upper Pyramid").add_exits(["Sandy Grave - Pyramid Top"],
                                                         {"Sandy Grave - Pyramid Top": medium_uppies})

    world.get_region("Forest of Doom").add_exits(["Forest of Doom - Main"],
                                                         {"Forest of Doom - Main": small_uppies})

    world.get_region("Forest of Doom - Main").add_exits(["Forest of Doom - Cave"],
                                                         {"Forest of Doom - Cave": strongies})

    world.get_region("Dark Academy").add_exits(["Dark Academy - Right Building"],
                                                         {"Dark Academy - Right Building": small_uppies | Has("Puppet Master")})

    world.get_region("Dark Academy - Right Building").add_exits(["Dark Academy - Main"],
                                                            {"Dark Academy - Main": big_uppies})

    world.get_region("Forgotten City").add_exits(["Forgotten City - Inner"],
                                                 {"Forgotten City - Inner": medium_uppies | Has("Puppet Master")})

    world.get_region("Forgotten City - Inner").add_exits(["Forgotten City - Inner Upper"],
                                                         {"Forgotten City - Inner Upper": medium_uppies | (HasAll("Puppet Master", "Acrobat Cube", "Call Cube"))})

    world.get_region("13th Street").add_exits(["13th Street - Main"],
                                              {"13th Street - Main": HasAll("Strength Glove", "Push Cube", "Call Cube")})  # This one ACTUALLY needs all 3

    world.get_region("Burnt Paradise").add_exits(["Burnt Paradise - Entrance"],
                                                            {"Burnt Paradise - Entrance": small_uppies | Has("Puppet Master")})

    if world.options.open_throne:
        world.get_region("Master's Keep - Upper Quarters").connect(world.get_region("The Throne Room"), "Throne Barrier")  #  No logic in this case, since it's already been opened
    else:
        if world.options.goal:
            # Add a connection to the throne room if goal is on
            world.get_region("Master's Keep - Upper Quarters").connect(world.get_region("The Throne Room"), "Throne Barrier",
                Has("Portrait Clear", FromOption(DraculaPortraits)) &
                Has("Brauner Defeated", options=[OptionFilter(BraunerRequired, 1)], filtered_resolution=True) &
                CanReachLocation("Nest of Evil: Doppelganger Reward", options=[OptionFilter(NestofEvil, NestofEvil.option_required)], filtered_resolution=True))
