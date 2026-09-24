from typing import NamedTuple


class BossRoomData(NamedTuple):
    layer_pointer: int  # Pointer to where layer data is stored
    room_pointer: int  # Raw pointer of the room's tile data
    entity_end: int  # End of this room's entity list
    file: str  # Which file this room is in
    base_tile: int = 0x00  # Tile to replace floor with. Defaults to blank tile


room_data = {
    "Dark Chapel": BossRoomData(0x022E508D, 0x2563FC, 0x020AEB94, "overlay_8", 0x021B),
    "Dark Chapel Inner": BossRoomData(0x022E475D, 0x255ACC, 0x020AEB10, "overlay_8"),
    "Mine of Judgment": BossRoomData(0x022EF921, 0x23EC90, 0x020B236C, "overlay_7")
}

# Byte sequences of tiles that make up a valid segment of wall.
# This is not any existing graphics or room data, I patterned these using available tiles to use the minimum data
# necessary to still look decent.
byte_sequences = {
    "Dark Chapel": bytes.fromhex("""E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41
                                    E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41"""),

    "Dark Chapel Inner": bytes.fromhex("""E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41
                                          E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41"""),


    "Mine of Judgment": bytes.fromhex("""76 00 77 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 77 40 76 40
                                         86 00 87 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 87 40 86 40""")
}


def expand_rahab_room(rom, room):
    # TODO! Pinnacle has no background beneath its floor
    # TODO! Lost Village needs its own floor builder
    # TODO! Set Pinnacle's Base Tile to 4E
    import struct
    print(room)
    data = room_data[room]
    if room == "Dark Chapel Inner":
        is_chapel2 = True
        floor_offset = 0x40  # We want to copy the top floor, not the lower set
    else:
        is_chapel2 = False
        floor_offset = 0

    if room == "Dark Chapel":
        rom.write_to_file(0x020AEB8D, "arm9", bytearray([0x00]))  # We need to delete these entities in DC
        rom.write_to_file(0x020AEB81, "arm9", bytearray([0x00]))  # so that the waterline is able to spawn

    rom.write_to_file(data.layer_pointer, data.file, bytearray([0x02]))  # Mark this room as having 2 height
    # Repoint the layer to the new room
    rom.write_to_file(data.layer_pointer + 0x0B, data.file, struct.pack("I", 0x021C8564))

    rom.copy_bytes(data.room_pointer, 0x300, 0xF5384)  # First we need to copy the original room's data
    for i in range(6):  # Next we need to extend the walls downward.
        rom.write_to_file(0x021C8864 + (0x80 * i), "overlay_0", byte_sequences[room])

    if room != "Lost Village":  # Every room except for Village we can just copy the existing floor data.

        rom.copy_bytes(0xF5648 - floor_offset, 0x38, 0xF5948)  # Copy the room's original floor down
        for i in range(0x1C):
            # Clear out the original floor
            rom.write_to_file(0x021C8828 + (i * 2), "overlay_0", struct.pack("H", data.base_tile))

            if is_chapel2:
                #  We need to also clear the higher floor of Chapel 2
                rom.write_to_file(0x21C87E8 + (i * 2), "overlay_0", struct.pack("H", 0x00))

    if room == "Dark Chapel Inner":
        rom.write_to_file(0x21C881A, "overlay_0", bytearray([0x37, 0xC1, 0x50, 0x81, 0x50, 0x81]))  # Corner the ramp
        rom.write_to_file(0x21C881A + 0x340, "overlay_0", bytearray([0x50, 0x01, 0x50, 0x01, 0x50, 0x01]))  # Cleanup the last tiles

    rom.write_to_file(data.entity_end, "arm9", struct.pack("H", 0x8005))  # Tell the room to spawn a waterline
