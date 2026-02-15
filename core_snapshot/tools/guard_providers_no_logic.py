#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.2: external/ 下禁止逻辑与决策依赖。
禁止：if.*produced_ts、import runtime、import intervention、import a3。
违规即 FAIL，打印 文件 + 行号。
"""
import re
import sys
from pathlib import Path

# 禁止的模式（在 external/ 下）；排除整行为注释
FORBIDDEN = [
    (re.compile(r"\bif\s+.*produced_ts", re.IGNORECASE), "if.*produced_ts"),
    (re.compile(r"^\s*import\s+runtime\b", re.MULTILINE), "import runtime"),
    (re.compile(r"^\s*from\s+runtime\b", re.MULTILINE), "from runtime"),
    (re.compile(r"^\s*import\s+intervention\b", re.MULTILINE), "import intervention"),
    (re.compile(r"^\s*from\s+intervention\b", re.MULTILINE), "from intervention"),
    (re.compile(r"^\s*import\s+a3\b", re.MULTILINE), "import a3"),
    (re.compile(r"^\s*from\s+a3\b", re.MULTILINE), "from a3"),
]


def main():
    root = Path(__file__).resolve().parents[1]
    external_dir = root / "external"
    if not external_dir.is_dir():
        print("✅ Phase 2.2 Provider Guard: no external/ dir, skip.")
        sys.exit(0)
    violations = []
    for py in external_dir.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = py.relative_to(root)
        rel_str = str(rel).replace("\\", "/")
        for pattern, name in FORBIDDEN:
            for i, line in enumerate(text.splitlines(), start=1):
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                if pattern.search(line):
                    violations.append((rel_str, i, stripped[:80], name))
    if violations:
        print("❌ Phase 2.2 Provider Guard: external/ 禁止逻辑/决策依赖：")
        for path, line_no, snippet, kind in violations:
            print(f"  {path}:{line_no}  [{kind}]  {snippet}")
        sys.exit(1)
    print("✅ Phase 2.2 Provider Guard: external/ 无逻辑违规")
    sys.exit(0)


if __name__ == "__main__":
    main()
