from typing import List, Optional, NamedTuple, TYPE_CHECKING
from .static_location_data import location_ids

if TYPE_CHECKING:
    from . import PoRWorld


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]

def get_locations(world: "DoSWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        #LocationData("Lost Village Upper", "Lost Village: Above Entrance", 0x01)
    ]

    return location_table