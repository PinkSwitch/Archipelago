import hashlib
import os
import Utils
import typing
import bsdiff4
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .local_data import item_id_table, location_dialogue, present_locations, psi_item_table, npc_locations, psi_locations, special_name_table, character_item_table, character_locations, locker_locations
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


    if world.options.random_start_location != 0:
        rom.write_bytes(0x0F96C2, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9618, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9629, bytearray([0x69, 0x00]))#Block Northern Onett
    else:
        rom.write_bytes(0x00B66A, bytearray([0x06]))#Fix starting direction
    
    rom.write_bytes(0x01FE9B, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE9E, bytearray(starting_area_coordinates[world.start_location][2:4]))#Start position

    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x04FD72, bytearray(world.options.sanctuaries_required.value + 2))

    if world.options.magicant_mode == 2:
        rom.write_bytes(0x04FD71, bytearray(world.options.sanctuaries_required.value + 1))
    elif world.options.magicant_mode == 1:
        rom.write_bytes(0x2E9C29, bytearray([0x01, 0x95, 0xEE])) #Replace Sanctuary goal with Magicant if forced goal

    rom.write_bytes(0x04FD70, bytearray(world.options.sanctuaries_required.value))
    if world.options.giygas_required:
        if world.options.magicant_mode == 1:
            rom.write_bytes(0x2EA26A, bytearray([0xFF])) #Change Magicant to absorb FIX THIS!!!!!!!!!!!!!!!!!!
    else:
        if world.options.magicant_mode == 1:
            rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE])) #Change Magicant to win if required and goal
        else:
            rom.write_bytes(0x2E9C29, bytearray([0x10, 0xA5, 0xEE])) #If no final boss, write goal at sanc

    for location in world.multiworld.get_locations(player):
        if location.address:
            name = location.name
            item = location.item.name
            if item not in item_id_table:
                item_id = 0xAD
            elif item == "Lucky Sandwich":
                item_id = world.random.randint(0xE2, 0xE7)
            else:
                item_id = item_id_table[item]

            if name in location_dialogue:
                for i in range(len(location_dialogue[name])):
                    if item in item_id_table or location.item.player != location.player:
                        rom.write_bytes(location_dialogue[name][i], bytearray([item_id]))
                    elif item in [psi_item_table] or [character_item_table]:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x16, special_name_table[item][0]]))

            if name in present_locations:
                if item == "Nothing": #I can change this to "In nothing_table" later todo: make it so nonlocal items do not follow this table
                    rom.write_bytes(present_locations[name], bytearray([0x00, 0x01]))
                elif item in item_id_table or location.item.player != location.player:
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00]))
                elif item in psi_item_table:
                    rom.write_bytes(present_locations[name], bytearray([psi_item_table[item], 0x00, 0x02]))
                elif item in character_item_table:
                    rom.write_bytes(present_locations[name], bytearray([character_item_table[item], 0x00, 0x03]))

            elif name in npc_locations:
                for i in range(len(npc_locations[name])):
                    if item in item_id_table or location.item.player != location.player:
                        rom.write_bytes(npc_locations[name][i], bytearray([item_id]))
                    elif item in [psi_item_table] or [character_item_table]:
                        rom.write_bytes(npc_locations[name][i] -3, bytearray([0x0E, 0x00, 0x0E, special_name_table[item][4]]))
                        rom.write_bytes(npc_locations[name][i] +2, bytearray([0xA5, 0xAA, 0xEE]))

            elif name in psi_locations:
                if item in special_name_table:
                    rom.write_bytes(psi_locations[name][0], bytearray(special_name_table[item][1:4]))
                else:
                    rom.write_bytes(psi_locations[name], bytearray(psi_locations[name][1:4]))
                    rom.write_bytes(psi_locations[name][5], bytearray([item_id]))

            elif name in character_locations:
                if item in character_item_table:
                    rom.write_bytes(character_locations[name][0], bytearray(special_name_table[item][1:4]))
                    if name == "Snow Wood - Bedroom":#Use lying down sprites for the bedroom check
                        rom.write_bytes(character_locations[name][1], bytearray([character_item_table[item][1]]))
                    else:
                        rom.write_bytes(character_locations[name][1], bytearray(character_item_table[item][1:4]))
                elif item in psi_item_table:
                    rom.write_bytes(character_locations[name][0], bytearray([special_name_table[item][1:4]]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x62]))
                    rom.write_bytes(character_locations[name][2], bytearray([0xE0, 0xF8, 0xD5]))
                else:
                    rom.write_bytes(character_locations[name][0], bytearray(character_locations[name][4:7]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x97]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x18, 0xF9, 0xD5]))
                    rom.write_bytes(character_locations[name][3], bytearray([item_id]))

            elif name in locker_locations:
                if item in item_id_table or location.item.player != location.player:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x00]))
                    rom.write_bytes(locker_locations[name][1], bytearray(item_id))
                elif item in psi_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x02]))
                    rom.write_bytes(locker_locations[name][1], bytearray(psi_item_table[item]))
                elif item in character_item_table:
                    rom.write_bytes(locker_locations[name][0], bytearray([0x03]))
                    rom.write_bytes(locker_locations[name][1], bytearray(character_item_table[item]))
            else:
                print(f"WARNING: "+name +" NOT PLACED")
        

    from Main import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x00FFC0, rom.name)

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


#Write sanctuary count figure later
#Fix NPC item names around Fourside, Moonside one broke
#Remove hint man text, give it an area i wrote this down
#Write Poo's starting item...? I can do this by setting some arbitrary rom address to an item, and having Poo check it.
#log tpt stuff when interacting with npcs...?
#Think about getting items from NPCs. Maybe I can insert that GetItemNamecall to more scripts...
#NPC teleports have weird line beaks; garbage cans need line breaks
#Saturn valley gave me magicant huh