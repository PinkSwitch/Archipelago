from .local_data import item_id_table, character_item_table, party_id_nums
from .text_data import eb_text_table, text_encoder
from .static_location_data import location_groups

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
    world.hinted_items = {}
    world.hinted_regions = {}

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
            #text = f"PLAYER's ITEM can be found at {location}."
            world.hinted_locations[index] = location
        
        elif hint == "region_progression_check":
            print("sadge")

        elif hint == "hint_for_good_item" or hint == "prog_item_at_region":
            item = world.random.choice(local_hintable_items)
            world.hinted_items[index] = item

        elif hint == "item_in_local_region":
            key, value = world.random.choice(list(location_groups.items()))
            group = key
            location = world.random.choice(sorted(value))
            world.hinted_regions[index] = group
            world.hinted_locations[index] = location
        else:
            print("jonkler")


def parse_hint_data(world, location, rom, hint):
    #Check hint types? yeah, I'll do it by hint type
    if hint == "item_at_location":
        if world.player == location.item.player and location.item.name in character_item_table:
            player_text = "your friend "
            item_text = bytearray([0x1C, 0x02, party_id_nums[location.item.name]]) #In-game text command to display party member names
        elif world.player == location.item.player:
            player_text = "your "
            if location.item.name in item_id_table:
                item_text = bytearray([0x1C, 0x05, item_id_table[location.item.name]]) #In-game text command to display item names
            else:
                item_text = text_encoder(location.item.name, eb_text_table, 128) #if the item doesn't have a name (e.g it's PSI)
        else:
            player_text = f"{world.multiworld.get_player_name(location.item.player)}'s "
            item_text = text_encoder(location.item.name, eb_text_table, 128)

        player_text = text_encoder(player_text, eb_text_table, 255)
        location_text = text_encoder(f"can be found at {location.name}.", eb_text_table, 255)
        text = player_text + item_text + location_text
        #[player]'s [item] can be found at [location].
        text.append(0x02)

    elif hint == "region_progression_check":
        print("help sadge")
    elif hint == "hint_for_good_item":
        if location.item.name in character_item_table:
            item_text = text_encoder("your friend ", eb_text_table, 255)
            item_text.extend([0x1C, 0x02, party_id_nums[location.item.name]])
        elif location.item.name in item_id_table:
            item_text = text_encoder("your ", eb_text_table, 255)
            item_text.extend([0x1C, 0x05, item_id_table[location.item.name]])
        else:
            item_text = text_encoder(f"your {location.item.name}", eb_text_table, 128)
        item_text.extend(text_encoder(" can be found ", eb_text_table, 255))
        if location.player != world.player:
            player_text = text_encoder(f"by {world.multiworld.get_player_name(location.player)}", eb_text_table, 255)
        else:
            player_text = text_encoder("", eb_text_table, 255)
        location_text = text_encoder(f"at {location.name}", eb_text_table, 255)
        text = item_text + player_text + location_text
        #your [item] can be found by [player] at [location]
        text.append(0x02)
    #add spaces? test all of these...

        
    rom.write_bytes(0x310000 + world.hint_pointer, text)
    #rom.write_bytes(0x310000 + world.hint_pointer, text) text call
    # rom.write_bytes(0x310000 + world.hint_pointer, text) text call 2
    world.hint_pointer = world.hint_pointer + len(text)

def write_hints(world, rom):
    print("hi")



    #Word on the street is that PLAYER's ITEM can be found at LOCATION
    #Word on the street is that REGION may be hiding a critical item. in PLAYER's world.../may be hiding an import-sounding item./may have nothing of much conseuqence.
    #Word on the street is that your ITEM can be found by PLAYER at LOCATION
    #Word on the street is that PLAYER's ITEM can be found somewhere near REGION...
    #Word on the street is that your ITEM can be found somewhere near REGION...
    #char item hint?
    #That's all for today.
    #I should delete this function. I can write and translate the hints in the second function instead. Instead of doing the whole replace bit, I can + add to the text or chain them together?
    #Like text part 1, extend 0x1C 0x05 0xItem Item, extend (the rest of the string)