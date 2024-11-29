from dataclasses import dataclass

@dataclass
class EarthBoundGift:
    name: str
    value: int



gift_properties = {
    0x02: EarthBoundGift("Teddy Bear", 178)
}

traits_list = {
    "Teddy Bear": ["Bear", "Toy", "Stuffed", "Fluffy", "Brown", "MeatShield", "Animal"],
    "Super Plush Bear": ["Bear", "Toy", "Stuffed", "Fluffy", "Brown", "MeatShield", "Animal"],
    "Boiled Egg": ["Boiled", "Cooked", "Heal", "Consumable", "Egg", "White", "Food", "AnimalProduct"],
}