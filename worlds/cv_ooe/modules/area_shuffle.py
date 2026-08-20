from enum import IntEnum
from typing import NamedTuple
import struct

from BaseClasses import EntranceType
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances

castle_entrances = [
    "Sec00Rm07",  # Castle entrance upper door -> Library
    "Sec01Rm03",  # Castle Entrance lower left door -> Underground Labyrinth
    "Sec01Rm07",  # Castle Entrance -> Shortcut into Barracks

    "Sec02Rm00",  # Underground Labyrinth Entrance -> Castle Entrance
    "Sec02Rm0E",  # Underground Labyrinth Exit -> Barracks

    "Sec05Rm04",  # Barracks bottom -> Underground labyrinth right
    "Sec05Rm03",  # Barracks Left -> Castle Entrance Shortcut
    "Sec05Rm11",  # Barracks Right -> Mechanical Tower Center

    "Sec07Rm01",  # Mechanical Tower Center Door -> Barracks
    "Sec06Rm01",  # Mechanical Tower Bottom -> Arms Depot
    "Sec06Rm0B",  # Mechanical Tower Top -> Forsaken Cloister East

    "Sec08Rm02",  # Arms Depot -> Mechanical Tower Bottom

    "Sec03Rm00",  # Library -> Entrance
    "Sec03Rm0B",  # Library -> Final Approach Shortcut
    "Sec03Rm10",  # Library -> Forsaken Cloister West

    "Sec09Rm03",  # Forsaken Cloister West -> Library
    "Sec09Rm07",  # Forsaken Cloister East -> Mechanical Tower

    "Sec0ARm01"  # Final Approach -> Library

]

left_facing_doors = {  # Left facing doors are doors that the player ENTERS WALKING FROM THE LEFT
    "Sec00Rm07",
    "Sec01Rm07",
    "Sec01Rm03",
    "Sec02Rm0E",
    "Sec05Rm11",
    "Sec08Rm02",
    "Sec03Rm0B",
    "Sec03Rm10",
    "Sec09Rm07"
}

entrance_names = {
    "Sec00Rm07": "Castle Entrance: Upper Door",
    "Sec01Rm03": "Castle Entrance: Lower Door",
    "Sec01Rm07": "Castle Entrance: Shortcut Door",
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
        if connection_room in left_facing_doors:
            entrance.randomization_group = DoorOrientation.Left
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Left)
        else:
            entrance.randomization_group = DoorOrientation.Right
            disconnect_entrance_for_randomization(entrance, DoorOrientation.Right)
    world.connected_doors = randomize_entrances(world, True, entrance_map).pairings


class DoorTransitionData(NamedTuple):
    source_pointer: int  # Pointer to this door's data field in Overlay 22.
    room_pointer: int  # Pointer to which room this door belongs to
    x_pos: int  # X-Position of this door
    y_pos: int  # Y-Position of this door


door_data = {
    "Sec00Rm07": DoorTransitionData(0x022ABC70, 0x022ABC80, 0x00, 0x00),
    "Sec03Rm00": DoorTransitionData(0x022ACB70, 0x022ACB80, 0x00, 0x180),

    "Sec01Rm03": DoorTransitionData(0x022ABEE0, 0x022ABEF0, 0x00, 0x00),
    "Sec02Rm00": DoorTransitionData(0x022AC2D8, 0x022AC2B8, 0x00, 0x00),

    "Sec02Rm0E": DoorTransitionData(0x022AD578, 0x022AD588, 0x00, 0x00),
    "Sec05Rm04": DoorTransitionData(0x022AD528, 0x022AD4E8, 0x00, 0x0180),

    "Sec01Rm07": DoorTransitionData(0x022AD458, 0x022AD468, 0x00, 0x00),
    "Sec05Rm03": DoorTransitionData(0x022AD4B8, 0x022AD488, 0x100, 0x00),

    "Sec05Rm11": DoorTransitionData(0x022AE108, 0x022AE118, 0x00, 0x00),
    "Sec07Rm01": DoorTransitionData(0x022AE138, 0x022AE158, 0x100, 0x00),

    "Sec03Rm0B": DoorTransitionData(0x022AE358, 0x022AE368, 0x100, 0x00),
    "Sec0ARm01": DoorTransitionData(0x022AE388, 0x022AE3A8, 0x00, 0x00),

    "Sec09Rm07": DoorTransitionData(0x022AF1B8, 0x022AF1C8, 0x00, 0x00),
    "Sec06Rm0B": DoorTransitionData(0x022ADC38, 0x022ADC58, 0x00, 0x00),

    "Sec08Rm02": DoorTransitionData(0x022AD978, 0x022AD988, 0x00, 0x00),
    "Sec06Rm01": DoorTransitionData(0x022AD9A8, 0x022AD9C8, 0x00, 0x00),

    "Sec03Rm10": DoorTransitionData(0x022AF028, 0x022ACF80, 0x00, 0x0180),
    "Sec09Rm03": DoorTransitionData(0x022AF018, 0x022AF078, 0x00, 0x00)
}


def patch_castle_connections(world, rom):
    for door in world.connected_doors:
        source = door[0]
        destination = door[1]
        address = door_data[source].source_pointer
        des_pointer = door_data[destination].room_pointer

        rom.write_to_file(address, "overlay_22", struct.pack("I", des_pointer))
        rom.write_to_file(address + 0x0A, "overlay_22", struct.pack("H", door_data[destination].x_pos))
        rom.write_to_file(address + 0x0C, "overlay_22", struct.pack("H", door_data[destination].y_pos))
        print(f"{source} Links to {destination}")