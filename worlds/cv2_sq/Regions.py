from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .Locations import get_locations
from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation, OptionFilter

if TYPE_CHECKING:
    from . import CV2World


class OoELocation(Location):
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

    "Uta Lower Road 1",
    "Uta Lower Road 2",

    "Debious Woods",

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