"""
Enemy randomizer integration for cv_dos (partial).

This module expects extracted tables to live in experimental/tabellen as JSON files.
- experimental/tabellen/enemies.json         -> list of {"id": int, "name": str, "requires_overlay": int|None, "is_spawner": bool}
- experimental/tabellen/resource_intensive.json -> list of enemy names (strings) or objects with id/name
- experimental/tabellen/boss_list.json       -> list of boss ids or objects

This file implements:
- generate_enemy_mapping(world, ...)
- write_enemies(world, rom, mode='full_swap', dry_run=True)

The mapping generation uses grouping by overlay requirement and preserves bosses/resource-intensive entries by default.

Run `python3 experimental/tabellen/generate_tables.py` to regenerate the JSON files from the /experimental sources if they change.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "experimental", "tabellen")
ENEMIES_JSON = os.path.normpath(os.path.join(BASE_DIR, "enemies.json"))
RESOURCE_INTENSIVE_JSON = os.path.normpath(os.path.join(BASE_DIR, "resource_intensive.json"))
BOSS_LIST_JSON = os.path.normpath(os.path.join(BASE_DIR, "boss_list.json"))

ENEMY_DEFINITION_SIZE = 0x24

try:
    from .boss_randomizer import base_enemy_address as BASE_ENEMY_ADDRESS, direct_enemy_address as DIRECT_ENEMY_ADDRESS
except Exception:
    BASE_ENEMY_ADDRESS = 0x02078CAC
    DIRECT_ENEMY_ADDRESS = 0x007CCAC


@dataclass
class EnemyInfo:
    id: int
    name: str
    requires_overlay: Optional[int]
    is_spawner: bool


def _load_tables():
    enemies: List[EnemyInfo] = []
    resource_intensive_entries: List[dict] = []
    boss_list_raw = []

    if os.path.exists(ENEMIES_JSON):
        try:
            with open(ENEMIES_JSON, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for e in raw:
                enemies.append(EnemyInfo(id=e.get("id"), name=e.get("name"), requires_overlay=e.get("requires_overlay"), is_spawner=bool(e.get("is_spawner"))))
        except Exception:
            logger.exception("Failed to load enemies.json")

    if os.path.exists(RESOURCE_INTENSIVE_JSON):
        try:
            with open(RESOURCE_INTENSIVE_JSON, "r", encoding="utf-8") as f:
                resource_intensive_entries = json.load(f)
        except Exception:
            logger.exception("Failed to load resource_intensive.json")

    if os.path.exists(BOSS_LIST_JSON):
        try:
            with open(BOSS_LIST_JSON, "r", encoding="utf-8") as f:
                boss_list_raw = json.load(f)
        except Exception:
            logger.exception("Failed to load boss_list.json")

    return enemies, resource_intensive_entries, boss_list_raw


def _extract_boss_ids(boss_list_raw: List, enemies: List[EnemyInfo]) -> List[int]:
    """Normalize boss_list entries into integer IDs.
    boss_list_raw may contain ints or dicts like {"id":..., "name":...}.
    """
    name_to_id = {e.name: e.id for e in enemies}
    ids = []
    for item in boss_list_raw:
        if isinstance(item, int):
            ids.append(item)
        elif isinstance(item, dict):
            # prefer explicit id
            if item.get("id") is not None:
                ids.append(item.get("id"))
            else:
                nm = item.get("name")
                if nm and nm in name_to_id:
                    ids.append(name_to_id[nm])
        elif isinstance(item, str):
            if item in name_to_id:
                ids.append(name_to_id[item])
    # dedupe
    seen = set(); out = []
    for i in ids:
        if i not in seen:
            seen.add(i); out.append(i)
    return out


def _group_key(e: EnemyInfo):
    return (e.requires_overlay if e.requires_overlay is not None else -1, e.is_spawner)


def _ensure_boss_preservation(mapping: Dict[int, int]):
    """
    Defensive check: ensure any boss IDs present in the boss_list are forced to map to themselves.
    This guarantees bosses are not swapped even if upstream logic attempted to.
    """
    enemies, resource_entries, boss_list_raw = _load_tables()
    boss_ids = set(_extract_boss_ids(boss_list_raw, enemies))
    if not boss_ids:
        return mapping
    changed = False
    for b in boss_ids:
        if mapping.get(b, b) != b:
            logger.warning("Reverting boss mapping for %02X to itself (was mapping to %02X).", b, mapping.get(b))
            mapping[b] = b
            changed = True
    if changed:
        logger.info("Boss preservation enforced for %d bosses.", len(boss_ids))
    return mapping


def generate_enemy_mapping(world, allow_bosses: bool = False, preserve_resource_intensive: bool = True, debug_subset: Optional[int] = None) -> Dict[int, int]:
    """
    Generate mapping old_id -> new_id.
    Uses world.random for determinism (world.random must be provided by the world generator).
    """
    enemies, resource_intensive_entries, boss_list_raw = _load_tables()
    if not enemies:
        logger.warning("No enemy table found to randomize.")
        world.enemy_mapping = {}
        return {}

    name_to_id = {e.name: e.id for e in enemies}
    resource_intensive_ids = {entry.get("id") for entry in resource_intensive_entries if entry.get("id") is not None}
    boss_ids = set(_extract_boss_ids(boss_list_raw, enemies))

    rng = getattr(world, "random", None)
    if rng is None:
        import random
        rng = random.Random()

    groups: Dict = {}
    for e in enemies:
        key = _group_key(e)
        groups.setdefault(key, []).append(e)

    mapping: Dict[int, int] = {}

    # shuffle within groups
    for key, group in groups.items():
        ids = [g.id for g in group]
        dst = ids.copy()
        rng.shuffle(dst)
        # try to derange
        if len(dst) > 1:
            for _ in range(10):
                if any(a == b for a, b in zip(ids, dst)):
                    rng.shuffle(dst)
                else:
                    break
        for s, d in zip(ids, dst):
            mapping[s] = d

    # enforce protections
    # Always protect bosses for this project (defensive)
    for b in boss_ids:
        mapping[b] = b

    if preserve_resource_intensive:
        for r in resource_intensive_ids:
            if r is not None:
                mapping[r] = r

    # debug subset: only apply to first N non-protected mappings
    if debug_subset:
        protected = set(boss_ids) | {r for r in resource_intensive_ids if r is not None}
        non_protected = [k for k in mapping.keys() if k not in protected and mapping[k] != k]
        to_keep = set(non_protected[debug_subset:]) if len(non_protected) > debug_subset else set()
        for k in non_protected:
            if k in to_keep:
                mapping[k] = k

    # final defensive enforcement (ensure bosses preserved)
    mapping = _ensure_boss_preservation(mapping)

    world.enemy_mapping = mapping
    logger.info("Generated enemy mapping with %d entries (allow_bosses=%s, preserve_resource_intensive=%s)", len(mapping), allow_bosses, preserve_resource_intensive)
    return mapping


def _read_block_safe(rom, addr: int, length: int):
    try:
        return rom.read_direct(addr, length)
    except Exception:
        try:
            return rom.read_from_file(addr, "arm9", length)
        except Exception:
            logger.exception("Failed to read block at 0x%X", addr)
            return None


def _write_block_safe(rom, addr: int, data: bytes):
    try:
        rom.write_direct(addr, data)
        return True
    except Exception:
        try:
            rom.write_to_file(addr, "arm9", data)
            return True
        except Exception:
            logger.exception("Failed to write block at 0x%X", addr)
            return False


def write_enemies(world, rom, mode: str = "full_swap", dry_run: bool = True):
    mapping = getattr(world, "enemy_mapping", None)
    if mapping is None:
        logger.info("No enemy mapping present; skipping write.")
        return

    # Defensive: ensure boss preservation before applying writes
    mapping = _ensure_boss_preservation(mapping)

    swaps = []
    for old, new in mapping.items():
        if old == new:
            continue
        swaps.append((old, new))

    report = {
        "swaps": [],
        "dry_run": bool(dry_run)
    }

    for old, new in swaps:
        src_direct = DIRECT_ENEMY_ADDRESS + (new * ENEMY_DEFINITION_SIZE)
        dst_direct = DIRECT_ENEMY_ADDRESS + (old * ENEMY_DEFINITION_SIZE)
        src_base = BASE_ENEMY_ADDRESS + (new * ENEMY_DEFINITION_SIZE)
        dst_base = BASE_ENEMY_ADDRESS + (old * ENEMY_DEFINITION_SIZE)

        src_block = _read_block_safe(rom, src_direct, ENEMY_DEFINITION_SIZE)
        if src_block is None:
            src_block = _read_block_safe(rom, src_base, ENEMY_DEFINITION_SIZE)

        entry = {"old": old, "new": new, "src_read_ok": bool(src_block), "writes": []}

        if src_block is None:
            entry["warning"] = "source unreadable"
            report["swaps"].append(entry)
            continue

        if dry_run:
            # do not write, but report addresses
            entry["src_direct"] = hex(src_direct)
            entry["dst_direct"] = hex(dst_direct)
            entry["src_base"] = hex(src_base)
            entry["dst_base"] = hex(dst_base)
            report["swaps"].append(entry)
            continue

        ok1 = _write_block_safe(rom, dst_direct, src_block)
        entry["writes"].append({"addr": hex(dst_direct), "ok": bool(ok1)})
        ok2 = _write_block_safe(rom, dst_base, src_block)
        entry["writes"].append({"addr": hex(dst_base), "ok": bool(ok2)})
        report["swaps"].append(entry)

    # write report to world if possible
    try:
        out_path = os.path.normpath(os.path.join(os.getcwd(), "enemy_randomizer_mapping_report.json"))
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info("Wrote enemy randomizer report to %s", out_path)
    except Exception:
        logger.exception("Failed to write report file")

    logger.info("Applied full-swap (dry_run=%s) for %d swaps", dry_run, len(report.get("swaps", [])))
