"""CSV export for gear entries."""

from __future__ import annotations

import csv
from typing import List

from gear_tracker.models import GearEntry

FIELDNAMES = [
    "id",
    "slot",
    "item_name",
    "item_level",
    "materia",
    "source",
    "date",
    "notes",
]


def export_csv(entries: List[GearEntry], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for entry in entries:
            row = entry.to_dict()
            row["materia"] = ";".join(row["materia"])
            writer.writerow(row)
