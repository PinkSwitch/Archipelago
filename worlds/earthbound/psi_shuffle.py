import struct

def shuffle_psi(world):
    world.offensive_psi_slots = [
        "Special",
        "Flash",
        "Fire",
        "Freeze",
        "Thunder",
        "Starstorm",
        "Blast",
        "Missile"
    ]

    world.assist_psi_slots = [
        "Hypnosis",
        "Paralysis",
        "Offense Up",
        "Defense Down",
        "Brainshock"
    ]

    world.shield_slots = [
        "Shield",
        "PSI Shield"
    ]
    #Can I shuffle shield with regular assists?

    world.jeff_offense_items = []

    world.psi_address = {
        "Special": [0x158A5F, 4],
        "Flash": [0x158B4F, 4],
        "Fire": [0x158A9B, 4],
        "Freeze": [0x158AD7, 4],
        "Thunder": [0x158B13, 4],
        "Starstorm": [0x3503FC, 4],

        "Shield": [0x158C21, 4],
        "PSI Shield": [0x158C5D, 4],

        "Hypnosis": [0x158CD5, 2],
        "Paralysis": [0x158D11, 2],
        "Offense Up": [0x158C99, 2],
        "Defense Down": [0x158CB7, 2],
        "Brainshock": [0x158D2F, 2],

        "Blast": [0x35041A, 4],
        "Missile": [0x350456, 4],
    }

    if world.options.psi_shuffle:
        world.random.shuffle(world.offensive_psi_slots)

        if world.options.psi_shuffle == 2:
            world.jeff_offense_items.extend(world.offensive_psi_slots[-2:])
            world.offensive_psi_slots = world.offensive_psi_slots[:-2]
        else:
            world.jeff_offense_items.extend(["Blast", "Missile"])

        world.random.shuffle(world.assist_psi_slots)
        world.random.shuffle(world.shield_slots)

        shield_data = {key: world.psi_address[key] for key in world.shield_slots}
        assist_data = {key: world.psi_address[key] for key in world.assist_psi_slots}
        world.psi_address = {key: world.psi_address[key] for key in world.offensive_psi_slots}
        world.psi_address.update(shield_data)
        world.psi_address.update(assist_data)
        print(world.offensive_psi_slots)
        print(world.jeff_offense_items)
    

    world.psi_slot_data = [
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Special
        [[0x09, 0x01], [0x0B, 0x01], [0x0D, 0x01], [0x0F, 0x01]], #Flash
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Fire
        [[0x09, 0x01], [0x0B, 0x01], [0x0D, 0x01], [0x0F, 0x01]], #Freeze
        [[0x09, 0x02], [0x0B, 0x02], [0x0D, 0x02], [0x0F, 0x02]], #Thunder
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Starstorm

        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Shield
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #PSI Shield

        [[0x09, 0x01], [0x0B, 0x01]], #Hypnosis
        [[0x09, 0x02], [0x0B, 0x02]], #Paralysis
        [[0x09, 0x01], [0x0B, 0x01]], #Offense Up
        [[0x09, 0x02], [0x0B, 0x02]], #Defense Down
        [[0x09, 0x01], [0x0B, 0x01]], #Brainshock

        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Blast
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]], #Missile
    ]
    world.psi_action_data = [
        [[0x0A, 0x00], [0x0B, 0x00], [0x0C, 0x00], [0x0D, 0x00]], #Special
        [[0x1A, 0x00], [0x1B, 0x00], [0x1C, 0x00], [0x1D, 0x00]], #Flash
        [[0x0E, 0x00], [0x0F, 0x00], [0x10, 0x00], [0x11, 0x00]], #Fire
        [[0x12, 0x00], [0x13, 0x00], [0x14, 0x00], [0x15, 0x00]], #Freeze
        [[0x16, 0x00], [0x17, 0x00], [0x18, 0x00], [0x19, 0x00]], #Thunder
        [[0x6F, 0x01], [0x70, 0x01], [0x1E, 0x00], [0x1F, 0x00]] #Starstorm
    ]
    world.psi_level_data = [
        [[0x08, 0x00, 0x00], [0x16, 0x00, 0x00], [0x31, 0x00, 0x00], [0x4B, 0x00, 0x00]], #Special
        [[0x12, 0x00, 0x00], [0x26, 0x00, 0x00], [0x3D, 0x00, 0x00], [0x43, 0x00, 0x00]], #Flash
        [[0x00, 0x03, 0x00], [0x00, 0x13, 0x00], [0x00, 0x25, 0x00], [0x00, 0x40, 0x00]], #Fire
        [[0x00, 0x01, 0x01], [0x00, 0x0B, 0x01], [0x00, 0x1F, 0x21], [0x00, 0x2E, 0x00]], #Freeze
        [[0x00, 0x08, 0x01], [0x00, 0x19, 0x01], [0x00, 0x39, 0x29], [0x00, 0x00, 0x37]], #Thunder
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]], #Starstorm

        [[0x0C, 0x00, 0x0E], [0x00, 0x00, 0x0F], [0x22, 0x00, 0x10], [0x00, 0x00, 0x33]], #Shield
        [[0x00, 0x06, 0x00], [0x00, 0x1B, 0x00], [0x00, 0x33, 0x00], [0x00, 0x3C, 0x00]], #PSI Shield

        [[0x04, 0x00, 0x00], [0x1B, 0x00, 0x00]], #Hypnosis
        [[0x0E, 0x00, 0x00], [0x1D, 0x00, 0x00]], #Paralysis
        [[0x00, 0x15, 0x00], [0x00, 0x28, 0x00]], #Offense Up
        [[0x00, 0x1D, 0x00], [0x00, 0x36, 0x00]], #Defense Down
        [[0x00, 0x00, 0x18], [0x00, 0x00, 0x2C]], #Brainshock

        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]], #Blast
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]], #Missile
        
    ]

    world.bomb_names = {
        "Special": ["Psycho bomb", "????"],
        "Flash": ["Flashbang", "????"],
        "Freeze": ["Ice bomb", "Dry ice bomb"],
        "Fire": ["Fire bomb", "Napalm bomb"],
        "Thunder": ["Electric bomb", "EMP bomb"],
        "Starstorm": ["Comet bomb", "?????"],
        "Blast": ["Bomb", "Super bomb"],
        "Missile": ["Rocket", "Super rocket"]

    }

    world.rocket_names = {
        "Special": ["????", "????", "????"],
        "Flash": ["Flashbang", "????", "????"],
        "Freeze": ["????", "????", "????"],
        "Fire": ["????", "????", "????"],
        "Thunder": ["????", "????", "????"],
        "Starstorm": ["????", "?????", "????"],
        "Blast": ["Grenade", "Big grenade", "Combat grenade"],
        "Missile": ["Bottle Rocket", "Big bottle rocket", "Multi»bottle rocket"]

    }

    world.starstorm_address = {
        "Special": [0x002D, 0x003C],
        "Flash": [0x011D, 0x012C],
        "Fire": [0x0069, 0x0078],
        "Freeze": [0x00A5, 0x00B4],
        "Thunder": [0x00E1, 0x00F0],
        "Starstorm": [0x013B, 0x014A]
    }

    world.starstorm_spell_id = {
        "Special": [0x03, 0x04],
        "Flash": [0x13, 0x14],
        "Fire": [0x07, 0x08],
        "Freeze": [0x0B, 0x0C],
        "Thunder": [0x0F, 0x10],
        "Starstorm": [0x15, 0x16]
    }

    world.jeff_addresses = [
        0x156665, #Bomb
        0x15668C, #Super Bomb
        0x1565F0, #Bottle Rocket
        0x156616, #Big Bottle Rocket
        0x15663E #multi Bottle Rocket

    ]

    world.jeff_item_counts = [
        2, #Bomb
        3 #Bottle Rocket
    ]

    world.jeff_item_names = [
        world.bomb_names,
        world.rocket_names
    ]


def write_psi(world, rom):
    from .text_data import text_encoder, eb_text_table
    psi_num = 0
    for key, (address, levels) in world.psi_address.items():
        for i in range(levels):
            rom.write_bytes(address + 9, bytearray(world.psi_slot_data[psi_num][i]))
            rom.write_bytes(address + 6, bytearray(world.psi_level_data[psi_num][i]))
            if psi_num == 0:
                rom.write_bytes(address, bytearray([0x01]))
            elif psi_num == 5 and i > 1:
                rom.write_bytes(0x01C4AB + (0x9E * (i - 2)), struct.pack("H", world.starstorm_address[key][i - 2]))
                rom.write_bytes(0x01C536 + (0x78 * (i - 2)), bytearray([world.starstorm_spell_id[key][i - 2]]))
                rom.write_bytes(0x2E957F + (0x11 * (i - 2)), bytearray([world.starstorm_spell_id[key][i - 2]]))
                rom.write_bytes(address + 9, bytearray(world.psi_slot_data[psi_num][i - 2]))

            if key == "Special" and psi_num != 0:
                rom.write_bytes(address, bytearray([0x12]))

            address += 15
            if key == "Starstorm" and i == 1:
                address = 0x158B8B
    #todo; expanded psi
    #todo; animation for Starstorm L/D
    #todo; swap enemy actions for Special?
        psi_num += 1

    jeff_item_num = 0
    jeff_item_index = 0
    for item in world.jeff_offense_items:
        for i in range(world.jeff_item_counts[jeff_item_num]):
            address = world.jeff_addresses[jeff_item_index]
            jeff_item_index += 1
            name = world.jeff_item_names[jeff_item_num][item][i]
            name = text_encoder(name, eb_text_table, 23)
        jeff_item_num += 1
