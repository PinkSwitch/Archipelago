from typing import TYPE_CHECKING, Optional, NamedTuple, List

if TYPE_CHECKING:
    from . import OoEWorld


class LocationData(NamedTuple):
    region: str
    name: str
    is_event: Optional[bool] = False


def get_locations(world: "OoEWorld") -> List[LocationData]:
    location_table: List[LocationData] = [
        LocationData("Entrance - Hub", "Entrance: Drawbridge Pit Item"),
    ]

    return location_table