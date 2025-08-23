import logging
import struct
import typing
import traceback
import uuid
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
LAST_RECV_ITEM_ADDR = 0x8045C368
COIN_COUNTER = 0x8045C10A
TROPHY_COUNT = 0x8045C390
MENU_ID = 0x80479D30
AP_CHAR_UNLOCKS = 0x80001e40 #TODO!!! MOVE THIS SOMEWHERE PERMANENT!
SECRET_CHAR_ADDRESS = 0x8045BF28
SECRET_STAGE_ADDRESS = 0x8045BF2A
AP_EVENT_COUNTER = 0x80001E0F  #TODO!!! MOVE THIS SOMEWHERE PERMANENT!
LOTTERY_POOL_UPGRADES = 0x80001e44 #TODO!!! MOVE THIS SOMEWHERE PERMANENT!

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
    trophy_total: "Label" = None

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

    async def draw_trophy_counter(self):
        # KivyMD support, also keeps support with regular Kivy (hopefully)
        try:
            from kvui import MDLabel as Label
        except ImportError:
            from kvui import Label

        if not self.trophy_total:
            self.trophy_total = Label(text=f"", size_hint_x=None, width=120, halign="center")
            self.ui.connect_layout.add_widget(self.trophy_total)

        read_trophy_count = int.from_bytes(dme.read_bytes(TROPHY_COUNT, 2))
        self.trophy_total.text = f"Trophies: {read_trophy_count}/50"

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

    def on_package(self, cmd: str, args: dict):
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        super().on_package(cmd, args)
        if cmd == "Connected":  # On Connect
            self.total_trophies_required = int(args["slot_data"]["trophies_required"])
            self.giga_bowser_goal = bool(args["slot_data"]["giga_bowser_required"])
            self.crazy_hand_required = bool(args["slot_data"]["crazy_hand_goal"])
            self.event_51_required = bool(args["slot_data"]["goal_evn_51"])
            self.all_events_required = bool(args["slot_data"]["goal_all_events"])
            self.all_targets_required = bool(args["slot_data"]["targets_required"])

    async def ssbm_check_locations(self, auth):
        new_checks = []
        from . import in_game_data
        from .static_location_data import location_ids
        bonus_checks = in_game_data.bonus_checks
        trophy_checks = in_game_data.trophy_checks
        event_checks = in_game_data.event_checks
        mode_clears = in_game_data.mode_clears
        flag_checks = in_game_data.flag_checks
        trophy_owned_checks = in_game_data.trophy_owned_checks

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

            for location in trophy_owned_checks:
                check_id = location_ids[location]
                trophy = trophy_table[((trophy_owned_checks[location] - 1) * 2) + 1]
                if trophy:
                    new_checks.append(check_id)

            for new_check_id in new_checks:
                self.locations_checked.add(new_check_id)
                
        await self.check_locations(self.locations_checked)

    async def give_majors(self, auth):
        from .in_game_data import global_trophy_table, coin_items, secret_characters, all_characters, secret_stages, mode_items, lottery_pool_static
        current_menu = int.from_bytes(dme.read_bytes(MENU_ID, 1))
        auth_id = read_bytearray(AUTH_ID_ADDRESS, 25)
        auth_id = auth_id.decode("ascii").rstrip("\x00")
        if current_menu != 0x0C and auth_id == auth:
            event_packs = 0
            for item in self.items_received:
                name = self.item_names.lookup_in_game(item.item)
                if name not in coin_items and name not in global_trophy_table:
                    if name in secret_characters:
                        item_bit = (1 << secret_characters.index(name))
                        secret_chars = int.from_bytes(dme.read_bytes(SECRET_CHAR_ADDRESS, 2))
                        secret_chars |= item_bit
                        secret_chars = struct.pack(">H", secret_chars)
                        dme.write_bytes(SECRET_CHAR_ADDRESS, secret_chars)

                    if name in all_characters:
                        item_bit = (1 << all_characters.index(name))
                        unlocked_characters = int.from_bytes(dme.read_bytes(AP_CHAR_UNLOCKS, 4))
                        unlocked_characters |= item_bit
                        unlocked_characters = struct.pack(">I", unlocked_characters)
                        dme.write_bytes(AP_CHAR_UNLOCKS, unlocked_characters)

                    if name in secret_stages:
                        item_bit = (1 << secret_stages.index(name))
                        stages = int.from_bytes(dme.read_bytes(SECRET_STAGE_ADDRESS, 2))
                        stages |= item_bit
                        stages = struct.pack(">H", stages)
                        dme.write_bytes(SECRET_STAGE_ADDRESS, stages)

                    if name in mode_items:
                        item_bit = (2 << mode_items.index(name))
                        modes = int.from_bytes(dme.read_bytes(AP_CHAR_UNLOCKS, 1))
                        modes |= item_bit
                        modes = modes.to_bytes(1, "big")
                        dme.write_bytes(AP_CHAR_UNLOCKS, modes)

                    event_total = sum(1 for item in self.items_received if item.item == 0x2B)
                    event_total = min(event_total, 8)
                    event_total = event_total.to_bytes(1, "big")
                    dme.write_bytes(AP_EVENT_COUNTER, event_total)

                    lottery_total = 0
                    lottery_bit = 0
                    lottery_pool_total = sum(1 for item in self.items_received if item.item == 0x151)
                    lottery_pool_total = min(lottery_pool_total, 4)
                    for i in range(lottery_pool_total):
                        lottery_bit |= 0x10 << lottery_pool_total
                    lottery_total |= lottery_bit

                    if name in lottery_pool_static:
                        item_bit = (0x10 << lottery_pool_static.index(name))
                        lottery_pool = int.from_bytes(dme.read_bytes(LOTTERY_POOL_UPGRADES, 1))
                        lottery_pool |= item_bit
                        lottery_pool = lottery_pool.to_bytes(1, "big")
                        dme.write_bytes(LOTTERY_POOL_UPGRADES, lottery_pool)


                #you are here

                
                
        await self.check_locations(self.locations_checked)

async def dolphin_sync_task(ctx: SSBMClient):
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.slot:
                    if ctx.ui:
                        await ctx.draw_trophy_counter()
                    await ctx.ssbm_check_locations(ctx.auth)
                    await ctx.give_majors(ctx.auth)
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
    from .in_game_data import coin_items, global_trophy_table
    async def wait_for_next_loop(time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    while not ctx.exit_event.is_set():
        if not (dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS):
            await wait_for_next_loop(5)
            continue

        menu_id = int.from_bytes(dme.read_bytes(MENU_ID, 1))
        if menu_id == 0x0D:
            continue

        last_recv_idx = int.from_bytes(dme.read_bytes(LAST_RECV_ITEM_ADDR, 4))
        if len(ctx.items_received) == last_recv_idx:
            await wait_for_next_loop(0.5)
            continue

        recv_items = ctx.items_received[last_recv_idx:]
        for item in recv_items:
            name = ctx.item_names.lookup_in_game(item.item)
            if name in coin_items:
                coin_count = int.from_bytes(dme.read_bytes(COIN_COUNTER, 2))
                coin_count += coin_items[name]
                coin_count = struct.pack(">H", coin_count)
                dme.write_bytes(COIN_COUNTER, coin_count)
            elif name in global_trophy_table:
                trophy_index = global_trophy_table.index(name)
                trophy_amount = int.from_bytes(dme.read_bytes(0x8045C395 + (trophy_index * 2), 1))
                if not trophy_amount:
                    trophy_counter = int.from_bytes(dme.read_bytes(TROPHY_COUNT, 2))
                    trophy_counter += 1
                    trophy_counter = struct.pack(">H", trophy_counter)
                    dme.write_bytes(TROPHY_COUNT, trophy_counter)
                trophy_amount = 1
                dme.write_byte(0x8045C395 + (trophy_index * 2), trophy_amount)

            last_recv_idx += 1
            dme.write_word(LAST_RECV_ITEM_ADDR, last_recv_idx)
        await wait_for_next_loop(0.5)


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