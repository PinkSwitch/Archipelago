from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation
from rule_builder.field_resolvers import FromOption
from .Regions import small_uppies, big_uppies, can_cast_spell, medium_uppies, strongies, is_smol
from .Options import NestofEvil, BraunerPortraits, Goal
from . modules.quest_data import set_quest_rules


def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Entrance: Drawbridge Upper Item"), big_uppies | HasAll("Acrobat Cube", "Call Cube", "Stone of Flight", "Puppet Master"))
    set_rule(world.get_location("Entrance: Above Metal Block Room"), big_uppies |
                                                                    HasAll("Stone of Flight", "Puppet Master") |
                                                                    strongies & ((Has("Stone of Flight")) | HasAll("Acrobat Cube", "Call Cube")))
                                                                    
    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Lower Alcove"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Upper Alcove"), medium_uppies | Has("Puppet Master") | (can_cast_spell & Has("Speed Up")))
    set_rule(world.get_location("Great Stairway: Lower Grand Staircase Middle Alcove"), medium_uppies | HasAll("Speed Up", "Puppet Master", "Call Cube"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Lower Alcove"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Middle Alcove"), medium_uppies | HasAll("Speed Up", "Puppet Master", "Call Cube"))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Upper Alcove"), medium_uppies | Has("Puppet Master") | (can_cast_spell & Has("Speed Up")))
    set_rule(world.get_location("Great Stairway: Upper Grand Staircase Top Left Item"), small_uppies | Has("Puppet Master") | (can_cast_spell & Has("Speed Up")))
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

    set_rule(world.get_location("City of Haze: Cart Secret Left"), big_uppies)
    set_rule(world.get_location("City of Haze: Cart Secret Right"), big_uppies)
    set_rule(world.get_location("City of Haze: Cart Secret Right"), big_uppies)
    set_rule(world.get_location("City of Haze: Right Dance Hall Item"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("City of Haze: Tunnel Room Left"), (can_cast_spell & HasAny("Toad Morph", "Owl Morph")) | Has("Puppet Master"))
    set_rule(world.get_location("City of Haze: Left Dance Hall Left Item"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("City of Haze: Left Dance Hall Right Item"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("City of Haze: Central Hallway Lower"), is_smol)

    set_rule(world.get_location("13th Street: Train Room Secret Left"), big_uppies)
    set_rule(world.get_location("13th Street: Train Room Secret Right"), big_uppies)
    set_rule(world.get_location("13th Street: Right Dance Hall Top Left"), small_uppies)
    set_rule(world.get_location("13th Street: Right Dance Hall Top Right"), small_uppies)
    set_rule(world.get_location("13th Street: Many Nyxes Room"), (medium_uppies | HasAll("Acrobat Cube", "Call Cube", "Puppet Master")) & (HasAll("Puppet Master", "Lizard Tail") | (can_cast_spell & HasAny("Toad Morph", "Owl Morph"))))

    set_rule(world.get_location("Sandy Grave: Behind Bricks"), big_uppies)
    set_rule(world.get_location("Sandy Grave: Boulder Room Tunnel"), can_cast_spell & HasAny("Toad Morph", "Owl Morph"))
    set_rule(world.get_location("Sandy Grave: Boulder Room Corner Alcove"), big_uppies)
    set_rule(world.get_location("Sandy Grave: Lonely Mimic Alcove"), medium_uppies | HasAll("Acrobat Cube", "Call Cube", "Puppet Master"))
    set_rule(world.get_location("Sandy Grave: Lower Big Underground Room Top"), medium_uppies)
    set_rule(world.get_location("Sandy Grave: Upper Big Underground Top Left"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Sandy Grave: Upper Big Underground Top Right"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Sandy Grave: Eastmost Item"), small_uppies)
    set_rule(world.get_location("Sandy Grave: Pyramid East 1F"), big_uppies | HasAll("Stone of Flight", "Acrobat Cube", "Call Cube"))

    set_rule(world.get_location("Forgotten City: Pyramid East 5F"), small_uppies | Has("Puppet Master"))
    set_rule(world.get_location("Forgotten City: Pyramid 1F Bricks"), big_uppies)
    set_rule(world.get_location("Forgotten City: Lower Boulder Room Upper Alcove"), big_uppies)
    set_rule(world.get_location("Forgotten City: Lower Boulder Room Tunnel Alcove"), can_cast_spell & HasAny("Toad Morph", "Owl Morph"))
    set_rule(world.get_location("Forgotten City: Lower Underground Square Upper Item"), medium_uppies | HasAll("Call Cube", "Acrobat Cube", "Puppet Master"))
    set_rule(world.get_location("Forgotten City: Pyramid East 1F"), big_uppies | HasAll("Call Cube", "Acrobat Cube", "Stone of Flight"))
    set_rule(world.get_location("Forgotten City: Pyramid East 1F"), big_uppies | HasAll("Call Cube", "Acrobat Cube", "Stone of Flight"))
    set_rule(world.get_location("Forgotten City: Big Shaft Room Left"), big_uppies)
    set_rule(world.get_location("Forgotten City: Big Shaft Room Right"), big_uppies)
    set_rule(world.get_location("Forgotten City: Pyramid East 3F"), medium_uppies | HasAll("Call Cube", "Acrobat Cube", "Puppet Master") | (can_cast_spell & HasAll("Speed Up", "Puppet Master")))

    set_rule(world.get_location("Nation of Fools: Bottom Left Medium Square On Wall"), big_uppies | HasAll("Call Cube", "Acrobat Cube", "Stone of Flight") | HasAll("Stone of Flight", "Puppet Master"))
    set_rule(world.get_location("Nation of Fools: Crevice Item"), Has("Puppet Master") | (can_cast_spell & HasAny("Toad Morph", "Owl Morph")))

    set_rule(world.get_location("Burnt Paradise: Right Upper Big Corner On Wall"), big_uppies | HasAll("Call Cube", "Acrobat Cube", "Stone of Flight") | HasAll("Stone of Flight", "Puppet Master"))
    set_rule(world.get_location("Burnt Paradise: Lower Vertical Hall"), Has("Puppet Master") | (can_cast_spell & HasAny("Toad Morph", "Owl Morph")))

    set_rule(world.get_location("Forest of Doom: Secret Cave Room"), big_uppies)

    set_rule(world.get_location("Lost Gallery: Studio Portrait Fight"),
             Has("Portrait Clear", FromOption(BraunerPortraits)) &
             CanReachLocation("Nest of Evil: Doppelganger Reward", options=[OptionFilter(NestofEvil, NestofEvil.option_required), OptionFilter(Goal, True)], filtered_resolution=True))

    if world.options.goal:
        set_rule(world.get_location("The Throne Room: Great Stairs Under Stairs"), medium_uppies | HasAll("Acrobat Cube", "Call Cube", "Puppet Master"))
        set_rule(world.get_location("The Throne Room: Great Stairs Hidden"), big_uppies)
        set_rule(world.get_location("The Throne Room: Above Throne Left"), big_uppies)
        set_rule(world.get_location("The Throne Room: Above Throne Right"), big_uppies)
        set_rule(world.get_location("The Throne Room: Great Stairs Center"), big_uppies)
        set_rule(world.get_location("The Throne Room: Great Stairs Left"), big_uppies)

    set_quest_rules(world)