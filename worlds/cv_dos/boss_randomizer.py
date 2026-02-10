

@dataclass
class DoSBoss:
    flag: int # The SLOT's Boss Defeated flag.
    assigned_soul: int # Which Soul is assigned to the SLOT's original boss. Soul randomization reworks how souls are given so this needs to stay the same.
    floor_height: int # The SLOT's room floor height
    room_width: int # The SLOT's room width
    flag_address_pointer: int # Pointer to where the boss's Death Flag is applied
    boss_address_pointer: int # Which adress we write to to place the boss
    old_boss: str # The SLOT's original boss
    new_boss: str = "NULL" # Which boss has been randomized to be here

def randomize_bosses(world):
    world.boss_slots = {
        "Lost Village": DoSBoss(0x02, 0x35, 1, 2, 0x3817F8, 0x, "Flying Armor"),  # Flying Armor
        "Wizardry Lab": DoSBoss(0x04, 0x74, 1, 1, 0x364874, 0x, "Balore"),  # Balore
        "Dark Chapel": DoSBoss(0x08, 0xFF, 1, 2, 0x3B3B4C, 0x, "Dimitrii"), # Dimitrii
        "Dark Chapel 2": DoSBoss(0x10, 0x75, 2, 2, 0x37E920, 0x, "Malphas"),  # Malphas
        "Garden of Madness": DoSBoss(0x20, 0xFF, 1, 2, 0x187FD4, 0x, "Dario"),  # Dario 1 Make sure this is the right address for the flag. Seems low.
        "Demon Guest House": DoSBoss(0x40, 0x00, 1, 2, 0x36AA04, 0x, "Puppet Master"),  # Puppet Master
        "Condemned Tower": DoSBoss(0x80, 0x57, 1, 1, 0x30E920, 0x, "Gergoth"),  # Gergoth
        "Cursed Clock Tower": DoSBoss(0x0200, 0x01, 1, 2, 0x38D198, 0x, "Zephyr"),  # Zephyr | 2C
        "Subterranean Hell": DoSBoss(0x0100, 0x77, 1, 2, 0x37054C, 0x, "Rahab"),  # Rahab | 1C
        "Silenced Ruins": DoSBoss(0x0400, 0x36, 1, 1, 0x, 0x, "Bat Company"),  # Bat Company
        "Demon Guest House Upper": DoSBoss(0x1000, 0x02, 1, 1, 0x, 0x, "Paranoia"), # Paranoia
        "The Pinnacle": DoSBoss(0x0800, 0x2B, 1, 2, 0x, 0x, "Aguni"), # Aguni, not Dario 2
        "Mine of Judgement": DoSBoss(0x2000, 0x58, 1, 2, 0x, 0x, "Death"), # Death
        "The Abyss": DoSBoss(0x8000, 0x2C, 1, 1, 0x, 0x, "Abaddon") # Abaddon
    }
      # TODO! Have bosses check the NEW flag when spawning, as well as when being defeated
      # Instead of what I was doing before. Have a list of all the bosses in order. Use the index, and have a Base Address where the flags START.
      # Did Puppet Master set his flag TWICE?



    # Balore needs to have a 1-tile floor
    # Puppet master needs a 2-tile room
    # Rahab needs a 2-tile room
    # Malphas, Dimitrii, Dario, Gergoth, Zephyr, Paranoia, and Abaddon cannot spawn in Rahab's room


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
# - I need to change the Defeat flag to the ORIGINAL boss's defeat flag so that I don't have to change the door at all
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


# CURRENT NOTES!
# I have all of the boss Set flags done. I need to test that they all work. Going down the list, I'm at Puppet master currently.
# Puppet master sets flag 0x40 AFTER the call, so im gonna need to fix that. Maybe I can just NOP it and be fine? 022FFF4C
# I just realized I'm going to need to go through every. single. boss. again. And make sure they're CHECKING the new flag when spawning.
# I should make THAT into a subroutine