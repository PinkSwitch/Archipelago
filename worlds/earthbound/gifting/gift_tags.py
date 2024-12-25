from dataclasses import dataclass
from typing import List

gift_qualities = {
    "Super Plush Bear": {"Stuffed": 2, "MeatShield": 3},
    "Cracked Bat": {"Weapon": 0.07},
    "Tee Ball Bat": {"Weapon": 0.14},
    "Sand Lot Bat": {"Weapon": 0.27},
    "Minor League Bat": {"Weapon": 0.48},
    "Mr. Baseball Bat": {"Weapon": 0.70},
    "Hall of Fame Bat": {"Weapon": 1.14},
    "Magicant Bat": {"Weapon": 1.48},
    "Legendary Bat": {"Weapon": 2.03},
    "Gutsy Bat": {"Weapon": 4.0},
    "Casey Bat": {"Weapon": 0.1},
    "T-rex's Bat": {"Weapon": 0.88},
    "Ultimate Bat": {"Weapon": 1.25},
} 


@dataclass
class EarthBoundGift:
    name: str
    value: int
    traits: list


def make_trait(trait: str, name, duration: float = 1):
    if name in gift_qualities and trait in gift_qualities[name]:
        quality = gift_qualities[name][trait]
    else:
        quality = 1
    return {"Trait": trait, "Quality": quality, "Duration": duration}


def make_default_traits(traits: List[str], name: str):
    return [make_trait(trait, name) for trait in traits]


def create_gift(name, value, traits):
    return EarthBoundGift(name, value, make_default_traits(traits, name))


gift_properties = {
    0x02: create_gift("Teddy Bear", 178, ["Bear", "Toy", "Stuffed", "Brown", "MeatShield", "Animal"]),

    0x03: create_gift("Super Plush Bear", 1198, ["Bear", "Toy", "Stuffed", "Brown", "MeatShield", "Animal"]),

    0x04: create_gift("Broken Machine", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x05: create_gift("Broken Gadget", 109, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x06: create_gift("Broken Air Gun", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x07: create_gift("Broken Spray Can", 189, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x08: create_gift("Broken Laser", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x09: create_gift("Broken Iron", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x0A: create_gift("Broken Pipe", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Pipe", "Junk"]),

    0x0B: create_gift("Broken Cannon", 218, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x0C: create_gift("Broken Tube", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x0D: create_gift("Broken Bazooka", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Weapon", "Junk"]),

    0x0E: create_gift("Broken Trumpet", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument", "Junk"]),

    0x0F: create_gift("Broken Harmonica", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument", "Junk"]),

    0x10: create_gift("Broken Antenna", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    0x11: create_gift("Cracked Bat", 18, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x12: create_gift("Tee Ball Bat", 48, ["MeleeWeapon", "Metal", "Toy", "Weapon"]),

    0x13: create_gift("Sand Lot Bat", 98, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x14: create_gift("Minor League Bat", 399, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x15: create_gift("Mr. Baseball Bat", 498, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x16: create_gift("Big League Bat", 3080, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x17: create_gift("Hall of Fame Bat", 1880, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x18: create_gift("Magicant Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Dreamlike"]),

    0x19: create_gift("Legendary Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Legendary"]),

    0x1A: create_gift("Gutsy Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Gutsy"]),

    0x1B: create_gift("Casey Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    0x1C: create_gift("Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    0x1D: create_gift("Thick Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "Thick"]),

    0x1E: create_gift("Deluxe Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    0x1F: create_gift("Chef's Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    0x20: create_gift("French Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "French"]),

    0x21: create_gift("Magic Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    0x22: create_gift("Holy Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "Holy"]),

    35: create_gift("Sword of Kings", 0, ["MeleeWeapon", "Metal", "Sword", "Weapon", "Artifact"]),

    0x58: create_gift("Cookie", 7, ["Confectionary", "Comsumable", "Heal", "Food"]),

    0x59: create_gift("Bag of Fries", 8, ["FastFood", "Comsumable", "Heal", "Food", "Potato", "Processed", "Salted", "Vegetable"]),

    0x5A: create_gift("Hamburger", 14, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed", "Meat"]),

    91: create_gift("Boiled Egg", 0, ["Egg", "Comsumable", "Heal", "Food", "White"]),

    92: create_gift("Fresh Egg", 0, ["Egg", "Comsumable", "Heal", "Food", "White"]),

    93: create_gift("Picnic Lunch", 24, ["ArtisanGood", "Comsumable", "Heal", "Food"]),

    94: create_gift("Pasta di Summers", 0, ["Pasta", "Comsumable", "Heal", "Food", "ArtisanGood"]),

    95: create_gift("Pizza", 0, ["Comsumable", "Heal", "Food", "Italian"]),

    96: create_gift("Chef's Special", 0, ["Comsumable", "Heal", "Food"]),

    97: create_gift("Large Pizza", 0, ["Comsumable", "Heal", "Food", "Italian", "Large"]),

    98: create_gift("PSI Caramel", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    99: create_gift("Magic Truffle", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    100: create_gift("Brain Food Lunch", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    101: create_gift("Rock Candy", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    102: create_gift("Croissant", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    103: create_gift("Bread Roll", 0, ["Comsumable", "Mana", "Food", "Confectionary", "PSI"]),

    106: create_gift("Can of Fruit Juice", 0, ["Comsumable", "Heal", "Drink", "Liquid", "Fruit"]),

    107: create_gift("Royal Iced Tea", 0, ["Comsumable", "Heal", "Drink", "Liquid"]),

    108: create_gift("Protein Drink", 0, ["Comsumable", "Heal", "Drink", "Liquid"]),

    109: create_gift("Kraken Soup", 0, ["Comsumable", "Heal", "Food", "Liquid", "ArtisanGood"]),

    110: create_gift("Bottle of Water", 0, ["Comsumable", "Mana", "Drink", "Liquid", "PSI"]),

    111: create_gift("Cold Remedy", 0, ["Comsumable", "Medicine", "Drink", "Liquid", "Cure"]),

    112: create_gift("Vial of Serum", 0, ["Comsumable", "Medicine", "Drink", "Liquid", "Cure"]),

    113: create_gift("IQ Capsule", 0, ["Comsumable", "Medicine", "IQ", "StatBoost"]),

    114: create_gift("Guts Capsule", 0, ["Comsumable", "Medicine", "Guts", "StatBoost"]),

    115: create_gift("Speed Capsule", 0, ["Comsumable", "Medicine", "Speed", "StatBoost"]),

    116: create_gift("Vital Capsule", 0, ["Comsumable", "Medicine", "HP", "StatBoost"]),

    117: create_gift("Luck Capsule", 0, ["Comsumable", "Medicine", "Lucky", "StatBoost", "Luck"]),

    118: create_gift("Ketchup Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "Red", "Tomato"]),

    119: create_gift("Sugar Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "White"]),

    120: create_gift("Tin of Cocoa", 0, ["Comsumable", "Heal", "Food", "Condiment", "Brown", "Chocolate"]),

    121: create_gift("Carton of Cream", 0, ["Comsumable", "Heal", "Food", "Condiment", "White", "Liquid"]),

    122: create_gift("Sprig of Parsley", 0, ["Comsumable", "Heal", "Food", "Condiment", "Green", "Plant"]),

    123: create_gift("Jar of Hot Sauce", 0, ["Comsumable", "Heal", "Food", "Condiment", "Orange", "Spicy"]),

    124: create_gift("Salt Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "White", "Salted"]),

    126: create_gift("Jar of Delisauce", 0, ["Comsumable", "Heal", "Food", "Condiment", "Green"]),

    127: create_gift("Wet Towel", 0, ["Comsumable", "Medicine", "Cure"]),

    128: create_gift("Refreshing Herb", 0, ["Comsumable", "Medicine", "Cure", "Food"]),

    129: create_gift("Secret Herb", 0, ["Comsumable", "Medicine", "Cure", "Food", "Revive"]),

    130: create_gift("Horn of Life", 0, ["Comsumable", "Medicine", "Cure", "Revive"]),

    131: create_gift("Counter-PSI Unit", 0, ["Machine", "PSI", "Electronics", "Metal"]),

    132: create_gift("Shield Killer", 0, ["Machine", "Shields", "Electronics", "Metal", "Neutralizing"]),

    133: create_gift("Bazooka", 0, ["Machine", "Weapon", "Electronics", "Explosive", "RangedWeapon", "Heavy"]),

    134: create_gift("Heavy Bazooka", 0, ["Machine", "Weapon", "Electronics", "Explosive", "RangedWeapon", "Heavy"]),

    135: create_gift("HP-Sucker", 0, ["Machine", "Draining", "Electronics"]),

    136: create_gift("Hungry HP-Sucker", 0, ["Machine", "Draining", "Electronics"]),

    137: create_gift("Xterminator Spray", 0, ["Can", "Metal", "Insecticide", "Weapon", "Chemicals"]),

    138: create_gift("Slime Generator", 0, ["Machine", "Slime", "Electronics"]),

    140: create_gift("Ruler", 0, ["Long", "Wood", "Junk", "Trash", "IQ"]),

    141: create_gift("Snake Bag", 0, ["Animal", "Bag", "Many", "Throwing"]),

    142: create_gift("Mummy Wrap", 0, ["Ancient", "Paper", "Weapon", "Throwing", "Consumable"]),

    143: create_gift("Protractor", 0, ["Angular", "Metal", "Junk", "Trash", "IQ"]),

    144: create_gift("Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    145: create_gift("Big Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    146: create_gift("Multi Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    147: create_gift("Bomb", 0, ["Weapon", "Explosive", "Throwing", "Consumable"]),

    148: create_gift("Super Bomb", 0, ["Weapon", "Explosive", "Throwing", "Consumable"]),

    149: create_gift("Insecticide Spray", 0, ["Can", "Metal", "Insecticide", "Weapon", "Consumable", "Chemicals"]),

    150: create_gift("Rust Promoter", 0, ["Can", "Metal", "Rusting", "Weapon", "Consumable", "Chemicals"]),

    151: create_gift("Rust Promoter DX", 0, ["Can", "Metal", "Rusting", "Weapon", "Consumable", "Chemicals"]),

    152: create_gift("Pair of Dirty Socks", 0, ["Consumable", "Throwing", "Stinky", "Clothes"]),

    153: create_gift("Stag Beetle", 0, ["Consumable", "Throwing", "Animal", "Insect"]),

    154: create_gift("Toothbrush", 0, ["Consumable", "Tool"]),

    155: create_gift("Handbag Strap", 0, ["Consumable", "Weapon", "Throwing", "Leather"]),

    156: create_gift("Pharaoh's Curse", 0, ["Consumable", "Weapon", "Throwing", "Poison", "Goo", "Slime", "Poison", "Chemicals"]),

    157: create_gift("Defense Shower", 0, ["Can", "Machine", "Chemicals", "StatBoost", "Defense", "Liquid"]),

    159: create_gift("Sudden Guts Pill", 0, ["Consumable", "Medicine", "Guts", "FastActing"]),

    160: create_gift("Bag of Dragonite", 0, ["Consumable", "Medicine", "Weapon", "Powder"]),

    161: create_gift("Defense Spray", 0, ["Can", "Consumable", "Chemicals", "StatBoost", "Defense", "Liquid"]),

    165: create_gift("Picture Postcard", 0, ["Paper", "Photograph", "Sad", "Junk", "Trash"]),

    168: create_gift("Chick", 0, ["Animal", "Happy", "Yellow", "Bird"]),

    169: create_gift("Chicken", 0, ["Animal", "SellFodder", "White", "Bird"]),

    186: create_gift("Meteotite", 0, ["Mineral", "SellFodder", "Artifact", "Brown"]),

    188: create_gift("Hand-Aid", 0, ["Consumable", "Heal", "Fabric", "UltraHeal", "Band-Aid"]),

    189: create_gift("Trout Yogurt", 0, ["Consumable", "Heal", "Food", "Fish", "Dairy"]),

    190: create_gift("Banana", 0, ["Consumable", "Heal", "Food", "Fruit", "Yellow"]),

    191: create_gift("Calorie Stick", 0, ["Consumable", "Heal", "Food", "Jerky", "Processed"]),

    194: create_gift("Earth Pendant", 0, ["Wearable", "Jewelry", "FireProof", "WaterProof", "LightProof"]),

    195: create_gift("Neutralizer", 0, ["Machine", "PSI", "Electronics", "Metal", "Neutralizing"]),

    198: create_gift("Gelato de Resort", 0, ["Consumable", "Food", "Heal", "Dairy", "FrozenFood"]),

    199: create_gift("Snake", 0, ["Animal", "Weapon", "Throwing", "Consumable"]),

    200: create_gift("Viper", 0, ["Animal", "Weapon", "Throwing", "Poison", "Consumable"]),

    201: create_gift("Brain Stone", 0, ["Rock", "Mineral", "PSI", "Junk", "Trash"]),

    207: create_gift("Magic Tart", 0, ["Food", "Consumable", "PSI", "Mana", "Confectionary"]),

    209: create_gift("Monkey's Love", 0, ["Weapon", "Animal"]),

    212: create_gift("T-Rex's Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    213: create_gift("Big League Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]), # Todo? Figure out which one is in game

    214: create_gift("Ultimate Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    215: create_gift("Double Beam", 0, ["RangedWeapon", "Gun", "Beam", "Weapon"]),

    216: create_gift("Platinum Band", 0, ["Wearable", "Defense", "Platinum", "Jewelry"]),

    217: create_gift("Diamond Band", 0, ["Wearable", "Defense", "Diamond", "Jewelry"]),

    218: create_gift("Defense Ribbon", 0, ["Wearable", "Cloth", "Defense"]),

    219: create_gift("Talisman Ribbon", 0, ["Wearable", "Cloth", "Defense"]),

    220: create_gift("Saturn Ribbon", 0, ["Wearable", "Cloth", "Defense"]),

    221: create_gift("Coin of Silence", 0, ["Wearable", "Defense", "Charm"]),

    222: create_gift("Charm Coin", 0, ["Wearable", "Defense", "Charm"]),

    223: create_gift("Cup of Noodles", 0, ["Food", "Consumable", "Heal", "FastFood", "Noodles", "Sandwich"]),

    224: create_gift("Repel Sandwich", 0, ["Food", "Consumable", "Heal", "ArtisanGood", "Repellant", "Sandwich"]),

    225: create_gift("Repel Superwich", 0, ["Food", "Consumable", "Heal", "ArtisanGood", "Repellant", "Sandwich"]),

    226: create_gift("Lucky Sandwich", 0, ["Food", "Consumable", "Heal", "Lucky", "Luck", "Mana", "Sandwich"]),

    232: create_gift("Cup of Coffee", 0, ["Drink", "Consumable", "Heal", "Liquid", "Coffee"]),

    233: create_gift("Double Burger", 0, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed", "Meat"]),

    234: create_gift("Peanut Cheese Bar", 0, ["Comsumable", "Heal", "Food", "Candy", "ExoticFood"]),

    235: create_gift("Piggy Jelly", 0, ["Comsumable", "Heal", "Food", "Candy", "ExoticFood", "Gelatin", "Jelly"]),

    236: create_gift("Bowl of Rice Gruel", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "ExoticFood", "Liquid"]),

    237: create_gift("Bean Croquette", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "ExoticFood"]),

    238: create_gift("Molokheiya Soup", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "ExoticFood", "Vegetable", "Liquid"]),

    239: create_gift("Plain Roll", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "Bread"]),

    240: create_gift("Kabob", 0, ["Comsumable", "Heal", "Food", "ExoticFood", "Meat", "Lamb"]),

    241: create_gift("Plain Yogurt", 0, ["Comsumable", "Heal", "Food", "Slime", "Dairy"]),

    242: create_gift("Beef Jerky", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "Meat", "Dried", "Jerky"]),

    243: create_gift("Mammoth Burger", 0, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed", "Meat"]),

    244: create_gift("Spicy Jerky", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "Meat", "Dried", "Jerky", "Spicy"]),

    245: create_gift("Luxury Jerky", 0, ["Comsumable", "Heal", "Food", "ArtisanGood", "Meat", "Dried", "Jerky"]),

    246: create_gift("Bottle of DXWater", 0, ["Comsumable", "Mana", "Drink", "Liquid", "PSI"]),
    #Todo; separate traits for GoodWeapon and BadWeapon
    # Todo; Satus heals should be Medicine, Cure
}

acceptable_gifts = [
    "Confectionary",
    "Vegetable",
    "Food"
]

parent_trait_list = [
    "Broken",
    "Machine",
    "Gun",
    "Heal",
    "Mana",
    "Food",
    "Baseball",
    "Egg"
]