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
        "Tenda",
        "Sturdy",
        "Sleek"
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
            "Drizzle",
            "Rain"
        ],

        "Fire": [
            "Smoke",
            "Ember",
            "Flame"
        ],

        "FreezeFire": [
            "???",
            "Frostburn",
            "Antipode"
        ],
        "FreezeFlash": [
            "???",
            "???",
            "???"
        ],
        "FireFlash": [
            "???",
            "???",
            "Day"
        ]
    }

    all_armor = [
        "Travel Charm",
        "Great Charm",
        "Crystal Charm",
        "Rabbit's Foot",
        "Flame Pendant",
        "Rain Pendant",
        "Night Pendant",
        "Sea Pendant",
        "Star Pendant",
        "Cloak of Kings",
        "Cheap Bracelet",
        "Copper Bracelet",
        "Silver Bracelet",
        "Gold Bracelet",
        "Platinum Band",
        "Diamond Band",
        "Pixie's Bracelet",
        "Cherub's Band",
        "Goddess Band",
        "Bracer of Kings",
        "Baseball Cap",
        "Holmes Hat",
        "Mr. Baseball Cap",
        "Hard Hat",
        "Ribbon",
        "Red Ribbon",
        "Goddess Ribbon",
        "Coin of Slumber",
        "Coin of Defense",
        "Lucky Coin",
        "Talisman Coin",
        "Shiny Coin",
        "Souvenir Coin",
        "Diadem of Kings",
        "Earth Pendant",
        "Defense Ribbon",
        "Talisman Ribbon",
        "Saturn Ribbon",
        "Coin of Silence",
        "Charm Coin",
        "Mr. Saturn Coin"

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
        "Travel Charm": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Great Charm": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Crystal Charm": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Rabbit's Foot": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Flame Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Rain Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Night Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Sea Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Star Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Cloak of Kings": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Cheap Bracelet": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Copper Bracelet": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Silver Bracelet": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Gold Bracelet": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Platinum Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Diamond Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Pixie's Bracelet": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Cherub's Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Goddess Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Bracer of Kings": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Arm"),
        "Baseball Cap": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Holmes Hat": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Mr. Baseball Cap": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Hard Hat": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Red Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Goddess Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Coin of Slumber": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Coin of Defense": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Lucky Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Talisman Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Shiny Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Souvenir Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Diadem of Kings": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Earth Pendant": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Body"),
        "Defense Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Talisman Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Saturn Ribbon": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Coin of Silence": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Charm Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other"),
        "Mr. Saturn Coin": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, "None", "Other")
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
            #Todo; If 2 are equal, combine them and make a combo name
            names = ("Flash", "Freeze", "Fire")
            strengths = (armor.flash_res, armor.freeze_res, armor.fire_res)
            best_elements = [(name, strength) for name, strength in zip(names, strengths) if strength == max(strengths)]
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

#todo: custom description bank and description stuff like "X defense", with an optional call of "Equipment for X character", and "It protects you from X element?"