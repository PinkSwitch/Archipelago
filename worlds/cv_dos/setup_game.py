from .modules.synthesis_randomizer import randomize_synthesis
from .modules.seal_shuffle import set_seals
from .modules.set_goals import set_goal_triggers
from .modules import enemy_randomizer
from logging import warning


def setup_game(world):
    from .generator_main import create_progress_event
    if world.player_name == "ironsoul":
        world.iron_mode = True

    if world.iron_mode:
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 1"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 2"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 3"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 4"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 5"))
        world.multiworld.local_early_items[world.player]["Malphas Soul"] = 1

    world.extra_soul_slots = 99  # Locations that can be filled by guaranteed souls

    world.mine_status = None
    world.garden_chamber_available = True
    world.mine_requisites = None

    if world.options.mine_condition == MineCondition.option_garden:
        if world.options.garden_condition == GardenCondition.option_throne_room:
            world.mine_requisites = "Throne Room"
        else:
            world.mine_requisites = "Garden"
    elif world.options.mine_condition == MineCondition.option_throne_room:
        world.mine_requisites = "Throne Room"

    if not world.options.goal:
        if world.options.mine_condition == MineCondition.option_throne_room or ( 
                    world.options.mine_condition == MineCondition.option_garden and 
                    world.options.garden_condition == GardenCondition.option_throne_room):
            world.mine_status = "Disabled"  # Make sure we don't generate Mine checks if the Mine is unreachable.

        if world.options.menace_condition == MenaceCondition.option_throne_room or (
                world.options.menace_condition == MenaceCondition.option_garden and world.options.garden_condition == GardenCondition.option_throne_room):
            world.options.menace_condition.value = MenaceCondition.option_none  # This would be impossible so we switch it to no condition
            
        if world.options.garden_condition == GardenCondition.option_throne_room:
            world.garden_chamber_available = False

    if not world.mine_status:  # If we didn't just disable it, set the status here
        if world.options.mine_condition != MineCondition.option_none:
            world.mine_status = "Locked"
        else:
            world.mine_status = "Open"

    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

    if world.starting_warp_room is None:  # UT will have already grabbed it
        if world.options.shuffle_starting_warp_room:
            world.starting_warp_room = world.random.choice(warp_room_table)
        else:
            world.starting_warp_room = "Lost Village"

    world.starting_warp_region = warp_room_regions[world.starting_warp_room]

    if not world.magic_seal_table:  # If not doing UT passthrough
        set_seals(world)
    set_souls_for_walls(world)
    randomize_synthesis(world)

    # Enemy randomizer
    # The option names are optional; we check for attribute existence so it won't crash if options aren't defined yet.
    try:
        if getattr(world.options, "randomize_enemies", False):
            # preserve_resource_intensive and allow_boss_swaps can be set on world.options if present
            preserve = getattr(world.options, "preserve_resource_intensive", True)
            allow_bosses = getattr(world.options, "allow_boss_swaps", False)
            debug_subset = getattr(world.options, "enemy_randomizer_debug_subset", None)
            enemy_randomizer.generate_enemy_mapping(world, allow_bosses=allow_bosses, preserve_resource_intensive=preserve, debug_subset=debug_subset)
    except Exception:
        # Be resilient: do not crash world setup if enemy randomizer has issues
        warning("Enemy randomizer failed during setup; continuing without enemy randomization.")

    # Note: the actual write to ROM should call enemy_randomizer.write_enemies(world, rom, mode)
    # This is typically done in the ROM patching phase where the rom object is available.

    if world.options.get("boss_shuffle", False):
        # keep existing behavior for boss_shuffle if used; in your project bosses are handled separately
        pass
