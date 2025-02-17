from dataclasses import dataclass
import dataclasses



@dataclass
class EBDungeonDoor:
    address: int
    destination_y: int
    destination_x: int
    exit_type: int


def shuffle_dungeons(world):
    # Is the dept. store a dungeon
    single_exit_dungeons = [
        "Giant Step",
        "Happy-Happy HQ",
        "Lilliput Steps",
        "Milky Well",
        "Gold Mine",
        "Moonside",
        "Monkey Caves",
        "Monotoli Building",
        "Magnet Hill",
        "Pink Cloud",
        "Dungeon Man",
        "Stonehenge Base",
        "Lumine Hall",
        "Fire Spring",
        "Sea of Eden"
    ]

    double_exit_dungeons = [
        "Arcade",
        "Brickroad Maze",
        "Rainy Circle",
        "Belch's Factory",
        "Pyramid"
        ]

    world.dungeon_connections = {
        "Arcade": "Arcade",
        "Giant Step": "Giant Step",
        "Happy-Happy HQ": "Happy-Happy HQ",
        "Lilliput Steps": "Lilliput Steps",
        "Belch's Factory": "Belch's Factory",
        "Milky Well": "Milky Well",
        "Gold Mine": "Gold Mine",
        "Moonside": "Moonside",
        "Monkey Caves": "Monkey Caves",
        "Monotoli Building": "Monotoli Building",
        "Magnet Hill": "Magnet Hill",
        "Pink Cloud": "Pink Cloud",
        "Dungeon Man": "Dungeon Man",
        "Stonehenge Base": "Stonehenge Base",
        "Brickroad Maze": "Brickroad Maze",
        "Rainy Circle": "Rainy Circle",
        "Pyramid": "Pyramid",
        "Lumine Hall": "Lumine Hall",
        "Fire Spring": "Fire Spring",
        "Sea of Eden": "Sea of Eden"
    }
    
    if world.options.magicant_mode:
        # Don't shuffle Magicant when it's important
        single_exit_dungeons.remove("Sea of Eden")

    shuffled_single_dungeons = single_exit_dungeons.copy()
    shuffled_double_dungeons = double_exit_dungeons.copy()

    if world.options.dungeon_shuffle:
        world.random.shuffle(shuffled_single_dungeons)
        world.random.shuffle(shuffled_double_dungeons)

    for index, entrance in enumerate(single_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_single_dungeons[index]

    for index, entrance in enumerate(double_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_double_dungeons[index]
    
def write_dungeon_entrances(world, rom):
    # 4 bytes of script pointer
    # 2 byte flag lock
    # 2 byte Y
    # 2 byte X
    # 1 byte style
    dungeon_entrances = {
        "Arcade": ["Arcade Entrance", "Arcade Exit", "Arcade Back Exit", "Arcade Back Entrance"],
        "Giant Step": ["Giant Step Entrance", "Giant Step Exit"],
        "Happy-Happy HQ": ["Happy-Happy HQ Entrance", "Happy-Happy HQ Exit"],
        "Lilliput Steps": ["Lilliput Steps Entrance", "Lilliput Steps Exit"],
        "Belch's Factory": ["Factory Entrance", "Factory Exit", "Factory Back Exit", "Factory Back Entrance"],
        "Milky Well": ["Milky Well Entrance", "Milky Well Exit"],
        "Gold Mine": ["Mine Entrance", "Mine Exit"],
        "Monkey Caves": ["Monkey Entrance", "Monkey Exit"],
        "Monotoli Building": [],
        "Moonside": [],
        "Brickroad Maze": [],
        "Rainy Circle": [],
        "Magnet Hill": [],
        "Pink Cloud": [],
        "Pyramid": [],
        "Dungeon Man": [],
        "Stonehenge Base": [],
        "Lumine Hall": [],
        "Fire Spring": ["Fire Spring Entrance", "Fire Spring Exit"],
        "Sea of Eden": []
    }

    all_dungeon_doors = {
        "Arcade Entrance": EBDungeonDoor(0x0F00CC, 0xC059, 0x03E4, 0x03),
        "Arcade Exit": EBDungeonDoor(0x0F029A, 0x00DA, 0x00C5, 0x0C),
        "Arcade Back Exit": EBDungeonDoor(0x0F026E, 0x40D1, 0x00C5, 0x0A),
        "Arcade Back Entrance": EBDungeonDoor(0x0F00C1, 0x0056, 0x03D1, 0x04),
        "Giant Step Entrance": EBDungeonDoor(0x0F0032, 0x0158, 0xC434, 0x01),
        "Giant Step Exit": EBDungeonDoor(0x0F04B5, 0x003F, 0x00B1, 0x01),
        "Happy-Happy HQ Entrance": EBDungeonDoor(0x0F09E9, 0xC122, 0x03F1, 0x04),
        "Happy-Happy HQ Exit": EBDungeonDoor(0x0F0A99, 0x03DC, 0x01DF, 0x0A),
        "Lilliput Steps Entrance": EBDungeonDoor(0x0F09F4, 0x80D1, 0x0187, 0x01),
        "Lilliput Steps Exit": EBDungeonDoor(0x0F0B1A, 0xC3C4, 0x020C, 0x01),
        "Factory Entrance": EBDungeonDoor(0x0F1277, 0x0021, 0x031C, 0x01),
        # Factory Script Warp: EBDungeonDoor()
        "Factory Exit": EBDungeonDoor(0x0F1159, 0x0021, 0x031C, 0x01),
        "Factory Back Exit": EBDungeonDoor(0x0F11BC, 0x8379, 0x03A3, 0x01),
        "Factory Back Entrance": EBDungeonDoor(0x0F11FE, 0x024F, 0x022E, 0x01),
        "Milky Well Entrance": EBDungeonDoor(0x0F12E9, 0x8279, 0x0383, 0x01),
        "Milky Well Exit": EBDungeonDoor(0x0F11E8, 0x0391, 0x0045, 0x01),
        "Mine Entrance": EBDungeonDoor(0x0F1378, 0xC35A, 0x03F8, 0x01),
        "Mine Exit": EBDungeonDoor(0x0F1400, 0x84B4, 0x01CC, 0x01),
        "Monkey Entrance": EBDungeonDoor(0x0F1458, 0xC2A9, 0x0310, 0x01),
        "Monkey Exit": EBDungeonDoor(0x0F1513, 0x8299, 0x0383, 0x01),
        "Fire Spring Entrance": EBDungeonDoor(0x0F23D4, 0x8351, 0x0167, 0x01),
        "Fire Spring Exit": EBDungeonDoor(0x0F2437, 0x0183, 0x00EA, 0x01),
    }

    for dungeon in world.dungeon_connections:
        destination = world.dungeon_connections[dungeon]
        for index, entrance in enumerate(dungeon_entrances[dungeon]):
            door = all_dungeon_doors[entrance]
            dest_door = dungeon_entrances[destination]
            print(dest_door[index])

    print(world.dungeon_connections)