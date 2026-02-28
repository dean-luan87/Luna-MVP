#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D0.1-2 可选验收：扫描 a3/ 禁止 time.time( / datetime.now( / monotonic(（注释行排除）。
仅做告警（exit 0）；headless 路径已通过 initial_now_ms/now_ms 注入避免墙钟。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A3_DIR = ROOT / "a3"
PATTERN = re.compile(r"(time\.time\s*\(|datetime\.now\s*\(|monotonic\s*\()", re.I)


def main() -> int:
    hits = []
    for path in sorted(A3_DIR.rglob("*.py")):
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = line.strip()
            if s.startswith("#") or s.startswith('"""') or s.startswith("'''"):
                continue
            if PATTERN.search(line):
                hits.append((path, i, line.strip()[:70]))
    if hits:
        for path, line_no, content in hits:
            print(f"WARN: {path}:{line_no} {content}")
        print("(Headless 应通过 initial_now_ms/now_ms 注入时间；上述为 fallback 保留)")
        return 0
    print("PASS: no wall-clock usage in a3/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
