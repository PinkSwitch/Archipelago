material_table = [
    "Salt",
    "Horse Hair",
    "Eagle Feather",
    "Black Ink",
    "Cotton Thread",
    "Silk Thread",
    "Sage",
    "Chamomile",
    "Rue",
    "Zircon",
    "Lapis Lazuli",
    "Ruby",
    "Sapphire",
    "Emerald",
    "Copper Ore",
    "Iron Ore",
    "Silver Ore",
    "Salt"]

rare_material_table = [
    "Gold Ore",
    "Onyx",
    "Diamond",
    "Alexandrite",
    "Chrysoberyl",
    "Mandrake Root",
    "Merman Meat",
    "Cashmere Thread",
    "Raw Killer Fish",
]

weak_healing_table = [
    "Potion",
    "Tonic",
    "Anti-Venom",
    "Uncurse Potion",
    "Meat",
    "Raw Killer Fish",
    "Salt",
    "Rice Ball",
    "Mushroom",
    "Corn Soup",
    "Cream Puff",
    "Pudding",
    "Mocha Eclair",
    "Mint Sundae",
    "Milk",
    "Coffee",
    "Earl Grey",
    "Dajeerling Tear",
    "Amanita",
    "Rotten Meat",
    "Spoiled Milk"
]

mid_healing_table = [
    "High Potion",
    "High Tonic",
    "Heart Repair",
    "Minestrone",
    "Ramen Noodles",
    "Tart Tatin",
    "Choco Souffle",
]

great_healing_table = [
    "Super Potion",
    "Super Tonic",
    "Crepes Susette",
    "Croque Monsieur",
    "Schnitzel",
    "Eisbein",
    "Killer Fish BBQ",
    "Tasty Meat",
    "Thick Steak"
]

drops_table = [
    "Red Drops",
    "Blue Drops",
    "Green Drops",
    "White Drops",
    "Black Drops"
]

static_consumable_table = [
    "Record 1",
    "Record 2",
    "Record 3",
    "Record 4",
    "Record 5",
    "Record 6",
    "Record 7",
    "Record 8",
    "VIP Card"
]

armor_table = [
    "Casual Clothes",
    "Military Wear",
    "Rubber Suit",
    "Reinforced Suit",
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
    "Empire Dress",
    "Corset Dress",
    "Eye for Decay",
    "L. Eye of God",
    "R. Eye of Devil",
    "Cotton Hat",
    "Garbo Hat",
    "Treasure Hat",
    "Dowsing Hat",
    "Traveler's Hat",
    "Babushka",
    "Cabriolet",
    "Crochet",
    "Barbarian Helm",
    "Stephanie",
    "Sword Helm",
    "Rapier Helm",
    "Lance Helm",
    "Hammer Helm",
    "Arrow Helm",
    "Sickle Helm",
    "Knife Helm",
    "Shield Helm",
    "Winged Boots",
    "Combo Boots",
    "Sabrina Shoes",
    "Cossack Boots",
    "Baggy Boots",
    "Battle Boots",
    "Ghillie Boots",
    "Cavalier Boots",
    "Iron Leggings",
    "Barbarian Shoes",
    "Crimson Greaves",
    "Sandals"

]

good_armor_table = [
    "Gold Plate",
    "Platinum Plate",
    "Knight Cuirass",
    "Minerva Mail",
    "Party Dress",
    "Wedding Dress",
    "Robe Decollete",
    "Ribbon",
    "Caprine",
    "Knight Helm",
    "Minerva Mask",
    "Ruby Pins",
    "Sapphire Pins",
    "Emerald Pins",
    "Diamond Pins",
    "Onyx Pins",
    "Royal Crown",
    "Silver Leggings",
    "Gold Leggings",
    "Plat Leggings",
    "Knight Leggings",
    "Minerva Greaves",
    "Valkyrie Greaves",
    "Valkyrie Mask",
    "Crimson Mask",
    "Valkyrie Mail",
    "Heart Cuirass",
]

accessory_table = [
    "Protect Ring",
    "Resist Ring",
    "Fool Ring",
    "Magician Ring",
    "Priestess Ring",
    "Empress Ring",
    "Emperor Ring",
    "Hierophant Ring",
    "Lovers Ring",
    "Chariot Ring",
    "Justice Ring",
    "Hermit Ring",
    "Fortune Ring",
    "Strength Ring",
    "Hanged Man Ring",
    "Death Ring",
    "Temperance Ring",
    "Devil Ring",
    "Tower Ring",
    "Star Ring",
    "Moon Ring",
    "Sun Ring",
    "Judgement Ring",
    "World Ring",
    "Archer Ring",
    "Blow Ring",
    "Wind Ring",
    "Ruby Ring",
    "Sapphire Ring",
    "Emerald Ring",
    "Diamond Ring",
    "Onyx Ring",
    "Heart Earrings",
    "Gold Ring",
    "Miser Ring",
    "Lucky Clover",
    "Thief Ring"
]


def shuffle_drops(world, rom) -> None:
    full = {"material": 1, "rare_material": 5, "weak_healing": 60, "mid_healing": 30, "great_healing": 10,
            "drops": 1, "static_consumable": 1, "armor": 40, "good_armor": 15, "accessory": 5}

    star_tier_1 = {"material": 80, "rare_material": 20, "weak_healing": 60, "mid_healing": 10, "great_healing": 5,
                   "drops": 0, "static_consumable": 10, "armor": 1, "good_armor": 1, "accessory": 1}

    star_tier_2 = {"material": 30, "rare_material": 40, "weak_healing": 80, "mid_healing": 60, "great_healing": 20,
                   "drops": 0, "static_consumable": 10, "armor": 15, "good_armor": 5, "accessory": 1}

    star_tier_3 = {"material": 10, "rare_material": 15, "weak_healing": 40, "mid_healing": 80, "great_healing": 30,
                   "drops": 1, "static_consumable": 15, "armor": 20, "good_armor": 10, "accessory": 5}

    star_tier_4 = {"material": 5, "rare_material": 10, "weak_healing": 20, "mid_healing": 30, "great_healing": 40,
                   "drops": 1, "static_consumable": 10, "armor": 60, "good_armor": 50, "accessory": 5}

    star_tier_5 = {"material": 1, "rare_material": 5, "weak_healing": 10, "mid_healing": 50, "great_healing": 70,
                   "drops": 2, "static_consumable": 1, "armor": 40, "good_armor": 60, "accessory": 30}

    for i in range(0x6B):
        address = 0x020B6364 + (0x24 * i)
        common_item = 0
        rare_item = 0
        if world.random.randint(1, 100) <= 33:  # 33% chance for a Common
            print("Comm")
            common_item = get_drop_item(world, full)
            common_chance = world.random.randint(0x01, 0x10)

        if world.random.randint(1, 100) <= 14:  # 14% chance for a Rare
            print("Rare")
            rare_item = get_drop_item(world, full)
            rare_chance = world.random.randint(0x01, 0x10)


def get_drop_item(world, weight_map) -> int:
    weight_table = {
        "material": material_table,
        "rare_material": rare_material_table,
        "weak_healing": weak_healing_table,
        "mid_healing": mid_healing_table,
        "great_healing": great_healing_table,
        "drops": drops_table,
        "static_consumable": static_consumable_table,
        "armor": armor_table,
        "good_armor": good_armor_table,
        "accessory": accessory_table
    }

    print("b")