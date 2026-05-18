from typing import NamedTuple


class QuestData(NamedTuple):
    vanilla_reward: str


quest_data = {
    "Quest: Preparations": QuestData("Lizard Tail"),
    "Quest: Supersonic Punch": QuestData("Bullet Punch"),
    "Quest: Ghosts of the Desert": QuestData("Bible"),
    "Quest: Defender of the Stairs": QuestData("Whip Skill 2"),
    "Quest: The Spinning Art": QuestData("Spinning Art"),
    "Quest: Art of the Zephyr": QuestData("Rocket Slash"),
    "Quest: Find the King of Birds": QuestData("Thief Ring"),
    "Quest: Overcome the Curse": QuestData("Blessed Ring"),
    "Quest: The Statue's Tear": QuestData("Holy Water"),
    "Quest: The Martial Art": QuestData("Martial Art"),
    "Quest: Holy Appearance": QuestData("Heal"),
    "Quest: Number of Fortune": QuestData("LUCK Boost"),
    "Quest: Mental Training 1": QuestData("MP Max Up"),
    "Quest: Mental Training 2": QuestData("MP Max Up"),
    "Quest: The Spear of Legend": QuestData("Alucard's Spear"),
    "Quest: Mental Training 3": QuestData("MP Max Up"),
    "Quest: The Nest of Evil": QuestData("None"),
    "Quest: Defeat the Ghoul King": QuestData("Immunity Ring"),
    "Quest: Abandon Greed": QuestData("Miser Ring"),
    "Quest: A Rank Hunter": QuestData("Royal Sword"),
    "Quest: Mental Training 4": QuestData("MP Max Up"),
    "Quest: S Rank Hunter": QuestData("Undead Killer"),
    "Quest: The Gambler": QuestData("Gambler Glasses"),
    "Quest: Hands of the Clock": QuestData("Time Stop"),
    "Quest: Poison vs. Poison": QuestData("Assassin Blade"),
    "Quest: Build Your Strength 1": QuestData("HP Max Up"),
    "Quest: Build Your Strength 2": QuestData("HP Max Up"),
    "Quest: The Lonely Stage": QuestData("Record Player"),
    "Quest: Build Your Strength 3": QuestData("HP Max Up"),
    "Quest: Pray Before the Cross": QuestData("Cross"),
    "Quest: Build Your Strength 4": QuestData("HP Max Up"),
    "Quest: Lost Page": QuestData("Tome of Arms X"),
    "Quest: The Hundred Tasks": QuestData("Sage Ring"),
    "Quest: Master the Holy Power": QuestData("Grand Cruz"),
    "Quest: Almighty": QuestData("Stellar Sword"),
    "Quest: The Great Sage": QuestData("Sorceress Crest"),
    "Quest: Kill Gergoth": QuestData("Cocytus")
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
    # World.vanilla_quests?
    # Handle excluded quests
    for quest in world.active_quests:
        world.quest_reward_pool.append(quest_data[quest].vanilla_reward)
    print(world.quest_reward_pool)
