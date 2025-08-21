import os
import Utils
import typing
import struct
import settings
import zipfile
from worlds.Files import APAutoPatchInterface
from typing import TYPE_CHECKING, Optional, Any
from logging import warning
from typing_extensions import override

if TYPE_CHECKING:
    from . import SSBMWorld


def apply_patch(world, basepatch, output):
    from jinja2 import Template
    template = Template(basepatch)
    if world.options.lottery_pool_mode:
        disable_class_upgrades = True
    else:
        disable_class_upgrades = False
        
    result = template.render(
            PLAYER_NAME = world.player_name,
            GAME_FILE_NAME = world.encoded_slot_name,
            SLOT_NUM = world.player,
            AUTH_ID = world.authentication_id,
            CSTICK_SMASH_SOLO = world.options.solo_cstick_smash,
            #ENCODED_PLAYER_NAME = world.encoded_slot_name,
            TROPHYCLASS_IN_POOl = disable_class_upgrades)
    return result
    