from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, FreeText, Visibility, DefaultOnToggle, Choice)


class TrophiesRequired(Range):
    """How many Trophies need to be found to complete the seed."""
    display_name = "Trophies Required"
    range_start = 1
    range_end = 293
    default = 100

class TrophiesExtra(Range):
    """How many extra Trophies will be in the item pool. Total trophies cannot exceed 293."""
    display_name = "Extra Trophies"
    range_start = 0
    range_end = 293
    default = 50

class BonusSanity(Toggle):
    """Enables Bonuses as checks. Which bonuses are enabled can be tweaked."""
    display_name = "Bonus-sanity"

class EventSanity(Toggle):
    """Enables all Event match clears as checks. If this is disabled, events
        with major unlocks will still give checks."""
    display_name = "Eventsanity"

class GoalGigaBowser(DefaultOnToggle):
    """If enabled, you will need to defeat Giga Bowser in Adventure Mode and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Giga Bowser Goal"

class GoalCrazyHand(Toggle):
    """If enabled, you will need to defeat Crazy Hand in Classic Mode and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Crazy Hand Goal"

class GoalEvent51(Toggle):
    """If enabled, you will need to complete Event 51 and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "Event 51 Goal"

class GoalAllEvents(Toggle):
    """If enabled, you will need to complete every event besides 51 and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "All Events Goal"

class RarePokemonChecks(Toggle):
    """Enables 2 checks for seeing Mew and Celebi as well as 2 related Bonus checks."""
    display_name = "Pokemon Bonus Checks"

class HardBonuses(Toggle):
    """Enables a few specific difficult Bonus checks. Does nothing with Bonus-sanity off, such as All Variations or bonuses which are easier with 2 human players."""
    display_name = "Hard Bonus Checks"

class ExtremeBonuses(Toggle):
    """Enables a few very difficult Bonus checks, such as Hammer Throw or No-Damage Clear. Does nothing with Bonus-sanity off."""
    display_name = "Extreme Bonus Checks"

class DiskunTrophyCheck(Toggle):
    """Enables a check on the Diskun trophy, which requires getting all 249 Bonuses."""
    display_name = "Diskun Check"

class MewtwoUnlockCheck(Toggle):
    """Enables a check on unlocking Mewtwo, which requires 1 total hour of VS play."""
    display_name = "Mewtwo Check"

class GoalTargets(Toggle):
    """If enabled, you will need to complete Target Test with every character and collect your required trophies to win.
       This option can stack with other Goals."""
    display_name = "All Targets Goal"

class AnnoyingMultiMan(Toggle):
    """Enables checks on 15-Minute and Cruel Melee"""
    display_name = "Annoying Multi-Man Checks"

class VsCountChecks(Toggle):
    """Enables checks on VS match counts. WARNING. These are really high and will likely take a long time."""
    display_name = "VS Count Checks"

class LotteryPool(Choice):
    """Changes how the Lottery Trophy pool works.
       Vanilla: The lottery pool expands when meeting the vanilla requirement. The 200 VS trophies are unlocked with 5 matches instead.
       Progressive: The lottery pool will increase every time you get a Progressive Lottery Pool item.
       Non-progressive: The lottery pool has specific upgrade items"""
    display_name = "Lottery Pool Mode"
    option_vanilla = 0
    option_progressive = 1
    option_non_progressive = 2
    default = 1

class SoloCSmash(DefaultOnToggle):
    """Enables the use of Smash Attacks with the C-Stick during 1-Player modes."""
    display_name = "1-P C Smash"

class TargetSanity(Toggle):
    """Enables a check for every individual character's Target Test being cleared."""
    display_name = "Pokemon Bonus Checks"

class LongTargetChecks(Toggle):
    """Enables Target Test checks locked behind most or all characters."""
    display_name = "Long Target Test Checks"

@dataclass
class SSBMOptions(PerGameCommonOptions):
    trophies_required: TrophiesRequired
    extra_trophies: TrophiesExtra
    bonus_checks: BonusSanity
    target_checks: TargetSanity
    enable_rare_pokemon_checks: RarePokemonChecks
    enable_hard_bonuses: HardBonuses
    enable_extreme_bonuses: ExtremeBonuses
    enable_annoying_multiman_checks: AnnoyingMultiMan
    diskun_trophy_check: DiskunTrophyCheck
    mewtwo_unlock_check: MewtwoUnlockCheck
    vs_count_checks: VsCountChecks
    long_targettest_checks: LongTargetChecks
    lottery_pool_mode: LotteryPool
    event_checks: EventSanity
    goal_giga_bowser: GoalGigaBowser
    goal_crazy_hand: GoalCrazyHand
    goal_event_51: GoalEvent51
    goal_all_events: GoalAllEvents
    goal_all_targets: GoalTargets
    solo_cstick_smash: SoloCSmash


ssbm_option_groups = [
    OptionGroup("Trophy Settings", [
        TrophiesRequired,
        TrophiesExtra,
    ]),

    OptionGroup("Check Settings", [
        BonusSanity,
        EventSanity,
        TargetSanity
    ]),

    OptionGroup("Annoying Checks", [
        HardBonuses,
        RarePokemonChecks,
        ExtremeBonuses,
        AnnoyingMultiMan,
        VsCountChecks,
        DiskunTrophyCheck,
        MewtwoUnlockCheck,
        LongTargetChecks
    ]),

    OptionGroup("Goal Settings", [
        GoalGigaBowser,
        GoalCrazyHand,
        GoalEvent51,
        GoalAllEvents,
        GoalTargets
    ]),

    OptionGroup("QOL Settings", [
        SoloCSmash
    ]),
]
