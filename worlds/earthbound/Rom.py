import hashlib
import os
import Utils
import typing
import bsdiff4
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .local_data import (item_id_table, location_dialogue, present_locations, psi_item_table, npc_locations, psi_locations, 
                         special_name_table, character_item_table, character_locations, locker_locations, starting_psi_table, item_space_checks,
                         special_name_overrides, protection_checks, badge_names, protection_text)
from .text_data import barf_text, eb_text_table, text_encoder
from .flavor_data import flavor_data
from .enemy_data import combat_regions, scale_enemies
from BaseClasses import ItemClassification, CollectionState
from settings import get_settings
from typing import TYPE_CHECKING
from logging import warning
#from .local_data import local_locations

if TYPE_CHECKING:
    from . import EarthBoundWorld
valid_hashes = ["a864b2e5c141d2dec1c4cbed75a42a85", #Cartridge
                "6d71ccc8e2afda15d011348291afdf4f"]#VC


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
    starting_area_coordinates = {
                    0: [0x50, 0x04, 0xB5, 0x1F], #North Onett
                    1: [0x52, 0x06, 0x4C, 0x1F], #Onett
                    2: [0xEF, 0x22, 0x41, 0x1F], #Twoson
                    3: [0x53, 0x06, 0x85, 0x1D], #Happy Happy
                    4: [0x55, 0x24, 0x69, 0x1D], #Threed
                    5: [0x60, 0x1D, 0x30, 0x01], #Saturn Valley
                    6: [0xAB, 0x10, 0xF3, 0x09], #Fourside
                    7: [0xE3, 0x09, 0xA3, 0x1D], #Winters
                    8: [0xCB, 0x24, 0x7B, 0x1E], #Summers
                    9: [0xD0, 0x1E, 0x31, 0x1D], #Dalaam
                    10: [0xC7, 0x1F, 0x37, 0x19], #Scaraba
                    11: [0xDD, 0x1B, 0xB7, 0x17], #Deep Darkness
                    12: [0xD0, 0x25, 0x47, 0x18], #Tenda Village
                    13: [0x9C, 0x00, 0x84, 0x17], #Lost Underworld
                    14: [0x4B, 0x11, 0xAD, 0x18] #Magicant
    }
    world.start_items = []
    world.handled_locations = []
    
    for item in world.multiworld.precollected_items[world.player]:
        world.start_items.append(item.name)

    if world.options.random_start_location != 0:
        rom.write_bytes(0x0F96C2, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9618, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9629, bytearray([0x69, 0x00]))#Block Northern Onett
    else:
        rom.write_bytes(0x00B66A, bytearray([0x06]))#Fix starting direction
    
    rom.write_bytes(0x01FE9B, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE9E, bytearray(starting_area_coordinates[world.start_location][2:4]))#Start position

    rom.write_bytes(0x01FE91, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE8B, bytearray(starting_area_coordinates[world.start_location][2:4]))#Respawn position

    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x04FD72, bytearray([world.options.sanctuaries_required.value + 2]))
    else:
        rom.write_bytes(0x04FD72, bytearray([0xFF]))

    if world.options.giygas_required == 0:
        rom.write_bytes(0x2E9C29, bytearray([0x10, 0xA5]))

    if world.options.magicant_mode == 2:
        rom.write_bytes(0x04FD71, bytearray([world.options.sanctuaries_required.value + 1]))
        rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE])) #Alt goal magicant sets the credits
    elif world.options.magicant_mode == 1:
        rom.write_bytes(0x2E9C29, bytearray([0x00, 0xA5]))
        if world.options.giygas_required:
            rom.write_bytes(0x2EA26A, bytearray([0x08, 0xD9, 0x9B, 0xEE])) #Give stat boost if magicant + giygas required
        else:
            rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE])) #If no giygas, set credits
    elif world.options.magicant_mode == 3:
        rom.write_bytes(0x2EA26A, bytearray([0x08, 0x0F, 0x9C, 0xEE]))# Give only stat boost if set to boost

    rom.write_bytes(0x04FD70, bytearray([world.options.sanctuaries_required.value]))

    if world.options.monkey_caves_mode == 2:
        rom.write_bytes(0x062B87, bytearray([0x0A, 0x28, 0xCA, 0xEE]))
    elif world.options.monkey_caves_mode == 3:
        rom.write_bytes(0x0F1388, bytearray([0x03, 0xCA, 0xEE]))

    #Todo: sanc alt goal, change sanc script

    for location in world.multiworld.get_locations(player):
        if location.address:
            receiver_name = world.multiworld.get_player_name(location.item.player)
            name = location.name
            item = location.item.name
            item_name_loc = (((location.address - 0xEB0000) * 128) + 0x3F0000)
            item_text = bytearray(0)
            player_text = bytearray(0)
            for char in location.item.name[:128]:
                if char in eb_text_table:
                    item_text.extend(eb_text_table[char])
                else:
                    item_text.extend([0x6F])
            item_text.extend([0x00])
            player_name_loc = (((location.address - 0xEB0000) * 48) + 0x3F8000)
            for char in receiver_name[:48]:
                if char in eb_text_table:
                    player_text.extend(eb_text_table[char])
                else:
                    player_text.extend([0x6F])
            player_text.extend([0x00])
            rom.write_bytes(item_name_loc, bytearray(item_text))
            rom.write_bytes(player_name_loc, bytearray(player_text))

            if item not in item_id_table or location.item.player != location.player:
                item_id = 0xAD
            elif item == "Lucky Sandwich":
                item_id = world.random.randint(0xE2, 0xE7)
            else:
                item_id = item_id_table[item]

            if name in location_dialogue:
                for i in range(len(location_dialogue[name])):
                    if location.item.player != location.player:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x17, location.address - 0xEB0000]))
                    elif item in item_id_table:
                        rom.write_bytes(location_dialogue[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x16, special_name_table[item][0]]))

            if name in present_locations:
                world.handled_locations.append(name)
                if item == "Nothing": #I can change this to "In nothing_table" later todo: make it so nonlocal items do not follow this table
                    rom.write_bytes(present_locations[name], bytearray([0x00, 0x00, 0x01]))
                elif location.item.player != location.player:
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00, 0x00, (location.address - 0xEB0000)]))
                elif item in item_id_table:
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00]))
                elif item in psi_item_table:
                    rom.write_bytes(present_locations[name], bytearray([psi_item_table[item], 0x00, 0x02]))
                elif item in character_item_table:
                    rom.write_bytes(present_locations[name], bytearray([character_item_table[item][0], 0x00, 0x03]))

            if name in npc_locations:
                world.handled_locations.append(name)
                for i in range(len(npc_locations[name])):
                    if item in item_id_table or location.item.player != location.player:
                        rom.write_bytes(npc_locations[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(npc_locations[name][i] - 3, bytearray([0x0E, 0x00, 0x0E, special_name_table[item][4]]))
                        rom.write_bytes(npc_locations[name][i] + 2, bytearray([0xA5, 0xAA, 0xEE]))

            if name in psi_locations:
                world.handled_locations.append(name)
                if item in special_name_table and location.item.player == location.player:
                    rom.write_bytes(psi_locations[name][0], bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(psi_locations[name][0] + 4, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
                else:
                    rom.write_bytes(psi_locations[name][0], bytearray(psi_locations[name][1:4]))
                    rom.write_bytes(psi_locations[name][4], bytearray([item_id]))

            if name in character_locations:
                world.handled_locations.append(name)
                if item in character_item_table and location.item.player == location.player:
                    rom.write_bytes(character_locations[name][0], bytearray(special_name_table[item][1:4]))
                    if name == "Snow Wood - Bedroom": #Use lying down sprites for the bedroom check
                        rom.write_bytes(character_locations[name][1], bytearray(character_item_table[item][2:4]))
                        rom.write_bytes(0x0FB0D8, bytearray([0x06]))
                    else:
                        rom.write_bytes(character_locations[name][1], bytearray([character_item_table[item][1]]))
                elif item in psi_item_table and location.item.player == location.player:
                    rom.write_bytes(character_locations[name][0], bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x62]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x70, 0xF9, 0xD5]))
                else:
                    rom.write_bytes(character_locations[name][0], bytearray(character_locations[name][4:7]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x97]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x18, 0xF9, 0xD5]))
                    rom.write_bytes(character_locations[name][3], bytearray([item_id]))
                if name == "Deep Darkness - Barf Character":
                    if item in character_item_table and location.item.player == location.player:
                        rom.write_bytes(0x2EA0E2, bytearray(barf_text[item][0:3]))
                        rom.write_bytes(0x2EA0E8, bytearray(barf_text[item][3:6]))
                    elif item in psi_item_table and location.item.player == location.player:
                        rom.write_bytes(0x2EA0E2, bytearray([0x98, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xF7, 0xC4, 0xEE]))
                    else:
                        rom.write_bytes(0x2EA0E2, bytearray([0x6A, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xB4, 0xC4, 0xEE]))
            
            if name in locker_locations:
                world.handled_locations.append(name)
                if item in item_id_table or location.item.player != location.player:
                    rom.write_bytes(locker_locations[name][0], bytearray([0xFF]))
                    rom.write_bytes(locker_locations[name][1], bytearray([item_id]))
                elif item in psi_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x02]))
                    rom.write_bytes(locker_locations[name][1], bytearray([psi_item_table[item]]))
                elif item in character_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x03]))
                    rom.write_bytes(locker_locations[name][1], bytearray(character_item_table[item]))

            if name == "Poo Starting Item":
                world.handled_locations.append(name)
                if item in item_id_table and location.item.player == location.player:
                    rom.write_bytes(0x15F63C, bytearray([item_id]))
                else:
                    rom.write_bytes(0x15F63C, bytearray([0x00])) #Don't give anything if the item doesn't have a tangible ID

                if item in special_name_table and location.item.player == location.player: #Apply a special script if teleport or character
                    rom.write_bytes(0x15F7F6, bytearray(special_name_table[item][1:4]))
                    rom.write_bytes(0x2EC618, bytearray([special_name_table[item][4]]))
                    rom.write_bytes(0x2EC61A, bytearray([0xA5, 0xAA, 0xEE]))
            if name not in world.handled_locations:
                warning(f"{name} not placed in {world.multiworld.get_player_name(world.player)}'s EarthBound world. Something went wrong here.")
            
            if name in item_space_checks:
                if item not in item_id_table or location.item.player != location.player:
                    if len(item_space_checks[name]) == 4:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                    else:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                        rom.write_bytes(item_space_checks[name][4], bytearray(item_space_checks[name][5:8]))

            if name in special_name_overrides:
                if location.item.player != location.player:
                    rom.write_bytes(special_name_overrides[name], bytearray([0x1C, 0xB7, location.address - 0xEB0000]))
                else:
                    rom.write_bytes(special_name_overrides[name], bytearray([0x01, 0x01, 0x01]))

    if world.options.skip_prayer_sequences:
        rom.write_bytes(0x07BC96, bytearray([0x02]))
        rom.write_bytes(0x07BA2C, bytearray([0x02]))
        rom.write_bytes(0x07BAC7, bytearray([0x02]))
        rom.write_bytes(0x07BB38, bytearray([0x02]))
        rom.write_bytes(0x07BBF3, bytearray([0x02])) 
        rom.write_bytes(0x07BC56, bytearray([0x02])) 
        rom.write_bytes(0x07B9A1, bytearray([0x1f, 0xeb, 0xff, 0x02, 0x1f, 0x1f, 0xca, 0x01, 0x06, 0x1f, 0x1f, 0x72, 0x01, 0x06, 0x02])) #Clean up overworld stuff

    if world.options.easy_deaths:
        rom.write_bytes(0x2EBFF9, bytearray([0x0A]))
        rom.write_bytes(0x04C7CE, bytearray([0x5C, 0x8A, 0xFB, 0xEF]))#Jump to code that restores the party
        rom.write_bytes(0x04C7D4, bytearray([0xEA, 0xEA, 0xEA]))
        #rom.write_bytes(0x04C7DA, bytearray([0xEA, 0xEA]))#Stop the game from zeroing stuff
        rom.write_bytes(0x0912F2, bytearray([0x0A, 0xFE, 0xBF, 0xEE]))
        rom.write_bytes(0x2EBFFE, bytearray([0x00, 0x1B, 0x04, 0x15, 0x38, 0x1F, 0x81, 0xFF, 0xFF, 0x1B, 0x04, 0x0A, 0xF7, 0x12, 0xC9]))#Hospitals = 0$
        rom.write_bytes(0x04C822, bytearray([0xEA, 0xEA, 0xEA, 0xEA]))

    if world.options.magicant_mode == 2:
        rom.write_bytes(0x077629, bytearray([item_id_table[world.magicant_junk[0]]]))
        rom.write_bytes(0x0FF25C, bytearray([item_id_table[world.magicant_junk[1]]]))
        rom.write_bytes(0x0FF27E, bytearray([item_id_table[world.magicant_junk[2]]]))
        rom.write_bytes(0x0FF28F, bytearray([item_id_table[world.magicant_junk[3]]]))
        rom.write_bytes(0x0FF2A0, bytearray([item_id_table[world.magicant_junk[4]]]))
        rom.write_bytes(0x0FF26D, bytearray([item_id_table[world.magicant_junk[5]]]))

    rom.write_bytes(0x02EC1AA, bytearray([world.options.sanctuaries_required.value]))
    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x02EC1E2, bytearray([0xFD, 0xC1, 0xEE]))

    if world.options.magicant_mode == 1:
        rom.write_bytes(0x2EC1D8, bytearray([0x33, 0xC2, 0xEE]))
    elif world.options.magicant_mode == 2:
        rom.write_bytes(0x2EC1D8, bytearray([0x6A, 0xC2, 0xEE]))
    
    flavor_address = 0x3FAF10
    for i in range(4):
        rom.write_bytes(flavor_address, bytearray(world.flavor_text[i]))
        flavor_addr = flavor_address - 0x3F0000
        flavor_addr = struct.pack("H", flavor_addr)
        rom.write_bytes(world.flavor_pointer[i], flavor_addr)
        flavor_address += len(world.flavor_text[i])

    rom.write_bytes(0x202008, bytearray(flavor_data[world.available_flavors[0]]))
    rom.write_bytes(0x202048, bytearray(flavor_data[world.available_flavors[1]]))
    rom.write_bytes(0x202088, bytearray(flavor_data[world.available_flavors[2]]))
    rom.write_bytes(0x2020C8, bytearray(flavor_data[world.available_flavors[3]]))

    rom.write_bytes(0x048037, bytearray(world.lumine_text))
    starting_item_address = 0
    starting_psi = 0
    starting_char = 0
    starting_psi_types = []
    starting_character_count = []
    for item in world.multiworld.precollected_items[player]:
        if item.name in item_id_table:
            rom.write_bytes(0x17FC70 + starting_item_address, bytearray([item_id_table[item.name]]))
            starting_item_address += 1
        elif item.name in psi_item_table:
            if item.name != "Progressive Poo PSI":
                if item.name not in starting_psi_types:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
            else:
                if starting_psi_types.count(item.name) < 2:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
        elif item.name in character_item_table:
            if item.name not in starting_character_count:
                rom.write_bytes(0x17FC8D + starting_char, bytearray([character_item_table[item.name][1]]))
                starting_character_count.append(item.name)
                starting_char += 1

    world.Paula_placed = False
    world.Jeff_placed = False
    world.Poo_placed = False
    for sphere_number, sphere in enumerate(world.multiworld.get_spheres(), start=1):
        for location in sphere:
            if location.item.name in ["Paula", "Jeff", "Poo"] and not getattr(world, f"{location.item.name}_placed"):
                setattr(world, f"{location.item.name}_region", location.parent_region.name)
                setattr(world, f"{location.item.name}_placed", True)

    scale_enemies(world, rom)
    world.badge_name = badge_names[world.franklin_protection]
    world.badge_name = text_encoder(world.badge_name, eb_text_table, 23)
    world.badge_name.extend([0x00])
    rom.write_bytes(0x17FCD0, world.starting_money)
    rom.write_bytes(0x17FCE0, world.prayer_player)
    rom.write_bytes(0x155027, world.badge_name)

    for element in world.franklinbadge_elements:
        for address in protection_checks[element]:
            if element == world.franklin_protection:
                rom.write_bytes(address, [0xF0])
            else:
                rom.write_bytes(address, [0x80])
    rom.write_bytes(0x2EC909, bytearray(protection_text[world.franklin_protection][0:3])) #help text
    rom.write_bytes(0x2EC957, bytearray(protection_text[world.franklin_protection][3:6]))# battle text
    from Main import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x00FFC0, rom.name)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class EBProcPatch(APProcedurePatch, APTokenMixin):
    hash = valid_hashes
    game = "EarthBound"
    patch_file_ending = ".apeb"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["earthbound_basepatch.bsdiff4"]),
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
        rom_hash = basemd5.hexdigest
        if basemd5.hexdigest() not in valid_hashes:
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


#Fix hint text, I have a special idea where I can give it info on a random region
