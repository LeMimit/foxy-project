# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
import sys

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Dict
from typing import TypedDict
from typing import cast


if sys.version_info >= (3, 11):
    from tomllib import loads as load_toml
else:
    from tomli import loads as load_toml

if TYPE_CHECKING:
    from pathlib import Path

    from typing_extensions import TypeAlias

TOML_RESULT: TypeAlias = Dict[str, Any]
TOML_LOADER: TypeAlias = Callable[[str], TOML_RESULT]


def read_toml_content(path: Path, default: TOML_RESULT | None = None) -> TOML_RESULT:
    try:
        data = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        if default is None:
            raise

        logging.debug("%s missing, presuming default %r", path, default)
        return default
    else:
        return load_toml(data)


class _CheatTomlData(TypedDict):
    cheat: dict[str, Any]


def load_toml_or_inline_map(data: str | None) -> dict[str, Any]:
    """
    load toml data - with a special hack if only a inline map is given
    """
    if not data:
        return {}
    if data[0] == "{":
        data = "cheat=" + data
        loaded: _CheatTomlData = cast(_CheatTomlData, load_toml(data))
        return loaded["cheat"]
    return load_toml(data)
