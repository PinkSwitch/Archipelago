from typing import Dict, Set, NamedTuple, Optional
from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    default_count: Optional[int] = 1


item_table: Dict[str, ItemData] = {
    "Progressive Whip": ItemData("Whip Upgrades", 0x01, ItemClassification.progression, 4),
    "Laurels": ItemData("Consumables", 0x02, ItemClassification.progression),
    "Garlic": ItemData("Consumables", 0x03, ItemClassification.progression),
    "Silk Bag": ItemData("Consumables", 0x04, ItemClassification.useful),
    "Magic Cross": ItemData("Relics", 0x05, ItemClassification.progression),
    "Dagger": ItemData("Subweapons", 0x10, ItemClassification.useful),
    "Silver Knife": ItemData("Subweapons", 0x11, ItemClassification.useful),
    "Gold Knife": ItemData("Subweapons", 0x12, ItemClassification.useful),
    "Holy Water": ItemData("Subweapons", 0x13, ItemClassification.progression),
    "Diamond": ItemData("Subweapons", 0x14, ItemClassification.useful),
    "Sacred Flame": ItemData("Subweapons", 0x15, ItemClassification.useful),
    "Oak Stake": ItemData("Subweapons", 0x16, ItemClassification.progression),
    "Dracula's Rib": ItemData("Dracula Parts", 0x20, ItemClassification.progression),
    "Dracula's Heart": ItemData("Dracula Parts", 0x21, ItemClassification.progression),
    "Dracula's Eyeball": ItemData("Dracula Parts", 0x22, ItemClassification.progression),
    "Dracula's Nail": ItemData("Dracula Parts", 0x23, ItemClassification.progression),
    "Dracula's Ring": ItemData("Dracula Parts", 0x24, ItemClassification.progression),
    "White Crystal": ItemData("Relics", 0x25, ItemClassification.progression),
    "Blue Crystal": ItemData("Relics", 0x26, ItemClassification.progression),
    "Red Crystal": ItemData("Relics", 0x27, ItemClassification.progression),
    "Heart": ItemData("Hearts", 0x81, ItemClassification.filler, 0),
    "Half Heart": ItemData("Hearts", 0x85, ItemClassification.filler, 0),
    "Big Heart": ItemData("Hearts", 0x90, ItemClassification.filler, 0),


    "Dracula Defeated": ItemData("Events", None, ItemClassification.progression, 0)}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
