import hashlib
import os
import Utils
import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence
from .in_game_data import (global_weapon_table, base_weapons, valid_random_starting_weapons, global_soul_table,
                           base_check_address_table, easter_egg_table, warp_room_bits, world_version)
from Options import OptionError
from .Options import StartingWeapon, SoulRandomizer
from .Items import soul_filler_table
from BaseClasses import ItemClassification

hash_us = "cc0f25b8783fb83cb4588d1c111bdc18"


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
    # This is the entirety of the patched code
    rom.write_bytes(0x2F6DC50, code_patch)

    weapon = world.options.starting_weapon.value

    if isinstance(weapon, str):
        if weapon not in global_weapon_table:
            raise OptionError(f"Error generating for player {world.player_name}. Attempted to set an invalid starting weapon: {weapon}.")
    else:
        if weapon == StartingWeapon.option_random_base:
            weapon = world.random.choice(base_weapons)
        else:
            weapon = world.random.choice(valid_random_starting_weapons)

    starting_weapon = global_weapon_table.index(weapon)

    # Options handling
    rom.write_bytes(0x122E88, bytearray([starting_weapon]))

    warp_room = warp_room_bits[world.starting_warp_room]
    rom.write_bytes(0x2F6DD4E, struct.pack("H", warp_room))  # The initial warp room bit

    if world.options.replace_menace_with_soma:
        rom.write_bytes(0xC2418, bytearray([0x03]))

    if world.options.remove_money_gates:
        rom.write_bytes(0xAD661, bytearray([0x00]))
        rom.write_bytes(0xB0A2D, bytearray([0x00]))
        rom.write_bytes(0xBD135, bytearray([0x00]))

    if world.options.disable_boss_seals:
        rom.write_bytes(0x11EA18, bytearray([0x00]))
        rom.write_bytes(0x140A24, bytearray([0x01, 0x00, 0xA0, 0xE3]))

    if world.options.reveal_map:
        rom.write_bytes(0x260C7, bytearray([0xE1, 0x00, 0x00, 0xA0, 0xE1]))
        rom.write_bytes(0x28BE8, bytearray([0x00, 0x00, 0xE0, 0xE3, 0x1E, 0xFF, 0x2F]))

    if world.options.open_drawbridge:
        rom.write_bytes(0x0CF046, bytearray([0xA0, 0xE1]))  # Make the drawbridge always be down

    if world.options.fix_luck:
        rom.write_bytes(0xF087D, bytearray([0x22]))
        rom.write_bytes(0xF0888, bytearray([0x02, 0x70]))
        rom.write_bytes(0xF088D, bytearray([0x71]))
        rom.write_bytes(0xF0890, bytearray([0x00, 0x00]))
        rom.write_bytes(0xF0893, bytearray([0xE1]))
        rom.write_bytes(0xF089A, bytearray([0xA0, 0xE3]))
        rom.write_bytes(0xF08BE, bytearray([0x87, 0xE0]))
        rom.write_bytes(0xF09A0, bytearray([0x00, 0x00, 0xA0, 0xE1]))
        rom.write_bytes(0xF09C8, bytearray([0x02, 0x0A]))
        rom.write_bytes(0xF09CB, bytearray([0xE3]))
        rom.write_bytes(0xF09F0, bytearray([0x47, 0x91, 0x80, 0xE0]))
        rom.write_bytes(0xF0A00, bytearray([0x89]))
        rom.write_bytes(0xF0A04, bytearray([0x02, 0x0A]))
        rom.write_bytes(0xF0A07, bytearray([0xE3]))

    if world.options.reveal_hidden_walls:
        rom.write_bytes(0xA5231, bytearray([0x00]))
        rom.write_bytes(0xA57AD, bytearray([0x00]))
        rom.write_bytes(0xAA45D, bytearray([0x00]))
        rom.write_bytes(0xAD3E5, bytearray([0x00]))
        rom.write_bytes(0xB0199, bytearray([0x00]))
        rom.write_bytes(0xBEE21, bytearray([0x00]))
        rom.write_bytes(0xBEE8D, bytearray([0x00]))
        rom.write_bytes(0xBEFC5, bytearray([0x00]))
        rom.write_bytes(0xB84A9, bytearray([0x00]))

    if not world.options.goal:  # Remove the better ending trigger and replace Dario with Menace
        rom.write_bytes(0xBD508, bytearray([0x60, 0xDC]))
        rom.write_bytes(0xBD50E, bytearray([0xFF, 0xFE, 0xD0, 0xFF]))
        rom.write_bytes(0xC1C30, bytearray([0xD4, 0x94]))
        rom.write_bytes(0xC1C38, bytearray([0xD0]))
        rom.write_bytes(0xB05A1, bytearray([0x00]))

    if world.options.goal == 2:
        rom.write_bytes(0x2F6DD48, bytearray([0x01]))

    if world.options.one_screen_mode:
        rom.write_bytes(0x2F6DD4C, bytearray([0x01]))

    if world.options.boost_speed:
        rom.write_bytes(0x15B2A9, bytearray([0x20]))
        
    soul_check_table = 0x2F6DC50

    if world.options.soul_randomizer == SoulRandomizer.option_shuffled:
        vanilla_souls = {"Skeleton Soul", "Axe Armor Soul", "Killer Clown Soul", "Ukoback Soul", "Skeleton Ape Soul", "Bone Ark Soul"}
        shuffled_keys = [item for item in soul_filler_table.copy() if item not in vanilla_souls]
        souls_output = {key: key for key in soul_filler_table.copy()}  # this is assuming all vanilla souls are in soul_filler_table
        shuffled_vals = world.random.sample(shuffled_keys, k=len(shuffled_keys))
        for key, val in zip(shuffled_keys, shuffled_vals):
            souls_output[key] = val

        for soul in souls_output:
            soul_data = bytearray([global_soul_table.index(souls_output[soul]), 0x05])
            rom.write_bytes(soul_check_table + (global_soul_table.index(soul) * 2), soul_data)

    for location in world.multiworld.get_locations(player):
        item_type = 0
        item_id = 0
        if location.address:
            if location.item.player == world.player:   # If this is an item for the player, we need to extract it's Type and ID
                item_type = (location.item.code & 0xFF00) >> 8
                item_id = location.item.code & 0x00FF
            else:  # AP items are item type 2 and then use ID for progression.
                item_type = 2
                if ItemClassification.progression in location.item.classification:
                    item_id = 0x0C3B
                elif ItemClassification.useful in location.item.classification:
                    item_id = 0x073A
                elif ItemClassification.trap in location.item.classification:
                    item_id = 0x063A
                else:
                    item_id = 0x093A

        if location.address:  # Filter out events
            if location.name in global_soul_table:
                if location.item.player != world.player:
                    # AP items on souls can use the Type as the color
                    item_type = (item_id & 0xFF00) >> 8
                    item_id = item_id & 0xFF
                item_struct = (item_type << 8) | item_id
                index = (global_soul_table.index(location.name) * 2)
                rom.write_bytes(soul_check_table + index, struct.pack("H", item_struct))
            elif location.name in easter_egg_table:
                if item_id > 0xFF: # If this has a color
                    item_type = (item_id & 0xFF00) >> 8 # Replace the type with the color if it has one
                    item_id = item_id & 0xFF
                rom.write_bytes(easter_egg_table[location.name][0], bytearray([item_type]))
                rom.write_bytes(easter_egg_table[location.name][1], bytearray([item_id]))
            else:
                # Regular item checks
                address = base_check_address_table[location.name]
                if location.item.name in global_soul_table and location.item.player == world.player:
                    rom.write_bytes(address + 9, bytearray([item_id]))  # High byte of the flag is used as Soul /Color ID
                    rom.write_bytes(address + 10, bytearray([0x3C]))
                    item_type = 2
                else:
                    rom.write_bytes(address + 9, struct.pack(">H", item_id))
                rom.write_bytes(address + 6, bytearray([item_type]))

    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = rom.name + "\0"
    patch_name = bytearray(rom.name, "utf8")[:0x14]
    rom.write_bytes(0x2F6DD50, patch_name)
    rom.write_bytes(0x2F6DD7C, world_version.encode("ascii"))

    rom.write_file("token_patch.bin", rom.get_token_binary())


class DoSProcPatch(APProcedurePatch, APTokenMixin):
    hash = hash_us
    game = "Castlevania: Dawn of Sorrow"
    patch_file_ending = ".apcvdos"
    result_file_ending = ".nds"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["dos_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("adjust_item_positions", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset: int, value: typing.Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))
    
    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class DoSPatchExtensions(APPatchExtension):
    game = "Castlevania: Dawn of Sorrow"

    @staticmethod
    def adjust_item_positions(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x2F6DD7C, 15)
        version = version_check.rstrip(b"\x69")
        version = version.decode("ascii")
        if version != world_version:  # Installed world is different from generated world
            raise Exception(f"Error! this patch was generated on Dawn of Sorrow APworld version: {version}, but installed APworld is version: {world_version}. " +
                            f"Please use APWorld version {version} to patch your game.")

        for check in base_check_address_table:
            address = base_check_address_table[check]
            item_type = int.from_bytes(rom.read_bytes(address + 6, 1))
            item_id = int.from_bytes(rom.read_bytes(address + 10, 1))
            if (item_type == 0x01 and item_id < 4) or (item_type == 0x02 and item_id >= 0x3D):
                # Coins and Magic Seals spawn slightly in the ground, so we need to raise them up a little bit
                y_pos = int.from_bytes(rom.read_bytes(address + 2, 2), byteorder="little")
                y_pos -= 10
                rom.write_bytes(address + 2, struct.pack("H", y_pos))

        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash_us != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from worlds.cv_dos import DoSWorld
    if not file_name:
        file_name = DoSWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
