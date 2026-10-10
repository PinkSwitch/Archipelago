from enum import IntEnum
from typing import NamedTuple
import struct

from BaseClasses import EntranceType
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances


class DoorTransitionData(NamedTuple):
    source_pointer: int  # Pointer to this door's data field
    room_pointer: int  # Pointer to which room this door belongs to
    x_pos: int  # X-Position of this door
    y_pos: int  # Y-Position of this door
    entrance_name: str
    is_left_facing: bool = False


castle_entrances = [
    "Sec01Rm14",  # Entrance -> Stairway (Upper)
    "Sec00Rm0B",  # Entrance -> Stairway (Metal Block)
    "Sec00Rm0A",  # Entrance -> Buried Chamber

    "Sec02Rm03",  # Buried Chamber -> Entrance
    "Sec02Rm1C",  # Buried Chamber -> Stairway

    "Sec03Rm06",  # Stairway -> Buried Chamber
    "Sec03Rm00",  # Stairway -> Entrance (Lower)
    "Sec06Rm00",  # Stairway -> Entrance (Higher)
    "Sec06Rm0C",  # Stairway -> Tower (Toad Hole)
    "Sec03Rm0C",  # Stairway -> Tower (Push Block)

    "Sec07Rm17",  # Tower -> Stairway (Base)
    "Sec07Rm1B",  # Tower -> Keep (Elevator bottom floor)
    "Sec07Rm19",  # Tower -> Keep (Elevator middle floor)
    "Sec08Rm0A",  # Tower -> Stairway (Waterwheel left)
    "Sec08Rm07",  # Tower -> Keep (Waterwheel right)

    "Sec0BRm03",  # Keep -> Tower (Bridge left)
    "Sec0BRm05",  # Keep -> Tower (Bridge Right)
    "Sec0ARm13"  # Keep -> Tower (Main Entrance
]

door_data = {
    "Sec01Rm14": DoorTransitionData(0x020E5558, 0x020E5568, 0x00, 0x00, "Entrance: Upper East Door", True),
    "Sec00Rm0B": DoorTransitionData(0x020E4E50, 0x020E4E60, 0x00, 0x00, "Entrance: Iron Block Door", True),
    "Sec00Rm0A": DoorTransitionData(0x020E4DF0, 0x020E4DA0, 0x00, 0x240, "Entrance: Lower Post-Behemoth Door"),

    "Sec02Rm03": DoorTransitionData(0x020E57C0, 0x020E57D0, 0x00, 0x00, "Buried Chamber: West Door", True),
    "Sec02Rm1C": DoorTransitionData(0x020E5D10, 0x020E5D30, 0x00, 0x00, "Buried Chamber: East Door"),

    "Sec03Rm06": DoorTransitionData(0x020E5D60, 0x020E5D70, 0x00, 0x00, "Great Stairway: Lower East Door", True),
    "Sec03Rm00": DoorTransitionData(0x020E5E10, 0x020E5DF0, 0x00, 0xC0, "Great Stairway: Lower West Door"),
    "Sec06Rm00": DoorTransitionData(0x020E69C8, 0x020E69E8, 0x00, 0x00, "Great Stairway: Ramparts West Door"),
    "Sec06Rm0C": DoorTransitionData(0x020E6D48, 0x020E6D38, 0x00, 0x00, "Great Stairway: Pipe Door", True),
    "Sec03Rm0C": DoorTransitionData(0x020E6180, 0x020E6190, 0x00, 0x00, "Great Stairway: Push Block Door", True),

    "Sec07Rm17": DoorTransitionData(0x020E7418, 0x020E7438, 0x00, 0x00, "Tower of Death: Tower Base Door"),
    "Sec07Rm1B": DoorTransitionData(0x020E7518, 0x020E7538, 0x00, 0x00, "Tower of Death: Elevator Bottom Floor Door"),
    "Sec07Rm19": DoorTransitionData(0x020E7498, 0x020E74B8, 0x00, 0x00, "Tower of Death: Elevator Middle Floor Door"),
    "Sec08Rm0A": DoorTransitionData(0x020E7870, 0x020E7890, 0x00, 0x00, "Tower of Death: Belt Area West Door"),
    "Sec08Rm07": DoorTransitionData(0x020E7820, 0x020E7830, 0x00, 0x00, "Tower of Death: Belt Area East Door", True),

    "Sec0BRm03": DoorTransitionData(0x020E8430, 0x020E8450, 0x00, 0x00, "Master's Keep: Bridge West Door"),
    "Sec0BRm05": DoorTransitionData(0x020E74E8, 0x020E74F8, 0x00, 0x00, "Master's Keep: Bridge East Door", True),
    "Sec0ARm13": DoorTransitionData(0x020E7468, 0x020E7478, 0x00, 0x00, "Master's Keep: Main Entrance Door", True)
}


class DoorOrientation(IntEnum):
    # Directions
    Left = 1
    Right = 2


entrance_map: dict[int, list[int]] = {
  DoorOrientation.Left: [DoorOrientation.Right],  # Left-facing Doors
  DoorOrientation.Right: [DoorOrientation.Left]   # Right-facing doors
}


def shuffle_doors(world):
    for connection_room in castle_entrances:
        entrance = world.get_entrance(connection_room)
        entrance.randomization_type = EntranceType.TWO_WAY
        if door_data[connection_room].is_left_facing:
            entrance.randomization_group = DoorOrientation.Left
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Left)
        else:
            entrance.randomization_group = DoorOrientation.Right
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Right)
    world.connected_doors = randomize_entrances(world, True, entrance_map).pairings


def patch_castle_connections(world, rom):
    for door in world.connected_doors:
        source = door[0]
        destination = door[1]
        address = door_data[source].source_pointer
        des_pointer = door_data[destination].room_pointer

        rom.write_to_file(address, "arm9", struct.pack("I", des_pointer))
        rom.write_to_file(address + 0x0A, "arm9", struct.pack("H", door_data[destination].x_pos))
        rom.write_to_file(address + 0x0C, "arm9", struct.pack("H", door_data[destination].y_pos))


exit_regions = {
    "Sec01Rm14": "Entrance - Upper Area",
    "Sec00Rm0B": "Entrance - Iron Block Door",
    "Sec00Rm0A": "Entrance - Post Behemoth",

    "Sec02Rm03": "Buried Chamber",
    "Sec02Rm1C": "Buried Chamber",

    "Sec03Rm06": "Great Stairway - Lower",
    "Sec03Rm00": "Great Stairway - Lower",
    "Sec06Rm00": "Great Stairway - Entrance Connector",
    "Sec06Rm0C": "Great Stairway - Pipe Door",
    "Sec03Rm0C": "Great Stairway - Push Block Door",

    "Sec07Rm17": "Tower of Death - Bottom",
    "Sec07Rm1B": "Tower of Death - Elevator Room",
    "Sec07Rm19": "Tower of Death - Elevator Exit",
    "Sec08Rm0A": "Tower of Death - Belt Area",
    "Sec08Rm07": "Tower of Death - Belt Area",

    "Sec0BRm03": "Master's Keep - Bridge",
    "Sec0BRm05": "Master's Keep - Bridge",
    "Sec0ARm13": "Master's Keep - Lower"
}


def set_ut_regions(world):
    for door in world.connected_doors:
        world.get_entrance(door[0]).connected_region = world.get_region(exit_regions[door[1]])
