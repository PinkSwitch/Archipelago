from ..Options import PortraitShuffle
from typing import NamedTuple


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


def portrait_shuffle(world) -> None:
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
        
