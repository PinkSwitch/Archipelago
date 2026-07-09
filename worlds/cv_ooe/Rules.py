from rule_builder.rules import HasAll, HasAny, Has, OptionFilter, CanReachLocation, HasGroupUnique
from rule_builder.field_resolvers import FromOption
from .Options import VillagersRequired, AddBrownChests


def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Ecclesia: Barlowe Fight"), HasAll("Dominus Hatred", "Dominus Anger", "Dominus Agony") & HasGroupUnique("Villagers", FromOption(VillagersRequired)))

    set_rule(world.get_location("Kalidus Channel: First Room Underwater"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Second Room Underwater"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Right Side Underwater Chest"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Right Exit Underwater Chest"), Has("Serpent Scale"))

    set_rule(world.get_location("Somnus Reef: Hidden Room"), Has("Lizard Tail"))

    set_rule(world.get_location("Minera Prison Island: Top Room"), HasAny("Ordinary Rock", "Volaticus"))
    set_rule(world.get_location("Minera Prison Island: Top Room Chest"), HasAny("Ordinary Rock", "Volaticus"))
    set_rule(world.get_location("Minera Prison Island: Right Vertical Hidden Item"), HasAny("Ordinary Rock", "Volaticus", "Magnes"))

    set_rule(world.get_location("Tymeo Mountains: Left Hill Alcove Chest"), Has("Lizard Tail"))
    set_rule(world.get_location("Tymeo Mountains: Left Hill Alcove Pickup"), Has("Lizard Tail"))
    set_rule(world.get_location("Tymeo Mountains: Lower Mountain Lower Paries Chest"), Has("Paries"))
    set_rule(world.get_location("Tymeo Mountains: Lower Mountain Upper Paries Chest"), Has("Paries"))
    set_rule(world.get_location("Tymeo Mountains: Wind Glyph"), Has("Magnes"))
    set_rule(world.get_location("Tymeo Mountains: Upper Hill Chest"), Has("Lizard Tail"))

    if world.options.add_brown_chests == AddBrownChests.option_include:
        set_rule(world.get_location("Kalidus Channel: Third Room Underwater"), Has("Serpent Scale"))
        set_rule(world.get_location("Tymeo Mountains: Right Hill Alcove Chest"), Has("Lizard Tail"))
        