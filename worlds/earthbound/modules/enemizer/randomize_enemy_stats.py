from .enemy_attributes import excluded_enemies

def randomize_enemy_stats(world, rom):
    for enemy in world.enemies:
        if enemy not in excluded_enemies and " (" not in enemy:
            world.enemies[enemy].hp = world.random.randint(10, 900)
            if world.random.randint(1,100) < 20:
                world.enemies[enemy].pp = int(world.random.randint(10, 500) / 2)
            else:
                world.enemies[enemy].pp = 0
            world.enemies[enemy].offense = world.random.randint(1, 200)
            world.enemies[enemy].defense = world.random.randint(1, 200)
            world.enemies[enemy].speed = world.random.randint(10, 65)
            world.enemies[enemy].level = world.random.randint(10, 70)
            world.enemies[enemy].exp = world.random.randint(10, 62000)
            print(f"HAHAHA! {world.enemies[enemy].name}! {world.enemies[enemy].exp}")
            world.enemies[enemy].money = world.random.randint(10, 1000)
            guts = world.random.randint(1,255)
            luck = world.random.randint(1,255)
            rom.write_bytes(world.enemies[enemy].address + 0x3D, bytearray([guts]))
            rom.write_bytes(world.enemies[enemy].address + 0x3E, bytearray([luck]))
            if world.enemies[enemy].attack_extensions > 0:
                world.enemies[f"{enemy} (2)"].hp = world.enemies[enemy].hp
                world.enemies[f"{enemy} (2)"].pp = world.enemies[enemy].pp
                world.enemies[f"{enemy} (2)"].offense = world.enemies[enemy].offense
                world.enemies[f"{enemy} (2)"].defense = world.enemies[enemy].defense
                world.enemies[f"{enemy} (2)"].speed = world.enemies[enemy].speed
                world.enemies[f"{enemy} (2)"].level = world.enemies[enemy].level
                world.enemies[f"{enemy} (2)"].exp = world.enemies[enemy].exp
                world.enemies[f"{enemy} (2)"].money = world.enemies[enemy].money
                rom.write_bytes(world.enemies[f"{enemy} (2)"].address + 0x3D, bytearray([guts]))
                rom.write_bytes(world.enemies[f"{enemy} (2)"].address + 0x3E, bytearray([luck]))
                