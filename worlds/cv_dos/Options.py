from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, DefaultOnToggle, Choice, TextChoice)


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
        Shuffled: Shuffles which soul enemies drop.
        Soulsanity Simple:"""
    option_normal = 0
    option_shuffled = 1
    option_soulsanity = 2
    default = 0

class SoulSanityLevel(Choice):
    """Randomizes Enemy souls.
        Shuffled: Shuffles which soul enemies drop.
        Soulsanity Simple:"""
    option_normal = 0
    option_shuffled = 1
    option_soulsanity = 2
    default = 0

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
    soul_randomizer: Soulsanity
    one_screen_mode: OneScreenMode

dos_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        ReplaceMenaceWithSoma

    ]),

    OptionGroup("Soul Randomization", [
        Soulsanity

    ]),

    OptionGroup("Item Options", [
        StartingWeapon,
        EarlySeal1

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
