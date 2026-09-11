class AllowBossSwaps(Toggle):
    """
    Allow bosses to be included in enemy randomization (not recommended for safety).
    """

    display_name = "Allow Boss Swaps"


class PreserveResourceIntensive(Toggle):
    """
    Protect resource-intensive enemies from being swapped to avoid crashes.
    """

    display_name = "Preserve Resource-Intensive"
    default = True


class EnemyRandomizerMode(Choice):
    """
    Mode for enemy randomizer.
    """

    display_name = "Enemy Randomizer Mode"
    option_full_swap = 0
    option_spawn_swap = 1
    default = 0


class EnemyRandomizerDebugSubset(Range):
    """
    If >0, only swap this many non-protected enemies (useful for debugging).
    """

    display_name = "Enemy Randomizer Debug Subset"
    range_start = 0
    range_end = 500
    default = 5
