from BaseClasses import CollectionState


enemy_list = {
    "Northern Onett": 
        ["Coil Snake",
        "Runaway Dog",
        "Spiteful Crow"],

    "Onett":
        ["Pogo Punk",
         "Skate Punk",
         "Yes Man Junior",
         "Frank",
         "Frankystein Mark II"],
    
    "Giant Step":
        ["Attack Slug",
         "Black Antoid",
         "Rowdy Mouse",
         "Titanic Ant"],
    
    "Twoson":
        ["Cop",
        "Ramblin' Evil Mushroom",
        "Ctapin Strong",
        "Annoying Old Party Man",
        "Cranky Lady",
        "Mobile Sprout",
        "New Age Retro Hippie",
        "Unassuming Local Guy",
        "Everdred"]
}

combat_regions = [
    "Northern Onett",
    "Onett",
    "Giant Step",
    "Twoson",
    "Everdred's House"
    "Peaceful Rest Valley",
    "Happy-Happy Village",
    "Lilliput Steps",
    "Threed",
    "Winters",
    "Southern Winters"
    "Grapefruit Falls",
    "Belch's Factory",
    "Milky Well",
    "Dusty Dunes Desert",
    "Fourside",
    "Gold Mine",
    "Monkey Caves",
    "Monotoli Building",
    "Rainy Circle",
    "Summers",
    "Magnet Hill",
    "Pink Cloud",
    "Scaraba",
    "Pyramid",
    "Dungeon Man",
    "Deep Darkness",
    "Deep Darkness Darkness",
    "Stonehenge Base",
    "Lumine Hall",
    "Lost Underworld",
    "Fire Spring",
    "Magicant",
    "Cave of the Past",
    "Endgame"
]


def scale_enemies(world):
    state = world.multiworld.get_all_state(True)
    distances: Dict[str, int] = {}
    for region in world.multiworld.get_regions(world.player):
        if region.name != "Menu":
            connected, connection = state.path[region]
            distance = 0
            while connection is not None:
                if not any(connected == entrance.name for entrance in world.multiworld.get_entrances(world.player)):
                    distance += 1
                connected, connection = connection
            distances[region.name] = distance

    paths = state.path
    location_order = []
    for i, sphere in enumerate(world.multiworld.get_spheres()):
        locs = [loc for loc in sphere if loc.player == world.player and loc.parent_region.name in combat_regions and loc.parent_region.name not in location_order]
        regions = {loc.parent_region.name for loc in locs}
        location_order.extend(sorted(regions, key=lambda x: distances[x]))
    print(location_order)