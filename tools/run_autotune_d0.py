#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3-D0: 统计型 AutoTune。只读 outputs/ 与 annotations/，写 outputs/v1.1/autotune_report_v0.json。
不修改 runtime、不写 library_store。
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from library.autotune_analyzer import AutoTuneAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="D0: generate autotune_report_v0.json from episode summaries and explanations."
    )
    parser.add_argument("--base-dir", default="library_store", help="Base dir (for API consistency)")
    parser.add_argument("--version-tag", default="v1.1", help="Version tag")
    parser.add_argument("--out-dir", default="outputs", help="Output directory")
    args = parser.parse_args()

    version = args.version_tag
    out_dir = args.out_dir.rstrip("/")
    out_version = os.path.join(out_dir, version)
    report_path = os.path.join(out_version, "autotune_report_v0.json")

    analyzer = AutoTuneAnalyzer(
        base_dir=args.base_dir,
        version_tag=version,
        out_dir=out_version,
    )
    n = analyzer.load_data()

    if n < 50:
        print("WARNING: episode_count < 50, report is for reference only.", file=sys.stderr)

    report = analyzer.generate_report()
    os.makedirs(out_version, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("episodes loaded:", n)
    print("report generated:", report_path)


if __name__ == "__main__":
    main()
