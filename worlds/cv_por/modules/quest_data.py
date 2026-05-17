from typing import NamedTuple


class QuestData(NamedTuple):
    pointer: int


quest_data = {
    "Quest: Preparations": QuestData(0),
    "Quest: Supersonic Punch": QuestData(0),
    "Quest: Ghosts of the Desert": QuestData(0),
    "Quest: Defender of the Stairs": QuestData(0),
    "Quest: The Spinning Art": QuestData(0),
    "Quest: Art of the Zephyr": QuestData(0),
    "Quest: Find the King of Birds": QuestData(0),
    "Quest: Overcome the Curse": QuestData(0),
    "Quest: The Statue's Tear": QuestData(0),
    "Quest: The Martial Art": QuestData(0),
    "Quest: Holy Appearance": QuestData(0),
    "Quest: Number of Fortune": QuestData(0),
    "Quest: Mental Training 1": QuestData(0),
    "Quest: Mental Training 2": QuestData(0),
    "Quest: The Spear of Legend": QuestData(0),
    "Quest: Mental Training 3": QuestData(0),
    "Quest: The Nest of Evil": QuestData(0),
    "Quest: Defeat the Ghoul King": QuestData(0),
    "Quest: Abandon Greed": QuestData(0),
    "Quest: A Rank Hunter": QuestData(0),
    "Quest: Mental Training 4": QuestData(0),
    "Quest: S Rank Hunter": QuestData(0),
    "Quest: The Gambler": QuestData(0),
    "Quest: Hands of the Clock": QuestData(0),
    "Quest: Poison vs. Poison": QuestData(0),
    "Quest: Build Your Strength 1": QuestData(0),
    "Quest: Build Your Strength 2": QuestData(0),
    "Quest: The Lonely Stage": QuestData(0),
    "Quest: Build Your Strength 3": QuestData(0),
    "Quest: Pray Before the Cross": QuestData(0),
    "Quest: Build Your Strength 4": QuestData(0),
    "Quest: Lost Page": QuestData(0),
    "Quest: The Hundred Tasks": QuestData(0),
    "Quest: Master the Holy Power": QuestData(0),
    "Quest: Almighty": QuestData(0),
    "Quest: The Great Sage": QuestData(0),
    "Quest: Kill Gergoth": QuestData(0)
}

simple_quests = {
    "Quest: The Spinning Art",
    "Quest: Overcome the Curse",
    "Quest: The Martial Art",
    "Quest: Number of Fortune",
    "Quest: Mental Training 1",
    "Quest: Abandon Greed",
    "Quest: Hands of the Clock",
    "Quest: The Lonely Stage",
    "Quest: Pray Before the Cross"
}

item_required_quests = {
    "Quest: Supersonic Punch",
    "Quest: Art of the Zephyr",
    "Quest: The Statue's Tear",
    "Quest: Holy Appearance",
    "Quest: Mental Training 2",
    "Quest: The Gambler",
    "Quest: Poison vs. Poison",
    "Quest: Build Your Strength 1",
    "Quest: Build Your Strength 2",
    "Quest: Build Your Strength 3",
    "Quest: Lost Page"
}

enemy_quests = {
    "Quest: Ghosts of the Desert",
    "Quest: Defender of the Stairs",
    "Quest: Find the King of Birds",
    "Quest: Defeat the Ghoul King",
    "Quest: Kill Gergoth"
}

mastery_quests = {
    "Quest: The Spear of Legend",
    "Quest: Master the Holy Power"
}

grindy_quests = {
    "Quest: Mental Training 3",
    "Quest: A Rank Hunter",
    "Quest: Mental Training 4",
    "Quest: S Rank Hunter",
    "Quest: Strength Training 4",
    "Quest: The Hundred Tasks",
    "Quest: Master the Holy Power",
    "Quest: Almighty",
    "Quest: The Great Sage"
}


def setup_quests(world):
    selected_quests = {quest.casefold() for quest in world.options.randomized_quests.value}
    if "all" in selected_quests:
        for quest in quest_data:
            if quest not in ["Quest: Preparatations", "Quest: The Nest of Evil"]:
                selected_quests.add(quest)

    if "simple" in selected_quests:
        selected_quests |= simple_quests

    if "requires item" in selected_quests:
        selected_quests |= item_required_quests

    if "defeat enemies" in selected_quests:
        selected_quests |= enemy_quests

    if "mastery" in selected_quests:
        selected_quests |= mastery_quests

    if "grindy" in selected_quests:
        selected_quests |= grindy_quests

    for quest in quest_data:
        if quest.casefold() in selected_quests or quest.split(": ")[1].casefold() in selected_quests:
            world.active_quests.append(quest)
    print(world.active_quests)
