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
    2: create_gift("Teddy Bear", 178, ["Bear", "Toy", "Stuffed", "Brown", "MeatShield", "Animal"]),

    3: create_gift("Super Plush Bear", 1198, ["Bear", "Toy", "Stuffed", "Brown", "MeatShield", "Animal"]),

    4: create_gift("Broken Machine", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    5: create_gift("Broken Gadget", 109, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    6: create_gift("Broken Air Gun", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    7: create_gift("Broken Spray Can", 189, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    8: create_gift("Broken Laser", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    9: create_gift("Broken Iron", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    10: create_gift("Broken Pipe", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Pipe", "Junk"]),

    11: create_gift("Broken Cannon", 218, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    12: create_gift("Broken Tube", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    13: create_gift("Broken Bazooka", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Weapon", "Junk"]),

    14: create_gift("Broken Trumpet", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument", "Junk"]),

    15: create_gift("Broken Harmonica", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument", "Junk"]),

    16: create_gift("Broken Antenna", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Junk"]),

    17: create_gift("Cracked Bat", 18, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    18: create_gift("Tee Ball Bat", 48, ["MeleeWeapon", "Metal", "Toy", "Weapon"]),

    19: create_gift("Sand Lot Bat", 98, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    20: create_gift("Minor League Bat", 399, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    21: create_gift("Mr. Baseball Bat", 498, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    22: create_gift("Big League Bat", 3080, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    23: create_gift("Hall of Fame Bat", 1880, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    24: create_gift("Magicant Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Dreamlike"]),

    25: create_gift("Legendary Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Legendary"]),

    26: create_gift("Gutsy Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Gutsy"]),

    27: create_gift("Casey Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    28: create_gift("Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    29: create_gift("Thick Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "Thick"]),

    30: create_gift("Deluxe Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    31: create_gift("Chef's Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    32: create_gift("French Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "French"]),

    33: create_gift("Magic Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    34: create_gift("Holy Fry Pan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon", "Holy"]),

    35: create_gift("Sword of Kings", 0, ["MeleeWeapon", "Metal", "Sword", "Weapon", "Artifact"]),

    36: create_gift("Pop Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    37: create_gift("Stun Gun", 0, ["RangedWeapon", "Weapon"]),

    38: create_gift("Toy Air Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    39: create_gift("Magnum Air Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    40: create_gift("Zip Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    41: create_gift("Laser Gun", 0, ["RangedWeapon", "Beam", "Weapon"]),

    42: create_gift("Hyper Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    43: create_gift("Crusher Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),
    
    44: create_gift("Spectrum Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    45: create_gift("Death Ray", 0, ["RangedWeapon", "Beam", "Weapon"]),

    46: create_gift("Baddest Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    47: create_gift("Moon Beam Gun", 0, ["RangedWeapon", "Beam", "Weapon"]),

    48: create_gift("Gaia Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    49: create_gift("Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    50: create_gift("Slingshot", 0, ["RangedWeapon", "Toy", "Weapon"]),

    51: create_gift("Bionic Slingshot", 0, ["RangedWeapon", "Toy", "Weapon"]),

    52: create_gift("Trick Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    53: create_gift("Combat Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    54: create_gift("Travel Charm", 0, ["Wearable", "Jewelry", "Defense"]),

    55: create_gift("Great Charm", 0, ["Wearable", "Jewelry", "Defense"]),

    56: create_gift("Crystal Charm", 0, ["Wearable", "Jewelry", "Defense"]),

    57: create_gift("Rabbit's Foot", 0, ["Wearable", "Jewelry", "Defense", "Speed"]),

    58: create_gift("Flame Pendant", 0, ["Wearable", "Jewelry", "Defense", "FireProof"]),

    59: create_gift("Rain Pendant", 0, ["Wearable", "Jewelry", "Defense", "WaterProof"]),

    60: create_gift("Night Pendant", 0, ["Wearable", "Jewelry", "Defense", "LightProof"]),

    61: create_gift("Sea Pendant", 0, ["Wearable", "Jewelry", "Defense", "LightProof", "FireProof", "WaterProof"]),

    62: create_gift("Star Pendant", 0, ["Wearable", "Jewelry", "Defense", "LightProof", "FireProof", "WaterProof"]),

    63: create_gift("Cloak of Kings", 0, ["Wearable", "Jewelry", "Defense", "Artifact"]),

    64: create_gift("Cheap Bracelet", 0, ["Wearable", "Jewelry", "Defense", "Plastic"]),

    65: create_gift("Copper Bracelet", 0, ["Wearable", "Jewelry", "Defense", "Copper"]),

    66: create_gift("Silver Bracelet", 0, ["Wearable", "Jewelry", "Defense", "Silver"]),

    67: create_gift("Gold Bracelet", 0, ["Wearable", "Jewelry", "Defense", "Gold"]),

    68: create_gift("Platinum Band", 0, ["Wearable", "Jewelry", "Defense", "Platinum"]),

    69: create_gift("Diamond Band", 0, ["Wearable", "Jewelry", "Defense", "Diamond"]),

    70: create_gift("Pixie's Bracelet", 0, ["Wearable", "Jewelry", "Defense"]),

    71: create_gift("Cherub's Band", 0, ["Wearable", "Jewelry", "Defense"]),

    72: create_gift("Goddess Band", 0, ["Wearable", "Jewelry", "Defense"]),

    73: create_gift("Bracer of Kings", 0, ["Wearable", "Jewelry", "Defense", "Artifact", "FireProof"]),

    74: create_gift("Baseball Cap", 0, ["Wearable", "Baseball", "Defense", "Hat"]),

    75: create_gift("Holmes Hat", 0, ["Wearable", "Defense", "Hat"]),

    76: create_gift("Mr. Baseball Cap", 0, ["Wearable", "Defense", "Hat", "Baseball"]),

    77: create_gift("Hard Hat", 0, ["Wearable", "Defense", "Hat"]),

    78: create_gift("Ribbon", 0, ["Wearable", "Cloth", "Defense"]),

    79: create_gift("Red Ribbon", 0, ["Wearable", "Cloth", "Defense", "Red"]),

    80: create_gift("Goddess Ribbon", 0, ["Wearable", "Cloth", "Defense"]),

    81: create_gift("Coin of Slumber", 0, ["Wearable", "Defense", "Charm"]),

    82: create_gift("Coin of Defense", 0, ["Wearable", "Defense", "Charm"]),

    83: create_gift("Lucky Coin", 0, ["Wearable", "Defense", "Charm", "Lucky", "Luck"]),

    84: create_gift("Talisman Coin", 0, ["Wearable", "Defense", "Charm"]),

    85: create_gift("Shiny Coin", 0, ["Wearable", "Defense", "Charm"]),

    86: create_gift("Souvenir Coin", 0, ["Wearable", "Defense", "Charm"]),

    87: create_gift("Diadem of Kings", 0, ["Wearable", "Jewelry", "Defense", "Artifact", "FireProof", "WaterProof","LightProof"]),

    88: create_gift("Cookie", 7, ["Confectionary", "Comsumable", "Heal", "Food"]),

    89: create_gift("Bag of Fries", 8, ["FastFood", "Comsumable", "Heal", "Food", "Potato", "Processed", "Salted", "Vegetable"]),

    90: create_gift("Hamburger", 14, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed", "Meat"]),

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

    223: create_gift("Cup of Noodles", 0, ["Food", "Consumable", "Heal", "FastFood", "Pasta"]),

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

    247: create_gift("Magic Pudding", 0, ["Comsumable", "Mana", "Food", "Candy", "PSI"]),

    248: create_gift("Non-Stick Frypan", 0, ["MeleeWeapon", "Metal", "Cooking", "Tool", "Weapon"]),

    249: create_gift("Mr. Saturn Coin", 0, ["Wearable", "Defense", "Charm"]),

    250: create_gift("Meteornium", 0, ["Mineral", "SellFodder", "Artifact", "Brown", "SpaceMineral"]),

    251: create_gift("Popsicle", 0, ["Consumable", "Food", "Heal", "Candy", "FrozenFood"]),

    252: create_gift("Cup of Lifenoodles", 0, ["Consumable", "Food", "Cure", "Revive", "Pasta"])
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