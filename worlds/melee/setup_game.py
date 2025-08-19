import logging

def setup_gamevars(world) -> None:
    world.all_trophies.remove("Birdo (Trophy)")
    world.all_trophies.remove("Kraid (Trophy)")
    world.all_trophies.remove("UFO (Trophy)")
    world.all_trophies.remove("Falcon Flyer (Trophy)")
    world.all_trophies.remove("Sudowoodo (Trophy)")  # These are always in the pool and need to not be rolled randomly

    world.starting_character = world.random.choice(["Dr. Mario", "Mario", "Luigi", "Bowser", "Peach",
                                                   "Yoshi", "Donkey Kong", "Captain Falcon", "Ganondorf", "Falco",
                                                   "Fox", "Ness", "Ice Climbers", "Kirby", "Samus",
                                                   "Zelda", "Link", "Young Link", "Pichu", "Pikachu",
                                                   "Jigglypuff", "Mewtwo", "Mr. Game & Watch", "Marth", "Roy"])
    world.multiworld.push_precollected(world.create_item(world.starting_character))

    if world.options.lottery_pool_mode == 1:
        for i in range(4):
            world.multiworld.itempool.append(world.create_item("Progressive Lottery Pool"))
            world.extra_item_count += 1
    elif world.options.lottery_pool_mode == 2:
        world.multiworld.itempool.extend[world.create_item("Lottery Pool Upgrade (Adventure/Classic Clear)"),
                                         world.create_item("Lottery Pool Upgrade (Secret Characters)"),
                                         world.create_item("Lottery Pool Upgrade (200 Vs. Matches)"),
                                         world.create_item("Lottery Pool Upgrade (250 Trophies)"),]
        world.extra_item_count += 4

    world.total_trophy_count = world.options.trophies_required + world.options.extra_trophies
    if world.total_trophy_count > 293:
        logger.warning(f"""Warning: {world.multiworld.get_player_name(world.player)}'s generated Trophy Count is too high.
                Required: {world.options.trophies_required} | Extra: {world.options.extra_trophies}. This will be automatically capped.""")
        world.total_trophy_count = 293
        world.options.extra_trophies = 293 - world.options.trophies_required

    for i in range(world.total_trophy_count):
        if not world.all_trophies:
            break
        else:
            trophy = world.random.choice(world.all_trophies)
            world.all_trophies.remove(trophy)
            world.picked_trophies.add(trophy)
            world.multiworld.itempool.append(world.create_item(trophy))
            world.extra_item_count += 1





def place_static_items(world):
    world.get_location("Trophy Room - Admire Collection").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_giga_bowser:
        world.get_location("Goal: Giga Bowser Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_crazy_hand:
        world.get_location("Goal: Crazy Hand Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_event_51:
        world.get_location("Goal: Event 51").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_all_events:
        world.get_location("Goal: All Events").place_locked_item(world.create_item("Sense of Accomplishment"))

    if world.options.goal_all_targets:
        world.get_location("Goal: All Targets Clear").place_locked_item(world.create_item("Sense of Accomplishment"))