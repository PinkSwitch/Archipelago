def shuffle_dungeons(world):
    # Is the dept. store a dungeon
    single_exit_dungeons = [
        "Giant Step",
        "Happy-Happy HQ",
        "Lilliput Steps",
        "Milky Well",
        "Gold Mine",
        "Moonside",
        "Monkey Caves",
        "Monotoli Building",
        "Magnet Hill",
        "Pink Cloud",
        "Dungeon Man",
        "Stonehenge Base",
        "Lumine Hall",
        "Fire Spring",
        "Sea of Eden"

    ]

    double_exit_dungeons = [
        "Arcade",
        "Brickroad Maze",
        "Rainy Circle",
        "Belch's Factory",
        "Pyramid"

        ]

    world.dungeon_connections = {
        "Arcade": "Arcade",
        "Giant Step": "Giant Step",
        "Happy-Happy HQ": "Happy-Happy HQ",
        "Lilliput Steps": "Lilliput Steps",
        "Belch's Factory": "Belch's Factory",
        "Milky Well": "Milky Well",
        "Gold Mine": "Gold Mine",
        "Moonside": "Moonside",
        "Monkey Caves": "Monkey Caves",
        "Monotoli Building": "Monotoli Building",
        "Magnet Hill": "Magnet Hill",
        "Pink Cloud": "Pink Cloud",
        "Dungeon Man": "Dungeon Man",
        "Stonehenge Base": "Stonehenge Base",
        "Brickroad Maze": "Brickroad Maze",
        "Rainy Circle": "Rainy Circle",
        "Pyramid": "Pyramid",
        "Lumine Hall": "Lumine Hall",
        "Fire Spring": "Fire Spring",
        "Sea of Eden": "Sea of Eden"
    }
    
    if world.options.magicant_mode:
        # Don't shuffle Magicant when it's important
        single_exit_dungeons.remove("Sea of Eden")

    shuffled_single_dungeons = single_exit_dungeons.copy()
    shuffled_double_dungeons = double_exit_dungeons.copy()

    if world.options.dungeon_shuffle:
        world.random.shuffle(shuffled_single_dungeons)
        world.random.shuffle(shuffled_double_dungeons)

    for index, entrance in enumerate(single_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_single_dungeons[index]

    for index, entrance in enumerate(double_exit_dungeons):
        world.dungeon_connections[entrance] = shuffled_double_dungeons[index]
    