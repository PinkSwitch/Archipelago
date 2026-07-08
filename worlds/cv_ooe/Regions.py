from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .Locations import get_locations
from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation

if TYPE_CHECKING:
    from . import OoEWorld


class OoELocation(Location):
    game: str = "Castlevania: Order of Ecclesia"


region_list = [
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

    "Kalidus Channel Depths",
    "Somnus Reef Main",  # Swim
    "Lighthouse Past Spikes",  # Magnes, flight, speed, or Machina
    "Lighthouse Post-Boss",  # Uppes or Magnes
    "Giant's Dwelling Main",  # Need Uppes
    "Tymeo Mountains Past Spikes Room",  # Magnes, flight, or Machina
    "Tymeo Mountains East",  # Uppies or speed
    "Tristis Pass Frozen Area",  # Uppes
    "Tristis Pass Waterfall",  # Needs to be unfrozen. Can reach the frozen waterfall glyph. Hard requires Magnes
    "Monastery Magnets Area",  # Magnes or flight
    "Mystery Manor Main",  # Uppes or speed,
    "Minera Prison Island Main",  # Double Jump, Magnes, Flight
    "Minera Prison Island Final Segment",  # Flight or Magnes

    "Castle Entrance",  # Needs Uppes
    "Castle Entrance - Right Side",  # Needs Paries
    "Library",
    "Library - Past Wallman",  # Paries
    "Forsaken Cloister - Left",
    "Underground Labyrinth",
    "Barracks",
    "Mechanical Tower",
    "Mechanical Tower Upper",  # Magnes or flight
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

    if world.options.remove_large_cavern:
        world_map_regions.remove("Large Cavern")

    if world.options.remove_training_hall:
        world_map_regions.remove("Training Hall")

    for area in world_map_regions:
        world.get_region("World Map").add_exits([area], {area: Has(f"Map: {area}")})

    world.get_region("World Map").add_exits(["Dracula's Castle", "Ecclesia"], {
                                             "Dracula's Castle": Has("Castle Access")})

    world.get_region("Ecclesia").add_exits(["World Map"])

    world.get_region("Kalidus Channel").add_exits(["Kalidus Channel Depths"], {"Kalidus Channel Depths": Has("Serpent Scale")})
        