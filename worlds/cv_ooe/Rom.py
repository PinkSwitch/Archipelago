import hashlib
import os
import typing
import Utils
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from .static_location_data import location_data_table
from .game_data import area_list, villager_list
from BaseClasses import ItemClassification
from .Items import item_table

world_version = "1.0.0"
hash_us = "e13bdcf706989486df939556eeb42ece"


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int


file_pointers = {
    "arm9": FilePointer(0x4000, 0x02000000, 0xFEE18),
    "overlay_0": FilePointer(0x103C00, 0x021DD280, 0x1F7DF),
    "overlay_42": FilePointer(0x2ED600, 0x022C1FE0, 0x1117F),
    "overlay_86": FilePointer(0x302E600, 0x022EB1A0, 0x32000),
    "comgfx_4": FilePointer(0x1A49200, 0, 0x1FFF),
    #"itemgfx_0": FilePointer(0x, 0, 0x)
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
    rom.write_direct(0x0302E464, code_patch)  # Apply the basepatch's data. Inlined because it includes some padding

    rom.write_to_file(0x022EB200, "overlay_86", patch_name)  # Write in the player's name
    rom.write_to_file(0x022EB215, "overlay_86", world_version.encode("ascii"))  # Write the patch version

    #  Options handling
    rom.write_to_file(0x022D3040, "overlay_42", bytearray([item_table[world.starting_glyph].code]))  # Starting Glyph needs to be assigned to VarB of the intro object

    rom.write_to_file(0x022EB220, "overlay_86", bytearray([world.options.reveal_hidden_chests.value]))
    rom.write_to_file(0x022EB22E, "overlay_86", bytearray([world.options.reveal_map.value]))
    rom.write_to_file(0x022EB223, "overlay_86", bytearray([world.options.reveal_hidden_walls.value]))
    rom.write_to_file(0x022EB22F, "overlay_86", bytearray([world.options.experience_percent.value]))

    #  Starting relics. These are all bits within one byte.#################
    starting_relics = 0
    if world.options.start_with_lizard_tail:
        starting_relics |= 0x01

    if world.options.start_with_glyph_union:
        starting_relics |= 0x02

    if world.options.start_with_glyph_sleeve:
        starting_relics |= 0x04

    rom.write_to_file(0x022EB222, "overlay_86", bytearray([starting_relics]))
    #  Starting area  ###################
    starting_area_value = 0
    if world.starting_area:
        starting_area_value = area_list.index(world.starting_area)

    rom.write_to_file(0x022EB221, "overlay_86", bytearray([starting_area_value]))
    #####################################################
    #  Starting Villagers
    starting_villagers = 0
    for villager in world.options.starting_villagers:
        starting_villagers |= villager_list.index(villager)
    rom.write_to_file(0x022EB22A, "overlay_86", struct.pack("H", starting_villagers))
    ################################################
    rom.write_to_file(0x022EB226, "overlay_86", struct.pack("H", world.options.villagers_required.value))
    rom.write_to_file(0x021E98BE, "overlay_0", struct.pack("H", world.options.villagers_required.value))  # Barlowe's dialogue in the bad ending
    ###############################################


    rom.write_file("token_patch.bin", rom.get_token_binary())


class OoEProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania: Order of Ecclesia"
    patch_file_ending = ".apcvooe"
    result_file_ending = ".nds"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["ooe_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("check_patch_version", []),
        ("copy_money_gfx", []),
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

    def write_direct(self, offset: int, value: typing.Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


class OoEPatchExtensions(APPatchExtension):
    game = "Castlevania: Order of Ecclesia"

    @staticmethod
    def check_patch_version(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_from_file(0x022EB215, "overlay_86", 11)
        version = version_check.rstrip(b"\x00")
        version = version.decode("ascii")
        if version != world_version:  # Installed world is different from generated world
            raise Exception(
                f"Error! this patch was generated on Order of  Ecclesia APworld version: {version}, but installed APworld is version: {world_version}. " +
                f"Please use APWorld version {version} to patch your game.")
        return rom.get_bytes()

    @staticmethod
    def apply_modifiers(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        exp_multiplier = struct.unpack("H", rom.read_from_file(0x022EB22F, "overlay_86", 2))[0]  # Read the multiplier
        exp_multiplier = exp_multiplier / 100

        for i in range(0x78):
            address = 0x020B6364 + (0x24 * i)
            enemy_exp = struct.unpack("H", rom.read_from_file(address + 16, "arm9", 2))[0]
            enemy_exp = int(min(0xFFFF, (enemy_exp * exp_multiplier)))

        return rom.get_bytes()

    @staticmethod
    def copy_money_gfx(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        #  Money bag sprite
        source_sprite = []
        for i in range(16):
            source_tile_row = rom.read_from_file(0x10 + (i * 0x40), "comgfx_4", 8)

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
