
def shuffle_enemies(world):
    print("NOT IMPLEMENTED")


def apply_enemy_shuffle(rom):
    enemy_group_pointers = []
    for i in range(0x01E2):
        enemy_group_pointers.append(
            int.from_bytes(rom.read_bytes(0x10C615 + (i * 8), 4)) #to do, not in right byte order
        )
    for pointer in enemy_group_pointers:
        print(hex(pointer))