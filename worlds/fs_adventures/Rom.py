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
    from . import FSAdventuresWorld


def apply_patch(world, basepatch, output):
    from jinja2 import Template
    template = Template(basepatch)
    result = template.render(DUNGEONS=world.maidens_required)
    return result
    