from worlds.generic.Rules import set_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import FSAdventuresWorld


def set_location_rules(world: "FSAdventuresWorld") -> None:
    player = world.player

    # set_rule(world.multiworld.get_location("Onett - Traveling Entertainer", player), lambda state: state.has("Key to the Shack", player))
