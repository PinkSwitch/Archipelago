import struct
from .Items import common_items, uncommon_items, rare_items, common_gear, uncommon_gear, rare_gear
from .flavor_data import random_flavors
from .text_data import lumine_hall_text, eb_text_table
from .local_data import item_id_table


def setup_gamevars(world):
    valid_starts = 14
    if world.options.magicant_mode != 00:
        valid_starts -= 1

    if world.options.random_start_location == 1:
        world.start_location = world.random.randint(1, valid_starts)
    else:
        world.start_location = 0

    if world.options.prefixed_items:
        world.multiworld.itempool.append(world.create_item("Counter-PSI Unit"))
        world.multiworld.itempool.append(world.create_item("Magnum Air Gun"))
        world.multiworld.itempool.append(world.create_item("Laser Gun"))
        world.multiworld.itempool.append(world.create_item("Shield Killer"))
        world.multiworld.itempool.append(world.create_item("Hungry HP-Sucker"))
        world.multiworld.itempool.append(world.create_item("Defense Shower"))
        world.multiworld.itempool.append(world.create_item("Baddest Beam"))
        world.multiworld.itempool.append(world.create_item("Heavy Bazooka"))
        world.common_items.append("Defense Spray")
        world.common_gear.append("Double Beam")
        world.uncommon_items.append("Slime Generator")
        world.uncommon_gear.append("Spectrum Beam")
        world.rare_gear.append("Gaia Beam")
    else:
        world.multiworld.itempool.append(world.create_item("Broken Machine"))
        world.multiworld.itempool.append(world.create_item("Broken Air Gun"))
        world.multiworld.itempool.append(world.create_item("Broken Laser"))
        world.multiworld.itempool.append(world.create_item("Broken Pipe"))
        world.multiworld.itempool.append(world.create_item("Broken Tube"))
        world.multiworld.itempool.append(world.create_item("Broken Trumpet"))
        world.multiworld.itempool.append(world.create_item("Broken Harmonica"))
        world.multiworld.itempool.append(world.create_item("Broken Bazooka"))
        world.common_items.append("Broken Spray Can")
        world.common_gear.append("Broken Gadget")
        world.uncommon_items.append("Broken Iron")
        world.uncommon_gear.append("Broken Cannon")
        world.rare_gear.append("Broken Antenna")

    world.franklinbadge_elements = [
        "thunder",
        "fire",
        "freeze",
        "flash",
        "starstorm",
        "special",
        "explosive"
    ]

    if world.options.randomize_franklinbadge_protection:
        world.franklin_protection = world.random.choice(world.franklinbadge_elements)
    else:
        world.franklin_protection = "thunder"

    world.hinted_regions = [
        "Northern Onett",
        "Onett",
        "Giant Step",
        "Twoson",
        "Peaceful Rest Valley",
        "Happy-Happy Village",
        "Lilliput Steps",
        "Threed",
        "Grapefruit Falls",
        "Belch's Factory",
        "Saturn Valley",
        "Upper Saturn Valley",
        "Milky Well",
        "Dusty Dunes Desert",
        "Gold Mine",
        "Monkey Caves",
        "Fourside",
        "Magnet Hill",
        "Monotoli Building",
        "Winters",
        "Snow Wood Boarding School",
        "Southern Winters",
        "Rainy Circle",
        "Stonehenge Base",
        "Summers",
        "Dalaam",
        "Pink Cloud",
        "Scaraba",
        "Pyramid",
        "Southern Scaraba",
        "Dungeon Man",
        "Deep Darkness",
        "Tenda Village",
        "Lumine Hall",
        "Lost Underworld",
        "Fire Spring",
        "Magicant",
        "Cave of the Present",
        "Cave of the Past"
    ]
    
    world.random.shuffle(world.hinted_regions)
    del world.hinted_regions[6:39]

    if world.options.random_start_location == 1:
        world.valid_teleports = [
            "Onett Teleport",
            "Twoson Teleport",
            "Happy-Happy Village Teleport",
            "Threed Teleport",
            "Saturn Valley Teleport",
            "Fourside Teleport",
            "Winters Teleport",
            "Summers Teleport",
            "Dalaam Teleport",
            "Scaraba Teleport",
            "Deep Darkness Teleport",
            "Tenda Village Teleport",
            "Lost Underworld Teleport"
        ]

        if world.options.magicant_mode == 0:
            world.valid_teleports.append("Magicant Teleport")

        del world.valid_teleports[world.start_location - 1]

        world.starting_teleport = world.random.choice(world.valid_teleports)

    filler_items = world.common_items + world.uncommon_items + world.rare_items + world.common_gear + world.uncommon_gear + world.rare_gear
    world.filler_drops = [item_id_table[i] for i in filler_items if i in item_id_table]
    world.filler_drops.append(0x00)
    if not world.options.prefixed_items:
        world.filler_drops.extend([0xA1, 0xD7, 0x8A, 0x2C, 0x30])
    else:
        world.filler_drops.extend([0x07, 0x05, 0x09, 0x0B, 0x10])

    if world.options.magicant_mode == 2:
        world.magicant_junk = []
        for i in range(6):
            world.magicant_junk.append(world.random.choice(filler_items))

    world.available_flavors = []
    if world.options.random_flavors:
        for i in range(4):
            chosen_flavor = world.random.choice(random_flavors)
            world.available_flavors = world.random.sample(random_flavors, 4)
    else:
        world.available_flavors = [
            "Mint flavor",
            "Strawberry flavor",
            "Banana flavor",
            "Peanut flavor"
        ]

    world.lumine_text = []
    world.prayer_player = []
    lumine_str = world.random.choice(lumine_hall_text)
    for char in lumine_str[:213]:
        world.lumine_text.extend(eb_text_table[char])
    world.lumine_text.extend([0x00])
    world.starting_money = struct.pack('<I', world.options.starting_money.value)

    prayer_player = world.multiworld.get_player_name(world.random.randint(1, world.multiworld.players))
    for char in prayer_player[:24]:
        if char in eb_text_table:
            world.prayer_player.extend(eb_text_table[char])
        else:
            world.prayer_player.extend([0x6F])
    world.prayer_player.extend([0x00])


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

    if world.options.giygas_required == 1:
        world.get_location("Giygas").place_locked_item(world.create_item("Saved Earth"))#Normal final boss
        if world.options.magicant_mode == 1:
            world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Power of the Earth"))#If required magicant
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Magicant Unlock"))
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Power of the Earth"))#If not required, place this condition on sanctuary goal
    else:
        if world.options.magicant_mode == 1:
            world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Saved Earth"))#If Magicant required but not Giygas, place goal
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Magicant Unlock"))
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Saved Earth"))# If neither final boss, place goal

    if world.options.alternate_sanctuary_goal:
        world.get_location("+2 Sanctuaries").place_locked_item(world.create_item("Alternate Goal"))

    if world.options.magicant_mode == 2:
        world.get_location("+1 Sanctuary").place_locked_item(world.create_item("Magicant Unlock"))
        world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Alternate Goal"))

    if world.options.random_start_location:
        world.multiworld.push_precollected(world.create_item(world.starting_teleport))

        #Add magicant, add sanc stuff, add alt goals...
            

##TOdo; client, rules, static location stuff
