#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.2-Explain Guard: 扫描 library/episode_explainer.py 与 tools/run_episode_explainer.py。
禁止 import runtime/intervention/a3/main/external；
禁止出现关键词（作为数据读取）：ocr_text / map_hint / speech_event / produced_ts。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "library" / "episode_explainer.py",
    ROOT / "tools" / "run_episode_explainer.py",
]
FORBIDDEN_IMPORT = re.compile(r"\b(runtime|intervention|a3|main|external)\b", re.I)
# 禁止作为键读取：.get("ocr_text") 或 ["ocr_text"] 等
FORBIDDEN_KEY_USE = re.compile(
    r'(\.get\s*\(\s*["\'](?:ocr_text|map_hint|speech_event|.*produced_ts)["\']\s*\)|'
    r'\[["\'](?:ocr_text|map_hint|speech_event|.*produced_ts)["\']\s*\])',
    re.I,
)


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
                    errors.append((path, i, "forbidden import: " + s[:80]))
            if FORBIDDEN_KEY_USE.search(line):
                errors.append((path, i, "forbidden key read: " + s[:80]))

    if errors:
        for path, line_no, msg in errors:
            print(f"{path}:{line_no} {msg}")
        print("FAIL: Explain must not import runtime/intervention/a3/main/external or read ocr_text/map_hint/speech_event/produced_ts")
        return 1
    print("PASS: no forbidden imports or external-field reads in Explain modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
