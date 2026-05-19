
from typing import NamedTuple
from rule_builder.rules import CanReachLocation, OptionFilter, CanReachRegion, And, Has, HasAll
from rule_builder.field_resolvers import FromOption

class QuestData(NamedTuple):
    vanilla_reward: str
    clear_requirement: str  # Which boss you need to clear to unlock the quest


quest_data = {
    "Quest: Preparations": QuestData("Lizard Tail", "None"),
    "Quest: Supersonic Punch": QuestData("Bullet Punch", "Dullahan"),
    "Quest: Ghosts of the Desert": QuestData("Bible", "Keremet"),
    "Quest: Defender of the Stairs": QuestData("Whip Skill 2", "Keremet"),
    "Quest: The Spinning Art": QuestData("Spinning Art", "Astarte"),
    "Quest: Art of the Zephyr": QuestData("Rocket Slash", "Legion"),
    "Quest: Find the King of Birds": QuestData("Thief Ring", "The Creature"),
    "Quest: Overcome the Curse": QuestData("Blessed Ring", "Astarte"),
    "Quest: The Statue's Tear": QuestData("Holy Water", "Legion"),
    "Quest: The Martial Art": QuestData("Martial Art", "Legion"),
    "Quest: Holy Appearance": QuestData("Heal", "Stella"),
    "Quest: Number of Fortune": QuestData("LUCK Boost", "Stella"),
    "Quest: Mental Training 1": QuestData("MP Max up", "Stella"),
    "Quest: Mental Training 2": QuestData("MP Max up", "Stella"),
    "Quest: The Spear of Legend": QuestData("Alucard's Spear", "The Creature"),
    "Quest: Mental Training 3": QuestData("MP Max up", "The Creature"),
    # "Quest: The Nest of Evil": QuestData("None", "Werewolf"),
    "Quest: Defeat the Ghoul King": QuestData("Immunity Ring", "Sisters"),
    "Quest: Abandon Greed": QuestData("Miser Ring", "Sisters"),
    "Quest: A Rank Hunter": QuestData("Royal Sword", "Dagon"),
    "Quest: Mental Training 4": QuestData("MP Max up", "The Creature"),
    "Quest: S Rank Hunter": QuestData("Undead Killer", "Werewolf"),
    "Quest: The Gambler": QuestData("Gambler Glasses", "Dagon"),
    "Quest: Hands of the Clock": QuestData("Time Stop", "Death"),
    "Quest: Poison vs. Poison": QuestData("Assassin Blade", "Legion"),
    "Quest: Build Your Strength 1": QuestData("HP Max up", "Death"),
    "Quest: Build Your Strength 2": QuestData("HP Max up", "Death"),
    "Quest: The Lonely Stage": QuestData("Record Player", "The Creature"),
    "Quest: Build Your Strength 3": QuestData("HP Max up", "The Creature"),
    "Quest: Pray Before the Cross": QuestData("Cross", "Werewolf"),
    "Quest: Build Your Strength 4": QuestData("HP Max up", "The Creature"),
    "Quest: Lost Page": QuestData("Tome of Arms X", "None"),
    "Quest: The Hundred Tasks": QuestData("Sage Ring", "None"),
    "Quest: Master the Holy Power": QuestData("Grand Cruz", "None"),
    "Quest: Almighty": QuestData("Stellar Sword", "None"),
    "Quest: The Great Sage": QuestData("Sorceress Crest", "None"),
    "Quest: Kill Gergoth": QuestData("Cocytus", "None")
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
    
    
def set_quest_rules(world):
    from ..Options import UnlockAllQuests, NestPortraits
    set_rule = world.set_rule

    supersonic_punch_active = CanReachLocation("City of Haze: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    ghosts_of_desert_active = CanReachLocation("Great Stairway: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    defender_stairs_active = CanReachLocation("Great Stairway: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    spinning_art_active = CanReachLocation("Sandy Grave: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    zephyr_art_active = And(CanReachLocation("Nation of Fools: Boss Room"), CanReachLocation("Quest: The Spinning Art"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) 
    king_bird_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    overcome_curse_active = CanReachLocation("Sandy Grave: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    statue_tear_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    martial_art_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    holy_appearance_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    number_fortune_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_1_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_2_active = And(CanReachLocation("Tower of Death: Stella Item"), CanReachLocation("Quest: Mental Training 1"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)   # Mental 1
    legend_spear_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_3_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Mental Training 2"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)  # Mental 2
    ghoul_king_active = CanReachRegion("Master's Keep - Portrait Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    abandon_greed_active = CanReachRegion("Master's Keep - Portrait Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    a_rank_active = CanReachLocation("Forest of Doom: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_4_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Mental Training 3"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    s_rank_active = And(CanReachLocation("13th Street: Boss Room"), CanReachLocation("Quest: A Rank Hunter"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    the_gambler_active = CanReachLocation("Forest of Doom: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    clock_hands_active = CanReachLocation("Tower of Death: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    poison_v_poison_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    strength_1_active = CanReachLocation("Tower of Death: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    
    strength_2_active = And(CanReachLocation("Tower of Death: Boss Room"), CanReachLocation("Quest: Build Your Strength 1"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    lonely_stage_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    strength_3_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Build Your Strength 2"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    pray_cross_active = CanReachLocation("13th Street: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    strength_4_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Build Your Strength 3"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)

    lost_page_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    hundred_tasks_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    holy_master_active = And(Has("Portrait Clear", FromOption(NestPortraits)),
                             HasAll("Cross", "Holy Water", "Bible"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    almighty_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    great_sage_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    kill_gergoth_active = And(Has("Portrait Clear", FromOption(NestPortraits)), CanReachRegion("Nest of Evil"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    
    set_rule(world.get_location("Quest: Supersonic Punch"), supersonic_punch_active)
    set_rule(world.get_location("Quest: Ghosts of the Desert"), ghosts_of_desert_active)
    set_rule(world.get_location("Quest: Defender of the Stairs"), defender_stairs_active)
    set_rule(world.get_location("Quest: The Spinning Art"), spinning_art_active)
    set_rule(world.get_location("Quest: Art of the Zephyr"), zephyr_art_active)
    set_rule(world.get_location("Quest: Find the King of Birds"), king_bird_active)
    set_rule(world.get_location("Quest: Overcome the Curse"), overcome_curse_active)
    set_rule(world.get_location("Quest: The Statue's Tear"), statue_tear_active)
    set_rule(world.get_location("Quest: The Martial Art"), martial_art_active)
    set_rule(world.get_location("Quest: Holy Appearance"), holy_appearance_active)
    set_rule(world.get_location("Quest: Number of Fortune"), number_fortune_active)
    set_rule(world.get_location("Quest: Mental Training 1"), mental_1_active)
    set_rule(world.get_location("Quest: Mental Training 2"), mental_2_active)
    set_rule(world.get_location("Quest: The Spear of Legend"), legend_spear_active)
    set_rule(world.get_location("Quest: Mental Training 3"), mental_3_active)
    set_rule(world.get_location("Quest: Defeat the Ghoul King"), ghoul_king_active)
    set_rule(world.get_location("Quest: Abandon Greed"), abandon_greed_active)
    set_rule(world.get_location("Quest: A Rank Hunter"), a_rank_active)
    set_rule(world.get_location("Quest: Mental Training 4"), mental_4_active)
    set_rule(world.get_location("Quest: S Rank Hunter"), s_rank_active)
    set_rule(world.get_location("Quest: The Gambler"), the_gambler_active)
    set_rule(world.get_location("Quest: Hands of the Clock"), clock_hands_active)
    set_rule(world.get_location("Quest: Poison vs. Poison"), poison_v_poison_active)
    set_rule(world.get_location("Quest: Build Your Strength 1"), strength_1_active)
    set_rule(world.get_location("Quest: Build Your Strength 2"), strength_2_active)
    set_rule(world.get_location("Quest: The Lonely Stage"), lonely_stage_active)
    set_rule(world.get_location("Quest: Build Your Strength 3"), strength_3_active)
    set_rule(world.get_location("Quest: Pray Before the Cross"), pray_cross_active)
    set_rule(world.get_location("Quest: Build Your Strength 4"), strength_4_active)
    set_rule(world.get_location("Quest: Lost Page"), lost_page_active)
    set_rule(world.get_location("Quest: The Hundred Tasks"), hundred_tasks_active)
    set_rule(world.get_location("Quest: Master the Holy Power"), holy_master_active)
    set_rule(world.get_location("Quest: Almighty"), almighty_active)
    set_rule(world.get_location("Quest: The Great Sage"), great_sage_active)
    set_rule(world.get_location("Quest: Kill Gergoth"), kill_gergoth_active)
