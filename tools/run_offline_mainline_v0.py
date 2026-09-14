#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-004
Unified Offline Mainline Runner v0 (CLI).
"""

from __future__ import annotations

import argparse
import json
import os
import sys


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-matrix", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--source-policy", required=True)
    ap.add_argument("--offline-evaluation", default="true", choices=["true", "false"])
    ap.add_argument("--disable-yolo", default="false", choices=["true", "false"])
    ap.add_argument("--yolo-manifest", required=True)
    args = ap.parse_args()

    from capabilities.offline_mainline.offline_mainline_runner_v0 import run_offline_mainline_v0  # type: ignore

    out = run_offline_mainline_v0(
        sample_matrix_path=str(args.sample_matrix),
        output_root=str(args.output_root),
        source_policy_id=str(args.source_policy),
        offline_evaluation=(str(args.offline_evaluation).lower() == "true"),
        disable_yolo=(str(args.disable_yolo).lower() == "true"),
        yolo_manifest_path=str(args.yolo_manifest),
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

