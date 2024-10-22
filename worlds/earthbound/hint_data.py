
def setup_hints(world):
    hint_types = [
        "item_at_location",  #gives a hint for a specific out of the way location in this player's world, regardless of what item it is 
        "region_progression_check",  # woth or foolish hint, checks specific subregions of this world so as to be more helpful.
        "hint_for_good_item", # gives the exact location and player of a good item for this player
        "item_in_local_region", # Hints a random item that can be found in a specific subregion
        "prog_item_at_region", #Hints the region that a good item can be found for this player
        "joke_hint" # Doesn't hint anything
    ]
    world.in_game_hint_types = []

    for i in range(6):
        world.in_game_hint_types.append(world.random.choice(hint_types))