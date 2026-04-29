import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from . import world_version

hash_us = "2edd57540cae45842fbd19c45a4214f9"

class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int

file_pointers = {
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

    #  Options handling
    rom.write_to_file(0x0230916E, "overlay_119", world.options.nest_portraits.value)  # Portraits for nest of evil
    rom.write_to_file(0x0230916F, "overlay_119", world.options.brauner_portraits.value)  # Portraits for Brauner
    rom.write_to_file(0x02309170, "overlay_119", world.options.dracula_portraits.value)  # Portraits for Dracula
    rom.write_to_file(0x02309173, "overlay_119", world.options.reveal_hidden_walls.value)  # Reveal hidden walls
    rom.write_to_file(0x02309174, "overlay_119", world.options.start_with_change_cube.value)  # Start with Change Cube
    
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