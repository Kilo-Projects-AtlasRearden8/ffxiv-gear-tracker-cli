"""Tally logic for gear entries."""

from __future__ import annotations

from typing import Dict, List

from gear_tracker.models import GearEntry


def tally_by_slot(entries: List[GearEntry]) -> Dict[str, dict]:
    """Summarize entries grouped by gear slot.

    Returns a dict mapping slot name to stats:
        count, avg_item_level, sources (source -> count), materia_count
    """
    grouped: Dict[str, List[GearEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.slot, []).append(entry)

    result: Dict[str, dict] = {}
    for slot, slot_entries in grouped.items():
        levels = [e.item_level for e in slot_entries if e.item_level]
        avg_level = round(sum(levels) / len(levels), 2) if levels else 0
        sources: Dict[str, int] = {}
        materia_count = 0
        for e in slot_entries:
            sources[e.source] = sources.get(e.source, 0) + 1
            materia_count += len(e.materia)
        result[slot] = {
            "count": len(slot_entries),
            "avg_item_level": avg_level,
            "sources": sources,
            "materia_count": materia_count,
        }
    return result


def tally_totals(entries: List[GearEntry]) -> dict:
    """Overall totals across all entries."""
    levels = [e.item_level for e in entries if e.item_level]
    sources: Dict[str, int] = {}
    materia_count = 0
    for e in entries:
        sources[e.source] = sources.get(e.source, 0) + 1
        materia_count += len(e.materia)
    return {
        "total_entries": len(entries),
        "avg_item_level": round(sum(levels) / len(levels), 2) if levels else 0,
        "sources": sources,
        "materia_count": materia_count,
    }
