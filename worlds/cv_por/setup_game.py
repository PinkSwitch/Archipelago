def setup_game(world):
    world.portrait_connections = {
        "City of Haze": "City of Haze",
        "13th Street": "13th Street",
        "Sandy Grave": "Sandy Grave",
        "Forgotten City": "Forgotten City",
        "Nation of Fools": "Nation of Fools",
        "Burnt Paradise": "Burnt Paradise",
        "Forest of Doom": "Forest of Doom",
        "Dark Academy": "Dark Academy",
        "Nest of Evil": "Nest of Evil"
    }

def place_static_items(world):
    print("TODO. THIS.")
    #world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))