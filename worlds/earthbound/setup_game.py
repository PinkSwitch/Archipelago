import struct, random
from .Items import common_items, uncommon_items, rare_items
from .flavor_data import random_flavors


def setup_gamevars(world):
    valid_starts = 14
    if world.options.magicant_mode != 00:
        valid_starts -= 1

    if world.options.random_start_location == 1:
        world.start_location = world.random.randint(1, valid_starts)
    else:
        world.start_location = 0

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
        valid_teleports = [
            "Onett Teleport",
            "Twoson Teleport",
            "Happy-Happy Village Teleport",
            "Threed Teleport",
            "Saturn Valley Teleport",
            "Dusty Dunes Teleport",
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
            valid_teleports.append("Magicant Teleport")

        del valid_teleports[world.start_location - 1]

        world.starting_teleport = world.random.choice(valid_teleports)

    filler_items = common_items + uncommon_items + rare_items

    if world.options.magicant_mode == 2:
        world.magicant_junk = []
        for i in range(5):
            world.magicant_junk.append(world.random.choice(filler_items))

    world.available_flavors = []
    if world.options.random_flavors:
        for i in range(4):
            chosen_flavor = world.random.choice(random_flavors)
            world.available_flavors.append(chosen_flavor)
            random_flavors.remove(chosen_flavor)
    else:
        world.available_flavors = [
            "Mint flavor",
            "Strawberry flavor",
            "Banana flavor",
            "Peanut flavor"
        ]

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
            

#TOdo; client, rules, static location stuff