import struct

def set_goal_triggers(world, condition, area):
    if condition == "throne_room":
        goal = {"Aguni Defeated"}
    elif condition == "garden":
        goal = {"Power of Darkness"}
    elif condition == "bosses":
        goal = {"Village Boss Clear", "Lab Boss Clear", "Chapel Boss Clear", "Inner Chapel Boss Clear", "Garden Boss Clear", "Guest House Boss Clear",
               "Subterranean Hell Boss Clear", "Tower Boss Clear", "Clock Tower Boss Clear", "Ruins Boss Clear", "Aguni Defeated", "Upper Guest House Boss Clear",
               "Mine Boss Clear", "Abyss Boss Clear"}
        if area == "Mine" or world.mine_status == "Disabled":
            goal.remove("Mine Boss Clear")
            goal.remove("Abyss Boss Clear")
        if not world.options.goal:
            goal.remove("Aguni Defeated")
    else:
        goal = None
    
    return goal

def write_goal_triggers(world, rom):
    goal_settings = [
        world.options.garden_condition,
        world.options.mine_condition,
        world.options.menace_condition
    ]

    trigger_keys = [
        "none",
        "throne_room",
        "garden",
        "bosses"
    ]

    goal_rule_order = [
        world.garden_triggers,
        world.mine_triggers,
        world.menace_triggers
    ]

    boss_flags = {
        "Village Boss Clear": 0x02,
        "Lab Boss Clear": 0x04,
        "Chapel Boss Clear": 0x08,
        "Inner Chapel Boss Clear": 0x10,
        "Garden Boss Clear": 0x20,
        "Guest House Boss Clear": 0x40,
        "Tower Boss Clear": 0x80,
        "Subterranean Hell Boss Clear": 0x0100,
        "Clock Tower Boss Clear": 0x0200,
        "Ruins Boss Clear": 0x0400,
        "Aguni Defeated": 0x0800,
        "Upper Guest House Boss Clear": 0x1000,
        "Mine Boss Clear": 0x2000,
        "Abyss Boss Clear": 0x8000  # 4000 is used for the Garden

    }

    for index, trigger in enumerate(goal_settings):
        condition = trigger.current_key
        rom.write_bytes(0x153F47 + 0x10 * index, bytearray([trigger_keys.index(condition)]))  # Write the actual condition key
        required_flags = 0
        if condition in ["bosses"]:  # More will be added to this in the future
            condition_list = goal_rule_order[index]
            for flag in condition_list:
                required_flags |= boss_flags[flag]
        rom.write_bytes(0x153F48 + 0x10 * index, struct.pack("H", required_flags))
        print(trigger_keys.index(condition))