from ..Options import PortraitShuffle

def portrait_shuffle(world) -> None:
    world.portrait_connections = {
        "City of Haze": "City of Haze",
        "13th Street": "13th Street",
        "Sandy Grave": "Sandy Grave",
        "Forgotten City": "Forgotten City",
        "Nation of Fools": "Nation of Fools",
        "Burnt Paradise": "Burnt Paradise",
        "Forest of Doom": "Forest of Doom",
        "Dark Academy": "Dark Academy",
        "Nest of Evil": "Nest of Evil"
    }

    if world.options.portrait_shuffle:
        portrait_pool = list(world.portrait_connections.values())
        world.random.shuffle(portrait_pool)
        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            portrait_pool.remove("Nest of Evil")

        world.portrait_connections = dict(zip(world.portrait_connections, portrait_pool))

        if world.options.portrait_shuffle != PortraitShuffle.option_add_nest_of_evil:
            world.portrait_connections["Nest of Evil"] = "Nest of Evil"  # Set this back to normal
        
        print(world.portrait_connections)
