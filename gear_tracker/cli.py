"""Command line interface for the FFXIV gear tracker."""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import date
from typing import List, Optional

from gear_tracker.models import GearEntry
from gear_tracker.storage import GearStore
from gear_tracker.tally import tally_by_slot, tally_totals
from gear_tracker.export import export_csv


def _new_id() -> str:
    return str(uuid.uuid4())[:8]


def _today() -> str:
    return date.today().isoformat()


def cmd_add(args: argparse.Namespace, store: GearStore) -> int:
    materia = [m.strip() for m in args.materia.split(",") if m.strip()] if args.materia else []
    entry = GearEntry(
        id=_new_id(),
        slot=args.slot,
        item_name=args.name,
        item_level=args.item_level,
        materia=materia,
        source=args.source,
        date=args.date or _today(),
        notes=args.notes or "",
    )
    store.add(entry)
    print(f"Added {args.name} ({args.slot}, ilvl {args.item_level}) id={entry.id}")
    return 0


def cmd_list(args: argparse.Namespace, store: GearStore) -> int:
    entries = store.load()
    if not entries:
        print("No gear entries logged yet.")
        return 0
    for e in entries:
        materia = ",".join(e.materia) if e.materia else "-"
        print(
            f"{e.id} | {e.date} | {e.slot} | {e.item_name} | ilvl {e.item_level} "
            f"| materia: {materia} | source: {e.source or '-'} | {e.notes or '-'}"
        )
    return 0


def cmd_tally(args: argparse.Namespace, store: GearStore) -> int:
    entries = store.load()
    if not entries:
        print("No gear entries logged yet.")
        return 0
    by_slot = tally_by_slot(entries)
    totals = tally_totals(entries)
    print("Gear tally by slot:")
    for slot in sorted(by_slot):
        stats = by_slot[slot]
        sources = ", ".join(f"{k}={v}" for k, v in stats["sources"].items()) or "-"
        print(
            f"  {slot}: {stats['count']} item(s), avg ilvl {stats['avg_item_level']}, "
            f"materia {stats['materia_count']}, sources: {sources}"
        )
    print("Totals:")
    print(
        f"  entries: {totals['total_entries']}, avg ilvl {totals['avg_item_level']}, "
        f"materia {totals['materia_count']}"
    )
    sources = ", ".join(f"{k}={v}" for k, v in totals["sources"].items()) or "-"
    print(f"  sources: {sources}")
    return 0


def cmd_export(args: argparse.Namespace, store: GearStore) -> int:
    entries = store.load()
    export_csv(entries, args.output)
    print(f"Exported {len(entries)} entries to {args.output}")
    return 0


def cmd_remove(args: argparse.Namespace, store: GearStore) -> int:
    if store.remove(args.id):
        print(f"Removed entry {args.id}")
        return 0
    print(f"No entry found with id {args.id}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ffxiv-gear",
        description="Log FFXIV gear upgrades, item level, materia, and sources locally.",
    )
    parser.add_argument(
        "--data", default="gear_log.json", help="Path to the local JSON data file (default: gear_log.json)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a gear entry")
    p_add.add_argument("--slot", required=True, help="Gear slot (e.g. head, chest, weapon)")
    p_add.add_argument("--name", required=True, help="Item name")
    p_add.add_argument("--item-level", type=int, required=True, dest="item_level", help="Item level")
    p_add.add_argument("--materia", default="", help="Comma-separated materia list")
    p_add.add_argument("--source", default="", help="Source (e.g. tomestone, raid, crafted)")
    p_add.add_argument("--date", default="", help="Date (YYYY-MM-DD), defaults to today")
    p_add.add_argument("--notes", default="", help="Notes")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all gear entries")
    p_list.set_defaults(func=cmd_list)

    p_tally = sub.add_parser("tally", help="Show gear tally summary")
    p_tally.set_defaults(func=cmd_tally)

    p_export = sub.add_parser("export", help="Export entries to CSV")
    p_export.add_argument("--output", required=True, help="Output CSV path")
    p_export.set_defaults(func=cmd_export)

    p_remove = sub.add_parser("remove", help="Remove a gear entry by id")
    p_remove.add_argument("--id", required=True, help="Entry id to remove")
    p_remove.set_defaults(func=cmd_remove)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = GearStore(args.data)
    return args.func(args, store)


if __name__ == "__main__":
    sys.exit(main())
