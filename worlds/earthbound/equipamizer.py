from dataclasses import dataclass
from typing import Dict

def roll_resistances(world, element, armor):
    chance = world.random.randint(0, 100)
    if chance < 95:
        setattr(armor, element, world.random.randint(1, 3))
    else:
        setattr(armor, element, 0)

def randomize_armor(world):
    adjectives = [
        "Hard",
        "Wild",
        "Boring",
        "Lavish",
        "Grouchy",
        "Elastic",
        "Unsightly",
        "Long",
        "Wide",
        "Cheap",
        "Copper",
        "Silver",
        "Gold",
        "Platinum",
        "Diamond",
        "Jade",
        "Ruby",
        "Sapphire",
        "Pearl",
        "Dull",
        "Cold",
        "Fair",
        "Awful",
        "Bad",
        "Dry",
        "Wet",
        "Shiny",
        "Damp",
        "Elite",
        "Beefy",
        "Better",
        "Alright",
        "Okay",
        "Metal",
        "Pixie's",
        "Cherub's",
        "Demon's",
        "Goddess",
        "Sprite's",
        "Fairy's",
        "Devil's",
        "Best",
        "Spiteful",
        "Travel",
        "Great",
        "Crystal",
        "Baseball",
        "Holmes",
        "Mr. Baseball",
        "Red",
        "Talisman",
        "Defense",
        "Mr. Saturn",
        "Slumber",
        "Lucky",
        "Shiny",
        "Souvenir",
        "Silence",
        "Ulitmate",
        "Charm",
        "Saturn",
        "Tenda"
    ]

    equalized_names = [
        "???",
        "Earth",
        "Sea"
    ]

    ult_names = [
        "???",
        "Sun",
        "Star"
    ]

    elemental_names = {
        "Flash": [
            "???",
            "Cloud",
            "Night"
        ],
        "Freeze": [
            "Puddle",
            "???",
            "Rain"
        ],

        "Fire": [
            "Smoke",
            "Ember",
            "Flame"
        ]
    }

    all_armor = [
        "Cheap Bracelet"
    ]

    @dataclass
    class EBArmor:
        name: str
        address: int
        defense: int
        aux_stat: int
        poo_def: int
        flash_res: int
        freeze_res: int
        fire_res: int
        par_res: int
        only_char: str
        equip_type: str

    world.armor_list: Dict[str, EBArmor] = {
        "Cheap Bracelet": EBArmor("Cheap bracelet", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
    }

    for item in all_armor:
        armor = world.armor_list[item]
        armor.defense = world.random.randint(1,127)

        roll_resistances(world, "flash_res", armor)
        roll_resistances(world, "freeze_res", armor)
        roll_resistances(world, "fire_res", armor)
        roll_resistances(world, "par_res", armor)

        if armor.flash_res + armor.freeze_res + armor.fire_res == 0:
            #If no resistances are active use a normal name
            front_name = world.random.choice(adjectives)
        elif armor.flash_res == armor.freeze_res == armor.fire_res:
            #Get a combined name for the level
            front_name = equalized_names[armor.flash_res - 1]
        elif armor.par_res == armor.flash_res == armor.freeze_res == armor.fire_res:
            #Should be used if Paralysis + the others all succeed
            front_name = ult_names[armor.flash_res - 1]
        else:
            #If resistances are inequal, use the strongest as the name and pull a name from its strength
            #If 2 are equal pick a random of them
            names = ("Flash", "Freeze", "Fire")
            strengths = (armor.flash_res, armor.freeze_res, armor.fire_res)
            best_elements = [(name, strength) for name, strength in zip(names, strengths, strict=True) if strength == max(strengths)]
            best_name, best_strength = world.random.choice(best_elements)
            front_name = elemental_names[best_name][best_strength - 1]


        chance = world.random.randint(0,100)
        if chance < 10:
            armor.only_char = world.random.choice(["Ness", "Paula", "Jeff", "Poo"])
        else:
            armor.only_char = "None"

        if armor.only_char != "Poo":
            armor.poo_def = 216 # defense is signed, all non-kings equipment has this value
        else:
           armor.poo_def = world.random.randint(1,127)

        #Roll a 15% chance to have an aux stat increase?


#Jeff-only Arm: Watch
#Paula-nly arm equipment; Ring


#No-element body: Shirt
#Element Body: Pendant
#any-arm is bracelet, bracer, 
#Paula-Only Body: Dress
#Poo-only: Of Kings

#Jeff-only Other: Glasses
#Paula-only Other: Ribbon 

#All poo equipment should be "Of Kings"