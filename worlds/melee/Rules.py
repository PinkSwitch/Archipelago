from rule_builder.rules import HasAll, HasAny, Has, HasGroupUnique
from .in_game_data import all_characters
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SSBMWorld

adventure_trophies = {
    "Mario (Smash Trophy)",
    "Donkey Kong (Smash Trophy)",
    "Link (Smash Trophy)",
    "Samus Aran (Smash Trophy)",
    "Yoshi (Smash Trophy)",
    "Kirby (Smash Trophy)",
    "Fox McCloud (Smash Trophy)",
    "Pikachu (Smash Trophy)",
    "Ness (Smash Trophy)",
    "Captain Falcon (Smash Trophy)",
    "Bowser (Smash Trophy)",
    "Peach (Smash Trophy)",
    "Ice Climbers (Smash Trophy)",
    "Zelda (Smash Trophy)",
    "Sheik (Smash Trophy)",
    "Luigi (Smash Trophy)",
    "Jigglypuff (Smash Trophy)",
    "Mewtwo (Smash Trophy)",
    "Marth (Smash Trophy)",
    "Mr. Game & Watch (Smash Trophy)",
    "Dr. Mario (Smash Trophy)",
    "Ganondorf (Smash Trophy)",
    "Falco Lombardi (Smash Trophy)",
    "Young Link (Smash Trophy)",
    "Pichu (Smash Trophy)",
    "Roy (Smash Trophy)",
}

classic_trophies = {
    "Mario (Trophy)",
    "Donkey Kong (Trophy)",
    "Link (Trophy)",
    "Samus Aran (Trophy)",
    "Yoshi (Trophy)",
    "Kirby (Trophy)",
    "Fox McCloud (Trophy)",
    "Pikachu (Trophy)",
    "Ness (Trophy)",
    "Captain Falcon (Trophy)",
    "Bowser (Trophy)",
    "Peach (Trophy)",
    "Ice Climbers (Trophy)",
    "Zelda (Trophy)",
    "Sheik (Trophy)",
    "Luigi (Trophy)",
    "Jigglypuff (Trophy)",
    "Mewtwo (Trophy)",
    "Marth (Trophy)",
    "Mr. Game & Watch (Trophy)",
    "Dr. Mario (Trophy)",
    "Ganondorf (Trophy)",
    "Falco Lombardi (Trophy)",
    "Young Link (Trophy)",
    "Pichu (Trophy)",
    "Roy (Trophy)",
    }

allstar_trophies = {
    "Mario (Smash Alt Trophy)",
    "Donkey Kong (Smash Alt Trophy)",
    "Link (Smash Alt Trophy)",
    "Samus Aran (Smash Alt Trophy)",
    "Yoshi (Smash Alt Trophy)",
    "Kirby (Smash Alt Trophy)",
    "Fox McCloud (Smash Alt Trophy)",
    "Pikachu (Smash Alt Trophy)",
    "Ness (Smash Alt Trophy)",
    "Captain Falcon (Smash Alt Trophy)",
    "Bowser (Smash Alt Trophy)",
    "Peach (Smash Alt Trophy)",
    "Ice Climbers (Smash Alt Trophy)",
    "Zelda (Smash Alt Trophy)",
    "Sheik (Smash Alt Trophy)",
    "Luigi (Smash Alt Trophy)",
    "Jigglypuff (Smash Alt Trophy)",
    "Mewtwo (Smash Alt Trophy)",
    "Marth (Smash Alt Trophy)",
    "Mr. Game & Watch (Smash Alt Trophy)",
    "Dr. Mario (Smash Alt Trophy)",
    "Ganondorf (Smash Alt Trophy)",
    "Falco Lombardi (Smash Alt Trophy)",
    "Young Link (Smash Alt Trophy)",
    "Pichu (Smash Alt Trophy)",
    "Roy (Smash Alt Trophy)"}

secret_characters = {"Dr. Mario", "Luigi", "Ganondorf", "Falco", "Marth", "Roy", "Jigglypuff", "Mewtwo", "Pichu", "Young Link", "Mr. Game & Watch"}

everyone_besides_gamewatch = {
    "Dr. Mario",
    "Mario",
    "Luigi",
    "Bowser",
    "Peach",
    "Yoshi",
    "Donkey Kong",
    "Captain Falcon",
    "Ganondorf",
    "Falco",
    "Fox",
    "Ness",
    "Ice Climbers",
    "Kirby",
    "Samus",
    "Zelda",
    "Link",
    "Young Link",
    "Pichu",
    "Pikachu",
    "Jigglypuff",
    "Mewtwo",
    "Marth",
    "Roy"
}


def set_location_rules(world: "SSBMWorld") -> None:
    set_rule = world.set_rule

    can_meteor = {"Captain Falcon", "Donkey Kong", "Falco", "Fox", "Ganondorf",
                  "Ice Climbers", "Kirby", "Link", "Luigi", "Young Link",
                  "Mario", "Marth", "Mewtwo", "Mr. Game & Watch", "Ness",
                  "Peach", "Roy", "Samus", "Yoshi", "Zelda"}

    can_reflect = {"Mario", "Dr. Mario", "Fox", "Falco", "Ness"}

    regular_stages = {"Mushroom Kingdom II", "Poké Floats", "Big Blue", "Flat Zone", "Fourside", "Brinstar Depths"}

    base_characters = {"Mario", "Donkey Kong", "Bowser", "Peach", "Captain Falcon", "Yoshi", "Fox", "Ness", "Ice Climbers", "Kirby", "Samus", "Link", "Pikachu", "Zelda"}

    good_hr_characters = {"Ganondorf", "Yoshi", "Jigglypuff", "Roy"}  # Can get over 1,400
    decent_hr_characters = {"Dr. Mario"}  # Can get over 1,326 casually

    good_combo_char = {"Kirby", "Fox", "Pichu", "Pikachu", "Zelda", "Link", "Young Link", "Mewtwo"}
    decent_combo_char = {"Yoshi", "Falco"}

    event_chars = {"Mario", "Donkey Kong", "Ness", "Yoshi", "Kirby", "Samus", "Link", "Bowser", "Falco", "Captain Falcon", "Young Link", "Luigi", "Jigglypuff", "Marth", "Fox", "Mr. Game & Watch"}

    set_rule(world.get_location("Event Match - Game & Watch Forever!"), Has("Mr. Game & Watch"))

    set_rule(world.get_location("Game - Pikmin Memory Card Data"), Has("Pikmin Savefile"))

    if world.options.adventure_clear_trophies:
        for character in all_characters:
            set_rule(world.get_location(f"{character} - Adventure Trophy Unlock"), Has(f"{character}"))

    if world.options.classic_clear_trophies:
        for character in all_characters:
            set_rule(world.get_location(f"{character} - Classic Trophy Unlock"), Has(f"{character}"))

    if world.options.all_star_clear_trophies:
        for character in all_characters:
            set_rule(world.get_location(f"{character} - All-Star Trophy Unlock"), Has(f"{character}"))

    set_rule(world.get_location("Training Mode - 125 Combined Combos"), HasAll(*good_combo_char, "Bowser"))
    set_rule(world.get_location("Training Mode - 10-Hit Combo"), HasAny(*decent_combo_char) | (HasAny(*good_combo_char) & Has("Bowser")))
    set_rule(world.get_location("Training Mode - 20-Hit Combo"), HasAny(*good_combo_char) & Has("Bowser"))

    set_rule(world.get_location("Home-Run Contest - 16,404 Ft. Combined"), HasGroupUnique("Characters", 16))
    # set_rule(world.get_location("Home-Run Contest - 984 Ft."), ("????")) expect everyone to get at least 1K
    set_rule(world.get_location("Home-Run Contest - 1,312 Ft."), HasAny(*decent_hr_characters) | HasAny(*good_hr_characters))
    set_rule(world.get_location("Home-Run Contest - 1,476 Ft."), HasAny(*good_hr_characters))

    set_rule(world.get_location("Game - All Stages + Secret Characters"), HasGroupUnique("Stages", 11) & HasAll(*secret_characters))
    set_rule(world.get_location("Game - Unlock Luigi, Jigglypuff, Mewtwo, Mr. Game & Watch, and Marth"), HasAll(
        "Luigi", "Jigglypuff", "Mewtwo", "Mr. Game & Watch", "Marth"))

    set_rule(world.get_location("Game - Unlock Roy, Pichu, Ganondorf, Dr. Mario, Young Link, and Falco"), HasAll(
        "Roy", "Pichu", "Ganondorf", "Dr. Mario", "Young Link", "Falco"))

    if "Birdo (Trophy)" in world.picked_trophies:
        set_rule(world.get_location("Game - Have Birdo Trophy"), Has("Birdo (Trophy)"))

    if "Kraid (Trophy)" in world.picked_trophies:
        set_rule(world.get_location("Game - Have Kraid Trophy"), Has("Kraid (Trophy)"))

    if "Falcon Flyer (Trophy)" in world.picked_trophies:
        set_rule(world.get_location("Game - Have Falcon Flyer Trophy"), Has("Falcon Flyer (Trophy)"))

    if "UFO (Trophy)" in world.picked_trophies:
        set_rule(world.get_location("Game - Have UFO Trophy"), Has("UFO (Trophy)"))

    if "Sudowoodo (Trophy)" in world.picked_trophies:
        set_rule(world.get_location("Game - Have Sudowoodo Trophy"), Has("Sudowoodo (Trophy)"))

    set_rule(world.get_location("Game - Unlock All Regular Stages"), HasAll(*regular_stages))

    set_rule(world.get_location("Any 1P - Game & Watch Clear"), Has("Mr. Game & Watch"))

    set_rule(world.get_location("Any 1P - Dr. Mario Unlock Match"), Has("Mario"))
    set_rule(world.get_location("Game - Marth Unlock Match"), HasAll(*base_characters))
    set_rule(world.get_location("Any 1P - Young Link Unlock Match"), HasGroupUnique("Characters", 10))
    set_rule(world.get_location("Any 1P - Roy Unlock Match"), Has("Marth"))
    set_rule(world.get_location("Any 1P - Game & Watch Unlock Match"), HasAll(*everyone_besides_gamewatch) & HasAny(
                                                                        "Adventure Mode", "All-Star Mode", "Classic Mode", "Target Test"))

    set_rule(world.get_location("Event Match - Ganondorf Unlock Match"), Has("Link"))

    set_rule(world.get_location("Trophy Room - Admire Collection"), HasGroupUnique("Trophies", world.options.trophies_required.value))

    if world.all_adventure_trophies:
        set_rule(world.get_location("Adventure Mode - All Character Trophies"), HasAll(*adventure_trophies))

    if world.all_classic_trophies:
        set_rule(world.get_location("Classic Mode - All Character Trophies"), HasAll(*classic_trophies))

    if world.all_allstar_trophies:
        set_rule(world.get_location("All-Star Mode - All Character Trophies"), HasAll(*allstar_trophies))

    if world.options.event_checks:
        set_rule(world.get_location("Event Match - Trouble King"), Has("Mario"))
        set_rule(world.get_location("Event Match - Lord of the Jungle"), Has("Donkey Kong"))
        set_rule(world.get_location("Event Match - Spare Change"), Has("Ness"))
        set_rule(world.get_location("Event Match - Yoshi's Egg"), Has("Yoshi"))
        set_rule(world.get_location("Event Match - Kirby's Air-raid"), Has("Kirby"))
        set_rule(world.get_location("Event Match - Bounty Hunters"), Has("Samus"))
        set_rule(world.get_location("Event Match - Link's Adventure"), Has("Link"))
        set_rule(world.get_location("Event Match - Peach's Peril"), Has("Mario"))
        set_rule(world.get_location("Event Match - Gargantuans"), Has("Bowser"))
        set_rule(world.get_location("Event Match - Cold Armor"), Has("Samus"))
        set_rule(world.get_location("Event Match - Triforce Gathering"), Has("Link"))
        set_rule(world.get_location("Event Match - Target Acquired"), Has("Falco"))
        set_rule(world.get_location("Event Match - Lethal Marathon"), Has("Captain Falcon"))
        set_rule(world.get_location("Event Match - Seven Years"), Has("Young Link"))
        set_rule(world.get_location("Event Match - Time for a Checkup"), Has("Luigi"))
        set_rule(world.get_location("Event Match - Space Travelers"), Has("Ness"))
        set_rule(world.get_location("Event Match - Jigglypuff Live!"), Has("Jigglypuff"))
        set_rule(world.get_location("Event Match - En Garde!"), Has("Marth"))
        set_rule(world.get_location("Event Match - Trouble King 2"), Has("Luigi"))
        set_rule(world.get_location("Event Match - Birds of Prey"), Has("Fox"))
    
    if world.options.target_checks:
        for character in all_characters:
            set_rule(world.get_location(f"Target Test - {character}"), Has(f"{character}"))

    if world.options.ten_man_checks:
        for character in all_characters:
            set_rule(world.get_location(f"Multi Man Melee - {character} 10-man"), Has(f"{character}"))

    if world.options.bonus_checks:
        set_rule(world.get_location("Bonus - Meteor Smash"), HasAny(*can_meteor))
                                                                                                            
        set_rule(world.get_location("Bonus - Meteor Clear"), HasAny(*can_meteor))
        set_rule(world.get_location("Bonus - Poser Power"), Has("Luigi"))
        set_rule(world.get_location("Bonus - Poser KO"), Has("Luigi"))
        set_rule(world.get_location("Bonus - Bank-Shot KO"), HasAny(*can_reflect))
        set_rule(world.get_location("Bonus - Metal Bros. KO"), Has("Luigi"))

        if world.options.enable_hard_bonuses:
            set_rule(world.get_location("Bonus - Meteor Survivor"), HasAny(*can_meteor))
            set_rule(world.get_location("Bonus - Meteor Master"), HasAny(*can_meteor))
            set_rule(world.get_location("Bonus - Flying Meteor"), HasAny(*can_meteor))
            set_rule(world.get_location("Bonus - Quadruple KO"), HasAny("Adventure Mode", "All-Star Mode"))
            set_rule(world.get_location("Bonus - Quintuple KO"), HasAny("Adventure Mode", "All-Star Mode"))

    if world.options.diskun_trophy_check:
        set_rule(world.get_location("Melee - All Bonuses"), HasAll("Adventure Mode", "All-Star Mode", "Classic Mode", "Luigi") & HasAny(*can_meteor) and HasAny(*can_reflect))

    if "All Targets" in world.options.goal_triggers:
        set_rule(world.get_location("Goal: All Targets Clear"), HasGroupUnique("Characters", 25))

    if "Other Events" in world.options.goal_triggers:
        set_rule(world.get_location("Goal: Other Events Clear"), HasAll(*event_chars))

    if world.options.long_targettest_checks:
        set_rule(world.get_location("Target Test - All Characters, Sub 12:30 Total Time"), HasGroupUnique("Characters", 25))
        set_rule(world.get_location("Target Test - All Characters, Sub 25 Minutes Total Time"), HasGroupUnique("Characters", 25))
        set_rule(world.get_location("Target Test - All Characters"), HasGroupUnique("Characters", 25))
