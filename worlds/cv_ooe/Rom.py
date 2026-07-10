import hashlib
import os
import Utils
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from .static_location_data import location_data_table
from BaseClasses import ItemClassification
from .Items import item_table

world_version = "1.0.0"
hash_us = "e13bdcf706989486df939556eeb42ece"


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int


file_pointers = {
    "dummy": FilePointer(0x4000, 0x02000000, 0xFDBB7),
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
    rom.write_to_file(0x022EB220, "overlay_86", code_patch)  # Apply the basepatch's data
    rom.write_to_file(0x022EB200, "overlay_86", patch_name)  # Write in the player's name
    rom.write_to_file(0x022EB215, "overlay_86", world_version.encode("ascii"))  # Write the patch version

    #  Options handling
    rom.write_to_file(0x022D3040, "overlay_42", bytearray([item_table[world.starting_glyph].code]))  # Starting Glyph needs to be assigned to VarB of the intro object

    rom.write_to_file(0x022EB220, "overlay_86", bytearray([world.options.reveal_hidden_chests.value]))
    rom.write_to_file(0x022EB22E, "overlay_86", bytearray([world.options.reveal_map.value]))
    rom.write_to_file(0x022EB223, "overlay_86", bytearray([world.options.reveal_hidden_walls.value]))

    starting_relics = 0
    if world.options.start_with_lizard_tail:
        starting_relics |= 0x01

    if world.options.start_with_glyph_union:
        starting_relics |= 0x02

    if world.options.start_with_glyph_sleeve:
        starting_relics |= 0x04

    rom.write_to_file(0x022EB222, "overlay_86", bytearray([starting_relics]))

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
        ("apply_modifiers", [])
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


class OoEPatchExtensions(APPatchExtension):
    game = "Castlevania: Order of Ecclesia"

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
        exp_multiplier = struct.unpack("H", rom.read_from_file(0x02309176, "overlay_86", 2))[0]  # Read the multiplier
        exp_multiplier = exp_multiplier / 100

        for i in range(0x78):
            address = 0x020B6364 + (0x24 * i)
            enemy_exp = struct.unpack("H", rom.read_from_file(address + 16, "arm9", 2))[0]
            enemy_exp = int(min(0xFFFF, (enemy_exp * exp_multiplier)))

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
    from worlds.cv_ooe import OoEWorld
    if not file_name:
        file_name = OoEWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
