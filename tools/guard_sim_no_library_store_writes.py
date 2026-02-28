#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0 Guard: simulation 与 run_sim_runner 禁止写入 library_store。
只允许写 outputs/。允许对 library_store 只读 open。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_DIR = ROOT / "simulation"
RUNNER = ROOT / "tools" / "run_sim_runner.py"
# 写入：open(..., "w"/"wb"/"a"), write_text, write_bytes, 且路径含 library_store
LIBRARY_STORE = re.compile(r"library_store", re.I)
WRITE_PATTERN = re.compile(r'(open\s*\([^)]*["\']w|open\s*\([^)]*["\']wb|open\s*\([^)]*["\']a|\.write_text\s*\(|\.write_bytes\s*\()', re.I)


def main():
    errors = []
    files = list(SIM_DIR.rglob("*.py")) + ([RUNNER] if RUNNER.exists() else [])
    for path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if LIBRARY_STORE.search(line) and WRITE_PATTERN.search(line):
                errors.append((path, i, "write to library_store forbidden: " + line.strip()[:70]))

    if errors:
        for path, line_no, msg in errors:
            print(f"{path}:{line_no} {msg}")
        print("FAIL: SimRunner must not write to library_store")
        return 1
    print("PASS: no library_store writes in simulation and run_sim_runner")
    return 0


if __name__ == "__main__":
    sys.exit(main())
