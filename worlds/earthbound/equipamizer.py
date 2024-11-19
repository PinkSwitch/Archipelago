from dataclasses import dataclass
import dataclasses
from typing import Dict
from .text_data import text_encoder, eb_text_table, calc_pixel_width
from operator import attrgetter
import struct


def roll_resistances(world, element, armor):
    chance = world.random.randint(0, 100)
    if chance < 11:
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
        "Ultimate",
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
        "Gutsy",
        "Hyper",
        "Crusher",
        "Thick",
        "Deluxe",
        "Chef's",
        "Cracked",
        "Plastic",
        "Cotton",
        "Mr. Baseball",
        "Razor",
        "Gilded",
        "Master",
        "Fighter's",
        "Worn",
        "Magicant",
        "Happy",
        "Well-Done",
        "Rare",
        "Gnarly",
        "Wicked",
        "Bionic",
        "Combat"
    ]

    other_adjectives = adjectives.copy()
    arm_adjectives = adjectives.copy()
    body_adjectives = adjectives.copy()

    armor_dict = {
        "arm": arm_adjectives,
        "body": body_adjectives,
        "other": other_adjectives
    }

    equalized_names = [
        "Mild",
        "Earth",
        "Sea"
    ]

    ult_names = [
        "Day",
        "Sun",
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
        ]
    }

    plain_elemental_names = [
        "Dark",
        "Cloud",
        "Night",
        "Puddle",
        "Drizzle",
        "Rain",
        "Smoke",
        "Ember",
        "Flame",
        "Mild",
        "Earth",
        "Sea",
        "Day",
        "Sun",
        "Star"
    ]

    usage_bytes = {
        "All": 0x0F,
        "Ness": 0x01,
        "Paula": 0x02,
        "Jeff": 0x03,
        "Poo": 0x04
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
        "Summers Platinum Band",
        "Summers Diamond Band"

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
        "arm": ["bracelet", "band", "bracer", "gauntlet", "sleeve", "glove", "bangle", "armlet", "sweatband"],
        "other": ["cap", "hat", "coin", "crown", "diadem", "helmet", "mask", "wig", "pants", "jeans", "grieves", "boot"]
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
        can_equip: str
        equip_type: str

    world.armor_list: Dict[str, EBArmor] = {
        "Travel Charm": EBArmor("None", 0x15583A, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Great Charm": EBArmor("None", 0x155861, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Crystal Charm": EBArmor("None", 0x155888, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Rabbit's Foot": EBArmor("None", 0x1558AF, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Flame Pendant": EBArmor("None", 0x1558D6, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Rain Pendant": EBArmor("None", 0x1558FD, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Night Pendant": EBArmor("None", 0x155924, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Sea Pendant": EBArmor("None", 0x15594B, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Star Pendant": EBArmor("None", 0x155972, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Cloak of Kings": EBArmor("None", 0x155999, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Cheap Bracelet": EBArmor("None", 0x1559C0, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Copper Bracelet": EBArmor("None", 0x1559E7, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Silver Bracelet": EBArmor("None", 0x155A0E, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Gold Bracelet": EBArmor("None", 0x155A35, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Platinum Band": EBArmor("None", 0x155A5C, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Diamond Band": EBArmor("None", 0x155A83, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Pixie's Bracelet": EBArmor("None", 0x155AAA, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Cherub's Band": EBArmor("None", 0x155AD1, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Goddess Band": EBArmor("None", 0x155AF8, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Bracer of Kings": EBArmor("None", 0x155B1F, 0, 0, 0, 0, 0, 0, 0, 0, "All", "arm"),
        "Baseball Cap": EBArmor("None", 0x155B46, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Holmes Hat": EBArmor("None", 0x155B6D, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Mr. Baseball Cap": EBArmor("None", 0x155B94, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Hard Hat": EBArmor("None", 0x155BBB, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Ribbon": EBArmor("None", 0x155BE2, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Red Ribbon": EBArmor("None", 0x155C09, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Goddess Ribbon": EBArmor("None", 0x155C30, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Coin of Slumber": EBArmor("None", 0x155C57, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Coin of Defense": EBArmor("None", 0x155C7E, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Lucky Coin": EBArmor("None", 0x155CA5, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Talisman Coin": EBArmor("None", 0x155CCC, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Shiny Coin": EBArmor("None", 0x155CF3, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Souvenir Coin": EBArmor("None", 0x155D1A, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Diadem of Kings": EBArmor("None", 0x155D41, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Earth Pendant": EBArmor("None", 0x156D8E, 0, 0, 0, 0, 0, 0, 0, 0, "All", "body"),
        "Defense Ribbon": EBArmor("None", 0x157136, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Talisman Ribbon": EBArmor("None", 0x15715D, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Saturn Ribbon": EBArmor("None", 0x157184, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Coin of Silence": EBArmor("None", 0x1571AB, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Charm Coin": EBArmor("None", 0x1571D2, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Mr. Saturn Coin": EBArmor("None", 0x1575EF, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Summers Platinum Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
        "Summers Diamond Band": EBArmor("None", 0x0, 0, 0, 0, 0, 0, 0, 0, 0, "All", "other"),
    }
    description_pointer = 0x1000

    for item in all_armor:
        if "Summers" in item:
            world.armor_list[item] = dataclasses.replace(world.armor_list["Platinum Band"])
            armor.name += "Summers"
            print(world.armor_list[item].name)
            continue
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
            front_name = world.random.choice(armor_dict[armor.equip_type])
            armor_dict[armor.equip_type].remove(front_name)
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
            armor.can_equip = world.random.choice(["Ness", "Paula", "Jeff", "Poo"])
        else:
            armor.can_equip = "All"

        if armor.can_equip != "Poo":
            armor.poo_def = 216  # defense is signed, all non-kings equipment has this value
        else:
            armor.poo_def = armor.defense

        if armor.can_equip == "Poo":
            back_name = "of kings"
            front_name = world.random.choice(armor_names[armor.equip_type]).capitalize()
        elif armor.can_equip in ["Ness", "Paula", "Jeff"]:
            back_name = char_armor_names[armor.can_equip][armor.equip_type]
        else:
            back_name = world.random.choice(armor_names[armor.equip_type])

        armor.name = front_name + " " + back_name

        pixel_length = calc_pixel_width(armor.name)
        first_armor = False
        names_to_try = armor_names[armor.equip_type].copy()
        while pixel_length > 70:
            # First we replace any spaces with half-width spaces, a common tech used in vanilla to fix long names
            if first_armor is False:
                armor.name = armor.name.replace(" ", " ")
                first_armor = True
            else:
                if names_to_try and front_name not in plain_elemental_names:
                    # If it's still too long, change the second part of the name to try and roll a shorter name
                    back_name = world.random.choice(names_to_try)
                    names_to_try.remove(back_name)
                else:
                    # If it's *STILL* too long, chop a letter off the end of the front
                    front_name = front_name[:-1]
                    if front_name == "":
                        # we ran out of letters rip
                        front_name = "Long"
                first_armor = False
                armor.name = front_name + " " + back_name

            pixel_length = calc_pixel_width(armor.name)
        
        description = f"“{armor.name}”\n"
        if armor.can_equip != "All":
            description += f"@{armor.can_equip}'s {armor.equip_type} equipment.\n"
        else:
            if armor.equip_type == "other":
                description += "@Must be equipped as “other”.\n"
            else:
                description += f"@Must be equipped on your {armor.equip_type}.\n"

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

        description = text_encoder(description, eb_text_table, 0x100)
        description = description[:-2]
        description.extend([0x13, 0x02])
        item_name = text_encoder(armor.name, eb_text_table, 25)
        item_name.extend([0x00])
        rom.write_bytes((0x310000 + description_pointer), description)
        rom.write_bytes((armor.address + 35), struct.pack("I", (0xF10000 + description_pointer)))
        rom.write_bytes(armor.address, item_name)
        rom.write_bytes(armor.address + 28, bytearray([usage_bytes[armor.can_equip]]))
        resistance = (1 * armor.fire_res) + (4 * armor.freeze_res) + (16 * armor.flash_res) + (64 * armor.par_res)
        rom.write_bytes(armor.address + 31, bytearray([armor.defense, armor.poo_def, armor.aux_stat, resistance]))
        description_pointer += len(description)
    
    sorted_armor = sorted(world.armor_list.values(), key=attrgetter("defense"))

    sorted_arm_gear = [armor for armor in sorted_armor if armor.equip_type == "arm"]
    sorted_body_gear = [armor for armor in sorted_armor if armor.equip_type == "body"]
    sorted_other_gear = [armor for armor in sorted_armor if armor.equip_type == "other"]
    price = 0
    
    # there's probably a better way to do this
    for index, armor in enumerate(sorted_arm_gear):
        price = (99 * (index + 1) + price) + (50 * armor.flash_res + armor.fire_res + armor.freeze_res + armor.par_res) + armor.defense
        if "Summers" in armor.name:
            armor.name = armor.name.replace("Summers", "")
            price = price *2
        price = min(price, 50000)
        rom.write_bytes((armor.address + 26), struct.pack("H", price))

    for index, armor in enumerate(sorted_body_gear):
        price = (60 * (index + 1) + price) + (50 * armor.flash_res + armor.fire_res + armor.freeze_res + armor.par_res) + armor.defense
        if "Summers" in armor.name:
            armor.name = armor.name.replace("Summers", "")
            price = price * 2
        price = min(price, 50000)
        rom.write_bytes((armor.address + 26), struct.pack("H", price))

    for index, armor in enumerate(sorted_other_gear):
        price = (99 * (index + 1) + price) + (50 * armor.flash_res + armor.fire_res + armor.freeze_res + armor.par_res) + armor.defense
        if "Summers" in armor.name:
            armor.name = armor.name.replace("Summers", "")
            price = price * 2
        price = min(price, 50000)
        rom.write_bytes((armor.address + 26), struct.pack("H", price))
        #TODO: FIX SUMMERS PRICING IT'S TOO HIGH AND AFFECTING THE REST OF THE NUMBERS!!!!

        # Todo; Chaos setting that randomizes type.
        # Todo; sort defense for all equipment in order by progressive armor order. This works, do it for the other types
        # Todo; Summers needs to copy the Diamond band and something else
        # test capping armor defense (50, 100, 127 for body arm other)
