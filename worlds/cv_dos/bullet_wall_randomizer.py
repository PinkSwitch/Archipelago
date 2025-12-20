from dataclasses import dataclass
from .in_game_data import global_soul_table
import struct

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
    palette_adress: int  # Address the sprite's palette can be found at
    height: int
    width: int = 0x10
    mirror_sprite: bool = True  # Sprites that need to be horizontally flipped
    swap_colors: bool = True
    convert_to_gradient: bool = True  # Convert most sprites to use a gradient

    #TODO! I wonder if, instead of filling the initial wall with 0xFF, we instead copy bytes from the original wall and build it out of that?

def set_souls_for_walls(world):
    if world.options.randomize_red_soul_walls:
        world.red_soul_walls = world.random.sample(viable_wall_souls, 4)
    else:
        world.red_soul_walls = ["Killer Clown Soul", "Axe Armor Soul", "Skeleton Soul", "Ukoback Soul"]
    
    world.important_souls.update(world.red_soul_walls)  # All of these souls instantly become important


def apply_souls_and_gfx(rom):
    enem_sprite_data_table = {
        "Skeleton Soul": SpriteData(0x16F00C0, 0x1E9724, 40),
        "Zombie Soul": SpriteData(0x163F680, 0x1E8D74, 37, 0x0B),
        "Axe Armor Soul": SpriteData(0x10888F0, 0xFFFFFFFF, 26, 16, False, False, False), #Try with palette
        "Student Witch Soul": SpriteData(0x13860B0, 0x1ECD28, 37),
        "Warg Soul": SpriteData(0x11F58C0, 0x1E8C70, 27),
        "Bomber Armor Soul": SpriteData(0x10CF520, 0x1EA924, 17, 8, False, False, False), # Looks fine, but consider palette matching if we get the rock texture to load. though id need to figure out transp. hmmm
        "Amalaric Sniper Soul": SpriteData(0x152A010, 0xFFFFFFFF, 64, 16, False, False, False),
        "Cave Troll Soul": SpriteData(0x16BE040, 0x1EA010, 38, 0x0C),
        "Waiter Skeleton Soul": SpriteData(0x152CF00, 0x1E94F8, 11, 8, False), # Waiter needs a proper palette
        "Slime Soul": SpriteData(0x1488200, 0x1E7A18, 16),
        "Yorick Soul": SpriteData(0x14F8D00, 0x1E9724, 8, 8),
        "Une Soul": SpriteData(0x16EA124, 0x1E82D4, 16, 16, False),
        "Mandragora Soul": SpriteData(0x138C8C0, 0x1E7B24, 26, 8, False),
        "Rycuda Soul": SpriteData(0x1504DA0, 0x1ED270, 59, 16, True),
        "Fleaman Soul": SpriteData(0x16E952A, 0x1EA60C, 16, 8, True, True),
        "Ripper Soul": SpriteData(0x1535D90, 0x1EA60C, 4, 16, True, True),
        "Guillotiner Soul": SpriteData(0x12B4040, 0xFFFFFFFF, 30, 16, False, True),
        "Killer Clown Soul": SpriteData(0x10ED100, 0xFFFFFFFF, 58, 16, True),
        "Malachi Soul": SpriteData(0x16D2E70, 0xFFFFFFFF, 46, 16, True, True),
        "Disc Armor Soul": SpriteData(0x114B4F0, 0xFFFFFFFF, 42),
        "Great Axe Armor Soul": SpriteData(0x125C150, 0xFFFFFFFF, 80, 16, True),
        "Slaughterer Soul": SpriteData(0x11DE000, 0xFFFFFFFF, 32, 16, True),
        "Hell Boar Soul": SpriteData(0x12CE0C0, 0xFFFFFFFF, 34, 16, True),
        "Frozen Shade Soul": SpriteData(0x13D4140, 0xFFFFFFFF, 53, 16, True),
        "Merman Soul": SpriteData(0x16D6100, 0xFFFFFFFF, 52, 16, True),
        "Larva Soul": SpriteData(0x132E100, 0xFFFFFFFF, 16),
        "Ukoback Soul": SpriteData(0x16EE880, 0xFFFFFFFF, 27, True),
        "Decarabia Soul": SpriteData(0x112A040, 0xFFFFFFFF, 46),
        "Succubus Soul": SpriteData(0x1463000, 0xFFFFFFFF, 32, True),
        "Slogra Soul": SpriteData(0x10A5110, 0xFFFFFFFF, 25, True),
        "Erinys Soul": SpriteData(0x11AFB30, 0xFFFFFFFF, 38, True),
        "Homunculus Soul": SpriteData(0x12D60C0, 0xFFFFFFFF, 50, 16),
        "Witch Soul": SpriteData(0x1384000, 0xFFFFFFFF, 48, True),
        "Fish Head Soul": SpriteData(0x16DA040, 0xFFFFFFFF, 23, True),
        "Mollusca Soul": SpriteData(0x1263640, 38, True),
        "Dead Mate Soul": SpriteData(0x12BC710, 41, True),
        "Malacoda Soul": SpriteData(0x13DA000, 64, True),
        "Flame Demon Soul": SpriteData(0x12100A0, 21, True),
        "Aguni Soul": SpriteData(0x1060080, 0xFFFFFFFF, 43, 16, True),
        "Abaddon Soul": SpriteData(0x1051870, 0xFFFFFFFF, 14, 16, True),
    }
    # TODO; FINISH THIS TABLE! Colors and width! And palettes!

    soul_wall_1 = int.from_bytes(rom.read_bytes(0x158BC0, 1))
    soul_wall_2 = int.from_bytes(rom.read_bytes(0x158BBA, 1))
    soul_wall_3 = int.from_bytes(rom.read_bytes(0x158BB4, 1))
    soul_wall_4 = int.from_bytes(rom.read_bytes(0x158BC6, 1))

    soul_walls = [
    global_soul_table[soul_wall_1],
    global_soul_table[soul_wall_2],
    global_soul_table[soul_wall_3],
    global_soul_table[soul_wall_4],
        ]
    soul_walls = [
        "Waiter Skeleton Soul",
        "Guilltoiner Soul",
        "Killer Clown Soul",
        "Malachi Soul",
    ]

    for i in range(0x1801):
        rom.write_bytes(0x10D6000 + i, bytearray([0xFF]))  # Blank out the original graphic

    for i, soul in enumerate(soul_walls):
        height = enem_sprite_data_table[soul].height
        width = enem_sprite_data_table[soul].width
        address = enem_sprite_data_table[soul].address
        palette_pointer = enem_sprite_data_table[soul].palette_adress
        color_invert = enem_sprite_data_table[soul].swap_colors
        starting_height = int((96 - height) / 2)  # Calculate the rough center of the block, heightwise
        palette = extract_palette(palette_pointer, rom)
        palette_sorted = sorted(palette, key=lum)  # Sort the palette by luminosity

        for j in range (height + 1):
            tile_row = rom.read_bytes(address + (0x40 * j), width)  # Read each row of the image

            if enem_sprite_data_table[soul].convert_to_gradient:
                tile_row = convert_sprite_to_new_palette(tile_row, palette, palette_sorted)

            tile_row = convert_transparency_and_colors(tile_row, color_invert)

            if enem_sprite_data_table[soul].mirror_sprite:
                tile_row = mirror_tiles(tile_row)  # Sprites should face right. If they're not, mirror the image
                
            rom.write_bytes((0x10D6000 + (i * 0x10) + (j * 0x40) + (starting_height * 0x40)) + (int((16 - width) / 2)), tile_row)  # Write the current tile over the wall we made earlier


def mirror_tiles(tile_row) -> bytearray:
    pix_row = list(tile_row)  # Convert the bytes to a list
    front_tiles = pix_row[:8][::-1]
    back_tiles = pix_row[8:][::-1]

    tile_row = back_tiles + front_tiles  # Reverse the byte order
    tile_row = [((tile & 0x0F) << 4) | (tile >> 4) for tile in tile_row]  # Invert the nybbles of each byte
    return bytearray(tile_row)

def convert_transparency_and_colors(tile_row, color_invert) -> bytearray:
    pix_row = list(tile_row)
    new_row = []
    for pixel in pix_row:
        if color_invert:
            pixel = pixel ^ 0xFF # Invert the bits

        pixel = (
            ((pixel & 0xF0) or 0xF0) |
            ((pixel & 0x0F) or 0x0F)
        )
        
        new_row.append(pixel)
    return bytearray(new_row)

def extract_palette(pointer, rom) -> list:
    palette_rgb = []
    palette = rom.read_bytes(pointer, 0x20)
    palette = list(struct.unpack("<{}H".format(len(palette)//2), palette))
    for color in palette:
        
        r = (((color >> 0)  & 0x1F) * 255 + 15) // 0x1F
        g = (((color >> 5)  & 0x1F) * 255 + 15) // 0x1F
        b = (((color >> 10)  & 0x1F) * 255 + 15) // 0x1F
        palette_rgb.append([r, g, b])

    return palette_rgb

def lum(rgb):
    r, g, b = rgb
    return 0.2126*r + 0.7152*g + 0.0722*b

def convert_sprite_to_new_palette(tile_row, palette, palette_sorted):
    new_row = []
    for tile in tile_row:
        pixel_high = (tile >> 4) & 0x0F
        pixel_low = tile & 0x0F

        pixel_high = 0 if not pixel_high else palette_sorted.index(palette[pixel_high])
        pixel_low = 0 if not pixel_low else palette_sorted.index(palette[pixel_low])

        new_pixel = (pixel_high << 4) | pixel_low
        new_row.append(new_pixel)
    return bytearray(new_row)