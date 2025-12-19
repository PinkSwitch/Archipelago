from dataclasses import dataclass

viable_wall_souls = [
    "Skeleton Soul",
    "Zombie Soul",
    "Axe Armor Soul",
    "Student Witch Soul",
    "Warg Soul",
    "Bomber Armor Soul",
    "Amalaric Sniper Soul",
    "Cave Troll Soul",
    "Waiter Skeleton Soul",
    "Slime Soul",
    "Yorick Soul",
    "Une Soul",
    "Mandragora Soul",
    "Rycuda Soul",
    "Fleaman Soul",
    "Ripper Soul",
    "Guillotiner Soul",
    "Killer Clown Soul",
    "Malachi Soul",
    "Disc Armor Soul",
    "Great Axe Armor Soul",
    "Slaughterer Soul",
    "Hell Boar Soul",
    "Frozen Shade Soul",
    "Merman Soul",
    "Larva Soul",
    "Ukoback Soul",
    "Decarabia Soul",
    "Succubus Soul",
    "Slogra Soul",
    "Erinys Soul",
    "Homunculus Soul",
    "Witch Soul",
    "Fish Head Soul",
    "Mollusca Soul",
    "Dead Mate Soul",
    "Malacoda Soul",
    "Flame Demon Soul",
    "Aguni Soul",
    "Abaddon Soul",
]

@dataclass
class SpriteData:
    address: int
    height: int
    mirror_sprite: bool = False  # Sprites that need to be horizontally flipped

# TODO! If this is done as a proc, there IS no world here. GET THESE IN THE ROM!
# I know what to do. In the ROM, I can read the Soul value used to Destroy the wall, and THAT can be written in the main rom file

def set_souls_for_walls(world):
    if world.options.randomize_red_soul_walls:
        world.red_soul_walls = world.random.sample(viable_wall_souls, 4)
    else:
        world.red_soul_walls = ["Killer Clown Soul", "Axe Armor Soul", "Skeleton Soul", "Ukoback Soul"]
    
    world.important_souls.update(world.red_soul_walls)  # All of these souls instantly become important



def apply_souls_and_gfx(rom):
    enem_sprite_data_table = {
        "Skeleton Soul": SpriteData(0x16F00C0, 40, True),
        "Zombie Soul": SpriteData(0x163F680, 38, True),
        "Axe Armor Soul": SpriteData(0x10888F0, 26),
        "Student Witch Soul": SpriteData(0x13860B0, 37, True),
        "Warg Soul": SpriteData(0x11F58C0, 27, True),
        "Bomber Armor Soul": SpriteData(0x10CF520, 17),
        "Amalaric Sniper Soul": SpriteData(0x152A010, 64),
        "Cave Troll Soul": SpriteData(0x16BE040, 38, True),
        "Waiter Skeleton Soul": SpriteData(0x152CF00, 11),
        "Slime Soul": SpriteData(0x1488200, 16),
        "Yorick Soul": SpriteData(0x14F8D00, 8),
        "Une Soul": SpriteData(0x16EA720, 16),
        "Mandragora Soul": SpriteData(0x138C8C0, 26),
        "Rycuda Soul": SpriteData(0x1504DA0, 59, True),
        "Fleaman Soul": SpriteData(0x16E9520, 16, True),
        "Ripper Soul": SpriteData(0x1535D90, 4),
        "Guillotiner Soul": SpriteData(0x12B4040, 30),
        "Killer Clown Soul": SpriteData(0x10ED100, 58, True),
        "Malachi Soul": SpriteData(0x16D2E70, 46, True),
        "Disc Armor Soul": SpriteData(0x114B4F0, 42),
        "Great Axe Armor Soul": SpriteData(0x125C150, 80, True),
        "Slaughterer Soul": SpriteData(0x11DE000, 32, True),
        "Hell Boar Soul": SpriteData(0x12CE0C0, 34, True),
        "Frozen Shade Soul": SpriteData(0x13D4140, 53, True),
        "Merman Soul": SpriteData(0x16D6100, 52, True),
        "Larva Soul": SpriteData(0x132E100, 16),
        "Ukoback Soul": SpriteData(0x16EE880, 27, True),
        "Decarabia Soul": SpriteData(0x112A040, 46),
        "Succubus Soul": SpriteData(0x1463000, 32, True),
        "Slogra Soul": SpriteData(0x10A5110, 25, True),
        "Erinys Soul": SpriteData(0x11AFB30, 38, True),
        "Homunculus Soul": SpriteData(0x12D60C0, 50),
        "Witch Soul": SpriteData(0x1384000, 48, True),
        "Fish Head Soul": SpriteData(0x16DA040, 23, True),
        "Mollusca Soul": SpriteData(0x1263640, 38, True),
        "Dead Mate Soul": SpriteData(0x12BC710, 41, True),
        "Malacoda Soul": SpriteData(0x13DA000, 64, True),
        "Flame Demon Soul": SpriteData(0x12100A0, 21, True),
        "Aguni Soul": SpriteData(0x1060080, 43, True),
        "Abaddon Soul": SpriteData(0x1051870, 14, True),
    }

    for i in range(0x1801):
        rom.write_bytes(0x10D6000, bytearray([0xFF]))  # Blank out the original graphic

    for i, soul in enumerate(world.red_soul_walls):
        height = enem_sprite_data_table[soul].height
        starting_height = int(96 - height) / 2  # Calculate the rough center of the block, heightwise
        for j in range (height + 1):
            tile_row = rom.read_bytes(address + (0x30 * j), 0x0F)  # Read each row of the image
            if enem_sprite_data_table[soul].mirror_sprite:
                tile_row = mirror_tiles(tile_row)  # Sprites should face right. If they're not, mirror the image
                
            rom.write_bytes((0x10D6000 + (i * 0x10) + (j * 0x30) + (starting_height * 0x30)), tile_row)  # Write the current tile over the wall we made earlier


def mirror_tiles(tile_row) -> bytearray:
    pix_row = list(tile_row)  # Convert the bytes to a list
    front_tiles = pix_row[:8][::-1]
    back_tiles = pix_row[8:][::-1]

    tile_row = back_tiles + front_tiles  # Reverse the byte order
    tile_row = [((tile & 0x0F) << 4) | (tile >> 4) for tile in tile_row]  # Invert the nybbles of each byte
    return bytearray(tile_row)