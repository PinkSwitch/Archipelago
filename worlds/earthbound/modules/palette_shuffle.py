
palette_list = [
    0x00,  # Pyramid
    0x01,  # Underworld
    0x02,  # Cave of the Past
    0x03,  # Giygas's lair


    0x04,   # Onett daytime
    0x05,   # Onett night
    0x06,   # Onett memory/grayscale

    0x07,  # Twoson
    0x08,  # Happy-Happy village
    0x09,  # Happy-Happy restored
    0x0A,  # Two-Three tunnel

    0x0B,  # Threed Dark
    0x0C,  # Threed daytime

    0x0D,  # Fourside
    0x0E,  # Moonside

    0x0F,  # Magicant Main
    0x10,  # Road Tunnel
    0x11,  # Magicant Indoors
    0x12,  # Tents

    0x13,  # Peaceful Rest Valley
    0x14,  # Grapefruit Falls
    0x15,  # Saturn valley
    0x16,  # Deep Darkness
    0x17,  # Lilliput Steps
    0x18,  # Milky Well
    0x19,  # Deep Darkness with darkness effect

    0x1A,  # Summers

    0x1B,  # Dusty Dunes
    0x1C,  # Sky Runner scene

    0x1D,  # Dalaam
    0x1E,  # Dalaam Palace
    0x1F,  # Cave of the Present
    0x20,  # Pink Cloud
    0x21,  # Scaraba Sea
    0x22,  # ???

    0x23,  # Monotoli Offices
    0x24,  # Onett Hotel
    0x25,  # Red Threed house
    0x26,  # ???
    0x27,  # Threed Houses 1
    0x28,  # Threed Houses 2
    0x29,  # Pokey's house
    0x2A,  # Moonside Hospital

    0x2B,  # Onett House 1
    0x2C,  # Onett House 2
    0x2D,  # Onett house 3
    0x2E,  # ?
    0x2F,  # ?
    0x30,  # ?
    0x31,  # Onett House 4
    0x32,  # Ness's house memory

    0x33,  # Hospital 1
    0x34,  # Apple kid house
    0x35,  # ?
    0x36,  # Orange kid house
    0x37,  # Everdred's House
    0x38,  # ?
    0x39,  # Ness's room
    0x3A,  # Police station back room
    
    0x3B,  # Winters
    0x3C,  # ? Winters again
    0x3D,  # Night winters
    0x3E,  # Even darker winters

    0x3F,  # Hospitals 2
    0x40,
    0x41,
    0x42,
    0x43,  # Monotoli golden rooms
    0x44,  # Happy-Happy Stately building?
    0x45,  # Happy-Happy  House
    0x46,

    0x47,
    0x48,
    0x49,  # Fourside hotel room
    0x4A,
    0x4B,
    0x4C,
    0x4D,
    0x4E,

    0x4F,  # Monotoli lobby
    0x50,
    0x51,
    0x52,

    0x53,
    0x54,
    0x55,  # Fourside hotel room
    0x56,
    0x57,
    0x58,
    0x59,
    0x5A,

    0x5B,  # Scaraba

    0x5C,  # Dalaam house
    0x5D,  # Scaraba House
    0x5E,  # Happy Happy HQ
    0x5F  # Cafe backroom
]

good_palettes = {
    "Onett": [0x04, 0x05, 0x07, 0x09, 0x0B, 0x0C, 0x0D, 0x0E, 0x2A, 0x3E],
    "Giant Step": [],
    "Twoson": [0x04, 0x05, 0x07, 0x09, 0x0B, 0x0C, 0x0D, 0x0E, 0x2A, 0x3E],
    "Peaceful Rest Valley": [],
    "Happy-Happy Village": [],
    "Lilliput Steps": [],
    "Two-Three Tunnel": [],
    "Threed": [0x04, 0x05, 0x07, 0x09, 0x0B, 0x0C, 0x0D, 0x2A, 0x3E, 0x3F],
    "Winters": [0x3E],
}

good_palettes_plus = {
    "Onett": [0x01, 0x02, 0x06, 0x08, 0x0A, 0x13, 0x15, 0x16, 0x1A, 0x1B, 0x27, 0x5B],

}


def randomize_psi_palettes(world, rom):
    spell_palettes = []
    for i in range(34):
        spell_palettes.append(0x0CF47F + (i * 8))
    
    for i in range(7):
        spell_palettes.append(0x360710 + (i * 8))
        
    shuffled_palettes = spell_palettes.copy()

    if world.options.randomize_psi_palettes == 1:
        world.random.shuffle(shuffled_palettes)

    elif world.options.randomize_psi_palettes == 2:
        for i in range(0x010E):
            rom.write_bytes(0x0CF47F + i, bytearray([world.random.randint(0x00, 0xFF)]))

        for i in range(0x50):
            rom.write_bytes(0x36F710 + i, bytearray([world.random.randint(0x00, 0xFF)]))

    for index, pointer in enumerate(spell_palettes):
        rom.copy_bytes(pointer, 8, shuffled_palettes[index])
        