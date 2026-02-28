#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0 Guard: simulation 与 run_sim_runner 禁止 import runtime/intervention/a3/main/external；
禁止 time.time( / CLOCK.now( / sleep( 。
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIM_DIR = ROOT / "simulation"
RUNNER = ROOT / "tools" / "run_sim_runner.py"
FORBIDDEN_IMPORT = re.compile(r"\b(runtime|intervention|a3|main|external)\b", re.I)
FORBIDDEN_TIME = re.compile(r"(time\.time\s*\(|CLOCK\.now\s*\(|sleep\s*\()")


def main():
    errors = []
    files = list(SIM_DIR.rglob("*.py")) + ([RUNNER] if RUNNER.exists() else [])
    # Phase 2 recompute: 仅允许 simulation/logic/a3_headless_adapter.py 导入 a3
    ALLOW_A3_PATH = "simulation" + os.sep + "logic" + os.sep + "a3_headless_adapter.py"
    for path in files:
        if not path.exists():
            continue
        allow_a3 = ALLOW_A3_PATH in str(path) or path.name == "a3_headless_adapter.py"
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith('"""') or s.startswith("'''"):
                continue
            if s.startswith("import ") or s.startswith("from "):
                if FORBIDDEN_IMPORT.search(line):
                    if allow_a3 and "a3" in line and "runtime" not in line.lower() and "intervention" not in line.lower():
                        continue
                    errors.append((path, i, "forbidden import: " + s[:70]))
            stripped = s.lstrip()
            if FORBIDDEN_TIME.search(line) and not stripped.startswith("#") and not (stripped.startswith('"""') or stripped.startswith("'''")):
                errors.append((path, i, "forbidden time/sleep: " + s[:70]))

    if errors:
        for path, line_no, msg in errors:
            print(f"{path}:{line_no} {msg}")
        print("FAIL: SimRunner must not import runtime/intervention/a3/main/external or use time.time/CLOCK.now/sleep")
        return 1
    print("PASS: no forbidden imports or time/sleep in simulation and run_sim_runner")
    return 0


if __name__ == "__main__":
    sys.exit(main())
