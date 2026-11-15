from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .Locations import get_locations
from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation, OptionFilter, AtLeast, HasGroupUnique
from rule_builder.field_resolvers import FromOption
from .Options import InclusiveWhtCrystal, PoisonRing, ReqRelics, ReqOrbs

if TYPE_CHECKING:
    from . import CV2World


class CV2Location(Location):
    game: str = "Castlevania II: Simon's Quest"


# Regions are divided into screens
region_list = [
    "Town of Jova",

    "Jova Woods",

    "South Bridge",

    "Veros Woods 1",
    "Veros Woods 2",

    "Denis Woods 1",
    "Denis Woods 2",
    "Denis Woods 3",

    "Berkeley Mansion Entrance",
    "Berkeley Mansion",


    "Town of Veros",

    "Dabi's Path 1",
    "Dabi's Path 2",

    "Aljiba Woods 1",
    "Aljiba Woods 2",
    "Aljiba Woods 3",

    "Town of Aljiba",

    "Lower Road",

    "Yuba Lake",

    "Lauber Mansion Entrance",
    "Lauber Mansion",

    "Camilla Cemetery",

    "Belasco Marsh",

    "Dead River",

    "Brahm's Mansion Entrance",
    "Brahm's Mansion",

    "Vrad Mountain 1",
    "Vrad Mountain 2",

    "Town of Alba",

    "Sadam Woods 1",
    "Sadam Woods 2",
    "Sadam Woods 3",

    "Storigoi Graveyard",

    "Town of Ondol",

    "Jam Wasteland",

    "Deborah Cliff",

    "Bodley Mansion Entrance",
    "Bodley Mansion",

    "Uta Road",

    "Uta Lower Road",

    "Debious Woods Left",
    "Debious Woods Right",

    "Joma Marsh 1",
    "Joma Marsh 2",

    "Laruba Mansion Entrance",
    "Laruba Mansion",

    "Wicked Ditch",

    "Town of Doina",

    "North Bridge",

    "Dora Woods 1",
    "Dora Woods 2",
    "Dora Woods 3",

    "East Bridge",

    "Denis Marsh",

    "Town of Yomi",

    "Vrad Graveyard",

    "West Bridge",

    "Castlevania"
]


def init_areas(world: "CV2World") -> None:
    regions = []

    active_regions = region_list.copy()

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
        region.locations.append(CV2Location(world.player, location.name, None if location.is_event
                                else location_ids[location.name], region))


def connect_regions(world):
    dracula_access_rule = Has("Magic Cross") & HasAny("Holy Water", "Dracula's Nail")
    dracula_access_rule &= AtLeast(FromOption(ReqOrbs), CanReachLocation("Berkeley Mansion: Evil Orb"),
                                   CanReachLocation("Lauber Mansion: Evil Orb"),
                                   CanReachLocation("Brahm's Mansion: Evil Orb"),
                                   CanReachLocation("Bodley Mansion: Evil Orb"),
                                   CanReachLocation("Laruba Mansion: Evil Orb"))
    dracula_access_rule &= HasGroupUnique("Dracula Parts", count=FromOption(ReqRelics))

    world.get_region("Town of Jova").add_exits({"Belasco Marsh", "Jova Woods"})

    world.get_region("Jova Woods").add_exits({"Town of Jova", "South Bridge"})
    world.get_region("South Bridge").add_exits({"Jova Woods", "Veros Woods 1"})
    world.get_region("Veros Woods 1").add_exits({"South Bridge", "Veros Woods 2"})
    world.get_region("Veros Woods 2").add_exits({"Veros Woods 1", "Denis Woods 1", "Town of Veros"})
    world.get_region("Town of Veros").add_exits({"Veros Woods 2", "Dabi's Path 1"})
    world.get_region("Denis Woods 1").add_exits({"Veros Woods 2", "Berkeley Mansion Entrance"})
    world.get_region("Denis Woods 2").add_exits({"Berkeley Mansion Entrance", "Denis Woods 3"})
    world.get_region("Denis Woods 3").add_exits({"Denis Woods 2", "Dabi's Path 1"})
    world.get_region("Berkeley Mansion Entrance").add_exits({"Denis Woods 1", "Denis Woods 2", "Berkeley Mansion"})

    world.get_region("Dabi's Path 1").add_exits({"Denis Woods 3", "Town of Veros", "Dabi's Path 2"})
    world.get_region("Dabi's Path 2").add_exits({"Dabi's Path 1", "Aljiba Woods 1"})

    world.get_region("Aljiba Woods 1").add_exits({"Dabi's Path 2", "Aljiba Woods 2"})
    world.get_region("Aljiba Woods 2").add_exits({"Aljiba Woods 3", "Lower Road"})
    world.get_region("Aljiba Woods 3").add_exits({"Aljiba Woods 2", "Town of Aljiba"})

    world.get_region("Town of Aljiba").add_exits({"Aljiba Woods 3", "Camilla Cemetery"})

    world.get_region("Camilla Cemetery").add_exits({"Town of Aljiba"})

    world.get_region("Lower Road").add_exits({"Aljiba Woods 2", "Yuba Lake"}, {
        "Aljiba Woods 2": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Yuba Lake").add_exits({"Lower Road", "Lauber Mansion Entrance"}, {
                                            "Lauber Mansion Entrance": Has("Blue Crystal")})

    world.get_region("Lauber Mansion Entrance").add_exits({"Lauber Mansion"})

    world.get_region("Belasco Marsh").add_exits({"Dead River", "Town of Jova"})

    world.get_region("Dead River").add_exits({"Town of Alba", "Belasco Marsh", "Brahm's Mansion Entrance"}, {
        "Brahm's Mansion Entrance": Has("Dracula's Heart")
    })

    world.get_region("Brahm's Mansion Entrance").add_exits({"Brahm's Mansion", "Dead River", "Vrad Mountain 2"})

    world.get_region("Vrad Mountain 2").add_exits({"Vrad Mountain 1", "Brahm's Mansion Entrance"}, {
        "Vrad Mountain 1": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Town of Alba").add_exits({"Sadam Woods 1", "Dead River"})

    world.get_region("Sadam Woods 1").add_exits({"Sadam Woods 2", "Town of Alba"})
    world.get_region("Sadam Woods 2").add_exits({"Sadam Woods 3", "Storigoi Graveyard", "Sadam Woods 1"})
    world.get_region("Sadam Woods 3").add_exits({"Town of Ondol", "Sadam Woods 2"})

    world.get_region("Town of Ondol").add_exits({"Jam Wasteland", "Sadam Woods 3"})

    world.get_region("Jam Wasteland").add_exits({"Deborah Cliff", "Town of Ondol"}, {
        "Deborah Cliff": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Deborah Cliff").add_exits({"Bodley Mansion Entrance"}, {
        "Bodley Mansion Entrance": Has("Red Crystal")
    })

    world.get_region("Bodley Mansion Entrance").add_exits({"Uta Road", "Bodley Mansion", "Wicked Ditch"})

    world.get_region("Uta Road").add_exits({"Bodley Mansion Entrance", "Uta Lower Road"}, {
        "Uta Lower Road": Has("Blue Crystal")
    })

    world.get_region("Uta Lower Road").add_exits({"Debious Woods Right", "Uta Road"})

    world.get_region("Debious Woods Right").add_exits({"Debious Woods Left", "Uta Lower Road"}, {
        "Debious Woods Left": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Debious Woods Left").add_exits({"Debious Woods Right", "Joma Marsh 2"}, {
        "Debious Woods Right": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Joma Marsh 2").add_exits({"Laruba Mansion Entrance", "Debious Woods Left"}, {
        "Laruba Mansion Entrance": Has("Laurels") | Has("Dracula's Ring", options=[OptionFilter(PoisonRing, True)]),
        "Debious Woods Left": Has("Laurels") | Has("Dracula's Ring", options=[OptionFilter(PoisonRing, True)]),
    })

    world.get_region("Joma Marsh 1").add_exits({"Camilla Cemetery", "Laruba Mansion Entrance"}, {
        "Laruba Mansion Entrance": Has("Laurels") | Has("Dracula's Ring", options=[OptionFilter(PoisonRing, True)]),
        "Camilla Cemetery": Has("Laurels") | Has("Dracula's Ring", options=[OptionFilter(PoisonRing, True)])
    })

    world.get_region("Laruba Mansion Entrance").add_exits({"Joma Marsh 1", "Laruba Mansion", "Joma Marsh 2"})

    world.get_region("Wicked Ditch").add_exits({"Bodley Mansion Entrance", "Town of Doina"})

    world.get_region("Town of Doina").add_exits({"Wicked Ditch", "North Bridge"})

    world.get_region("North Bridge").add_exits({"Town of Doina", "Dora Woods 1"}, {
        "Town of Doina": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False),
        "Dora Woods 1": Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)
    })

    world.get_region("Dora Woods 1").add_exits({"North Bridge", "Dora Woods 2"})
    world.get_region("Dora Woods 2").add_exits({"Dora Woods 1", "Dora Woods 3", "Town of Yomi"})
    world.get_region("Dora Woods 3").add_exits({"Dora Woods 2", "East Bridge"})

    world.get_region("East Bridge").add_exits({"Denis Marsh"})

    world.get_region("Town of Yomi").add_exits({"Dora Woods 3", "Vrad Graveyard"})

    world.get_region("Vrad Graveyard").add_exits({"Town of Yomi", "West Bridge"})

    world.get_region("West Bridge").add_exits({"Vrad Graveyard", "Castlevania"}, {
        "Castlevania": dracula_access_rule
    })
