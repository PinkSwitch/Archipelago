from typing import NamedTuple


class QuestData(NamedTuple):
    vanilla_reward: str  # We only use this to set vanilla quests
    villager: str  # Which Villager this quest is assigned to
    quest_number: int  # Which local quest number for this villager this is
    required_items: list = []  # Which items the player needs to complete this Quest

# TODO:
    # Add required items to the item pool. But make sure that we only add one guaranteed copy, so make
    # A local pool of ones that were already added. Check if it's not already in the iteem pool for like, cat col?
    # Some wy to tell when EARLIER quests are required. Also, Requesites need to be able to say the relevant quest is Important!
    # TODO! Update important quests with subquests if necessary
    # Logic
    # Remove Unwelcome Guest entirely if Large Cavern is off


quest_data = {
    "Quest: Running Out of Sage": QuestData("Nothing", "Abram", 1, ["Sage"]),
    "Quest: Medicinal Ingredients Needed": QuestData("Nothing", "Abram", 2, ["Chamomile", "Rue"]),
    "Quest: Mandrake is the Best Medicine": QuestData("Nothing", "Abram", 3, ["Sage", "Mandrake Root"]),
    "Quest: Unusual Medicine Components": QuestData("Nothing", "Abram", 4, ["Sage", "Merman Meat"]),

    "Quest: A Lucky Stone": QuestData("Nothing", "Laura", 1, ["Lapis Lazuli"]),
    "Quest: A Pleasant Accessory": QuestData("Nothing", "Laura", 2, ["Ruby", "Sapphire", "Emerald"]),
    "Quest: A Heartwarming Accessory": QuestData("Nothing", "Laura", 3, ["Diamond", "Onyx"]),
    "Quest: The Job of a Lifetime": QuestData("Royal Crown", "Laura", 4, ["Alexandrite"]),

    "Quest: Poor Preparation is Costly": QuestData("2400G", "Eugen", 1, ["Iron Ore"]),
    "Quest: What the Blacksmith Does Best": QuestData("3600G", "Eugen", 2, ["Silver Ore"]),
    "Quest: Work of the Finest Quality": QuestData("7200G", "Eugen", 3, ["Gold Ore"]),

    "Quest: Needs More Salt": QuestData("Corn Soup", "Aeon", 1, ["Salt"]),
    "Quest: I've Never Eaten That": QuestData("Killer Fish BBQ", "Aeon", 2, ["Raw Killer Fish"]),
    "Quest: Can't Cook Without Ingredients": QuestData("Thick Steak", "Aeon", 3, ["Tasty Meat"]),

    "Quest: Case of the Vicious Blight": QuestData("6000G", "Marcel", 1),
    "Quest: Case of the Demon Horse": QuestData("8000G", "Marcel", 2),
    "Quest: Case of the Hideous Snowman": QuestData("12000G", "Marcel", 3),

    "Quest: The Silent Violin": QuestData("Nothing", "George", 1, ["Horse Hair"]),
    "Quest: The Killing Scream": QuestData("Nothing", "George", 2),
    "Quest: Artists Can Be Selfish": QuestData("Nothing", "George", 3, ["Black Ink", "Eagle Feather"]),

    "Quest: Hide and Seek!": QuestData("Red Drops", "Serge", 1),
    "Quest: Show Me the Owl!": QuestData("Blue Drops", "Serge", 2, ["Fidelis Noctua"]),
    "Quest: Can't Catch Me!": QuestData("Green Drops", "Serge", 3),

    "Quest: Finding Tom": QuestData("Black Drops", "Anna", 1),
    "Quest: Mice Make for Good Eats": QuestData("Heart Earrings", "Anna", 2, ["Mouse"]),
    "Quest: Tom and Jewelry": QuestData("Ribbon", "Anna", 3, ["Cat Collar"]),

    "Quest: Making a Dress!": QuestData("Cotton Dress", "Monica", 1, ["Cotton Thread"]),
    "Quest: Silkworm's Tragedy": QuestData("Silk Dress", "Monica", 2, ["Silk Thread"]),
    "Quest: Is That Cashmere?": QuestData("Party Dress", "Monica", 3, ["Cashmere Thread"]),

    "Quest: Vicious Crows": QuestData("Mocha Eclair", "Irina", 1),
    "Quest: Do You Hear Howling?": QuestData("Tart Tatin", "Irina", 2),
    "Quest: An Unwelcome Guest": QuestData("Winged Boots", "Irina", 3),

    "Quest: A Beacon of Hope": QuestData("Garbo Hat", "Daniela", 1),
    "Quest: Important Resting Place": QuestData("Treasure Hat", "Daniela", 2),
    "Quest: Tragic Memories": QuestData("Dowsing Hat", "Daniela", 3),
}

simple_quests = {"Quest: Case of the Vicious Blight", "Quest: Case of the Demon Horse",
                 "Quest: Case of the Hideous Snowman", "Quest: The Killing Scream", "Quest: Hide and Seek!",
                 "Quest: Can't Catch Me!", "Quest: Finding Tom", "Quest: A Beacon of Hope",
                 "Quest: Important Resting Place", "Quest: Tragic Memories"}


def setup_quests(world) -> None:
    set_quests = world.options.randomized_quests.value
    set_exclusions = world.options.excluded_quests.value
    world.active_quests = get_filtered_quests(set_quests)
    world.excluded_quests = get_filtered_quests(set_exclusions)

    world.important_quests.update(world.active_quests)  # Auto mark all active quests
    world.important_quests.difference_update(world.excluded_quests)  # Remove exclusions from the Important quests
    if not world.options.unlock_all_quests:
        # Quests need to be done in order, so if a higher tier is active the lower tiers also need to be active
        quest_queue = list(world.important_quests)
        while quest_queue:
            quest = quest_queue.pop(0)
            if quest_data[quest].quest_number > 1:  # If this is a non-1 quest, we need to add all lower quests
                villager = quest_data[quest].villager
                quest_queue.extend(checked_quest for checked_quest in quest_data if quest_data[checked_quest].villager == villager and
                                   quest_data[checked_quest].quest_number < quest_data[quest].quest_number and checked_quest not in quest_queue)
            world.important_quests.add(quest)

    if world.options.remove_large_cavern:
        if "Quest: An Unwelcome Guest" in world.important_quests:
            world.important_quests.remove("Quest: An Unwelcome Guest")

        if "Quest: An Unwelcome Guest" in world.active_quests:
            world.active_quests.remove("Quest: An Unwelcome Guest")

    for quest in sorted(world.important_quests):
        if quest_data[quest].required_items:
            world.quest_items.extend(quest_data[quest].required_items)  # Add quest items to da list
        elif quest_data[quest].villager == "Marcel":
            world.quest_items.append("Camera")
        elif quest_data[quest].villager == "Daniela":
            world.quest_items.append("Sketch Book")
        elif quest == "Quest: The Killing Scream":
            world.quest_items.append("Phonograph")


def get_filtered_quests(quests) -> set[str]:
    filtered_quests = set()
    for quest in quest_data:
        data = quest_data[quest]
        if ((data.villager in quests) or  # Set all of that Villager's quests
                (quest in quests or quest.split(": ")[1] in quests) or  # Set the quest directly by name
                ("No Reward" in quests and data.vanilla_reward == "Nothing") or  # Filter no rewards
                ("Has Reward" in quests and data.vanilla_reward != "Nothing") or  # Filter rewards
                ("Requires Item" in quests and data.required_items) or  # Check for item requirements
                ("Defeat Enemies" in quests and data.villager == "Irina") or  # Only Irina has enemy quests
                ("Simple" in quests and quest in simple_quests) or
                ("All" in quests)):  # Set every quest active
            filtered_quests.add(quest)
    return filtered_quests


def set_quest_rules(world) -> None:
    from rule_builder.rules import HasAll, Has, CanReachRegion, HasAny, CanReachLocation
    for quest in quest_data:
        data = quest_data[quest]
        if quest in world.important_quests:
            rule = Has(data.villager)  # All quests need their respective villagers
            if data.required_items:
                rule &= HasAll(*set(data.required_items))  # Mark that we need all of the relevant items...
            #  The 3 family quests can only be done if all of the members are rescued
            if data.villager == "Serge":
                rule &= HasAll("Anna", "Irina")
            elif data.villager == "Anna":
                rule &= HasAll("Serge", "Irina")
            elif data.villager == "Irina":
                rule &= HasAll("Serge", "Anna")

            # Quests with specific rules
            # Using has map if basic region access for performance
            if quest == "Quest: Case of the Vicious Blight":
                rule &= (Has("Camera") & (CanReachRegion("Forsaken Cloister - Left") | CanReachRegion("Forsaken Cloister - Right") | CanReachRegion("Tymeo Mountains East"))) | Has("Photo 1")
            elif quest == "Quest: Case of the Demon Horse":
                rule &= Has("Camera") & HasAny("Photo 2", "Map: Argila Swamp")
            elif quest == "Quest: Case of the Hideous Snowman":
                rule &= (Has("Camera") & CanReachRegion("Tymeo Mountains East")) | Has("Photo 3")
            elif quest == "Quest: The Killing Scream":
                rule &= HasAll("Phonograph", "Map: Monastery")
            elif quest == "Quest: Finding Tom":
                rule &= CanReachRegion("Tristis Pass Waterfall")
            elif quest == "Quest: Vicious Crows":
                rule &= Has("Map: Tymeo Mountains")
            elif quest == "Quest: Do You Hear Howling?":
                rule &= Has("Map: Oblivion Ridge")
            elif quest == "Quest: An Unwelcome Guest":
                rule &= CanReachRegion("Large Cavern")
            elif quest == "Quest: A Beacon of Hope":
                rule &= (Has("Sketch Book") & CanReachRegion("Lighthouse Post-Boss")) | Has("Lighthouse Art")
            elif quest == "Quest: Important Resting Place":
                rule &= HasAll("Map: Tristis Pass", "Sketch Book") | Has("Waterfall Art")
            elif quest == "Quest: Tragic Memories":
                rule &= (Has("Sketch Book") & CanReachRegion("Oblivion Ridge Beyond Boss") | Has("Church Art"))

            # If not all quests are unlocked, earlier quests also need to be reached
            if not world.options.unlock_all_quests:
                if data.quest_number > 1:
                    previous_quest = [quest for quest in quest_data if quest_data[quest].villager == data.villager
                                      and quest_data[quest].quest_number == data.quest_number - 1][0]
                    rule &= CanReachLocation(previous_quest)  # Get this villager's previous quest
            world.set_rule(world.get_location(quest), rule)
