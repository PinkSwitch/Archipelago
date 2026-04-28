from BaseClasses import Item
from .Items import item_table


class CVPoRItem(Item):
    game: str = "Castlevania: Portrait of Ruin"


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
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)

    if world.options.shuffle_whip:
        pool.append(set_classifications(world, "True Vampire Killer"))

    if world.options.add_extra_items:
        pool.extend([
            set_classifications(world, "Puppet Master"),
            set_classifications(world, "Tori"),
            set_classifications(world, "Seiryu"),
            set_classifications(world, "Suzaku"),
            set_classifications(world, "Byakko"),
            set_classifications(world, "Gnebu"),
        ])

    if not world.options.exclude_owl_morph:
        pool.append(set_classifications(world, "Owl Morph"))

    if world.options.nest_of_evil_state:
        pool.extend([
            set_classifications(world, "Greatest Five"),
            set_classifications(world, "Tome of Arms p1"),
            set_classifications(world, "Tome of Arms p2"),
        ])

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)
    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool

def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def set_classifications(world, name) -> CVPoRItem:
    # Make quest items be prog, here.
    item_data = item_table[name]
    item = CVPoRItem(name, item_data.classification, item_data.code, world.player)
    return item


def get_filler_item_name(world) -> str:
    from .Items import money_table, good_food_table, consumable_table
    weights = {"subweapon": 5, "good_weapon": 7, "accessory": 8, "good_food": 10, "good_armor": 15, "money": 20,
               "weapon": 30, "armor": 40, "consumable": 60}
    
    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    weight_table = {
        "subweapon": world.subweapon_filler_table,
        "good_weapon": world.good_weapon_table,
        "weapon": world.weapon_table,
        "armor": world.armor_table,
        "good_armor": world.good_armor_table,
        "money": money_table,
        "consumable": consumable_table,
        "good_food": good_food_table,
        "accessory": world.accessory_table
    }

    filler_item = world.random.choice(weight_table[filler_type])
    if not world.has_tried_magus_ring:
        world.has_tried_magus_ring = True
        if world.random.randint(0, 101) <= 10:  # Magus ring should have a single 10/100 chance to be placed
            filler_item = "Magus Ring"
            return filler_item

    if filler_type not in ["consumable", "good_food", "money"]:
        weight_table[filler_type].remove(filler_item)  # Remove equipment from the corresponding table so it doesn't gen again

        if not weight_table[filler_type]:  # If we have exhausted the entire pool
            weights[filler_type] = 0  # Make sure it won't be rolled again

    return filler_item

def create_item(world, name: str) -> CVPoRItem:
    data = set_classifications(world, name)
    return CVPoRItem(name, data.classification, data.code, world.player)
