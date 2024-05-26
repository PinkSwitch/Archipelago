import struct, random


def setup_gamevars(world):
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

        world.random.shuffle(world.teleport_list)

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

def place_static_items(self):
    self.get_location("Onett Police Station").place_locked_item(self.create_item("Onett Roadblocks Removed"))
    self.get_location("Belch Defeated").place_locked_item(self.create_item("Threed Tunnels Clear"))
    self.get_location("Dungeon Man Submarine").place_locked_item(self.create_item("Submarine to Deep Darkness"))

    self.get_location("Giant Step Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Lilliput Steps Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Milky Well Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Rainy Circle Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Magnet Hill Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Pink Cloud Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Lumine Hall Sanctuary").place_locked_item(self.create_item("Melody"))
    self.get_location("Fire Spring Sanctuary").place_locked_item(self.create_item("Melody"))

    if self.options.psi_shuffle == 0:
        print(self.teleport_list)
        self.get_location("Onett - Buzz Buzz").place_locked_item(self.create_item(self.teleport_list[0]))
        self.get_location("Onett - Mani Mani Statue").place_locked_item(self.create_item(self.teleport_list[1]))
        self.get_location("Saturn Valley - Saturn Coffee").place_locked_item(self.create_item(self.teleport_list[2]))
        self.get_location("Monkey Caves - Monkey Power").place_locked_item(self.create_item(self.teleport_list[3]))
        self.get_location("Fourside - Department Store Blackout").place_locked_item(self.create_item(self.teleport_list[4]))
        self.get_location("Summers - Magic Cake").place_locked_item(self.create_item(self.teleport_list[5]))
        self.get_location("Dalaam - Trial of Mu").place_locked_item(self.create_item(self.teleport_list[6]))
        self.get_location("Scaraba - Star Master").place_locked_item(self.create_item(self.teleport_list[7]))
        self.get_location("Tenda Village - Tenda Tea").place_locked_item(self.create_item(self.teleport_list[8]))
        self.get_location("Lost Underworld - Talking Rock").place_locked_item(self.create_item(self.teleport_list[9]))
        self.get_location("Cave of the Present - Star Master").place_locked_item(self.create_item(self.teleport_list[10]))
        if self.options.magicant_mode == 0:
            self.get_location("Magicant - Ness's Nightmare").place_locked_item(self.create_item(self.teleport_list[11]))

    if self.options.character_shuffle == 0:
        self.get_location("Happy-Happy Village - Prisoner").place_locked_item(self.create_item(self.character_list[0]))
        self.get_location("Threed - Zombie Prisoner").place_locked_item(self.create_item(self.character_list[1]))
        self.get_location("Snow Wood - Bedroom").place_locked_item(self.create_item(self.character_list[2]))
        self.get_location("Monotoli Building - Monotoli Character").place_locked_item(self.create_item(self.character_list[3]))
        self.get_location("Dalaam - Throne Character").place_locked_item(self.create_item(self.character_list[4]))
        self.get_location("Deep Darkness - Barf Character").place_locked_item(self.create_item(self.character_list[5]))

    if self.options.giygas_required == 1:
        self.get_location("Giygas").place_locked_item(self.create_item("Saved Earth"))#Normal final boss
        if self.options.magicant_mode == 1:
            self.get_location("Ness's Nightmare").place_locked_item(self.create_item("Power of the Earth"))#If required magicant
        else:
            self.get_location("Sanctuary Goal").place_locked_item(self.create_item("Power of the Earth"))#If not required, place this condition on sanctuary goal
    else:
        if self.options.magicant_mode == 1:
            self.get_location("Ness's Nightmare").place_locked_item(self.create_item("Saved Earth"))#If Magicant required but not Giygas, place goal
        else:
            self.get_location("Sanctuary Goal").place_locked_item(self.create_item("Saved Earth"))# If neither final boss, place goal

        #Add magicant, add sanc stuff, add alt goals...
            

#TOdo; client, rules, static location stuff