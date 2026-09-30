"""Small value types shared across the bot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Slot:
    """An available appointment offered by the portal."""

    hub: str  # vaccination centre
    when: datetime
    dose: int = 1

    def __str__(self) -> str:
        return f"{self.when:%d/%m/%Y %H:%M} @ {self.hub}"
