# STATUS

## What was built

A local-first Python CLI for Final Fantasy XIV players to log gear upgrades,
track item level, materia, and sources, with JSON storage and CSV export.

Files:
- `gear_tracker/models.py` — `GearEntry` dataclass (slot, item_name, item_level,
  materia, source, date, notes) with JSON serialization.
- `gear_tracker/storage.py` — `GearStore`: load/save/add/remove entries in a
  local JSON file.
- `gear_tracker/tally.py` — `tally_by_slot` and `tally_totals` summary logic
  (counts, average item level, sources, materia count).
- `gear_tracker/export.py` — `export_csv` writing entries to CSV.
- `gear_tracker/cli.py` — argparse CLI: `add`, `list`, `tally`, `export`,
  `remove`. Defaults to `gear_log.json`; override with `--data`.
- `gear_tracker/__init__.py` — package marker.
- `tests/test_tally.py` — 5 tests covering tally grouping, averages, sources,
  materia counts, totals, and empty input.
- `pyproject.toml` — project metadata and `ffxiv-gear` console script entry
  point.
- `README.md` — usage, install, credits, license.
- `LICENSE` — MIT, copyright exactly "Copyright (c) 2026 Asdale Dynamics, LLC".

## How to run

```bash
# From the project folder
python3 -m gear_tracker.cli --help

# Add an entry
python3 -m gear_tracker.cli add --slot head --name "Test Helm" \
  --item-level 620 --materia "Materia IV" --source tomestone

# List entries
python3 -m gear_tracker.cli list

# Tally summary
python3 -m gear_tracker.cli tally

# Export to CSV
python3 -m gear_tracker.cli export --output gear_backup.csv

# Or install the console script
pip install -e .
ffxiv-gear tally
```

## Verification results

- `python3 -m pytest -q`: 5 passed (tally logic tests).
- CLI smoke test: add → list → tally → export → remove all work; CSV output
  correct; removal by id works; default date and empty materia handled.

## Known gaps

- No input validation beyond argparse type coercion (e.g. negative item levels
  accepted).
- No deduplication or edit command; entries are append-only plus remove by id.
- CSV export re-joins materia with `;`, reading CSV back in is not supported.
- No tests for storage, CLI, or export modules — only tally logic is tested.
- No packaging/publishing configuration beyond `pyproject.toml`; not published.

## Credits

Built by Asdale Dynamics, LLC (Indiana, formed October 2026). Fan project, no
game assets, not affiliated with Square Enix.
