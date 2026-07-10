from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .Locations import get_locations
from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation

if TYPE_CHECKING:
    from . import OoEWorld


class OoELocation(Location):
    game: str = "Castlevania: Order of Ecclesia"


region_list = [
    "Game Start",
    "World Map",

    "Dracula's Castle",  # World map areas
    "Ecclesia",
    "Wygol Village",
    "Training Hall",
    "Ruvas Forest",
    "Argila Swamp",
    "Kalidus Channel",
    "Somnus Reef",
    "Minera Prison Island",
    "Lighthouse",
    "Tymeo Mountains",
    "Tristis Pass",
    "Large Cavern",
    "Giant's Dwelling",
    "Mystery Manor",
    "Misty Forest Road",
    "Oblivion Ridge",
    "Skeleton Cave",
    "Monastery",

    "Kalidus Channel Depths Right",
    "Kalidus Channel Depths Left",
    "Somnus Reef Main",
    "Lighthouse Past Spikes",
    "Lighthouse Post-Boss",
    "Giant's Dwelling Main",
    "Tymeo Mountains Past Spikes Room",
    "Tymeo Mountains East",
    "Tristis Pass Frozen Area",
    "Tristis Pass Waterfall",
    "Monastery Magnets Area",
    "Mystery Manor Main",
    "Minera Prison Island Main",
    "Minera Prison Island Final Segment",

    "Castle Entrance",
    "Castle Entrance - Right Side",
    "Library",
    "Library - Past Wallman",
    "Forsaken Cloister - Left",
    "Underground Labyrinth",
    "Barracks",
    "Mechanical Tower",
    "Mechanical Tower Upper",  # Magnes or flight
    "Mechanical Tower Lower",
    "Arms Depot",
    "Forsaken Cloister - Right",
    "Forsaken Cloister - Upper",
    "Final Approach",
    "Final Approach - Throne"  # FLight only
]


def init_areas(world: "OoEWorld") -> None:
    regions = []
    active_regions = region_list.copy()

    if world.options.remove_training_hall:
        active_regions.remove("Training Hall")

    if world.options.remove_large_cavern:
        active_regions.remove("Large Cavern")

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
        region.locations.append(OoELocation(world.player, location.name, None if location.is_event else location_ids[location.name], region))


def connect_regions(world):
    world_map_regions = ["Training Hall", "Ruvas Forest", "Argila Swamp", "Kalidus Channel", "Somnus Reef", "Minera Prison Island",
                         "Lighthouse", "Tymeo Mountains", "Tristis Pass", "Large Cavern", "Giant's Dwelling", "Mystery Manor",
                         "Misty Forest Road", "Oblivion Ridge", "Skeleton Cave", "Monastery"]

    world.get_region("Game Start").connect(world.get_region("Ecclesia"), rule=Has(world.starting_glyph))

    if world.options.remove_large_cavern:
        world_map_regions.remove("Large Cavern")

    if world.options.remove_training_hall:
        world_map_regions.remove("Training Hall")

    for area in world_map_regions:
        world.get_region("World Map").add_exits([area], {area: Has(f"Map: {area}")})

    world.get_region("World Map").add_exits(["Dracula's Castle", "Ecclesia", "Wygol Village", "Kalidus Channel Depths Right"], {
                                             "Dracula's Castle": Has("Castle Access"),
                                             "Kalidus Channel Depths Right": Has("Map: Kalidus Channel", 2) & Has("Serpent Scale")})

    world.get_region("Ecclesia").add_exits(["World Map"])

    world.get_region("Kalidus Channel Depths Right").connect(world.get_region("Kalidus Channel Depths Left"), rule=Has("Lizard Tail"))

    world.get_region("Somnus Reef").connect(world.get_region("Somnus Reef Main"), rule=Has("Serpent Scale"))

    world.get_region("Lighthouse").connect(world.get_region("Lighthouse Past Spikes"), rule=HasAny("Magnes", "Volaticus", "Rapidus Fio", "Arma Machina"))
    world.get_region("Lighthouse Past Spikes").connect(world.get_region("Lighthouse Post-Boss"), rule=HasAny("Magnes", "Volaticus", "Ordinary Rock"))

    world.get_region("Giant's Dwelling").connect(world.get_region("Giant's Dwelling Main"), rule=HasAny("Volaticus", "Ordinary Rock"))

    world.get_region("Tymeo Mountains").connect(world.get_region("Tymeo Mountains Past Spikes Room"), rule=HasAny("Magnes", "Volaticus", "Arma Machina"))
    world.get_region("Tymeo Mountains Past Spikes Room").connect(world.get_region("Tymeo Mountains East"), rule=HasAny("Ordinary Rock", "Volaticus", "Rapidus Fio"))

    world.get_region("Tristis Pass").connect(world.get_region("Tristis Pass Frozen Area"), rule=HasAny("Ordinary Rock", "Volaticus"))
    world.get_region("Tristis Pass Frozen Area").connect(world.get_region("Tristis Pass Waterfall"), rule=CanReachLocation("Tristis Pass: Frozen Waterfall Glyph"))
    
    world.get_region("Monastery").connect(world.get_region("Monastery Magnets Area"), rule=HasAny("Magnes", "Volaticus"))

    world.get_region("Mystery Manor").connect(world.get_region("Mystery Manor Main"), rule=HasAny("Ordinary Rock", "Volaticus", "Rapidus Fio"))

    world.get_region("Minera Prison Island").connect(world.get_region("Minera Prison Island Main"), rule=HasAny("Ordinary Rock", "Volaticus", "Magnes"))
    world.get_region("Minera Prison Island Main").connect(world.get_region("Minera Prison Island Final Segment"), rule=HasAny("Volaticus", "Magnes"))

    world.get_region("Dracula's Castle").connect(world.get_region("Castle Entrance"), rule=HasAny("Volaticus", "Ordinary Rock"))

    world.get_region("Castle Entrance").connect(world.get_region("Castle Entrance - Right Side"), rule=Has("Paries"))
    world.get_region("Castle Entrance").connect(world.get_region("Library"))
    world.get_region("Castle Entrance - Right Side").connect(world.get_region("Underground Labyrinth"))

    world.get_region("Library").connect(world.get_region("Library - Past Wallman"), rule=Has("Paries"))
    world.get_region("Library - Past Wallman").connect(world.get_region("Forsaken Cloister - Left"))

    world.get_region("Underground Labyrinth").connect(world.get_region("Barracks"))

    world.get_region("Barracks").connect(world.get_region("Mechanical Tower"))

    world.get_region("Mechanical Tower").add_exits(["Arms Depot", "Mechanical Tower Upper", "Mechanical Tower Lower"], {
                                             "Mechanical Tower Upper": HasAny("Magnes", "Volaticus"),
                                             "Mechanical Tower Lower": HasAny("Magnes", "Volaticus")})

    world.get_region("Mechanical Tower Upper").connect(world.get_region("Forsaken Cloister - Right"))

    world.get_region("Forsaken Cloister - Right").connect(world.get_region("Forsaken Cloister - Left"))
    world.get_region("Forsaken Cloister - Left").connect(world.get_region("Forsaken Cloister - Upper"), rule=HasAll("Dextro Custos", "Sinestro Custos", "Arma Custos"))
    world.get_region("Forsaken Cloister - Upper").connect(world.get_region("Final Approach"))

    world.get_region("Final Approach").connect(world.get_region("Final Approach - Throne"), rule=Has("Volaticus"))
