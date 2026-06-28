from Options import OptionError
from .Options import StartingGlyph, RandomizeVillagers
from .game_data import base_glyphs, starting_glyph_pool, valid_starting_glyphs
from .generator_main import create_progress_event


def setup_game(world) -> None:
    if world.options.starting_glyph == StartingGlyph.option_random_base:
        world.starting_glyph = world.random.choice(base_glyphs)  # Pick a random base-level glyph
    elif world.options.starting_glyph == StartingGlyph.option_random_any:
        world.starting_glyph = world.random.choice(starting_glyph_pool)  # Pick any random valid glyph
    else:
        glyph = world.options.starting_glyph.value.title()
        if glyph not in valid_starting_glyphs:  # if it's not valid, error out
            raise OptionError(f"Option Error for Player {world.player_name}. Attempted to set invalid Starting Glyph '{glyph}'.")
        else:
            world.starting_glyph = glyph  # If valid custom glyph is found, use it as the starting glyph
    world.multiworld.push_precollected(create_progress_event(world.starting_glyph))  # Collect the starting glyph as an Event item.

    if world.options.start_with_lizard_tail:
        world.multiworld.push_precollected(create_progress_event("Lizard Tail"))

    if world.options.start_with_glyph_sleeve:
        world.multiworld.push_precollected(create_progress_event("Glyph Sleeve"))

    if world.options.start_with_glyph_union:
        world.multiworld.push_precollected(create_progress_event("Glyph Union"))

    for villager in world.options.starting_villagers:
        world.multiworld.push_precollected(create_progress_event(villager))


def place_static_items(world) -> None:
    world.get_location("Final Approach: Dracula").place_locked_item(world.create_item("Dracula Defeated"))

    if not world.options.shuffle_dominus:  # If the player turned this off, place these vanilla
        world.get_location("Minera Prison Island: Albus 1").place_locked_item(world.create_item("Dominus Hatred"))
        world.get_location("Giant's Dwelling: Albus 2").place_locked_item(world.create_item("Dominus Anger"))
        world.get_location("Mystery Manor: Albus 3").place_locked_item(world.create_item("Dominus Agony"))

    if world.options.randomize_villagers != RandomizeVillagers.option_anywhere:
        # A list of villagers and their corresponding original location
        villager_pool = {
            "Nikolai": "Wygol Village: Grounded Chest",
            "Jacob": "Kalidus Channel: Hallway Item 1",
            "Abram": "Minera Prison Island: Lowest Room",
            "Laura": "Tymeo Mountains: Side Room",
            "Eugen": "Lighthouse: Right Hall",
            "Aeon": "Minera Prison Island: Top Room",
            "Marcel": "Tymeo Mountains: Right Exit Item",
            "George": "Skeleton Cave: Final Room Pickup",
            "Serge": "Somnus Reef: Right Side Cave Item",
            "Anna": "Somnus Reef: Hidden Room",
            "Monica": "Kalidus Channel: Deepest Room",
            "Irina": "Tristis Pass: Room Behind Waterfall",
            "Daniela": "Giant's Dwelling: First Corner"}

        if world.options.randomize_villagers == RandomizeVillagers.option_shuffled:
            zip(world.random.shuffle(villager_pool.keys()), villager_pool.values())  # Shuffle as neeeded

        for villager in villager_pool:  # Place the corresponding items/locations here
            if villager not in world.multiworld.precollected_items(world.player):
                world.get_location(villager_pool[villager].place_locked_item(world.create_item(villager)))
        