import struct

enemy_table = [
    "Bat",
    "Zombie",
    "Skeleton",
    "Ghost",
    "Banshee",
    "Bone Scimitar",
    "Sea Stinger",
    "Nominon",
    "Axe Knight",
    "Une",
    "Merman",
    "Necromancer",
    "Bone Archer",
    "Spear Guard",
    "Invisible Man",
    "Gelso",
    "Needles",
    "Demon",
    "Fishhead",
    "Dark Octopus",
    "Killer Fish",
    "Forneus",
    "The Creature",
    "Black Crow",
    "Skull Spider",
    "Scarecrow",
    "Sea Demon",
    "Winged Guard",
    "Nightmare",
    "Rock Knight",
    "Fire Demon",
    "Bitterfly",
    "Specter",
    "Grave Digger",
    "Werebat",
    "Black Fomor",
    "Enkidu",
    "Bone Pillar",
    "Skeleton Frisky",
    "Skeleton Hero",
    "Dullahan",
    "Skeleton Rex",
    "White Dragon",
    "Saint Elmo",
    "Lorelai",
    "Edimmu",
    "Decarabia",
    "Merman",
    "Ladycat",
    "Ectoplasm",
    "Curse Diva",
    "Miss Murder",
    "Automaton ZX26",
    "Skeleton Beast",
    "Balloon",
    "Arachne",
    "Lizardman",
    "Armored Beast",
    "Yeti",
    "Thunder Demon",
    "Owl",
    "Werewolf",
    "Altair",
    "Mandragora",
    "Jersey Devil",
    "Owl Knight",
    "Chosen Une",
    "Stone Rose",
    "Mad Butcher",
    "White Fomor",
    "Evil Force",
    "Flea Man",
    "Ghoul",
    "Peeping Eye",
    "Gargoyle",
    "Blood Skeleton",
    "Black Panther",
    "Mimic",
    "Draculina",
    "Tin Man",
    "Polkir",
    "Nova Skeleton",
    "Gashida",
    "Devil",
    "Gurkha Master",
    "Red Smasher",
    "Cave Troll",
    "Blade Master",
    "Lilith",
    "Lizardman Blade",
    "Hammer Shaker",
    "Rebuild",
    "Imp",
    "Bugbear",
    "Spectral Sword",
    "Auutomaton ZX27",
    "Medusa Head",
    "Gorgon Head",
    "Mad Snatcher",
    "Great Knight",
    "King Skeleton",
    "Winged Skeleton",
    "Final Knight",
    "Jiang Shi",
    "Demon Lord",
    "Double Hammer",
    "Weapon Master",
    "Giant Skeleton",
    "Arthroverta",
    "Brachyura",
    "Maneater",
    "Rusalka",
    "Goliath",
    "Gravedorcus",
    "Albus",
    "Barlowe",
    "Wallman",
    "Blackmore",
    "Eligor",
    "Death",
    "Dracula"
]

base_elements = ["Strike", "Slash", "Fire", "Ice", "Lightning", "Holy", "Dark"]

attr_flags = {
    "Strike": 0x01,
    "Slash": 0x02,
    "Fire": 0x04,
    "Ice": 0x08,
    "Lightning": 0x10,
    "Holy": 0x20,
    "Dark": 0x40,
    "Poison": 0x0100,
    "Curse": 0x0200,
    "Stone": 0x0400,
    "Freeze": 0x0800
}


def randomize_enemy_weaknesses(world) -> None:
    if not world.options.randomize_enemy_weaknesses:
        world.enemy_properties["Tin Man"] = {"Resistances:": ["Slash"]}  # Set this so we can use it for logic

    if world.enemy_properties:
        return  # This is used for UT handling as well as not shuffling the others

    for enemy in enemy_table:
        world.enemy_properties[enemy] = {"Weaknesses:": [],
                                         "Resistances:": []}
        element_pool = ["Strike", "Slash", "Fire", "Ice", "Lightning", "Holy", "Dark", "Poison", "Curse", "Stone"]
        element_chance = 100

        for i in range(9):
            chance = world.random.randint(0, 100)
            if chance <= element_chance:
                if not i:
                    element = world.random.choice(base_elements)  # First weakness should always be a base one
                else:
                    element = world.random.choice(element_pool)
                element_pool.remove(element)
                element_chance = element_chance // 2  # Divide the chance by half for the next roll
            else:
                continue

            if i and element not in ["Poison", "Curse", "Stone"]:
                #  Ps/Cr/Stn do nothing if resisted. Also, the first weakness should never be resisted.
                if world.random.randint(0, 100) < 50:
                    world.enemy_properties[enemy]["Resistances:"].append(element)
                else:
                    world.enemy_properties[enemy]["Weaknesses:"].append(element)
            else:
                world.enemy_properties[enemy]["Weaknesses:"].append(element)

        if world.random.randint(0, 100) < 11:
            world.enemy_properties[enemy]["Weaknesses:"].append("Freeze")


def write_enemy_weaknesses(world, rom) -> None:
    for enemy in world.enemy_properties:
        weak_flags = 0
        res_flags = 0
        address = 0x020B6364 + (0x24 * enemy_table.index(enemy))
        weak_list = world.enemy_properties[enemy]["Weaknesses:"]
        res_list = world.enemy_properties[enemy]["Resistances:"]
        for attr in weak_list:
            weak_flags |= attr_flags[attr]

        for attr in res_list:
            res_flags |= attr_flags[attr]
        rom.write_to_file(address + 0x1E, "arm9", struct.pack("H", weak_flags))
        rom.write_to_file(address + 0x22, "arm9", struct.pack("H", res_flags))
        rom.write_to_file(address + 0x13, "arm9", bytearray([0x01]))  # Flag that we need to copy these in patching


def patch_enemy_weaknesses(rom) -> None:
    for i in range(len(enemy_table)):
        address = 0x020B6364 + (0x24 * i)
        copy_flag = rom.read_from_file(address + 0x13, "arm9", 1)[0]
        if copy_flag:
            rom.write_to_file(address + 0x13, "arm9", bytearray([0x00]))  # Reset this
            for j in range(2):
                props = rom.read_from_file(address + (0x1C + j * 4), "arm9", 4)
                old_props = struct.unpack("H", props[:2])[0]
                new_props = struct.unpack("H", props[2:])[0]
                old_props &= 0x8000  # Get rid of all of the bits except for the Flesh one
                props = old_props | new_props
                rom.write_to_file(address + (0x1C + j * 4), "arm9", struct.pack("I", props))
