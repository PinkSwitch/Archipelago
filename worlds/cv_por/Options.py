from dataclasses import dataclass
from Options import PerGameCommonOptions, Choice, DefaultOnToggle, Range, NamedRange, Toggle, ExcludeLocations, OptionGroup

class Goal(Choice):   # TODO!!!! IMPLEMENT
    """The goal for your game.
       Brauner: Defeat Brauner in the studio portrait.
       Dracula: Defeat Dracula in the throne room."""
    display_name = "Goal"
    option_brauner = 0
    option_dracula = 1
    default = 0

class RevealMap(DefaultOnToggle):  #  TODO!!! IMPLEMENT
    """Start with the entire map visible."""
    display_name = "Reveal Map"

class RevealBreakableWalls(Toggle):   # TODO!!! IMPLEMENT
    """Automatically reveals all breakable walls/objects."""
    display_name = "Reveal Hidden Walls"

class NestofEvil(Choice):   # TODO!!! IMPLEMENT
    """The state of the Nest of Evil.
         Vanilla: Nest of Evil has its original rewards, the two tome pages and Greatest Five.
         Randomized: The three items in the Nest of Evil are random, and added to the item pool.
         Required: You are required to clear the Nest of Evil before you can access your final boss.
         Removed: The three items are added to the item pool, and the Nest of Evil is inaccessible."""
    display_name = "Nest of Evil State"

class BraunerRequired(DefaultOnToggle):  #  TODO!!! IMPLEMENT
    """If enabled, you will be required to fight Brauner before you can access the Throne Room,
       Of course, this won't do anything if the goal is set to Brauner."""
    display_name = "Brauner Required"

class NestPortraits(Range):  # TODO!!! Implement
    """How many Portraits are required to be cleared to access the underground passage
       at the castle entrance."""
    display_name = "Passage Portraits"
    range_start = 0
    range_end = 8
    default = 8

class BraunerPortraits(Range):  #TODO!!! IMPLEMENT
    """How many of ANY portraits are required to be cleared to access Brauner's portrait."""
    display_name = "Brauner Portraits"
    range_start = 0
    range_end = 8
    default = 4

class DraculaPortraits(Range):  # TODO!!! IMPLEMENT
    """How many portraits are required to be cleared to access the Throne Room."""
    display_name = "Throne Portraits"
    range_start = 0
    range_end = 8
    default = 0

class ExperiencePercent(NamedRange):  # TODO!!! IMPLEMENT
    """What percentage of EXP enemies give you. This is a percent of their original EXP amount."""
    display_name = "Experience Percentage"
    range_start = 0
    range_end = 500
    default = 100
    special_range_names = {
        "none": 0,
        "half": 50,
        "normal": 100,
        "double": 200,
        "quadruple": 400
    }

class ShuffleWhip(Toggle):  # TODO!!! Implement
    """If enabled, the True Vampire Killer will be added to the item pool,
       and the Whip's Memory fight will grant you a random item.
       Otherwise, it will be at its normal location."""
    display_name = "Shuffle True Vampire Killer"

class PoRExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"Dark Chasm of Old"})

@dataclass
class PoROptions(PerGameCommonOptions):
    goal: Goal
    brauner_portraits: BraunerPortraits
    dracula_portraits: DraculaPortraits
    nest_portraits: NestPortraits
    brauner_required: BraunerRequired
    nest_of_evil_state: NestofEvil
    shuffle_whip: ShuffleWhip
    reveal_map: RevealMap
    reveal_hidden_walls: RevealBreakableWalls
    experience_percentage: ExperiencePercent
    exclude_locations: PoRExcludeLocations
    
por_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        BraunerPortraits,
        DraculaPortraits,
        BraunerRequired,

    ]),

    OptionGroup("Nest of Evil Options", [
        NestofEvil,
        NestPortraits

    ]),

    OptionGroup("Item Options", [
        ShuffleWhip

    ]),

    OptionGroup("Enemy Settings", [
        ExperiencePercent

    ]),

    OptionGroup("Quality of Life", [
        RevealMap,
        RevealBreakableWalls
    ])
]