

def generate_early(world) -> None:
    from .setup_game import setup_game
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Order of Ecclesia" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Order of Ecclesia"]
        world.options.required_villagers.value = passthrough["required_villagers"]
        world.options.starting_area.value = passthrough["starting_area"]
        world.options.remove_large_cavern.value = passthrough["remove_large_cavern"]
        world.options.remove_training_hall.value = passthrough["remove_training_hall"]

    setup_game(world)
    world.auth_id = world.random.getrandbits(32)