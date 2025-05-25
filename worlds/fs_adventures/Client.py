import logging
import struct
import typing
import time
import uuid
from struct import pack
from CommonClient import ClientCommandProcessor, CommonContext
import Utils
import asyncio

from NetUtils import ClientStatus, color


class FSACommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Four Swords Adventures client commands.

    This class handles commands specific to Four Swords Adventures.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status.
        """
        if isinstance(self.ctx, TWWContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

class FSAdventuresClient(CommonContext):
    game = "The Legend of Zelda: Four Swords Adventures"
    patch_suffix = ".apfsa"
    most_recent_connect: str = ""
    items_handling = 0b011

    async def validate_rom(self, ctx):
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, EB_ROMHASH_START, ROMHASH_SIZE)

        item_handling = await snes_read(ctx, ITEM_MODE, 1)
        if rom_name is None or rom_name[:6] != b"MOM2AP":
            return False

        ctx.game = self.game
        ctx.rom = rom_name


        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read, snes_write
        if rom != ctx.rom:
            ctx.rom = None
            return
        
        if giygas_clear[0] & 0x01 == 0x01:  # Are we in the epilogue
            return

        if save_num[0] == 0x00:  # If on the title screen
            return

        if ctx.slot is None:
            return

        if game_clear[0] & 0x01 == 0x01:  # Goal should ignore the item queue and textbox check
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        
        new_checks = []
        from .game_data.local_data import check_table

        location_ram_data = await snes_read(ctx, WRAM_START + 0x9C00, 0x88)
        for loc_id, loc_data in check_table.items():
            if loc_id not in ctx.locations_checked:
                if loc_id >= 0xEB1000:
                    data = shop_location_flags[loc_data[0]]
                else:
                    data = location_ram_data[loc_data[0]]
                masked_data = data & (1 << loc_data[1])
                bit_set = masked_data != 0
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit and loc_id in ctx.server_locations:
                    if text_open[0] == 0xFF or shop_scout[0]:  # Don't check locations while in a textbox
                        new_checks.append(loc_id)
                        
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_slot(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])
            await snes_write(ctx, [(WRAM_START + 0x0770, bytes([0]))])

        if item_received[0] or special_received[0] != 0x00 or money_received[0] != 0x00:  # If processing any item from the server
            return

        if cur_script[0]:  # Stop items during cutscenes
            return

        recv_count = await snes_read(ctx, ITEMQUEUE_HIGH, 2)
        recv_index = struct.unpack("H", recv_count)[0]
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            item_id = (item.item - 0xEB0000)
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_slot(item.item), "red", "bold"),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, ITEMQUEUE_HIGH, pack("H", recv_index))
            if item_id <= 0xFD:
                snes_buffered_write(ctx, WRAM_START + 0xB570, bytes([item_id]))
            elif item.name in money_item_table:
                snes_buffered_write(ctx, WRAM_START + 0xB5F1, bytes([list(money_item_table).index(item.name)]))
            else:
                snes_buffered_write(ctx, WRAM_START + 0xB572, bytes([client_specials[item_id]]))

        await snes_flush_writes(ctx)

def _patch_and_run_game(patch_file: str):
    try:
        metadata, output_file = Patch.create_rom_file(patch_file)
        Utils.async_start(_run_game(output_file))
        return metadata
    except Exception as exc:
        logger.exception(exc)
        Utils.messagebox("Error Patching Game", str(exc), True)
        return {}



def launch(*launch_args: str) -> None:
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
        args = parser.parse_args(launch_args)

        if args.patch_file != "":
            metadata = _patch_and_run_game(args.patch_file)
            if "server" in metadata:
                args.connect = metadata["server"]

        ctx = FSAdventuresClient(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        watcher_task = asyncio.create_task(_game_watcher(ctx), name="GameWatcher")

        try:
            await watcher_task
        except Exception as e:
            logger.exception(e)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("Four Swords Adventures Client", exception_logger="Client")
    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()