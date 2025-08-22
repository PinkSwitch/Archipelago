import logging
import struct
import typing
import traceback
import uuid
from struct import pack
from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, logger, gui_enabled
import Patch
import Utils
import asyncio
from . import SSBMWorld
import dolphin_memory_engine as dme
from .Helper_Functions import StringByteFunction as sbf
from typing import Optional

from NetUtils import ClientStatus, color

CONNECTION_LOST_STATUS = "Dolphin connection was lost. Please restart your emulator and make sure SSBM is running."
CONNECTION_FAILED_STATUS = "Unable to connect to Dolphin. Ensure Dolphin is running and SSBM is loaded."
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."
CONNECTION_REFUSED_GAME_STATUS = "Dolphin failed to connect. Ensure your randomized Melee patch is running. Trying again in 5 seconds..."

AUTH_ID_ADDRESS = 0x803BAC5C #
GAME_SEED_ADDRESS = 0x803BAC6A

def read_bytes(console_address: int, length: int):
    return int.from_bytes(dme.read_bytes(console_address, length))

def read_bytearray(console_address: int, length: int):
    return bytearray(dme.read_bytes(console_address, length))


def read_table(console_address: int, length: int) -> list[int]:
    return list(dme.read_bytes(console_address, length))


def write_short(console_address: int, value: int):
    dme.write_bytes(console_address, value.to_bytes(2))


def read_string(console_address: int, strlen: int):
    return sbf.byte_string_strip_null_terminator(dme.read_bytes(console_address, strlen))


def check_if_addr_is_pointer(addr: int):
    return 2147483648 <= dme.read_word(addr) <= 2172649471


async def write_bytes_and_validate(addr: int, ram_offset: list[str] | None, curr_value: bytes) -> None:
    if not ram_offset:
        dme.write_bytes(addr, curr_value)
    else:
        dme.write_bytes(dme.follow_pointers(addr, ram_offset), curr_value)

class SSBMCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Melee client commands.

    This class handles commands specific to Melee.
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
        if isinstance(self.ctx, SSBMClient):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

class SSBMClient(CommonContext):
    command_processor = SSBMCommandProcessor 
    game = "Super Smash Bros. Melee"
    patch_suffix = ".xml"
    items_handling = 0b111
    slot_data: dict | None = {}

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        # Handle various Dolphin connection related tasks
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.locations_checked = set()

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Super Smash Bros. Melee Archipelago Client"
        return ui

    async def disconnect(self, allow_autoreconnect: bool = False):
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super(SSBMClient, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            if dme.is_hooked():
                logger.info("A game is playing in dolphin, waiting to verify additional details...")
            return
        await self.send_connect()

    async def ssbm_check_locations(self, auth):
        new_checks = []
        from . import in_game_data
        from .static_location_data import location_ids
        bonus_checks = in_game_data.bonus_checks
        trophy_checks = in_game_data.trophy_checks
        event_checks = in_game_data.event_checks
        mode_clears = in_game_data.mode_clears
        flag_checks = in_game_data.flag_checks

        bonus_table = read_table(0x8045C348, 0x20)
        trophy_table = read_table(0x8045C394, 0x249)
        event_table = read_table(0x8045C129, 0x7)
        special_flag_table = read_table(0x8045C20C, 7)
        auth_id = read_bytearray(AUTH_ID_ADDRESS, 25)
        auth_id = auth_id.decode("ascii").rstrip("\x00")

        if auth_id == auth:  #Authenticate we're in the same room so savestates don't override checks
            for location, (entry, bit) in bonus_checks.items():
                if location not in self.locations_checked and bonus_table[entry] & bit:
                    new_checks.append(location)

            for location in trophy_checks:
                check_id = location_ids[location]
                trophy = trophy_table[(trophy_checks[location] - 1) * 2]
                if trophy & 0x80:
                    new_checks.append(check_id)

            for location, (entry, bit) in event_checks.items():
                if location not in self.locations_checked and event_table[entry] & bit:
                    new_checks.append(location)

            for location in mode_clears:
                target_check = read_bytes(mode_clears[location], 1)
                if target_check & 0x80:
                    new_checks.append(location)

            for location, (entry, bit) in flag_checks.items():
                if location not in self.locations_checked and special_flag_table[entry] & bit:
                    new_checks.append(location)

                            
            for new_check_id in new_checks:
                self.locations_checked.add(new_check_id)
                
        await self.check_locations(self.locations_checked)

async def dolphin_sync_task(ctx: SSBMClient):
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.slot:
                    await ctx.ssbm_check_locations(ctx.auth)
                    #await ctx.lm_update_non_savable_ram()
                else:
                    if not ctx.auth:
                        auth_id = read_bytearray(AUTH_ID_ADDRESS, 25)
                        ctx.auth = auth_id.decode("ascii").rstrip("\x00")
                        if not ctx.auth:
                            ctx.auth = None
                            ctx.awaiting_rom = False
                            logger.info("No slot name was detected. Ensure a randomized ROM is loaded, " +
                                        "retrying in 5 seconds...")
                            ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                            dme.un_hook()
                            await asyncio.sleep(5)
                            continue
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS

                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if not dme.is_hooked():
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_FAILED_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue

                logger.info(CONNECTION_CONNECTED_STATUS)
                ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                ctx.locations_checked = set()
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


async def give_player_items(ctx: SSBMClient):
    print("nuh uh")


def launch(connect=None, password=None):
    server_address: str = ""


    async def _main(connect, password):
        ctx = SSBMClient(server_address if server_address else connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")
        ctx.give_item_task = asyncio.create_task(give_player_items(ctx), name="GiveItemFunc")

        await ctx.exit_event.wait()
        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

        if ctx.give_item_task:
            await ctx.give_item_task

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(_main(connect, password))
    colorama.deinit()