import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from . import world_version
from .static_location_data import location_data_table
from .Options import NestofEvil

hash_us = "2edd57540cae45842fbd19c45a4214f9"


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int


file_pointers = {
    "arm9": FilePointer(0x4000, 0x02000000, 0xFDBB8),
    "overlay_113": FilePointer(0x636600, 0x022E8820, 0x6220),
    "overlay_119": FilePointer(0x2CF0800, 0x02308EC0, 0x1F000),
}


class LocalRom(object):

    def __init__(self, file: bytes, name: str | None = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world, rom, player: int, code_patch):
    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = bytearray(rom.name, "utf8")[:0x14]
    patch_name.append(0)  # Add a terminator here
    rom.write_to_file(0x02309140, "overlay_119", code_patch)  # Apply the basepatch's data
    rom.write_to_file(0x02308F20, "overlay_119", patch_name)  # Write in the player's name
    rom.write_to_file(0x02308F35, "overlay_119", world_version.encode("ascii"))  # Write the patch version

    #  Options handling ###################
    rom.write_to_file(0x0230916E, "overlay_119", bytearray([world.options.nest_portraits.value]))  # Portraits for nest of evil
    rom.write_to_file(0x0230916F, "overlay_119", bytearray([world.options.brauner_portraits.value]))  # Portraits for Brauner
    rom.write_to_file(0x02309170, "overlay_119", bytearray([world.options.dracula_portraits.value]))  # Portraits for Dracula
    rom.write_to_file(0x02309172, "overlay_119", bytearray([world.options.goal.value]))  # Goal mode, 1 if Dracula
    rom.write_to_file(0x02309173, "overlay_119", bytearray([world.options.reveal_hidden_walls.value]))  # Reveal hidden walls
    rom.write_to_file(0x02309174, "overlay_119", bytearray([world.options.start_with_change_cube.value]))  # Start with Change Cube
    rom.write_to_file(0x02309175, "overlay_119", bytearray([world.options.reveal_map.value]))  # Reveal map

    if world.options.reveal_map:
        rom.write_to_file(0x0202F3B0, "arm9", bytearray([0x00, 0x00, 0xA0, 0xE1]))  # Nop out the instruction that hides room borders
    
    goal_requirements = 0

    if world.options.brauner_required:
        goal_requirements |= 1  # Brauner Flag

    if world.options.nest_of_evil_state == NestofEvil.option_required:
        goal_requirements |= 2  # Nest flag
    elif world.options.nest_of_evil_state == NestofEvil.option_removed:
        # Block off the Nest of Evil entrance with bricks
        rom.write_to_file(0x022EB0CA, "overlay_113", struct.pack("H", 0x4027))
        rom.write_to_file(0x022EB0EA, "overlay_113", struct.pack("H", 0x4027))
        rom.write_to_file(0x022EB10A, "overlay_113", struct.pack("H", 0x4027))
        rom.write_to_file(0x022EB12A, "overlay_113", struct.pack("H", 0x4027))

    # This is the singular Goal Requirements flag.
    # Brauner will never check if brauner is required...
    # If Nest of Evil is required, your goal (either brauner OR drac) will check it.
    rom.write_to_file(0x02309171, "overlay_119", bytearray([goal_requirements]))
    ####################################
    for location in world.get_locations():
        if not location.address:  # Filter all events out of this
            continue
        
        data = location_data_table[location.name]


    rom.write_file("token_patch.bin", rom.get_token_binary())


class PoRProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania: Portrait of Ruin"
    patch_file_ending = ".apcvpor"
    result_file_ending = ".nds"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["por_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("adjust_item_positions", []),
        ("apply_modifiers", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_to_file(self, offset: int, file_name: str, value: typing.Iterable[int]) -> None:
        file = file_pointers[file_name]
        address = offset - file.base_address
        if address < 0 or address > file.file_size:
            raise ValueError(f"Out of Range: Tried to write {value} at {hex(offset)} in {file_name}")
        address = file.rom_address + address
        self.write_token(APTokenTypes.WRITE, address, bytes(value))
    
    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))