from dataclasses import dataclass
from Options import (Toggle, PerGameCommonOptions, OptionGroup, Range, StartInventoryPool)


class RandomTunic(Toggle):
    """Randomize the color of Simon's tunic."""
    display_name = "Randomize Tunic Color"


class ReqRelics(Range):
    """How many of Dracula's parts you need to find in order to revive Dracula."""
    display_name = "Dracula Parts Required"
    range_start = 0
    range_end = 5
    default = 5


class ReqOrbs(Range):
    """How many Orbs you're required to break at the end of Mansions to revive Dracula."""
    display_name = "Orbs Required"
    range_start = 0
    range_end = 5
    default = 0


class StartingHearts(Range):
    """How many Hearts you start the game with."""
    display_name = "Starting Hearts"
    range_start = 0
    range_end = 9999
    default = 50


class HeartMultiplier(Range):
    """Multiplier for the amount of Hearts you get from pickups"""
    display_name = "Heart Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class PoisonRing(Toggle):
    """If enabled, Dracula's Ring will protect you from poison water when equipped."""
    display_name = "Poisonproof Ring"


class InclusiveWhtCrystal(Toggle):
    """If enabled, all moving platforms will require the White Crystal to be visible."""
    display_name = "Inclusive White Crystal"


@dataclass
class CV2Options(PerGameCommonOptions):
    dracula_parts_required: ReqRelics
    orbs_required: ReqOrbs
    heart_multiplier: HeartMultiplier
    starting_hearts: StartingHearts
    poison_proof_ring: PoisonRing
    inclusive_white_crystal: InclusiveWhtCrystal
    randomize_tunic_color: RandomTunic
    start_inventory_from_pool: StartInventoryPool


cv2_option_groups = [
    OptionGroup("Goal Settings", [
        ReqRelics,
        ReqOrbs
    ]),

    OptionGroup("World Settings", [
        PoisonRing,
        InclusiveWhtCrystal
    ]),

    OptionGroup("Quality of Life", [
        HeartMultiplier,
        StartingHearts

    ]),

    OptionGroup("Aesthetic Settings", [
        RandomTunic
    ])
]
