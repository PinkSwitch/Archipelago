from ..Options import PortraitShuffle
from typing import NamedTuple
import struct


class PortraitData(NamedTuple):
    destination_pointer: list[int | str]  # Pointer, file
    destination_map: int  # Which map this leads you to
    destination_room: int  # Which room you land in
    spoiler_map_name: str = "None"


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
        "13th Street": "13th Street",
        "Forgotten City": "Forgotten City",
        "Burnt Paradise": "Burnt Paradise",
        "Dark Academy": "Dark Academy",
        "Nest of Evil": "Nest of Evil"
    }

    if world.options.portrait_shuffle:
        portrait_pool = list(world.portrait_connections.values())
        world.random.shuffle(portrait_pool)
        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            portrait_pool.remove("Nest of Evil")

        world.portrait_connections = dict(zip(world.portrait_connections, portrait_pool))

        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            world.portrait_connections["Nest of Evil"] = "Nest of Evil"  # Set this back to normal
        

def write_portrait_data(world, rom) -> None:
    #  It would be too easy to break logic with the Shortcut portraits, so just remove them
    #  13th Street
    rom.write_to_file(0x022FF324, "overlay_106", bytearray([0x00]))
    rom.write_to_file(0x022FF33C, "overlay_106", bytearray([0x00]))
    rom.write_to_file(0x022FF348, "overlay_106", bytearray([0x00]))
    #  Forgotten City
    rom.write_to_file(0x02304714, "overlay_103", bytearray([0x00]))
    rom.write_to_file(0x02304720, "overlay_103", bytearray([0x00]))
    rom.write_to_file(0x0230472C, "overlay_103", bytearray([0x00]))
    #  Burnt Paradise
    rom.write_to_file(0x023037C4, "overlay_107", bytearray([0x00]))
    rom.write_to_file(0x023037D0, "overlay_107", bytearray([0x00]))
    rom.write_to_file(0x023037E8, "overlay_107", bytearray([0x00]))
    #  Dark Academy
    rom.write_to_file(0x022F62B8, "overlay_109", bytearray([0x00]))
    rom.write_to_file(0x022F62C4, "overlay_109", bytearray([0x00]))
    rom.write_to_file(0x022F62D0, "overlay_109", bytearray([0x00]))

    # Variable used to check which Portrait is used for the Stella's Locket scene
    rom.write_to_file(0x0230917B, "overlay_119", bytearray([portrait_data[world.portrait_connections["Forest of Doom"]].destination_map]))

    for portrait in world.portrait_connections:
        destination = world.portrait_connections[portrait]
        data = portrait_data[destination]
        return_data = portrait_data[portrait]
        if destination in ["13th Street", "Forgotten City", "Burnt Paradise", "Dark Academy"]:
            frame = 0x76
        elif destination == "Nest of Evil":
            frame = 0x86
        else:  # City of Haze, Sandy Grave, Nation of Fools, Forest of Doom
            frame = 0x1A
        area = data.destination_map
        room = data.destination_room
        address = data.destination_pointer[0]
        file = data.destination_pointer[1]
        #  Write the shuffled portraits into the game
        rom.write_to_file(address + 6, file, bytearray([frame]))
        rom.write_to_file(address + 8, file, struct.pack("H", area))  # Portrait Area
        rom.write_to_file(address + 10, file, struct.pack("H", room))  # Portrait room
        #  Write the return portraits as well
        area = return_data.destination_room
        room = return_data.destination_room
        address = return_data.destination_pointer[0]
        file = return_data.destination_pointer[1]
        rom.write_to_file(address + 8, file, struct.pack("H", area))  # Portrait Area
        rom.write_to_file(address + 10, file, struct.pack("H", room))  # Portrait room

    #  Write the shortcuts used at the end of the Remix portraits
    for obj in remix_shortcuts:
        data = portrait_data[obj]
        portrait = remix_shortcuts[obj]
        rom.write_to_file(portrait[0] + 10, portrait[1], struct.pack("H", data.destination_room))
