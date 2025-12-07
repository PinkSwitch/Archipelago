from typing import TYPE_CHECKING

from NetUtils import ClientStatus
from .in_game_data import location_ram_table, global_soul_table, world_version
from .static_location_data import location_ids
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import time
import struct

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class DoSClient(BizHawkClient):
    game = "Castlevania: Dawn of Sorrow"
    system = ("NDS")
    patch_suffix = ".apcvdos"
    most_recent_connect: str = ""
    client_version: str = world_version

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:

        try:
            # Check ROM name/patch version
            rom_names = await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 18, "ROM"), # Original ROM name
                                                            (0x308A6C, 0x14, "Main RAM")]) # AP ROM name

            patch_data = await bizhawk.read(ctx.bizhawk_ctx, [(???, 15, "ROM")])  # APworld version in the patch

            base_rom_name = rom_names[0].decode("ascii")
            patch_version = patch_data[0].rstrip(b"\x69")
            patch_version = patch_version.decode("ascii")

            if patch_version != self.most_recent_connect and patch_version != self.client_version:
                ctx.gui_error("Bad Version", f"Installed Dawn of Sorrow APworld version {self.client_version} does not match patch version {patch_version}")
                self.most_recent_connect = apworld_version
                return False

            if not base_rom_name.startswith("CASTLEVANIA1ACVEA4"):
                return False

            
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b101
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:

        slot_name_bytes = await bizhawk.read(
            ctx.bizhawk_ctx, [(0x2F6DD50, 0x14, "ROM")])

        slot_name_bytes = slot_name_bytes[0].rstrip(b'\xFF')
        ctx.auth = slot_name_bytes.decode("ascii")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from CommonClient import logger
        from .in_game_data import location_ram_table

        if ctx.server_version.build > 0:
            ctx.connected = True
        else:
            ctx.connected = False
            ctx.refresh_connect = True

        if ctx.slot_data is not None:
            ctx.data_present = True
        else:
            ctx.data_present = False

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return


        read_state = await bizhawk.read(ctx.bizhawk_ctx, [(0x0F7190, 0x10, "Main RAM"), # Check table
                                                          (0x0F7257, 0x01, "Main RAM"), # Game Mode
                                                          (0x11504C, 0x01, "Main RAM"), #Current Map
                                                          (0x0F703C, 0x04, "Main RAM"), #Gameplay timer. Will be 0 if not in game
                                                           (0x308930, 0x20, "Main RAM")]) #AP data


        location_flag_table = bytearray(read_state[0])
        game_mode = int.from_bytes(read_state[1], "little")
        cur_map = int.from_bytes(read_state[2], "little")
        game_timer = int.from_bytes(read_state[3], "little")
        ap_data = bytearray(read_state[4])

        soul_flag_table = list(ap_data[:0x10])
        current_received_item = ap_data[0x10]
        total_items_received = int.from_bytes(ap_data[0x1E:0x20], "little")

        new_checks = []

        if game_mode == 1:  # Ignore AP handling if the game is in Julius mode
            return

        if not game_timer: # The in-game itmer is only 0 when not in-game
            return

        for location_name in location_ids:
            loc_id = location_ids[location_name]
            if loc_id not in ctx.locations_checked:
                if location_name in global_soul_table:
                    index = global_soul_table.index(location_name)
                    bit = 1 << (index % 8)
                    offset = int(index / 8)
                    print(f"We are using {offset}")
                    location = soul_flag_table[offset]
                else:
                    pointer = location_ram_table[location_name][0]
                    bit = location_ram_table[location_name][1]
                    location = location_flag_table[pointer]

                if location & bit:
                    new_checks.append(loc_id)
                
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_slot(new_check_id)
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

        if total_items_received < len(ctx.items_received) and current_received_item == 0:
            item = ctx.items_received[total_items_received]
            total_items_received += 1
            item_data = struct.pack(">H", item.item)
            await bizhawk.write(ctx.bizhawk_ctx, [(0x308940, item_data, "Main RAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x30894E, bytes([total_items_received]), "Main RAM")])

        if not ctx.finished_game and cur_map == 0x0D:  # Map 0x0D is used for the Epilogue. If we're here, trigger goal
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])
