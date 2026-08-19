from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .Locations import get_locations
from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation
from .glyph_regions import set_enemy_glyph_regions
from .Options import RandomStolenGlyphs, RandomDropGlyphs
from .modules.area_shuffle import shuffle_doors

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
    "Oblivion Ridge Beyond Boss",
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
    "Castle Entrance - Barracks Shortcut",
    "Library",
    "Library - Past Wallman",
    "Library Upper Exit",
    "Forsaken Cloister - Left",
    "Underground Labyrinth",
    "Barracks",
    "Mechanical Tower",
    "Mechanical Tower Upper",  # Magnes or flight
    "Mechanical Tower Lower",
    "Mechanical Tower Upper Exit",
    "Arms Depot",
    "Forsaken Cloister - Right",
    "Forsaken Cloister - Upper",
    "Final Approach",
    "Final Approach - Throne",  # FLight only
    "Final Approach - Shortcut"
]


def init_areas(world: "OoEWorld") -> None:
    regions = []
    active_glyphs = ["Wallman"]
    #  Calculate the glyph pool
    if world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_glyphsanity:
        active_glyphs.extend(list(world.glyph_steals))
        if world.options.remove_large_cavern:
            #  Remove inaccessible glyph checks
            active_glyphs = [glyph for glyph in active_glyphs if glyph not in ["Demon Lord", "Jiang Shi"]]

    if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_glyphsanity:
        active_glyphs.extend(list(world.glyph_drops))

    active_regions = region_list.copy()

    if world.options.remove_training_hall:
        active_regions.remove("Training Hall")

    if world.options.remove_large_cavern:
        active_regions.remove("Large Cavern")

    active_regions.extend(active_glyphs)

    for area in active_regions:
        regions.append(Region(area, world.player, world.multiworld))

    world.multiworld.regions += regions
    create_locations(world, active_regions)
    connect_regions(world)
    #  If world.options.shuffle_castle_areas
    shuffle_doors(world)


def create_locations(world, active_regions):
    from .static_location_data import location_ids
    all_locations = get_locations(world)

    for location in all_locations:
        if location.region not in active_regions:
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

    world.get_region("Oblivion Ridge").connect(world.get_region("Oblivion Ridge Beyond Boss"), rule=Has("Lizard Tail"))

    world.get_region("Minera Prison Island").connect(world.get_region("Minera Prison Island Main"), rule=HasAny("Ordinary Rock", "Volaticus", "Magnes"))
    world.get_region("Minera Prison Island Main").connect(world.get_region("Minera Prison Island Final Segment"), rule=HasAny("Volaticus", "Magnes"))

    world.get_region("Dracula's Castle").connect(world.get_region("Castle Entrance"), rule=HasAny("Volaticus", "Ordinary Rock"))

    ###################################################
    world.get_region("Castle Entrance").connect(world.get_region("Castle Entrance - Right Side"), rule=Has("Paries"))
    world.get_region("Castle Entrance").connect(world.get_region("Library"), "Sec00Rm07")  # Entrance is named after Sector, Room

    world.get_region("Castle Entrance - Right Side").connect(world.get_region("Underground Labyrinth"), "Sec01Rm03")
    world.get_region("Castle Entrance - Right Side").connect(world.get_region("Castle Entrance"), rule=Has("Paries"))

    world.get_region("Castle Entrance - Barracks Shortcut").connect(world.get_region("Barracks"), "Sec01Rm07")
    world.get_region("Castle Entrance - Barracks Shortcut").connect(world.get_region("Castle Entrance - Right Side"))
    ####################################################
    world.get_region("Library").connect(world.get_region("Castle Entrance"), "Sec03Rm00")
    world.get_region("Library").connect(world.get_region("Library - Past Wallman"), rule=Has("Paries"))
    world.get_region("Library - Past Wallman").add_exits({"Forsaken Cloister - Left": "Sec03Rm10", "Library Upper Exit": None, "Library": None}, {
                     "Library Upper Exit": Has("Volaticus"),
                     "Library": Has("Paries")})

    world.get_region("Library Upper Exit").add_exits({"Library - Past Wallman": None, "Final Approach - Shortcut": "Sec03Rm0B"})
    #####################################################
    world.get_region("Underground Labyrinth").connect(world.get_region("Castle Entrance - Right Side"), "Sec02Rm00")
    world.get_region("Underground Labyrinth").connect(world.get_region("Barracks"), "Sec02Rm0E")
    #####################################################
    world.get_region("Barracks").connect(world.get_region("Underground Labyrinth"), "Sec05Rm04")
    world.get_region("Barracks").connect(world.get_region("Mechanical Tower"), "Sec05Rm11")
    world.get_region("Barracks").connect(world.get_region("Castle Entrance - Barracks Shortcut"), "Sec05Rm03")
    ######################################################
    world.get_region("Mechanical Tower").add_exits({"Mechanical Tower Upper": None, "Mechanical Tower Lower": None, "Barracks": "Sec07Rm01"}, {
                                             "Mechanical Tower Upper": HasAny("Magnes", "Volaticus"),
                                             "Mechanical Tower Lower": HasAny("Magnes", "Volaticus")})

    world.get_region("Mechanical Tower Upper").connect(world.get_region("Mechanical Tower Upper Exit"))
    world.get_region("Mechanical Tower Upper Exit").connect(world.get_region("Forsaken Cloister - Right"), "Sec06Rm0B")
    world.get_region("Mechanical Tower Upper Exit").connect(world.get_region("Mechanical Tower Upper"), rule=HasAny("Magnes", "Volaticus"))

    world.get_region("Mechanical Tower Lower").connect(world.get_region("Arms Depot"), "Sec06Rm01")
    world.get_region("Mechanical Tower Lower").connect(world.get_region("Mechanical Tower"), rule=HasAny("Volaticus", "Magness"))
    ########################################################
    world.get_region("Arms Depot").connect(world.get_region("Mechanical Tower Lower"), "Sec08Rm02")
    ########################################################
    world.get_region("Forsaken Cloister - Right").connect(world.get_region("Forsaken Cloister - Left"))
    world.get_region("Forsaken Cloister - Right").connect(world.get_region("Mechanical Tower Upper Exit"), "Sec09Rm07")
    world.get_region("Forsaken Cloister - Left").connect(world.get_region("Forsaken Cloister - Upper"), rule=HasAll("Dextro Custos", "Sinestro Custos", "Arma Custos"))
    world.get_region("Forsaken Cloister - Left").connect(world.get_region("Library - Past Wallman"), "Sec09Rm03")
    world.get_region("Forsaken Cloister - Upper").connect(world.get_region("Final Approach"))
    ########################################################

    world.get_region("Final Approach").add_exits(["Final Approach - Throne", "Library Upper Exit"], {
                                                 "Final Approach - Throne": Has("Volaticus"),
                                                 "Final Approach - Shortcut": Has("Volaticus")})
    world.get_region("Final Approach - Shortcut").connect(world.get_region("Library Upper Exit"), "Sec0ARm01")
    set_enemy_glyph_regions(world)
