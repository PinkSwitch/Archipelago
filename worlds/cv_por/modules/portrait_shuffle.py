from ..Options import PortraitShuffle
from typing import NamedTuple
from dataclasses import dataclass
import struct


class PortraitData(NamedTuple):
    destination_pointer: list[int | str]  # Pointer, file
    destination_map: int  # Which map this leads you to
    destination_room: int  # Which room you land in
    spoiler_map_name: str = "None"


area_map = [
    "City of Haze",
    "13th Street",
    "Sandy Grave",
    "Forgotten City",
    "Nation of Fools",
    "Burnt Paradise",
    "Forest of Doom",
    "Dark Academy",
    "Nest of Evil"
]

sprite_order = [
    "City of Haze",
    "Sandy Grave",
    "Nation of Fools",
    "Forest of Doom",
    "13th Street",
    "Forgotten City",
    "Burnt Paradise",
    "Dark Academy",
    "Nest of Evil"
]

palette_order = [
    "City of Haze",
    "Sandy Grave",
    "Forest of Doom",
    "Nation of Fools",
    "13th Street",
    "Forgotten City",
    "Dark Academy",
    "Burnt Paradise",
    "Nest of Evil"
]


portrait_data = {
    "City of Haze": PortraitData([0x02304A44, "overlay_79"], 0x01, 0x1A, "Hub Portrait"),
    "Sandy Grave": PortraitData([0x022FAF58, "overlay_82"], 0x03, 0x00, "Great Stairway Underground Portrait"),
    "Nation of Fools": PortraitData([0x022F875C, "overlay_84"], 0x05, 0x21, "Great Stairway Central Portrait"),
    "Forest of Doom": PortraitData([0x022FC278, "overlay_86"], 0x07, 0x00, "Tower Portrait"),
    "Forgotten City": PortraitData([0x022F1F4C, "overlay_89"], 0x04, 0x00, "Brauner Portrait 1"),
    "13th Street": PortraitData([0x022F1F58, "overlay_89"], 0x02, 0x07, "Brauner Portrait 2"),
    "Burnt Paradise": PortraitData([0x022F1F64, "overlay_89"], 0x06, 0x20, "Brauner Portrait 3"),
    "Dark Academy": PortraitData([0x022F1F70, "overlay_89"], 0x08, 0x46, "Brauner Portrait 4"),
    "Nest of Evil": PortraitData([0x022F9194, "overlay_78"], 0x09, 0x00, "Secret Passage Portrait")
}

return_portraits = {
    "City of Haze": PortraitData([0x02301E14, "overlay_93"], 0x00, 0x40),
    "Sandy Grave": PortraitData([0x02306F30, "overlay_91"], 0x00, 0x112),
    "Nation of Fools": PortraitData([0x023006C0, "overlay_96"], 0x00, 0x181),
    "Forest of Doom": PortraitData([0x022FAEE0, "overlay_99"], 0x00, 0x201),
    "Forgotten City": PortraitData([0x0230881C, "overlay_102"], 0x00, 0x02C0),
    "13th Street": PortraitData([0x022F3C58, "overlay_104"], 0x00, 0x02C0),
    "Burnt Paradise": PortraitData([0x02303C5C, "overlay_107"], 0x00, 0x02C0),
    "Dark Academy": PortraitData([0x022F2654, "overlay_110"], 0x00, 0x02C0),
    "Nest of Evil": PortraitData([0x022ED9A0, "overlay_113"], 0x00, 0x05)
}

remix_shortcuts = {
    "Forgotten City": [0x02304708, "overlay_103"],
    "13th Street": [0x022FF33C, "overlay_106"],
    "Burnt Paradise": [0x023037DC, "overlay_107"],
    "Dark Academy": [0x022F62DC, "overlay_109"]
}


def portrait_shuffle(world) -> None:
    if world.portrait_connections:
        return
    world.portrait_connections = {
        "City of Haze": "City of Haze",
        "Sandy Grave": "Sandy Grave",
        "Nation of Fools": "Nation of Fools",
        "Forest of Doom": "Forest of Doom",
        "Forgotten City": "Forgotten City",
        "13th Street": "13th Street",
        "Burnt Paradise": "Burnt Paradise",
        "Dark Academy": "Dark Academy",
        "Nest of Evil": "Nest of Evil"
    }

    if world.options.portrait_shuffle:
        portrait_pool = list(world.portrait_connections.values())
        world.random.shuffle(portrait_pool)
        while portrait_pool.index("Nest of Evil") in [5, 7]:
            world.random.shuffle(portrait_pool)  # Nest doesn't have a boss room, so if it's a Lock we need to remove it

        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            portrait_pool.remove("Nest of Evil")

        world.portrait_connections = dict(zip(world.portrait_connections, portrait_pool))

        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            world.portrait_connections["Nest of Evil"] = "Nest of Evil"  # Set this back to normal
        

def write_portrait_data(world, rom) -> None:
    #  It would be too easy to break logic with the Shortcut portraits, so just remove them
    #  13th Street
    rom.write_to_file(0x022FF329, "overlay_106", bytearray([0x00]))
    rom.write_to_file(0x022FF341, "overlay_106", bytearray([0x00]))
    rom.write_to_file(0x022FF34D, "overlay_106", bytearray([0x00]))
    #  Forgotten City
    rom.write_to_file(0x02304719, "overlay_103", bytearray([0x00]))
    rom.write_to_file(0x02304725, "overlay_103", bytearray([0x00]))
    rom.write_to_file(0x02304731, "overlay_103", bytearray([0x00]))
    #  Burnt Paradise
    rom.write_to_file(0x023037C9, "overlay_107", bytearray([0x00]))
    rom.write_to_file(0x023037D5, "overlay_107", bytearray([0x00]))
    rom.write_to_file(0x023037ED, "overlay_107", bytearray([0x00]))
    #  Dark Academy
    rom.write_to_file(0x022F62BD, "overlay_109", bytearray([0x00]))
    rom.write_to_file(0x022F62C9, "overlay_109", bytearray([0x00]))
    rom.write_to_file(0x022F62D5, "overlay_109", bytearray([0x00]))

    # Variable used to check which Portrait is used for the Stella's Locket scene
    rom.write_to_file(0x0230917B, "overlay_119", bytearray([portrait_data[world.portrait_connections["Forest of Doom"]].destination_map]))

    #  The two locked portraits in the Gallery. Write what they are so we know which ones to check
    rom.write_to_file(0x0230917D, "overlay_119", bytearray([portrait_data[world.portrait_connections["13th Street"]].destination_map]))
    rom.write_to_file(0x0230917E, "overlay_119", bytearray([portrait_data[world.portrait_connections["Burnt Paradise"]].destination_map]))

    # List of brauner portraits in order. Used for determining return position
    rom.write_to_file(0x0230917F, "overlay_119", bytearray([portrait_data[world.portrait_connections["Forgotten City"]].destination_map]))
    rom.write_to_file(0x02309180, "overlay_119", bytearray([portrait_data[world.portrait_connections["13th Street"]].destination_map]))
    rom.write_to_file(0x02309181, "overlay_119", bytearray([portrait_data[world.portrait_connections["Burnt Paradise"]].destination_map]))
    rom.write_to_file(0x02309182, "overlay_119", bytearray([portrait_data[world.portrait_connections["Dark Academy"]].destination_map]))

    for portrait in world.portrait_connections:
        destination = world.portrait_connections[portrait]
        source = portrait_data[destination]
        data = portrait_data[portrait]

        return_data = return_portraits[portrait]
        return_address = return_portraits[destination]
        area = source.destination_map
        room = source.destination_room
        address = data.destination_pointer[0]
        file = data.destination_pointer[1]
        #  Write the shuffled portraits into the game
        rom.write_to_file(address + 8, file, struct.pack("H", area))  # Portrait Area
        rom.write_to_file(address + 10, file, bytearray([room]))  # Portrait room
        #  Write the return portraits as well

        room = return_data.destination_room
        address = return_address.destination_pointer[0]
        file = return_address.destination_pointer[1]
        rom.write_to_file(address + 10, file, struct.pack("H", room))  # Portrait room

    #  Write the shortcuts used at the end of the Remix portraits
    for obj in remix_shortcuts:
        data = portrait_data[obj]
        portrait = remix_shortcuts[obj]
        rom.write_to_file(portrait[0] + 10, portrait[1], struct.pack("H", data.destination_room))


def adjust_portrait_gfx(rom):
    @dataclass
    class PortraitGFX:
        sprite: list
        palette: list
        destination_map: int = 0

    portraits = {
        "City of Haze": PortraitGFX([], []),
        "Sandy Grave": PortraitGFX([], []),
        "Nation of Fools": PortraitGFX([], []),
        "Forest of Doom": PortraitGFX([], []),
        "13th Street": PortraitGFX([], []),
        "Forgotten City": PortraitGFX([], []),
        "Burnt Paradise": PortraitGFX([], []),
        "Dark Academy": PortraitGFX([], []),
        "Nest of Evil": PortraitGFX([], [])
    }

    #  Read the regular portraits
    for i in range(4):
        portrait = portraits[sprite_order[i]]
        sprite_start = (i // 2) * 0x2000  # The bottom portraits are 0x2000 bytes down
        for j in range(62):  # Portraits are 62 pixels tall
            address = 0x89 + sprite_start  # Read the start of the sprite
            address += (0x40 * (i % 2))  # Make sure we read the correct painting
            address += (0x80 * j)  # Each row is 0x80 bytes apart
            portrait.sprite.append(rom.read_from_file(address, "portrait_set_1", 0x2E))

    #  Also read the Remix portraits
    for i in range(4):
        portrait = portraits[sprite_order[i + 4]]
        sprite_start = (i // 2) * 0x2000  # The bottom portraits are 0x2000 bytes down
        for j in range(62):  # Portraits are 62 pixels tall
            address = 0x89 + sprite_start  # Read the start of the sprite
            address += (0x40 * (i % 2))  # Make sure we read the correct painting
            address += (0x80 * j)  # Each row is 0x80 bytes apart
            portrait.sprite.append(rom.read_from_file(address, "portrait_set_2", 0x2E))

    for i in range(62):  # Nest of evil is the only portrait we need out of Set 3
        portraits["Nest of Evil"].sprite.append(rom.read_from_file(0xC9 + (0x80 * i), "portrait_set_3", 0x2E))

    #  Read all of the shuffled Portrait destinations
    for portrait in portraits:
        destination = portrait_data[portrait].destination_pointer
        new_map = rom.read_from_file(destination[0] + 8, destination[1], 1)[0]
        portraits[portrait].destination_map = new_map

    for index, portrait in enumerate(portraits):
        destination = portraits[portrait].destination_map
        destination = area_map[destination - 1]
        sprite = portraits[destination].sprite
        if index == 8:
            index = 9  # Bump up Nest because we skip over the real portrait 9
        for row in sprite:
            for i, pixel in enumerate(row):
                if index % 2:
                    row[i] = pixel | 0x80
                else:
                    row[i] = pixel & 0x7F

    for i in range(4):
        portrait = sprite_order[i]
        destination = portraits[portrait].destination_map
        destination = area_map[destination - 1]
        new_portrait = portraits[destination].sprite

        sprite_start = (i // 2) * 0x2000
        for j in range(62):
            address = 0x89 + sprite_start
            address += (0x40 * (i % 2))
            address += (0x80 * j)
            rom.write_to_file(address, "portrait_set_1", new_portrait[j])

    for i in range(4):
        portrait = sprite_order[i + 4]
        destination = portraits[portrait].destination_map
        destination = area_map[destination - 1]
        new_portrait = portraits[destination].sprite
        
        sprite_start = (i // 2) * 0x2000
        for j in range(62):
            address = 0x89 + sprite_start
            address += (0x40 * (i % 2))
            address += (0x80 * j)
            rom.write_to_file(address, "portrait_set_2", new_portrait[j])

    nest_destination = portraits["Nest of Evil"].destination_map
    nest_portrait = area_map[nest_destination - 1]
    nest_portrait_sprite = portraits[nest_portrait].sprite
    for i in range(62):  # Nest of evil is the only portrait we need out of Set 3
        rom.write_to_file(0xC9 + (0x80 * i), "portrait_set_3", nest_portrait_sprite[i])

    for i in range(8):
        portrait = palette_order[i]
        portraits[portrait].palette.append(rom.read_from_file(
            (0x22BD6C4 + (0x3028 * (i // 4))) + (0x100 * (i % 4)), "overlay_7", 0x100))

    portraits["Nest of Evil"].palette.append(rom.read_from_file(0x022C0BF0, "overlay_7", 0x100))  # Nest of evil

    for i in range(8):
        base = sprite_order[i]
        portrait = portraits[base].destination_map
        new_map = area_map[portrait - 1]
        new_palette = portraits[new_map].palette[0]
        rom.write_to_file((0x22BD6C4 + (0x3028 * (i // 4))) + (0x100 * (i % 4)), "overlay_7", new_palette)

    palette = portraits[nest_portrait].palette
    rom.write_to_file(0x022C0BF0, "overlay_7", palette[0])
