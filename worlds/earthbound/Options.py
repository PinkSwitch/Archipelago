from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions, StartInventoryPool


class GiygasRequired(DefaultOnToggle):
    """If enabled, your goal will be to defeat Giygas at the Cave of the Past.
       If disabled, your goal will either complete automatically upon completing
       enough Sanctuaries, or completing Magicant if it is required."""
    display_name = "Starting Lives"

class SanctuariesRequired(Range):
    """How many of the eight "Your Sanctuary" locations are required to be cleared."""
    display_name = "Required Sanctuaries"
    range_start = 1
    range_end = 8
    default = 4

class SanctuaryAltGoal(Toggle):
    """If enabled, you will be able to win by completing 2 more Sanctuaries than are required.
       Does nothing if 7 or more Sanctuaries are required, or if Magicant and Giygas are not required."""
    display_name = "Sanctuary Alternate Goal"

class MagicantMode(Choice):
    """PSI Location: You will be able to find a Magicant teleport item. Ness's Nightmare contains a PSI location, and no stat boost.
       Required: You will unlock the Magicant Teleport upon reaching your Sanctuary goal. If Giygas is required, beating Ness's Nightmare will unlock the Cave of the Past. Otherwise, Ness's Nightmare will finish your game.
       Alternate Goal: You will unlock the Magicant Teleport upon reaching one more Sanctuary than required. Beating Ness's Nightmare will finish your game. Does nothing if Giygas is not required, or if 8 Sanctuaries are required."""
    display_name = "Magicant Mode"
    option_psi_location = 0
    option_required = 1
    option_alternate_goal = 2
    default = 0
    

class ShortenPrayers(DefaultOnToggle):
    """If enabled, the Prayer cutscenes while fighting Giygas will be skipped, excluding the final one."""
    display_name = "Skip Prayer Sequences"

class RandomStartLocation(Toggle):
    """If disabled, you will always start at Ness's house with no teleports unlocked.
       If enabled, you will start at a random teleport destination with one teleport unlocked.
       Additionally, you will need to fight Captain Strong to access the north part of Onett if this is enabled."""
    display_name = "Random Starting Location"

class PSIShuffle(Choice):
    """PSI Locations: Teleports and Starstorm will be shuffled amongst the PSI locations. A few redundant Teleports may not be available.
       Anywhere: Teleports and Starstorm will be placed anywhere in the multiworld, and PSI locations will have regular checks.
       See the Game Page for more information on PSI Locations."""
    display_name = "PSI Shuffle"
    option_psi_locations = 0
    option_anywhere = 1
    default = 0

class CharacterShuffle(Choice):
    """Character Locations: Characters will be shuffled amongst Character Locations. Extra locations will have Flying Man, a Teddy Bear, or a Super Plush Bear.
       Anywhere: Characters can be found anywhere in the multiworld, and character locations will have regular checks.
       See the Game Page for more information on Character Locations."""
    display_name = "Character Shuffle"
    option_psi_locations = 0
    option_anywhere = 1
    default = 0

class CommonWeight(Range):
    """How many of the eight "Your Sanctuary" locations are required to be cleared."""
    display_name = "Common Filler Weight"
    range_start = 1
    range_end = 100
    default = 80

class UncommonWeight(Range):
    """How many of the eight "Your Sanctuary" locations are required to be cleared."""
    display_name = "Uncommon Filler Weight"
    range_start = 1
    range_end = 100
    default = 30

class RareWeight(Range):
    """How many of the eight "Your Sanctuary" locations are required to be cleared."""
    display_name = "Rare Filler Weight"
    range_start = 0
    range_end = 100
    default = 5

@dataclass
class EBOptions(PerGameCommonOptions):
    giygas_required: GiygasRequired
    sanctuaries_required: SanctuariesRequired
    skip_prayer_sequences: ShortenPrayers
    random_start_location: RandomStartLocation
    alternate_sanctuary_goal: SanctuaryAltGoal
    magicant_mode: MagicantMode
    psi_shuffle: PSIShuffle# Better name?
    character_shuffle: CharacterShuffle
    common_filler_weight: CommonWeight
    uncommon_filler_weight: UncommonWeight
    rare_filler_weight: RareWeight
    #RepairJeffItems
    #PSI Checks
    #Character Checks
    #EXP Multiplier
    start_inventory_from_pool: StartInventoryPool
    #death_link: DeathLink