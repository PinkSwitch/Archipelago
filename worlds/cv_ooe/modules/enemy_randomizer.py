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


def randomize_enemy_weaknesses(world) -> None:
    world.enemy_weakness_table = {}
    world.enemy_res_table = {}
    world.enemy_properties = {}
    for enemy in enemy_table:
        world.enemy_weakness_table[enemy] = []
        world.enemy_res_table[enemy] = []
        world.enemy_properties[enemy] = {"Weaknesses:": [],
                                         "Resistances": []}
        print(world.enemy_properties[enemy]["Weaknesses"])
        element_pool = ["Strike", "Slash", "Fire", "Ice", "Lightning", "Holy", "Dark", "Poison", "Curse", "Stone"]
        element_chance = 100

        for i in range(9):
            chance = world.random.randint(0, 100)
            if chance <= element_chance:
                element = world.random.choice(element_pool)
                element_pool.remove(element)
                element_chance = element_chance // 2  # Divide the chance by half for the next roll
            else:
                continue

            if i > 0:  # Only handle resistances after the first Weakness.
                if world.random.randint(0, 100) < 50:
                    world.enemy_properties[enemy]["Resistances"].append(element)
                else:
                    world.enemy_properties[enemy]["Weaknesses"].append("glorp")

        if world.random.randint(0, 100) < 11:
            world.enemy_weakness_table[enemy].append("Freeze")
    print(world.enemy_properties)