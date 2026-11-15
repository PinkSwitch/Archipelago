from typing import NamedTuple

location_ids = {
    "Town of Jova: Right Building Merchant": 0x01,
    "Town of Jova: Merchant": 0x02,
    "Town of Jova: Left Building Merchant": 0x03,

    "Town of Alba: Hidden Wall Merchant": 0x04,
    "Town of Alba: Basement Merchant": 0x05,
    "Town of Alba: Crystal Trader": 0x06,

    "Storigoi Graveyard: Graveyard Duck": 0x07,

    "Town of Ondol: Double Hidden Merchant": 0x08,
    "Town of Ondol: Basement Merchant": 0x09,

    "Deborah Cliff: Hidden Book": 0x0A,

    "Bodley Mansion: Hidden Book": 0x0B,
    "Bodley Mansion: Wall Merchant": 0x0C,
    "Bodley Mansion: Evil Orb": 0x0D,

    "Town of Doina: Basement Merchant": 0x0E,

    "Uta Lower Road: Cursed Guy": 0x0F,

    "Debious Woods: Hidden Book": 0x10,

    "Laruba Mansion: Salesman": 0x11,
    "Laruba Mansion: Beggar": 0x12,
    "Laruba Mansion: Camilla Drop": 0x13,
    "Laruba Mansion: Evil Orb": 0x14,

    "Camilla Cemetery: Garlic Guy": 0x15,

    "Town of Aljiba: Basement Plus a Room Merchant": 0x16,
    "Town of Aljiba: Crystal Trader": 0x17,
    "Town of Aljiba: Hidden Book": 0x18,
    "Town of Aljiba: Basement Merchant": 0x19,

    "Lauber Mansion: Spikes Merchant": 0x1A,
    "Lauber Mansion: Spikes Book": 0x1B,
    "Lauber Mansion: Upper Book": 0x1C,
    "Lauber Mansion: Evil Orb": 0x1D,

    "Aljiba Woods: Hidden Book": 0x1E,

    "Dabi's Path: Hidden Item": 0x1F,

    "Town of Veros: Basement Book": 0x20,
    "Town of Veros: Basement Merchant": 0x21,
    "Town of Veros: Hidden Wall Merchant": 0x22,

    "Berkeley Mansion: Left Book": 0x23,
    "Berkeley Mansion: Right Book": 0x24,
    "Berkeley Mansion: Merchant": 0x25,
    "Berkeley Mansion: Near Orb Book": 0x26,
    "Berkeley Mansion: Evil Orb": 0x27,

    "Vrad Mountain: Hobo": 0x28,

    "Brahm's Mansion: Top Left Book": 0x29,
    "Brahm's Mansion: Spikes Book": 0x2A,
    "Brahm's Mansion: Merchant": 0x2B,
    "Brahm's Mansion: Death Drop": 0x2C,
    "Brahm's Mansion: Evil Orb": 0x2D
}


def get_location_groups():
    location_groups = {
        "Town of Jova": set(),
        "Town of Veros": set(),
        "Town of Aljiba": set(),
        "Town of Alba": set(),
        "Town of Ondol": set(),
        "Town of Doina": set(),

        "Camilla Cemetery": set(),
        "Storigoi Graveyard": set(),
        "Deborah Cliff": set(),
        "Uta Lower Road": set(),
        "Debious Woods": set(),
        "Aljiba Woods": set(),
        "Dabi's Path": set(),
        "Vrad Mountain": set(),

        "Berkeley Mansion": set(),
        "Lauber Mansion": set(),
        "Brahm's Mansion": set(),
        "Bodley Mansion": set(),
        "Laruba Mansion": set()

    }

    for location in location_ids:
        group = location.split(":")[0]
        location_groups[group].add(location)

    return location_groups
