from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, FreeText, Visibility)


class MaidensRequired(Range):
    """How many Maidens need to be saved to access the Palace of Winds"""
    display_name = "Required Maidens"
    range_start = 0
    range_end = 7
    default = 4

@dataclass
class FSAOptions(PerGameCommonOptions):
    maidens_required: MaidensRequired


fsa_option_groups = [
    OptionGroup("Goal Settings", [
        MaidensRequired,
    ])
]
