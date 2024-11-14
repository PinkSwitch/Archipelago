from dataclasses import dataclass
from typing import Dict

def roll_resistances(world, element, armor):
    chance = world.random.randint(0, 100)
    if chance < 15:
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
        "Saturn"
    ]

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
        armor.name = "Butts"
        armor.defense = world.random.randint(1,127)

        #make this a def? or a loop at least
        roll_resistances(world, "flash_res", armor)
        roll_resistances(world, "freeze_res", armor)
        roll_resistances(world, "fire_res", armor)
        roll_resistances(world, "par_res", armor)

        chance = world.random.randint(0,100)
        if chance < 20:
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