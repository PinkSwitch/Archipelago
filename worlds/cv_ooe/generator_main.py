from BaseClasses import Item, ItemClassification


class CVOoEItem(Item):
    game: str = "Castlevania: Order of Ecclesia"


def generate_early(world) -> None:
    from .setup_game import setup_game
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Order of Ecclesia" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Order of Ecclesia"]
        world.options.required_villagers.value = passthrough["required_villagers"]
        world.options.starting_area.value = passthrough["starting_area"]
        world.options.remove_large_cavern.value = passthrough["remove_large_cavern"]
        world.options.remove_training_hall.value = passthrough["remove_training_hall"]

    setup_game(world)
    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)


def create_items(world) -> None:
    print("TODO! Implement")


def create_item(world, name: str) -> CVOoEItem:
    data = set_classifications(world, name)
    return CVOoEItem(name, data.classification, data.code, world.player)


def create_progress_event(world, name: str) -> CVOoEItem:
    # Create item name [str] as a Progression Event item.
    return CVOoEItem(name, ItemClassification.progression, None, world.player)

# TODO; Options, starting stuff, events, make locations, filler gen, filler should be unique and removed, do one-time gens for master ring and queen of hearts
