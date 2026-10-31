"""JSON storage for gear entries."""

from __future__ import annotations

import json
import os
from typing import List

from gear_tracker.models import GearEntry


class GearStore:
    """Persists gear entries to a local JSON file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def load(self) -> List[GearEntry]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(raw, list):
            return []
        entries: List[GearEntry] = []
        for item in raw:
            if isinstance(item, dict):
                entries.append(GearEntry.from_dict(item))
        return entries

    def save(self, entries: List[GearEntry]) -> None:
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        data = [entry.to_dict() for entry in entries]
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def add(self, entry: GearEntry) -> List[GearEntry]:
        entries = self.load()
        entries.append(entry)
        self.save(entries)
        return entries

    def remove(self, entry_id: str) -> bool:
        entries = self.load()
        filtered = [e for e in entries if e.id != entry_id]
        if len(filtered) == len(entries):
            return False
        self.save(filtered)
        return True
