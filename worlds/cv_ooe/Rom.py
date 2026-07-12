import hashlib
import os
import typing
import Utils
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from .static_location_data import location_data_table
from .game_data import area_list, villager_list, villager_flags
from BaseClasses import ItemClassification
from .Items import item_table
from .Options import AddBrownChests
from .modules.brown_chest_shuffler import shuffle_brown_chest_pool

world_version = "1.0.0"
hash_us = "e13bdcf706989486df939556eeb42ece"


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int


file_pointers = {
    "arm9": FilePointer(0x4000, 0x02000000, 0xFEE18),
    "overlay_0": FilePointer(0x103C00, 0x021DD280, 0x1F7DF),
    "overlay_19": FilePointer(0x14A400, 0x021FFFC0, 0x23C7F),
    "overlay_40": FilePointer(0x2DD000, 0x022C1FE0, 0xA73F),
    "overlay_41": FilePointer(0x2E7800, 0x022C1FE0, 0x5CDF),
    "overlay_42": FilePointer(0x2ED600, 0x022C1FE0, 0x1117F),
    "overlay_43": FilePointer(0x2FE800, 0x022C1FE0, 0xDFDF),
    "overlay_44": FilePointer(0x30C800, 0x022C1FE0, 0xB5FF),
    "overlay_45": FilePointer(0x317E00, 0x022C1FE0, 0x843F),
    "overlay_46": FilePointer(0x320400, 0x022C1FE0, 0x22ABF),
    "overlay_47": FilePointer(0x343000, 0x022C1FE0, 0xD83F),
    "overlay_48": FilePointer(0x350A00, 0x022C1FE0, 0x1B5FF),
    "overlay_50": FilePointer(0x371000, 0x022C1FE0, 0xC87F),
    "overlay_51": FilePointer(0x37DA00, 0x022C1FE0, 0xD73F),
    "overlay_52": FilePointer(0x38B200, 0x022C1FE0, 0xAE1F),
    "overlay_53": FilePointer(0x396200, 0x022C1FE0, 0xB8DF),
    "overlay_54": FilePointer(0x3A1C00, 0x022C1FE0, 0x1937F),
    "overlay_55": FilePointer(0x3BB000, 0x022C1FE0, 0xD99F),
    "overlay_56": FilePointer(0x3C8A00, 0x022C1FE0, 0x1421F),
    "overlay_57": FilePointer(0x3DCE00, 0x022C1FE0, 0xF17F),
    "overlay_58": FilePointer(0x3EC000, 0x022C1FE0, 0x885F),
    "overlay_59": FilePointer(0x3F4A00, 0x022C1FE0, 0x1187F),
    "overlay_60": FilePointer(0x406400, 0x022C1FE0, 0x10E1F),
    "overlay_61": FilePointer(0x417400, 0x022C1FE0, 0xECBF),
    "overlay_62": FilePointer(0x426200, 0x022C1FE0, 0x3FFF),
    "overlay_63": FilePointer(0x42A200, 0x022C1FE0, 0xE69F),
    "overlay_64": FilePointer(0x438A00, 0x022C1FE0, 0xBCBF),
    "overlay_65": FilePointer(0x444800, 0x022C1FE0, 0xE59F),
    "overlay_66": FilePointer(0x452E00, 0x022C1FE0, 0xBEDF),
    "overlay_68": FilePointer(0x466A00, 0x022C1FE0, 0x291BF),
    "overlay_69": FilePointer(0x48FC00, 0x022C1FE0, 0x1821F),
    "overlay_70": FilePointer(0x4A8000, 0x022C1FE0, 0xAE9F),
    "overlay_71": FilePointer(0x4B3000, 0x022C1FE0, 0x135BF),
    "overlay_72": FilePointer(0x4C6600, 0x022C1FE0, 0x1AEFF),
    "overlay_73": FilePointer(0x4E1600, 0x022C1FE0, 0x5E9F),
    "overlay_74": FilePointer(0x4E7600, 0x022C1FE0, 0x13B3F),
    "overlay_75": FilePointer(0x4FB200, 0x022C1FE0, 0xCF7F),
    "overlay_76": FilePointer(0x508200, 0x022C1FE0, 0x1321F),
    "overlay_77": FilePointer(0x51B600, 0x022C1FE0, 0x939F),
    "overlay_78": FilePointer(0x524A00, 0x022C1FE0, 0x1633F),
    "overlay_86": FilePointer(0x302E600, 0x022EB1A0, 0x32000),
    "comgfx_4": FilePointer(0x1A49200, 0, 0x1FFF),
    "itemgfx_0": FilePointer(0x1CFF200, 0, 0x1FFF)
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
    if world.options.add_brown_chests == AddBrownChests.option_random_rewards:
        shuffle_brown_chest_pool(world, rom)
    ###############################################
    # Locations handler
    patch_locations(world, rom, world.get_locations())

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
            rom.write_to_file(address + 16, "arm9", struct.pack("H", enemy_exp))

        return rom.get_bytes()

    @staticmethod
    def copy_money_gfx(caller: APProcedurePatch, rom: bytes) -> bytes:
        import itertools
        rom = LocalRom(rom)
        #  Money bag sprite
        for i in range(2):
            source_sprite = []
            for j in range(8):
                source_tile_row = rom.read_from_file(0x10 + (j * 0x40) + (i * 0x200), "comgfx_4", 8)
                source_sprite.append(source_tile_row)

            sprite = [[a[:4] + b[:4] + c[:4] + d[:4] for (a, b, c, d) in itertools.batched(source_sprite, 4)],
                      [a[4:] + b[4:] + c[4:] + d[4:] for (a, b, c, d) in itertools.batched(source_sprite, 4)]]

            row_new = []
            for half in sprite:  # We need to recombine this into a single 4-item Array
                for row in half:
                    row_new.append(row)

            for j, half in enumerate(row_new):
                rom.write_to_file(0x500 + (0x200 * i) + (0x10 * j), "itemgfx_0", half)
        ########################
        #  Coin sprite
        for i in range(2):
            for j in range(8):
                source_sprite = rom.read_from_file(0x18 + (0x40 * j) + (0x2 * i), "comgfx_4", 2)
                rom.write_to_file(0x742 + (4 * j) + (0x1E * i), "itemgfx_0", source_sprite)

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


def get_item_id(world, item):
    if item.player == world.player:
        item_id = item_table[item.name].code
    else:
        if ItemClassification.progression or ItemClassification.trap in item.classification:
            item_id = 0xD6
        elif ItemClassification.useful in item.classification:
            item_id = 0xD5
        else:
            item_id = 0xD4 
    return item_id


def patch_locations(world, rom, locations):
    for location in locations:
        if not location.address:
            continue  # Skip over Events
        item = location.item
        data = location_data_table[location.name]
        item_id = get_item_id(world, location.item)

        #  Location specs can be found with the data table
        if data.location_type == "Chest":
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", item_id))

        elif data.location_type == "Wood Chest":
            rom.write_to_file(data.pointer + 6, data.file, bytes([0x16]))
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", item_id))
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", location.address))

        elif data.location_type == "Freestanding":
            if item_id < 0x70:  # Glyphs need to be spawned as Glyph Statues
                object_type = 0x02
                sub_type = 0x02
                var_a = 0x8000 | location.address
                var_b = item_id
            elif item_id in range(0x168, 0x175):  # Villagers need to be spawned as the rescuable Villager Obj
                object_type = 0x02
                sub_type = 0x89
                var_a = villager_flags[item.name]
                var_b = location.address
            else:
                object_type = 0x04  # Free pickup
                if item_id in range(0x161, 0x168):  # Money
                    sub_type = 0x01
                    var_b = item_id - 0x161
                else:
                    sub_type = 0xFF
                    var_b = item_id
                var_a = location.address
            rom.write_to_file(data.pointer + 5, data.file, bytes([object_type]))
            rom.write_to_file(data.pointer + 6, data.file, bytes([sub_type]))
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", var_a))
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", var_b))
            
        elif data.location_type == "Area Exit":
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", item_id))
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", location.address))
        elif data.location_type == "Event Glyph":
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", item_id))
        elif data.location_type == "Freestanding Glyph":
            #  This is handled the same way as Freestanding, except Glyphs are handled as Glyphs instead of statues
            if item_id in range(0x168, 0x175):  # Villagers need to be spawned as the rescuable Villager Obj
                object_type = 0x02
                sub_type = 0x89
                var_a = villager_flags[item.name]
                var_b = location.address
            else:
                object_type = 0x04  # Free pickup
                if item_id in range(0x161, 0x168):  # Money
                    sub_type = 0x01
                    var_b = item_id - 0x161
                elif item_id < 0x70:  # Glyphs
                    sub_type = 0x02
                    var_b = item_id
                else:
                    sub_type = 0xFF
                    var_b = item_id
                var_a = location.address
            rom.write_to_file(data.pointer + 5, data.file, bytes([object_type]))
            rom.write_to_file(data.pointer + 6, data.file, bytes([sub_type]))
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", var_a))
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", var_b))
        elif data.location_type == "Event Chest":
            rom.write_to_file(data.pointer + 8, data.file, struct.pack("H", item_id))
        elif data.location_type == "Inline":
            rom.write_to_file(data.pointer, data.file, struct.pack("H", item_id))
        elif data.location_type == "Enemy Glyph":
            rom.write_to_file(data.pointer + 0x14, data.file, struct.pack("H", item_id))
        elif data.location_type == "Hidden Item":
            #  This is handled the same way as Freestanding, except all items are just, their item.
            if item_id in range(0x161, 0x168):  # Money
                sub_type = 0x01
                var_b = item_id - 0x161
            elif item_id < 0x70:  # Glyphs
                sub_type = 0x02
                var_b = item_id
            else:
                sub_type = 0xFF
                var_b = item_id
            rom.write_to_file(data.pointer + 6, data.file, bytes([sub_type]))
            rom.write_to_file(data.pointer + 10, data.file, struct.pack("H", var_b))
        else:
            raise ValueError(f"Error! Location {location.name} has invalid location type {data.location_type}!")
