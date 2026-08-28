from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData, get_locations
from .Rules import small_uppies, big_uppies
from .soul_regions import create_soul_regions
from .Options import GateItems
if TYPE_CHECKING:
    from . import DoSWorld


class DoSLocation(Location):
    game: str = "Castlevania: Dawn of Sorrow"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


region_list = [
    "Lost Village Upper",
    "Lost Village Upper Doorway",
    "Lost Village Lower",
    "Lost Village Underground Bottom",
    "Lost Village Underground Middle",
    "Lost Village Underground Top",
    "Lost Village Courtyard",

    "Wizardry Lab Main",
    "Wizardry Lab West Gate",
    "Wizardry Lab East Gate",
    "Wizardry Lab Sunken",
    "Wizardry Lab Sunken West Door",
    "Wizardry Lab Sunken East Door",

    "Garden of Madness Lower",
    "Garden of Madness Upper",
    "Garden of Madness Water Blocked",
    "Garden of Madness Post-Boss",
    "Garden of Madness East Gate",

    "Demon Guest House Main",
    "Demon Guest House Puppet Wall Right",
    "Demon Guest House Lower",
    "Demon Guest House Number Puzzle",
    "Demon Guest House Number Puzzle West",
    "Demon Guest House West Wing",
    "Demon Guest House Upper",

    "Dark Chapel",
    "Dark Chapel Big Room",
    "Dark Chapel Catacombs Exit",

    "Condemned Tower Bottom",
    "Condemned Tower Main",
    "Condemned Tower Top",

    "Cursed Clock Tower Entrance",
    "Cursed Clock Tower Central",
    "Cursed Clock Tower Boss Area",
    "Cursed Clock Tower Post-Boss",
    "Cursed Clock Tower Exit",

    "Subterranean Hell Top Entrance",
    "Subterranean Hell East",
    "Subterranean Hell Central/East Connection",
    "Subterranean Hell Central Upper",
    "Subterranean Hell Central Exit",
    "Subterranean Hell Central Lower",
    "Subterranean Hell Central/Shaft Divide",
    "Subterranean Hell Shaft Middle",
    "Subterranean Hell Shaft Top",
    "Subterranean Hell Shaft Bottom",
    "Subterranean Hell Shaft Bottom Stairs",
    "Subterranean Hell Spike Room West",
    "Subterranean Hell Spike Room East",
    "Subterranean Hell Button Gate Room",

    "Silenced Ruins Antechamber",
    "Silenced Ruins",
    "Silenced Ruins Back Exit",
    "Silenced Ruins Upper Entrance",

    "The Pinnacle",
    "The Pinnacle Throne Room",
    "The Pinnacle Lower",
    "Warp Room"



]


def init_areas(world: "DoSWorld") -> None:
    player = world.player
    regions = []
    if world.options.boost_speed:
        sub_hell_speed = lambda state: True
    else:
        sub_hell_speed = lambda state: state.has_any({"Flying Armor Soul", "Black Panther Soul"}, player)

    active_regions = region_list.copy()

    if world.mine_status != "Disabled":
        active_regions.extend([
            "Mine of Judgment",
            "The Abyss",
            'The Abyss Beyond Abaddon'])

    for region in world.common_souls:
        active_regions.append(region)

    for region in world.uncommon_souls:
        active_regions.append(region)

    for region in world.rare_souls:
        active_regions.append(region)

    for area in active_regions:
        regions.append(Region(area, world.player, world.multiworld))

    world.multiworld.regions += regions
    create_locations(world, active_regions)
    connect_regions(world)


def create_locations(world, active_regions):
    from .static_location_data import location_ids
    all_locations = get_locations(world)

    for location in all_locations:
        if location.region not in active_regions:
            raise ValueError(f"Error: Region {location.region} is invalid for location {location.name}.")
        region = world.get_region(location.region)
        region.locations.append(
            DoSLocation(world.player, location.name, None if location.is_event else location_ids[location.name],
                        region))


def connect_regions(world):
    from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation, HasGroupUnique, OptionFilter
    # Lost Village
    world.get_region("Lost Village Upper").add_exits(["Wizardry Lab Main", "Lost Village Upper Doorway"],
                                                     {"Wizardry Lab Main": Has("Moat Drained"),
                                                     "Lost Village Upper Doorway": small_uppies | (Has("Puppet Master Soul") & HasAny("Flying Armor Soul", "Skeleton Ape Soul")),
                                                      "Lost Village Lower": Has(world.magic_seal_table["Lost Village"])})  # Is the ape trick hard? Can be done without ape if speedboost on

    if world.options.open_drawbridge:
        # Open courtyard removes this rule
        world.get_region("Lost Village Upper").add_exits(["Lost Village Courtyard"])
    else:
        world.get_region("Lost Village Upper").add_exits(["Lost Village Courtyard"],
                                                         {"Lost Village Courtyard": small_uppies})

    world.get_region("Lost Village Courtyard").add_exits(["Lost Village Upper", "Demon Guest House Lower"])

    world.get_region("Lost Village Upper Doorway").add_exits(["Lost Village Upper", "Demon Guest House Number Puzzle West"])

    world.get_region("Lost Village Lower").add_exits(["Lost Village Upper", "Warp Room"],
                                                     {"Lost Village Upper": Has(world.magic_seal_table["Lost Village"])})

    world.get_region("Lost Village Underground Bottom").add_exits(["Lost Village Underground Middle", "Wizardry Lab Sunken"],
                                                                  {"Lost Village Underground Middle": small_uppies | Has("Puppet Master Soul"),
                                                                   "Wizardry Lab Sunken": Has("Rahab Soul")})

    world.get_region("Lost Village Underground Middle").add_exits(["Lost Village Underground Top", "Wizardry Lab West Gate", "Lost Village Underground Bottom"],
                                                                  {"Lost Village Underground Top": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Lost Village Underground Top").add_exits(["Lost Village Lower", "Lost Village Underground Middle"])
    #######################
    # Wizardry Lab

    world.get_region("Wizardry Lab Main").add_exits(["Lost Village Lower", "Garden of Madness Lower", "Warp Room", "Wizardry Lab West Gate", "Wizardry Lab East Gate"],
                                                    {"Lost Village Lower": Has("Moat Drained"),
                                                     "Garden of Madness Lower": small_uppies | Has("Balore Soul"),
                                                     "Wizardry Lab West Gate": Has("West Lab Gate Key"),
                                                     "Wizardry Lab East Gate": Has("East Lab Gate Key")})

    world.get_region("Wizardry Lab West Gate").add_exits(["Lost Village Underground Middle"])
    world.get_region("Wizardry Lab East Gate").add_exits(["Subterranean Hell Shaft Top"])
    world.get_region("Wizardry Lab Sunken West Door").add_exits(["Lost Village Underground Bottom", "Wizardry Lab Sunken"],
                                                                {"Wizardry Lab Sunken": Has("Rahab Soul")})

    world.get_region("Wizardry Lab Sunken").add_exits(["Wizardry Lab Sunken West Door", "Wizardry Lab Sunken East Door"],
                                                      {"Wizardry Lab Sunken West Door": big_uppies})

    world.get_region("Wizardry Lab Sunken East Door").add_exits(["Wizardry Lab Sunken", "Subterranean Hell Spike Room West"],
                                                                {"Wizardry Lab Sunken": Has("Rahab Soul")})
    
    if world.options.gate_items < GateItems.option_buttonsanity:
        world.get_region("Wizardry Lab West Gate").add_exits(["Wizardry Lab Main"])
        world.get_region("Wizardry Lab East Gate").add_exits(["Wizardry Lab Main"])
    else:
        world.get_region("Wizardry Lab West Gate").add_exits(["Wizardry Lab Main"],
                                                             {"Wizardry Lab Main": Has("West Lab Gate Key")})
        world.get_region("Wizardry Lab East Gate").add_exits(["Wizardry Lab Main"],
                                                             {"Wizardry Lab Main": Has("East Lab Gate Key")})
    ##########################
    # Garden of Madness
    world.get_region("Garden of Madness Lower").add_exits(["Wizardry Lab Main", "Garden of Madness Water Blocked", "Demon Guest House Lower", "Garden of Madness Upper", "Dark Chapel", "Warp Room"],
                                                          {"Garden of Madness Water Blocked": Has("Rahab Soul"),
                                                           "Garden of Madness Upper": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Garden of Madness Water Blocked").add_exits(["Garden of Madness Lower", "Subterranean Hell Central Exit"],
                                                                  {"Garden of Madness Lower": Has("Rahab Soul")})

    world.get_region("Garden of Madness Upper").add_exits(["Garden of Madness Lower", "Garden of Madness Post-Boss"],
                                                          {"Garden of Madness Post-Boss": Has(world.magic_seal_table["Garden of Madness"])})

    world.get_region("Garden of Madness Post-Boss").add_exits(["Garden of Madness Upper", "Demon Guest House Main", "Garden of Madness East Gate"],
                                                              {"Garden of Madness Upper": Has(world.magic_seal_table["Garden of Madness"]),
                                                               "Garden of Madness East Gate": Has("Garden Gate Key")})

    world.get_region("Garden of Madness East Gate").add_exits(["Cursed Clock Tower Entrance"])
    if world.options.gate_items < GateItems.option_buttonsanity:
        world.get_region("Garden of Madness East Gate").add_exits(["Garden of Madness Post-Boss"])
    else:
        world.get_region("Garden of Madness East Gate").add_exits(["Garden of Madness Post-Boss"],
                                                                  {"Garden of Madness Post-Boss": Has("Garden Gate Key")})
    #############################
    # Demon Guest House
    world.get_region("Demon Guest House Main").add_exits(["Garden of Madness Post-Boss", "Demon Guest House Puppet Wall Right", "Demon Guest House Number Puzzle", "Demon Guest House West Wing"],
                                                         {"Demon Guest House Puppet Wall Right": HasAny("Puppet Master Soul", "Bat Company Soul"),
                                                          "Demon Guest House West Wing": HasAny("Puppet Master Soul", "Bat Company Soul")})

    world.get_region("Demon Guest House Puppet Wall Right").add_exits(["Demon Guest House Main", "Demon Guest House Lower"],
                                                                      {"Demon Guest House Main": HasAny("Puppet Master Soul", "Bat Company Soul")})

    world.get_region("Demon Guest House Lower").add_exits(["Lost Village Upper", "Garden of Madness Lower", "Demon Guest House Puppet Wall Right"],
                                                          {"Demon Guest House Puppet Wall Right": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Demon Guest House Number Puzzle").add_exits(["Demon Guest House Main", "Demon Guest House West Wing", "Demon Guest House Number Puzzle West"],
                                                                  {"Demon Guest House West Wing": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Demon Guest House Number Puzzle West").add_exits(["Lost Village Upper Doorway"])

    world.get_region("Demon Guest House West Wing").add_exits(["Demon Guest House Main", "Demon Guest House Number Puzzle", "Warp Room"],
                                                              {"Demon Guest House Main": HasAny("Puppet Master Soul", "Bat Company Soul")})

    world.get_region("Demon Guest House Upper").add_exits(["Demon Guest House Main", "The Pinnacle Lower"])
    ###############################
    # Dark Chapel
    world.get_region("Dark Chapel").add_exits(["Garden of Madness Lower", "Dark Chapel Catacombs Exit", "Dark Chapel Big Room", "Warp Room"],
                                              {"Dark Chapel Catacombs Exit": HasAny("Puppet Master Soul", "Bat Company Soul"),
                                               "Dark Chapel Big Room": HasAny("Puppet Master Soul", "Bat Company Soul")})

    world.get_region("Dark Chapel Big Room").add_exits(["Condemned Tower Bottom", "Dark Chapel"])

    world.get_region("Dark Chapel Catacombs Exit").add_exits(["Subterranean Hell Top Entrance", "Dark Chapel"],
                                                             {"Dark Chapel": HasAny("Puppet Master Soul", "Bat Company Soul")})
    ##########################################################################################################
    # Condemned Tower
    world.get_region("Condemned Tower Bottom").add_exits(["Dark Chapel", "Dark Chapel Big Room", "Condemned Tower Main"],
                                                         {"Condemned Tower Main": small_uppies | Has("Puppet Master Soul"),
                                                          "Dark Chapel Big Room": small_uppies})
    if world.mine_status != "Disabled":
        if not world.mine_status or world.mine_status == "Open":
            world.get_region("Condemned Tower Bottom").add_exits(["Mine of Judgment"])  # Add a ruleless connector here
        else:
            world.get_region("Condemned Tower Bottom").add_exits(["Mine of Judgment"],
                                                                 {"Mine of Judgment": HasAll(*world.mine_triggers)})

    world.get_region("Condemned Tower Main").add_exits(["Condemned Tower Bottom", "Cursed Clock Tower Entrance", "Condemned Tower Top"],
                                                       {"Cursed Clock Tower Entrance": Has("Tower Key"),
                                                        "Condemned Tower Top": Has(world.magic_seal_table["Condemned Tower"])})

    world.get_region("Condemned Tower Top").add_exits(["Condemned Tower Main", "Warp Room"],
                                                      {"Condemned Tower Main": Has(world.magic_seal_table["Condemned Tower"])})
                                                                    
    ################################
    # Cursed Clock Tower
    world.get_region("Cursed Clock Tower Entrance").add_exits(["Garden of Madness East Gate", "Condemned Tower Main", "Cursed Clock Tower Central"],
                                                              {"Cursed Clock Tower Central": small_uppies | Has("Puppet Master Soul"),
                                                               "Condemned Tower Main": Has("Tower Key")})

    world.get_region("Cursed Clock Tower Central").add_exits(["Cursed Clock Tower Entrance", "Cursed Clock Tower Boss Area"],
                                                             {"Cursed Clock Tower Boss Area": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Cursed Clock Tower Boss Area").add_exits(["Cursed Clock Tower Central", "Cursed Clock Tower Post-Boss"],
                                                               {"Cursed Clock Tower Post-Boss": Has(world.magic_seal_table["Cursed Clock Tower"])})

    world.get_region("Cursed Clock Tower Post-Boss").add_exits(["Cursed Clock Tower Boss Area", "Cursed Clock Tower Exit", "Cursed Clock Tower Central", "Warp Room"],
                                                               {"Cursed Clock Tower Boss Area": Has(world.magic_seal_table["Cursed Clock Tower"]),
                                                                "Cursed Clock Tower Exit": Has("Bat Company Soul")})

    world.get_region("Cursed Clock Tower Exit").add_exits(["Cursed Clock Tower Post-Boss", "The Pinnacle Lower"],
                                                          {"Cursed Clock Tower Post-Boss": Has("Bat Comapny Soul")})
    ####################################################################################
    # Subterranean Hell
    world.get_region("Subterranean Hell Top Entrance").add_exits(["Dark Chapel Catacombs Exit", "Subterranean Hell East"],
                                                                 {"Subterranean Hell East": HasAll("Rahab Soul", world.magic_seal_table["Subterranean Hell"])})

    world.get_region("Subterranean Hell East").add_exits(["Subterranean Hell Top Entrance", "Subterranean Hell Central/East Connection", "Subterranean Hell Button Gate Room"],
                                                         {"Subterranean Hell Top Entrance": lambda state: state.has_all({"Rahab Soul", world.magic_seal_table["Subterranean Hell"]}) and (state.has_any(small_uppies) or state.has("Puppet Master Soul")),
                                                          "Subterranean Hell Central/East Connection": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Subterranean Hell Central/East Connection").add_exits(["Subterranean Hell Central Upper", "Subterranean Hell East"],
                                                                            {"Subterranean Hell Central Upper": HasAny("Rahab Soul", "Malphas Soul"),
                                                                             "Subterranean Hell East": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Subterranean Hell Central Upper").add_exits(["Subterranean Hell Central/East Connection", "Subterranean Hell Central Exit", "Subterranean Hell Central Lower"],
                                                                  {"Subterranean Hell Central Exit": lambda state: state.has_any(small_uppies) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}),
                                                                   "Subterranean Hell Central/East Connection": HasAny("Rahab Soul", "Malphas Soul")})

    world.get_region("Subterranean Hell Central Exit").add_exits(["Subterranean Hell Central Upper", "Garden of Madness Water Blocked"],
                                                                 {"Subterranean Hell Central Upper": HasAny("Rahab Soul", "Malphas Soul")})

    world.get_region("Subterranean Hell Central Lower").add_exits(["Subterranean Hell Central Upper", "Subterranean Hell Central/Shaft Divide", "Warp Room", "Subterranean Hell Shaft Middle"],
                                                                  {"Subterranean Hell Central Upper": small_uppies | Has("Puppet Master Soul"),
                                                                   "Subterranean Hell Shaft Middle": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Subterranean Hell Shaft Middle").add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Shaft Bottom", "Subterranean Hell Shaft Top", "Subterranean Hell Shaft Bottom Stairs"],
                                                                 {"Subterranean Hell Central Lower": small_uppies | Has("Puppet Master Soul"),
                                                                  "Subterranean Hell Shaft Top": big_uppies})

    world.get_region("Subterranean Hell Shaft Top").add_exits(["Subterranean Hell Shaft Middle", "Wizardry Lab East Gate", "Subterranean Hell Shaft Bottom Stairs"],
                                                              {"Subterranean Hell Shaft Middle": sub_hell_speed})

    world.get_region("Subterranean Hell Shaft Bottom").add_exits(["Subterranean Hell Spike Room East", "Silenced Ruins Antechamber", "Subterranean Hell Shaft Bottom Stairs"],
                                                                 {"Subterranean Hell Shaft Middle": small_uppies | Has("Puppet Master Soul"),
                                                                  "Subterranean Hell Shaft Bottom Stairs": small_uppies | Has("Puppet Master Soul"),
                                                                  "Subterranean Hell Spike Room East": small_uppies | Has("Puppet Master Soul"),
                                                                  "Silenced Ruins Antechamber": lambda state: state.has_any(small_uppies) or state.has_any({"Puppet Master Soul", "Flying Armor Soul", "Black Panther Soul"})})

    world.get_region("Subterranean Hell Shaft Bottom Stairs").add_exits(["Subterranean Hell Shaft Bottom", "Subterranean Hell Central/Shaft Divide"],
                                                                        {"Subterranean Hell Central/Shaft Divide": small_uppies | Has("Puppet Master Soul")})

    world.get_region("Subterranean Hell Spike Room East").add_exits(["Subterranean Hell Shaft Bottom"])

    world.get_region("Subterranean Hell Spike Room West").add_exits(["Wizardry Lab Sunken East Door"])

    world.get_region("Subterranean Hell Central/Shaft Divide").add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Shaft Bottom Stairs"])

    world.get_region("Subterranean Hell Button Gate Room").add_exits(["Subterranean Hell East", "Silenced Ruins Back Exit"],
                                                                     {"Subterranean Hell East": small_uppies | Has("Puppet Master Soul"),
                                                                      "Silenced Ruins Back Exit": Has("Cavern Gate Key")})

    #####################################################
    # Silenced Ruins
    world.get_region("Silenced Ruins Antechamber").add_exits(["Subterranean Hell Shaft Bottom", "Silenced Ruins Upper Entrance"],
                                                             {"Silenced Ruins Upper Entrance": Has("Zephyr Soul")})

    world.get_region("Silenced Ruins Upper Entrance").add_exits(["Silenced Ruins Antechamber", "Silenced Ruins"],
                                                                {"Silenced Ruins Antechamber": Has("Zephyr Soul")})

    world.get_region("Silenced Ruins").add_exits(["Silenced Ruins Back Exit", "Silenced Ruins Upper Entrance", "Warp Room"],
                                                 {"Silenced Ruins Upper Entrance": small_uppies | Has("Puppet Master Soul"),
                                                 "Silenced Ruins Back Exit": lambda state: state.has_any(small_uppies) or state.has_all({"Puppet Master Soul", "Black Panther Soul"})})

    world.get_region("Silenced Ruins Back Exit").add_exits(["Silenced Ruins"])
    if world.options.gate_items < GateItems.option_buttonsanity:
        world.get_region("Silenced Ruins Back Exit").add_exits(["Subterranean Hell Button Gate Room"])
    else:
        world.get_region("Silenced Ruins Back Exit").add_exits(["Subterranean Hell Button Gate Room"],
                                                               {"Subterranean Hell Button Gate Room": Has("Cavern Gate Key")})

    ###############################
    # The Pinnacle
    world.get_region("The Pinnacle Lower").add_exits(["The Pinnacle", "Demon Guest House Upper", "Cursed Clock Tower Exit", "Warp Room"],
                                                     {"The Pinnacle": small_uppies,
                                                      "Cursed Clock Tower Exit": small_uppies | Has("Puppet Master Soul"),
                                                      "Warp Room": small_uppies | Has("Puppet Master Soul")})

    world.get_region("The Pinnacle").add_exits(["The Pinnacle Lower", "The Pinnacle Throne Room"],
                                               {"The Pinnacle Throne Room": big_uppies})

    ###############################
    # Mine of Judgment
    if world.mine_status != "Disabled":
        world.get_region("Mine of Judgment").add_exits(["The Abyss", "Warp Room"],
                                                       {"The Abyss": lambda state: (state.has_any(small_uppies) or state.has("Pupper Master Soul")) and state.has(world.magic_seal_table["Mine of Judgment"])})

        world.get_region("The Abyss").add_exits(["Mine of Judgment", "The Abyss Beyond Abaddon"],
                                                {"Mine of Judgment": small_uppies,
                                                 "The Abyss Beyond Abaddon": big_uppies & Has(world.magic_seal_table["The Absyss"])})

        world.get_region("The Abyss Beyond Abaddon").add_exits(["Warp Room"])

    world.get_region("Warp Room").add_exits([world.starting_warp_region])
    world.get_region("Subterranean Hell Spike Room East").add_exits(["Subterranean Hell Spike Room West"],
                                                                    {"Subterranean Hell Spike Room West": lambda state: state.has("Rahab Soul") and (state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}) or state.has("Bone Ark Soul"))})

    world.get_region("Subterranean Hell Spike Room West").add_exits(["Subterranean Hell Spike Room East"],
                                                                    {"Subterranean Hell Spike Room East": lambda state: state.has("Rahab Soul") and (state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}) or state.has("Bone Ark Soul"))})

    create_soul_regions(world)


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = DoSLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "DoSWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
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
    

# TODO; Skeletone Ape in tower with speedboost on
