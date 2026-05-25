from typing import NamedTuple
from rule_builder.rules import (CanReachLocation, OptionFilter, CanReachRegion,
                                And, Has, HasAll, HasFromListUnique, HasAny)
from rule_builder.field_resolvers import FromOption


class QuestData(NamedTuple):
    vanilla_reward: str
    required_items: list = []  # Which boss you need to clear to unlock the quest
    requires_filler_items: bool = False  # Whether this requires us to find filler items or not


cakes = ["Pancake", "Wheat Roll", "Sachertorte", "NY Cheesecake", "Mille-feuille", "Tarte au Poire",
         "Gateau Fraise", "Kugelhopf", "Green Tea Cake", "Gateau Marron", "Langues de Chat", "Financier",
         "Birthday Cake"]

cakes_notforsale = [
        "Pancake", "Tarte au Poire", "Gateau Fraise", "Kugelhopf", "Green Tea Cake", "Gateau Marron",
        "Langues de Chat", "Financier", "Birthday Cake"]

subweapons = ["Knife Subweapon", "Axe Subweapon", "Cross", "Holy Water", "Bible", "Javelin",
              "Ricochet Rock", "Boomerang", "Bwaka Knife", "Shuriken", "Yagyu Shuriken",
              "Discus", "Kunimitsu", "Kunai", "Paper Airplane", "Cream Pie", "Crossbow",
              "Dart", "Grenade", "Steel Ball", "Stonewall", "Offensive Form", "Defensive Form",
              "Taunt", "Wrecking Ball", "Rampage", "Knee Strike", "Aura Blast", "Rocket Slash"]

spells = ["Toad Morph", "Owl Morph", "Sanctuary", "Speed Up", "Berserker", "Eye for an Eye",
          "Clear Skies", "Time Stop", "Heal", "Cure Poison", "Cure Curse", "STR Boost",
          "CON Boost", "INT Boost", "MIND Boost", "LUCK Boost", "ALL Boost", "Gale Force",
          "Rock Riot", "Raging Fire", "Ice Fang", "Thunderbolt", "Spirit of Light",
          "Dark Rift", "Tempest", "Stone Circle", "Ice Needle", "Explosion", "Chain Lightning",
          "Piercing Beam", "Nightmare", "Summon Medusa", "Acidic Bubbles", "Hex", "Salamander",
          "Cocytus", "Thor's Bellow", "Summon Crow", "Summon Skeleton", "Summon Ghost", "Summon Gunman",
          "Summon Frog"]


quest_data = {
    "Quest: Preparations": QuestData("Lizard Tail"),
    "Quest: Supersonic Punch": QuestData("Bullet Punch", ["Ground Meat"]),
    "Quest: Ghosts of the Desert": QuestData("Bible"),
    "Quest: Defender of the Stairs": QuestData("Whip Skill 2"),
    "Quest: The Spinning Art": QuestData("Spinning Art"),
    "Quest: Art of the Zephyr": QuestData("Rocket Slash", ["Spinning Art"]),
    "Quest: Find the King of Birds": QuestData("Thief Ring", ["Time Stop"]),
    "Quest: Overcome the Curse": QuestData("Blessed Ring", ["Skull Ring"]),
    "Quest: The Statue's Tear": QuestData("Holy Water", ["Statue's Tear"]),
    "Quest: The Martial Art": QuestData("Martial Art"),
    "Quest: Holy Appearance": QuestData("Heal", ["Nun's Habit", "Nun's Robes", "Nun's Shoes"], True),
    "Quest: Number of Fortune": QuestData("LUCK Boost"),
    "Quest: Mental Training 1": QuestData("MP Max up"),
    "Quest: Mental Training 2": QuestData("MP Max up", ["Thick Glasses"], True),
    "Quest: The Spear of Legend": QuestData("Alucard's Spear", ["Javelin"], True),
    "Quest: Mental Training 3": QuestData("MP Max up", ["INT Boost"]),
    # "Quest: The Nest of Evil": QuestData("None", "Werewolf"),
    "Quest: Defeat the Ghoul King": QuestData("Immunity Ring"),
    "Quest: Abandon Greed": QuestData("Miser Ring"),
    "Quest: A Rank Hunter": QuestData("Royal Sword"),
    "Quest: Mental Training 4": QuestData("MP Max up", ["MIND Boost"]),
    "Quest: S Rank Hunter": QuestData("Undead Killer"),
    "Quest: The Gambler": QuestData("Gambler Glasses", ["Spade", "Heart", "Diamond", "Club", "Joker"], True),
    "Quest: Hands of the Clock": QuestData("Time Stop"),
    "Quest: Poison vs. Poison": QuestData("Assassin Blade", ["Moldy Bread", "Amanita", "Long Sword"], True),
    "Quest: Build Your Strength 1": QuestData("HP Max up", ["Beehive"]),
    "Quest: Build Your Strength 2": QuestData("HP Max up", ["New York Steak"], True),
    "Quest: The Lonely Stage": QuestData("Record Player"),
    "Quest: Build Your Strength 3": QuestData("HP Max up", cakes + ["Gold Ring"]),
    "Quest: Pray Before the Cross": QuestData("Cross"),
    "Quest: Build Your Strength 4": QuestData("HP Max up", ["CON Boost"]),
    "Quest: Lost Page": QuestData("Tome of Arms X", ["Tome of Arms p1", "Tome of Arms p2"]),
    "Quest: The Hundred Tasks": QuestData("Sage Ring"),
    "Quest: Master the Holy Power": QuestData("Grand Cruz", ["Bible", "Holy Water", "Cross"]),
    "Quest: Almighty": QuestData("Stellar Sword", subweapons, True),
    "Quest: The Great Sage": QuestData("Sorceress Crest", spells, True),
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
    spell_quests = ["Quest: Holy Apperance", "Quest: Number of Fortune", "Quest: Kill Gergoth",
                    "Quest: Hands of the Clock"]

    subweapon_quests = ["Quest: Ghosts of the Desert", "Quest: Art of the Zephyr", "Quest: The Statue's Tear",
                        "Quest: Pray Before the Cross"]

    holy_quests = ["Quest: The Statue's Tear", "Quest: Ghosts of the Desert", "Quest: Pray Before the Cross"]

    if "all" in selected_quests:
        for quest in quest_data:
            if quest not in ["Quest: Preparations", "Quest: The Nest of Evil"]:
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
        if quest.casefold() in selected_quests or quest.split(": ")[1].casefold() in selected_quests or quest in selected_quests:
            world.active_quests.append(quest)
        else:
            world.vanilla_quests.append(quest)

    if "Quest: Kill Gergoth" in world.active_quests and world.options.nest_of_evil_state == NestofEvil.option_removed:
        world.active_quests.remove("Quest: Kill Gergoth")  # This would be impossible, so remove it

    if "Quest: Preparations" in world.vanilla_quests:
        world.vanilla_quests.remove("Quest: Preparations")  # This should never be vanilla

    for quest in world.active_quests:
        world.quest_reward_pool.append(quest_data[quest].vanilla_reward)

        if quest.casefold() in excluded_quests or quest.split(": ")[1].casefold() in excluded_quests:
            excluded_quests.add(quest)

    # After adding the active quest rewards, REMOVE excluded quests from active
    # We do this here at this point so that it only excludes quests that are active in the first place
    if "all" in excluded_quests:
        world.active_quests = []

    if "simple" in excluded_quests:
        world.active_quests = [quest for quest in world.active_quests if quest not in simple_quests]

    if "requires item" in excluded_quests:
        world.active_quests = [quest for quest in world.active_quests if quest not in item_required_quests]

    if "defeat enemies" in excluded_quests:
        world.active_quests = [quest for quest in world.active_quests if quest not in enemy_quests]

    if "mastery" in excluded_quests:
        world.active_quests = [quest for quest in world.active_quests if quest not in mastery_quests]

    if "grindy" in excluded_quests:
        world.active_quests = [quest for quest in world.active_quests if quest not in grindy_quests]

    for quest in excluded_quests:
        if quest in world.active_quests:
            world.active_quests.remove(quest)

        if quest in quest_data:
            world.excluded_quests.append(quest)

    for quest in world.active_quests:
        world.important_quests.add(quest)

    if not world.options.unlock_all_quests:
        #  These are quests that require you to have completed a previous Quest.
        #  We want these to be logical if you need to complete them.
        if "Quest: The Great Sage" in world.important_quests:
            if world.options.nest_of_evil_state == NestofEvil.option_removed:
                spell_quests.remove("Quest: Kill Gergoth")
            for quest in spell_quests:
                if quest in world.vanilla_quests:
                    world.important_quests.add(quest)  # We need the rewards from these

        if "Quest: Almighty" in world.important_quests:
            for quest in subweapon_quests:
                if quest in world.vanilla_quests:
                    world.important_quests.add(quest)

        if "Quest: Master the Holy Power" in world.important_quests:
            for quest in holy_quests:
                if quest in world.vanilla_quests:
                    world.important_quests.add(quest)

        if "Quest: Art of the Zephyr" in world.important_quests:
            world.important_quests.add("Quest: The Spinning Art")

        if "Quest: S Rank Hunter" in world.important_quests:
            world.important_quests.add("Quest: A Rank Hunter")

        if "Quest: Mental Training 4" in world.important_quests:
            world.important_quests.add("Quest: Mental Training 3")

        if "Quest: Mental Training 3" in world.important_quests:
            world.important_quests.add("Quest: Mental Training 2")

        if "Quest: Mental Training 2" in world.important_quests:
            world.important_quests.add("Quest: Mental Training 1")

        if "Quest: Build Your Strength 4" in world.important_quests:
            world.important_quests.add("Quest: Build Your Strength 3")

        if "Quest: Build Your Strength 3" in world.important_quests:
            world.important_quests.add("Quest: Build Your Strength 2")

        if "Quest: Build Your Strength 2" in world.important_quests:
            world.important_quests.add("Quest: Build Your Strength 1")

    for quest in world.important_quests:
        world.quest_requirements.update(quest_data[quest].required_items)
    
    
def set_quest_rules(world):
    from ..Options import UnlockAllQuests, NestPortraits
    from ..Regions import has_change_cube, can_cast_spell
    set_rule = world.set_rule
    logic_spells = spells.copy()
    if world.options.exclude_owl_morph:
        logic_spells.remove("Owl Morph")  # This would be impossible so we remove it

    supersonic_punch_active = CanReachLocation("City of Haze: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                             Has("Ground Meat") | CanReachRegion("City of Haze"))
                             
    ghosts_of_desert_active = CanReachLocation("Great Stairway: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                            CanReachRegion("Sandy Grave - Upper Pyramid"))

    defender_stairs_active = CanReachLocation("Great Stairway: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                             CanReachRegion("Great Stairway - Staircases") | CanReachRegion("Entrance - Upper Area"))

    spinning_art_active = CanReachLocation("Sandy Grave: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)

    zephyr_art_active = And(CanReachLocation("Nation of Fools: Boss Room"), CanReachLocation("Quest: The Spinning Art"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                             Has("Spinning Art"))

    king_bird_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        CanReachRegion("Forgotten City") & (can_cast_spell & Has("Time Stop")))
    
    overcome_curse_active = CanReachLocation("Sandy Grave: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Skull Ring") | CanReachRegion("Entrance - Upper Area") | CanReachLocation("Tower of Death: Rampart Room") | CanReachRegion("Tower of Death - Ascent")) | CanReachRegion("Sandy Grave")

    statue_tear_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        CanReachRegion("Nation of Fools - Main") | Has("Statue's Tear"))

    martial_art_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    holy_appearance_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll("Nun's Habit", "Nun's Robes", "Nun's Shoes"))

    number_fortune_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_1_active = CanReachLocation("Tower of Death: Stella Item", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    mental_2_active = And(CanReachLocation("Tower of Death: Stella Item"), CanReachLocation("Quest: Mental Training 1"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Thick Glasses"))

    legend_spear_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Javelin") & Has("Portrait Clear", 2))

    mental_3_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Mental Training 2"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 5) | (Has("Portrait Clear", 3) & (Has("INT Boost") & has_change_cube)))

    ghoul_king_active = CanReachRegion("Master's Keep - Portrait Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        CanReachRegion("13th Street - Main"))

    abandon_greed_active = CanReachRegion("Master's Keep - Portrait Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True)
    a_rank_active = CanReachLocation("Forest of Doom: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 5))

    mental_4_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Mental Training 3"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 5) | (Has("Portrait Clear", 3) & (Has("MIND Boost") & has_change_cube)))

    s_rank_active = And(CanReachLocation("13th Street: Boss Room"), CanReachLocation("Quest: A Rank Hunter"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 7))

    the_gambler_active = CanReachLocation("Forest of Doom: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll("Spade", "Diamond", "Heart", "Club", "Joker"))

    clock_hands_active = CanReachLocation("Tower of Death: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Death Defeated"))

    poison_v_poison_active = CanReachLocation("Nation of Fools: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll("Moldy Bread", "Amanita", "Long Sword"))

    strength_1_active = CanReachLocation("Tower of Death: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Beehive") | CanReachRegion("Forest of Doom - Main"))

    strength_2_active = And(CanReachLocation("Tower of Death: Boss Room"), CanReachLocation("Quest: Build Your Strength 1"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("New York Steak"))

    lonely_stage_active = CanReachLocation("Dark Academy: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        CanReachRegion("Dark Academy - Main"))
                        
    strength_3_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Build Your Strength 2"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasFromListUnique(*cakes, count=5) | (HasAny(*cakes_notforsale) & CanReachRegion("City of Haze")) | (Has("Gold Ring") & CanReachRegion("City of Haze")))

    pray_cross_active = CanReachLocation("13th Street: Boss Room", options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
        CanReachRegion("13th Street - Main"))

    strength_4_active = And(CanReachLocation("Dark Academy: Boss Room"), CanReachLocation("Quest: Build Your Strength 3"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 5) | (Has("Portrait Clear", 3) & (Has("CON Boost") & has_change_cube)))
    lost_page_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll("Tome of Arms p1", "Tome of Arms p2"))

    hundred_tasks_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        Has("Portrait Clear", 5) | (Has("Portrait Clear", 4) & CanReachRegion("Nest of Evil")))

    holy_master_active = And(Has("Portrait Clear", FromOption(NestPortraits)), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll("Bible", "Cross", "Holy Water") & Has("Portrait Clear", 2))

    almighty_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll(*subweapons))

    great_sage_active = Has("Portrait Clear", FromOption(NestPortraits), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        HasAll(*logic_spells))
    kill_gergoth_active = And(Has("Portrait Clear", FromOption(NestPortraits)), CanReachRegion("Nest of Evil"), options=[OptionFilter(UnlockAllQuests, 0)], filtered_resolution=True) & (
                        CanReachRegion("Nest of Evil") & has_change_cube)

    quest_rules = {
        "Quest: Supersonic Punch": supersonic_punch_active,
        "Quest: Ghosts of the Desert": ghosts_of_desert_active,
        "Quest: Defender of the Stairs": defender_stairs_active,
        "Quest: The Spinning Art": spinning_art_active,
        "Quest: Art of the Zephyr": zephyr_art_active,
        "Quest: Find the King of Birds": king_bird_active,
        "Quest: Overcome the Curse": overcome_curse_active,
        "Quest: The Statue's Tear": statue_tear_active,
        "Quest: The Martial Art": martial_art_active,
        "Quest: Holy Appearance": holy_appearance_active,
        "Quest: Number of Fortune": number_fortune_active,
        "Quest: Mental Training 1": mental_1_active,
        "Quest: Mental Training 2": mental_2_active,
        "Quest: The Spear of Legend": legend_spear_active,
        "Quest: Mental Training 3": mental_3_active,
        "Quest: Defeat the Ghoul King": ghoul_king_active,
        "Quest: Abandon Greed": abandon_greed_active,
        "Quest: A Rank Hunter": a_rank_active,
        "Quest: Mental Training 4": mental_4_active,
        "Quest: S Rank Hunter": s_rank_active,
        "Quest: The Gambler": the_gambler_active,
        "Quest: Hands of the Clock": clock_hands_active,
        "Quest: Poison vs. Poison": poison_v_poison_active,
        "Quest: Build Your Strength 1": strength_1_active,
        "Quest: Build Your Strength 2": strength_2_active,
        "Quest: The Lonely Stage": lonely_stage_active,
        "Quest: Build Your Strength 3": strength_3_active,
        "Quest: Pray Before the Cross": pray_cross_active,
        "Quest: Build Your Strength 4": strength_4_active,
        "Quest: Lost Page": lost_page_active,
        "Quest: The Hundred Tasks": hundred_tasks_active,
        "Quest: Master the Holy Power": holy_master_active,
        "Quest: Almighty": almighty_active,
        "Quest: The Great Sage": great_sage_active,
        "Quest: Kill Gergoth": kill_gergoth_active
    }

    for quest in world.important_quests:
        if quest != "Quest: Preparations":
            set_rule(world.get_location(quest), quest_rules[quest])
            
