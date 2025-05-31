from typing import Dict, Set, NamedTuple, Optional
from BaseClasses import ItemClassification


class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: Optional[int] = 1


item_table: Dict[str, ItemData] = {
    "Dummy": ItemData("Test", 0x01, ItemClassification.progression),

}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories


filler_item_table = ["Dummy"]