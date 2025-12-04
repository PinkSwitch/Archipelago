from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .Rules import small_uppies, big_uppies
if TYPE_CHECKING:
    from . import DoSWorld


class DoSLocation(Location):
    game: str = "Castlevania: Dawn of Sorrow"

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "DoSWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    locations_per_region = get_locations_per_region(locations)
    mine_conditions = {"Power of Darkness"}

    regions = [
        create_region(world, player, locations_per_region, "Lost Village Upper"),
        create_region(world, player, locations_per_region, "Lost Village Upper Doorway"),
        create_region(world, player, locations_per_region, "Lost Village Lower"),
        create_region(world, player, locations_per_region, "Lost Village Underground Bottom"), 
        create_region(world, player, locations_per_region, "Lost Village Underground Middle"), 
        create_region(world, player, locations_per_region, "Lost Village Underground Top"),
        create_region(world, player, locations_per_region, "Lost Village Courtyard"),

        create_region(world, player, locations_per_region, "Wizardry Lab Main"),
        create_region(world, player, locations_per_region, "Wizardry Lab West Gate"),
        create_region(world, player, locations_per_region, "Wizardry Lab East Gate"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken West Door"),
        create_region(world, player, locations_per_region, "Wizardry Lab Sunken East Door"),

        create_region(world, player, locations_per_region, "Garden of Madness Lower"),
        create_region(world, player, locations_per_region, "Garden of Madness Upper"),
        create_region(world, player, locations_per_region, "Garden of Madness Water Blocked"),
        create_region(world, player, locations_per_region, "Garden of Madness Post-Boss"),
        create_region(world, player, locations_per_region, "Garden of Madness East Gate"),

        create_region(world, player, locations_per_region, "Demon Guest House Main"),
        create_region(world, player, locations_per_region, "Demon Guest House Puppet Wall Right"),
        create_region(world, player, locations_per_region, "Demon Guest House Lower"),
        create_region(world, player, locations_per_region, "Demon Guest House Number Puzzle"),
        create_region(world, player, locations_per_region, "Demon Guest House Number Puzzle West"),
        create_region(world, player, locations_per_region, "Demon Guest House West Wing"),
        create_region(world, player, locations_per_region, "Demon Guest House Upper"),

        create_region(world, player, locations_per_region, "Dark Chapel"),
        create_region(world, player, locations_per_region, "Dark Chapel Big Room"),
        create_region(world, player, locations_per_region, "Dark Chapel Catacombs Exit"),

        create_region(world, player, locations_per_region, "Condemned Tower Bottom"),
        create_region(world, player, locations_per_region, "Condemned Tower Top"),

        create_region(world, player, locations_per_region, "Cursed Clock Tower Entrance"),
        create_region(world, player, locations_per_region, "Cursed Clock Tower Central"),
        create_region(world, player, locations_per_region, "Cursed Clock Tower Boss Area"), #if i do warp room swap i need to make pre and post boss
        create_region(world, player, locations_per_region, "Cursed Clock Tower Exit"),

        create_region(world, player, locations_per_region, "Subterranean Hell Top Entrance"),
        create_region(world, player, locations_per_region, "Subterranean Hell East"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central/East Connection"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Upper"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Exit"),
        create_region(world, player, locations_per_region, "Subterranean Hell Central Lower"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Middle"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Top"),
        create_region(world, player, locations_per_region, "Subterranean Hell Shaft Bottom"),
        create_region(world, player, locations_per_region, "Subterranean Hell Spike Room West"),
        create_region(world, player, locations_per_region, "Subterranean Hell Spike Room East"),

        create_region(world, player, locations_per_region, "Silenced Ruins Antechamber"),
        create_region(world, player, locations_per_region, "Silenced Ruins"),
        create_region(world, player, locations_per_region, "Silenced Ruins Back Exit"),

        create_region(world, player, locations_per_region, "The Pinnacle"),
        create_region(world, player, locations_per_region, "The Pinnacle Throne Room"),
        create_region(world, player, locations_per_region, "The Pinnacle Lower"),

        create_region(world, player, locations_per_region, "Mine of Judgment"),

        create_region(world, player, locations_per_region, "The Abyss"),
        create_region(world, player, locations_per_region, "The Abyss Beyond Abaddon"),

        create_region(world, player, locations_per_region, "Warp Room"),
    ]

    if world.options.soul_randomizer == 2:
        for region in world.common_souls:
            regions.append(create_region(world, player, locations_per_region, region))

        if world.options.soulsanity_level:
            for region in world.uncommon_souls:
                regions.append(create_region(world, player, locations_per_region, region))

        if world.options.soulsanity_level == 2:
            for region in world.rare_souls:
                regions.append(create_region(world, player, locations_per_region, region))  

    multiworld.regions += regions
    ########################################

    #Lost Village
    multiworld.get_region("Lost Village Upper", player).add_exits(["Lost Village Lower", "Wizardry Lab Main", "Lost Village Upper Doorway", "Lost Village Courtyard"],
                                                    {"Lost Village Lower": lambda state: state.has("Magic Seal 1", player),
                                                     "Wizardry Lab Main": lambda state: state.has("Moat Drained", player),
                                                     "Lost Village Courtyard": lambda state: state.has_any(small_uppies, player),
                                                     "Lost Village Upper Doorway": lambda state: state.has_all({"Puppet Master Soul", "Flying Armor Soul"}, player) or state.has_any(small_uppies, player) or state.has_all({"Puppet Master Soul", "Skeleton Ape Soul"}, player)}) #Is the ape trick hard? Can be done without ape if speedboost on

    multiworld.get_region("Lost Village Courtyard", player).add_exits(["Lost Village Upper", "Demon Guest House Lower"])

    multiworld.get_region("Lost Village Upper Doorway", player).add_exits(["Lost Village Upper", "Demon Guest House Number Puzzle West"])

    multiworld.get_region("Lost Village Lower", player).add_exits(["Lost Village Upper"],
                                                    {"Lost Village Upper": lambda state: state.has("Magic Seal 1", player)})

    multiworld.get_region("Lost Village Underground Bottom", player).add_exits(["Lost Village Underground Middle", "Wizardry Lab Sunken"],
                                                    {"Lost Village Underground Middle": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Lost Village Underground Middle", player).add_exits(["Lost Village Underground Top", "Wizardry Lab West Gate", "Lost Village Underground Bottom"],
                                                    {"Lost Village Underground Top": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Lost Village Underground Top", player).add_exits(["Lost Village Lower", "Lost Village Underground Middle"])
    #######################
    #Wizardry Lab

    multiworld.get_region("Wizardry Lab Main", player).add_exits(["Lost Village Lower", "Garden of Madness Lower", "Warp Room"],
                                                    {"Lost Village Lower": lambda state: state.has("Moat Drained", player),
                                                     "Garden of Madness Lower": lambda state: state.has("Balore Soul", player) or state.has_any(small_uppies, player)})

    multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Wizardry Lab Main", "Lost Village Underground Middle"])
    multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Wizardry Lab Main", "Subterranean Hell Shaft Bottom"])
    multiworld.get_region("Wizardry Lab Sunken West Door", player).add_exits(["Lost Village Underground Bottom", "Wizardry Lab Sunken"],
                                                    {"Wizardry Lab Sunken": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Wizardry Lab Sunken", player).add_exits(["Wizardry Lab Sunken West Door", "Wizardry Lab Sunken East Door"],
                                                {"Wizardry Lab Sunken West Door": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Wizardry Lab Sunken East Door", player).add_exits(["Wizardry Lab Sunken", "Subterranean Hell Spike Room West"],
                                                {"Wizardry Lab Sunken": lambda state: state.has("Rahab Soul", player)})
    ##########################
    #Garden of Madness
    multiworld.get_region("Garden of Madness Lower", player).add_exits(["Wizardry Lab Main", "Garden of Madness Water Blocked", "Demon Guest House Lower", "Garden of Madness Upper", "Dark Chapel", "Warp Room"],
                                                    {"Garden of Madness Water Blocked": lambda state: state.has("Rahab Soul", player),
                                                     "Garden of Madness Upper": lambda state: (state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player))})

    multiworld.get_region("Garden of Madness Water Blocked", player).add_exits(["Garden of Madness Lower", "Subterranean Hell Central Exit"],
                                                    {"Garden of Madness Lower": lambda state: state.has("Rahab Soul", player)})

    multiworld.get_region("Garden of Madness Upper", player).add_exits(["Garden of Madness Lower", "Garden of Madness Post-Boss"],
                                                    {"Garden of Madness Post-Boss": lambda state: state.has("Magic Seal 2", player)})

    multiworld.get_region("Garden of Madness Post-Boss", player).add_exits(["Garden of Madness Upper", "Demon Guest House Main"],
                                                    {"Garden of Madness Upper": lambda state: state.has("Magic Seal 2", player)})

    multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Garden of Madness Post-Boss", "Cursed Clock Tower Entrance"])
    #############################
    #Demon Guest House
    multiworld.get_region("Demon Guest House Main", player).add_exits(["Garden of Madness Post-Boss", "Demon Guest House Puppet Wall Right", "Demon Guest House Number Puzzle", "Demon Guest House West Wing"],
                                                                    {"Demon Guest House Puppet Wall Right": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player),
                                                                     "Demon Guest House West Wing": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Puppet Wall Right", player).add_exits(["Demon Guest House Main", "Demon Guest House Lower"],
                                                                    {"Demon Guest House Main": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Lower", player).add_exits(["Lost Village Upper", "Garden of Madness Lower", "Demon Guest House Puppet Wall Right"],
                                                                    {"Demon Guest House Puppet Wall Right": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Demon Guest House Number Puzzle", player).add_exits(["Demon Guest House Main", "Demon Guest House West Wing", "Demon Guest House Number Puzzle West"],
                                                                    {"Demon Guest House West Wing": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Demon Guest House Number Puzzle West", player).add_exits(["Lost Village Upper Doorway"])

    multiworld.get_region("Demon Guest House West Wing", player).add_exits(["Demon Guest House Main", "Demon Guest House Number Puzzle", "Warp Room"],
                                                                    {"Demon Guest House Main": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Demon Guest House Upper", player).add_exits(["Demon Guest House Main", "The Pinnacle Lower"])
    ###############################
    #Dark Chapel
    multiworld.get_region("Dark Chapel", player).add_exits(["Garden of Madness Lower", "Dark Chapel Catacombs Exit", "Dark Chapel Big Room", "Warp Room"],
                                                                    {"Dark Chapel Catacombs Exit": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player),
                                                                     "Dark Chapel Big Room": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})

    multiworld.get_region("Dark Chapel Big Room", player).add_exits(["Condemned Tower Bottom", "Dark Chapel"])

    multiworld.get_region("Dark Chapel Catacombs Exit", player).add_exits(["Subterranean Hell Top Entrance", "Dark Chapel"],
    {"Dark Chapel": lambda state: state.has_any({"Puppet Master Soul", "Bat Company Soul"}, player)})
    ##########################################################################################################
    #Condemned Tower
    multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Dark Chapel", "Dark Chapel Big Room", "Condemned Tower Top", "Mine of Judgment"],
                                                                    {"Condemned Tower Top": lambda state: state.has_any(big_uppies, player) or (state.has("Flying Armor Soul", player) and state.has_any({"Malphas Soul", "Puppet Master Soul"}, player)) or (state.has("Black Panther Soul", player)),
                                                                     "Dark Chapel Big Room": lambda state: state.has_any(small_uppies, player),
                                                                     "Mine of Judgment": lambda state: state.has_all(mine_conditions, player)})

    multiworld.get_region("Condemned Tower Top", player).add_exits(["Condemned Tower Bottom", "Cursed Clock Tower Entrance", "Warp Room"],
                                                                    {"Cursed Clock Tower Entrance": lambda state: state.has("Tower Key", player),
                                                                     "Warp Room": lambda state: state.has("Magic Seal 3", player)})
                                                                    
    ################################
    #Cursed Clock Tower
    multiworld.get_region("Cursed Clock Tower Entrance", player).add_exits(["Garden of Madness East Gate", "Condemned Tower Top", "Cursed Clock Tower Central"],
                                                                    {"Cursed Clock Tower Central": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                                     "Condemned Tower Top": lambda state: state.has("Tower Key", player)})

    multiworld.get_region("Cursed Clock Tower Central", player).add_exits(["Cursed Clock Tower Entrance", "Cursed Clock Tower Boss Area"],
                                                                    {"Cursed Clock Tower Boss Area": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Cursed Clock Tower Boss Area", player).add_exits(["Cursed Clock Tower Central", "Cursed Clock Tower Exit", "Warp Room"],
                                                                    {"Cursed Clock Tower Exit": lambda state: state.has_all({"Bat Company Soul", "Magic Seal 4"}, player),
                                                                     "Warp Room": lambda state: state.has("Magic Seal 4", player)})

    multiworld.get_region("Cursed Clock Tower Exit", player).add_exits(["Cursed Clock Tower Boss Area", "The Pinnacle Lower"],
                                                                    {"Cursed Clock Tower Boss Area": lambda state: state.has_all({"Bat Company Soul", "Magic Seal 4"}, player)})
    ####################################################################################
    #Subterranean Hell
    multiworld.get_region("Subterranean Hell Top Entrance", player).add_exits(["Dark Chapel Catacombs Exit", "Subterranean Hell East"],
                                                {"Subterranean Hell East": lambda state: state.has_all({"Rahab Soul", "Magic Seal 3"}, player)})

    multiworld.get_region("Subterranean Hell East", player).add_exits(["Subterranean Hell Top Entrance", "Subterranean Hell Central/East Connection"],
                                                {"Subterranean Hell Top Entrance": lambda state: state.has_all({"Rahab Soul", "Magic Seal 3"}, player) and (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)),
                                                 "Subterranean Hell Central/East Connection": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Central/East Connection", player).add_exits(["Subterranean Hell Central Upper", "Subterranean Hell East"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player)})

    multiworld.get_region("Subterranean Hell Central Upper", player).add_exits(["Subterranean Hell Central/East Connection", "Subterranean Hell Central Exit", "Subterranean Hell Central Lower"],
                                                {"Subterranean Hell Central/East Connection": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player) and (state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)),
                                                "Subterranean Hell Central Exit": lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Black Panther Soul"}, player)})

    multiworld.get_region("Subterranean Hell Central Exit", player).add_exits(["Subterranean Hell Central Upper", "Garden of Madness Water Blocked"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any({"Rahab Soul", "Malphas Soul"}, player)})

    multiworld.get_region("Subterranean Hell Central Lower", player).add_exits(["Subterranean Hell Central Upper", "Subterranean Hell Shaft Middle", "Warp Room"],
                                                {"Subterranean Hell Central Upper": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player)})

    multiworld.get_region("Subterranean Hell Shaft Middle", player).add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Shaft Bottom", "Subterranean Hell Shaft Top"],
                                                {"Subterranean Hell Central Lower": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Subterranean Hell Shaft Top": lambda state: state.has_any(big_uppies, player)})

    multiworld.get_region("Subterranean Hell Shaft Top", player).add_exits(["Subterranean Hell Shaft Middle", "Wizardry Lab East Gate"])

    multiworld.get_region("Subterranean Hell Shaft Bottom", player).add_exits(["Subterranean Hell Central Lower", "Subterranean Hell Spike Room East", "Silenced Ruins Antechamber"],
                                                {"Subterranean Hell Shaft Middle": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Subterranean Hell Spike Room East": lambda state: state.has_any(small_uppies, player) or state.has("Puppet Master Soul", player),
                                                 "Silenced Ruins Antechamber": lambda state: state.has_any(small_uppies, player) or state.has_any({"Puppet Master Soul", "Flying Armor Soul", "Black Panther Soul"}, player)})

    multiworld.get_region("Subterranean Hell Spike Room East", player).add_exits(["Subterranean Hell Spike Room West", "Subterranean Hell Shaft Bottom"],
                                                {"Subterranean Hell Spike Room West": lambda state: state.has_all({"Rahab Soul", "Puppet Master Soul"}, player) and state.can_reach("Garden of Madness Lower", 'Region', player)}) # Or bone ark...

    multiworld.get_region("Subterranean Hell Spike Room West", player).add_exits(["Wizardry Lab Sunken East Door", "Subterranean Hell Spike Room East"],
                                                {"Subterranean Hell Spike Room East": lambda state: state.has_all({"Rahab Soul", "Puppet Master Soul"}, player) and state.can_reach("Garden of Madness Lower", 'Region', player)})

    multiworld.register_indirect_condition(world.get_region("Garden of Madness Lower"), world.get_entrance("Demon Guest House Lower -> Garden of Madness Lower"))
    #####################################################
    #Silenced Ruins
    multiworld.get_region("Silenced Ruins Antechamber", player).add_exits(["Subterranean Hell Shaft Bottom", "Silenced Ruins"],
                                                {"Silenced Ruins": lambda state: state.has("Zephyr Soul", player)})

    multiworld.get_region("Silenced Ruins", player).add_exits(["Silenced Ruins Back Exit", "Silenced Ruins Antechamber", "Warp Room"],
                                                {"Silenced Ruins Antechamber": lambda state: state.has("Zephyr Soul", player),
                                                 "Silenced Ruins Back Exit": lambda state: state.has_any(small_uppies, player)})

    multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Silenced Ruins", "Subterranean Hell East"])

    ###############################
    #The Pinnacle
    multiworld.get_region("The Pinnacle Lower", player).add_exits(["The Pinnacle", "Demon Guest House Upper", "Cursed Clock Tower Exit", "Warp Room"],
                                                                 {"The Pinnacle": lambda state: state.has_any(small_uppies, player),
                                                                 "Cursed Clock Tower Exit": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player),
                                                                 "Warp Room": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player)})

    multiworld.get_region("The Pinnacle", player).add_exits(["The Pinnacle Lower", "The Pinnacle Throne Room"],
                                                                 {"The Pinnacle Throne Room": lambda state: state.has_any(big_uppies, player)})

    ###############################
    #Mine of Judgment
    multiworld.get_region("Mine of Judgment", player).add_exits(["The Abyss", "Warp Room"],
                                                                 {"The Abyss": lambda state: state.has_any(small_uppies, player) or state.has("Pupper Master Soul", player)})

    multiworld.get_region("The Abyss", player).add_exits(["Mine of Judgment", "The Abyss Beyond Abaddon"],
                                                        {"Mine of Judgment": lambda state: state.has_any(small_uppies, player),
                                                         "The Abyss Beyond Abaddon": lambda state: state.has_any(big_uppies, player) and state.has("Magic Seal 5", player)})

    multiworld.get_region("The Abyss Beyond Abaddon", player).add_exits(["Warp Room"])

    multiworld.get_region("Warp Room", player).add_exits(["Lost Village Lower"])
    #Paranoia; If not soulsanity, ADD the can_reach rules
    #Maybe I should make Bone Ark progression anyways? So you can be expected to use it from the left side...
    #Also, ukoback. Receiving Ukoback should always be an alternative to reaching. Oh I can do an or if not soulsanity, and it is the only one if soulsanity

    if world.options.soul_randomizer == 2:
        multiworld.get_region("Lost Village Upper", player).add_exits(["Skeleton Soul", "Bat Soul", "Armor Knight Soul", "Peeping Eye Soul", "Yeti Soul", "Zombie Soul", "Axe Armor Soul", "Warg Soul", "Spin Devil Soul"],
        {"Spin Devil Soul": lambda state: state.has("Moat Drained", player),
         "Yeti Soul": lambda state: state.has("Waiter Skeleton Soul", player)})

        multiworld.get_region("Lost Village Upper Doorway", player).add_exits(["Peeping Eye Soul", "Skelerang Soul"])

        multiworld.get_region("Lost Village Lower", player).add_exits(["Skeleton Soul", "Armor Knight Soul", "Bat Soul", "Zombie Soul", "Ouija Table Soul", "Spin Devil Soul", "Student Witch Soul"],
        {"Student Witch Soul": lambda state: state.has("Moat Drained", player)}) #It's in the same area as the switch

        multiworld.get_region("Lost Village Courtyard", player).add_exits(["Warg Soul", "Skeleton Ape Soul", "Hell Boar Soul"],
        {"Hell Boar Soul": lambda state: state.has_any(big_uppies, player)})

        multiworld.get_region("Lost Village Underground Top", player).add_exits(["Axe Armor Soul", "Great Axe Armor Soul", "Merman Soul"])

        multiworld.get_region("Lost Village Underground Bottom", player).add_exits(["White Dragon Soul"])
        ####### WIZARDRY LAB SOULS ########
        multiworld.get_region("Wizardry Lab Main", player).add_exits(["Ghost Soul", "Bomber Armor Soul", "Slime Soul", "Axe Armor Soul", "Student Witch Soul", "Skull Archer Soul", "Skeleton Soul", "Slaughterer Soul", "Manticore Soul", "The Creature Soul", "Armor Knight Soul", "Golem Soul"])

        multiworld.get_region("Wizardry Lab West Gate", player).add_exits(["Great Axe Armor Soul", "Heart Eater Soul"])

        multiworld.get_region("Wizardry Lab East Gate", player).add_exits(["Cave Troll Soul", "Mimic Soul"])

        multiworld.get_region("Wizardry Lab Sunken", player).add_exits(["Homunculus Soul", "Larva Soul", "Mimic Soul"])

        multiworld.get_region("Wizardry Lab Sunken West Door", player).add_exits(["Iron Golem Soul"])
        ####### GARDEN OF MADNESS ######
        multiworld.get_region("Garden of Madness Lower", player).add_exits(["Une Soul", "Skelerang Soul", "Mandragora Soul", "Catoblepas Soul", "Treant Soul", "Corpseweed Soul", "Skeleton Ape Soul", "Mollusca Soul", "Skeleton Farmer Soul", "Mimic Soul", "Yorick Soul", "Rycuda Soul"],
        {"Mimic Soul": lambda state: state.has_any(small_uppies, player)})

        multiworld.get_region("Garden of Madness Upper", player).add_exits(["Barbariccia Soul", "Rycuda Soul", "Skeleton Ape Soul", "Corpseweed Soul", "Mollusca Soul", "Corpseweed Soul", "Skeleton Ape Soul", "Mollusca Soul"])

        multiworld.get_region("Garden of Madness Post-Boss", player).add_exits(["Skelerang Soul", "Une Soul", "Corpseweed Soul", "Skeleton Ape Soul", "Ghoul Soul", "Fleaman Soul"])

        multiworld.get_region("Garden of Madness East Gate", player).add_exits(["Wakwak Tree Soul"])
        ##### DEMON GUEST HOUSE ####
        multiworld.get_region("Demon Guest House Lower", player).add_exits(["Axe Armor Soul", "Peeping Eye Soul", "Skeleton Soul"])

        multiworld.get_region("Demon Guest House Puppet Wall Right", player).add_exits(["Skelerang Soul"])

        multiworld.get_region("Demon Guest House Main", player).add_exits(["Persephone Soul", "Skelerang Soul", "Devil Soul", "Lilith Soul", "Ghost Dancer Soul", "Killer Clown Soul", "Valkyrie Soul", "Waiter Skeleton Soul", "Killer Doll Soul", "Bone Pillar Soul"])

        multiworld.get_region("Demon Guest House Number Puzzle West", player).add_exits(["Persephone Soul"])

        multiworld.get_region("Demon Guest House West Wing", player).add_exits(["Killer Doll Soul", "Killer Clown Soul", "Bone Pillar Soul", "Lilith Soul", "Buer Soul", "Quetzalcoatl Soul"])

        multiworld.get_region("Demon Guest House Upper", player).add_exits(["Flame Demon Soul", "Malachi Soul", "Skelerang Soul", "Werewolf Soul", "Ghost Dancer Soul", "Student Witch Soul", "Lilith Soul", "Witch Soul", "Succubus Soul", "Persephone Soul", "Iron Golem Soul", "Mimic Soul"])
        ##### DARK CHAPEL #####

        multiworld.get_region("Dark Chapel", player).add_exits(["Witch Soul", "Mini Devil Soul", "Ghoul Soul", "Amalaric Sniper Soul", "Ghost Dancer Soul", "The Creature Soul", "Hell Boar Soul", "Bone Pillar Soul", "Barbariccia Soul", "White Dragon Soul", "Guillotiner Soul", "Great Armor Soul", "Valkyrie Soul", "Ghost Soul", "Quetzalcoatl Soul", "Tombstone Soul"],
        {"Quetzalcoatl Soul": lambda state: state.has("Magic Seal 2", player)})

        multiworld.get_region("Dark Chapel Big Room", player).add_exits(["Valkyrie Soul", "Mini Devil Soul", "Quetzalcoatl Soul"])

        multiworld.get_region("Dark Chapel Catacombs Exit", player).add_exits(["Catoblepas Soul"])
        #####CONDEMNED TOWER #####
        multiworld.get_region("Condemned Tower Bottom", player).add_exits(["Draghignazzo Soul"])

        multiworld.get_region("Condemned Tower Top", player).add_exits(["Disc Armor Soul", "Skeleton Ape Soul", "Great Axe Armor Soul", "Werewolf Soul", "Buer Soul", "Fleaman Soul"])
        ##### CURSED CLOCK TOWER ######
        multiworld.get_region("Cursed Clock Tower Entrance", player).add_exits(["Harpy Soul", "Medusa Head Soul", "Catoblepas Soul", "Imp Soul", "Malachi Soul", "Tanjelly Soul", "Dead Pirate Soul"])

        multiworld.get_region("Cursed Clock Tower Central", player).add_exits(["Imp Soul", "Medusa Head Soul", "Bugbear Soul", "Slime Soul", "Tanjelly Soul"])

        multiworld.get_region("Cursed Clock Tower Boss Area", player).add_exits(["Flying Humanoid Soul"],
        {"Flying Humanoid Soul": lambda state: state.has("Mandragora Soul", player)})

        multiworld.get_region("Cursed Clock Tower Exit", player).add_exits(["Devil Soul", "Harpy Soul"])
        ##### SUBTERRANEAN HELL #####
        multiworld.get_region("Subterranean Hell Top Entrance", player).add_exits(["Une Soul", "Dead Pirate Soul", "Cave Troll Soul", "Decarabia Soul"],
        {"Decarabia Soul": lambda state: state.has("Magic Seal 3", player)})

        multiworld.get_region("Subterranean Hell East", player).add_exits(["Fish Head Soul", "Decarabia Soul", "Mimic Soul", "Needles Soul", "Frozen Shade Soul", "Killer Fish Soul", "Merman Soul", "Procel Soul"],
        {"Fish Head Soul": lambda state: state.has("Rahab Soul", player),
        "Decarabia Soul": lambda state: state.has("Rahab Soul", player),
        "Mimic Soul": lambda state: state.has("Rahab Soul", player),
        "Needles Soul": lambda state: state.has("Rahab Soul", player)})

        multiworld.get_region("Subterranean Hell Central/East Connection", player).add_exits(["Une Soul", "Alura Une Soul"])

        multiworld.get_region("Subterranean Hell Shaft Bottom", player).add_exits(["Dead Pirate Soul", "Ukoback Soul", "Medusa Head Soul", "Merman Soul"])

        multiworld.get_region("Subterranean Hell Shaft Middle", player).add_exits(["Frozen Shade Soul", "Devil Soul"])

        multiworld.get_region("Subterranean Hell Shaft Top", player).add_exits(["Killer Fish Soul", "Ukoback Soul"])

        multiworld.get_region("Subterranean Hell Central Lower", player).add_exits(["Frozen Shade Soul", "Dead Pirate Soul", "Merman Soul", "Procel Soul"])

        multiworld.get_region("Subterranean Hell Central Upper", player).add_exits(["Ukoback Soul", "Frozen Shade Soul", "Dead Pirate Soul", "Killer Fish Soul", "Needles Soul", "Merman Soul", "Bone Ark Soul"])

        multiworld.get_region("Subterranean Hell Central Exit", player).add_exits(["Ukoback Soul", "Frozen Shade Soul", "Merman Soul", "Mimic Soul"])
        ####S ILENCED RUINS #####
        multiworld.get_region("Silenced Ruins", player).add_exits(["Ghoul Soul", "Skeleton Soul", "Peeping Eye Soul", "Bat Soul", "Skull Archer Soul", "Dead Crusader Soul", "Devil Soul", "Dead Mate Soul", "Larva Soul", "Bone Ark Soul", "Skelerang Soul"],
        {"Devil Soul": lambda state: state.has("Balore Soul", player)})

        multiworld.get_region("Silenced Ruins Back Exit", player).add_exits(["Gorgon Soul", "Waiter Skeleton Soul"])
        ##### PINNACLE #####
        multiworld.get_region("The Pinnacle", player).add_exits(["Dead Crusader Soul", "Erinys Soul", "Werewolf Soul", "Guillotiner Soul", "Mushussu Soul", "Alastor Soul", "Final Guard Soul", "Mothman Soul"],
        {"Mothman Soul": lambda state: state.has("Rycuda Soul", player)})

        multiworld.get_region("The Pinnacle Lower", player).add_exits(["Succubus Soul", "Bugbear Soul", "Malachi Soul", "Dead Warrior Soul", "Mushussu Soul", "Werewolf Soul", "Flame Demon Soul", "Erinys Soul", "Guillotiner Soul"])

        if world.options.goal:
            multiworld.get_region("Mine of Judgment", player).add_exits(["Tanjelly Soul", "Slogra Soul", "Ripper Soul", "Giant Slug Soul", "Bugbear Soul", "Gaibon Soul"])

            multiworld.get_region("The Abyss", player).add_exits(["Arc Demon Soul", "Alastor Soul", "Erinys Soul", "Mud Demon Soul", "Heart Eater Soul", "Frozen Shade Soul", "Stolas Soul", "Final Guard Soul", "Malachi Soul", "White Dragon Soul", "Malacoda Soul"])

            multiworld.get_region("The Abyss Beyond Abaddon", player).add_exits(["Black Panther Soul", "Iron Golem Soul", "Succubus Soul"])














def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = DoSLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "DoSWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
    

#TODO; Skeletone Ape in tower with speedboost on