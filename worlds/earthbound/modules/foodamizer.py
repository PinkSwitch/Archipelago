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
    all_foods = {
        "Cookie": EBFood(0x58, "Undefined Item", 0, 0, 0),
        "Bag of Fries": EBFood(0x59, "Undefined Item", 0, 0, 0),
        "Hamburger": EBFood(0x5A, "Undefined Item", 0, 0, 0),
        "Boiled Egg": EBFood(0x5B, "Undefined Item", 0, 0, 0),
        # "Fresh Egg": EBFood(0x5C, "Undefined Item", 0, 0, 0),
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
        is_liquid = False
        can_repel = False
        heals_hp = False
        heals_pp = False
        heal_chance = world.random.randint(1,100)
        # Determine what type of healing item it is
        if heal_chance < 5:
            heals_hp = True
            heals_pp = True
        elif heal_chance < 15:
            heals_pp = True
        else:
            heals_hp = True
        repel_chance = world.random.randint(1,100)

        if repel_chance < 10:
            food.hp_recovery = 1
            front_name = "Repel"
            food.repel_timer = world.random.randint(0x00, 0xFF)
        else:
            if heals_hp:
                food.hp_recovery = world.random.randint(0x01, 0xFFFF)
            if heals_pp:
                food.pp_recovery = world.random.randint(0x01, 0xFFFF)

        if not food.repel_timer:
            liquid_chance = world.random.randint(1,100)
            if liquid_chance < 16:
                liquid = "pizza"