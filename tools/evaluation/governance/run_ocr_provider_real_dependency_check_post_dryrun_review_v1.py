#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Real Dependency Check Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    run_ocr_provider_real_dependency_check_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("real_dependency_check_dryrun_input_review", "real_dependency_check_dryrun_input_review_v1.json"),
    ("dependency_check_sequence_review", "dependency_check_sequence_review_v1.json"),
    ("paddleocr_dependency_check_review", "paddleocr_dependency_check_review_v1.json"),
    ("rapidocr_dependency_check_review", "rapidocr_dependency_check_review_v1.json"),
    ("external_ocr_dependency_check_review", "external_ocr_dependency_check_review_v1.json"),
    ("evidence_package_candidate_review", "evidence_package_candidate_review_v1.json"),
    ("failure_route_candidate_review", "failure_route_candidate_review_v1.json"),
    ("rollback_plan_candidate_review", "rollback_plan_candidate_review_v1.json"),
    ("environment_isolation_boundary_review", "environment_isolation_boundary_review_v1.json"),
    ("future_execution_gate_review", "future_execution_gate_review_v1.json"),
    ("real_dependency_check_blocked_path_review", "real_dependency_check_blocked_path_review_v1.json"),
    ("real_dependency_check_no_execution_review", "real_dependency_check_no_execution_review_v1.json"),
    ("real_dependency_check_closure_decision", "real_dependency_check_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-provider-real-dependency-check-dryrun-root", default=DEFAULT_DRYRUN)
    args = p.parse_args()

    result = run_ocr_provider_real_dependency_check_post_dryrun_review_v1(
        ocr_provider_real_dependency_check_dryrun_root=args.ocr_provider_real_dependency_check_dryrun_root,
        review_output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "dryrun_closed": sm.get("ocr_provider_real_dependency_check_dryrun_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
