from dataclasses import dataclass
from typing import Dict
from .text_data import text_encoder, eb_text_table
import struct


def roll_resistances(world, element, armor):
    chance = world.random.randint(0, 100)
    if chance < 5:
        setattr(armor, element, world.random.randint(1, 3))
    else:
        setattr(armor, element, 0)


def randomize_armor(world, rom):
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
        "Sleek",
        "Green",
        "Blue",
        "White",
        "Yellow",
        "Azure",
        "Emerald",
        "Handmade",
        "Hank's",
        "Real",
        "Peace",
        "Magic",
        "Protect",
        "Brass",
        "Cursed",
        "Rabbit's",
        "Odd",
        "Cheese",
        "Casual",
        "Silk",
        "Gusty",
        "Hyper",
        "Crusher",
        "Thick",
        "Deluxe",
        "Chef's",
        "Cracked",
        "Plastic",
        "Cotton"
    ]

    equalized_names = [
        "Mild",
        "Earth",
        "Sea"
    ]

    ult_names = [
        "???",
        "???",
        "Star"
    ]

    elemental_names = {
        "Flash": [
            "Dark",
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
        "Mr. Saturn Coin",

    ]

    char_armor_names = {
        "Ness": {
            "body": "tee",
            "arm": "mitt",
            "other": "pack"
        },

        "Paula": {
            "body": "dress",
            "arm": "ring",
            "other": "ribbon"
        },

        "Jeff": {
            "body": "tie",
            "arm": "watch",
            "other": "glasses"
        },
    }

    aux_stat = {
        "arm": "Luck",
        "body": "Speed",
        "other": "Luck"
    }

    armor_names = {
        "body": ["pendant", "charm", "foot", "brooch", "shirt", "amulet", "cloak", "suit", "plate", "vest", "coat"],
        "arm": ["bracelet", "band", "bracer", "gauntlet", "sleeve", "glove", "bangle", "armlet"],
        "other": ["cap", "hat", "coin", "crown", "diadem", "helmet", "mask", "wig", "pants"]
    }

    res_strength = [
        ", just a little bit",
        " somewhat",
        ""
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
        sleep_res: int
        only_char: str
        equip_type: str

    world.armor_list: Dict[str, EBArmor] = {
        "Travel Charm": EBArmor("None", 0x15583A, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Great Charm": EBArmor("None", 0x155861, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Crystal Charm": EBArmor("None", 0x155888, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Rabbit's Foot": EBArmor("None", 0x1558AF, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Flame Pendant": EBArmor("None", 0x1558D6, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Rain Pendant": EBArmor("None", 0x1558FD, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Night Pendant": EBArmor("None", 0x155924, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Sea Pendant": EBArmor("None", 0x15594B, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Star Pendant": EBArmor("None", 0x155972, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Cloak of Kings": EBArmor("None", 0x155999, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Cheap Bracelet": EBArmor("None", 0x1559C0, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Copper Bracelet": EBArmor("None", 0x1559E7, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Silver Bracelet": EBArmor("None", 0x15590E, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Gold Bracelet": EBArmor("None", 0x155A35, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Platinum Band": EBArmor("None", 0x155A5C, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Diamond Band": EBArmor("None", 0x155A83, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Pixie's Bracelet": EBArmor("None", 0x155AAA, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Cherub's Band": EBArmor("None", 0x155AD1, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Goddess Band": EBArmor("None", 0x155AF8, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Bracer of Kings": EBArmor("None", 0x155B1F, 0, 0, 0, 0, 0, 0, 0, 0, "None", "arm"),
        "Baseball Cap": EBArmor("None", 0x155B46, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Holmes Hat": EBArmor("None", 0x155B6D, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Mr. Baseball Cap": EBArmor("None", 0x155B94, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Hard Hat": EBArmor("None", 0x155BBB, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Ribbon": EBArmor("None", 0x155BE2, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Red Ribbon": EBArmor("None", 0x155C09, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Goddess Ribbon": EBArmor("None", 0x155C30, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Coin of Slumber": EBArmor("None", 0x155C57, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Coin of Defense": EBArmor("None", 0x155C7E, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Lucky Coin": EBArmor("None", 0x155CA5, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Talisman Coin": EBArmor("None", 0x155CCC, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Shiny Coin": EBArmor("None", 0x155CF3, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Souvenir Coin": EBArmor("None", 0x155D1A, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Diadem of Kings": EBArmor("None", 0x155D41, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Earth Pendant": EBArmor("None", 0x156D8E, 0, 0, 0, 0, 0, 0, 0, 0, "None", "body"),
        "Defense Ribbon": EBArmor("None", 0x157136, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Talisman Ribbon": EBArmor("None", 0x15715D, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Saturn Ribbon": EBArmor("None", 0x157184, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Coin of Silence": EBArmor("None", 0x1571AB, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Charm Coin": EBArmor("None", 0x1571D2, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other"),
        "Mr. Saturn Coin": EBArmor("None", 0x1575EF, 0, 0, 0, 0, 0, 0, 0, 0, "None", "other")
    }
    description_pointer = 0x1000

    for item in all_armor:
        armor = world.armor_list[item]
        armor.defense = world.random.randint(1, 127)

        chance = world.random.randint(0, 100)
        if chance < 8:
            armor.aux_stat = world.random.randint(1, 127)
        else:
            armor.aux_stat = 0


        if armor.equip_type != "arm":
            roll_resistances(world, "flash_res", armor)
            roll_resistances(world, "freeze_res", armor)
            roll_resistances(world, "fire_res", armor)
            roll_resistances(world, "par_res", armor)
            armor.sleep_res = 0
        else:
            armor.flash_res = 0
            armor.freeze_res = 0
            armor.fire_res = 0
            armor.par_res = 0
            # Only Arm gear can have sleep resistance; arm gear cannot have elemental resistance
            roll_resistances(world, "sleep_res", armor)

        if armor.flash_res + armor.freeze_res + armor.fire_res == 0:
            # If no resistances are active use a normal name
            front_name = world.random.choice(adjectives)
        elif armor.flash_res == armor.freeze_res == armor.fire_res:
            # Get a combined name for the level
            front_name = equalized_names[armor.flash_res - 1]
        elif armor.par_res == armor.flash_res == armor.freeze_res == armor.fire_res:
            # Should be used if Paralysis + the others all succeed
            front_name = ult_names[armor.flash_res - 1]
        else:
            # If resistances are inequal, use the strongest as the name and pull a name from its strength
            # If 2 are equal pick a random of them
            # Todo; If 2 are equal, combine them and make a combo name
            names = ("Flash", "Freeze", "Fire")
            strengths = (armor.flash_res, armor.freeze_res, armor.fire_res)
            best_elements = [(name, strength) for name, strength in zip(names, strengths) if strength == max(strengths)]
            best_name, best_strength = world.random.choice(best_elements)
            front_name = elemental_names[best_name][best_strength - 1]

        chance = world.random.randint(0, 100)
        if chance < 10:
            armor.only_char = world.random.choice(["Ness", "Paula", "Jeff", "Poo"])
        else:
            armor.only_char = "None"

        if armor.only_char != "Poo":
            armor.poo_def = 216  # defense is signed, all non-kings equipment has this value
        else:
            armor.poo_def = armor.defense

        if armor.only_char == "Poo":
            back_name = "of kings"
            front_name = world.random.choice(armor_names[armor.equip_type]).capitalize()
        elif armor.only_char in ["Ness", "Paula", "Jeff"]:
            back_name = char_armor_names[armor.only_char][armor.equip_type]
        else:
            back_name = world.random.choice(armor_names[armor.equip_type])

        armor.name = front_name + " " + back_name
        description = f"“{armor.name}”\n"
        if armor.only_char != "None":
            description += f"@{armor.only_char}'s {armor.equip_type} equipment.\n"

        description += f"@+{armor.defense} Defense.\n"
        if armor.aux_stat > 0:
            description += f"@+{armor.aux_stat} {aux_stat[armor.equip_type]}. \n"

        if armor.flash_res > 0:
            description += f"@Protects against Flash attacks{res_strength[armor.flash_res - 1]}.\n"

        if armor.freeze_res > 0:
            description += f"@Protects against Freeze attacks{res_strength[armor.freeze_res - 1]}.\n"
        
        if armor.fire_res > 0:
            description += f"@Protects against Fire attacks{res_strength[armor.fire_res - 1]}.\n"

        if armor.par_res > 0:
            description += f"@Protects against Paralysis{res_strength[armor.par_res - 1]}.\n"

        if armor.sleep_res > 0:
            description += f"@Protects against Sleep{res_strength[armor.sleep_res - 1]}.\n"

        #print(description)
        description = text_encoder(description, eb_text_table, 0x100)
        description = description[:-2]
        description.extend([0x13, 0x02])
        item_name = text_encoder(armor.name, eb_text_table, 25)
        item_name.extend([0x00])
        rom.write_bytes((0x310000 + description_pointer), description)
        rom.write_bytes((armor.address + 35), struct.pack("I", (0xF10000 + description_pointer)))
        rom.write_bytes(armor.address, item_name)
        description_pointer += len(description)
        pixel_length = 255
        

        # Todo; Chaos setting that randomizes type.
        # Todo; sort defense for all equipment in order by progressive armor order
        #todo; name truncation
        #Idea. Run a calculation. Truncate the first word by X letters and appedn .
        #Ex; Diam. Bracelet| Diamon Bracelet| D. bracelet
        #Actually, run this check with each character until it's under 70 pixels.
        #So if Diamon. Bracelet is still too long, truncate another letter
