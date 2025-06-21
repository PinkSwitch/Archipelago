from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, FreeText, Visibility, Choice)


class MaidensRequired(Range):
    """How many Maidens need to be saved to access the Palace of Winds"""
    display_name = "Required Maidens"
    range_start = 0
    range_end = 7
    default = 4

class GemsRequired(Range):
    """How many Force Gems are required for the Sword Upgrade check. Gems are counted globally, across all levels"""
    display_name = "Force Gems for Sword"
    range_start = 1
    range_end = 9999
    default = 5000

class ForceGemItem(Toggle):
    """If enabled, reaching the Force Gem milestone will grant a random item. Otherwise, it will grant your Sword Upgrade."""
    display_name = "Shuffle Gem Milestone Item"

@dataclass
class FSAOptions(PerGameCommonOptions):
    maidens_required: MaidensRequired
    force_gems_for_sword_upgrade: GemsRequired
    shuffle_gem_milestone_item: ForceGemItem



fsa_option_groups = [
    OptionGroup("Goal Settings", [
        MaidensRequired,
    ]),

    OptionGroup("Gem/Sword Settings", [
        GemsRequired,
        ForceGemItem
    ])
]
