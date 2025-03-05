from dataclasses import dataclass
from typing import Optional

@dataclass
class EBFood:
    ID: int
    name: str
    price: int
    hp_recovery: int
    pp_recovery: int
    is_liquid: Optional[bool] = False
    is_poo_food: Optional[bool] = False
    is_large: Optional[bool] = False
    repel_timer: Optional[int] = 0


def randomize_food(world, rom):
    front_names = {
        "hp_recovery": [
            "Ham",
            "Chef's",
            "Bread",
            "Plain",
            "Kraken",
            "Gelato",
            "Trout",
            "Piggy",
            "Picnic",
            "Brain",
            "Royal",
            "Protein",
            "Calorie",
            "Double",
            "Peanut",
            "Beef",
            "Mammoth",
            "Spicy",
            "Luxury",
            "Cheese",
            "Peculiar",
            "Baked",
            "Bean",
            "Boiled",
            "Old",
            "Stale",
            "Moldy",
            "Cold",
            "Edible",
            "Fresh",
            "Grilled",
            "Hot",
            "Molokheiya",
            "Noble",
            "Nut",
            "Pasta",
            "Pickled",
            "Pork",
            "Meaty",
            "Strawberry",
            "Apple",
            "Cherry",
            "Wet",
            "Pack of",
            "Bag of",
            "Can of",
            "Bottle of",
            "Jug of",
            "Pitcher of",
            "Mug of",
            "Cup of",
            "Bowl of",
            "Thermos of",
            "Glass of",
            "Goblet of",
            "Chalice of",
            "Canteen of",
            "Flask of",
            "Pouch of",
            "Spoon of",
        ],
        "pp_recovery": [
            "Magic",
            "PP",
            "PSI",
            "Magic",
            "Mana",
            "Spirit",
            "Mind",
            "Soul"
        ]
    }

    back_names = {
        "drinks": [
            " juice",
            " water",
            " cola"
        ],
        "food": [
            ""
        ]
    }

    all_foods = {
        "Cookie": EBFood(0x58, "Undefined Item", 0, 0, 0),
        "Bag of Fries": EBFood(0x59, "Undefined Item", 0, 0, 0),
        "Hamburger": EBFood(0x5A, "Undefined Item", 0, 0, 0),
        "Boiled Egg": EBFood(0x5B, "Undefined Item", 0, 0, 0),
        "Picnic Lunch": EBFood(0x5D, "Undefined Item", 0, 0, 0),
        "Pasta di Summers": EBFood(0x5E, "Undefined Item", 0, 0, 0),
        "Pizza": EBFood(0x5F, "Undefined Item", 0, 0, 0),
        "Chef's Special": EBFood(0x60, "Undefined Item", 0, 0, 0),
        "Large Pizza": EBFood(0x61, "Undefined Item", 0, 0, 0),
        "PSI Caramel": EBFood(0x62, "Undefined Item", 0, 0, 0),
        "Magic Truffle": EBFood(0x63, "Undefined Item", 0, 0, 0),
        "Brain Food Lunch": EBFood(0x64, "Undefined Item", 0, 0, 0),
        "Croissant": EBFood(0x66, "Undefined Item", 0, 0, 0),
        "Bread Roll": EBFood(0x67, "Undefined Item", 0, 0, 0),
        "Can of Fruit Juice": EBFood(0x6A, "Undefined Item", 0, 0, 0),
        "Royal Iced Tea": EBFood(0x6B, "Undefined Item", 0, 0, 0),
        "Protein Drink": EBFood(0x6C, "Undefined Item", 0, 0, 0),
        "Kraken Soup": EBFood(0x6D, "Undefined Item", 0, 0, 0),
        "Bottle of Water": EBFood(0x6E, "Undefined Item", 0, 0, 0),
        "Trout Yogurt": EBFood(0xBD, "Undefined Item", 0, 0, 0),
        "Banana": EBFood(0xBE, "Undefined Item", 0, 0, 0),
        "Calorie Stick": EBFood(0xBF, "Undefined Item", 0, 0, 0),
        "Gelato de Resort": EBFood(0xC6, "Undefined Item", 0, 0, 0),
        "Magic Tart": EBFood(0xCF, "Undefined Item", 0, 0, 0),
        "Cup of Noodles": EBFood(0xDF, "Undefined Item", 0, 0, 0),
        "Repel Sandwich": EBFood(0xE0, "Undefined Item", 0, 0, 0),
        "Repel Superwich": EBFood(0xE1, "Undefined Item", 0, 0, 0),
        "Cup of Coffee": EBFood(0xE8, "Undefined Item", 0, 0, 0),
        "Double Burger": EBFood(0xE9, "Undefined Item", 0, 0, 0),
        "Peanut Cheese Bar": EBFood(0xEA, "Undefined Item", 0, 0, 0),
        "Piggy Jelly": EBFood(0xEB, "Undefined Item", 0, 0, 0),
        "Bowl of Rice Gruel": EBFood(0xEC, "Undefined Item", 0, 0, 0),
        "Bean Croquette": EBFood(0xED, "Undefined Item", 0, 0, 0),
        "Molokheiya Soup": EBFood(0xEE, "Undefined Item", 0, 0, 0),
        "Plain Roll": EBFood(0xEF, "Undefined Item", 0, 0, 0),
        "Kabob": EBFood(0xF0, "Undefined Item", 0, 0, 0),
        "Plain Yogurt": EBFood(0xF1, "Undefined Item", 0, 0, 0),
        "Beef Jerky": EBFood(0xF2, "Undefined Item", 0, 0, 0),
        "Mammoth Burger": EBFood(0xF3, "Undefined Item", 0, 0, 0),
        "Spicy Jerky": EBFood(0xF4, "Undefined Item", 0, 0, 0),
        "Luxury Jerky": EBFood(0xF5, "Undefined Item", 0, 0, 0),
        "Bottle of DXwater": EBFood(0xF6, "Undefined Item", 0, 0, 0),
        "Magic Pudding": EBFood(0xF7, "Undefined Item", 0, 0, 0),
        "Popsicle": EBFood(0xFB, "Undefined Item", 0, 0, 0),
    }

    for item in all_foods:
        food = all_foods[item]
        healing_type_roll = world.random.randint(1,100)
        consumption_type_roll = world.random.randint(1,100)
        roll_for_if_poo_item = world.random.randint(1,100)
        repel_chance_roll = world.random.randint(1,100)

        if healing_type_roll < 5:
            healing_type = "hp_and_pp"
        elif healing_type_roll < 20:
            healing_type = "pp"
        else:
            healing_type = "hp"
        food.restoration_amount = world.random.randint(0x00,0x32)

        if consumption_type_roll < 2:
            food.consumption_type = "all_food"
        elif consumption_type_roll < 15:
            food.consumption_type = "liquid"
        else:
            food.consumption_type = "food"
        
        if roll_for_if_poo_item < 10:  # 10% chance of being healing for Poo
            food.is_poo_food = True

        if repel_chance_roll < 5:  # 5% chance of repelling enemies
            food.repel_timer = world.random.randint(1, 255)

        if food.repel_timer:
            front_name = "Repel"
        elif healing_type == "pp":
            front_name = world.random.choice(front_names["pp_recovery"])
        else:
            front_name = world.random.choice(front_names["hp_recovery"])
        
        if food.consumption_type == "liquid":
            back_name = world.random.choice(back_names["drinks"])
        else:
            back_name = world.random.choice(back_names["food"])
        
        food.name = front_name + back_name
        # print(food.name)


        # Rough healing is 6 * restoration value