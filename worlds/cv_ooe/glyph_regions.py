from .Options import RandomStolenGlyphs, RandomDropGlyphs
from rule_builder.rules import HasAll, CanReachLocation, Has, HasAny


def set_enemy_glyph_regions(world):
    world.get_region("Library").connect(world.get_region("Wallman"))
    world.get_region("Library - Past Wallman").connect(world.get_region("Wallman"))

    if world.options.randomize_stolen_glyphs == RandomStolenGlyphs.option_glyphsanity:
        world.get_region("Ruvas Forest").connect(world.get_region("Necromancer"))
        world.get_region("Kalidus Channel Depths Right").connect(world.get_region("Sea Demon"))
        world.get_region("Somnus Reef Main").connect(world.get_region("Sea Demon"))

        world.get_region("Tymeo Mountains East").connect(world.get_region("Fire Demon"))
        world.get_region("Misty Forest Road").connect(world.get_region("Black Fomor"))
        world.get_region("Tristis Pass Waterfall").connect(world.get_region("Thunder Demon"))
        world.get_region("Mystery Manor").connect(world.get_region("White Fomor"))
        world.get_region("Library").connect(world.get_region("White Fomor"))
        world.get_region("Library - Past Wallman").connect(world.get_region("White Fomor"))

        world.get_region("Underground Labyrinth").connect(world.get_region("Nova Skeleton"))
        world.get_region("Barracks").connect(world.get_region("Nova Skeleton"))
        world.get_region("Forsaken Cloister - Left").connect(world.get_region("Nova Skeleton"))
        world.get_region("Forsaken Cloister - Right").connect(world.get_region("Nova Skeleton"))

        world.get_region("Mystery Manor Main").connect(world.get_region("Albus"))
        world.get_region("Ecclesia").connect(world.get_region("Barlowe"), rule=CanReachLocation("Ecclesia: Barlowe Fight"))

        if not world.options.remove_training_hall:
            world.get_region("Training Hall").connect(world.get_region("Nova Skeleton"),
                                                      rule=HasAll("Lizard Tail", "Ordinary Rock", "Magnes"))

        if not world.options.remove_large_cavern:
            world.get_region("Large Cavern").connect(world.get_region("Jiang Shi"), rule=HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))
            world.get_region("Large Cavern").connect(world.get_region("Demon Lord"), rule=HasAll("Ordinary Rock", "Rapidus Fio", "Lizard Tail") | Has("Volaticus"))

    if world.options.randomize_dropped_glyphs == RandomDropGlyphs.option_glyphsanity:
        world.get_region("Monastery Magnets Area").connect(world.get_region("Bone Scimitar"))
        world.get_region("Ruvas Forest").connect(world.get_region("Bone Scimitar"))

        world.get_region("Ruvas Forest").connect(world.get_region("Axe Knight"))
        world.get_region("Minera Prison Island Main").connect(world.get_region("Axe Knight"))

        world.get_region("Minera Prison Island Main").connect(world.get_region("Bone Archer"))
        world.get_region("Minera Prison Island Main").connect(world.get_region("Spear Guard"))
        world.get_region("Misty Forest Road").connect(world.get_region("Werebat"))
        world.get_region("Kalidus Channel Depths Left").connect(world.get_region("Skull Spider"))
        world.get_region("Tymeo Mountains").connect(world.get_region("Skull Spider"))

        world.get_region("Tristis Pass Waterfall").connect(world.get_region("Owl"))
        world.get_region("Arms Depot").connect(world.get_region("Spectral Sword"))
        world.get_region("Final Approach").connect(world.get_region("Spectral Sword"))

        world.get_region("Mechanical Tower").connect(world.get_region("Automaton ZX27"), rule=HasAny("Volaticus", "Magnes", "Rapidus Fio", "Arma Machina"))
        world.get_region("Mechanical Tower Upper").connect(world.get_region("Automaton ZX27"))
        world.get_region("Mechanical Tower Upper Exit").connect(world.get_region("Automaton ZX27"))
        world.get_region("Final Approach").connect(world.get_region("Automaton ZX27"))

        world.get_region("Forsaken Cloister - Upper").connect(world.get_region("Gorgon Head"))
        world.get_region("Mechanical Tower Upper").connect(world.get_region("Gorgon Head"))

        world.get_region("Dracula's Castle").connect(world.get_region("Black Panther"))  # Entrance, no other items
        world.get_region("Library").connect(world.get_region("Black Panther"))

        world.get_region("Underground Labyrinth").connect(world.get_region("Polkir"))
        world.get_region("Barracks").connect(world.get_region("Red Smasher"))
        world.get_region("Mechanical Tower").connect(world.get_region("Red Smasher"))
        world.get_region("Arms Depot").connect(world.get_region("Red Smasher"))

        world.get_region("Underground Labyrinth").connect(world.get_region("Hammer Shaker"))
        world.get_region("Barracks").connect(world.get_region("Hammer Shaker"))
        world.get_region("Arms Depot").connect(world.get_region("Hammer Shaker"))
        world.get_region("Mechanical Tower").connect(world.get_region("Hammer Shaker"))
        world.get_region("Mechanical Tower Lower").connect(world.get_region("Hammer Shaker"))

        world.get_region("Arms Depot").connect(world.get_region("Great Knight"))
        world.get_region("Library Upper Exit").connect(world.get_region("Great Knight"))

        world.get_region("Final Approach").connect(world.get_region("Winged Skeleton"))
        world.get_region("Skeleton Cave").connect(world.get_region("Dullahan"))
        world.get_region("Tymeo Mountains East").connect(world.get_region("Dullahan"))

        world.get_region("Giant's Dwelling Main").connect(world.get_region("Miss Murder"))
        world.get_region("Oblivion Ridge").connect(world.get_region("Lizardman"))
        world.get_region("Tristis Pass").connect(world.get_region("Lizardman"))
