from typing import List, Optional, NamedTuple, TYPE_CHECKING
from .static_location_data import location_ids

if TYPE_CHECKING:
    from . import PoRWorld


class LocationData(NamedTuple):
    region: str
    name: str
    is_event: Optional[bool] = False

def get_locations(world: "PoRWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Entrance - Hub", "Entrance: Drawbridge Pit Item"),
        LocationData("Entrance - Hub", "Entrance: Drawbridge Switch Item"),
        LocationData("Entrance - Hub", "Entrance: Drawbridge Upper Item"),
        LocationData("Entrance - Hub", "Entrance: First Passage Upper Item"),
        LocationData("Entrance - Hub", "Entrance: First Passage Lower Item"),
        LocationData("Entrance - Hub", "Entrance: First Passage Hidden Wall"),
        LocationData("Entrance - Hub", "Entrance: Hub Room"),
        LocationData("Entrance - Hub", "Entrance: Above Hub"),
        LocationData("Entrance - Hub", "Entrance: Statue Room Upper"),
        LocationData("Entrance - Hub", "Entrance: Statue Room Above Statue"),
        LocationData("Entrance - Hub", "Entrance: Behemoth Chase Room"),
        LocationData("Entrance - Hub", "Entrance: Double Room Lower"),
        LocationData("Entrance - Behemoth Area", "Entrance: Double Room Upper"),
        LocationData("Entrance - Behemoth Area", "Entrance: Pre-Behemoth Boss Room"),
        LocationData("Entrance - Behemoth Area", "Entrance: Right Hidden Room"),
        LocationData("Entrance - Upper Area", "Entrance: Lilith Room"),
        LocationData("Entrance - Upper Area", "Entrance: Above Metal Block Room"),
        LocationData("Entrance - Upper Area", "Entrance: Center Hidden Room"),
        LocationData("Entrance - Upper Area", "Entrance: Beyond Great Armor Hallway"),

        LocationData("Buried Chamber", "Buried Chamber: Westmost Room"),
        LocationData("Buried Chamber", "Buried Chamber: Central Secret"),
        LocationData("Buried Chamber", "Buried Chamber: West Shaft"),
        LocationData("Buried Chamber", "Buried Chamber: Central Hall"),
        LocationData("Buried Chamber", "Buried Chamber: Hidden Wall Item"),
        LocationData("Buried Chamber", "Buried Chamber: Right Secret"),
        LocationData("Buried Chamber", "Buried Chamber: Right Shade Hall"),
        LocationData("Buried Chamber", "Buried Chamber: Final Shaft Item"),
        LocationData("Buried Chamber", "Buried Chamber: Right Shaft Top"),
        LocationData("Buried Chamber", "Buried Chamber: Eastmost Room"),

        LocationData("Great Stairway - Lower", "Great Stairway: After Keremet Lower"),
        LocationData("Great Stairway - Lower", "Great Stairway: Before Keremet Room"),
        LocationData("Great Stairway - Central Painting Area", "Great Stairway: Left Loft"),
        LocationData("Great Stairway - Central Painting Area", "Great Stairway: Left Loft Lower"),
        LocationData("Great Stairway - Entrance Connector", "Great Stairway: Central NookDummy"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Upper Grand Staircase Corner Nook"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Upper Grand Staircase Middle Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Upper Grand Staircase Lower Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Upper Grand Staircase Upper Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Lower Grand Staircase Corner Nook"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Lower Grand Staircase Lower Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Lower Grand Staircase Middle Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Lower Grand Staircase Upper Alcove"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Upper Underground Room"),
        LocationData("Great Stairway - Staircases", "Great Stairway: After Keremet Upper"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Big Underground Room Upper"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Big Underground Room Hidden Item"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Big Underground Room Lower"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Underground Hidden Room"),
        LocationData("Great Stairway - Staircases", "Great Stairway: Underground East Room"),
        LocationData("Great Stairway - Upper", "Great Stairway: Connector Pipe Left"),
        LocationData("Great Stairway - Upper", "Great Stairway: Connector Pipe Right"),
        LocationData("Great Stairway - Upper", "Great Stairway: Upper Grand Staircase Top Left Item"),
        LocationData("Great Stairway - Upper", "Great Stairway: Central Upper"),
        LocationData("Great Stairway - Upper", "Great Stairway: Right Loft"),

        LocationData("Dummy", "Dummy"),
        
    ]

    return location_table