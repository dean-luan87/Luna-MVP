#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Minimal Controlled Execution Final Ready Check v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1 import (
    run_ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1,
)

DEFAULT_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_execution_authorization_decision"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)
DEFAULT_PREFLIGHT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_final_preflight"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("final_ready_check_policy", "final_ready_check_policy_v1.json"),
    ("upstream_input_review", "upstream_input_review_v1.json"),
    ("minimal_execution_scope_lock_review", "minimal_execution_scope_lock_review_v1.json"),
    ("final_ready_check_result", "final_ready_check_result_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--authorization-decision-root", default=DEFAULT_AUTH)
    p.add_argument("--minimal-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    args = p.parse_args()

    result = run_ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_v1(
        ocr_real_dependency_real_minimal_execution_authorization_decision_root=args.authorization_decision_root,
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root=args.minimal_dryrun_root,
        ocr_real_dependency_execution_final_preflight_root=args.final_preflight_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "ready_check_pass": sm.get("ready_check_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "compressed_short_chain": sm.get("compressed_short_chain"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("ready_check_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
