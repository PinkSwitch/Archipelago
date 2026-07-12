import struct
from ..Items import item_table

consumable_table = [
    "Potion",
    "Tonic",
    "Anti-Venom",
    "Uncurse Potion",
    "Meat",
    "Raw Killer Fish",
    "Rice Ball",
    "Mushroom",
    "Corn Soup",
    "Cream Puff",
    "Pudding",
    "Mocha Eclair",
    "Salt",
    "Mint Sundae",
    "Milk",
    "Coffee",
    "Earl Grey",
    "Horse Hair",
    "Eagle Feather",
    "Black Ink",
    "Cotton Thread",
    "Silk Thread",
    "Sage",
    "Chamomile",
    "Rue",
    "Mandrake Root",
    "Merman Meat",
    "Zircon",
    "Copper Ore",
]

good_consumable_table = [
    "High Potion",
    "High Tonic",
    "Heart Repair",
    "Iron Ore",
    "Silver Ore",
    "Onyx",
    "Diamond",
    "Schnitzel",
    "Croque Monsieur",
    "Crepes Suzette",
    "Choco Souffle",
    "Lapis Lazuli",
    "Ruby",
    "Sapphire",
    "Emerald",
    "Cashmere Thread",
    "Ramen Noodles",
    "Minestrone",
    "Tart Tatin",
    "Darjeeling Tea",
]

rare_consumable_table = [
    "Super Potion",
    "Super Tonic",
    "Tasty Meat",
    "Thick Steak",
    "Gold Ore",
    "Curry",
    "Eisbein",
    "Killer Fish BBQ",
    "Chrysoberyl",
    "Alexandrite",
    "Red Drops",
    "Blue Drops",
    "Green Drops",
    "White Drops",
    "Black Drops"
]

chest_armor_table = [
    "Military Wear",
    "Rubber Suit",
    "Reinforced Suit",
    "Body Suit",
    "Leather Cuirass",
    "Copper Plate",
    "Iron Plate",
    "Silver Plate",
    "Mirror Cuirass",
    "Barbarian Belt",
    "Crimson Mail",
    "Cotton Dress",
    "Silk Dress",
    "Sequined Dress",
    "Corset Dress",
    "Garbo Hat",
    "Traveler's Hat",
    "Babushka",
    "Crochet",
    "Barbarian Helm",
    "Stephanie",
    "Combo Boots",
    "Sabrina Shoes",
    "Cossack Boots",
    "Baggy Boots",
    "Battle Boots",
    "Ghillie Boots",
    "Cavalier Boots",
    "Iron Leggings",
    "Barbarian Shoes",
    "Crimson Greaves"]


def shuffle_brown_chest_pool(world, rom):
    common_weights = {"rare_consumable": 5, "good_consumable": 50, "consumable": 90}
    rare_weights = {"good_armor": 5, "armor": 10, "accessory": 20, "rare_consumable": 30, "good_consumable": 90}

    for i in range(0x12):

        pool = world.random.randint(0, 0x0A)
        rom.write_to_file(0x02223B08 + i, "overlay_19", bytes([pool]))   # Randomize which com/rare pool each area uses

        for j in range(4):
            item = generate_chest_items(world, common_weights)
            rom.write_to_file(0x02223B20 + (2 * j) + (4 * i), "overlay_19", struct.pack("H", item))

        for j in range(4):
            #  Blank these out if they're empty
            if not world.chest_filler_accessories:
                rare_weights["accessory"] = 0

            if not world.filler_chest_good_armor:
                rare_weights["good_armor"] = 0

            if not world.filler_chest_amror:
                rare_weights["armor"] = 0
            item = generate_chest_items(world, rare_weights)

            rom.write_to_file(0x02223B98 + (2 * j) + (4 * i), "overlay_19", struct.pack("H", item))


def generate_chest_items(world, pool: dict):
    weight_table = {
        "consumable": consumable_table,
        "good_consumable": good_consumable_table,
        "rare_consumable": rare_consumable_table,
        "armor": world.filler_chest_amror,
        "good_armor": world.filler_chest_good_armor,
        "accessory": world.chest_filler_accessories
    }

    filler_type = world.random.choices(list(pool), weights=list(pool.values()), k=1)[0]
    filler_item = world.random.choice(weight_table[filler_type])
    #  We want to remove picked filler so it doesn't come back
    if filler_item in world.chest_filler_accessories:
        world.chest_filler_accessories.remove(filler_item)

    elif filler_item in world.filler_chest_good_armor:
        world.filler_chest_good_armor.remove(filler_item)

    elif filler_item in world.filler_chest_amror:
        world.filler_chest_amror.remove(filler_item)

    return item_table[filler_item].code
