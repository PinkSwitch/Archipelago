from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation
from .Regions import small_uppies, big_uppies, can_cast_spell, has_change_cube, medium_uppies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PoRWorld

def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Entrance: Drawbridge Upper Item"), big_uppies | HasAll("Acrobat Cube", "Call Cube", "Stone of Flight", "Puppet Master"))
    set_rule(world.get_location("Entrance: Above Metal Block Room"), big_uppies | (HasAll("Strength Glove", "Push Cube", "Call Cube") & (medium_uppies) | (HasAll("Acrobat Cube", "Puppet Master"))) | (HasAll("Puppet Master", "Stone of Flight", "Acrobat Cube", "Call Cube")))

    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Lower Alcove"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Upper Alcove"), medium_uppies | HasAny("Speed Up", "Puppet Master"))
    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Middle Alcove"), medium_uppies | HasAll("Speed Up", "Puppet Master"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Lower Alcove"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Middle Alcove"), medium_uppies | HasAll("Speed Up", "Puppet Master"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Upper Alcove"), medium_uppies | HasAny("Speed Up", "Puppet Master"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Top Left Item"), small_uppies | HasAny("Speed Up", "Puppet Master"))
    set_rule(world.get_location("Great Stairway: Connector Pipe Left"), can_cast_spell & HasAny("Owl Morph", "Toad Morph"))
    set_rule(world.get_location("Great Stairway: Connector Pipe Right"), can_cast_spell & HasAny("Owl Morph", "Toad Morph"))
    set_rule(world.get_location("Great Stairway: Right Loft"), small_uppies)
    set_rule(world.get_location("Great Stairway: Left Loft"), small_uppies)
    set_rule(world.get_location("Great Stairway: Left Loft Lower"), small_uppies)
    set_rule(world.get_location("Great Stairway: Central Nook"), medium_uppies)

    set_rule(world.get_location("Tower of Death: Secret Room"), medium_uppies | HasAll("Puppet Master", "Call Cube", "Acrobat Cube"))
    set_rule(world.get_location("Tower of Death: Elevator Room Lower"), big_uppies)
    set_rule(world.get_location("Tower of Death: Elevator Room Middle"), Has("Tower Elevator Active"))
    set_rule(world.get_location("Tower of Death: Elevator Room Top"), Has("Tower Elevator Active"))
    set_rule(world.get_location("Tower of Death: Above Motorcycles"), big_uppies | HasAll("Stone of Flight", "Call Cube", "Acrobat Cube"))
    



    set_rule(world.get_location("Dummy"), big_uppies | Has("Dummy"))
    