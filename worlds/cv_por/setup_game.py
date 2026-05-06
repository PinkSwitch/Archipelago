from .modules.portrait_shuffle import portrait_shuffle


def setup_game(world):
    portrait_shuffle(world)


def place_static_items(world):
    world.get_location("Tower of Death: Elevator Switch").place_locked_item(world.create_item("Tower Elevator Active"))
    world.get_location("City of Haze: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("13th Street: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Sandy Grave: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Forgotten City: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Nation of Fools: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Burnt Paradise: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Forest of Doom: Boss Room").place_locked_item(world.create_item("Portrait Clear"))
    world.get_location("Dark Academy: Boss Room").place_locked_item(world.create_item("Portrait Clear"))

    if world.options.goal:
        world.get_location("Lost Gallery: Studio Portrait Fight").place_locked_item(world.create_item("Brauner Defeated"))
        world.get_location("The Throne Room: Dracula").place_locked_item(world.create_item("Dracula Defeated"))
    else:
        world.get_location("Lost Gallery: Studio Portrait Fight").place_locked_item(world.create_item("Dracula Defeated"))

    if not world.options.shuffle_whip:
        world.get_location("Master's Keep: Whip Trial").place_locked_item(world.create_item("True Vampire Killer"))

    if not world.options.nest_of_evil_state:
        world.get_location("Nest of Evil: First Item").place_locked_item(world.create_item("Tome of Arms p1"))
        world.get_location("Nest of Evil: Second Item").place_locked_item(world.create_item("Tome of Arms p2"))
        world.get_location("Nest of Evil: Doppelganger Reward").place_locked_item(world.create_item("Greatest Five"))
