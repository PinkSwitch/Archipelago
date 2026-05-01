from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Rom import world_version

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class PoRClient(BizHawkClient):
    game = "Castlevania: Portrait of Ruin"
    system = ("NDS")
    patch_suffix = ".apcvpor"
    most_recent_connect: str = ""
    client_version: str = world_version

    def __init__(self) -> None:
        super().__init__()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            game_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 0x12, "ROM")])
            game_id = game_id[0].decode("ascii")
            if game_id != "CASTLEVANIA2ACBEA4":
                return False  # Only check Portrtait roms

            validation_data = await bizhawk.read(ctx.bizhawk_ctx, [(0x308F20, 0x20, "Main RAM")])
            patch_version = validation_data[0]
            patch_version = patch_version[0x15:].split(bytes(1), 1)[0].decode("ascii")
            if patch_version != self.client_version:
                if patch_version != self.most_recent_connect:
                    # We only want to display this error once
                    ctx.gui_error("Bad Version", f"Installed APworld for Portrait of ruin is {self.client_version}.")
                    self.most_recent_connect = patch_version

        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        print("NOT DONE YET")