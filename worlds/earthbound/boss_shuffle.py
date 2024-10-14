from typing import NamedTuple, List
import struct


def initialize_bosses(world):
    world.boss_list = [
        "Frank",
        "Frankystein Mark II",
        "Titanic Ant",
        "Captain Strong",
        "Everdred",
        "Mr. Carpainter",
        "Mondo Mole",
        "Boogey Tent",
        "Mini Barf",
        "Master Belch",
        "Trillionage Sprout",
        "Guardian Digger",
        "Dept. Store Spook",
        "Evil Mani-Mani",
        "Clumsy Robot",
        "Shrooom!",
        "Plague Rat of Doom",
        "Thunder and Storm",
        "Kraken",
        "Guardian General",
        "Master Barf",
        "Starman Deluxe",
        "Electro Specter",
        "Carbon Dog",
        "Ness's Nightmare",
        "Heavily Armed Pokey",
        "Starman Junior"
    ]

    class BossData(str):
        slot: str

    class SlotInfo(NamedTuple):
        sprite_addrs: List[int]
        short_names: List[int]
        long_names: List[int]
        battle_data: List[int]

    class BossData(NamedTuple):
        sprite_pointer: int
        short_name_pointer: int
        long_name_pointer: int
        battle_group: int

    world.slot_info: Dict[str, SlotInfo] = {
        "Frank": SlotInfo([0x0F9338], [0x066111, 0x066198, 0x0661AC], [0x065F11, 0x065F20, 0x066481, 0x0660C5, 0x0746E2, 0x074BC1, 0x074E1D], [0x0683FF]),
        "Frankystein Mark II": SlotInfo([0x0F96F0], [], [0x066146, 0x06648B, 0x0664FC], [0x068406]),
        "Titanic Ant": SlotInfo([], [], [], [0x06840D]),
        "Captain Strong": SlotInfo([0x0302CE, 0x05F870, 0x0F8E3D, 0x05F886, 0x05F8A1, 0x05F8E3, 0x05FB0E, 0x05FBFC, 0x05FD08, 0x05FD5C], [0x5FC2B, 0x05FCF7, 0x065F88, 0x066085], [0x05FC59], [0x068468]),
        "Everdred": SlotInfo([0x0F9A64, 0x0F9FB4], [0x2EEEEA], [0x095C70], [0x06846F]),
        "Mr. Carpainter": SlotInfo([0x0FA27E], [0x0990DA, 0x0684D0], [0x0993DB, 0x09945E, 0x099311, 0x099364, 0x098EF6, 0x099143, 0x099028, 0x0983BB, 0x09840C, 0x09835B, 0x09056F, 0x0794EC], [0x0684FD]),
        "Mondo Mole": SlotInfo([], [], [], [0x068414]),
        "Boogey Tent": SlotInfo([0x0FACEB], [], [], [0x068535]),
        "Mini Barf": SlotInfo([0x0FB0B4], [], [], [0x2F9515]),
        "Master Belch": SlotInfo([0x0FB7CF], [0x09E64D, 0x09E690, 0x2EEEED7, 0x08EF21, 0x08EF38], [0x2F6296, 0x2F62B3, 0x2F6910, 0x2F6973], [0x068558]),
        "Trillionage Sprout": SlotInfo([], [], [], [0x068422]),
        "Guardian Digger": SlotInfo([0x0FC11B, 0x0FC0B5, 0x0FC12C, 0x0FC0D7, 0x0FC0C6], [], [], [0x06858E, 0x068595, 0x06859C, 0x0685A3, 0x0685AA]),
        "Dept. Store Spook": SlotInfo([0x0FC803], [], [], [0x06855F]),
        "Evil Mani-Mani": SlotInfo([0x0FE6E4], [], [0x0978AD, 0x09782D, 0x097998], [0x068587]),
        "Clumsy Robot": SlotInfo([0x0FC429], [], [], [0x06856D]),
        "Shrooom!": SlotInfo([], [], [], [0x06841B]),
        "Plague Rat of Doom": SlotInfo([], [], [], [0x068429]),
        "Thunder and Storm": SlotInfo([], [], [], [0x068430]),
        "Kraken": SlotInfo([0x092CD0, 0x0FE370, 0x0FE381, 0x0FE392], [0x092D4D], [0x086061, 0x086139, 0x08B430, 0x08B6FC, 0x08B8B4, 0x08B591, 0x09AB2B], [0x0685B1, 0x2F9472, 0x2F9491, 0x2F94B1]),
        "Guardian General": SlotInfo([0x0FD7E2], [], [], [0x2F9453]),
        "Master Barf": SlotInfo([0x0FDB23], [], [], [0x068574]),
        "Starman Deluxe": SlotInfo([0x0FB626], [], [0x092C29], [0x2F942F]),
        "Electro Specter": SlotInfo([], [], [], [0x068437]),
        "Carbon Dog": SlotInfo([], [], [], [0x06843E]),
        "Ness's Nightmare": SlotInfo([0x0FE3B4], [], [], [0x068580]),
        "Heavily Armed Pokey": SlotInfo([0x09C2EC], [0x2EEEC3, 0x2EEECC], [], [0x068579]),
        "Starman Junior": SlotInfo([], [], [], [])
    }
    #todo, end boss action for Barf and mole/rat text

    world.boss_info: Dict[str, BossData] = {
        "Frank": BossData(0x0099, 0xEEEEBC, 0xEEEEBC, 0x01C0),
        "Frankystein Mark II": BossData(0x0191, 0xEEEF0A, 0xEEEEF6, 0x01C1),
        "Titanic Ant": BossData(0x0139, 0xEEEF1E, 0xEEEF16, 0x01C2),
        "Captain Strong": BossData(0x004B, 0xEEEF2A, 0xEEEF22, 0x01C4),
        "Everdred": BossData(0x009D, 0xEEEF31, 0xEEEF31, 0x01C5),
        "Mr. Carpainter": BossData(0x009F, 0xEEEF3E, 0xEEEF3A, 0x01C6),
        "Mondo Mole": BossData(0x019F, 0xEEEF4F, 0xEEEF49, 0x01C7),
        "Boogey Tent": BossData(0x0110, 0xEEEF5B, 0xEEEF54, 0x01CA),
        "Mini Barf": BossData(0x013B, 0xEEEF65, 0xEEEF60, 0x01E2),
        "Master Belch": BossData(0x0148, 0xEEEF71, 0xEEEF6A, 0x01C8),
        "Trillionage Sprout": BossData(0x013D, 0xEEEF83, 0xEEEF77, 0x01C9),
        "Guardian Digger": BossData(0x01A3, 0xEEEF93, 0xEEEF8A, 0x01CB),
        "Dept. Store Spook": BossData(0x01C7, 0xEEEFA6, 0xEEEF9A, 0x01CC),
        "Evil Mani-Mani": BossData(0x0125, 0xEEEFB1, 0xEEEFAC, 0x01CD),
        "Clumsy Robot": BossData(0x01A2, 0xEEEFC1, 0xEEEFBB, 0x01CE),
        "Shrooom!": BossData(0x0123, 0xEEEFD8, 0xEEEFD8, 0x01D1),
        "Plague Rat of Doom": BossData(0x01A0, 0xEEEFEE, 0xEEEFE0, 0x01CF),
        "Thunder and Storm": BossData(0x0144, 0xEEEFFF, 0xEEEFF3, 0x01D0),
        "Kraken": BossData(0x0127, 0xEEF005, 0xEEF005, 0x01D3),
        "Guardian General": BossData(0x0142, 0xEEF015, 0xEEEF0C, 0x01D4),
        "Master Barf": BossData(0x012B, 0xEEEF65, 0xEEF01D, 0x01D5),
        "Starman Deluxe": BossData(0x012F, 0xEEF034, 0xEEF029, 0x01D2),
        "Electro Specter": BossData(0x01A5, 0xEEF043, 0xEEF03B, 0x01D6),
        "Carbon Dog": BossData(0x014A, 0xEEF052, 0xEEF04B, 0x01D7),
        "Ness's Nightmare": BossData(0x0125, 0xEEF070, 0xEEF06A, 0x01D8),
        "Heavily Armed Pokey": BossData(0x01CA, 0xEEF064, 0xEEF056, 0x01D9),
        "Starman Junior": BossData(0x012F, 0xEEF082, 0xEEF07A, 0x01DA),
    }
    #todo, tomorrow try to fix this and figure out emily's idea

    if world.options.boss_shuffle:
        world.random.shuffle(world.boss_list)

def write_bosses(world, rom):
    #for boss, slot in boss_dict:
        #info: SlotInfo = world.slot_info[slot]
        #data: BossData = world.boss_info[slot]
        # do whatever
        #for sprite_addr in info.sprite_addrs:
            #rom.write_bytes(sprite_addr, bytearray(????))
    print(world.boss_list)
