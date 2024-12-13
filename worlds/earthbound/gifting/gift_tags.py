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
    "Boiled Egg": ["Boiled", "Cooked", "Heal", "Consumable", "Egg", "White", "Food", "AnimalProduct"],
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

    0x04: create_gift("Broken Machine", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x05: create_gift("Broken Gadget", 109, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x06: create_gift("Broken Air Gun", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x07: create_gift("Broken Spray Can", 189, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x08: create_gift("Broken Laser", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x09: create_gift("Broken Iron", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x0A: create_gift("Broken Pipe", 149, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Pipe"]),

    0x0B: create_gift("Broken Cannon", 218, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x0C: create_gift("Broken Tube", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x0D: create_gift("Broken Bazooka", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Weapon"]),

    0x0E: create_gift("Broken Trumpet", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument"]),

    0x0F: create_gift("Broken Harmonica", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource", "Instrument"]),

    0x10: create_gift("Broken Antenna", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

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

    0x58: create_gift("Cookie", 7, ["Confectionary", "Comsumable", "Heal", "Food"]),

    0x59: create_gift("Bag of Fries", 8, ["FastFood", "Comsumable", "Heal", "Food", "Potato", "Processed", "Salted", "Vegetable"]),

    0x5A: create_gift("Hamburger", 14, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed", "Meat"]),

    0x5D: create_gift("Picnic Lunch", 24, ["ArtisanGood", "Comsumable", "Heal", "Food"]),
    #Todo; separate traits for GoodWeapon and BadWeapon
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