import hashlib
import os
import Utils
import typing
import struct
import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import TYPE_CHECKING, Optional
from logging import warning
from gclib.gcm import GCM
from gclib.dol import DOL

if TYPE_CHECKING:
    from . import FSAdventuresWorld


valid_hashes = ["6156867bd3aa2fc410e9e307fe0fd98c"]


class LocalRom(object):

    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world, rom, player: int):

    rom.copy_bytes(0x1578DD, 0x3E, 0x34A060)  # Threed/Saturn teleport move
    rom.copy_bytes(0x15791B, 0xF8, 0x157959)

    rom.copy_bytes(0x34A000, 0x1F, 0x1578DD)
    rom.copy_bytes(0x34A020, 0x1F, 0x15793A)
    rom.copy_bytes(0x34A040, 0x1F, 0x157A51)
    rom.copy_bytes(0x34A060, 0x3E, 0x1578FC)
    rom.copy_bytes(0x15ED4B, 0x06, 0x15F1FB)

    rom.write_bytes(0x3FF0A0, world.world_version.encode("ascii"))

    from Main import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x00FFC0, rom.name)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class FSAProcPatch(APProcedurePatch, APTokenMixin):
    hash = valid_hashes
    game = "The Legend of Zelda: Four Swords Adventures"
    patch_file_ending = ".apfsa"
    result_file_ending = ".iso"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("patch_files", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))
    
    def copy_bytes(self, source, amount, destination):
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class FSAPatchExtensions(APPatchExtension):
    game = "The Legend of Zelda: Four Swords Adventures"

    @staticmethod
    def patch_files(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x3FF0A0, 16)
        version_check = version_check.split(b'\x00', 1)[0]
        version_check_str = version_check.decode("ascii")
        client_version = world_version
        if client_version != version_check_str and version_check_str != "":
            raise Exception(f"Error! Patch generated on EarthBound APWorld version {version_check_str} doesn't match client version {client_version}! " +
                            f"Please use EarthBound APWorld version {version_check_str} for patching.")
        elif version_check_str == "":
            raise Exception(f"Error! Patch generated on old EarthBound APWorld version, doesn't match client version {client_version}! " +
                            f"Please verify you are using the same APWorld as the generator.")

        gcm_local_var = GCM(r"C:\Path\To\ROM.iso")
        gcm_local_var.read_entire_disc()
        dol_local_var = DOL()

        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in valid_hashes:
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["fsa_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


# Fix hint text, I have a special idea where I can give it info on a random region
