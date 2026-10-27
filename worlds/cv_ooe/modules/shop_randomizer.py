from .drop_shuffle import get_drop_item


shop_pool = {"weak_healing": 50, "mid_healing": 40, "great_healing": 10,
             "static_consumable": 20, "armor": 30, "good_armor": 5, "accessory": 15}

shop_pools = {
    0x02200188: 7,  # Default shop
    0x0220020C: 3,  # Maneater shop
    0x02200260: 3,  # Goliath shop

    0x02222856: 2,  # Running out of Sage
    0x0222283E: 2,  # Medicinal Ingredients
    0x0222288A: 3,  # Mandrake
    0x0222281E: 1,  # Unusual Components

    0x02222826: 1,  # Lucky Stone
    0x022228B6: 6,  # Pleasant Accessory
    0x022228A2: 4,  # Heartwarming Accessory

    0x02222892: 3,  # Poor Prep
    0x0222285C: 2,  # Blacksmith Does
    0x022228AC: 4,  # Work of the finest

    0x02222862: 2,  # Needs salt
    0x02222868: 2,  # Never eaten that
    0x02222874: 2,  # Cant cook

    0x02222822: 1,  # Vicious Blight
    0x0222283A: 1,  # Demon Horse
    0x0222282A: 1,  # Hideous Snowman

    0x02222844: 2,  # Violin
    0x02222850: 2,  # Killing Scream
    0x0222287A: 2,  # Selfish

    0x0222286E: 2,  # Making a dress
    0x0222289A: 3,  # Silkworm Tragedy
    0x0222284A: 2  # Cashmere
}


def randomize_shop(world, rom):
    from ..Items import item_table
    import struct
    banned_items = ["VIP Card"]
    for pointer in shop_pools:
        for i in range(shop_pools[pointer]):
            item = roll_shop_item(world, banned_items)
            item_id = item_table[item].code
            banned_items.append(item)  # Add this item to the banlist so it can't be rolled again
            rom.write_to_file(pointer + (i * 2), "overlay_19", struct.pack("H", item_id))


def roll_shop_item(world, ban_list):
    item = ban_list[0]  # Initialize this to a banned item so it always rolls a new one
    while item in ban_list or item is None:
        item = get_drop_item(world, shop_pool, False)
    return item
