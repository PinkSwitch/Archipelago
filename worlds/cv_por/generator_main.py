from BaseClasses import Item
from .Locations import get_locations
from typing import List

def generate_early(world) -> None:
    from .setup_game import setup_game
    setup_game(world)

    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)

def create_items(world) -> None:
    pool = get_item_pool(world.get_excluded_items())
    fill_pool(pool)

    world.multiworld.itempool += pool

def fill_pool(world, pool: List[Item]) -> None:
    for _ in range(len(world.multiworld.get_unfilled_locations(world.player)) - len(pool) - world.extra_item_count):  # Change to fix event count
        item = self.set_classifications(world.get_filler_item_name())
        pool.append(item)


def get_item_pool(world) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        for _ in range(data.amount):
            item = self.set_classifications(name)
            pool.append(item)

    return pool