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
        return False


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        print("NOT DONE YET")