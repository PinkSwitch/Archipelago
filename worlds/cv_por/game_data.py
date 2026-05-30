from typing import NamedTuple


class BossDoorData(NamedTuple):  # In-game information used to define each Location in the ROM.
    pointer_table: list[int]
    file: str

boss_doors = {
    "Colosseum Key": BossDoorData([0x022F91DC, 0x022F9248], "overlay_78"),
    "Cavern Key": BossDoorData([0x022FAD18, 0x022FAD78], "overlay_82"),
    "Tower Base Key": BossDoorData([0x022FC53C, 0x022FC47C], "overlay_86"),
    "Clock Key": BossDoorData([0x023061D8, 0x02306154], "overlay_85"),
    "Gallery Key": BossDoorData([0x022FBB60], "overlay_88"),
    "Throne Key": BossDoorData([0x022F1B24], "overlay_87"),
    
    "City Key": BossDoorData([0x02302A78, 0x02302A00], "overlay_95"),
    "Sandy Key": BossDoorData([0x0230729C, 0x02307230], "overlay_91"),
    "Circus Arena Key": BossDoorData([0x022F6978], "overlay_98"),
    "Forest Key": BossDoorData([0x022FB150], "overlay_99"),
    
    "Street Key": BossDoorData([0x022FF048, 0x022FF300], "overlay_106"),
    "Forgotten Key": BossDoorData([0x0230466C], "overlay_103"),
    "Burnt Key": BossDoorData([0x02303EB4, 0x023036F8], "overlay_107"),
    "Academy Key": BossDoorData([0x022F60A8], "overlay_109"),
    "Nest Key": BossDoorData([0x022EE960], "overlay_113")}
