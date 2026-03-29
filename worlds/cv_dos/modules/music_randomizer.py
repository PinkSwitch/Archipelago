valid_area_music = [
    0x00,
    0x01,
    0x0B,
    0x0D,
    0x0E,
    0x0F,
    0x10,
    0x11,
    0x12,
    0x13,
    0x14,
    0x15,
    0x16,
    0x17,
    0x18
]

valid_boss_music = [
    0x02,
    0x03,
    0x05,
    0x06,
    0x1A,
    0x1B
]

boss_song_addresses = [
    0x381978,  # F. Armor
    0x364980,  # Balore
    0xF7558, # Dimitrii
    0x37E728, # Malphas
    0x0F8394, # Dario
    0x36BBA4, # P. Master
    0x39DDCC, # Gergoth
    0x37040C, # Rahab
    0x38E5F4, # Zephyr
    0x3A6BC8, # Bat Company
    0x39D0A0, # Paranoia
    0x39D09C, # Paranoia 2
    0xFA4CC, # Dario 2
    0x187E08, # Aguni
    0x3931F8, # Death
    0x3B0FB4, # Abaddon
    0xFF9BC, # Menace
    0x165544 # Soma

]

def area_music_randomizer(world, rom):
    music_pool = valid_area_music.copy()
    for i in range(0x11):
        if i in {0x0C, 0x0D, 0x0E, 0x0F}:
            continue  # Areas where music isn't used
        song = world.random.choice(music_pool)
        music_pool.remove(song)
        rom.write_bytes(0x9E634 + (i * 4), bytearray([song]))

def boss_music_randomizer(world, rom):
    for address in boss_song_addresses:
        song = world.random.choice(valid_boss_music)
        rom.write_bytes(address, bytearray([song]))