import struct, random


def setup_gamevars(world):
    if world.options.random_start_location == 1:
        world.start_location = world.random.randint(1, 14)
    else:
        world.start_location = 0

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
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Power of the Earth"))#If not required, place this condition on sanctuary goal
    else:
        if world.options.magicant_mode == 1:
            world.get_location("Ness's Nightmare").place_locked_item(world.create_item("Saved Earth"))#If Magicant required but not Giygas, place goal
        else:
            world.get_location("Sanctuary Goal").place_locked_item(world.create_item("Saved Earth"))# If neither final boss, place goal

        #Add magicant, add sanc stuff, add alt goals...
            

#TOdo; client, rules, static location stuff