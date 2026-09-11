#!/usr/bin/env python3
"""
generate_tables.py (improved)

Parses files in ../ (experimental) and worlds/cv_dos/in_game_data.py to extract tables used by the Python enemy randomizer.

Produces JSON files in this directory:
- enemies.json
- resource_intensive.json (list of {id,name})
- boss_list.json (list of ids)

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
IN_GAME_DATA_PY = Path(__file__).resolve().parents[3] / "worlds" / "cv_dos" / "in_game_data.py"


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
            # scan following 10 lines for keywords
            window = lines[ln+1:ln+12]
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


def parse_resource_intensive(name_to_id_map):
    """Parse RESOURCE_INTENSIVE_ENEMY_NAMES from enemy_randomizer.rb and map names to ids if possible."""
    if not RB_ENEMY_RANDOMIZER.exists():
        return []
    text = RB_ENEMY_RANDOMIZER.read_text(encoding="utf-8")
    m = re.search(r"RESOURCE_INTENSIVE_ENEMY_NAMES\s*=\s*\[(.*?)\]", text, re.S)
    if not m:
        return []
    inner = m.group(1)
    # find quoted strings
    names = re.findall(r'"([^"]+)"', inner)
    result = []
    for n in names:
        eid = name_to_id_map.get(n)
        result.append({"id": eid, "name": n})
    return result


def parse_boss_list_from_in_game_data(name_to_id_map):
    """Parse boss_list from worlds/cv_dos/in_game_data.py. Returns list of ids (if names present, mapped using name_to_id_map)."""
    if not IN_GAME_DATA_PY.exists():
        return []
    text = IN_GAME_DATA_PY.read_text(encoding="utf-8")
    # find boss_list = [...] or boss_list = { ... }
    m = re.search(r"\bboss_list\b\s*=\s*(\[[\s\S]*?\]|\{[\s\S]*?\})", text)
    if not m:
        return []
    block = m.group(1)
    # extract quoted strings or numeric literals
    names = re.findall(r'"([^"]+)"', block)
    nums = re.findall(r"\b(0x[0-9A-Fa-f]+|\d+)\b", block)

    ids = []
    for nm in nums:
        try:
            if nm.startswith("0x") or nm.startswith("0X"):
                ids.append(int(nm, 16))
            else:
                ids.append(int(nm))
        except Exception:
            continue
    # Map names to ids if possible
    for nm in names:
        if nm in name_to_id_map:
            ids.append(name_to_id_map[nm])
        else:
            # try removing non-alphanumeric
            key = re.sub(r"[^0-9A-Za-z ]", "", nm)
            if key in name_to_id_map:
                ids.append(name_to_id_map[key])
            else:
                # leave name as unresolved marker by storing negative hash
                ids.append({"name": nm})
    # dedupe preserving order
    seen = set()
    out = []
    for v in ids:
        t = v if isinstance(v, int) else str(v)
        if t in seen:
            continue
        seen.add(t)
        out.append(v)
    return out


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    enemies = parse_enemies()
    name_to_id = {e["name"]: e["id"] for e in enemies}

    resource_intensive = parse_resource_intensive(name_to_id)
    boss_list = parse_boss_list_from_in_game_data(name_to_id)

    (OUTDIR / "enemies.json").write_text(json.dumps(enemies, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "resource_intensive.json").write_text(json.dumps(resource_intensive, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "boss_list.json").write_text(json.dumps(boss_list, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote:", OUTDIR / "enemies.json")
    print("Wrote:", OUTDIR / "resource_intensive.json")
    print("Wrote:", OUTDIR / "boss_list.json")

if __name__ == '__main__':
    main()
