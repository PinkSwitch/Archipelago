import struct
import random
import json
import pkgutil
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

# ============================================================================
# TEIL 1: DNA-STRUKTUR NACH GEGNER-SPEZIFIKATION (DOKUMENT 5)
# ============================================================================

@dataclass
class EnemyDataBlock:
    """
    Bildet die exakte 36-Byte (0x24) Struktur eines Gegners im 
    ARM9-Arbeitsspeicher von Castlevania: Dawn of Sorrow ab.
    """
    enemy_id: int
    rom_offset: int                 
    create_code_pointer: bytes      # 0x00 (4 Bytes) -> Verhaltens-KI Startcode
    sprite_update_pointer: bytes    # 0x04 (4 Bytes) -> Grafik-Update-Routine
    item1_id: int                   # 0x08 (2 Bytes) -> Drop-Item 1
    item2_id: int                   # 0x0A (2 Bytes) -> Drop-Item 2
    petrify_palette: int            # 0x0C (1 Byte)  -> Farbpalette bei Versteinerung
    gfx_set_id: int                 # 0x0D (1 Byte)  -> GFX-Page im VRAM
    hp: int                         # 0x0E (2 Bytes) -> Maximale Lebenspunkte
    mp: int                         # 0x10 (2 Bytes) -> Maximale Magiepunkte
    exp: int                        # 0x12 (2 Bytes) -> Erfahrungspunkte bei Abschuss
    soul_drop_chance: int           # 0x14 (1 Byte)  -> Wert für Seelen-Drop
    atk: int                        # 0x15 (1 Byte)  -> Angriffs-Wert
    def_: int                       # 0x16 (1 Byte)  -> Abwehr-Wert
    item_drop_chance: int           # 0x17 (1 Byte)  -> Wert für Item-Drop
    unknown_space: int              # 0x18 (2 Bytes) -> Unbekannt / Reserviert
    soul_local_id: int              # 0x1A (1 Byte)  -> Lokale Seelen-ID (FF = Keine)
    set_mode_slots: int             # 0x1B (1 Byte)  -> Kosten im Enemy Set Mode
    weaknesses: int                 # 0x1C (4 Bytes) -> Elementar-Schwächen (Bitfeld)
    resistances: int                # 0x20 (4 Bytes) -> Elementar-Resistenzen (Bitfeld)

@dataclass
class DoSEnemy:
    enemy_id: int
    rom_offset: int
    data: EnemyDataBlock

CONF_BALANCED_STATS = True  

REQUIRED_ENEMY_OVERLAYS: Set[int] = {
    0x0E, 0x12, 0x19, 0x22, 0x25, 0x2F, 0x4D, 0x51, 0x5B, 0x5D, 0x61, 0x64
}

# ============================================================================
# TEIL 2: CORE ENGINE - INITIALISIERUNG
# ============================================================================

class EnemyRandomizer:
    def __init__(self, rom):
        self.enemies: Dict[int, DoSEnemy] = {}
        self.mappings: Dict[int, int] = {}  
        
        from ..Rom import get_base_rom_bytes, file_pointers
        base_rom_data = get_base_rom_bytes()
        arm9_info = file_pointers["arm9"]
        
        BASE_ENEMY_FILE_OFFSET = 0x7CCAC 
        
        for enemy_id in range(0x65):
            file_address = arm9_info.rom_address + BASE_ENEMY_FILE_OFFSET + (enemy_id * 0x24)
            
            create_ptr = bytes(base_rom_data[file_address + 0x00 : file_address + 0x04])
            sprite_ptr = bytes(base_rom_data[file_address + 0x04 : file_address + 0x08])
            
            gfx_set = base_rom_data[file_address + 0x0D]
            hp = int.from_bytes(base_rom_data[file_address + 0x0E : file_address + 0x10], byteorder='little')
            mp = int.from_bytes(base_rom_data[file_address + 0x10 : file_address + 0x12], byteorder='little')
            exp = int.from_bytes(base_rom_data[file_address + 0x12 : file_address + 0x14], byteorder='little')
            soul_chance = base_rom_data[file_address + 0x14]
            atk = base_rom_data[file_address + 0x15]
            def_ = base_rom_data[file_address + 0x16]
            item_chance = base_rom_data[file_address + 0x17]
            soul_id = base_rom_data[file_address + 0x1A]
            
            data = EnemyDataBlock(
                enemy_id=enemy_id, rom_offset=(BASE_ENEMY_FILE_OFFSET + (enemy_id * 0x24) + 0x02000000),
                create_code_pointer=create_ptr, sprite_update_pointer=sprite_ptr,
                item1_id=0, item2_id=0, petrify_palette=0,
                gfx_set_id=gfx_set, hp=hp, mp=mp, exp=exp,
                soul_drop_chance=soul_chance, atk=atk, def_=def_,
                item_drop_chance=item_chance, unknown_space=0,
                soul_local_id=soul_id, set_mode_slots=0, weaknesses=0, resistances=0
            )
            self.enemies[enemy_id] = DoSEnemy(enemy_id=enemy_id, rom_offset=(BASE_ENEMY_FILE_OFFSET + (enemy_id * 0x24) + 0x02000000), data=data)

    def generate_random_mapping(self, world_random):
        pool_ids = list(self.enemies.keys())
        shuffled_ids = pool_ids.copy()
        while shuffled_ids == pool_ids:
            world_random.shuffle(shuffled_ids)
        self.mappings = dict(zip(pool_ids, shuffled_ids))
        print("[DNA-Engine] Gegner-Mischverzeichnis live generiert.")

    def patch_rom_enemy_dna(self, rom):
        ARM9_RAM_BASE = 0x02000000
        BASE_ENEMY_ADDRESS = ARM9_RAM_BASE + 0x7CCAC 
        OVERLAY_41_RAM_START = 0x02308920
        SAFE_GFX_CACHE_RAM = OVERLAY_41_RAM_START + 0x3F00

        fallback_table_bytes = []
        for enemy_id in range(0x65):
            enemy_behavior = self.enemies[enemy_id].data
            fallback_table_bytes.extend(list(enemy_behavior.sprite_update_pointer))
            
        rom.write_to_file(SAFE_GFX_CACHE_RAM, "overlay_41", fallback_table_bytes)

        for original_id, new_id in self.mappings.items():
            original_slot_data = self.enemies[original_id].data
            new_enemy_behavior = self.enemies[new_id].data
            file_base_address = BASE_ENEMY_ADDRESS + (original_id * 0x24)
            
            if new_id in REQUIRED_ENEMY_OVERLAYS:
                custom_sprite_ram_pointer = SAFE_GFX_CACHE_RAM + (original_id * 4)
                rom.write_to_file(file_base_address + 0x04, "arm9", list(custom_sprite_ram_pointer.to_bytes(4, byteorder='little')))
                rom.write_to_file(custom_sprite_ram_pointer, "overlay_41", list(new_enemy_behavior.sprite_update_pointer))
            else:
                rom.write_to_file(file_base_address + 0x04, "arm9", list(new_enemy_behavior.sprite_update_pointer))
                
            rom.write_to_file(file_base_address + 0x00, "arm9", list(new_enemy_behavior.create_code_pointer)) 
            rom.write_to_file(file_base_address + 0x1A, "arm9", [new_enemy_behavior.soul_local_id])          

            if CONF_BALANCED_STATS:
                # Wir würfeln einen zufälligen Faktor zwischen 0.75 (-25%) und 1.50 (+50%)
                stat_multiplier = random.uniform(0.75, 1.50)
                
                # Wir nehmen die Werte des neuen Gegners und skalisieren sie dynamisch
                scaled_hp = max(1, int(new_enemy_behavior.hp * stat_multiplier))
                scaled_exp = max(1, int(new_enemy_behavior.exp * stat_multiplier))
                
                rom.write_to_file(file_base_address + 0x0E, "arm9", list(struct.pack("<H", scaled_hp)))
                rom.write_to_file(file_base_address + 0x10, "arm9", list(struct.pack("<H", original_slot_data.mp)))
                rom.write_to_file(file_base_address + 0x12, "arm9", list(struct.pack("<H", scaled_exp)))
                rom.write_to_file(file_base_address + 0x15, "arm9", [max(1, int(new_enemy_behavior.atk * stat_multiplier))])
                rom.write_to_file(file_base_address + 0x16, "arm9", [max(0, int(new_enemy_behavior.def_ * stat_multiplier))])

            else:
                rom.write_to_file(file_base_address + 0x0E, "arm9", list(struct.pack("<H", new_enemy_behavior.hp)))
                rom.write_to_file(file_base_address + 0x10, "arm9", list(struct.pack("<H", new_enemy_behavior.mp)))
                rom.write_to_file(file_base_address + 0x12, "arm9", list(struct.pack("<H", new_enemy_behavior.exp)))
                rom.write_to_file(file_base_address + 0x15, "arm9", [new_enemy_behavior.atk])
                rom.write_to_file(file_base_address + 0x16, "arm9", [new_enemy_behavior.def_])
                
            rom.write_to_file(file_base_address + 0x14, "arm9", [new_enemy_behavior.soul_drop_chance]) 
            rom.write_to_file(file_base_address + 0x17, "arm9", [new_enemy_behavior.item_drop_chance])
# ============================================================================
# TEIL 4: SPEZIFIKATIONS-TREUER ENTITY-INJEKTOR (FIXED: BASIS-ROM INTERFACE)
# ============================================================================

# ============================================================================
# TEIL 4: SPEZIFIKATIONS-TREUER ENTITY-INJEKTOR (FIXED: BASIS-ROM INTERFACE)
# ============================================================================

def write_enemies(world, rom, mode="normal"):
    from ..Rom import file_pointers, get_base_rom_bytes
    import json
    import pkgutil
    import os
    
    randomizer = EnemyRandomizer(rom)
    randomizer.generate_random_mapping(world.random)
    base_rom_bytes = get_base_rom_bytes()

    try:
        binary_rooms = pkgutil.get_data("worlds.cv_dos.modules", "room_pointer_extracted.json")
        room_data = json.loads(binary_rooms.decode("utf-8"))
    except Exception:
        current_dir = os.path.dirname(__file__)
        with open(os.path.join(current_dir, "room_pointer_extracted.json"), "r", encoding="utf-8") as f:
            room_data = json.load(f)

    print("[Archipelago] Injiziere Zufallsgegner direkt über die Hauptdatei (arm9)...")

    real_file = "arm9"
    if real_file not in file_pointers:
        print("[Fehler] 'arm9' wurde nicht in den file_pointers gefunden!")
        return
        
    pointer_info = file_pointers[real_file]
    arm9_ram_base = pointer_info.base_address  # Das ist 0x02000000
    arm9_rom_start = pointer_info.rom_address # Das ist 0x4000

    for room in room_data:
        if room.get("Notes") == "nicht randomizen" or not room.get("Room_pointer"):
            continue
            
        area_string = room["Area"]
        room_header_ram = int(room["Room_pointer"], 16)

        try:
            # 1. DEIN SCHRITT: Den JSON-Raumpointer holen und 0x02000000 abziehen
            relative_offset = room_header_ram - arm9_ram_base
            header_file_idx = sum([arm9_rom_start, relative_offset])
                
            if sum([header_file_idx, 31]) >= len(base_rom_bytes):
                continue

            # 2. DEIN SCHRITT: Zum Room-Header bei 9F11C gelangen und die 8 Nullen prüfen
            if base_rom_bytes[header_file_idx : header_file_idx + 8] != b"\x00\x00\x00\x00\x00\x00\x00\x00":
                continue
                    
            # 3. DEIN SCHRITT: Über das Header-Format 0x14 Bytes vorwärts gehen
            ptr_idx = sum([header_file_idx, 20])
                
            val0 = base_rom_bytes[ptr_idx]
            val1 = base_rom_bytes[ptr_idx + 1] * 256
            val2 = base_rom_bytes[ptr_idx + 2] * 65536
            val3 = base_rom_bytes[ptr_idx + 3] * 16777216
            entity_list_ram_ptr = sum([val0, val1, val2, val3])
                
            # 4. DEIN SCHRITT: Zum ersten Entity-Eintrag (0x020A0D4C) springen
            if entity_list_ram_ptr > 0:
                list_relative_offset = entity_list_ram_ptr - arm9_ram_base
                current_rom_idx = sum([arm9_rom_start, list_relative_offset])
                current_entity_ram_addr = entity_list_ram_ptr
                enemies_patched_in_room = 0
                
                while True:
                    if sum([current_rom_idx, 11]) >= len(base_rom_bytes):
                        break
                            
                    # Wir lesen die ersten 2 Bytes als 16-Bit-Wert (Little Endian)
                    m0 = base_rom_bytes[current_rom_idx]
                    m1 = base_rom_bytes[current_rom_idx + 1] * 256
                    end_marker = sum([m0, m1])
                        
                    # DEINE KORREKTUR: Wenn der Marker FF 7F (0x7FFF) erreicht wird -> Liste beenden!
                    if end_marker == 0x7FFF:
                        break
                            
                    # DEIN SCHRITT: Bei Offset +5 nach Typ 01 (Enemy) suchen
                    entity_type = base_rom_bytes[sum([current_rom_idx, 5])]
                        
                    if entity_type == 1:
                        # DEIN SCHRITT: Wenn gefunden, den Subtyp bei Offset +6 holen (Gegner-ID)
                        current_enemy_id = base_rom_bytes[sum([current_rom_idx, 6])]
                        
                        # DEIN SCHRITT: Nur ändern, wenn er innerhalb von 00 bis 64 (Hex / 100 Dezimal) liegt!
                        if 0 <= current_enemy_id <= 100:
                            # DEIN SCHRITT: Den neuen Gegner aus der Mapping-Tabelle holen
                            new_enemy_id = randomizer.mappings.get(current_enemy_id, current_enemy_id)
                                
                            # DEIN SCHRITT: Den neuen Gegner in die ROM-Datei schreiben
                            rom.write_to_file(sum([current_entity_ram_addr, 6]), "arm9", [new_enemy_id])
                            enemies_patched_in_room += 1
                    
                    # HIER IST DIE KORREKTUR: Diese beiden Zeilen rücken nach links!
                    # Sie müssen exakt bündig unter dem "if entity_type == 1:" stehen!
                    current_rom_idx += 12
                    current_entity_ram_addr += 12

                if enemies_patched_in_room > 0:
                    print(f"[Erfolg] Raum {hex(room_header_ram)} ({area_string}): {enemies_patched_in_room} Gegner erfolgreich randomisiert.")
                                
        except Exception as e:
            print(f"[Fehler] Raum {hex(room_header_ram)} ({area_string}): {e}")
            import tracebacktrace
            back.print_exc()
            continue

 

    randomizer.patch_rom_enemy_dna(rom)
    print("[Mod-Mischer] Gegner-Randomizer erfolgreich abgeschlossen!")
