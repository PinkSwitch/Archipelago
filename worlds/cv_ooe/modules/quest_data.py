from typing import NamedTuple


class QuestData(NamedTuple):
    vanilla_reward: str  # We only use this to set vanilla quests
    villager: str  # Which Villager this quest is assigned to
    required_items: list = []  # Which items the player needs to complete this Quest

# TODO:
    # Add required items to the item pool. But make sure that we only add one guaranteed copy, so make
    # A local pool of ones that were already added. Check if it's not already in the iteem pool for like, cat col?

quest_data = {
    "Quest: Running Out of Sage": QuestData("Nothing", "Abram", ["Sage"]),
    "Quest: Medicinal Ingredients Needed": QuestData("Nothing", "Abram", ["Chamomile", "Rue"]),
    "Quest: Mandrake is the Best Medicine": QuestData("Nothing", "Abram", ["Sage", "Mandrake Root"]),
    "Quest: Unusual Medicine Components": QuestData("Nothing", "Abram", ["Sage", "Merman Meat"]),

    "Quest: A Lucky Stone": QuestData("Nothing", "Laura", ["Lapis Lazuli"]),
    "Quest: A Pleasant Accessory": QuestData("Nothing", "Laura", ["Ruby", "Sapphire", "Emerald"]),
    "Quest: A Heartwarming Accessory": QuestData("Nothing", "Laura", ["Diamond", "Onyx"]),
    "Quest: The Job of a Lifetime": QuestData("Royal Crown", "Laura", ["Alexandrite"]),

    "Quest: Poor Preparation is Costly": QuestData("2400G", "Eugen", ["Iron Ore"]),
    "Quest: What the Blacksmith Does Best": QuestData("3600G", "Eugen", ["Silver Ore"]),
    "Quest: Work of the Finest Quality": QuestData("7200G", "Eugen", ["Gold Ore"]),

    "Quest: Needs More Salt": QuestData("Corn Soup", "Aeon", ["Salt"]),
    "Quest: I've Never Eaten That": QuestData("Killer Fish BBQ", "Aeon", ["Raw Killer Fish"]),
    "Quest: Can't Cook Without Ingredients": QuestData("Thick Steak", "Aeon", ["Tasty Meat"]),

    "Quest: Case of the Vicious Blight": QuestData("6000G", "Marcel"),
    "Quest: Case of the Demon Horse": QuestData("8000G", "Marcel"),
    "Quest: Case of the Hideous Snowman": QuestData("12000G", "Marcel"),

    "Quest: The Silent Violin": QuestData("Nothing", "George", ["Horse Hair"]),
    "Quest: The Killing Scream": QuestData("Nothing", "George"),
    "Quest: Artists Can Be Selfish": QuestData("Nothing", "George", ["Black Ink", "Eagle Feather"]),

    "Quest: Hide and Seek!": QuestData("Red Drops", "Serge"),
    "Quest: Show Me the Owl!": QuestData("Blue Drops", "Serge", ["Fidelis Noctua"]),
    "Quest: Can't Catch Me!": QuestData("Green Drops", "Serge"),

    "Quest: Finding Tom": QuestData("Black Drops", "Anna"),
    "Quest: Mice Make for Good Eats": QuestData("Heart Earrings", "Anna", ["Mouse"]),
    "Quest: Tom and Jewelry": QuestData("Ribbon", "Anna", ["Cat Collar"]),

    "Quest: Making a Dress!": QuestData("Cotton Dress", "Monica", ["Cotton Thread"]),
    "Quest: Silkworm's Tragedy": QuestData("Silk Dress", "Monica", ["Silk Thread"]),
    "Quest: Is That Cashmere?": QuestData("Party Dress", "Monica", ["Cashmere Thread"]),

    "Quest: Vicious Crows": QuestData("Mocha Eclair", "Irina"),
    "Quest: Do You Hear Howling?": QuestData("Tart Tatin", "Irina"),
    "Quest: An Unwelcome Guest": QuestData("Winged Boots", "Irina"),

    "Quest: A Beacon of Hope": QuestData("Garbo Hat", "Daniela"),
    "Quest: Important Resting Place": QuestData("Treasure Hat", "Daniela"),
    "Quest: Tragic Memories": QuestData("Dowsing Hat", "Daniela"),
}