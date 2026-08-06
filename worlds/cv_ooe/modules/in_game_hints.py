from ..Options import RandomizeVillagers
from ..game_data import enemy_table
from .text_builder import text_encoder, calculate_text_width
import re


def write_cat_hints(world, rom):
    hintable_majors = ["Dextro Custos", "Sinestro Custos", "Dominus Hatred", "Dominus Anger",
                       "Magnes", "Paries", "Volaticus", "Rapidus Fio", "Arma Custos", "Dominus Agony",
                       "Redire", "Lizard Tail", "Ordinary Rock", "Serpent Scale", "Glyph Union",
                       "Nikolai", "Jacob", "Abram", "Laura", "Eugen", "Aeon", "Marcel", "George",
                       "Serge", "Anna", "Monica", "Irina", "Daniela", "Map: Training Hall",
                       "Map: Ruvas Forest", "Map: Argila Swamp", "Map: Kalidus Channel",
                       "Map: Somnus Reef", "Map: Minera Prison Island", "Map: Lighthouse",
                       "Map: Tymeo Mountains", "Map: Tristis Pass", "Map: Large Cavern", "Map: Giant's Dwelling",
                       "Map: Mystery Manor", "Map: Misty Forest Road", "Map: Oblivion Ridge", "Map: Skeleton Cave",
                       "Map: Monastery"]
    hinted_majors = []

    if not world.options.shuffle_dominus:
        #  Since the player already knows where these are, we don't want to hint them
        hintable_majors.remove("Dominus Hatred")
        hintable_majors.remove("Dominus Anger")
        hintable_majors.remove("Dominus Agony")

    if world.options.randomize_villagers != RandomizeVillagers.option_anywhere:
        hintable_majors.remove("Nikolai")
        hintable_majors.remove("Jacob")
        hintable_majors.remove("Abram")
        hintable_majors.remove("Laura")
        hintable_majors.remove("Eugen")
        hintable_majors.remove("Aeon")
        hintable_majors.remove("Marcel")
        hintable_majors.remove("George")
        hintable_majors.remove("Serge")
        hintable_majors.remove("Anna")
        hintable_majors.remove("Monica")
        hintable_majors.remove("Irina")
        hintable_majors.remove("Daniela")

    if world.options.remove_large_cavern:
        #  Remove areas we can't access
        hintable_majors.remove("Map: Large Cavern")

    if world.options.remove_training_hall:
        hintable_majors.remove("Map: Training Hall")

    for item in world.multiworld.precollected_items[world.player]:
        #  If we start with any hintables, remove them
        if item.name in hintable_majors:
            hintable_majors.remove(item.name)

    for i in range(3):
        if not hintable_majors:
            #  If the hint list is exhausted, mark it as no hint
            hinted_majors.append("None")
        else:
            item = world.random.choice(hintable_majors)
            hinted_majors.append(item)
            hintable_majors.remove(item)

    for hint in hinted_majors:
        is_enemy_text = False
        location = world.multiworld.find_item(hint, world.player)
        groups = world.multiworld.worlds[location.player].location_name_groups
        possible_groups = [group_name for group_name, group_locations in groups.items()
                           if location.name in group_locations and group_name != "Everywhere"]
        if possible_groups:
            region = world.random.choice(possible_groups)
        else:
            region = location.parent_region.name

        if world.player == location.player and location.parent_region.name in enemy_table:
            region = location.parent_region.name
            is_enemy_text = True

        hint_text = "I think that "

        if hint == "None":
            hint_text += "You don't need any more hints!"
        else:
            if "Map" in hint:
                #  Split this so that it reads more naturally in dialogue
                hint = f"a map to {hint.split('Map: ')[1]}"
            hint_text += hint
            hint_text += " can be found"
            if location.player != world.player:
                #  If it's not local, append the finder
                hint_text += f" by {world.multiworld.get_player_name(location.player)}"
            if region == "Menu":
                hint_text += f"."  # Menu would be weird so just say they can find it
            else:
                if not is_enemy_text:
                    hint_text += f" at {region}."  # Else show the region
                else:
                    hint_text += f" with {region}."
            if len(hint_text) > 0x90:  # Max space allocated for this
                hint_text[:-3] += "..."  # Trail off if we run out of room

            text_split = re.split(r'( )', hint_text)  # Split by words
            width = 0
            lines = 0
            for index, string in enumerate(text_split):
                replace_char = "\n"  # If we run out of room, replace with a line break
                if width >= 117:  # If we hit this, we need to line break
                    lines += 1
                    if lines == 3:
                        replace_char = "\v"  # If we ran out the textbox, make a new page instead.
                        lines = 0
                    if string == " ":
                        text_split[index] = replace_char
                        width = 0
                    else:
                        text_split[index - 1] = replace_char  # If it's not a space, replace the last space
                        width = 0
                width += calculate_text_width(string)
            hint_text = "".join(text_split)
            print(hint_text)
