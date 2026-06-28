from Options import OptionError
from .Options import StartingGlyph
from .game_data import base_glyphs, starting_glyph_pool, valid_starting_glyphs


def setup_game(world):
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
    world.multiworld.push_precollected(world.create_progress_event(world.starting_glyph))
