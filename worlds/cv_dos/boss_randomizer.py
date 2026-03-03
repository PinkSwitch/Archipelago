from dataclasses import dataclass

@dataclass
class DoSBoss:
    flag: int # The SLOT's Boss Defeated flag.
    assigned_soul: int # Which Soul is assigned to the SLOT's original boss. Soul randomization reworks how souls are given so this needs to stay the same.
    floor_height: int # The SLOT's room floor height
    room_width: int # The SLOT's room width
    boss_address_pointer: int # Which adress we write to to place the boss
    seal: int # Which seal this slot uses
    new_boss: str = "None" # Which boss has been randomized to be here

@dataclass
class DoSBossData:
    enemy_id: int # The Enemy's internal ID number
    flag_index: int # Index used for writing boss flags

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
        "Lost Village": DoSBoss(0x02, 0x35, 1, 2, 0xA50B8, 1),  # Flying Armor
        "Wizardry Lab": DoSBoss(0x04, 0x74, 1, 1, 0xAD0B0, 1),  # Balore
        "Dark Chapel": DoSBoss(0x08, 0xFF, 1, 2, 0xB2B58, 2), # Dimitrii
        "Dark Chapel 2": DoSBoss(0x10, 0x75, 2, 2, 0xB2B04, 2),  # Malphas
        "Garden of Madness": DoSBoss(0x20, 0xFF, 1, 2, 0xB0500, 2),  # Dario 1 Make sure this is the right address for the flag. Seems low.
        "Demon Guest House": DoSBoss(0x40, 0x00, 1, 2, 0xA96F0, 3),  # Puppet Master
        "Condemned Tower": DoSBoss(0x80, 0x57, 1, 1, 0xB5BE0, 3),  # Gergoth
        "Cursed Clock Tower": DoSBoss(0x0200, 0x01, 1, 2, 0xBCDA0, 4),  # Zephyr
        "Subterranean Hell": DoSBoss(0x0100, 0x77, 1, 2, 0xB8B1C, 3),  # Rahab
        "Silenced Ruins": DoSBoss(0x0400, 0x36, 1, 1, 0xBA4B0, 4),  # Bat Company
        "Demon Guest House Upper": DoSBoss(0x1000, 0x02, 1, 1, 0xA99A8, 4), # Paranoia
        "The Pinnacle": DoSBoss(0x0800, 0x2B, 1, 2, 0x?????, 4), # Aguni, not Dario 2
        "Mine of Judgement": DoSBoss(0x2000, 0x58, 1, 2, 0xB6360, 5), # Death
        "The Abyss": DoSBoss(0x8000, 0x2C, 1, 1, 0xC2260, 5) # Abaddon
    }

    world.boss_data = {
        "Flying Armor": DoSBoss(0x65, 0)
        "Balore": DoSBoss(0x66, 2)
        "Malphas": DoSBoss(0x67, 6)
        "Dimitrii": DoSBoss(0x68, 4)
        "Dario": DoSBoss(0x69, 8)
        "Puppet Master": DoSBoss(0x6A, 10)
        "Rahab": DoSBoss(0x6B, 14)
        "Gergoth": DoSBoss(0x6C, 12)
        "Zephyr": DoSBoss(0x6D, 16)
        "Bat Company": DoSBoss(0x6E, 18)
        "Paranoia": DoSBoss(0x6F, 22)
        "Aguni": DoSBoss(0x70, 20)
        "Death": DoSBoss(0x71, 24)
        "Abaddon": DoSBoss(0x72, 26)
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
             # Puppet Master can teleport the player out of bounds, and Rahab would take an obnoxiously long time to be damagable.
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None" and world.boss_slots[room].room_width == 2]
        else:
            # All other combinations are valid
            valid_rooms = [room for room in world.boss_slots if world.boss_slots[room].new_boss == "None"]
            
        new_room = world.random.choice(valid_rooms)
        world.boss_slots[new_room].new_boss = boss

def write_bosses(world, rom):
    rom.write_bytes(0xAD0C1, bytearray([0x00])) # Delete the Balore pre-boss cutscene, it breaks the game

    for index, room in enumerate(world.boss_slots):
        slot = world.boss_slots[room]
        boss = world.boss_data[slot.new_boss]
        rom.write_bytes(slot.boss_address_pointer + 6, bytearray([boss.enemy_id])) # Write the new boss into the room
        rom.write_bytes(0x2F6DE1C + boss.flag_index, bytearray([slot.flag])) # Write the room's flag onto the new boss so the room still works properly
        var_a = 0
        var_b = 0
        x_pos = 0
        y_pos = 0

        if boss == "Flying Armor":
            var_a = 1
            var_b = 1
            x_pos = (room.width * 0x100) / 2 # Center horizontally
            y_pos = 0x50
        elif boss == "Balore":
            var_a = 1
            x_pos = 0x10
            y_pos = 0xB0
        elif boss == "Malphas":
            x_pos = (room.width * 0x100) / 2 # Center horizontally
        elif boss == "Dimitrii":
            ?????
        elif boss == "Dario":
            ??????
        elif boss == "Puppet Master":
            var_a = 1
            x_pos = 0x100
            y_pos = 0x60
            if room == "Demon Guest House": # If the room is vanilla, move him over for the shifted wall
                x_pos = 0x148
            elif room == "Subterranean Hell":
                y_pos = 0x70 # Move him down a bit so he's easier to hit in the tall room

            if room != "Demon Guest House": # Update hardcoded position for some extra entities
                ????
        elif boss == "Rahab":
            ????
        elif boss == "Gergoth":
            if room == "Condemned Tower":
                var_a = 1 # Falling Gergoth, for breaking the tower floors
        elif boss == "Zephyr":
            x_pos = (room.width * 0x100) / 2 # Center horizontally
            if room.room_width > 1:
                var_a = 1 # Normal Zephyr; Boss Rush is used to skip the scene if the room isn't wide enough.
        elif boss == "Bat Company":
            var_a = 1
            var_b = 0
        elif boss == "Paranoia":
            var_a = 2
            x_pos = 0x1F
            y_pox = 0x80
        elif boss == "Death":
            var_a = 1
            var_b = 1
            x_pos = (room.width * 0x100) / 2 # Center horizontally
            y_pos = 0x50
        elif boss == "Abaddon":
            var_a = 1
            x_pos = 0x80
            y_pos = 0xB0
        
        # The X/Y pos here are overrides. If none is specified, use the vanilla value
        if x_pos:
            rom.write_bytes([room.boss_address_pointer, struct.pack("H", x_pos)])

        if y_pos:
            rom.write_bytes([room.boss_address_pointer + 2, struct.pack("H", y_pos)])

        rom.write_bytes([room.boss_address_pointer + 8, var_a])
        rom.write_bytes([room.boss_address_pointer + 10, var_b])





# NOTES!
# Bosses need to check the new flag when spawning, too...
# - i should think of how I want to handle Boss Seals. Should I change the seal on the boss, or neither? Seals should match the doors. Make sure to handle this for Seal Rando
# - I need to swap the souls around so that their assigned soul matches the original boss's soul.
# - Flying Armor (and maybe other bosses) apparently require a soul drop, so they might not work in Dimitrii/Dario room
# - I might be able to randomize Aguni, but I will need to make sure the replacement spawns in the Mirror World.
# - Scale stats for what area they're in? I can maybe do order math here. Just replace them with the original boss's stats
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
# ON second thought, it might be that Dimitrii/Dario's rooms don't open after beating them. I wonder if maybe I can hook into the Julius Mode check that skips their cutscenes
# Consider NOPing out 0x02300808, which creates Balore's ice blocks after defeat
# Dario 2 probably SPAWNS aguni manually, and the one in the room is probably used for Julius mode. yes. aguni isnt even in.
# I just realized having a different boss in the mirror is going to fuck with the overlays REALLY REALLY BAD. FIGURE THAT OUT.
# Set SPAWN flags
# Balore in LV is WEIRD, he tries to spawn on the left side of the room, the camera's fucked up. hmm. can i fix this?
# There's code called LoadOverlay. Maybe I can call this during the Mirror transition?
# For room-center bosses, X pos is room_with * 100 / 2
# Boss Rush versions don't play music. Hmmm?
# - Delete the Right boss door in th e Throne room
# Get Aguni's address
# Set the Boss THrone flag
# Update death's scene radius in Rahab's room
# Figure out how to place bosses pls
# Consider the fact that I want to handle Seals through this. I should always run this code, just make sure bosses are vanilla if off.

 #     game.fs.write(0x0230282C, [0xE3A06D06].pack("V")) # mov r6, 180h increase death's search height
#      game.fs.write(0x02302838, [0xE3E02D06].pack("V")) # mvn r2, 180h (aka -181, can't do -180 because that constant won't fit)

# I want to check the cutscene actors for Dario/Dimitrii's fight. I want to add a condition where if Boss Shuffle is on, unset the boss flag if the defeat flag is set.

# CURRENT NOTES!
# Dario loads his flag dynamically. I need to figure out where that comes from and make sure I only change the flag for Dario 1, and leave Dario 2 alone.

# - Fix the flags. The first one (whatever address) should be 0x02 specifically to fix the battle
# - Make sure to reset the InBoss flag and the BossThrone flag when leaving the room
# - Failsafe for the orb to spawn near Soma if the actual coordinates didn't load
# - I need to get rid of the left wall in P.M's room



# TODO!
    # Change souls
    # Fix Dario/Dimitrii's room to open the doors anyways?
    # Fix Dario flag
    # Fix throne room
    # Move puppet master's shit
    # Fix Puppet Master's wall if needed
    # Move orb spawn coords