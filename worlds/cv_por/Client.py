from typing import TYPE_CHECKING
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Rom import world_version
import struct

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class PoRClient(BizHawkClient):
    game = "Castlevania: Portrait of Ruin"
    system = "NDS"
    patch_suffix = ".apcvpor"
    most_recent_connect: str = ""
    client_version: str = world_version
    has_received_death: bool = False
    has_reset_from_death: bool = True
    seen_events_bitfield: int = 0
    cur_map: int = 0

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            game_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 0x12, "ROM")])
            game_id = game_id[0].decode("ascii")
            if game_id != "CASTLEVANIA2ACBEA4":
                return False  # Only check Portrtait roms

            validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x308F20, 0x20, "Main RAM"),
                                                                           (0x0E537C, 0x04, "Main RAM")])
            vanilla_check = struct.unpack("I", validation_data[1])[0]  # post-behemoth entity pointer
            if vanilla_check == 0x2304ee8:  # rando changes this; if we get this value, it's vanilla
                if self.most_recent_connect != "Vanilla ROM":
                    ctx.gui_error("Unrandomized ROM", f"Loaded ROM appears to be unmodified. Please load a Castlevania: Portrait of Ruin Archipelago ROM.")
                    self.most_recent_connect = "Vanilla ROM"
                return False

            patch_version = validation_data[0]
            patch_version = patch_version[0x15:].split(bytes(1), 1)[0].decode("ascii")
            if patch_version != self.client_version:
                if patch_version != self.most_recent_connect:
                    # We only want to display this error once
                    ctx.gui_error("Bad Version", f"Installed APWorld for Portrait of Ruin is {self.client_version}. ROM was generated using version {patch_version}.")
                    self.most_recent_connect = patch_version
                return False

            post_validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x309187, 0x01, "Main RAM")])

            death_link_flag = int.from_bytes(post_validation_data[0])
            if death_link_flag:
                await ctx.update_death_link(True)

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
            ctx.bizhawk_ctx, [(0x308F20, 0x14, "Main RAM")])

        slot_name_bytes = slot_name_bytes[0].rstrip(b'\x00')
        ctx.auth = slot_name_bytes.decode("ascii")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"]:
            self.has_received_death = True

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
                    (0x0F6284, 0x01, "Main RAM"),  # Game State
                    (0x1119E0, 4, "Main RAM"),  # Clock Time
                    (0x111F51, 1, "Main RAM"),  # Game Mode
                    (0x111BB8, 0x19F, "Main RAM"),  # Location flags
                    (0x111EAC, 0x25, "Main RAM"),  # Quest data
                    (0x308ED0, 2, "Main RAM"),  # Received Item
                    (0x308ED2, 2, "Main RAM"),  # Total items
                    (0x1119DC, 4, "Main RAM"),  # Boss defeat flags
                    (0x11174C, 4, "Main RAM"),  # State bitfield
                    (0x111BA8, 1, "Main RAM"),  # Elevator Switch
                    (0x111785, 1, "Main RAM"),  # Current Map ID
        ])

        menu_states = [0x05, 0x0A, 0x12, 0x14, 0x13, 0x16, 0x15, 0x1B]
        game_state = read_state[0][0]
        clock_time = struct.unpack("I", read_state[1])[0]
        game_mode = read_state[2][0]
        boss_death_flags = struct.unpack("I", read_state[7])[0]
        game_status = struct.unpack("I", read_state[8])[0]

        if not clock_time or game_state in menu_states or game_mode:
            #  Clock time will be 0 if a file hasn't been booted.
            #  Don't read data if we're on one of the title screens
            #  If the game mode is not 0, we've laoded something other than John/Charlotte
            return

        if "DeathLink" in ctx.tags and game_state == 2 and not game_status & 0x100081:
            await self.handle_deathlink(game_status, ctx)

        await self.check_locations(read_state, ctx)
        await self.give_items(read_state, ctx)
        await self.check_events(read_state, ctx)
        if not ctx.finished_game and boss_death_flags & 0x20000:  # Dracula's defeat flag
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def check_locations(self, read_state, ctx):
        new_checks = []
        location_flags = read_state[3]
        quest_flags = read_state[4]

        from .static_location_data import location_ids, location_data_table
        for location_name in location_ids:
            loc_id = location_ids[location_name]
            if loc_id not in ctx.server_locations:
                continue
            data = location_data_table[location_name]
            if loc_id not in ctx.locations_checked:
                if data.location_type == "Quest":
                    quest_id = loc_id - 0x200
                    quest_state = quest_flags[quest_id]
                    if quest_state & 0x08:  # Bit that a quest has been completed
                        new_checks.append(loc_id)
                else:
                    offset = int(loc_id / 8)
                    bit = int(1 << (loc_id % 8))
                    flag = location_flags[offset]
                    if flag & bit:
                        new_checks.append(loc_id)

            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                # location = ctx.location_names.lookup_in_slot(new_check_id)
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

    async def give_items(self, read_state, ctx):
        currently_processed_item_type = read_state[5][1]
        items_from_server = struct.unpack("H", read_state[6])[0]

        if items_from_server < len(ctx.items_received) and not currently_processed_item_type:
            item = ctx.items_received[items_from_server]
            items_from_server += 1
            item_data = struct.pack("H", item.item)
            await bizhawk.write(ctx.bizhawk_ctx, [(0x308ED0, item_data, "Main RAM"),
                                                  (0x308ED2, bytes([items_from_server]), "Main RAM")])

    async def handle_deathlink(self, current_death_state, ctx):
        if current_death_state & 0x40:  # If the player is currently dead
            if self.has_received_death:  # This is the death that we just got from the server
                self.has_received_death = False
                self.has_reset_from_death = False
            else:  # Received death is false, meaning the player actually died here
                if self.has_reset_from_death:  # We only want this to run once per death
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} died!")
                    self.has_reset_from_death = False
        else:
            if self.has_received_death:
                current_death_state |= 0x40
                # Kill the player
                await bizhawk.write(ctx.bizhawk_ctx, [(0x11174C, struct.pack("I", current_death_state), "Main RAM"),
                                                       (0x11216C, struct.pack("H", 0), "Main RAM")])  # Player's HP
            else:
                # This should be normal gameplay after relaoding
                self.has_reset_from_death = True

    async def check_events(self, read_state, ctx):
        boss_death_flags = struct.unpack("I", read_state[7])[0]
        elevator_switch = read_state[9][0]
        map_id = read_state[10][0]
        events_key = f"cv_por_events_{ctx.team}_{ctx.slot}"

        if map_id != self.cur_map:
            await ctx.send_msgs(
                [{
                    "cmd": "Set",
                    "key": f"{events_key}",
                    "default": {"map_id": 0},
                    "want_reply": True,
                    "operations": [{"operation": "update", "value": {"map_id": map_id}}],
                }])
            self.cur_map = map_id

        events = [
            # We don't really need everyone, just people who lock quests/portrait clears. But who cares?
            (elevator_switch  >> 4 ) & 1, # Elevator Switch Flipped
            (boss_death_flags >> 0 ) & 1,
            (boss_death_flags >> 1 ) & 1, # Dullahan
            (boss_death_flags >> 2 ) & 1, # Behemoth
            (boss_death_flags >> 3 ) & 1,
            (boss_death_flags >> 4 ) & 1, # Keremt
            (boss_death_flags >> 5 ) & 1, # Legion
            (boss_death_flags >> 6 ) & 1, # Dagon
            (boss_death_flags >> 7 ) & 1, # Astarte
            (boss_death_flags >> 8 ) & 1, # Werewolf
            (boss_death_flags >> 9 ) & 1, # The Creature
            (boss_death_flags >> 10) & 1, # Mummy Man
            (boss_death_flags >> 11) & 1, # Medusa
            (boss_death_flags >> 12) & 1, # Richter
            (boss_death_flags >> 13) & 1, # Stella
            (boss_death_flags >> 14) & 1, # Stella & Loretta
            (boss_death_flags >> 15) & 1, # Brauner
            (boss_death_flags >> 16) & 1, # Death
            (boss_death_flags >> 17) & 1,
            (boss_death_flags >> 18) & 1, # Dracula
            (boss_death_flags >> 19) & 1, # Balore
            (boss_death_flags >> 20) & 1, # Gergoth
            (boss_death_flags >> 21) & 1, # Zephyr
            (boss_death_flags >> 22) & 1, # Aguni
            (boss_death_flags >> 23) & 1, # Abaddon
            (boss_death_flags >> 24) & 1, # Trevor, Grant and Sypha? idk it didn't proc for me
            (boss_death_flags >> 25) & 1, # Doppelganger
        ]
        event_bitfield = 0
        for i, event in enumerate(events):
            event_bitfield |= event << i
        if event_bitfield != self.seen_events_bitfield:
            await ctx.send_msgs(
                [{
                    "cmd": "Set",
                    "key": f"{events_key}",
                    "default": {"events": 0},
                    "want_reply": True,
                    "operations": [{"operation": "update", "value": {"events": event_bitfield}}],
                }])
            self.seen_events_bitfield = event_bitfield
