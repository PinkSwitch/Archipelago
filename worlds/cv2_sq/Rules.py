from rule_builder.rules import HasAll, HasAny, Has, OptionFilter
from .Options import InclusiveWhtCrystal


def set_location_rules(world):
    set_rule = world.set_rule
    world.set_completion_rule(Has("Dracula Defeated"))

    set_rule(world.get_location("Town of Veros: Hidden Wall Merchant"), HasAny("Holy Water", "Dracula's Nail"))
    set_rule(world.get_location("Town of Veros: Basement Book"), Has("Holy Water"))
    set_rule(world.get_location("Town of Veros: Basement Merchant"), Has("Holy Water"))

    set_rule(world.get_location("Berkeley Mansion: Left Book"),
             Has("White Crystal") & HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))

    set_rule(world.get_location("Berkeley Mansion: Right Book"),
             Has("White Crystal") & HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))

    set_rule(world.get_location("Berkeley Mansion: Merchant"), Has("White Crystal"))

    set_rule(world.get_location("Berkeley Mansion: Near Orb Book"),
             Has("White Crystal") & HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))

    set_rule(world.get_location("Berkeley Mansion: Evil Orb"), Has("White Crystal") & Has("Oak Stake"))

    set_rule(world.get_location("Dabi's Path: Hidden Item"), HasAny("Holy Water", "Dracula's Nail"))

    set_rule(world.get_location("Aljiba Woods: Hidden Book"), HasAny("Holy Water", "Dracula's Eyeball"))

    set_rule(world.get_location("Lauber Mansion: Spikes Book"),
             HasAny("Holy Water", "Dracula's Eyeball", "Dracula's Nail") & (Has("White Crystal") | OptionFilter(InclusiveWhtCrystal, False)))

    set_rule(world.get_location("Lauber Mansion: Upper Book"),
             HasAny("Holy Water", "Dracula's Eyeball", "Dracula's Nail"))

    set_rule(world.get_location("Lauber Mansion: Evil Orb"), Has("Oak Stake"))

    set_rule(world.get_location("Town of Aljiba: Basement Merchant"), Has("Holy Water"))
    set_rule(world.get_location("Town of Aljiba: Basement Plus a Room Merchant"), Has("Holy Water"))
    set_rule(world.get_location("Town of Aljiba: Crystal Trader"), Has("White Crystal"))
    set_rule(world.get_location("Town of Aljiba: Hidden Book"), Has("Holy Water"))

    set_rule(world.get_location("Camilla Cemetery: Garlic Guy"), Has("Garlic"))

    set_rule(world.get_location("Brahm's Mansion: Top Left Book"), Has("Holy Water"))
    set_rule(world.get_location("Brahm's Mansion: Spikes Book"), HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))
    set_rule(world.get_location("Brahm's Mansion: Evil Orb"), Has("Oak Stake"))

    set_rule(world.get_location("Town of Alba: Hidden Wall Merchant"), HasAny("Holy Water", "Dracula's Nail"))
    set_rule(world.get_location("Town of Alba: Basement Merchant"), Has("Holy Water"))
    set_rule(world.get_location("Town of Alba: Crystal Trader"), Has("Blue Crystal"))

    set_rule(world.get_location("Storigoi Graveyard: Graveyard Duck"), Has("Garlic"))

    set_rule(world.get_location("Town of Ondol: Double Hidden Merchant"), HasAny("Holy Water", "Dracula's Nail"))

    set_rule(world.get_location("Deborah Cliff: Hidden Book"),
             HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))

    set_rule(world.get_location("Bodley Mansion: Hidden Book"), HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))
    set_rule(world.get_location("Bodley Mansion: Evil Orb"), Has("Oak Stake"))

    set_rule(world.get_location("Uta Lower Road: Cursed Guy"), HasAny("Holy Water", "Dracula's Nail") &
             Has("Progressive Whip", 3))

    set_rule(world.get_location("Debious Woods: Hidden Book"), HasAny("Holy Water", "Dracula's Nail", "Dracula's Eyeball"))

    set_rule(world.get_location("Laruba Mansion: Evil Orb"), Has("Oak Stake"))

    set_rule(world.get_location("Dracula Battle"), Has("Holy Water"))
