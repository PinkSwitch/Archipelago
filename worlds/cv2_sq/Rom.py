import hashlib
import os
import typing
import Utils
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

world_version = "1.0"
hash_us = "87dae73b0c4c8fdeba8cf4209df87e2c"


class LocalRom(object):

    def __init__(self, file: bytes, name: typing.Optional[str] = None) -> None:
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


def patch_rom(world, rom):
    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = bytearray(rom.name, "utf8")[:0x13]

    rom.write_bytes(0xDD20, patch_name)  # Write in the player's name
    rom.write_bytes(0xDD10, world_version.encode("ascii"))  # Write the patch version

    #  Options handling
    if world.options.randomize_tunic_color:
        tunic_color = world.random.choice([i for i in range(0x00, 0x3D) if i not in [0x0D, 0x0E, 0x0F, 0x1D,
                                                                                     0x1E, 0x1F, 0x2E, 0x2F, 0x30]])
        rom.write_bytes(0x1CAC0, bytearray([tunic_color]))
        rom.write_bytes(0x1CAC5, bytearray([tunic_color]))

    if world.options.inclusive_white_crystal:
        rom.write_bytes(0x1FF11, bytearray([0x01]))
        rom.write_bytes(0x45BD, bytearray([0xFE]))  # Change objetc pointer to need whtcrys
        rom.write_bytes(0x45BF, bytearray([0xFE]))

    rom.write_bytes(0x1FF12, bytearray([world.options.orbs_required.value]))
    rom.write_bytes(0x1FF13, bytearray([world.options.dracula_parts_required.value]))
    rom.write_bytes(0xFE10, bytearray([world.options.poison_proof_ring.value]))

    rom.write_as_binary_decimal(0x474F, bytearray([2 * world.options.heart_multiplier.value]))
    rom.write_as_binary_decimal(0x475C, bytearray([4 * world.options.heart_multiplier.value]))
    rom.write_as_binary_decimal(0x4769, bytearray([6 * world.options.heart_multiplier.value]))

    if world.options.night_owl_towns:
        rom.write_bytes(0x4169, bytearray([0xEA, 0xEA]))  # Villagers

        rom.write_bytes(0xC7BA, bytearray([0xEA, 0xEA]))  # Too early doors
        rom.write_bytes(0xC7BE, bytearray([0xEA, 0xEA]))  # Too late doors

    rom.write_as_binary_decimal(0x1FF14, struct.pack("H", world.options.starting_hearts.value))

    ################################################
    # Locations handler
    for location in world.get_locations():
        if location.address:
            if location.item.player != world.player:
                item_id = 0
            else:
                item_id = location.item.code

            rom.write_bytes(0xDDB0 + location.address, bytearray([item_id]))

    rom.write_file("token_patch.bin", rom.get_token_binary())


class CV2ProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania II: Simon's Quest"
    patch_file_ending = ".apcv2"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["cv2_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("check_patch_version", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset: int, value: bytearray) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))

    def write_as_binary_decimal(self, offset: int, value: bytearray) -> None:
        value = int.from_bytes(value, byteorder="little")
        value = struct.pack("H", int(str(value), 16))
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


class CV2PatchExtensions(APPatchExtension):
    game = "Castlevania II: Simon's Quest"

    @staticmethod
    def check_patch_version(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0xDD10, 0x10)
        version = version_check.rstrip(b"\xFF")
        version = version.decode("ascii")
        if version != world_version:  # Installed world is different from generated world
            raise Exception(
                f"Error! this patch was generated on Castlevania II APworld version: {version}, but installed APworld is version: {world_version}. " +
                f"Please use APWorld version {version} to patch your game.")
        return rom.get_bytes()


header = bytes.fromhex("4E 45 53 1A 08 10 10 08 00 00 00 00 00 00 00 01")


def read_headerless_nes_rom(rom: bytes) -> bytes:
    if rom[:4] == b"NES\x1A":
        return rom
    else:
        rom[0:0] = header  # If we don't have a header, add one
        return rom


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
        headered_rom = bytearray(base_rom_bytes)
        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
        return bytes(headered_rom)

    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from . import CV2World
    if not file_name:
        file_name = CV2World.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
