from worlds.generic.Rules import set_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import SSBMWorld

adventure_trophies = {
    "Mario (Smash Trophy)",
    "Donkey Kong (Smash Trophy)",
    "Link (Smash Trophy)",
    "Samus (Smash Trophy)",
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
    "Samus (Trophy)",
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
    "Samus (Smash Alt Trophy)",
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
    "Roy (Smash Alt Trophy)",}


def set_location_rules(world: "SSBMWorld") -> None:
    player = world.player

    can_meteor = {"Captain Falcon", "Donkey Kong", "Falco", "Fox", "Ganondorf",
                                "Ice Climbers", "Kirby", "Link", "Luigi", "Young Link",
                                "Mario", "Marth", "Mewtwo", "Mr. Game & Watch", "Ness",
                                "Peach", "Roy", "Samus", "Yoshi", "Zelda"}

    can_reflect = {"Mario", "Dr. Mario", "Fox", "Falco", "Ness"}

    regular_stages = {"Mushroom Kingdom II", "Poké Floats", "Big Blue", "Flat Zone", "Fourside", "Brinstar Depths"}

    base_characters = {"Mario", "Donkey Kong", "Bowser", "Peach", "Captain Falcon", "Yoshi", "Fox", "Ness", "Ice Climbers", "Kirby", "Samus", "Link", "Pikachu", "Zelda"}

    set_rule(world.multiworld.get_location("Event Match - Game & Watch Forever!", player), lambda state: state.has("Mr. Game & Watch", player))

    set_rule(world.multiworld.get_location("Mario - Adventure Trophy Unlock", player), lambda state: state.has("Mario", player))
    set_rule(world.multiworld.get_location("Donkey Kong - Adventure Trophy Unlock", player), lambda state: state.has("Donkey Kong", player))
    set_rule(world.multiworld.get_location("Link - Adventure Trophy Unlock", player), lambda state: state.has("Link", player))
    set_rule(world.multiworld.get_location("Samus - Adventure Trophy Unlock", player), lambda state: state.has("Samus", player))
    set_rule(world.multiworld.get_location("Yoshi - Adventure Trophy Unlock", player), lambda state: state.has("Yoshi", player))
    set_rule(world.multiworld.get_location("Kirby - Adventure Trophy Unlock", player), lambda state: state.has("Kirby", player))
    set_rule(world.multiworld.get_location("Fox - Adventure Trophy Unlock", player), lambda state: state.has("Fox", player))
    set_rule(world.multiworld.get_location("Pikachu - Adventure Trophy Unlock", player), lambda state: state.has("Pikachu", player))
    set_rule(world.multiworld.get_location("Ness - Adventure Trophy Unlock", player), lambda state: state.has("Ness", player))
    set_rule(world.multiworld.get_location("Captain Falcon - Adventure Trophy Unlock", player), lambda state: state.has("Captain Falcon", player))
    set_rule(world.multiworld.get_location("Bowser - Adventure Trophy Unlock", player), lambda state: state.has("Bowser", player))
    set_rule(world.multiworld.get_location("Peach - Adventure Trophy Unlock", player), lambda state: state.has("Peach", player))
    set_rule(world.multiworld.get_location("Ice Climbers - Adventure Trophy Unlock", player), lambda state: state.has("Ice Climbers", player))
    set_rule(world.multiworld.get_location("Zelda - Adventure Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Sheik - Adventure Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Luigi - Adventure Trophy Unlock", player), lambda state: state.has("Luigi", player))
    set_rule(world.multiworld.get_location("Jigglypuff - Adventure Trophy Unlock", player), lambda state: state.has("Jigglypuff", player))
    set_rule(world.multiworld.get_location("Mewtwo - Adventure Trophy Unlock", player), lambda state: state.has("Mewtwo", player))
    set_rule(world.multiworld.get_location("Mr. Game & Watch - Adventure Trophy Unlock", player), lambda state: state.has("Mr. Game & Watch", player))
    set_rule(world.multiworld.get_location("Marth - Adventure Trophy Unlock", player), lambda state: state.has("Marth", player))
    set_rule(world.multiworld.get_location("Dr. Mario - Adventure Trophy Unlock", player), lambda state: state.has("Dr. Mario", player))
    set_rule(world.multiworld.get_location("Ganondorf - Adventure Trophy Unlock", player), lambda state: state.has("Ganondorf", player))
    set_rule(world.multiworld.get_location("Falco - Adventure Trophy Unlock", player), lambda state: state.has("Falco", player))
    set_rule(world.multiworld.get_location("Young Link - Adventure Trophy Unlock", player), lambda state: state.has("Young Link", player))
    set_rule(world.multiworld.get_location("Pichu - Adventure Trophy Unlock", player), lambda state: state.has("Pichu", player))
    set_rule(world.multiworld.get_location("Roy - Adventure Trophy Unlock", player), lambda state: state.has("Roy", player))

    set_rule(world.multiworld.get_location("Mario - Classic Trophy Unlock", player), lambda state: state.has("Mario", player))
    set_rule(world.multiworld.get_location("Donkey Kong - Classic Trophy Unlock", player), lambda state: state.has("Donkey Kong", player))
    set_rule(world.multiworld.get_location("Link - Classic Trophy Unlock", player), lambda state: state.has("Link", player))
    set_rule(world.multiworld.get_location("Samus - Classic Trophy Unlock", player), lambda state: state.has("Samus", player))
    set_rule(world.multiworld.get_location("Yoshi - Classic Trophy Unlock", player), lambda state: state.has("Yoshi", player))
    set_rule(world.multiworld.get_location("Kirby - Classic Trophy Unlock", player), lambda state: state.has("Kirby", player))
    set_rule(world.multiworld.get_location("Fox - Classic Trophy Unlock", player), lambda state: state.has("Fox", player))
    set_rule(world.multiworld.get_location("Pikachu - Classic Trophy Unlock", player), lambda state: state.has("Pikachu", player))
    set_rule(world.multiworld.get_location("Ness - Classic Trophy Unlock", player), lambda state: state.has("Ness", player))
    set_rule(world.multiworld.get_location("Captain Falcon - Classic Trophy Unlock", player), lambda state: state.has("Captain Falcon", player))
    set_rule(world.multiworld.get_location("Bowser - Classic Trophy Unlock", player), lambda state: state.has("Bowser", player))
    set_rule(world.multiworld.get_location("Peach - Classic Trophy Unlock", player), lambda state: state.has("Peach", player))
    set_rule(world.multiworld.get_location("Ice Climbers - Classic Trophy Unlock", player), lambda state: state.has("Ice Climbers", player))
    set_rule(world.multiworld.get_location("Zelda - Classic Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Sheik - Classic Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Luigi - Classic Trophy Unlock", player), lambda state: state.has("Luigi", player))
    set_rule(world.multiworld.get_location("Jigglypuff - Classic Trophy Unlock", player), lambda state: state.has("Jigglypuff", player))
    set_rule(world.multiworld.get_location("Mewtwo - Classic Trophy Unlock", player), lambda state: state.has("Mewtwo", player))
    set_rule(world.multiworld.get_location("Mr. Game & Watch - Classic Trophy Unlock", player), lambda state: state.has("Mr. Game & Watch", player))
    set_rule(world.multiworld.get_location("Marth - Classic Trophy Unlock", player), lambda state: state.has("Marth", player))
    set_rule(world.multiworld.get_location("Dr. Mario - Classic Trophy Unlock", player), lambda state: state.has("Dr. Mario", player))
    set_rule(world.multiworld.get_location("Ganondorf - Classic Trophy Unlock", player), lambda state: state.has("Ganondorf", player))
    set_rule(world.multiworld.get_location("Falco - Classic Trophy Unlock", player), lambda state: state.has("Falco", player))
    set_rule(world.multiworld.get_location("Young Link - Classic Trophy Unlock", player), lambda state: state.has("Young Link", player))
    set_rule(world.multiworld.get_location("Pichu - Classic Trophy Unlock", player), lambda state: state.has("Pichu", player))
    set_rule(world.multiworld.get_location("Roy - Classic Trophy Unlock", player), lambda state: state.has("Roy", player))

    set_rule(world.multiworld.get_location("Mario - All-Star Trophy Unlock", player), lambda state: state.has("Mario", player))
    set_rule(world.multiworld.get_location("Donkey Kong - All-Star Trophy Unlock", player), lambda state: state.has("Donkey Kong", player))
    set_rule(world.multiworld.get_location("Link - All-Star Trophy Unlock", player), lambda state: state.has("Link", player))
    set_rule(world.multiworld.get_location("Samus - All-Star Trophy Unlock", player), lambda state: state.has("Samus", player))
    set_rule(world.multiworld.get_location("Yoshi - All-Star Trophy Unlock", player), lambda state: state.has("Yoshi", player))
    set_rule(world.multiworld.get_location("Kirby - All-Star Trophy Unlock", player), lambda state: state.has("Kirby", player))
    set_rule(world.multiworld.get_location("Fox - All-Star Trophy Unlock", player), lambda state: state.has("Fox", player))
    set_rule(world.multiworld.get_location("Pikachu - All-Star Trophy Unlock", player), lambda state: state.has("Pikachu", player))
    set_rule(world.multiworld.get_location("Ness - All-Star Trophy Unlock", player), lambda state: state.has("Ness", player))
    set_rule(world.multiworld.get_location("Captain Falcon - All-Star Trophy Unlock", player), lambda state: state.has("Captain Falcon", player))
    set_rule(world.multiworld.get_location("Bowser - All-Star Trophy Unlock", player), lambda state: state.has("Bowser", player))
    set_rule(world.multiworld.get_location("Peach - All-Star Trophy Unlock", player), lambda state: state.has("Peach", player))
    set_rule(world.multiworld.get_location("Ice Climbers - All-Star Trophy Unlock", player), lambda state: state.has("Ice Climbers", player))
    set_rule(world.multiworld.get_location("Zelda - All-Star Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Sheik - All-Star Trophy Unlock", player), lambda state: state.has("Zelda", player))
    set_rule(world.multiworld.get_location("Luigi - All-Star Trophy Unlock", player), lambda state: state.has("Luigi", player))
    set_rule(world.multiworld.get_location("Jigglypuff - All-Star Trophy Unlock", player), lambda state: state.has("Jigglypuff", player))
    set_rule(world.multiworld.get_location("Mewtwo - All-Star Trophy Unlock", player), lambda state: state.has("Mewtwo", player))
    set_rule(world.multiworld.get_location("Mr. Game & Watch - All-Star Trophy Unlock", player), lambda state: state.has("Mr. Game & Watch", player))
    set_rule(world.multiworld.get_location("Marth - All-Star Trophy Unlock", player), lambda state: state.has("Marth", player))
    set_rule(world.multiworld.get_location("Dr. Mario - All-Star Trophy Unlock", player), lambda state: state.has("Dr. Mario", player))
    set_rule(world.multiworld.get_location("Ganondorf - All-Star Trophy Unlock", player), lambda state: state.has("Ganondorf", player))
    set_rule(world.multiworld.get_location("Falco - All-Star Trophy Unlock", player), lambda state: state.has("Falco", player))
    set_rule(world.multiworld.get_location("Young Link - All-Star Trophy Unlock", player), lambda state: state.has("Young Link", player))
    set_rule(world.multiworld.get_location("Pichu - All-Star Trophy Unlock", player), lambda state: state.has("Pichu", player))
    set_rule(world.multiworld.get_location("Roy - All-Star Trophy Unlock", player), lambda state: state.has("Roy", player))

    set_rule(world.multiworld.get_location("Training Mode - 125 Combined Combos", player), lambda state: state.has("????", player))
    set_rule(world.multiworld.get_location("Training Mode - 10-Hit Combo", player), lambda state: state.has("????", player))
    set_rule(world.multiworld.get_location("Training Mode - 20-Hit Combo", player), lambda state: state.has("????", player))

    set_rule(world.multiworld.get_location("Home Run Contest - 16,404 Ft. Combined", player), lambda state: state.has("????", player))
    set_rule(world.multiworld.get_location("Home Run Contest - 984 Ft.", player), lambda state: state.has("????", player))
    set_rule(world.multiworld.get_location("Home Run Contest - 1,312 Ft.", player), lambda state: state.has("????", player))
    set_rule(world.multiworld.get_location("Home Run Contest - 1,476 Ft.", player), lambda state: state.has("????", player))

    set_rule(world.multiworld.get_location("Game - Unlock All Stages", player), lambda state: state.has_group_unique("Stages", player, 11))
    set_rule(world.multiworld.get_location("Game - Unlock Luigi, Jigglypuff, Mewtwo, Mr. Game & Watch, and Marth", player), lambda state: state.has_all({
        "Luigi", "Jigglypuff", "Mewtwo", "Mr. Game & Watch", "Marth"}, player))

    set_rule(world.multiworld.get_location("Game - Unlock Roy, Pichu, Ganondorf, Dr. Mario, Young Link, and Falco", player), lambda state: state.has_all({
        "Roy", "Pichu", "Ganondorf", "Dr. Mario", "Young Link", "Falco"}, player))

    set_rule(world.multiworld.get_location("Game - Have Birdo Trophy", player), lambda state: state.has("Birdo (Trophy)", player))
    set_rule(world.multiworld.get_location("Game - Have Kraid Trophy", player), lambda state: state.has("Kraid (Trophy)", player))
    set_rule(world.multiworld.get_location("Game - Have Falcon Flyer Trophy", player), lambda state: state.has("Falcon Flyer (Trophy)", player))
    set_rule(world.multiworld.get_location("Game - Have UFO Trophy", player), lambda state: state.has("UFO (Trophy)", player))
    set_rule(world.multiworld.get_location("Game - Have Sudowoodo Trophy", player), lambda state: state.has("Sudowoodo (Trophy)", player))

    set_rule(world.multiworld.get_location("Game - Unlock All Regular Stages", player), lambda state: state.has_all(regular_stages, player))

    set_rule(world.multiworld.get_location("Any 1P - Dr. Mario Unlock Match", player), lambda state: state.has("Mario", player))
    set_rule(world.multiworld.get_location("Game - Marth Unlock Match", player), lambda state: state.has_all(base_characters, player))
    set_rule(world.multiworld.get_location("Any 1P - Young Link Unlock Match", player), lambda state: state.has_group_unique("Characters", player, 10))
    set_rule(world.multiworld.get_location("Any 1P - Roy Unlock Match", player), lambda state: state.has("Marth", player))
    set_rule(world.multiworld.get_location(
        "Any 1P - Game & Watch Unlock Match", player), lambda state: state.has_group_unique("Characters", player, 24) and state.has_any({
                                                                        "Adventure Mode", "All-Star Mode", "Classic Mode", "Target Test"}, player))

    set_rule(world.multiworld.get_location("Trophy Room - Admire Collection", player), lambda state: state.has_group_unique("Trophies", player, world.options.trophies_required.value))

    if world.all_adventure_trophies:
        set_rule(world.multiworld.get_location("Adventure Mode - All Character Trophies", player), lambda state: state.has_all(adventure_trophies, player))

    if world.all_classic_trophies:
        set_rule(world.multiworld.get_location("Classic Mode - All Character Trophies", player), lambda state: state.has_all(classic_trophies, player))

    if world.all_allstar_trophies:
        set_rule(world.multiworld.get_location("All-Star Mode - All Character Trophies", player), lambda state: state.has_all(allstar_trophies, player))

    if world.options.event_checks:
        set_rule(world.multiworld.get_location("Event Match - Trouble King", player), lambda state: state.has("Mario", player))
        set_rule(world.multiworld.get_location("Event Match - Lord of the Jungle", player), lambda state: state.has("Donkey Kong", player))
        set_rule(world.multiworld.get_location("Event Match - Spare Change", player), lambda state: state.has("Ness", player))
        set_rule(world.multiworld.get_location("Event Match - Yoshi's Egg", player), lambda state: state.has("Yoshi", player))
        set_rule(world.multiworld.get_location("Event Match - Kirby's Air-raid", player), lambda state: state.has("Kirby", player))
        set_rule(world.multiworld.get_location("Event Match - Bounty Hunters", player), lambda state: state.has("Samus", player))
        set_rule(world.multiworld.get_location("Event Match - Link's Adventure", player), lambda state: state.has("Link", player))
        set_rule(world.multiworld.get_location("Event Match - Peach's Peril", player), lambda state: state.has("Mario", player))
        set_rule(world.multiworld.get_location("Event Match - Gargantuans", player), lambda state: state.has("Bowser", player))
        set_rule(world.multiworld.get_location("Event Match - Cold Armor", player), lambda state: state.has("Samus", player))
        set_rule(world.multiworld.get_location("Event Match - Target Acquired", player), lambda state: state.has("Falco", player))
        set_rule(world.multiworld.get_location("Event Match - Lethal Marathon", player), lambda state: state.has("Captain Falcon", player))
        set_rule(world.multiworld.get_location("Event Match - Seven Years", player), lambda state: state.has("Young Link", player))
        set_rule(world.multiworld.get_location("Event Match - Time for a Checkup", player), lambda state: state.has("Luigi", player))
        set_rule(world.multiworld.get_location("Event Match - Space Travelers", player), lambda state: state.has("Ness", player))
        set_rule(world.multiworld.get_location("Event Match - Jigglypuff Live!", player), lambda state: state.has("Jigglypuff", player))
        set_rule(world.multiworld.get_location("Event Match - En Garde!", player), lambda state: state.has("Marth", player))
        set_rule(world.multiworld.get_location("Event Match - Trouble King 2", player), lambda state: state.has("Luigi", player))
        set_rule(world.multiworld.get_location("Event Match - Birds of Prey", player), lambda state: state.has("Fox", player))
    
    if world.options.target_checks:
        set_rule(world.multiworld.get_location("Target Test - Mario", player), lambda state: state.has("Mario", player))
        set_rule(world.multiworld.get_location("Target Test - Dr. Mario", player), lambda state: state.has("Dr. Mario", player))
        set_rule(world.multiworld.get_location("Target Test - Luigi", player), lambda state: state.has("Luigi", player))
        set_rule(world.multiworld.get_location("Target Test - Bowser", player), lambda state: state.has("Bowser", player))
        set_rule(world.multiworld.get_location("Target Test - Peach", player), lambda state: state.has("Peach", player))
        set_rule(world.multiworld.get_location("Target Test - Yoshi", player), lambda state: state.has("Yoshi", player))
        set_rule(world.multiworld.get_location("Target Test - Donkey Kong", player), lambda state: state.has("Donkey Kong", player))
        set_rule(world.multiworld.get_location("Target Test - Captain Falcon", player), lambda state: state.has("Captain Falcon", player))
        set_rule(world.multiworld.get_location("Target Test - Ganondorf", player), lambda state: state.has("Ganondorf", player))
        set_rule(world.multiworld.get_location("Target Test - Falco", player), lambda state: state.has("Falco", player))
        set_rule(world.multiworld.get_location("Target Test - Fox", player), lambda state: state.has("Fox", player))
        set_rule(world.multiworld.get_location("Target Test - Ness", player), lambda state: state.has("Ness", player))
        set_rule(world.multiworld.get_location("Target Test - Ice Climbers", player), lambda state: state.has("Ice Climbers", player))
        set_rule(world.multiworld.get_location("Target Test - Kirby", player), lambda state: state.has("Kirby", player))
        set_rule(world.multiworld.get_location("Target Test - Samus", player), lambda state: state.has("Samus", player))
        set_rule(world.multiworld.get_location("Target Test - Zelda", player), lambda state: state.has("Zelda", player))
        set_rule(world.multiworld.get_location("Target Test - Link", player), lambda state: state.has("Link", player))
        set_rule(world.multiworld.get_location("Target Test - Young Link", player), lambda state: state.has("Young Link", player))
        set_rule(world.multiworld.get_location("Target Test - Pichu", player), lambda state: state.has("Pichu", player))
        set_rule(world.multiworld.get_location("Target Test - Pikachu", player), lambda state: state.has("Pikachu", player))
        set_rule(world.multiworld.get_location("Target Test - Jigglypuff", player), lambda state: state.has("Jigglypuff", player))
        set_rule(world.multiworld.get_location("Target Test - Mewtwo", player), lambda state: state.has("Mewtwo", player))
        set_rule(world.multiworld.get_location("Target Test - Mr. Game & Watch", player), lambda state: state.has("Mr. Game & Watch", player))
        set_rule(world.multiworld.get_location("Target Test - Marth", player), lambda state: state.has("Marth", player))
        set_rule(world.multiworld.get_location("Target Test - Roy", player), lambda state: state.has("Roy", player))

    if world.options.bonus_checks:
        set_rule(world.multiworld.get_location("Bonus - Meteor Smash", player), lambda state: state.has_any({"Captain Falcon", "Donkey Kong", "Falco", "Fox", "Ganondorf",
                                                                                                             "Ice Climbers", "Kirby", "Link", "Luigi", "Young Link",
                                                                                                             "Mario", "Marth", "Mewtwo", "Mr. Game & Watch", "Ness",
                                                                                                             "Peach", "Roy", "Samus", "Yoshi", "Zelda"}, player))
                                                                                                             
        set_rule(world.multiworld.get_location("Bonus - Meteor Clear", player), lambda state: state.has_any(can_meteor, player))
        set_rule(world.multiworld.get_location("Bonus - Poser Power", player), lambda state: state.has("Luigi", player))
        set_rule(world.multiworld.get_location("Bonus - Poser KO", player), lambda state: state.has("Luigi", player))
        set_rule(world.multiworld.get_location("Bonus - Bank-Shot KO", player), lambda state: state.has_any(can_reflect, player))
        set_rule(world.multiworld.get_location("Bonus - Metal Bros. KO", player), lambda state: state.has("Luigi", player))

        if world.options.enable_hard_bonuses:
            set_rule(world.multiworld.get_location("Bonus - Meteor Survivor", player), lambda state: state.has_any(can_meteor, player))
            set_rule(world.multiworld.get_location("Bonus - Meteor Master", player), lambda state: state.has_any(can_meteor, player))
            set_rule(world.multiworld.get_location("Bonus - Flying Meteor", player), lambda state: state.has_any(can_meteor, player))
            set_rule(world.multiworld.get_location("Bonus - Quadruple KO", player), lambda state: state.has_any({"Adventure Mode", "All-Star Mode"}, player))
            set_rule(world.multiworld.get_location("Bonus - Quintuple KO", player), lambda state: state.has_any({"Adventure Mode", "All-Star Mode"}, player))

    if world.options.diskun_trophy_check:
        set_rule(world.multiworld.get_location("Melee - All Bonuses", player), lambda state: state.has_all({"Adventure Mode", "All-Star Mode", "Classic Mode", "Luigi"}, player) and state.has_any(can_meteor, player) and state.has_any(can_reflect, player))

    if world.options.goal_all_targets:
        set_rule(world.multiworld.get_location("Goal: All Targets Clear", player), lambda state: state.has_group_unique("Characters", player, 25))

    if world.options.goal_all_events:
        set_rule(world.multiworld.get_location("Goal: All Events Clear", player), lambda state: state.has_all(event_chars, player))
        