from dataclasses import dataclass
from Options import PerGameCommonOptions, Choice, DefaultOnToggle, Range, NamedRange, Toggle, ExcludeLocations, OptionGroup, StartInventoryPool, OptionSet
from .modules.quest_data import quest_data


class Goal(Choice):
    """The goal for your game.
       Brauner: Defeat Brauner in the studio portrait.
       Dracula: Defeat Dracula in the throne room."""
    display_name = "Goal"
    option_brauner = 0
    option_dracula = 1
    default = 1


class RevealMap(DefaultOnToggle):
    """Start with the entire map visible."""
    display_name = "Reveal Map"


class RevealBreakableWalls(Toggle):
    """Automatically reveals all breakable walls/objects."""
    display_name = "Reveal Hidden Walls"


class NestofEvil(Choice):
    """The state of the Nest of Evil.
         Vanilla: Nest of Evil has its original rewards, the two tome pages and Greatest Five.
         Randomized: The three items in the Nest of Evil are random, and added to the item pool.
         Required: You are required to clear the Nest of Evil before you can access your final boss.
         Removed: The three items are added to the item pool, and the Nest of Evil is inaccessible."""
    display_name = "Nest of Evil State"
    option_vanilla = 0
    option_randomized = 1
    option_required = 2
    option_removed = 3
    default = 0


class BraunerRequired(DefaultOnToggle):
    """If enabled, you will be required to fight Brauner before you can access the Throne Room,
       Of course, this won't do anything if the goal is set to Brauner."""
    display_name = "Brauner Required"


class NestPortraits(Range):
    """How many Portraits are required to be cleared to access the underground passage
       at the castle entrance."""
    display_name = "Passage Portraits"
    range_start = 0
    range_end = 8
    default = 8


class BraunerPortraits(Range):
    """How many of ANY portraits are required to be cleared to access Brauner's portrait."""
    display_name = "Brauner Portraits"
    range_start = 0
    range_end = 8
    default = 4


class DraculaPortraits(Range):
    """How many portraits are required to be cleared to access the Throne Room."""
    display_name = "Throne Portraits"
    range_start = 0
    range_end = 8
    default = 0


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


class ShuffleWhip(Toggle):
    """If enabled, the True Vampire Killer will be added to the item pool,
       and the Whip's Memory fight will grant you a random item.
       Otherwise, it will be at its normal location."""
    display_name = "Shuffle True Vampire Killer"


class PoRExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({"The Throne Room: Above Throne Left", "The Throne Room: Above Throne Right", "The Throne Room: Great Stairs Left",
                         "The Throne Room: Great Stairs Center", "The Throne Room: Great Stairs Under Stairs", "The Throne Room: Great Stairs Hidden"})


class StartWithChangeCube(Toggle):
    """If enabled, you'll start with the Change Cube by default"""
    display_name = "Start with Change Cube"


class AddExtraItems(Toggle):
    """If enabled, some items and spells that are otherwise only obtainable
       in other modes will be added to the item pool, such as Puppet Master."""
    display_name = "Add Extra Items"


class ExcludeOwlMorph(Toggle):
    """If enabled, Owl Morph will not be added to the item pool."""
    display_name = "Exclude Owl Morph"


class StrongerGlove(Toggle):
    """If enabled, the Strength Glove will be buffed and able to push stationary heavy objects on its own."""
    display_name = "Stronger Glove"


class OneScreenMode(Toggle):
    """Allows the entire game to be played with only the bottom screen. Press Select to view the map."""
    display_name = "One-Screen Mode"


class PortraitShuffle(Choice):
    """Shuffles which areas the Portraits lead you to."""
    display_name = "Portrait Shuffle"
    option_normal = 0
    option_shuffle = 1
    option_add_nest_of_evil = 2
    default = 0

class SPMultiplier(Range):
    """Multiplier for the amount of SP given by enemies."""
    display_name = "SP Multiplier"
    range_start = 1
    range_end = 100
    default = 1

class UnlockAllQuests(Toggle):
    """If enabled, all Quests will be unlocked by default."""
    display_name = "Unlock All Quests"

quest_keys = set()
for quest in quest_data:
    if quest not in ["Quest: Preparations", "Quest: The Nest of Evil"]:
        quest_keys.add(quest)
        quest_keys.add(quest.split(": ")[1])  # Truncate it to just the quest name
quest_keys |= {"All", "Requires Item", "Defeat Enemies", "Mastery", "Simple", "Grindy"}

class ActiveQuests(OptionSet):
    """Specify which Quests have random items. 'Preparations' is always included, regardless of settings. Nest of Evil is never included.
       You can type any quest name, as well as the following shortcuts:
       Requires Item: Any Quest which requires you to turn in an item or set of items (except for Almighty and Great Sage)
       Defeat Enemies: Any Quest which requires you to defeat specific enemies.
       Mastery: Any Quest which requires you to Master a subweapon.
       Simple: Any Quest with no specific requirement other than reaching an area or changing your status.
       Grindy: Any Quest with a high grinding requirement. (Includes the Mastery quests.)
       All: Enables ALL quests
       """
    display_name = "Randomized Quests"
    default = {}
    valid_keys = frozenset(key.casefold() for key in quest_keys)
    valid_keys_casefold = True

class ExcludedQuests(OptionSet):
    """Specify Excluded randomized quests from the above option. Excluded Quests will still be randomized, but will always be your own junk items.
       The same shortcuts from the above option apply."""
    display_name = "Excluded Quests"
    default = {"A Rank Hunter", "S Rank Hunter", "Hands of the Clock", "The Hundred Tasks", "Master the Holy Power", "Almighty", "The Great Sage"}
    valid_keys = frozenset(key.casefold() for key in quest_keys)
    valid_keys_casefold = True


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
    start_with_change_cube: StartWithChangeCube
    add_extra_items: AddExtraItems
    exclude_owl_morph: ExcludeOwlMorph
    stronger_glove: StrongerGlove
    one_screen_mode: OneScreenMode
    portrait_shuffle: PortraitShuffle
    sp_multiplier: SPMultiplier
    unlock_all_quests: UnlockAllQuests
    randomized_quests: ActiveQuests
    excluded_quests: ExcludedQuests
    start_inventory_from_pool: StartInventoryPool


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
        ShuffleWhip,
        StartWithChangeCube,
        AddExtraItems,
        ExcludeOwlMorph,
        StrongerGlove

    ]),

    OptionGroup("Quest Options", [
        UnlockAllQuests,
        ActiveQuests,
        ExcludedQuests

    ]),

    OptionGroup("Area Randomization", [
        PortraitShuffle

    ]),

    OptionGroup("Enemy Settings", [
        ExperiencePercent,
        SPMultiplier

    ]),

    OptionGroup("Quality of Life", [
        RevealMap,
        RevealBreakableWalls,
        OneScreenMode
    ])
]
