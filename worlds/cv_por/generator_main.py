from .Locations import get_locations

def generate_early(world) -> None:
    from .setup_game import setup_game
    setup_game(world)

    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world, get_locations(world))
    place_static_items(world)