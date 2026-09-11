#!/usr/bin/env python3
"""
generate_tables.py (fuzzy improvements)

Improves name resolution using normalization and difflib-based fuzzy matching.
Writes suggestion fields for unresolved entries.
"""

import re
import json
from pathlib import Path
from difflib import get_close_matches

ROOT = Path(__file__).resolve().parents[2] / "experimental"
OUTDIR = Path(__file__).resolve().parent

ENEMIES_TXT = ROOT / "DoS Enemies.txt"
RB_ENEMY_RANDOMIZER = ROOT / "enemy_randomizer.rb"
IN_GAME_DATA_PY = Path(__file__).resolve().parents[3] / "worlds" / "cv_dos" / "in_game_data.py"


def normalize_name(n: str) -> str:
    if not n:
        return ""
    s = n.lower()
    s = re.sub(r"[^0-9a-z ]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_enemies():
    enemies = []
    if not ENEMIES_TXT.exists():
        print("DoS Enemies.txt not found in experimental/. Please ensure experimental files are present.")
        return enemies

    text = ENEMIES_TXT.read_text(encoding="utf-8")
    pattern = re.compile(r"^([0-9A-Fa-f]{2})\s+(.+?)$", re.M)
    ids = []
    for m in pattern.finditer(text):
        idx = int(m.group(1), 16)
        name = m.group(2).strip()
        ids.append((idx, name))

    enemies = []
    lines = text.splitlines()
    id_positions = {}
    for i, line in enumerate(lines):
        m = re.match(r"^([0-9A-Fa-f]{2})\s+(.+?)$", line)
        if m:
            idx = int(m.group(1), 16)
            id_positions[idx] = i

    for idx, name in ids:
        info = {"id": idx, "name": name, "norm_name": normalize_name(name), "requires_overlay": None, "is_spawner": False}
        ln = id_positions.get(idx)
        if ln is not None:
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


def parse_resource_intensive(enemy_name_map):
    if not RB_ENEMY_RANDOMIZER.exists():
        return []
    text = RB_ENEMY_RANDOMIZER.read_text(encoding="utf-8")
    m = re.search(r"RESOURCE_INTENSIVE_ENEMY_NAMES\s*=\s*\[(.*?)\]", text, re.S)
    if not m:
        return []
    inner = m.group(1)
    names = re.findall(r'"([^"]+)"', inner)
    result = []
    # build normalized name map
    norm_to_id = {normalize_name(v): k for k, v in enemy_name_map.items()}
    all_norms = list(norm_to_id.keys())
    for n in names:
        norm = normalize_name(n)
        eid = norm_to_id.get(norm)
        suggested = None
        if eid is None:
            # fuzzy match
            matches = get_close_matches(norm, all_norms, n=1, cutoff=0.6)
            if matches:
                suggested_norm = matches[0]
                suggested = {"id": norm_to_id[suggested_norm], "name": enemy_name_map[norm_to_id[suggested_norm]]}
        result.append({"id": eid, "name": n, "normalized": norm, "suggested_match": suggested})
    return result


def parse_boss_list_from_in_game_data(enemy_name_map):
    if not IN_GAME_DATA_PY.exists():
        return []
    text = IN_GAME_DATA_PY.read_text(encoding="utf-8")
    m = re.search(r"\bboss_list\b\s*=\s*(\[[\s\S]*?\]|\{[\s\S]*?\})", text)
    if not m:
        return []
    block = m.group(1)
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
    for nm in names:
        norm = normalize_name(nm)
        # try direct name match in enemy_name_map
        found = None
        for id_, name in enemy_name_map.items():
            if normalize_name(name) == norm:
                found = id_
                break
        if found is not None:
            ids.append(found)
        else:
            # fuzzy
            norms = {normalize_name(v): k for k, v in enemy_name_map.items()}
            matches = get_close_matches(norm, list(norms.keys()), n=1, cutoff=0.6)
            if matches:
                ids.append(norms[matches[0]])
            else:
                ids.append({"name": nm})
    # dedupe
    seen = set(); out = []
    for v in ids:
        key = v if isinstance(v, int) else str(v)
        if key in seen:
            continue
        seen.add(key)
        out.append(v)
    return out


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    enemies = parse_enemies()
    enemy_name_map = {e["id"]: e["name"] for e in enemies}

    resource_intensive = parse_resource_intensive(enemy_name_map)
    boss_list = parse_boss_list_from_in_game_data(enemy_name_map)

    (OUTDIR / "enemies.json").write_text(json.dumps(enemies, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "resource_intensive.json").write_text(json.dumps(resource_intensive, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUTDIR / "boss_list.json").write_text(json.dumps(boss_list, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Wrote:", OUTDIR / "enemies.json")
    print("Wrote:", OUTDIR / "resource_intensive.json")
    print("Wrote:", OUTDIR / "boss_list.json")

if __name__ == '__main__':
    main()
