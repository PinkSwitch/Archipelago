from dataclasses import dataclass
import dataclasses
from ..game_data.text_data import text_encoder, eb_text_table, calc_pixel_width
from operator import attrgetter
import struct


def roll_resistances(world, element, armor):
    chance = world.random.randint(0, 100)
    if chance < 11:
        setattr(armor, element, world.random.randint(1, 3))
    else:
        setattr(armor, element, 0)


def price_weapons(weapons, rom):
    price = 0
    for index, weapon in enumerate(weapons):
        price = (99 * (index + 1) + price) + (2 * weapon.aux_stat) + weapon.offense
        if "Summers" in weapon.name:
            weapon.name = weapon.name.replace("Summers", "")
            rom.write_bytes((weapon.address + 26), struct.pack("H", min((price * 2), 50000)))
            item_name = text_encoder(weapon.name, eb_text_table, 25)
            item_name.extend([0x00])
            rom.write_bytes(weapon.address, item_name)
        else:
            rom.write_bytes((weapon.address + 26), struct.pack("H", price))


def price_armors(armor_pricing_list, rom):
    price = 0
    for index, armor in enumerate(armor_pricing_list):
        price = ((99 * (index + 1) + price) +
                 (50 * armor.flash_res + armor.fire_res + armor.freeze_res + armor.par_res) + armor.defense)
        if "Summers" in armor.name:
            armor.name = armor.name.replace("Summers", "")
            rom.write_bytes((armor.address + 26), struct.pack("H", min((price * 2), 50000)))
            item_name = text_encoder(armor.name, eb_text_table, 25)
            item_name.extend([0x00])
            rom.write_bytes(armor.address, item_name)
        else:
            rom.write_bytes((armor.address + 26), struct.pack("H", price))


def apply_progressive_weapons(world, weapons, progressives, rom):
    for index, item in enumerate(weapons):
        weapon = world.weapon_list[item]
        weapon.offense = progressives[index].offense
        rom.write_bytes(weapon.address + 31, bytearray([weapon.offense]))


def apply_progressive_armor(world, armors, progressives, rom):
    for index, item in enumerate(armors):
        armor = world.armor_list[item]
        armor.defense = progressives[index].defense
        rom.write_bytes(armor.address + 31, bytearray([armor.defense]))


@dataclass
class EBArmor:
    address: int
    equip_type: str
    defense: int = 0
    aux_stat: int = 0
    poo_def: int = 0
    flash_res: int = 0
    freeze_res: int = 0
    fire_res: int = 0
    par_res: int = 0
    sleep_res: int = 0
    description: str = ""
    name: str = "None"
    can_equip: str = "All"


@dataclass
class EBWeapon:
    can_equip: str
    equip_type: str
    address: int
    name: str = "None"
    offense: int = 0
    aux_stat: int = 0
    poo_off: int = 0
    miss_rate: int = 0
    description_pointer: int = 0
    description: str = ""


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
    "Combat",
    "Tee ball",
    "Sand lot",
    "Minor league",
    "Big league",
    "Hall of fame",
    "Famous",
    "Legendary",
    "Casey",
    "French",
    "Holy",
    "Pop",
    "Zip",
    "Gaia",
    "Baddest",
    "Death",
    "Spectrum",
    "Laser",
    "Moon",
    "Toy",
    "Magnum",
    "Stun",
    "Trick",
    "Dirty",
    "Washed",
    "Laundered",
    "Fresh",
    "New",
    "Old",
    "Alien",
    "T-rex's",
    "Double",
    "Non-stick",
    "Football",
    "Tennis",
    "Golf",
    "Hockey",
    "Burnt"
]

char_nums = {
    "Ness": 0x01,
    "Paula": 0x02,
    "Jeff": 0x03,
    "Poo": 0x04
}

usage_bytes = {
    "All": 0x0F,
    "Ness": 0x01,
    "Paula": 0x02,
    "Jeff": 0x04,
    "Poo": 0x08
}

type_bytes = {
    "body": 0x14,
    "arm": 0x18,
    "other": 0x1C,
    "Bash": 0x10,
    "Shoot": 0x11
}

summers_addresses = {
    "Summers Platinum Band": 0x155A5C,
    "Summers Diamond Band": 0x155A83,
    "Summers Big League Bat": 0x15535A
}

royal_names = [
    "of kings",
    "of dukes",
    "of princes",
    "of barons",
    "of lords",
    "of sultans",
    "of counts"
]


def randomize_armor(world, rom):
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
        "body": ["pendant", "charm", "foot", "brooch", "shirt",
                 "amulet", "cloak", "suit", "plate", "vest", "coat", "jersey"],
        "arm": ["bracelet", "band", "bracer", "gauntlet", "sleeve", "glove", "bangle", "armlet", "sweatband"],
        "other": ["cap", "hat", "coin", "crown", "diadem", "helmet", "mask", "wig", "pants", "jeans", "grieves", "boot"]
    }

    res_strength = [
        ", just a little bit",
        " somewhat",
        ""
    ]

    progressive_bracelets = [
    ]

    progressive_others = [
    ]

    world.armor_list = {
        "Travel Charm": EBArmor(0x15583A, "body"),
        "Great Charm": EBArmor(0x155861, "body"),
        "Crystal Charm": EBArmor(0x155888, "body"),
        "Rabbit's Foot": EBArmor(0x1558AF, "body"),
        "Flame Pendant": EBArmor(0x1558D6, "body"),
        "Rain Pendant": EBArmor(0x1558FD, "body"),
        "Night Pendant": EBArmor(0x155924, "body"),
        "Sea Pendant": EBArmor(0x15594B, "body"),
        "Star Pendant": EBArmor(0x155972, "body"),
        "Cloak of Kings": EBArmor(0x155999, "body"),
        "Cheap Bracelet": EBArmor(0x1559C0, "arm"),
        "Copper Bracelet": EBArmor(0x1559E7, "arm"),
        "Silver Bracelet": EBArmor(0x155A0E, "arm"),
        "Gold Bracelet": EBArmor(0x155A35, "arm"),
        "Platinum Band": EBArmor(0x1570E8, "arm"),
        "Diamond Band": EBArmor(0x15710F, "arm"),
        "Pixie's Bracelet": EBArmor(0x155AAA, "arm"),
        "Cherub's Band": EBArmor(0x155AD1, "arm"),
        "Goddess Band": EBArmor(0x155AF8, "arm"),
        "Bracer of Kings": EBArmor(0x155B1F, "arm"),
        "Baseball Cap": EBArmor(0x155B46, "other"),
        "Holmes Hat": EBArmor(0x155B6D, "other"),
        "Mr. Baseball Cap": EBArmor(0x155B94, "other"),
        "Hard Hat": EBArmor(0x155BBB, "other"),
        "Ribbon": EBArmor(0x155BE2, "other"),
        "Red Ribbon": EBArmor(0x155C09, "other"),
        "Goddess Ribbon": EBArmor(0x155C30, "other"),
        "Coin of Slumber": EBArmor(0x155C57, "other"),
        "Coin of Defense": EBArmor(0x155C7E, "other"),
        "Lucky Coin": EBArmor(0x155CA5, "other"),
        "Talisman Coin": EBArmor(0x155CCC, "other"),
        "Shiny Coin": EBArmor(0x155CF3, "other"),
        "Souvenir Coin": EBArmor(0x155D1A, "other"),
        "Diadem of Kings": EBArmor(0x155D41, "other"),
        "Earth Pendant": EBArmor(0x156D8E, "body"),
        "Defense Ribbon": EBArmor(0x157136, "other"),
        "Talisman Ribbon": EBArmor(0x15715D, "other"),
        "Saturn Ribbon": EBArmor(0x157184, "other"),
        "Coin of Silence": EBArmor(0x1571AB, "other"),
        "Charm Coin": EBArmor(0x1571D2, "other"),
        "Mr. Saturn Coin": EBArmor(0x1575EF, "other"),
        "Summers Platinum Band": EBArmor(0x0, "other"),
        "Summers Diamond Band": EBArmor(0x0, "other"),
    }

    for item in all_armor:
        if "Summers" in item:
            world.armor_list[item] = dataclasses.replace(
                world.armor_list[item.replace("Summers ", "")], address=summers_addresses[item]
                )
            world.armor_list[item].name += "Summers"
            continue

        armor = world.armor_list[item]
        if world.options.armorizer == 2:
            armor.equip_type = world.random.choice(["arm", "body", "other"])

        if armor.equip_type == "arm":
            progressive_bracelets.append(item)
        elif armor.equip_type == "other" and armor.can_equip == "All":
            progressive_others.append(item)

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
            back_name = world.random.choice(royal_names)
            front_name = world.random.choice(armor_names[armor.equip_type]).capitalize()
        elif armor.can_equip in ["Ness", "Paula", "Jeff"]:
            back_name = char_armor_names[armor.can_equip][armor.equip_type]
        else:
            back_name = world.random.choice(armor_names[armor.equip_type])

        armor.name = front_name + " " + back_name

        pixel_length = calc_pixel_width(armor.name)
        first_armor = False
        if armor.can_equip == "Poo":
            names_to_try = royal_names.copy()
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
        
        description = f" “{armor.name}”\n"
        if armor.can_equip != "All":
            description += f"@♪'s {armor.equip_type} equipment.\n"
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

        if armor.can_equip != "All":
            index = description.index(0xAC)
            description[index:index + 1] = bytearray([0x1C, 0x02, char_nums[armor.can_equip]])
        rom.write_bytes(armor.address, item_name)
        rom.write_bytes(armor.address + 28, bytearray([usage_bytes[armor.can_equip]]))
        resistance = (1 * armor.fire_res) + (4 * armor.freeze_res) + (16 * armor.flash_res) + (64 * armor.par_res)
        rom.write_bytes(armor.address + 31, bytearray([armor.defense, armor.poo_def, armor.aux_stat, resistance]))
        rom.write_bytes(armor.address + 25, bytearray([type_bytes[armor.equip_type]]))
        armor.description = description
    
    sorted_armor = sorted(world.armor_list.values(), key=attrgetter("defense"))

    sorted_arm_gear = [armor for armor in sorted_armor if armor.equip_type == "arm"]
    sorted_body_gear = [armor for armor in sorted_armor if armor.equip_type == "body"]
    sorted_other_gear = [armor for armor in sorted_armor if armor.equip_type == "other"]

    sorts = [
        sorted_arm_gear,
        sorted_other_gear,
        sorted_body_gear,
    ]

    prog_armors = [
        progressive_bracelets,
        progressive_others
    ]

    for i in range(3):
        price_armors(sorts[i], rom)
    
    if world.options.progressive_armor:
        for i in range(2):
            apply_progressive_armor(world, prog_armors[i], sorts[i], rom)

    for item in all_armor:
        armor = world.armor_list[item]
        rom.write_bytes((0x310000 + world.description_pointer), armor.description)
        rom.write_bytes((armor.address + 35), struct.pack("I", (0xF10000 + world.description_pointer)))
        world.description_pointer += len(armor.description)


def randomize_weapons(world, rom):
    weapon_names = {
        "Ness": ["bat", "stick", "club", "board", "racket", "cue", "pole", "paddle"],
        "Paula": ["fry pan", "frypan", "skillet", "whisk", "saucepan", "pin"],
        "Jeff": ["gun", "beam", "air gun", "beam gun", "cannon", "blaster", "pistol", "revolver"],
        "Poo": ["Sword", "Katana", "Knife", "Scisscors", "Cutter", "Blade", "Chisel", "Saw", "Axe"],
        "All": ["Yo-yo", "Slingshot"]
    }

    miss_rates = {
        "Ness": 1,
        "Paula": 1,
        "Jeff": 0,
        "Poo": 0,
        "All": 3
    }

    progressive_bats = [
    ]

    progressive_pans = [
    ]

    progressive_guns = [
    ]

    progressive_alls = [
    ]

    world.weapon_list = {
        "Cracked Bat": EBWeapon("Ness", "Bash", 0x155297),
        "Tee Ball Bat": EBWeapon("Ness", "Bash", 0x1552BE),
        "Sand Lot Bat": EBWeapon("Ness", "Bash", 0x1552E5),
        "Minor League Bat": EBWeapon("Ness", "Bash", 0x15530C),
        "Mr. Baseball Bat": EBWeapon("Ness", "Bash", 0x155333),
        "Big League Bat": EBWeapon("Ness", "Bash", 0x15535A),
        "Hall of Fame Bat": EBWeapon("Ness", "Bash", 0x155381),
        "Magicant Bat": EBWeapon("Ness", "Bash", 0x1553A8),
        "Legendary Bat": EBWeapon("Ness", "Bash", 0x1553CF),
        "Gutsy Bat": EBWeapon("Ness", "Bash", 0x1553F6),
        "Casey Bat": EBWeapon("Ness", "Bash", 0x15541D),
        "Fry Pan": EBWeapon("Paula", "Bash", 0x155444),
        "Thick Fry Pan": EBWeapon("Paula", "Bash", 0x15546B),
        "Deluxe Fry Pan": EBWeapon("Paula", "Bash", 0x155492),
        "Chef's Fry Pan": EBWeapon("Paula", "Bash", 0x1554B9),
        "French Fry Pan": EBWeapon("Paula", "Bash", 0x1554E0),
        "Magic Fry Pan": EBWeapon("Paula", "Bash", 0x155507),
        "Holy Fry Pan": EBWeapon("Paula", "Bash", 0x15552E),
        "Sword of Kings": EBWeapon("Poo", "Bash", 0x155555),
        "Pop Gun": EBWeapon("Jeff", "Shoot", 0x15557C),
        "Stun Gun": EBWeapon("Jeff", "Shoot", 0x1555A3),
        "Toy Air Gun": EBWeapon("Jeff", "Shoot", 0x1555CA),
        "Magnum Air Gun": EBWeapon("Jeff", "Shoot", 0x1555F1),
        "Zip Gun": EBWeapon("Jeff", "Shoot", 0x155618),
        "Laser Gun": EBWeapon("Jeff", "Shoot", 0x15563F),
        "Hyper Beam": EBWeapon("Jeff", "Shoot", 0x155666),
        "Crusher Beam": EBWeapon("Jeff", "Shoot", 0x15568D),
        "Spectrum Beam": EBWeapon("Jeff", "Shoot", 0x1556B4),
        "Death Ray": EBWeapon("Jeff", "Shoot", 0x1556DB),
        "Baddest Beam": EBWeapon("Jeff", "Shoot", 0x155702),
        "Moon Beam Gun": EBWeapon("Jeff", "Shoot", 0x155729),
        "Gaia Beam": EBWeapon("Jeff", "Shoot", 0x155750),
        "Yo-yo": EBWeapon("All", "Shoot", 0x155777),
        "Slingshot": EBWeapon("All", "Shoot", 0x15579E),
        "Bionic Slingshot": EBWeapon("All", "Shoot", 0x1557C5),
        "Trick Yo-yo": EBWeapon("All", "Shoot", 0x1557EC),
        "Combat Yo-yo": EBWeapon("All", "Shoot", 0x155813),
        "T-Rex's Bat": EBWeapon("Ness", "Bash", 0x15704C),
        "Ultimate Bat": EBWeapon("Ness", "Bash", 0x15709A),
        "Double Beam": EBWeapon("Jeff", "Shoot", 0x1570C1),
        "Non-stick Frypan": EBWeapon("Paula", "Bash", 0x1575C8),
        "Summers Big League Bat": EBWeapon("Ness", "Bash", 0x0),
    }

    all_weapons = [
        "Cracked Bat",
        "Tee Ball Bat",
        "Sand Lot Bat",
        "Minor League Bat",
        "Mr. Baseball Bat",
        "Big League Bat",
        "Hall of Fame Bat",
        "Magicant Bat",
        "Legendary Bat",
        "Gutsy Bat",
        "Casey Bat",
        "Fry Pan",
        "Thick Fry Pan",
        "Deluxe Fry Pan",
        "Chef's Fry Pan",
        "French Fry Pan",
        "Magic Fry Pan",
        "Holy Fry Pan",
        "Sword of Kings",
        "Pop Gun",
        "Stun Gun",
        "Toy Air Gun",
        "Magnum Air Gun",
        "Zip Gun",
        "Laser Gun",
        "Hyper Beam",
        "Crusher Beam",
        "Spectrum Beam",
        "Death Ray",
        "Baddest Beam",
        "Moon Beam Gun",
        "Gaia Beam",
        "Yo-yo",
        "Slingshot",
        "Bionic Slingshot",
        "Trick Yo-yo",
        "Combat Yo-yo",
        "T-Rex's Bat",
        "Ultimate Bat",
        "Double Beam",
        "Non-stick Frypan",
        "Summers Big League Bat"
    ]

    for item in all_weapons:
        if "Summers" in item:
            world.weapon_list[item] = dataclasses.replace(
                world.weapon_list[item.replace("Summers ", "")], address=summers_addresses[item]
                )
            world.weapon_list[item].name += "Summers"
            continue
        weapon = world.weapon_list[item]

        if world.options.weaponizer == 2:
            chance = world.random.randint(1, 100)
            if chance < 8:
                weapon.can_equip = "All"
            else:
                weapon.can_equip = world.random.choice(["Ness", "Paula", "Jeff", "Poo"])

            if item == "Tee Ball Bat":
                weapon.can_equip = "Ness"

        if weapon.can_equip == "Ness":
            progressive_bats.append(item)
        elif weapon.can_equip == "Paula":
            progressive_pans.append(item)
        elif weapon.can_equip == "Jeff":
            progressive_guns.append(item)

        if item == "Tee Ball Bat" and not world.options.progressive_weapons:
            weapon.offense = world.random.randint(3, 10)
        else:
            weapon.offense = world.random.randint(1, 127)

        if weapon.can_equip == "Poo":
            weapon.poo_off = world.random.randint(1, 127)
            front_name = world.random.choice(weapon_names[weapon.can_equip])
            back_name = world.random.choice(royal_names)
        else:
            weapon.poo_off = 250
            front_name = world.random.choice(adjectives)
            back_name = world.random.choice(weapon_names[weapon.can_equip])

        chance = world.random.randint(0, 100)
        if chance < 8:
            weapon.aux_stat = world.random.randint(1, 127)
        else:
            weapon.aux_stat = 0

        if weapon.can_equip in ["Jeff", "All"]:
            weapon.equip_type = "Shoot"
        else:
            weapon.equip_type = "Bash"

        chance = world.random.randint(1, 100)
        if chance < 4 and item != "Tee Ball Bat":
            weapon.miss_rate = 12
        else:
            weapon.miss_rate = miss_rates[weapon.can_equip]

        weapon.name = front_name + " " + back_name

        pixel_length = calc_pixel_width(weapon.name)
        half_space = False

        if weapon.can_equip == "Poo":
            names_to_try = royal_names.copy()
        else:
            names_to_try = weapon_names[weapon.can_equip].copy()
        while pixel_length > 70:
            # First we replace any spaces with half-width spaces, a common tech used in vanilla to fix long names
            if half_space is False:
                weapon.name = weapon.name.replace(" ", " ")
                half_space = True
            else:
                if names_to_try:
                    # If it's still too long, change the second part of the name to try and roll a shorter name
                    back_name = world.random.choice(names_to_try)
                    names_to_try.remove(back_name)
                else:
                    # If it's *STILL* too long, chop a letter off the end of the front
                    front_name = front_name[:-1]
                    if front_name == "":
                        # we ran out of letters rip
                        front_name = "Long"
                half_space = False
                weapon.name = front_name + " " + back_name
            pixel_length = calc_pixel_width(weapon.name)

        description = f" “{weapon.name}”\n"
        if weapon.can_equip != "All":
            description += f"@♪ can equip this weapon.\n"

        description += f"@+{weapon.offense} Offense.\n"
        if weapon.aux_stat > 0:
            description += f"@+{weapon.aux_stat} Guts.\n"
        
        if weapon.miss_rate == 12:
            description += "@If you use this, you might just whiff.\n"

        description = text_encoder(description, eb_text_table, 0x100)
        description = description[:-2]
        description.extend([0x13, 0x02])
        item_name = text_encoder(weapon.name, eb_text_table, 25)
        item_name.extend([0x00])

        if weapon.can_equip != "All":
            index = description.index(0xAC)
            description[index:index + 1] = bytearray([0x1C, 0x02, char_nums[weapon.can_equip]])

        rom.write_bytes(weapon.address, item_name)
        rom.write_bytes(weapon.address + 28, bytearray([usage_bytes[weapon.can_equip]]))
        rom.write_bytes(weapon.address + 31, bytearray([
            weapon.offense, weapon.poo_off, weapon.aux_stat, weapon.miss_rate]))
        rom.write_bytes(weapon.address + 25, bytearray([type_bytes[weapon.equip_type]]))
        weapon.description = description

    sorted_weapons = sorted(world.weapon_list.values(), key=attrgetter("offense"))

    sorted_bats = [weapon for weapon in sorted_weapons if weapon.can_equip == "Ness"]
    sorted_pans = [weapon for weapon in sorted_weapons if weapon.can_equip == "Paula"]
    sorted_guns = [weapon for weapon in sorted_weapons if weapon.can_equip == "Jeff"]
    sorted_swords = [weapon for weapon in sorted_weapons if weapon.can_equip == "Poo"]
    sorted_alls = [weapon for weapon in sorted_weapons if weapon.can_equip == "All"]

    sorts = [
        sorted_bats,
        sorted_pans,
        sorted_guns,
        sorted_alls,
        sorted_swords
    ]

    prog_weapons = [
        progressive_bats,
        progressive_pans,
        progressive_guns,
        progressive_alls
    ]

    for i in range(5):
        price_weapons(sorts[i], rom)

    if world.options.progressive_weapons:
        for i in range(4):
            apply_progressive_weapons(world, prog_weapons[i], sorts[i], rom)

    for item in all_weapons:
        weapon = world.weapon_list[item]
        rom.write_bytes((0x310000 + world.description_pointer), weapon.description)
        rom.write_bytes((weapon.address + 35), struct.pack("I", (0xF10000 + world.description_pointer)))
        weapon.description_pointer = world.description_pointer
        world.description_pointer += len(weapon.description)

        # test capping armor defense (50, 100, 127 for body arm other)

        #Rom.write_bytes(progressive_waepon address + index, weapon.id)
