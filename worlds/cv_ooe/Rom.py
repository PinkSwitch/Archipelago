import hashlib
import os
import Utils
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from .static_location_data import location_data_table
from BaseClasses import ItemClassification
from .Items import item_table

world_version = "1.3.1"
hash_us = "2edd57540cae45842fbd19c45a4214f9"


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int


file_pointers = {
    "arm9": FilePointer(0x4000, 0x02000000, 0xFDBB7),
    "overlay_1": FilePointer(0x154200, 0x0221F680, 0xD1BF),
    "overlay_2": FilePointer(0x161400, 0x0221F680, 0xBCDF),
    "overlay_7": FilePointer(0x268C00, 0x022B7660, 0x198DF),
    "overlay_78": FilePointer(0x369000, 0x022E8820, 0x10ABF),
    "overlay_79": FilePointer(0x379C00, 0x022E8820, 0x1C83F),
    "overlay_80": FilePointer(0x396600, 0x022E8820, 0x1671F),
    "overlay_81": FilePointer(0x3ACE00, 0x022E8820, 0x121BF),
    "overlay_82": FilePointer(0x3BF000, 0x022E8820, 0x1275F),
    "overlay_83": FilePointer(0x3D1800, 0x022E8820, 0x143FF),
    "overlay_84": FilePointer(0x3E5C00, 0x022E8820, 0x1029F),
    "overlay_85": FilePointer(0x3F6000, 0x022E8820, 0x1E19F),
    "overlay_86": FilePointer(0x414200, 0x022E8820, 0x13D5F),
    "overlay_87": FilePointer(0x428000, 0x022E8820, 0x941F),
    "overlay_88": FilePointer(0x431600, 0x022E8820, 0x137BF),
    "overlay_89": FilePointer(0x444E00, 0x022E8820, 0x997F),
    "overlay_91": FilePointer(0x452E00, 0x022E8820, 0x1EE7F),
    "overlay_92": FilePointer(0x471E00, 0x022E8820, 0x1DE7F),
    "overlay_93": FilePointer(0x48FE00, 0x022E8820, 0x1963F),
    "overlay_94": FilePointer(0x4A9600, 0x022E8820, 0xE83F),
    "overlay_95": FilePointer(0x4B8000, 0x022E8820, 0x1A59F),
    "overlay_96": FilePointer(0x4D2600, 0x022E8820, 0x1809F),
    "overlay_97": FilePointer(0x4EA800, 0x022E8820, 0x1D49F),
    "overlay_98": FilePointer(0x507E00, 0x022E8820, 0xE29F),
    "overlay_99": FilePointer(0x516200, 0x022E8820, 0x129BF),
    "overlay_100": FilePointer(0x528C00, 0x022E8820, 0x1A53F),
    "overlay_101": FilePointer(0x543200, 0x022E8820, 0x1577F),
    "overlay_102": FilePointer(0x558A00, 0x022E8820, 0x2067F),
    "overlay_103": FilePointer(0x579200, 0x022E8820, 0x1C59F),
    "overlay_104": FilePointer(0x595800, 0x022E8820, 0xB45F),
    "overlay_105": FilePointer(0x5A0E00, 0x022E8820, 0x1493F),
    "overlay_106": FilePointer(0x5B5800, 0x022E8820, 0x16B3F),
    "overlay_107": FilePointer(0x5CC400, 0x022E8820, 0x1B6DF),
    "overlay_108": FilePointer(0x5E7C00, 0x022E8820, 0x1C8FF),
    "overlay_109": FilePointer(0x604600, 0x022E8820, 0xDBDF),
    "overlay_110": FilePointer(0x612200, 0x022E8820, 0x9E5F),
    "overlay_111": FilePointer(0x61C200, 0x022E8820, 0xFEDF),
    "overlay_112": FilePointer(0x62C200, 0x022E8820, 0xA33F),
    "overlay_113": FilePointer(0x636600, 0x022E8820, 0x621F),
    "overlay_119": FilePointer(0x2CF0800, 0x02308EC0, 0x1F000),
    "portrait_set_1": FilePointer(0x1936000, 0x00, 0x3FFF),
    "portrait_set_2": FilePointer(0x193A000, 0x00, 0x3FFF),
    "portrait_set_3": FilePointer(0x193E000, 0x00, 0x3FFF)
}


class LocalRom(object):

    def __init__(self, file: bytes, name: str | None = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_from_file(self, offset: int, file_name: str, length: int) -> bytes:
        file = file_pointers[file_name]
        address = offset - file.base_address
        if address < 0 or (address + length > file.file_size):
            raise ValueError(f"Out of Range: Tried to read at {hex(offset)} in {file_name}")
        address = file.rom_address + address

        return self.file[address:address + length]

    def write_to_file(self, offset: int, file_name: str, values: Sequence[int]) -> None:
        file = file_pointers[file_name]
        address = offset - file.base_address
        if address < 0 or (address + len(values) > file.file_size):
            raise ValueError(f"Out of Range: Tried to write {values} at {hex(offset)} in {file_name}")
        address = file.rom_address + address
        self.file[address:address + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world, rom, code_patch):
    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = bytearray(rom.name, "utf8")[:0x13]
    patch_name.append(0)  # Add a terminator here
    rom.write_to_file(0x02309140, "overlay_119", code_patch)  # Apply the basepatch's data


    rom.write_file("token_patch.bin", rom.get_token_binary())


class OoEProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania: Order of Ecclesia"
    patch_file_ending = ".apcvooe"
    result_file_ending = ".nds"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["por_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("check_patch_version", []),
        ("adjust_item_positions", []),
        ("apply_modifiers", []),
        ("shuffle_portrait_gfx", []),
        ("adjust_quest_rewards", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_to_file(self, offset: int, file_name: str, value: bytearray) -> None:
        file = file_pointers[file_name]
        address = offset - file.base_address
        if address < 0 or (address + len(value) > file.file_size):
            raise ValueError(f"Out of Range: Tried to write {value} at {hex(offset)} in {file_name}")
        address = file.rom_address + address
        self.write_token(APTokenTypes.WRITE, address, bytes(value))

    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class PorPatchExtentions(APPatchExtension):
    game = "Castlevania: Portrait of Ruin"

    @staticmethod
    def check_patch_version(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_from_file(0x02308F35, "overlay_119", 11)
        version = version_check.rstrip(b"\x00")
        version = version.decode("ascii")
        if version != world_version:  # Installed world is different from generated world
            raise Exception(
                f"Error! this patch was generated on Portrait of Ruin APworld version: {version}, but installed APworld is version: {world_version}. " +
                f"Please use APWorld version {version} to patch your game.")
        return rom.get_bytes()

    def apply_modifiers(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        exp_multiplier = struct.unpack("H", rom.read_from_file(0x02309176, "overlay_119", 2))[0]  # Read the multiplier
        exp_multiplier = exp_multiplier / 100
        sp_multiplier = rom.read_from_file(0x0230917C, "overlay_119", 1)[0]

        for i in range(0x9A):
            address = 0x020BE568 + (0x20 * i)
            enemy_exp = struct.unpack("H", rom.read_from_file(address + 16, "arm9", 2))[0]
            enemy_exp = int(min(0xFFFF, (enemy_exp * exp_multiplier)))

            enemy_sp = rom.read_from_file(address + 13, "arm9", 1)[0]
            enemy_sp = int(min(255, (enemy_sp * sp_multiplier)))
            rom.write_to_file(address + 16, "arm9", struct.pack("H", enemy_exp))
            rom.write_to_file(address + 13, "arm9", bytearray([enemy_sp]))
        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash_us != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from worlds.cv_por import OoEWorld
    if not file_name:
        file_name = OoEWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name