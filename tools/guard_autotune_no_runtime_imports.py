#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0 Guard: 禁止 autotune  import runtime/intervention/a3/main/external；
禁止写入 library_store/，只允许写 outputs/。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "library" / "autotune_analyzer.py",
    ROOT / "tools" / "run_autotune_d0.py",
]
FORBIDDEN_IMPORT = re.compile(r"\b(runtime|intervention|a3|main|external)\b", re.I)
FORBIDDEN_WRITE = re.compile(r"library_store", re.I)


def main():
    errors = []
    for path in FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith('"""') or s.startswith("'''"):
                continue
            if s.startswith("import ") or s.startswith("from "):
                if FORBIDDEN_IMPORT.search(line):
                    errors.append((path, i, "forbidden import: " + s[:70]))
            # 禁止对 library_store 的写入（open w/wb, write_text, write 等）
            if FORBIDDEN_WRITE.search(line):
                low = line.lower()
                if "open" in low and ("'w'" in low or '"w"' in low or "'wb'" in low or "'a'" in low):
                    errors.append((path, i, "forbidden write to library_store: " + s[:70]))
                if "write_text" in low or "write_bytes" in low:
                    errors.append((path, i, "forbidden write to library_store: " + s[:70]))

    if errors:
        for path, line_no, msg in errors:
            print(f"{path}:{line_no} {msg}")
        print("FAIL: AutoTune must not import runtime/intervention/a3/main/external or write to library_store/")
        return 1
    print("PASS: no forbidden imports or library_store writes in AutoTune modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
