import struct
from ..Options import RandomGlyphAttributes

glyph_attribute_list = [
    "Strike",
    "Slash",
    "Fire",
    "Ice",
    "Lightning",
    "Holy",
    "Dark",
    "Poison",
    "Curse",
    "Stone"]

generator_glyphs = ["Fulgur",
                    "Ascia",
                    "Vol Ascia",
                    "Melio Ascia",
                    "Redire",
                    "Cubus",
                    "Ignis",
                    "Luminatio",
                    "Vol Luminatio",
                    "Umbra",
                    "Vol Umbra",
                    "Morbus",
                    "Globus"]


def set_glyph_attributes(world) -> None:
    if world.glyph_attributes:  # Skip setting this during UT passthrough
        return

    world.glyph_attributes = {
        "Confodere": ["Slash"],
        "Vol Confodere": ["Slash"],
        "Melio Confodere": ["Slash"],
        "Secare": ["Slash"],
        "Vol Secare": ["Slash"],
        "Melio Secare": ["Slash"],
        "Hasta": ["Slash"],
        "Vol Hasta": ["Slash"],
        "Melio Hasta": ["Slash"],
        "Macir": ["Strike"],
        "Vol Macir": ["Strike"],
        "Melio Macir": ["Strike"],
        "Arcus": ["Slash"],
        "Vol Arcus": ["Slash"],
        "Melio Arcus": ["Slash"],
        "Ascia": ["Slash"],
        "Vol Ascia": ["Slash"],
        "Melio Ascia": ["Slash"],
        "Falcis": ["Slash"],
        "Vol Falcis": ["Slash"],
        "Melio Falcis": ["Slash"],
        "Culter": ["Slash"],
        "Vol Culter": ["Slash"],
        "Melio Culter": ["Slash"],
        "Redire": ["Slash"],
        "Cubus": ["Stone"],
        "Torpor": ["Ice"],  # Torpor also needs to set the Torpor type internally.
        "Lapiste": ["Strike"],
        "Pneuma": ["Slash"],
        "Ignis": ["Fire"],
        "Vol Ignis": ["Fire"],
        "Grando": ["Ice"],
        "Vol Grando": ["Ice"],
        "Fulgur": ["Lightning"],
        "Vol Fulgur": ["Lightning"],
        "Luminatio": ["Holy"],
        "Vol Luminatio": ["Holy"],
        "Umbra": ["Dark"],
        "Vol Umbra": ["Dark"],
        "Morbus": ["Curse"],
        "Nitesco": ["Fire", "Holy"],
        "Acerbatus": ["Lightning", "Dark", "Curse"],
        "Globus": ["Strike"],
        "Dextro Custos": ["Slash"],
        "Sinestro Custos": ["Slash"],
        "Dominus Hatred": ["Dark"],
        "Dominus Anger": ["Dark"],

        "Sword Union": ["Slash"],
        "Axe Union": ["Slash"],
        "Sickle Union": ["Slash"],
        "Hammer Union": ["Strike"],
        "Wind Union": ["Slash"],
        "Lapiste Union": ["Strike"],
        "Fire Union": ["Fire"],
        "Ice Union": ["Ice"],
        "Lightning Union": ["Lightning"],
        "Antipode": ["Fire", "Ice"],
        "Light Union": ["Holy"],
        "Dark Union": ["Dark"],
        "Darklight": ["Holy", "Dark"],
        "Fire Weapon": ["Slash", "Fire"],
        "Ice Weapon": ["Slash", "Ice"],
        "Lightning Weapon": ["Slash", "Lightning"],
        "Wind Weapon": ["Slash", "Slash"],
        "Stone Weapon": ["Strike", "Strike"],
        "Holy Weapon": ["Slash", "Holy"],
        "Dark Weapon": ["Slash", "Dark"],
        "Nitesco Union": ["Fire", "Holy"],
        "Laser Weapon": ["Slash", "Fire", "Holy"],
        "Lance Union": ["Slash"],
        "Knife Union": ["Slash"],
        "Rapier Union": ["Slash"],
        "Arrow Union": ["Slash"]
    }

    if world.options.randomize_glyph_attributes:
        for glyph in world.glyph_attributes:
            attribute_count = len(world.glyph_attributes[glyph])  # For glyphs with multiple types, generate one for each type it usually has
            world.glyph_attributes[glyph] = world.random.sample(glyph_attribute_list, k=attribute_count)

        if world.options.randomize_glyph_attributes == RandomGlyphAttributes.option_consistent:
            #  Set Level glyphs to use the same type as their base
            world.glyph_attributes["Vol Confodere"] = world.glyph_attributes["Confodere"]
            world.glyph_attributes["Melio Confodere"] = world.glyph_attributes["Confodere"]
            world.glyph_attributes["Vol Secare"] = world.glyph_attributes["Secare"]
            world.glyph_attributes["Melio Secare"] = world.glyph_attributes["Secare"]
            world.glyph_attributes["Vol Hasta"] = world.glyph_attributes["Hasta"]
            world.glyph_attributes["Melio Hasta"] = world.glyph_attributes["Hasta"]
            world.glyph_attributes["Vol Macir"] = world.glyph_attributes["Macir"]
            world.glyph_attributes["Melio Macir"] = world.glyph_attributes["Macir"]
            world.glyph_attributes["Vol Arcus"] = world.glyph_attributes["Arcus"]
            world.glyph_attributes["Melio Arcus"] = world.glyph_attributes["Arcus"]
            world.glyph_attributes["Vol Ascia"] = world.glyph_attributes["Ascia"]
            world.glyph_attributes["Melio Ascia"] = world.glyph_attributes["Ascia"]
            world.glyph_attributes["Vol Falcis"] = world.glyph_attributes["Falcis"]
            world.glyph_attributes["Melio Falcis"] = world.glyph_attributes["Falcis"]
            world.glyph_attributes["Vol Culter"] = world.glyph_attributes["Culter"]
            world.glyph_attributes["Melio Culter"] = world.glyph_attributes["Culter"]
            world.glyph_attributes["Vol Ignis"] = world.glyph_attributes["Ignis"]
            world.glyph_attributes["Vol Grando"] = world.glyph_attributes["Grando"]
            world.glyph_attributes["Vol Fulgur"] = world.glyph_attributes["Fulgur"]
            world.glyph_attributes["Vol Luminatio"] = world.glyph_attributes["Luminatio"]
            world.glyph_attributes["Vol Umbra"] = world.glyph_attributes["Umbra"]
            #  And set the combinatorics for Unions
            world.glyph_attributes["Sword Union"] = world.glyph_attributes["Secare"]
            world.glyph_attributes["Axe Union"] = world.glyph_attributes["Ascia"]
            world.glyph_attributes["Sickle Union"] = world.glyph_attributes["Falcis"]
            world.glyph_attributes["Hammer Union"] = world.glyph_attributes["Macir"]
            world.glyph_attributes["Wind Union"] = world.glyph_attributes["Pneuma"]
            world.glyph_attributes["Lapiste Union"] = world.glyph_attributes["Lapiste"]
            world.glyph_attributes["Fire Union"] = world.glyph_attributes["Ignis"]
            world.glyph_attributes["Ice Union"] = world.glyph_attributes["Grando"]
            world.glyph_attributes["Lightning Union"] = world.glyph_attributes["Fulgur"]
            world.glyph_attributes["Antipode"] = world.glyph_attributes["Ignis"] + world.glyph_attributes["Grando"]
            world.glyph_attributes["Light Union"] = world.glyph_attributes["Luminatio"]
            world.glyph_attributes["Dark Union"] = world.glyph_attributes["Umbra"]
            world.glyph_attributes["Darklight"] = world.glyph_attributes["Luminatio"] + world.glyph_attributes["Umbra"]
            world.glyph_attributes["Fire Weapon"] = world.glyph_attributes["Ignis"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Ice Weapon"] = world.glyph_attributes["Grando"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Lightning Weapon"] = world.glyph_attributes["Fulgur"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Wind Weapon"] = world.glyph_attributes["Pneuma"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Stone Weapon"] = world.glyph_attributes["Lapiste"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Holy Weapon"] = world.glyph_attributes["Luminatio"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Dark Weapon"] = world.glyph_attributes["Umbra"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Nitesco Union"] = world.glyph_attributes["Nitesco"]
            world.glyph_attributes["Laser Weapon"] = world.glyph_attributes["Nitesco"] + world.glyph_attributes["Secare"]
            world.glyph_attributes["Lance Union"] = world.glyph_attributes["Hasta"]
            world.glyph_attributes["Knife Union"] = world.glyph_attributes["Culter"]
            world.glyph_attributes["Rapier Union"] = world.glyph_attributes["Confodere"]
            world.glyph_attributes["Arrow Union"] = world.glyph_attributes["Arcus"]

    for index, glyph in enumerate(world.glyph_attributes):
        if index == 47:  # We don't want Unions to be in logic here
            break
        if "Slash" not in world.glyph_attributes[glyph] and "Dominus" not in glyph:
            #  Tin Man needs a non-Slash and non-Dominus glyph to be in logic
            world.can_kill_tin_man.add(glyph)

        #  The generator needs a Lightning element glyph and also a hitbox that can hit both generators
        if "Lightning" in world.glyph_attributes[glyph] and "Dominus" not in glyph and glyph in generator_glyphs:
            world.generator_logic_glyphs.add(glyph)

    if not world.can_kill_tin_man:
        #  If we somehow didn't generate a SINGLE glyph that can kill Tin Man, failsafe Secare to being Strike
        world.glyph_attributes["Secare"] = ["Strike"]
        if world.options.randomize_glyph_attributes == RandomGlyphAttributes.option_consistent:
            world.glyph_attributes["Vol Secare"] = ["Strike"]
            world.glyph_attributes["Melio Secare"] = ["Strike"]
            world.can_kill_tin_man.update({"Vol Secare", "Melio Secare"})
        world.can_kill_tin_man.add("Secare")

    if not world.generator_logic_glyphs:
        #  If we didn't generate any Glyphs that can hit the generator, default to Fulgur
        world.glyph_attributes["Fulgur"] = ["Lightning"]
        if world.options.randomize_glyph_attributes == RandomGlyphAttributes.option_consistent:
            world.glyph_attributes["Vol Fulgur"] = ["Lightning"]
        world.generator_logic_glyphs.add("Fulgur")

    world.logical_regular_glyphs.update(world.can_kill_tin_man, world.generator_logic_glyphs)

    # We want to do this after the last step so they're not added to generator logic glyphs
    if "Torpor" in world.can_kill_tin_man:
        #  Every Villager also gives you a free Torpor glyph
        world.can_kill_tin_man.update({"Nikolai", "Jacob", "Abram", "Laura", "Eugen", "Aeon", "Marcel", "George",
                                      "Serge", "Anna", "Monica", "Daniela", "Irina"})


item_index = {
    "Confodere": 0x01,
    "Vol Confodere": 0x02,
    "Melio Confodere": 0x03,
    "Secare": 0x04,
    "Vol Secare": 0x05,
    "Melio Secare": 0x06,
    "Hasta": 0x07,
    "Vol Hasta": 0x08,
    "Melio Hasta": 0x09,
    "Macir": 0x0A,
    "Vol Macir": 0x0B,
    "Melio Macir": 0x0C,
    "Arcus": 0x0D,
    "Vol Arcus": 0x0E,
    "Melio Arcus": 0x0F,
    "Ascia": 0x10,
    "Vol Ascia": 0x11,
    "Melio Ascia": 0x12,
    "Falcis": 0x13,
    "Vol Falcis": 0x14,
    "Melio Falcis": 0x15,
    "Culter": 0x16,
    "Vol Culter": 0x17,
    "Melio Culter": 0x18,
    "Scutum": 0x19,
    "Vol Scutum": 0x1A,
    "Melio Scutum": 0x1B,
    "Redire": 0x1C,
    "Cubus": 0x1D,
    "Torpor": 0x1E,
    "Lapiste": 0x1F,
    "Pneuma": 0x20,
    "Ignis": 0x21,
    "Vol Ignis": 0x22,
    "Grando": 0x23,
    "Vol Grando": 0x24,
    "Fulgur": 0x25,
    "Vol Fulgur": 0x26,
    "Luminatio": 0x27,
    "Vol Luminatio": 0x28,
    "Umbra": 0x29,
    "Vol Umbra": 0x2A,
    "Morbus": 0x2B,
    "Nitesco": 0x2C,
    "Acerbatus": 0x2D,
    "Globus": 0x2E,
    "Dextro Custos": 0x2F,
    "Sinestro Custos": 0x30,
    "Dominus Hatred": 0x31,
    "Dominus Anger": 0x32,

    "Sword Union": 0x01,
    "Axe Union": 0x02,
    "Sickle Union": 0x03,
    "Hammer Union": 0x04,
    "Wind Union": 0x05,
    "Lapiste Union": 0x06,
    "Fire Union": 0x07,
    "Ice Union": 0x08,
    "Lightning Union": 0x09,
    "Antipode": 0x0A,
    "Light Union": 0x0B,
    "Dark Union": 0x0C,
    "Darklight": 0x0D,
    "Fire Weapon": 0x0E,
    "Ice Weapon": 0x0F,
    "Lightning Weapon": 0x10,
    "Wind Weapon": 0x11,
    "Stone Weapon": 0x12,
    "Holy Weapon": 0x13,
    "Dark Weapon": 0x14,
    "No Union": 0x15,
    "Nitesco Union": 0x16,
    "Laser Weapon": 0x17,
    "Megiddo": 0x18,
    "Shield Union": 0x19,
    "Albus Shot": 0x1A,
    "Lance Union": 0x1B,
    "Knife Union": 0x1C,
    "Rapier Union": 0x1D,
    "Arrow Union": 0x1E

}

attribute_bits = {
    "Strike": 0x01,
    "Slash": 0x02,
    "Fire": 0x04,
    "Ice": 0x08,
    "Lightning": 0x10,
    "Holy": 0x20,
    "Dark": 0x40,
    "Poison": 0x0100,
    "Curse": 0x0200,
    "Stone": 0x0400,
    "Torpor": 0x0800
}


def write_glyph_attributes(world, rom):
    glyph_attribute_table = list(world.glyph_attributes.items())
    #  Split the attribute table into Glyphs and Unions
    glyph_attributes = dict(glyph_attribute_table[:46 + 1])
    union_attributes = dict(glyph_attribute_table[46 + 1:])

    for glyph in glyph_attributes:
        if glyph == "Torpor":
            glyph_attributes[glyph].append("Torpor")  # Torpor needs to also set this special bit
        attribute_field = get_attribute_byte(glyph_attributes[glyph])
        rom.write_to_file(0x020F0A08 + (0x20 * item_index[glyph] + 0x0C), "arm9", attribute_field)

    for glyph in union_attributes:
        attribute_field = get_attribute_byte(union_attributes[glyph])
        rom.write_to_file(0x020F0164 + (0x20 * item_index[glyph] + 0x0C), "arm9", attribute_field)


def get_attribute_byte(attributes) -> bytes:
    #  Convert a list of Attributes into its respective bitfield
    attribute_byte = 0
    for attribute in attributes:
        attribute_byte |= attribute_bits[attribute]
    return struct.pack("I", attribute_byte)
