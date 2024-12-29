parent_traits = {
    "Life": {
        1: ["Secret Herb"],
        3: ["Horn of Life", "Cup of Lifenoodles"]
    },

    "Doll": {
        1: ["Teddy Bear"],
        3: ["Super Plush Bear"]
    },
    
    "Food": {},
}

special_traits = {
    ("Beef"): ["Hamburger", "Double Burger", "Mammoth Burger"],
    ("Jerky"): ["Beef Jerky", "Spicy Jerky", "Luxury Jerky"],
    ("Rock", "Candy"): ["Rock Candy"],
    ("Pasta", "Life"): ["Cup of Lifenoodles"],
    ("Chicken"): ["Chicken"],
    ("Spicy"): ["Jar of Hot Sauce", "Spicy Jerky"]
}


# IF trait is in special traits, give that item.
# Else if the trait is in a Scaled trait (Food, Armor, etc., then break them up by scaling)