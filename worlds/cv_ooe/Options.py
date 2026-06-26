from dataclasses import dataclass
from Options import (TextChoice, DefaultOnToggle, Toggle, PerGameCommonOptions, OptionGroup,
                     NamedRange, Range, Choice, OptionSet)


# TODO - IMPLEMENT
class StartingGlyph(TextChoice):
    """Which Arm Glyph you start the game with.
       Random Base selects any base-power Glyph"""
    option_random_base = 0
    option_random_any = 1
    default = 0
    display_name = "Starting Glyph"


# TODO - Implement
class ShuffleDominus(DefaultOnToggle):
    """Shuffles the three Dominus glyphs into the item pool."""
    display_name = "Shuffle Dominus"


# TODO - Implement
class StartWithLizardTail(DefaultOnToggle):
    """If disabled, Lizard Tail will be shuffled into the item pool."""
    display_name = "Start with Lizard Tail"


# TODO - Implement
class StartWithGlyphUnion(DefaultOnToggle):
    """If disabled, Glyph Union will be shuffled into the item pool."""
    display_name = "Start with Glyph Union"


# TODO - IMPLEMENT
class StartWithGlyphSleeve(Toggle):
    """If enabled, you'll start with the Glyph Sleeve."""
    display_name = "Start with Glyph Sleeve"


# TODO - IMPLEMENT
class RevealBreakableWalls(Toggle):
    """Automatically reveals all breakable walls/objects."""
    display_name = "Reveal Hidden Walls"


# TODO - IMPLEMENT
class VillagersRequired(Range):
    """How many Villagers you need to save in order to fight Barlowe."""
    display_name = "Villagers Required"
    range_start = 0
    range_end = 13
    default = 1


class ExperiencePercent(NamedRange):  # TODO!!! IMPLEMENT
    """What percentage of EXP enemies give you. This is a percent of their original EXP amount."""
    display_name = "Experience Percentage"
    range_start = 50
    range_end = 500
    default = 100
    special_range_names = {
        "none": 0,
        "half": 50,
        "normal": 100,
        "double": 200,
        "quadruple": 400
    }


# TODO- IMPLEMENT
class AddBrownChests(Choice):
    """Brown chest behavior.
       Normal; Brown chests are untouched
       Random Rewards; Shuffles the filler reward pool you get from brown chests
       Include; Converts all brown chests to regular chests."""
    display_name = "Brown Chest Shuffle"
    option_normal = 0
    option_random_rewards = 1
    option_include = 2
    default = 2


# TODO- Implement and get Casefold working
class StartingVillagers(OptionSet):
    """Specify which Villagers you want to start the game with."""
    display_name = "Starting Villagers"
    default = {"Jacob"}
    valid_keys = {
        "Nikolai",
        "Jacob",
        "Abram",
        "Laura",
        "Eugen",
        "Aeon",
        "Marcel",
        "George",
        "Serge",
        "Anna",
        "Monica",
        "Irina",
        "Daniela"}
    valid_keys_casefold = True


class RevealMap(DefaultOnToggle):
    """Start with the entire map visible."""
    display_name = "Reveal Map"


class RandomizeVillagers(Choice):
    """How Villagers are placed.
       Normal: Villagers are found in their normal locations.
       Shuffled: Villagers are shuffled amongst each other
       Anywhere: Villagers can be found anywhere."""
    display_name = "Randomize Villagers"
    option_normal = 0
    option_shuffled = 1
    option_anywhere = 2
    default = 0


@dataclass
class OoEOptions(PerGameCommonOptions):
    starting_glyph: StartingGlyph
    shuffle_dominus: ShuffleDominus
    start_with_lizard_tail: StartWithLizardTail
    start_with_glyph_union: StartWithGlyphUnion
    start_with_glyph_sleeve: StartWithGlyphSleeve
    add_brown_chests: AddBrownChests
    villagers_required: VillagersRequired
    starting_villagers: StartingVillagers
    reveal_map: RevealMap
    reveal_hidden_walls: RevealBreakableWalls
    experience_percent: ExperiencePercent
    randomize_villagers: RandomizeVillagers


ooe_option_groups = [
    OptionGroup("Goal Settings", [
        VillagersRequired
    ]),

    OptionGroup("Starting Items", [
        StartingGlyph,
        StartWithLizardTail,
        StartWithGlyphUnion,
        StartWithGlyphSleeve,
        StartingVillagers

    ]),

    OptionGroup("Location Options", [
        ShuffleDominus,
        AddBrownChests,
        RandomizeVillagers

    ]),

    OptionGroup("Enemy Settings", [
        ExperiencePercent,
        # APMultiplier,

    ]),

    OptionGroup("Quality of Life", [
        RevealMap,
        RevealBreakableWalls,
    ])
]
