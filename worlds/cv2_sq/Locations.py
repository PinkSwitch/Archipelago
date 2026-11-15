from typing import TYPE_CHECKING, Optional, NamedTuple, List

if TYPE_CHECKING:
    from . import CV2World


class LocationData(NamedTuple):
    region: str
    name: str
    is_event: Optional[bool] = False


def get_locations(world: "CV2World") -> List[LocationData]:
    location_table: List[LocationData] = [
        LocationData("Town of Jova", "Town of Jova: Right Building Merchant"),
        LocationData("Town of Jova", "Town of Jova: Merchant"),
        LocationData("Town of Jova", "Town of Jova: Left Building Merchant"),

        LocationData("Town of Alba", "Town of Alba: Hidden Wall Merchant"),
        LocationData("Town of Alba", "Town of Alba: Basement Merchant"),
        LocationData("Town of Alba", "Town of Alba: Crystal Trader"),

        LocationData("Storigoi Graveyard", "Storigoi Graveyard: Graveyard Duck"),

        LocationData("Town of Ondol", "Town of Ondol: Double Hidden Merchant"),
        LocationData("Town of Ondol", "Town of Ondol: Double Hidden Merchant"),

        LocationData("Deborah Cliff", "Deborah Cliff: Hidden Book"),

        LocationData("Bodley Mansion", "Bodley Mansion: Hidden Book"),
        LocationData("Bodley Mansion", "Bodley Mansion: Wall Merchant"),
        LocationData("Bodley Mansion", "Bodley Mansion: Evil Orb"),

        LocationData("Town of Doina", "Town of Doina: Basement Merchant"),

        LocationData("Uta Lower Road 2", "Uta Lower Road: Cursed Guy"),

        LocationData("Debious Woods", "Debious Woods: Hidden Book"),

        LocationData("Laruba Mansion", "Laruba Mansion: Salesman"),
        LocationData("Laruba Mansion", "Laruba Mansion: Beggar"),
        LocationData("Laruba Mansion", "Laruba Mansion: Camilla Drop"),
        LocationData("Laruba Mansion", "Laruba Mansion: Evil Orb"),

        LocationData("Camilla Cemetery", "Camilla Cemetery: Garlic Guy"),

        LocationData("Town of Aljiba", "Town of Aljiba: Basement Plus a Room Merchant"),
        LocationData("Town of Aljiba", "Town of Aljiba: Crystal Trader"),
        LocationData("Town of Aljiba", "Town of Aljiba: Hidden Book"),
        LocationData("Town of Aljiba", "Town of Aljiba: Basement Merchant"),

        LocationData("Lauber Mansion", "Lauber Mansion: Spikes Merchant"),
        LocationData("Lauber Mansion", "Lauber Mansion: Spikes Book"),
        LocationData("Lauber Mansion", "Lauber Mansion: Upper Book"),
        LocationData("Lauber Mansion", "Lauber Mansion: Evil Orb"),

        LocationData("Aljiba Woods 1", "Aljiba Woods: Hidden Book"),

        LocationData("Dabi's Path 2", "Dabi's Path: Hidden Item"),

        LocationData("Town of Veros", "Town of Veros: Basement Book"),
        LocationData("Town of Veros", "Town of Veros: Basement Merchant"),
        LocationData("Town of Veros", "Town of Veros: Hidden Wall Merchant"),

        LocationData("Berkeley Mansion", "Berkeley Mansion: Left Book"),
        LocationData("Berkeley Mansion", "Berkeley Mansion: Right Book"),
        LocationData("Berkeley Mansion", "Berkeley Mansion: Merchant"),
        LocationData("Berkeley Mansion", "Berkeley Mansion: Near Orb Book"),
        LocationData("Berkeley Mansion", "Berkeley Mansion: Evil Orb"),

        LocationData("Vrad Mountain 2", "Vrad Mountain: Hobo"),

        LocationData("Brahm's Mansion", "Brahm's Mansion: Top Left Book"),
        LocationData("Brahm's Mansion", "Brahm's Mansion: Spikes Book"),
        LocationData("Brahm's Mansion", "Brahm's Mansion: Merchant"),
        LocationData("Brahm's Mansion", "Brahm's Mansion: Death Drop"),
        LocationData("Brahm's Mansion", "Brahm's Mansion: Evil Orb"),


        LocationData("Castlevania", "Dracula Battle", True)
    ]

    return location_table
