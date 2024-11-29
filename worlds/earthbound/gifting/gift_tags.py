from dataclasses import dataclass

@dataclass
class EarthBoundGift:
    name: str
    value: int
    traits: list



gift_properties = {
    0x02: EarthBoundGift("Teddy Bear", 178, 
        [{"Trait": "Bear",
          "Quality": 1,
          "Duration": 1},
          
          {"Trait": "Toy",
          "Quality": 1,
          "Duration": 1},

          {"Trait": "Stuffed",
          "Quality": 1,
          "Duration": 1},

          {"Trait": "Fluffy",
          "Quality": 1,
          "Duration": 1},
          
          {"Trait": "Brown",
          "Quality": 1,
          "Duration": 1},
          
          {"Trait": "MeatShield",
          "Quality": 1,
          "Duration": 1},
          
          {"Trait": "Animal",
          "Quality": 1,
          "Duration": 1},])
}

traits_list = {
    "Teddy Bear": ["Bear", "Toy", "Stuffed", "Fluffy", "Brown", "MeatShield", "Animal"],
    "Super Plush Bear": ["Bear", "Toy", "Stuffed", "Fluffy", "Brown", "MeatShield", "Animal"],
    "Boiled Egg": ["Boiled", "Cooked", "Heal", "Consumable", "Egg", "White", "Food", "AnimalProduct"],
}