import struct, random


def setup_gamevars(world):
    can_proceed = True
    if world.options.psi_shuffle == 0:
        world.teleport_list = [
            "Onett Teleport",
            "Twoson Teleport",
            "Happy-Happy Village Teleport",
            "Threed Teleport",
            "Saturn Valley Teleport",
            "Dusty Dunes Teleport",
            "Fourside Teleport",
            "Winters Teleport",
            "Summers Teleport",
            "Scaraba Teleport",
            "Dalaam Teleport",
            "Deep Darkness Teleport",
            "Tenda Village Teleport",
            "Lost Underworld Teleport",
            "Magicant Teleport",
            "Progressive Poo PSI",
            "Progressive Poo PSI"
        ]

        required_psi = [
            "Progressive Poo PSI",
            "Progressive Poo PSI",
            "Magicant Teleport",
            "Dalaam Teleport",
            "Winters Teleport"
        ]

        if world.options.magicant_mode != 0:
            world.teleport_list.remove("Magicant Teleport")
            required_psi.remove("Magicant Teleport")
            teleport_locations = 11
        else:
            teleport_locations = 12

        for i in range(len(world.teleport_list) - teleport_locations):
            chosen_location = world.random.choice(world.teleport_list)
            while chosen_location in required_psi:
                chosen_location = world.random.choice(world.teleport_list)
            world.teleport_list.remove(chosen_location)

        while can_proceed == False:
            world.random.shuffle(world.teleport_list)
            if world.teleport_list[6] == "Dalaam Teleport":
                can_proceed = True

    if world.options.character_shuffle == 0:
        world.character_list = [
            "Paula",
            "Jeff",
            "Poo",
            "Flying Man",
            "Teddy Bear",
            "Super Plush Bear"
        ]
        world.random.shuffle(world.character_list)


    if world.options.random_start_location == 1:
        world.start_location = world.random.randint(1, 14)
    else:
        world.start_location = 0

def place_static_items(world):
    world.get_location("Onett Police Station").place_locked_item(world.create_item("Onett Roadblocks Removed"))
    world.get_location("Belch Defeated").place_locked_item(world.create_item("Threed Tunnels Clear"))
    world.get_location("Dungeon Man Submarine").place_locked_item(world.create_item("Submarine to Deep Darkness"))

    world.get_location("Giant Step Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Lilliput Steps Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Milky Well Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Rainy Circle Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Magnet Hill Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Pink Cloud Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Lumine Hall Sanctuary").place_locked_item(world.create_item("Melody"))
    world.get_location("Fire Spring Sanctuary").place_locked_item(world.create_item("Melody"))

    if world.options.character_shuffle == 0:
        world.get_location("Happy-Happy Village - Prisoner").place_locked_item(world.create_item(world.character_list[0]))
        world.get_location("Threed - Zombie Prisoner").place_locked_item(world.create_item(world.character_list[1]))
        world.get_location("Snow Wood - Bedroom").place_locked_item(world.create_item(world.character_list[2]))
        world.get_location("Monotoli Building - Monotoli Character").place_locked_item(world.create_item(world.character_list[3]))
        world.get_location("Dalaam - Throne Character").place_locked_item(world.create_item(world.character_list[4]))
        world.get_location("Deep Darkness - Barf Character").place_locked_item(world.create_item(world.character_list[5]))

    if world.options.giygas_required == 1:
        world.get_location("Giygas").place_locked_item(world.create_item("Saved Earth"))#Normal final boss
        if world.options.magicant_mode == 1:
            world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Power of the Earth"))#If required magicant
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Power of the Earth"))#If not required, place this condition on sanctuary goal
    else:
        if world.options.magicant_mode == 1:
            world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Saved Earth"))#If Magicant required but not Giygas, place goal
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Saved Earth"))# If neither final boss, place goal

        #Add magicant, add sanc stuff, add alt goals...
            

#TOdo; client, rules, static location stuff