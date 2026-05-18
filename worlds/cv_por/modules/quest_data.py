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
    "Quest: Mental Training 1": QuestData("MP Max up"),
    "Quest: Mental Training 2": QuestData("MP Max up"),
    "Quest: The Spear of Legend": QuestData("Alucard's Spear"),
    "Quest: Mental Training 3": QuestData("MP Max up"),
    # "Quest: The Nest of Evil": QuestData("None"),
    "Quest: Defeat the Ghoul King": QuestData("Immunity Ring"),
    "Quest: Abandon Greed": QuestData("Miser Ring"),
    "Quest: A Rank Hunter": QuestData("Royal Sword"),
    "Quest: Mental Training 4": QuestData("MP Max up"),
    "Quest: S Rank Hunter": QuestData("Undead Killer"),
    "Quest: The Gambler": QuestData("Gambler Glasses"),
    "Quest: Hands of the Clock": QuestData("Time Stop"),
    "Quest: Poison vs. Poison": QuestData("Assassin Blade"),
    "Quest: Build Your Strength 1": QuestData("HP Max up"),
    "Quest: Build Your Strength 2": QuestData("HP Max up"),
    "Quest: The Lonely Stage": QuestData("Record Player"),
    "Quest: Build Your Strength 3": QuestData("HP Max up"),
    "Quest: Pray Before the Cross": QuestData("Cross"),
    "Quest: Build Your Strength 4": QuestData("HP Max up"),
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
    from ..Options import NestofEvil
    selected_quests = {quest.casefold() for quest in world.options.randomized_quests.value}
    excluded_quests = {quest.casefold() for quest in world.options.excluded_quests.value}

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
        else:
            world.vanilla_quests.append(quest)

    world.vanilla_quests.remove("Quest: Preparations")  # This should never be vanilla

    for quest in world.active_quests:
        world.quest_reward_pool.append(quest_data[quest].vanilla_reward)

        if quest.casefold() in excluded_quests or quest.split(": ")[1].casefold() in excluded_quests:
            excluded_quests.add(quest)

    if "Quest: Kill Gergoth" in world.active_quests and world.options.nest_of_evil_state == NestofEvil.option_removed:
        world.active_quests.remove("Quest: Kill Gergoth")  # This would be impossible, so remove it

    # After adding the active quest rewards, REMOVE excluded quests from active
    # We do this here at this point so that it only excludes quests that are active in the first place
    if "all" in excluded_quests:
        world.active_quests = []

    if "simple" in selected_quests:
        world.active_quests -= simple_quests

    if "requires item" in selected_quests:
        world.active_quests -= item_required_quests

    if "defeat enemies" in selected_quests:
        world.active_quests -= enemy_quests

    if "mastery" in selected_quests:
        world.active_quests -= mastery_quests

    if "grindy" in selected_quests:
        world.active_quests -= grindy_quests

    for quest in excluded_quests:
        if quest in world.active_quests:
            world.active_quests.remove(quest)

        if quest in quest_data:
            world.excluded_quests.append(quest)
    