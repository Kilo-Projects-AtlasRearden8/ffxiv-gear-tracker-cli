# FFXIV Gear Tracker CLI

A local-first Python command-line tool for Final Fantasy XIV players to log gear
upgrades, track item level, materia, and sources, with JSON storage and CSV
export.

Built by **Asdale Dynamics, LLC** as a fan project. No game assets are included
or distributed. All data stays on your machine.

## Who this is for

FFXIV players who want a simple, private, offline way to keep track of gear
progression across slots, materia melds, and where each piece came from.

## Features

- Log gear entries: slot, item name, item level, materia, source, date, notes
- Store everything in a local JSON file (you own your data)
- Tally summary by slot: counts, average item level, sources, materia count
- Export your log to CSV
- Remove entries by id
- No accounts, no network, no secrets

## Install

```bash
git clone <this-repo>
cd ffxiv-gear-tracker-cli
pip install -e .
```

Or run directly without installing:

```bash
python -m gear_tracker.cli --help
```

## Usage

Add a piece of gear:

```bash
ffxiv-gear add --slot head --name "Gryphon's Circlet" \
  --item-level 620 --materia "Materia IV,Materia V" \
  --source tomestone --notes "Bought with Allied seals"
```

List your log:

```bash
ffxiv-gear list
```

See a tally summary:

```bash
ffxiv-gear tally
```

Export to CSV:

```bash
ffxiv-gear export --output gear_backup.csv
```

Remove an entry:

```bash
ffxiv-gear remove --id a1b2c3d4
```

Use `--data /path/to/file.json` to store the log somewhere else. Default is
`gear_log.json` in the current folder.

## Tests

```bash
pytest
```

## Credits

Created and maintained by **Asdale Dynamics, LLC** (Indiana, formed October
2026) — beginner-friendly AI education, books, guides, and practical tools.
Hub: dylanasdale.github.io. Book: *The Massive AI Manual*.

This is a fan project for Final Fantasy XIV players. It is not affiliated with
or endorsed by Square Enix. No game assets are included.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
