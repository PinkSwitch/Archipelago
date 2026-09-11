#!/usr/bin/env python3
"""
generate_tables.py

Parses files in ../ (experimental) to extract tables used by the Python enemy randomizer.

Produces JSON files in this directory:
- enemies.json
- resource_intensive.json
- boss_list.json

This is a best-effort text parser that reads the plain-text files under ../ and extracts patterns.
Run from repository root as:
  python3 experimental/tabellen/generate_tables.py
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "experimental"
OUTDIR = Path(__file__).resolve().parent

ENEMIES_TXT = ROOT / "DoS Enemies.txt"
RB_ENEMY_RANDOMIZER = ROOT / "enemy_randomizer.rb"
DOS_CONSTANTS_JP = ROOT / "dos_constants_jp.rb"


def parse_enemies():
    enemies = []
    if not ENEMIES_TXT.exists():
        print("DoS Enemies.txt not found in experimental/. Please ensure experimental files are present.")
        return enemies

    text = ENEMIES_TXT.read_text(encoding="utf-8")
    # match blocks like "00 Zombie" at start of line
    pattern = re.compile(r"^([0-9A-Fa-f]{2})\s+(.+?)$", re.M)
    ids = []
    for m in pattern.finditer(text):
        idx = int(m.group(1), 16)
        name = m.group(2).strip()
        ids.append((idx, name))

    # Now determine for each entry whether it has "Requires enemy overlay N" or "Spawner." nearby
    enemies = []
    lines = text.splitlines()
    # build index by hex id to line number
    id_positions = {}
    for i, line in enumerate(lines):
        m = re.match(r"^([0-9A-Fa-f]{2})\s+(.+?)$", line)
        if m:
            idx = int(m.group(1), 16)
            id_positions[idx] = i

    for idx, name in ids:
        info = {"id": idx, "name": name, "requires_overlay": None, "is_spawner": False}
        ln = id_positions.get(idx)
        if ln is not None:
            # scan following 6 lines for keywords
            window = lines[ln+1:ln+8]
            for w in window:
                if "Requires enemy overlay" in w:
                    ov = re.search(r"Requires enemy overlay\s*(\d+)", w)
                    if ov:
                        info["requires_overlay"] = int(ov.group(1))
                if "Spawner" in w:
                    info["is_spawner"] = True
        enemies.append(info)

    enemies.sort(key=lambda x: x["id"])
    return enemies


def parse_resource_intensive():
    if not RB_ENEMY_RANDOMIZER.exists():
        return []
    text = RB_ENEMY_RANDOMIZER.read_text(encoding="utf-8")
    m = re.search(r"RESOURCE_INTENSIVE_ENEMY_NAMES\s*=\s*\[(.*?)\]", text, re.S)
    if not m:
        return []
    inner = m.group(1)
    # find quoted strings
    names = re.findall(r'"([^"]+)"', inner)
    return names


def parse_boss_list_from_constants():
    # attempt to locate boss list in dos_constants_jp or other experimental files
    out = []
    if DOS_CONSTANTS_JP.exists():
        text = DOS_CONSTANTS_JP.read_text(encoding="utf-8")
        # no boss list in that file in our sample; return empty
    return out


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    enemies = parse_enemies()
    resource_intensive = parse_resource_intensive()
    boss_list = parse_boss_list_from_constants()

    (OUTDIR / "enemies.json").write_text(json.dumps(enemies, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "resource_intensive.json").write_text(json.dumps(resource_intensive, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "boss_list.json").write_text(json.dumps(boss_list, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote:", OUTDIR / "enemies.json")
    print("Wrote:", OUTDIR / "resource_intensive.json")
    print("Wrote:", OUTDIR / "boss_list.json")

if __name__ == '__main__':
    main()
