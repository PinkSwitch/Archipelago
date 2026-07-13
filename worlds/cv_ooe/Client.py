from typing import TYPE_CHECKING
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Rom import world_version
import struct

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class OoEClient(BizHawkClient):
    game = "Castlevania: Order of Ecclesia"
    system = "NDS"
    patch_suffix = ".apcvooe"
    most_recent_connect: str = ""
    client_version: str = world_version

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            game_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 0x12, "ROM")])
            game_id = game_id[0].decode("ascii")
            if game_id != "CASTLEVANIA3YR9EA4":
                return False  # Only check Ecclesia roms

            validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x2EB200, 0x20, "Main RAM"),
                                                                   (0x09D774, 0x04, "Main RAM")])
            vanilla_check = struct.unpack("I", validation_data[1])[0]  # Extended data pointers
            if vanilla_check != 0xE1A00000:  # NOP'd out in rando for extended data. If not present, assume vanilla
                if self.most_recent_connect != "Vanilla ROM":
                    ctx.gui_error("Unrandomized ROM", f"Loaded ROM appears to be unmodified. Please load a Castlevania: Order of Ecclesia Archipelago ROM.")
                    self.most_recent_connect = "Vanilla ROM"
                return False

            patch_version = validation_data[0]
            patch_version = patch_version[0x15:].split(bytes(1), 1)[0].decode("ascii")
            if patch_version != self.client_version:
                if patch_version != self.most_recent_connect:
                    # We only want to display this error once
                    ctx.gui_error("Bad Version", f"Installed APWorld for Order of Ecclesia is {self.client_version}. ROM was generated using version {patch_version}.")
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
            ctx.bizhawk_ctx, [(0x2EB200, 0x14, "Main RAM")])

        slot_name_bytes = slot_name_bytes[0].rstrip(b'\x00')
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
                    (0x223E00, 4, "Main RAM"),  # Start of Overlay 22
                    (0x100790, 1, "Main RAM"),  # Game Mode
                    (0x100398, 0x19F, "Main RAM"),  # Location flags
                    (0x2EB1B0, 2, "Main RAM"),  # Received Item
                    (0x2EB1B2, 2, "Main RAM"),  # Total items
        ])
        game_mode = read_state[1][0]  # If the game mode is non-zero, return
        overlay22_entry = struct.unpack("I", read_state[0])[0]

        if game_mode or overlay22_entry != 0xE3A00064:
            #  We don't want to run AP if the game mode isn't regular Shanoa mode.
            #  Aditionally, overlay 22 is loaded while we're in game, so if it's not loaded, don't do anything
            return

        await self.check_locations(read_state, ctx)
        await self.give_items(read_state, ctx)

    @staticmethod
    async def check_locations(read_state, ctx):
        new_checks = []
        location_flags = read_state[2]

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
                # location = ctx.location_names.lookup_in_slot(new_check_id)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])


    @staticmethod
    async def give_items(read_state, ctx):
        currently_processed_item = struct.unpack("H", read_state[3])[0]
        items_from_server = struct.unpack("H", read_state[4])[0]

        if items_from_server < len(ctx.items_received) and not currently_processed_item:
            item = ctx.items_received[items_from_server]
            items_from_server += 1
            item_data = struct.pack("H", item.item)
            await bizhawk.write(ctx.bizhawk_ctx, [(0x2EB1B0, item_data, "Main RAM"),
                                                  (0x2EB1B2, struct.pack("H", items_from_server), "Main RAM")])