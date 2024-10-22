
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

    local_hintable_locations = [
        "Lost Underworld - Talking Rock",
        "Dungeon Man - 2F Hole Present",
        "Poo Starting Item",
        "Summers - Magic Cake",
        "Onett - Mayor Pirkle",
        "Twoson - Orange Kid Donation",
        "Twoson - Everdred Meeting",
        "Onett - South Road Present",
        "Deep Darkness - Teleporting Monkey"
    ]

    for i in range(6):
        world.in_game_hint_types.append(world.random.choice(hint_types))

    print(world.in_game_hint_types)


    #Word on the street is that PLAYER's ITEM can be found at LOCATION
    #Word on the street is that REGION may be hiding a critical item./may be hiding an import-sounding item./may have nothing of much conseuqence.
    #Word on the street is that your ITEM can be found by PLAYER at LOCATION
    #Word on the street is that ITEM can be found somewhere near REGION...
    #Word on the street is that your ITEM can be found somewhere near REGION...
    #char item hint?
    #That's all for today.