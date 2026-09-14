#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.1-Guard: 外部感知“只写不读”硬检查。
非白名单文件中出现任意关键词 → FAIL（exit 1）。CI/本地门禁。

# NOTE:
# main.py is allowed to WRITE external perception fields into ObservationFrame,
# but must never READ or BRANCH on them.
"""
import re
import sys
from pathlib import Path

# 关键词（出现即触发检查；在非白名单文件中即违规）
KEYWORDS = [
    "obs.ocr_text",
    "obs.map_hint",
    "obs.speech_event",
    "ocr_produced_ts",
    "map_produced_ts",
    "speech_produced_ts",
]

# 白名单：仅允许以下路径出现上述关键词（序列化/构造/provider/验证脚本）
# 使用前缀匹配：external/、tools/ 表示该目录下所有文件
WHITELIST_PREFIXES = (
    "runtime/a3_logger.py",
    "runtime/observation_frame.py",
    "runtime/observation_builders.py",
    "main.py",  # Observation assembly only (write-only)
    "external/",
    "tools/",
)

# 扫描时排除的目录
SKIP_DIRS = (".venv", "venv", "build", "dist", "__pycache__", "logs", ".git")


def is_whitelisted(rel_path: str) -> bool:
    rel = rel_path.replace("\\", "/")
    for prefix in WHITELIST_PREFIXES:
        if prefix.endswith("/"):
            if rel.startswith(prefix):
                return True
        else:
            if rel == prefix or rel.startswith(prefix + "/"):
                return True
    return False


def main():
    root = Path(__file__).resolve().parents[1]
    violations = []  # (rel_path, line_no, line_snippet, keyword)

    for py in root.rglob("*.py"):
        rel = py.relative_to(root)
        rel_str = str(rel).replace("\\", "/")
        if any(skip in rel.parts for skip in SKIP_DIRS):
            continue
        if is_whitelisted(rel_str):
            continue
        try:
            lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            for kw in KEYWORDS:
                if kw in line:
                    violations.append((rel_str, i, line.strip()[:100], kw))
                    break

    if violations:
        print("❌ Phase 2.1-Guard: 外部感知字段在非白名单文件中被读取/引用（只写不读违规）")
        for path, line_no, snippet, keyword in violations:
            print(f"  {path}:{line_no}  [{keyword}]  {snippet}")
        sys.exit(1)
    print("✅ Phase 2.1-Guard: 外部字段只写不读检查通过")
    sys.exit(0)


if __name__ == "__main__":
    main()
