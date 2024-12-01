from dataclasses import dataclass
from typing import List

gift_qualities = {
    "Super Plush Bear": {"Stuffed": 2, "MeatShield": 3},
    "Boiled Egg": ["Boiled", "Cooked", "Heal", "Consumable", "Egg", "White", "Food", "AnimalProduct"],
}

@dataclass
class EarthBoundGift:
    name: str
    value: int
    traits: list


def make_trait(trait: str, name, quality = 1, duration: float = 1):
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

    0x0D: create_gift("Broken Bazooka", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x0E: create_gift("Broken Trumpet", 0, ["Broken", "Machine", "Metal", "Material", "Electronics", "Resource"]),

    0x58: create_gift("Cookie", 7, ["Confectionary", "Comsumable", "Heal", "Food"]),

    0x59: create_gift("Bag of Fries", 8, ["FastFood", "Comsumable", "Heal", "Food", "Potato", "Processed", "Salted"]),

    0x5A: create_gift("Hamburger", 14, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Processed"]),

    0x5D: create_gift("Picnic Lunch", 24, ["ArtisanGood", "Comsumable", "Heal", "Food"]),
}