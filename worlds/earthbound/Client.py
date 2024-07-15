import logging
import struct
import typing
import time
from struct import pack, unpack
from .local_data import check_table, client_specials
from .text_data import eb_text_table

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

EB_ROMHASH_START = 0x00FFC0
ROMHASH_SIZE = 0x15

ITEMQUEUE_HIGH = WRAM_START + 0xF686
ITEM_RECEIVED = WRAM_START + 0xF680
SPECIAL_RECEIVED = WRAM_START + 0xF682
SAVE_FILE = WRAM_START + 0xB4A1
GIYGAS_CLEAR = WRAM_START + 0x9C11
GAME_CLEAR = WRAM_START + 0x9C85
NPC_TEX_PONTER = WRAM_START + 0xF68E
OPEN_WINDOW = WRAM_START + 0x8958
PRESENT_TEXT_POINTER = WRAM_START + 0xF68C
OSS_FLAG = WRAM_START + 0x5D98
MELODY_TABLE = WRAM_START + 0x9C1E


class EarthBoundClient(SNIClient):
    game = "EarthBound"
    patch_suffix = ".apeb"

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom_name = await snes_read(ctx, EB_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name[:6] != b"MOM2AP":
            return False

        ctx.command_processor.commands["disable_oss_flag"] = cmd_disable_oss_flag
        ctx.command_processor.commands["kill"] = kill
        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.rom = rom_name
        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        giygas_clear = await snes_read(ctx, GIYGAS_CLEAR, 0x1)
        game_clear = await snes_read(ctx, GAME_CLEAR, 0x1)
        item_received = await snes_read(ctx, ITEM_RECEIVED, 0x1)
        special_received = await snes_read(ctx, SPECIAL_RECEIVED, 0x1)
        save_num = await snes_read(ctx, SAVE_FILE, 0x1)
        text_open = await snes_read(ctx, OPEN_WINDOW, 1)
        oss_status = await snes_read(ctx, OSS_FLAG, 1)
        melody_table = await snes_read(ctx, MELODY_TABLE, 2)

        rom = await snes_read(ctx, EB_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            return
        
        if giygas_clear[0] & 0x01 == 0x01: #Are we in the epilogue
            return

        if save_num[0] == 0x00: #If on the title screen
            return

        if game_clear[0] & 0x01 == 0x01: #Goal should ignore the item queue and textbox check
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        if text_open[0] != 0xFF: #Don't check locations or items while text is printing, but scouting is fine
            return

        if ctx.slot is None:
            return

        new_checks = []
        from .local_data import check_table


        location_ram_data = await snes_read(ctx, WRAM_START + 0x9C00, 0x88)
        for loc_id, loc_data in check_table.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0]]
                masked_data = data & (1 << loc_data[1])
                bit_set = masked_data != 0
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    new_checks.append(loc_id)
        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_slot(new_check_id)
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        if item_received[0] or special_received[0] != 0x00: #If processing any item from the server
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
                snes_buffered_write(ctx, WRAM_START + 0xF680, bytes([item_id]))
            else:
                snes_buffered_write(ctx, WRAM_START + 0xF682, bytes([client_specials[item_id]]))
                    
        await snes_flush_writes(ctx)

def cmd_disable_oss_flag(self, cmd: str = ""):
    from SNIClient import snes_buffered_write
    """Disables the OSS flag. Used for debugging as a failsafe"""
    if self.ctx.game != "EarthBound":
        print("This command can only be used while playing EarthBound")
        return
    print("Disabling OSS!")
    snes_buffered_write(self.ctx, OSS_FLAG, bytes([0x00]))

def kill(self, cmd: str = ""):
    from SNIClient import snes_buffered_write
    """Kills the player"""
    if self.ctx.game != "EarthBound":
        print("This command can only be used while playing EarthBound")
        return
    snes_buffered_write(self.ctx, WRAM_START + 0x9A13, bytes([0x00, 0x00, 0x00, 0x00]))
    snes_buffered_write(self.ctx, WRAM_START + 0x9A72, bytes([0x00, 0x00, 0x00, 0x00]))
    snes_buffered_write(self.ctx, WRAM_START + 0x9AD1, bytes([0x00, 0x00, 0x00, 0x00]))
    snes_buffered_write(self.ctx, WRAM_START + 0x9B30, bytes([0x00, 0x00, 0x00, 0x00]))