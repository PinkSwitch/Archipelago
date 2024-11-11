from .enemy_data import combat_regions

area_exits = {
    "Ness's Mind": ["Onett", "Twoson", "Happy-Happy Village", "Threed", "Saturn Valley", "Dusty Dunes Desert",
                    "Fourside", "Winters", "Summers", "Dalaam", "Scaraba", "Deep Darkness", "Tenda Village",
                    "Lost Underworld", "Magicant"],
    "Northern Onett": ["Onett"],
    "Onett": ["Northern Onett", "Twoson", "Giant Step"],
    "Giant Step": ["Giant Step"],
    "Twoson": ["Onett", "Peaceful Rest Valley", "Threed", "Everdred's House"],
    "Everdred's House": ["Everdred's House"],
    "Peaceful Rest Valley": ["Twoson", "Happy-Happy Village"],
    "Happy-Happy Village": ["Peaceful Rest Valley", "Lilliput Steps"],
    "Lilliput Steps": ["Lilliput Steps"],
    "Threed": ["Twoson", "Dusty Dunes Desert", "Southern Winters", "Threed Underground", "Boogey Tent", "Winters"],
    "Boogey Tent": ["Boogey Tent"],
    "Threed Underground": ["Grapefruit Falls"],
    "Grapefruit Falls": ["Belch's Factory", "Saturn Valley", "Threed Underground"],
    "Saturn Valley": ["Grapefruit Falls", "Cave of the Present", "Upper Saturn Valley"],
    "Belch's Factory": ["Upper Saturn Valley"],
    "Upper Saturn Valley": ["Saturn Valley", "Milky Well"],
    "Milky Well": ["Milky Well"],
    "Dusty Dunes Desert": ["Threed", "Monkey Caves", "Gold Mine", "Fourside"],
    "Monkey Caves": ["Monkey Caves"],
    "Gold Mine": ["Gold Mine"],
    "Fourside": ["Dusty Dunes Desert", "Monotoli Building", "Magnet Hill", "Threed", "Fourside Dept. Store"],
    "Monotoli Building": ["Monotoli Building"],
    "Fourside Dept. Store": ["Fourside Dept. Store"],
    "Magnet Hill": ["Magnet Hill"],
    "Winters": ["Snow Wood Boarding School", "Southern Winters"],
    "Snow Wood Boarding School": ["Snow Wood Boarding School"],
    "Southern Winters": ["Winters", "Rainy Circle", "Stonehenge Base"],
    "Stonehenge Base": ["Stonehenge Base"],
    "Rainy Circle": ["Rainy Circle"],
    "Summers": ["Scaraba", "Summers Museum"],
    "Summers Museum": ["Summers Museum"],
    "Dalaam": ["Pink Cloud"],
    "Pink Cloud": ["Pink Cloud"],
    "Scaraba": ["Pyramid"],
    "Pyramid": ["Southern Scaraba"],
    "Southern Scaraba": ["Dungeon Man"],
    "Dungeon Man": ["Deep Darkness"],
    "Deep Darkness": ["Deep Darkness Darkness"],
    "Deep Darkness Darkness": ["Tenda Village", "Deep Darkness"],
    "Tenda Village": ["Lumine Hall", "Deep Darkness Darkness"],
    "Lumine Hall": ["Lost Underworld"],
    "Lost Underworld": ["Fire Spring"],
    "Fire Spring": ["Fire Spring"],
    "Magicant": ["Magicant"],
    "Cave of the Present": ["Cave of the Past"],
    "Cave of the Past": ["Endgame"],
    "Endgame": ["Endgame"]
}

area_rules = {
    "Ness's Mind": {"Onett": [["Onett Teleport"]],
                    "Twoson": [["Twoson Teleport"]],
                    "Happy-Happy Village": [["Happy-Happy Village Teleport"]],
                    "Threed": [["Threed Teleport"]],
                    "Saturn Valley": [["Saturn Valley Teleport"]],
                    "Dusty Dunes Desert": [["Dusty Dunes Teleport"]],
                    "Fourside": [["Fourside Teleport"]],
                    "Winters": [["Winters Teleport"]],
                    "Summers": [["Summers Teleport"]],
                    "Dalaam": [["Dalaam Teleport"]],
                    "Scaraba": [["Scaraba Teleport"]],
                    "Deep Darkness": [["Deep Darkness Teleport"]],
                    "Tenda Village": [["Tenda Village Teleport"]],
                    "Lost Underworld": [["Lost Underworld Teleport"]],
                    "Magicant": [["Magicant Teleport"], ["Magicant Unlock"]]
                    },

    "Northern Onett": {"Onett": [["Nothing"]]},
    "Onett": 
             {"Northern Onett": [["Police Badge"]],
              "Twoson": [["Police Badge"]],
              "Giant Step": [["Key to the Shack"]]},
    
    "Giant Step": {"Giant Step": [["Nothing"]]},

    "Twoson": {"Onett": [["Police Badge"]],
               "Peaceful Rest Valley": [["Pencil Eraser"]],
               "Threed": [["Wad of Bills"], ["Threed Tunnels Clear"]],
               "Everdred's House": [["Paula"]]},

    "Everdred's House": {"Everdred's House": [["Nothing"]]},

    "Peaceful Rest Valley": {"Twoson": [["Pencil Eraser"], ["Franklin Badge"]],
                             "Happy-Happy Village": [["Nothing"]]},

    "Happy-Happy Village": {"Peaceful Rest Valley": [["Nothing"]],
                            "Lilliput Steps": [["Nothing"]]},

    "Lilliput Steps": {"Lilliput Steps": [["Nothing"]]},

    "Threed": {"Twoson": [["Threed Tunnels Clear"]],
               "Dusty Dunes Desert": [["Threed Tunnels Clear"]],
               "Southern Winters": [["UFO Engine", "Bad Key Machine"]],
               "Threed Underground": [["Zombie Paper"]],
               "Boogey Tent": [["Jeff"]],
               "Winters": [["UFO Engine", "Bad Key Machine"]]},

    "Boogey Tent": {"Boogey Tent": [["Nothing"]]},

    "Threed Underground": {"Grapefruit Falls": [["Nothing"]]},
                             
    "Grapefruit Falls": {"Belch's Factory": [["Jar of Fly Honey"]],
                         "Saturn Valley": [["Nothing"]],
                         "Threed Underground": [["Nothing"]]},

    "Saturn Valley": {"Grapefruit Falls": [["Nothing"]],
                      "Cave of the Present": [["Meteorite Piece"]],
                      "Upper Saturn Valley": [["Threed Tunnels Clear"]]},

    "Belch's Factory": {"Upper Saturn Valley": [["Threed Tunnels Clear"]]},

    "Upper Saturn Valley": {"Saturn Valley": [["Nothing"]],
                            "Milky Well": [["Nothing"]]},

    "Milky Well": {"Milky Well": [["Nothing"]]},

    "Dusty Dunes Desert": {"Threed": [["Threed Tunnels Clear"]],
                           "Monkey Caves": [["King Banana"]],
                           "Gold Mine": [["Mining Permit"]],
                           "Fourside": [["Nothing"]]},

    "Monkey Caves": {"Monkey Caves": [["Nothing"]]},

    "Gold Mine": {"Gold Mine": [["Nothing"]]},

    "Fourside": {"Dusty Dunes Desert": [["Nothing"]],
                 "Monotoli Building": [["Yogurt Dispenser"]],
                 "Threed": [["Diamond"]],
                 "Magnet Hill": [["Signed Banana"]],
                 "Fourside Dept. Store": [["Jeff"]]},

    "Monotoli Building": {"Monotoli Building": [["Nothing"]]},

    "Fourside Dept. Store": {"Fourside Dept. Store": [["Nothing"]]},

    "Magnet Hill": {"Magnet Hill": [["Nothing"]]},

    "Winters": {"Snow Wood Boarding School": [["Letter for Tony"]],
                "Southern Winters": [["Pak of Bubble Gum"]]},

    "Snow Wood Boarding School": {"Snow Wood Boarding School": [["Nothing"]]},

    "Southern Winters": {"Stonehenge Base": [["Eraser Eraser"]],
                         "Rainy Circle": [["Nothing"]],
                         "Winters": ["Nothing"]},

    "Rainy Circle": {"Rainy Circle": [["Nothing"]]},

    "Stonehenge Base": {"Stonehenge Base": [["Nothing"]]},

    "Summers": {"Scaraba": [["Nothing"]],
                "Summers Museum": [["Tiny Ruby"]]},
    
    "Summers Museum": {"Summers Museum": [["Nothing"]]},

    "Dalaam": {"Pink Cloud": [["Carrot Key"]]},

    "Pink Cloud": {"Pink Cloud": [["Nothing"]]},

    "Scaraba": {"Pyramid": [["Hieroglyph Copy"]]},

    "Pyramid": {"Southern Scaraba": [["Nothing"]]},
    
    "Southern Scaraba": {"Dungeon Man": [["Key to the Tower"]]},

    "Dungeon Man": {"Deep Darkness": [["Submarine to Deep Darkness"]]},

    "Deep Darkness": {"Deep Darkness Darkness": [["Hawk Eye"]]},

    "Deep Darkness Darkness": {"Tenda Village": [["Nothing"]],
                               "Deep Darkness": [["Nothing"]]},

    "Tenda Village": {"Lumine Hall": [["Shyness Book"]],
                      "Deep Darkness Darkness": [["Hawk Eye"]]},

    "Lumine Hall": {"Lost Underworld": [["Nothing"]]},

    "Lost Underworld": {"Fire Spring": [["Nothing"]]},

    "Fire Spring": {"Fire Spring": [["Nothing"]]},

    "Magicant": {"Magicant": [["Nothing"]]},

    "Cave of the Present": {"Cave of the Past": [["Power of the Earth"]]},

    "Cave of the Past": {"Endgame": [["Paula"]]},

    "Endgame": {"Endgame": [["Nothing"]]}
}


def calculate_scaling(world):
    inventory = {0: ["Nothing"]}  # Nothing means no item needed for connection
    unconnected_regions = [world.starting_region, "Ness's Mind"]
    world.accessible_regions = ["Ness's Mind", world.starting_region]
    world.scaled_area_order = []
    passed_connections = []
    sphere_count = 0
    for num, sphere in enumerate(world.multiworld.get_spheres()):
        for location in sphere:
            if location.item.player == world.player:
                if num not in inventory:
                    inventory[num] = []
                inventory[num].append(location.item.name)
            
            if location.player == world.player and location.parent_region.name in combat_regions:
                valid_level_region = location.parent_region.name

            if location.item.player == world.player and location.item.name == "Paula":
                print(world.paula_region)

        if sphere == set():
            inventory[num] = []
        sphere_count = num

    for item in range(1, len(inventory)):
        if item in inventory:
            inventory[item] = inventory[item - 1] + inventory[item]
        else:
            inventory[item] = inventory[item - 1]

    for i in range(sphere_count):
        new_regions = []
        for region in unconnected_regions:
            for connection in area_exits[region]:
                if f"{region} -> {connection}" not in passed_connections:
                    for rule_set in area_rules[region][connection]:
                        # check if this sphere has the items needed to make this connection
                        can_pass = all(item in inventory[i] for item in rule_set)
                        if can_pass:
                            passed_connections.append(f"{region} -> {connection}")
                            if connection not in world.accessible_regions:
                                world.accessible_regions.append(connection)
                                new_regions.append(connection)
        unconnected_regions.extend(new_regions)

    for region in world.multiworld.get_regions(world.player):
        if region.name not in world.accessible_regions and region.name != "Menu":
            world.accessible_regions.append(region.name)

    if world.options.magicant_mode == 2 and world.options.giygas_required:
        # If magicant is an alternate goal it should be scaled after Giygas
        world.accessible_regions.remove("Magicant")
        world.accessible_regions.insert(world.accessible_regions.index("Endgame") + 1, "Magicant")
    elif world.options.magicant_mode == 3 and world.options.giygas_required:
        world.accessible_regions.insert(world.accessible_regions.index("Endgame") - 1, "Magicant")
    elif world.options.magicant_mode == 3 and not world.options.giygas_required:
        # Just add it to the end of scaling
        world.accessible_regions.append("Magicant")
    print(world.accessible_regions)

    # calculate which areas need to have enemies scaled
    for region in world.accessible_regions:
        if region in combat_regions:
            world.scaled_area_order.append(region)
    # print(world.scaled_area_order)
