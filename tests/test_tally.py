"""Tests for tally logic."""

from gear_tracker.models import GearEntry
from gear_tracker.tally import tally_by_slot, tally_totals


def _entry(slot: str, item_level: int, source: str, materia=None) -> GearEntry:
    return GearEntry(
        id="x",
        slot=slot,
        item_name="item",
        item_level=item_level,
        materia=materia or [],
        source=source,
    )


def test_tally_by_slot_groups_and_counts():
    entries = [
        _entry("head", 600, "tomestone"),
        _entry("head", 610, "raid"),
        _entry("chest", 590, "crafted"),
    ]
    result = tally_by_slot(entries)
    assert set(result) == {"head", "chest"}
    assert result["head"]["count"] == 2
    assert result["chest"]["count"] == 1


def test_tally_by_slot_avg_item_level():
    entries = [_entry("head", 600, "a"), _entry("head", 620, "a")]
    assert tally_by_slot(entries)["head"]["avg_item_level"] == 610


def test_tally_by_slot_sources_and_materia():
    entries = [
        _entry("head", 600, "tomestone", ["Materia I", "Materia II"]),
        _entry("head", 610, "tomestone", []),
        _entry("head", 590, "raid", ["Materia III"]),
    ]
    stats = tally_by_slot(entries)["head"]
    assert stats["sources"] == {"tomestone": 2, "raid": 1}
    assert stats["materia_count"] == 3


def test_tally_totals():
    entries = [
        _entry("head", 600, "a", ["Materia I"]),
        _entry("chest", 620, "b", []),
    ]
    totals = tally_totals(entries)
    assert totals["total_entries"] == 2
    assert totals["avg_item_level"] == 610
    assert totals["sources"] == {"a": 1, "b": 1}
    assert totals["materia_count"] == 1


def test_tally_empty():
    assert tally_by_slot([]) == {}
    assert tally_totals([]) == {
        "total_entries": 0,
        "avg_item_level": 0,
        "sources": {},
        "materia_count": 0,
    }
