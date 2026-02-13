from dataclasses import dataclass

@dataclass
class DoSBoss:
    flag: int # The SLOT's Boss Defeated flag.
    assigned_soul: int # Which Soul is assigned to the SLOT's original boss. Soul randomization reworks how souls are given so this needs to stay the same.
    floor_height: int # The SLOT's room floor height
    room_width: int # The SLOT's room width
    boss_address_pointer: int # Which adress we write to to place the boss
    new_boss: str = "None" # Which boss has been randomized to be here

def randomize_bosses(world):
    boss_pool = [
        "Flying Armor",
        "Balore",
        "Dimitrii",
        "Malphas",
        "Dario",
        "Puppet Master",
        "Gergoth",
        "Zephyr",
        "Rahab",
        "Bat Company",
        "Paranoia",
        "Aguni",
        "Death",
        "Abaddon"
    ]

    available_boss_slots = [
        "Lost Village",
        "Wizardry Lab",
        "Dark Chapel",
        "Dark Chapel 2",
        "Garden of Madness",
        "Demon Guest House",
        "Condemned Tower",
        "Cursed Clock Tower",
        "Subterranean Hell",
        "Silenced Ruins",
        "Demon Guest House Upper",
        "The Pinnacle",
        "Mine of Judgement",
        "The Abyss"
    ]


    world.boss_slots = {
        "Lost Village": DoSBoss(0x02, 0x35, 1, 2, 0xA50B8),  # Flying Armor
        "Wizardry Lab": DoSBoss(0x04, 0x74, 1, 1, 0xAD0B0),  # Balore
        "Dark Chapel": DoSBoss(0x08, 0xFF, 1, 2, 0xB2B58), # Dimitrii
        "Dark Chapel 2": DoSBoss(0x10, 0x75, 2, 2, 0xB2B04),  # Malphas
        "Garden of Madness": DoSBoss(0x20, 0xFF, 1, 2, 0xB0500),  # Dario 1 Make sure this is the right address for the flag. Seems low.
        "Demon Guest House": DoSBoss(0x40, 0x00, 1, 2, 0xA96F0),  # Puppet Master
        "Condemned Tower": DoSBoss(0x80, 0x57, 1, 1, 0xB5BE0),  # Gergoth
        "Cursed Clock Tower": DoSBoss(0x0200, 0x01, 1, 2, 0xBCDA0),  # Zephyr
        "Subterranean Hell": DoSBoss(0x0100, 0x77, 1, 2, 0xB8B1C),  # Rahab
        "Silenced Ruins": DoSBoss(0x0400, 0x36, 1, 1, 0xBA4B0),  # Bat Company
        "Demon Guest House Upper": DoSBoss(0x1000, 0x02, 1, 1, 0xA99A8), # Paranoia
        "The Pinnacle": DoSBoss(0x0800, 0x2B, 1, 2, 0x0), # Aguni, not Dario 2
        "Mine of Judgement": DoSBoss(0x2000, 0x58, 1, 2, 0xB6360), # Death
        "The Abyss": DoSBoss(0x8000, 0x2C, 1, 1, 0xC2260) # Abaddon
    }

    rahab_boss = world.random.choice([
        "Flying Armor",
        "Balore",
        "Puppet Master",
        "Rahab",
        "Bat Company",
        "Aguni",
        "Death"
    ])

    world.boss_slots["Subterranean Hell"].new_boss = rahab_boss  # Any other boss in Rahab's room will sink below the water level
    boss_pool.remove(rahab_boss)

    for boss in boss_pool:
        if boss == "Balore":
            # Balore needs to have a room with a 1-tile floor height, or there won't be room to dodge his laser attack
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None" and world.boss_slots[room].floor_height == 1]
        elif boss in ["Puppet Master", "Rahab"]:
             # Puppet Master and Rahab need to be in a room that is 2-tiles wide.
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None" and world.boss_slots[room].room_width == 2]
        else:
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None"]
            
        new_room = world.random.choice(valid_rooms)
        world.boss_slots[new_room] = boss  # All other combinations are valid
    print(world.boss_slots)



    # Balore needs to have a 1-tile floor
    # Puppet master needs a 2-tile room
    # Rahab needs a 2-tile room

    # TODO! Have bosses check the NEW flag when spawning, as well as when being defeated
    # Instead of what I was doing before. Have a list of all the bosses in order. Use the index, and have a Base Address where the flags START.


# NOTES!
# Bosses need to check the new flag when spawning, too...
# - i should think of how I want to handle Boss Seals. Should I change the seal on the boss, or neither?
# - I need to swap the souls around so that their assigned soul matches the original boss's soul.
# - Flying Armor (and maybe other bosses) apparently require a soul drop, so they might not work in Dimitrii/Dario room
# - I might be able to randomize Aguni, but I will need to make sure the replacement spawns in the Mirror World.
# - Scale stats for what area they're in? I can maybe do order math here. Just replace them with the original boss's stats
# - I need to hard-remove the Balore pre-boss cutscene if boss rando is on
# - Balore needs to be in a room with a 1-tile floor
# - Puppet master needs to be in a 2-tile wide room
# - Rahab needs to be in a 2-tile wide room
# - Malphas, Dimitrii, Dario, Gergoth, Zephy, Paranoia, and Abaddon sink in Rahab's room.
# - Apparently Puppet master's wall is too thick for some bosses, so it needs to be thinned out. Figure out what DSVania does in move_puppet_master_wall
# - Implement the code that moves and changes balore to face the player
# - game.fs.write(0x0225A988, [0xE1A00000].pack("V")) # nop Dario 1 might trigger the Aguni fight in a mirror. Will this affect any boss rooms?
# - Dimitrii has issues with his post-boss cutscene, place the boss rush variant
# - game.fs.write(0x0225BB6C, [0xE1A02800].pack("V")) # mov r2, r0, lsl 10h If Dario is in a 1-wide room, stop him from teleporting too far
# - If gergoth is NOT in the tower, use boss rush version
# - Puppet master's pos needs to be adjusted for specific roomms, including the limbs
# - Puppet Master needs these game.fs.write(0x022FFC1C, [0xE1A00000].pack("V")) # nop (for when he's alive)
# - game.fs.write(0x022FFA40, [0xE1A00000].pack("V")) # nop (for after he's dead)
# - Zephyr needs to be centered. Use boss-rush zephy if room width < 2
# -  Basically I need to look over all of adjust boss position and do it in ORDER.
# - Gergoth needs to face the player properly
# Bosses in the tower need to only spawn in the top floor room
# Death is really really fucked up and i might need to delete objects from any room he spawns in
# ON second thought, it might be that Dimitrii/Dario's rooms don't open after beating them. I wonder if maybe I can hook into the Julius Mode check that skips their cutscenes
# Consider NOPing out 0x02300808, which creates Balore's ice blocks after defeat
# Dario 2 probably SPAWNS aguni manually, and the one in the room is probably used for Julius mode. yes. aguni isnt even in.
# I just realized having a different boss in the mirror is going to fuck with the overlays REALLY REALLY BAD. FIGURE THAT OUT.
# Set SPAWN flags
# Balore in LV is WEIRD, he tries to spawn on the left side of the room, the camera's fucked up. hmm. can i fix this?
# There's code called LoadOverlay. Maybe I can call this during the Mirror transition?
# For room-center bosses, X pos is room_with * 100 / 2

# CURRENT NOTES!
# Aguni sets the flag twice. Check thsi again after finishing the rest
# Boss spawn flags are now SET correctly.
# Dario loads his flag dynamically. I need to figure out where that comes from and make sure I only change the flag for Dario 1, and leave Dario 2 alone.


# Check EVERY COMBINATION OF BOSSES for oddities. MANUALLY.



#TESTED COMBINATIONS;

#Flying Armor ROOM
# Flying Armor - ✓
# Balore - ✓
# Dimitrii - 
# Malphas - 
# Dario - 
# Puppet Master -
# Gergoth - 
# Zephyr - 
# Rahab - 
# Bat Company - 
# Paranoia - 
# Aguni - 
# Death - 
# Abaddon - 

