from typing import TYPE_CHECKING
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Rom import world_version
import struct

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class CV2Client(BizHawkClient):
    game = "Castlevania II: Simon's Quest"
    system = "NES"
    patch_suffix = ".apcv2"
    most_recent_connect: str = ""
    client_version: str = world_version

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            mem = await bizhawk.get_memory_size(ctx.bizhawk_ctx, "PRG ROM")
            print(mem)
            if mem < 0x20000:
                self.most_recent_connect = "Invalid Size"
                return False  # Non-MMC1 roms

            game_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x1FFE9, 7, "PRG ROM")])
            game_id = game_id[0].decode("ascii")
            if game_id != "CASTLE2":
                return False

            validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0xDD00, 0x10, "PRG ROM")])

            vanilla_check = struct.unpack("I", validation_data[0][0:4])[0]  # Extended data pointers

            if vanilla_check == 0xFFFFFFFF:  # If this is nothing, it means it wasn't patched
                if self.most_recent_connect != "Vanilla ROM":
                    ctx.gui_error("Unrandomized ROM", f"Loaded ROM appears to be unmodified. Please load a Castlevania II Archipelago ROM.")
                    self.most_recent_connect = "Vanilla ROM"
                return False

            patch_version = validation_data[0]
            patch_version = patch_version.rstrip(b'\xFF').decode("ascii")
            if patch_version != self.client_version:
                if patch_version != self.most_recent_connect:
                    # We only want to display this error once
                    ctx.gui_error("Bad Version", f"Installed APWorld for Castlevania II is {self.client_version}. ROM was generated using version {patch_version}.")
                    self.most_recent_connect = patch_version
                return False

            ctx.game = self.game
            ctx.items_handling = 0b101
            ctx.locations_checked = set()
            return True

        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = await bizhawk.read(
            ctx.bizhawk_ctx, [(0xDD10, 0x20, "PRG ROM")])

        slot_name_bytes = slot_name_bytes[0].rstrip(b'\xFF')
        ctx.auth = slot_name_bytes.decode("ascii")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
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

        read_state = await bizhawk.read(ctx.bizhawk_ctx, [
            (0x18, 1, "RAM"),  # Game Mode
            (0x10, 1, "WRAM"),  # Current item
            (0x11, 2, "WRAM"),  # Total items received
            (0x30, 0x0F, "WRAM"),  # Location flags
        ])
        game_mode = read_state[0]

        if game_mode[0] not in [0x05, 0x0A]:
            # Return if we're not in gameplay or the ending
            return

        await self.check_locations(read_state, ctx)
        await self.give_items(read_state, ctx)

        if game_mode == 0x0A and (not ctx.finished_game):
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    @staticmethod
    async def check_locations(read_state, ctx):
        new_checks = []
        location_flags = read_state[3]

        from .static_location_data import location_ids
        for location_name in location_ids:
            loc_id = location_ids[location_name]
            if loc_id not in ctx.server_locations:
                continue
            if loc_id not in ctx.locations_checked:
                offset = int(loc_id / 8)
                bit = int(1 << (loc_id % 8))
                flag = location_flags[offset]
                if flag & bit:
                    new_checks.append(loc_id)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

    @staticmethod
    async def give_items(read_state, ctx):
        currently_processed_item = read_state[1][0]
        items_from_server = struct.unpack("H", read_state[2])[0]

        if items_from_server < len(ctx.items_received) and not currently_processed_item:
            item = ctx.items_received[items_from_server]
            items_from_server += 1
            item_data = bytearray([item.item])
            print(item_data)
            await bizhawk.write(ctx.bizhawk_ctx, [(0x10, item_data, "WRAM"),
                                                  (0x11, struct.pack("H", items_from_server), "WRAM")])