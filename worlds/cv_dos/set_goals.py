
def set_goal_triggers(world, condition, area):
    if condition == "throne_room":
        goal = {"Aguni Defeated"}
    elif condition == "garden":
        goal = {"Power of Darkness"}
    elif condition == "bosses":
        goal = {"Village Boss Clear", "Lab Boss Clear", "Chapel Boss Clear", "Inner Chapel Boss Clear", "Garden Boss Clear", "Guest House Boss Clear",
               "Subterranean Hell Boss Clear", "Tower Boss Clear", "Clock Tower Boss Clear", "Ruins Boss Clear", "Aguni Defeated", "Upper Guest House Boss Clear",
               "Mine Boss Clear", "Abyss Boss Clear"}
        if area == "Mine" or world.mine_condition == "Disabled":
            goal.remove("Mine Boss Clear")
            goal.remove("Abyss Boss Clear")
        if not world.options.goal:
            goal.remove("Aguni Defeated")

    
    return goal