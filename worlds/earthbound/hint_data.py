from .local_data import item_id_table

def setup_hints(world):
    hint_types = [
        "item_at_location",  #gives a hint for a specific out of the way location in this player's world, regardless of what item it is 
        "region_progression_check",  # woth or foolish hint, checks specific location groups of this world so as to be more helpful.
        "hint_for_good_item", # gives the exact location and sender of a good item for the local player
        "item_in_local_region", # Hints a random item that can be found in a specific local location group
        "prog_item_at_region", #Hints the region that a good item can be found for this player
        "joke_hint" # Doesn't hint anything
        #specific characters?
        #dungeon er?
    ]
    world.in_game_hint_types = []
    world.hinted_locations = {}
    world.hinted_regions = {}
    world.hint_text = {}

    local_hintable_locations = [
        "Onett - Mayor Pirkle",
        "Onett - South Road Present",
        "Onett - Meteor Item",
        "Onett - Treehouse Guy",
        "Twoson - Orange Kid Donation",
        "Twoson - Everdred Meeting",
        "Twoson - Apple Kid Invention",
        "Fourside - Post-Moonside Delivery",
        "Lost Underworld - Talking Rock",
        "Dungeon Man - 2F Hole Present",
        "Poo Starting Item",
        "Summers - Magic Cake",
        "Deep Darkness - Teleporting Monkey",
        "Twoson - Insignificant Location",
        "Peaceful Rest Valley - North Side Present",
        "Twoson - Paula's Mother",
        "Happy-Happy Village - Prisoner",
        "Threed - Boogey Tent Trashcan",
        "Threed - Zombie Prisoner",
        "Grapefruit Falls - Saturn Cave Present",
        "Saturn Valley - Saturn Coffee",
        "Dusty Dunes - South Side Present",
        "Stonehenge - Tony Item",
        "Stonehenge - Kidnapped Mr. Saturn",
        "Stonehenge - Dead End Present",
        "Stonehenge - Near End of the Maze Present",
        "Stonehenge - Bridge Room East Balcony Present",
        "Gold Mine - B1F Isolated Present",
        "Fourside - Venus Gift",
        "Fourside - Bakery 2F Gift",
        "Fourside - Department Store Blackout",
        "Monotoli Building - Monotoli Character",
        "Dungeon Man - 1F Exit Ledge Present",
        "Deep Darkness - Barf Character",
        "Lumine Hall - B1F West Alcove Present",
        "Cave of the Present - Star Master",
        "Cave of the Present - Broken Phase Distorter",
        "Fire Spring - 1st Cave Present",
        "Tenda Village - Tenda Tea",
        "Deep Darkness - Barf Character",
        "Dalaam - Trial of Mu",
        "Pyramid - Northwest Door Sarcophagus"
    ]

    local_hintable_items = [
        "Franklin Badge",
        "Key to the Shack",
        "Key to the Cabin",
        "Key to the Tower",
        "Key to the Locker",
        "Bad Key Machine",
        "Pencil Eraser",
        "Eraser Eraser",
        "UFO Engine",
        "Yogurt Dispenser",
        "Zombie Paper",
        "King Banana",
        "Signed Banana",
        "Tendakraut",
        "Jar of Fly Honey",
        "Wad of Bills",
        "Tiny Ruby",
        "Diamond",
        "Meteorite Piece",
        "Hieroglyph Copy",
        "Piggy Nose",
        "Carrot Key",
        "Police Badge",
        "Letter For Tony",
        "Mining Permit",
        "Contact Lens",
        "Insignificant Item",
        "Pak of Bubble Gum",
        "Sea Pendant",
        "Shyness Book",
        "Hawk Eye",
        "Paula",
        "Jeff",
        "Poo",
        "Onett Teleport",
        "Twoson Teleport",
        "Happy-Happy Village Teleport",
        "Threed Teleport",
        "Saturn Valley",
        "Dusty Dunes Teleport",
        "Fourside Teleport",
        "Winters Teleport",
        "Summers Teleport",
        "Scaraba Teleport"
        "Dalaam Teleport",
        "Deep Darkness Teleport",
        "Tenda Village Teleport",
        "Lost Underworld Teleport"
    ]

    if world.options.magicant_mode.value in [0, 3]:
        local_hintable_items.append("Magicant Teleport")

    if world.options.giygas_required:
        local_hintable_locations.append("Cave of the Past - Present")
    
    if world.options.magicant_mode == 0:
        local_hintable_locations.append("Magicant - Ness's Nightmare")

    for i in range(6):
        world.in_game_hint_types.append(world.random.choice(hint_types))

    for index, hint in enumerate(world.in_game_hint_types):
        if hint == "item_at_location":
            location = world.random.choice(local_hintable_locations)
            text = f"PLAYER's ITEM can be found at {location}."
            world.hint_text[index] = text
            world.hinted_locations[index] = location
        elif hint == "hint_for_good_item":
            item = world.random.choice(local_hintable_items)
            text = "your ITEM can be found by PLAYER at LOCATION." #delete by player if it's local?

def parse_hint_data(world, location, text, hint):
    #Check hint types? yeah, I'll do it by hint type
    if hint == "item_at_location":
        if world.player == location.item.player:
            text = text.replace("PLAYER's", "your")
        else:
            text = text.replace("PLAYER", world.multiworld.get_player_name(location.item.player))

        if world.player == location.item.player and location.item.name in item_id_table:
            text = text.replace("ITEM", f"{hex(0x1C05)}{item_id_table[location.item.name]}")
        else:
            text = text.replace("ITEM", location.item.name)
        print(text)

def write_hints(world, rom):
    print("hi")



    #Word on the street is that PLAYER's ITEM can be found at LOCATION
    #Word on the street is that REGION may be hiding a critical item. in PLAYER's world.../may be hiding an import-sounding item./may have nothing of much conseuqence.
    #Word on the street is that your ITEM can be found by PLAYER at LOCATION
    #Word on the street is that ITEM can be found somewhere near REGION...
    #Word on the street is that your ITEM can be found somewhere near REGION...
    #char item hint?
    #That's all for today.
    #I should delete this function. I can write and translate the hints in the second function instead. Instead of doing the whole replace bit, I can + add to the text or chain them together?
    #Like text part 1, extend 0x1C 0x05 0xItem Item, extend (the rest of the string)