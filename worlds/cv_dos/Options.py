from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, DefaultOnToggle, Choice, TextChoice, OptionSet)
from .Items import soul_filler_table


class Goal(Choice):
    """The goal for your game.
       Throne Room: Get to the Throne Room and defeat Menace there.
       Abyss: Open the path to the Mine of Judgment, then defeat Menace in the Abyss.
       Abyss Plus: Defeat Aguni at the throne room, then open the path to the Mine of Judgment and defeat Menace in the Abyss."""
    display_name = "Goal"
    option_throne_room = 0
    option_abyss = 1
    option_abyss_plus = 2
    default = 0

class ReplaceMenaceWithSoma(Toggle):
    """Replaces Menace with Soma-Dracula"""
    display_name = "Soma Replaces Menace"

class RemoveMoneyGates(DefaultOnToggle):
    """Removes the gates that require you to own a specific amount of money."""
    display_name = "Remove Money Gates"

class DisableBossSeals(Toggle):
    """Removes the requirement to draw Magic Seals to defeat bosses."""
    display_name = "No Drawing Seals"

class EarlySeal1(Toggle):
    """Places Magic Seal 1 early in your own game to prevent getting stuck early."""
    display_name = "Early Seal 1"

class RevealMap(DefaultOnToggle):
    """Start with the entire map visible."""
    display_name = "Reveal Map"

class StartingWeapon(TextChoice):
    """The weapon you start the game with.
       Random Base: Start with a random base-level weapon
       Random Any: Start with any random weapon
       You can also choose to start with any specific weapon."""
    option_random_base = 0
    option_random_any = 1
    default = "Knife"

class FixLuck(DefaultOnToggle):
    """Fixes how the Luck stat is applied.
       With the fix applied, each point of luck gives +0.1% to any drop.
       Without the fix, each point of luck is +0.04% for souls, 0.25% for items."""
    display_name = "Fix Luck"

class RevealBreakableWalls(Toggle):
    """Automatically destroys/reveals all breakable walls"""
    display_name = "Reveal Hidden Walls"

class BoostSpeed(Toggle):
    """Increases Soma's base walking speed by 33%"""
    display_name = "Boost Speed"

class OneScreenMode(Toggle):
    """Allows the entire game to be played with only the bottom screen. Press Select to view the map."""
    display_name = "One-Screen Mode"

class SoulRandomizer(Choice):
    """Randomizes Enemy souls.
            Disabled: Enemy souls are unchanged.
            Shuffled: Enemy souls will be shuffled amongst each other. Souls that unlock things are unchanged.
            Soulsanity: Enemy soul drops can be anything, even important items or non-souls. You can change the expected soul rarity with Soulsanity level."""
    option_disabled = 0
    option_shuffled = 1
    option_soulsanity = 2
    default = 0

class SoulsanityLevel(Choice):
    """The maximum tier of soul rarity that have Locations on them.
       Rare souls always expect you to have the Soul Eater Ring."""
    option_simple = 0
    option_medium = 1
    option_rare = 2
    default = 0

class GuaranteedSouls(OptionSet):
    """The specified Souls will be guaranteed to have at least one copy in the item pool. Unspecified souls can still be randomly selected from the soul pool."""
    display_name = "Goal Triggers"
    default = {"Procel Soul", "Mud Demon Soul", "Black Panther Soul"}
    valid_keys = soul_filler_table

class RandomizeStartingWarp(Toggle):
    """Randomizes which Warp Room is unlocked by default."""
    display_name = "Random Starting Warp Room"

class OpenDrawbridge(Toggle):
    """If enabled, the drawbridge in Lost Village will start open instead of closed."""
    display_name = "Open Drawbridge"

class ShopRandomizer(Toggle):
    """Randomizes Hammer's shop items."""
    display_name = "Shop Randomizer"

@dataclass
class DoSOptions(PerGameCommonOptions):
    goal: Goal
    replace_menace_with_soma: ReplaceMenaceWithSoma
    remove_money_gates: RemoveMoneyGates
    disable_boss_seals: DisableBossSeals
    early_seal_1: EarlySeal1
    reveal_map: RevealMap
    starting_weapon: StartingWeapon
    reveal_hidden_walls: RevealBreakableWalls
    fix_luck: FixLuck
    boost_speed: BoostSpeed
    one_screen_mode: OneScreenMode
    soul_randomizer: SoulRandomizer
    soulsanity_level: SoulsanityLevel
    guaranteed_souls: GuaranteedSouls
    shuffle_starting_warp_room: RandomizeStartingWarp
    open_drawbridge: OpenDrawbridge
    shop_randomizer: ShopRandomizer

dos_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        ReplaceMenaceWithSoma

    ]),

    OptionGroup("Soul Settings", [
        SoulRandomizer,
        SoulsanityLevel,
        GuaranteedSouls

    ]),

    OptionGroup("Item Options", [
        StartingWeapon,
        EarlySeal1,
        ShopRandomizer

    ]),

    OptionGroup("World Settings", [
        RandomizeStartingWarp,
        OpenDrawbridge

    ]),

    OptionGroup("Quality of Life", [
        RemoveMoneyGates,
        DisableBossSeals,
        RevealMap,
        RevealBreakableWalls,
        FixLuck,
        BoostSpeed,
        OneScreenMode
    ])
]
