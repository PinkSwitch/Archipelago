from .modules.portrait_shuffle import portrait_shuffle
from .modules.quest_data import setup_quests, quest_data
from .generator_main import create_item_as_event, get_filler_item_name
from .Options import NestofEvil


def setup_game(world):
    setup_quests(world)
    portrait_shuffle(world)
    world.options.removed_boss_keys.value = {value.title() for value in world.options.removed_boss_keys.value}
    print(world.options.removed_boss_keys.value)
    if world.portrait_connections["Nest of Evil"] != "Nest of Evil" and world.options.nest_portraits.value == 8:
        world.options.nest_portraits.value = 7  # This would be otherwise impossible, so lower the count to 7


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

    world.get_location("Great Stairway: Boss Room").place_locked_item(world.create_item("Keremet Defeated"))
    world.get_location("Tower of Death: Boss Room").place_locked_item(world.create_item("Death Defeated"))

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

    for quest in world.vanilla_quests:
        if quest == "Quest: Kill Gergoth" and world.options.nest_of_evil_state == NestofEvil.option_removed:
            continue
        world.get_location(quest).place_locked_item(create_item_as_event(world, quest_data[quest].vanilla_reward))

    for quest in world.excluded_quests:
        world.get_location(quest).place_locked_item(create_item_as_event(world, get_filler_item_name(world), True))
