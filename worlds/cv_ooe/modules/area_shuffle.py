from enum import IntEnum

from BaseClasses import EntranceType
from Utils import visualize_regions
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances

castle_entrances = [
    "Sec00Rm07",  # Castle entrance upper door -> Library
    "Sec01Rm03",  # Castle Entrance lower left door -> Underground Labyrinth
    "Sec01Rm07",  # Castle Entrance -> Shortcut into Barracks

    "Sec02Rm00",  # Underground Labyrinth Entrance -> Castle Entrance
    "Sec02Rm0E",  # Underground Labryinth Exit -> Barracks

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
    state = world.multiworld.get_all_state(False, allow_partial_entrances=True)
    state.update_reachable_regions(world.player)
    visualize_regions(world.get_region("Game Start"), "my_world.puml", show_entrance_names=True,
                      regions_to_highlight=state.reachable_regions[world.player])
    randomize_entrances(world, True, entrance_map)
