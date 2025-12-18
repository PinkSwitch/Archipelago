@dataclass
class SpriteData:
    address: int
    height: int
    mirror_sprite: bool = False  # Sprites that need to be horizontally flipped


enem_sprite_data_table = {
    "Skeleton Soul": SpriteData(0x16F00C0, 40, True),
    "Zombie Soul": SpriteData(0x163F680, 38, True),
    "Axe Armor Soul": SpriteData(0x10888F0, 26),
    "Student Witch Soul": SpriteData(0x13860B0, 37, True),
    "Warg Soul": SpriteData(?????, ??),
    "Bomber Armor Soul": SpriteData(0x10CF520, 17),
    "Amalaric Sniper Soul": SpriteData(?????, ??),
    "Cave Troll Soul": SpriteData(?????, ??),
    "Waiter Skeleton Soul": SpriteData(?????, ??),
    "Slime Soul": SpriteData(0x1488200, 16),
    "Yorick Soul": SpriteData(?????, ??),
    "Une Soul": SpriteData(0x16EA720, 16),
    "Mandragora Soul": SpriteData(?????, ??),
    "Rycuda Soul": SpriteData(0x1504DA0, 59, True),
    "Fleaman Soul": SpriteData(?????, ??),
    "Ripper Soul": SpriteData(?????, ??),
    "Guillotiner Soul": SpriteData(?????, ??),
    "Killer Clown Soul": SpriteData(?????, ??),
    "Malachi Soul": SpriteData(?????, ??),
    "Disc Armor Soul": SpriteData(?????, ??),
    "Great Axe Armor Soul": SpriteData(?????, ??),
    "Slaughterer Soul": SpriteData(0x11DE000, 32, True),
    "Hell Boar Soul": SpriteData(?????, ??),
    "Frozen Shade Soul": SpriteData(?????, ??),
    "Merman Soul": SpriteData(?????, ??),
    "Larva Soul": SpriteData(?????, ??),
    "Ukoback Soul": SpriteData(?????, ??),
    "Decarabia Soul": SpriteData(?????, ??),
    "Succubus Soul": SpriteData(?????, ??),
    "Slogra Soul": SpriteData(?????, ??),
    "Erinys Soul": SpriteData(?????, ??),
    "Homunculus Soul": SpriteData(?????, ??),
    "Witch Soul": SpriteData(?????, ??),
    "Fish Head Soul": SpriteData(?????, ??),
    "Mollusca Soul": SpriteData(0x1263640, 38, True),
    "Dead Mate Soul": SpriteData(?????, ??),
    "Malacoda Soul": SpriteData(?????, ??),
    "Aguni Soul": SpriteData(?????, ??),
    "Abaddon Soul": SpriteData(0x1051870, 14, True),
}

# TODO! FINISH THIS TABLE! Figure out how to flip sprites properly!
# I know that I have to swap each individual Nybble of each byte. But is there a shift going on?

def set_souls_for_walls(world):
    if world.options.randomize_red_soul_walls:
        world.red_soul_walls = world.random.sample(viable_wall_souls, 4)
    else:
        world.red_soul_walls = ["Killer Clown Soul", "Axe Armor Soul", "Skeleton Soul", "Ukoback Soul"]



def apply_souls_and_gfx(world, rom):
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
    tile_row = [((tile & 0x0F) << 4) | ((tile & 0xF0) >> 4) for tile in tile_row]  # Invert the nybbles of each byte
    return bytearray(tile_row)