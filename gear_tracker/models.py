"""Gear tracker data models."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class GearEntry:
    """A single logged piece of FFXIV gear."""

    id: str
    slot: str
    item_name: str
    item_level: int
    materia: List[str] = field(default_factory=list)
    source: str = ""
    date: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "GearEntry":
        return GearEntry(
            id=str(data.get("id", "")),
            slot=str(data.get("slot", "")),
            item_name=str(data.get("item_name", "")),
            item_level=int(data.get("item_level", 0)),
            materia=list(data.get("materia", [])),
            source=str(data.get("source", "")),
            date=str(data.get("date", "")),
            notes=str(data.get("notes", "")),
        )
