from ..Options import RandomizeVillagers


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

    for i in range(4):
        if not hintable_majors:
            #  If the hint list is exhausted, mark it as no hint
            hinted_majors.append("None")
        else:
            item = world.random.choice(hintable_majors)
            hinted_majors.append(item)
            hintable_majors.remove(item)

    for hint in hinted_majors:
        location = world.multiworld.find_item(hint, world.player)
        region = location.parent_region.name
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
            #  TODO! Get location GROUPS here, fallback to region only if none are available
            if region == "Menu":
                hint_text += f"."  # Menu would be weird so just say they can find it
            else:
                hint_text += f" at {region}."  # Else show the region
            print(hint_text)
