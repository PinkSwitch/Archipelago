from ..game_data.local_data import item_id_table

wanted_traits = [
    "Confectionary",
    "Food",
    "Armor",
    "Weapon",
    "Medicine",
    "Cure",
    "Bomb",
    "Mana",
    "Heal",
    "Draining",
    "Consumable"
]

# If these traits are in the item, then pick randomly from the results
# If multiple fit, pick the combined highest quality.
special_traits = {
    ("Beef"): ["Hamburger", "Double Burger", "Mammoth Burger"],
    ("Jerky"): ["Beef Jerky", "Spicy Jerky", "Luxury Jerky"],
    ("Egg"): ["Fresh Egg", "Boiled Egg"],
    ("Rock", "Candy"): ["Rock Candy"],
    ("Pasta", "Life"): ["Cup of Lifenoodles"],
    ("Chicken"): ["Chicken"],
    ("Spicy"): ["Jar of Hot Sauce", "Spicy Jerky"],
    ("Broken"): ["Broken Machine", "Broken Gadget", "Broken Air Gun", "Broken Spray Can",
                 "Broken Laser", "Broken Iron", "Broken Pipe", "Broken Cannon", "Broken Tube",
                 "Broken Bazooka", "Broken Trumpet", "Broken Harmonica", "Broken Antenna"],
    ("Pizza"): ["Pizza", "Large Pizza"],
    ("Condiment"): ["Ketchup Packet", "Sugar Packet", "Salt Packet", "Tin of Cocoa",
                    "Carton of Cream", "Sprig of Parsley", "Jar of Delisauce", "Jar of Hot Sauce"],
    ("Dairy"): ["Plain Yogurt", "Trout Yogurt", "Gelato de Resort"],
    ("AnimalProduct"): ["Fresh Egg"],
    ("Copper"): ["Copper Bracelet"],
    ("Silver"): ["Silver Bracelet"],
    ("Gold"): ["Gold Bracelet"],
    ("Diamond"): ["Diamond Bracelet"],
    ("Herb"): ["Refreshing Herb", "Secret Herb"],
    ("Repellant"): ["Repel Sandwich", "Repel Superwich"],
    ("Slime"): ["Slime Generator"],
    ("Animal"): ["Chicken", "Chick", "Snake", "Viper"],
    ("Juice"): ["Can of Fruit Juice"],
    ("Meat"): ["Hamburger", "Double Burger", "Mammoth Burger", "Beef Jerky",
               "Spicy Jerky", "Luxury Jerky", "Kabob"]

}

scaled_traits = [
    "Armor",
    "Weapon",
    "Medicine",
    "Cure",
    "Bomb",
    "AntiNumb",
    "FireProof",
    "WaterProof",
    "LightProof",
    "Mana",
    "Heal",
    "Life",
    "Neutralizing",
    "Draining"
]

backup_traits = [
    "Confectionary",
    "Food",
    "Consumable",
    "Jewelry",
    "Baseball",
    "Tool"
]

gift_by_quality = {
    "Heal": {
        0.06: "Cookie",
        0.08: "Can of Fruit Juice",
        0.12: "Cup of Coffee",
        0.18: "Popsicle",
        0.22: "Banana",
        0.24: "Bag of Fries",
        0.30: "Trout Yogurt",
        0.35: "Bread Roll",
        0.42: "Bean Croquette",
        0.43: "Cup of Noodles",
        0.45: "Boiled Egg",
        0.48: "Hamburger",
        0.60: "Royal Iced Tea",
        0.63: "Calorie Stick",
        0.65: "Croissant",
        0.70: "Lucky Sandwich",
        0.80: "Picnic Lunch",
        0.82: "Plain Roll",
        0.84: "Fresh Egg",
        0.88: "Molokheiya Soup",
        0.96: "Double Burger",
        1.00: "Peanut Cheese Bar",
        1.10: "Pasta di Summers",
        1.20: "Pizza",
        1.26: "Kabob",
        1.50: "Beef Jerky",
        1.60: "Plain Yogurt",
        2.05: "Mammoth Burger",
        2.16: "Bowl of Rice Gruel",
        2.20: "Chef's Special",
        2.52: "Spicy Jerky",
        2.40: "Large Pizza",
        3.00: "Piggy Jelly",
        3.10: "Luxury Jerky",
        3.50: "Brain Food Lunch",
        4.00: "Kraken Soup",
        4.01: "Hand-Aid"
    },

    "Armor": {
        0.05: "Travel Charm",
        0.10: "Great Charm",
        0.12: "Cheap Bracelet",
        0.13: "Baseball Cap",
        0.14: "Mr. Baseball Cap",
        0.24: "Copper Bracelet",
        0.26: "Holmes Hat",
        0.20: "Crystal Charm",
        0.36: "Silver Bracelet",
        0.38: "Hard Hat",
        0.48: "Ribbon",
        0.50: "Diadem of Kings",
        0.60: "Red Ribbon",
        0.73: "Gold Bracelet",
        0.75: "Bracer of Kings",
        0.78: "Coin of Slumber",
        0.97: "Platinum Band",
        0.98: "Defense Ribbon",
        0.99: "Coin of Defense",
        1.00: "Cloak of Kings",
        1.21: "Diamond Band",
        1.25: "Lucky Coin",
        1.46: "Pixie's Bracelet",
        1.48: "Talisman Coin",
        1.50: "Talisman Ribbon",
        1.70: "Cherub's Band",
        1.75: "Shiny Coin",
        1.95: "Goddess Band",
        2.00: "Souvenir Coin",
        2.19: "Saturn Ribbon",
        2.68: "Goddess Ribbon"


    }
}


def trait_interpreter(gift):
    for trait in gift["Traits"]:
        if trait["Trait"] in scaled_traits:
            item_quality_table = gift_by_quality[trait["Trait"]]
            quality = min(item_quality_table.keys(), key=lambda x: abs(x - trait["Quality"]))
            item = item_quality_table[quality]
            break
    item = item_id_table[item]
    return item


# IF trait is in special traits, give that item.
# Else if the trait is in a Scaled trait (Food, Armor, etc., then break them up by scaling)
