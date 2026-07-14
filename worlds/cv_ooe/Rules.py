from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation, HasGroupUnique
from rule_builder.field_resolvers import FromOption
from .Options import VillagersRequired, AddBrownChests


def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Ecclesia: Barlowe Fight"), HasAll("Dominus Hatred", "Dominus Anger", "Dominus Agony") & HasGroupUnique("Villagers", count=FromOption(VillagersRequired)))

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

    set_rule(world.get_location("Tristis Pass: Frozen Waterfall Glyph"), Has("Magnes"))
    set_rule(world.get_location("Tristis Pass: Second Hill Lowest Chest"), Has("Lizard Tail"))

    set_rule(world.get_location("Mystery Manor: Dark Room Chest"), Has("Arma Machina"))

    set_rule(world.get_location("Misty Forest Road: Right Big Room Ledge"), HasAny("Volaticus", "Rapidus Fio", "Magnes"))
    set_rule(world.get_location("Misty Forest Road: Ledge Item"), HasAny("Volaticus", "Rapidus Fio"))
    set_rule(world.get_location("Misty Forest Road: Paries Room Hidden Item"), Has("Paries"))
    set_rule(world.get_location("Misty Forest Road: Paries Room Pickup"), Has("Paries"))
    set_rule(world.get_location("Misty Forest Road: Paries Room Chest"), Has("Paries"))

    set_rule(world.get_location("Oblivion Ridge: Pre-Boss Ledge"), HasAny("Volaticus", "Rapidus Fio"))
    set_rule(world.get_location("Oblivion Ridge: Post-Boss Ledge Item"), HasAny("Volaticus", "Rapidus Fio"))

    set_rule(world.get_location("Skeleton Cave: First Room"), HasAny("Volaticus", "Ordinary Rock", "Rapidus Fio"))
    set_rule(world.get_location("Skeleton Cave: Dead End Upper"), HasAny("Volaticus", "Ordinary Rock", "Rapidus Fio"))

    set_rule(world.get_location("Monastery: Big Room Ledge"), HasAny("Volaticus", "Ordinary Rock", "Rapidus Fio"))
    set_rule(world.get_location("Monastery: Big Room Under Shelf"), Has("Lizard Tail"))
    set_rule(world.get_location("Monastery: Blocks Glyph"), (HasAny("Secare", "Vol Secare", "Melio Secare") & Has("Glyph Union")) | HasAny("Redire", "Globus", "Melio Ascia", "Umbra"))
    set_rule(world.get_location("Monastery: Blocks Reward Chest"), (CanReachLocation("Monastery: Blocks Glyph")) & HasAny("Redire", "Melio Ascia", "Nitesco", "Luminatio", "Globus", "Acerbatus", "Umbra"))

    set_rule(world.get_location("Mechanical Tower: Generator Puzzle"), HasAny("Volaticus", "Magnes", "Rapidus Fio", "Arma Machina") & HasAll("Fulgur", "Vol Fulgur"))

    set_rule(world.get_location("Final Approach: Treasure Room Second From Right"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Treasure Room Far Right"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Treasure Room Far Left"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Treasure Room Second From Left"), Has("Volaticus"))

    set_rule(world.get_location("Final Approach: Final Stash Far Right"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Final Stash Second From Left"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Final Stash Second From Right"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Final Stash Far Left"), Has("Volaticus"))
    set_rule(world.get_location("Final Approach: Throne Right Chest"), Has("Paries"))
    set_rule(world.get_location("Final Approach: Throne Left Chest"), Has("Paries"))

    set_rule(world.get_location("Final Approach: Dracula"), HasAll("Dominus Hatred", "Dominus Anger", "Dominus Agony", "Glyph Union"))

    if not world.options.remove_training_hall:
        set_rule(world.get_location("Training Hall: Freestanding"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))

        if world.options.add_brown_chests == AddBrownChests.option_include:
            set_rule(world.get_location("Training Hall: Top Chest"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))
            set_rule(world.get_location("Training Hall: First Way Down Chest"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))
            set_rule(world.get_location("Training Hall: Second Way Down Chest"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))
            set_rule(world.get_location("Training Hall: Third Way Down Chest"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))
            set_rule(world.get_location("Training Hall: Final Chest"), HasAll("Ordinary Rock", "Rapidus Fio", "Magnes", "Lizard Tail"))

    # Regular brown cheests
    if world.options.add_brown_chests == AddBrownChests.option_include:
        set_rule(world.get_location("Kalidus Channel: Third Room Underwater"), Has("Serpent Scale"))
        set_rule(world.get_location("Tymeo Mountains: Right Hill Alcove Chest"), Has("Lizard Tail"))
        set_rule(world.get_location("Tristis Pass: First Alcove"), Has("Lizard Tail"))
        set_rule(world.get_location("Tristis Pass: Lower Hill Left"), Has("Lizard Tail"))
        set_rule(world.get_location("Tristis Pass: Third Hill Left"), Has("Lizard Tail"))
        set_rule(world.get_location("Tristis Pass: Lower Hill Right"), Has("Lizard Tail"))
        set_rule(world.get_location("Tristis Pass: Third Hill Right"), Has("Lizard Tail"))
