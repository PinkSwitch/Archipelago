import hashlib
import os
import Utils
import typing
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from BaseClasses import ItemClassification
from settings import get_settings
from typing import TYPE_CHECKING
#from .local_data import local_locations

if TYPE_CHECKING:
    from . import EarthBoundWorld
USHASH = "a864b2e5c141d2dec1c4cbed75a42a85"

item_ids = {
    0x696969: 0x01, #Money bag
    0x69696A: 0x02, #Coin
    0x69696B: 0x03, #Miracle
    0x69696C: 0x04, #Diamond
    0x69696D: 0x05, #Dynamite
    0x69696E: 0x06, #Flare
    0x69696F: 0x07, #Blue Key
    0x696970: 0x08, #Red Key
    0x696971: 0x09,
    0x696972: 0x0A,
    0x696973: 0x0B,
    0x696974: 0x0C

}

location_table = {
    0x198601: [0x16, 0x01]

}

hidden_table = {
    0x6969FD: 0x0D,
    0x6969FE: 0x1D,
    0x6969FF: 0x55,
    0x696A00: 0x66,
    0x696A01: 0x8F,
    0x696A02: 0xA2,
    0x696A03: 0xC6,
    0x696A04: 0xCA
}

class LocalRom(object):

    def __init__(self, file: str) -> None:
        self.name = None
        self.hash = hash
        self.orig_buffer = None

        with open(file, "rb") as stream:
            self.buffer = Utils.read_snes_rom(stream)

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = 1 << bit_number
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int) -> None:
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values: bytearray) -> None:
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file: str) -> None:
        with open(file, "wb") as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file: str) -> None:
        with open(file, "rb") as stream:
            self.buffer = bytearray(stream.read())

    def apply_patch(self, patch: bytes):
        self.file = bytearray(bsdiff4.patch(bytes(self.file), patch))



def patch_rom(world, rom, player: int, multiworld):

    from Main import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x007040, rom.name)

    player_name_length = 0
    for i, byte in enumerate(world.multiworld.player_name[player].encode("utf-8")):
        rom.write_byte(0x7051 + i, byte)
        player_name_length += 1
    rom.write_byte(0x7050, player_name_length)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class EBProcPatch(APProcedurePatch, APTokenMixin):
    hash = [USHASH]
    game = "EarthBound"
    patch_file_ending = ".apeb"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["earthbound_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
