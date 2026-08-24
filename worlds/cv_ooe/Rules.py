from rule_builder.rules import HasAll, HasAny, Has, CanReachLocation, HasGroupUnique, OptionFilter
from rule_builder.field_resolvers import FromOption
from .Options import VillagersRequired, AddBrownChests, BarloweRequired, LogicTricks

can_fly = Has("Volaticus") | HasAll("Magnes", "Redire",
                                    options=[OptionFilter(LogicTricks, "Redire Flight", operator="contains")])
can_slide = Has("Lizard Tail") | HasAll("Magnes", "Redire",
                                    options=[OptionFilter(LogicTricks, "Redire Slides", operator="contains")])


def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Ecclesia: Barlowe Fight"), HasAll("Dominus Hatred", "Dominus Anger", "Dominus Agony") & HasGroupUnique("Villagers", count=FromOption(VillagersRequired)))

    set_rule(world.get_location("Kalidus Channel: First Room Underwater"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Second Room Underwater"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Right Side Underwater Chest"), Has("Serpent Scale"))
    set_rule(world.get_location("Kalidus Channel: Right Exit Underwater Chest"), Has("Serpent Scale"))

    set_rule(world.get_location("Somnus Reef: Hidden Room"), can_slide)

    set_rule(world.get_location("Minera Prison Island: Top Room"), Has("Ordinary Rock") | can_fly)
    set_rule(world.get_location("Minera Prison Island: Top Room Chest"), Has("Ordinary Rock") | can_fly)
    set_rule(world.get_location("Minera Prison Island: Right Vertical Hidden Item"), HasAny("Ordinary Rock", "Volaticus", "Magnes", "Redire"))
    set_rule(world.get_location("Minera Prison Island: Tin Man Chest"), HasAny(*world.can_kill_tin_man))

    set_rule(world.get_location("Tymeo Mountains: Left Hill Alcove Chest"), Has("Arma Felix") | can_slide)
    set_rule(world.get_location("Tymeo Mountains: Left Hill Alcove Pickup"), Has("Arma Felix") | can_slide)
    set_rule(world.get_location("Tymeo Mountains: Lower Mountain Lower Paries Chest"), Has("Paries"))
    set_rule(world.get_location("Tymeo Mountains: Lower Mountain Upper Paries Chest"), Has("Paries"))
    set_rule(world.get_location("Tymeo Mountains: Wind Glyph"), Has("Magnes"))
    set_rule(world.get_location("Tymeo Mountains: Upper Hill Chest"), HasAny("Arma Felix") | can_slide)

    set_rule(world.get_location("Tristis Pass: Frozen Waterfall Glyph"), Has("Magnes"))
    set_rule(world.get_location("Tristis Pass: Second Hill Lowest Chest"), Has("Arma Felix") | can_slide)

    set_rule(world.get_location("Mystery Manor: Dark Room Chest"), Has("Arma Machina"))

    set_rule(world.get_location("Misty Forest Road: Right Big Room Ledge"), HasAny("Volaticus", "Rapidus Fio", "Magnes"))
    set_rule(world.get_location("Misty Forest Road: Ledge Item"), Has("Rapidus Fio") | can_fly)
    set_rule(world.get_location("Misty Forest Road: Paries Room Hidden Item"), Has("Paries"))
    set_rule(world.get_location("Misty Forest Road: Paries Room Pickup"), Has("Paries"))
    set_rule(world.get_location("Misty Forest Road: Paries Room Chest"), Has("Paries"))

    set_rule(world.get_location("Oblivion Ridge: Pre-Boss Ledge"), HasAny("Rapidus Fio", "Ordinary Rock") | can_fly)
    set_rule(world.get_location("Oblivion Ridge: Post-Boss Ledge Item"), HasAny("Rapidus Fio", "Ordinary Rock") | can_fly)

    set_rule(world.get_location("Skeleton Cave: First Room"), HasAny("Ordinary Rock", "Rapidus Fio") | can_fly)
    set_rule(world.get_location("Skeleton Cave: Dead End Upper"), HasAny("Ordinary Rock", "Rapidus Fio") | can_fly)

    set_rule(world.get_location("Monastery: Big Room Ledge"), HasAny("Ordinary Rock", "Rapidus Fio") | can_fly)
    set_rule(world.get_location("Monastery: Big Room Under Shelf"), can_slide)
    set_rule(world.get_location("Monastery: Blocks Glyph"),
             HasAny("Redire", "Globus", "Melio Ascia", "Umbra", "Nitesco") |
             (HasAny("Luminatio", "Vol Luminatio") & HasAny("Umbra", "Vol Umbra") |
                 HasAny("Ignis", "Vol Ignis") & HasAny("Grando", "Vol Grando") & Has("Glyph Union")) |
             (HasAny("Secare", "Vol Secare", "Melio Secare") & Has("Glyph Union") &
              OptionFilter(LogicTricks, "Monastery Cubes Glyph With Secare Union", operator="contains"))
             )
    set_rule(world.get_location("Monastery: Blocks Reward Chest"), (CanReachLocation("Monastery: Blocks Glyph")) & HasAny("Redire", "Melio Ascia", "Nitesco", "Luminatio", "Globus", "Acerbatus", "Umbra"))

    set_rule(world.get_location("Underground Labyrinth: Boulder Room Glyph"), Has("Paries"))

    set_rule(world.get_location("Mechanical Tower: Generator Puzzle"), HasAny("Volaticus", "Magnes", "Rapidus Fio", "Arma Machina") & HasAny(*world.generator_logic_glyphs))

    set_rule(world.get_location("Final Approach: Treasure Room Second From Right"), can_fly)
    set_rule(world.get_location("Final Approach: Treasure Room Far Right"), can_fly)
    set_rule(world.get_location("Final Approach: Treasure Room Far Left"), can_fly)
    set_rule(world.get_location("Final Approach: Treasure Room Second From Left"), can_fly)

    set_rule(world.get_location("Final Approach: Final Stash Far Right"), can_fly)
    set_rule(world.get_location("Final Approach: Final Stash Second From Left"), can_fly)
    set_rule(world.get_location("Final Approach: Final Stash Second From Right"), can_fly)
    set_rule(world.get_location("Final Approach: Final Stash Far Left"), can_fly)
    set_rule(world.get_location("Final Approach: Throne Right Chest"), Has("Paries"))
    set_rule(world.get_location("Final Approach: Throne Left Chest"), Has("Paries"))

    set_rule(world.get_location("Final Approach: Dracula"), HasAll("Dominus Hatred", "Dominus Anger", "Dominus Agony", "Glyph Union") &
            CanReachLocation("Ecclesia: Barlowe Fight", options=[OptionFilter(BarloweRequired, True)], filtered_resolution=True))

    if not world.options.remove_large_cavern:
        if world.options.add_brown_chests == AddBrownChests.option_include:
            set_rule(world.get_location("Large Cavern: Rest Room 1"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | HasAll("Volaticus"))
            set_rule(world.get_location("Large Cavern: Rest Room 2"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))
            set_rule(world.get_location("Large Cavern: Rest Room 3"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))
            set_rule(world.get_location("Large Cavern: Rest Room 4"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))
            set_rule(world.get_location("Large Cavern: Final Reward 1"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))
            set_rule(world.get_location("Large Cavern: Final Reward 2"), HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))

    # Regular brown cheests
    if world.options.add_brown_chests == AddBrownChests.option_include:
        set_rule(world.get_location("Kalidus Channel: Third Room Underwater"), Has("Serpent Scale"))
        set_rule(world.get_location("Tymeo Mountains: Right Hill Alcove Chest"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Tristis Pass: First Alcove"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Tristis Pass: Lower Hill Left"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Tristis Pass: Third Hill Left"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Tristis Pass: Lower Hill Right"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Tristis Pass: Third Hill Right"), Has("Arma Felix") | can_slide)
        set_rule(world.get_location("Mechanical Tower: First Gears Room Chest"), HasAny("Volaticus", "Magnes"))

    if world.options.add_no_hit_chests:
        set_rule(world.get_location("Minera Prison Island: Giant Skeleton No-Hit Chest"), HasAny("Ordinary Rock", "Magnes", "Volaticus") | OptionFilter(LogicTricks, "Giant Skeleton No-Hit Without Movement", operator="contains"))
        set_rule(world.get_location("Ecclesia: Barlowe No-Hit Chest"), CanReachLocation("Ecclesia: Barlowe Fight"))
        set_rule(world.get_location("Mechanical Tower: Death No-Hit Chest"), Has("Lizard Tail"))

        