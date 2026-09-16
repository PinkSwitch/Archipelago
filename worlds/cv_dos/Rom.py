import hashlib
import os
import Utils
import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Sequence, NamedTuple
from .in_game_data import (global_weapon_table, base_weapons, valid_random_starting_weapons, global_soul_table,
                           easter_egg_table, warp_room_bits, world_version, global_item_table, common_filler_pool,
                           boss_list, enemy_table, global_armor_table)
from .modules.music_randomizer import area_music_randomizer, boss_music_randomizer
from .modules.boss_randomizer import write_bosses
from .modules.synthesis_randomizer import write_synthesis
from .modules.bullet_wall_randomizer import apply_souls_and_gfx
from Options import OptionError
from .Options import StartingWeapon, SoulRandomizer, SoulsanityLevel, GateItems
from .Items import soul_filler_table
from .modules.seal_shuffle import write_seals, randomize_seal_patterns
from .modules.set_goals import write_goal_triggers
from BaseClasses import ItemClassification
from .static_location_data import location_data_table

hash_us = "cc0f25b8783fb83cb4588d1c111bdc18"

base_enemy_address = 0x2078CAC
soul_check_table = 0x02308970
button_check_table = 0x02308b2c


class FilePointer(NamedTuple):
    rom_address: int
    base_address: int
    file_size: int

file_pointers = {
    "arm9": FilePointer(0x4000, 0x02000000, 0xC6B97),
    "overlay_0": FilePointer(0x000CB200, 0x0219E3E0, 0x0009235F),
    "overlay_1": FilePointer(0x0015D600, 0x02230A00, 0x00069F1F),
    "overlay_2": FilePointer(0x001C7600, 0x0229A920, 0x00003CDF),   """Sprite data that isn't stored in individual files."""   
    "overlay_3": FilePointer(0x001CB400, 0x0229E600, 0x0001B2FF),   """Sprite data that isn't stored in individual files."""
    "overlay_4": FilePointer(0x001E6800, 0x022B9900, 0x0001D57F),   """GFX wrappers."""
    "overlay_5": FilePointer(0x00203E00, 0x022D6E80, 0x0000361F),
    
    # SEKTOR ROOMS (6-22): Alle teilen sich im RAM Bank 0x022DA4A0!
    "overlay_6": FilePointer(0x00207600, 0x022DA4A0, 0x0002219F),
    "overlay_7": FilePointer(0x00229800, 0x022DA4A0, 0x00021F9F),
    "overlay_8": FilePointer(0x0024B800, 0x022DA4A0, 0x0001927F),
    "overlay_9": FilePointer(0x00264C00, 0x022DA4A0, 0x0001FD9F),
    "overlay_10": FilePointer(0x00284A00, 0x022DA4A0, 0x0001C61F),
    "overlay_11": FilePointer(0x002A1200, 0x022DA4A0, 0x0002551F),
    "overlay_12": FilePointer(0x002C6800, 0x022DA4A0, 0x00003BBF),
    "overlay_13": FilePointer(0x002CA400, 0x022DA4A0, 0x000186BF),
    "overlay_14": FilePointer(0x002E2C00, 0x022DA4A0, 0x0001DD5F),
    "overlay_15": FilePointer(0x00300A00, 0x022DA4A0, 0x0000CDBF),
    "overlay_16": FilePointer(0x0030D800, 0x022DA4A0, 0x0001783F),
    "overlay_17": FilePointer(0x00325200, 0x022DA4A0, 0x000246DF),
    "overlay_18": FilePointer(0x00349A00, 0x022DA4A0, 0x0000583F),
    "overlay_19": FilePointer(0x0034F400, 0x022DA4A0, 0x0000313F),
    "overlay_20": FilePointer(0x00352600, 0x022DA4A0, 0x0000881F),
    "overlay_21": FilePointer(0x0035AE00, 0x022DA4A0, 0x0000563F),
    "overlay_22": FilePointer(0x00360800, 0x022DA4A0, 0x0000313F),
    
    # SEKTOR ENEMY CODE (23-40): Alle teilen sich im RAM Bank 0x022FF9C0!
    "overlay_23": FilePointer(0x00363A00, 0x022FF9C0, 0x0000335F),
    "overlay_24": FilePointer(0x00366E00, 0x022FF9C0, 0x000037DF),
    "overlay_25": FilePointer(0x0036A600, 0x022FF9C0, 0x00005BFF),
    "overlay_26": FilePointer(0x00370200, 0x022FF9C0, 0x000042BF),
    "overlay_27": FilePointer(0x00374600, 0x022FF9C0, 0x0000333F),
    "overlay_28": FilePointer(0x00377A00, 0x022FF9C0, 0x00005A7F),
    "overlay_29": FilePointer(0x0037D600, 0x022FF9C0, 0x00002E9F),
    "overlay_30": FilePointer(0x00380600, 0x022FF9C0, 0x00003A5F),
    "overlay_31": FilePointer(0x00384200, 0x022FF9C0, 0x0000377F),
    "overlay_32": FilePointer(0x00387A00, 0x022FF9C0, 0x000032FF),
    "overlay_33": FilePointer(0x0038B600, 0x022FF9C0, 0x0000499F),
    "overlay_34": FilePointer(0x00390000, 0x022FF9C0, 0x000073DF),
    "overlay_35": FilePointer(0x00397400, 0x022FF9C0, 0x0000649F),
    "overlay_36": FilePointer(0x0039DA00, 0x022FF9C0, 0x00008F5F),
    "overlay_37": FilePointer(0x003A6A00, 0x022FF9C0, 0x00002FDF),
    "overlay_38": FilePointer(0x003A9A00, 0x022FF9C0, 0x0000725F),
    "overlay_39": FilePointer(0x003B0E00, 0x022FF9C0, 0x000019FF),
    "overlay_40": FilePointer(0x003B2800, 0x022FF9C0, 0x000014DF),
    
    # DEINE ERWEITERTE FREISPEICHER-BASIS MIT MOD-SCHUTZ
    "overlay_41": FilePointer(0x2F6DC00, 0x02308920, 0xC000),
    "bullet_wall_gfx": FilePointer(0x10D6000, 0x00000000, 0x1FFF)
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

    def read_direct(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def get_bytes(self) -> bytes:
        return bytes(self.file)
def patch_rom(world, rom, code_patch):
    from .modules.area_shuffle import patch_castle_connections
    
    rom.write_to_file(0x02308970, "overlay_41", code_patch)
    rom.name = f"{world.player}_{world.auth_id}"
    patch_name = bytearray(rom.name, "utf8")[:0x14]

    rom.write_to_file(0x02308A70, "overlay_41", patch_name)
    rom.write_to_file(0x02308A9C, "overlay_41", world_version.encode("ascii"))

    write_goal_triggers(world, rom)

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
    
    if world.player_name == "ironsoul":
        starting_armor = world.random.choice(["Casual Clothes", "Cloth Tunic", "Leather Armor", "Silk Robe"])
        starting_armor = global_armor_table.index(starting_armor)
        starting_weapon = world.random.choice(["Rapier", "Short Sword", "Claymore", "Mace", "Blunt Sword",
                                               "Axe", "Spear", "Handgun", "Brass Knuckles"])
        starting_weapon = global_weapon_table.index(starting_weapon)
        rom.write_to_file(0x02308E40, "overlay_41", bytearray([0x01]))
        rom.write_to_file(0x02308E41, "overlay_41", bytearray([0x01]))
        rom.write_to_file(0x02308E42, "overlay_41", bytearray([0x01]))
        rom.write_to_file(0x02308E43, "overlay_41", bytearray([0x01]))
        rom.write_to_file(0x02308E44, "overlay_41", struct.pack("H", starting_weapon))
        rom.write_to_file(0x02308E46, "overlay_41", struct.pack("H", starting_armor))

    rom.write_to_file(0x021F6068, "overlay_0", bytearray([starting_weapon]))

    warp_room = warp_room_bits[world.starting_warp_room]
    rom.write_to_file(0x02308a6e, "overlay_41", struct.pack("H", warp_room))

    if world.options.replace_menace_with_soma:
        rom.copy_bytes(0x158C3C, 8, 0x158C34)

    if world.options.remove_money_gates:
        rom.write_to_file(0x020A9661, "arm9", bytearray([0x00]))
        rom.write_to_file(0x020ACA2D, "arm9", bytearray([0x00]))
        rom.write_to_file(0x020B9135, "arm9", bytearray([0x00]))

    if world.options.disable_boss_seals:
        rom.write_to_file(0x21f1bf8, "overlay_0", bytearray([0x00]))
        rom.write_to_file(0x2213c04, "overlay_0", bytearray([0x01, 0x00, 0xA0, 0xE3]))

    if world.options.reveal_map:
        rom.write_to_file(0x20220C7, "arm9", bytearray([0xE1, 0x00, 0x00, 0xA0, 0xE1]))
        rom.write_to_file(0x2024BE8, "arm9", bytearray([0x00, 0x00, 0xE0, 0xE3, 0x1E, 0xFF, 0x2F]))

    if world.options.open_drawbridge:
        rom.write_to_file(0x21A2226, "overlay_0", bytearray([0xA0, 0xE1]))

    if world.options.reveal_hidden_walls:
        rom.write_to_file(0x20A1231, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20A17AD, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20A645D, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20A93e5, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20AC199, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20BAE21, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20BAE8D, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20BAFC5, "arm9", bytearray([0x00]))
        rom.write_to_file(0x20B44A9, "arm9", bytearray([0x00]))

    if not world.options.goal:
        rom.write_to_file(0x20B9508, "arm9", bytearray([0x60, 0xDC]))
        rom.write_to_file(0x20B950e, "arm9", bytearray([0xFF, 0xFE, 0xD0, 0xFF]))
        rom.write_to_file(0x20BDC30, "arm9", bytearray([0xD4, 0x94]))
        rom.write_to_file(0x20BDC38, "arm9", bytearray([0xD0]))

        rom.write_to_file(0x22EE17C, "overlay_13", bytearray([0x2F]))
        rom.write_to_file(0x22EE1BC, "overlay_13", bytearray([0x3F]))
        rom.write_to_file(0x22EE1FC, "overlay_13", bytearray([0x4F]))
        rom.write_to_file(0x22EE23C, "overlay_13", bytearray([0x5F]))
        rom.write_to_file(0x22EE27C, "overlay_13", bytearray([0x5F]))
        rom.write_to_file(0x22EE2bC, "overlay_13", bytearray([0x41]))
    if world.mine_status == "Disabled":
        rom.write_to_file(0x02308B1D, "overlay_41", bytearray([0xFF]))
        rom.write_to_file(0x2308B1E, "overlay_41", bytearray([0xFF]))

    if not world.options.goal:
        rom.write_to_file(0x2308B22, "overlay_41", bytearray([0xFF]))

    if world.options.one_screen_mode:
        rom.write_to_file(0x2308a6c, "overlay_41", bytearray([0x01]))

    if world.options.boost_speed:
        rom.write_to_file(0x222E489, "overlay_0", bytearray([0x20]))

    if world.options.death_link:
        rom.write_to_file(0x2308aad, "overlay_41", bytearray([0x01]))

    if world.options.no_mp_bat:
        rom.write_to_file(0x209d782, "arm9", bytearray([0x00]))

    rom.write_to_file(0x02308D7C, "overlay_41", bytearray([world.options.start_with_doppelganger.value]))

    if world.options.randomize_seal_patterns:
        randomize_seal_patterns(world, rom)

    rom.write_to_file(0x2308AAE, "overlay_41", struct.pack("H", world.options.experience_percentage))
    rom.write_to_file(0x2308AB0, "overlay_41", struct.pack("H", world.options.soul_drop_percentage))

    soul_total = set(world.common_souls)
    if world.options.soulsanity_level:
        soul_total |= world.uncommon_souls
    if world.options.soulsanity_level == SoulsanityLevel.option_rare:
        soul_total |= world.rare_souls
    soul_total = list(soul_total)

    for i, soul in enumerate(soul_total):
        rom.write_to_file(0x2308ab4 + i, "overlay_41", bytearray([global_soul_table.index(soul)]))

    if world.options.soul_randomizer == SoulRandomizer.option_shuffled:
        vanilla_souls = [soul for soul in world.important_souls if soul not in world.excluded_static_souls]
        shuffled_keys = [item for item in soul_filler_table.copy() if item not in vanilla_souls]
        souls_output = {key: key for key in soul_filler_table.copy()}
        shuffled_vals = world.random.sample(shuffled_keys, k=len(shuffled_keys))
        for key, val in zip(shuffled_keys, shuffled_vals):
            souls_output[key] = val

        for soul in souls_output:
            soul_data = bytearray([global_soul_table.index(souls_output[soul]), 0x05])
            rom.write_to_file(soul_check_table + (global_soul_table.index(soul) * 2), "overlay_41", soul_data)

    elif world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        rom.write_to_file(0x2308a69, "overlay_41", bytearray([0x01]))

    if world.options.shop_randomizer:
        shop_pool = common_filler_pool.copy()
        shop_pool = [item for item in shop_pool if item not in ["Potion", "Mind Up", "Claymore"]]
        for i in range(10):
            item = world.random.choice(shop_pool)
            rom.write_to_file(0x209df14 + i, "arm9", bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        for i in range(18):
            item = world.random.choice(shop_pool)
            rom.write_to_file(0x209df38 + i, "arm9", bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        for i in range(19):
            item = world.random.choice(shop_pool)
            rom.write_to_file(0x209df4f + i, "arm9", bytearray([global_item_table.index(item) + 1]))
            shop_pool.remove(item)

        rom.write_to_file(0x209df4e, "arm9", bytearray([global_item_table.index("Claymore") + 1]))

    if world.options.shuffle_enemy_drops:
        drop_pool = common_filler_pool.copy()
        for enemy in enemy_table:
            if enemy in boss_list:
                continue

            index = (base_enemy_address + (enemy_table.index(enemy) * 0x24))
            common_drop_address = index + 8
            rare_drop_address = index + 10
            if world.random.randint(0, 99) < 45:
                item = world.random.choice(drop_pool)
                common_item = global_item_table.index(item) + 1
            else:
                common_item = 0

            if world.random.randint(0, 99) < 29:
                item = world.random.choice(drop_pool)
                rare_item = global_item_table.index(item) + 1
            else:
                rare_item = 0

            rom.write_to_file(common_drop_address, "arm9", bytearray([common_item]))
            rom.write_to_file(rare_drop_address, "arm9", bytearray([rare_item]))


    if getattr(world.options, "enemy_randomizer", False):
        from .modules import enemy_randomizer
        enemy_randomizer.write_enemies(world, rom, mode="normal")
        print(f"[{world.player_name}] Gegner-Mischer erfolgreich injiziert!")


    write_synthesis(world, rom)
    write_seals(world, rom)
    patch_castle_connections(world, rom)

    if world.options.boss_shuffle:
        write_bosses(world, rom)

    if world.options.area_music_randomizer:
        area_music_randomizer(world, rom)

    if world.options.boss_music_randomizer:
        boss_music_randomizer(world, rom)

    if world.options.randomize_red_soul_walls:
        rom.write_to_file(0x2308b28, "overlay_41", bytearray([0x01]))
        
        # 🛠️ ORIGINAL-RESTORE: Konvertiert das Set in eine Liste, damit die Indizes 
        # der vier originalen roten Seelen (Red Souls) exakt zugewiesen werden.
        walls_list = list(world.red_soul_walls)
        rom.write_to_file(0x0222BDA0, "overlay_0", bytearray([global_soul_table.index(walls_list[0])]))
        rom.write_to_file(0x0222BD9A, "overlay_0", bytearray([global_soul_table.index(walls_list[1])]))
        rom.write_to_file(0x0222BD94, "overlay_0", bytearray([global_soul_table.index(walls_list[2])]))
        rom.write_to_file(0x0222BDA6, "overlay_0", bytearray([global_soul_table.index(walls_list[3])]))

    if world.options.gate_items == GateItems.option_buttonsanity:
        rom.write_to_file(0x2308b29, "overlay_41", bytearray([0x01]))

    if world.options.hard_mode:
        rom.write_to_file(0x2308b2a, "overlay_41", bytearray([0x01]))

    if world.options.passive_soul_eater_ring:
        rom.write_to_file(0x2308b2b, "overlay_41", bytearray([0x01]))
        
    patch_locations(world, rom, world.get_locations())
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
        ("adjust_item_positions", []),
        ("apply_modifiers", []),
        ("modify_soulwall_gfx", [])
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


class DoSPatchExtensions(APPatchExtension):
    game = "Castlevania: Dawn of Sorrow"

    @staticmethod
    def adjust_item_positions(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_from_file(0x2308a9c, "overlay_41", 15)
        version = version_check.rstrip(b"\x69").decode("ascii")
        if version != world_version:
            raise Exception(f"Version Mismatch! Generated: {version}, Installed: {world_version}")

        for check in location_data_table:
            if location_data_table[check].location_type != "Normal":
                continue
            address = location_data_table[check].pointer
            item_type = int.from_bytes(rom.read_from_file(address + 6, "arm9", 1))
            item_id = int.from_bytes(rom.read_from_file(address + 10, "arm9", 1))
            if (item_type == 0x01 and item_id < 4) or (item_type == 0x02 and item_id >= 0x3D):
                y_pos = struct.unpack("H", rom.read_from_file(address + 2, "arm9", 2))[0]
                y_pos -= 10
                rom.write_to_file(address + 2, "arm9", struct.pack("H", y_pos))

        return rom.get_bytes()

    @staticmethod
    def apply_modifiers(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        exp_multiplier = struct.unpack("H", rom.read_from_file(0x2308aae, "overlay_41", 2))[0] / 100
        soul_chance_multiplier = struct.unpack("H", rom.read_from_file(0x2308ab0, "overlay_41", 2))[0] / 100

        for enemy in enemy_table:
            address = (base_enemy_address + (enemy_table.index(enemy) * 0x24))
            exp_address = address + 18
            exp = struct.unpack("H", rom.read_from_file(exp_address, "arm9", 2))[0]
            exp = int(min(0xFFFF, (exp * exp_multiplier)))
            rom.write_to_file(exp_address, "arm9", struct.pack("H", exp))

            soul_chance_address = address + 20
            soul_chance = int.from_bytes(rom.read_from_file(soul_chance_address, "arm9", 1))
            if soul_chance:
                soul_chance = int(min(0xFF, (soul_chance * soul_chance_multiplier)))
                rom.write_to_file(soul_chance_address, "arm9", bytearray([soul_chance]))

        return rom.get_bytes()

    @staticmethod
    def modify_soulwall_gfx(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        soul_wall_randomizer = int.from_bytes(rom.read_from_file(0x2308b28, "overlay_41", 1))
        if soul_wall_randomizer:
            apply_souls_and_gfx(rom)
        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash_us != basemd5.hexdigest():
            raise Exception('Base ROM Hash Mismatch!')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    from worlds.cv_dos import DoSWorld
    if not file_name:
        file_name = DoSWorld.settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def get_item_data(world, item) -> tuple:
    if item.player == world.player:
        item_type = (item.code & 0xFF00) >> 8
        item_id = item.code & 0x00FF
        item_color = 0
    else:
        item_type = 2
        if ItemClassification.progression in item.classification:
            item_id = 0x3B
            item_color = 0x0C
        elif ItemClassification.useful in item.classification:
            item_id = 0x3A
            item_color = 0x07
        elif ItemClassification.trap in item.classification:
            item_id = 0x3A
            item_color = 0x06
        else:
            item_id = 0x3A
            item_color = 0x0E
    return item_id, item_type, item_color


def patch_locations(world, rom, locations) -> None:
    for location in locations:
        if not location.address:
            continue
        item = location.item
        data = location_data_table[location.name]
        item_struct = get_item_data(world, item)
        item_id = item_struct[0]
        item_type = item_struct[1]
        item_color = item_struct[2]

        if data.location_type == "Normal":
            address = data.pointer
            if item.name in global_soul_table and item.player == world.player:
                item_id = 0x3C << 8 | item_id
                item_type = 0x02
                rom.write_to_file(address + 9, "arm9", struct.pack("H", item_id))
            else:
                item_id = item_color << 8 | item_id
                rom.write_to_file(address + 9, "arm9", struct.pack(">H", item_id))
            rom.write_to_file(address + 6, "arm9", bytearray([item_type]))

        elif data.location_type == "Soul":
            if item_color:
                item_type = item_color
            item_struct_val = (item_type << 8) | item_id
            index = (global_soul_table.index(location.name) * 2)
            rom.write_to_file(soul_check_table + index, "overlay_41", struct.pack("H", item_struct_val))
        elif data.location_type == "Easter Egg":
            if item_color:
                item_type = item_color
            rom.write_to_file(data.pointer + 11, "arm9", bytearray([item_type]))
            rom.write_to_file(easter_egg_table[location.name], "overlay_0", struct.pack("H", item_id))
        elif data.location_type == "Button":
            address = button_check_table + ((location.address - 0x200) * 4)
            rom.write_to_file(address, "overlay_41", bytearray([item_type, item_id, item_color]))
        else:
            raise ValueError(f"Error! Location {location.name} has invalid location type {data.location_type}!")
