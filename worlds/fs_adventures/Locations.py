from typing import List, Optional, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from . import FSAdventuresWorld


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]


def get_locations(world: "FSAdventuresWorld") -> List[LocationData]:

    location_table: List[LocationData] = [
        LocationData("Lake Hylia", "Lake Hylia - Riverside Cave", 0x01),
        LocationData("Lake Hylia", "Lake Hylia - Riverbank Rock Circle", 0x02),
        LocationData("Lake Hylia", "Lake Hylia - Riverbank House Backyard", 0x03),
        LocationData("Lake Hylia", "Lake Hylia - Riverbank Floating Item", 0x04),
        LocationData("Lake Hylia", "Lake Hylia - Riverbank Underwater Item", 0x05),
        LocationData("Lake Hylia", "Lake Hylia - Riverbank Cave Chest", 0x06),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Lower Cave Floating Item", 0x07),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Lower Cave Chest", 0x08),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Upper Cave Floating Item", 0x09),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Upper Cave Pedestal", 0x0A),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Waterfall Item", 0x0B),
        LocationData("Lake Hylia", "Lake Hylia - Three Caves Left Chest", 0x0C),
        LocationData("Lake Hylia", "Lake Hylia - Three Caves Right Chest", 0x0D),
        LocationData("Lake Hylia", "Lake Hylia - Three Caves Under Waterfall", 0x0E),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Base Underwater", 0x0F),
        LocationData("Lake Hylia", "Lake Hylia - Pit Cave Floating Item", 0x10),
        LocationData("Lake Hylia", "Lake Hylia - N-Shaped Cave Left Chest", 0x11),
        LocationData("Lake Hylia", "Lake Hylia - N-Shaped Cave Right Chest", 0x12),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Base Cave Chest", 0x13),
        LocationData("Lake Hylia", "Lake Hylia - Waterfall Base Cave Pedestal", 0x14),
        LocationData("Lake Hylia", "Lake Hylia - Bridge Left Chest", 0x15),
        LocationData("Lake Hylia", "Lake Hylia - Bridge Right Chest", 0x16),
    ]

    return location_table
