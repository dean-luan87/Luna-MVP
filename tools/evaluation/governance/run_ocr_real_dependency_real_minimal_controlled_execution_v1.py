#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Minimal Controlled Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_v1 import (
    run_ocr_real_dependency_real_minimal_controlled_execution_v1,
)

DEFAULT_READY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
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
    "ocr_real_dependency_real_minimal_controlled_execution"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("real_minimal_controlled_execution_policy", "real_minimal_controlled_execution_policy_v1.json"),
    ("final_ready_check_input_review", "final_ready_check_input_review_v1.json"),
    ("execution_environment_snapshot", "execution_environment_snapshot_v1.json"),
    ("package_presence_check_result", "package_presence_check_result_v1.json"),
    ("model_cache_path_check_result", "model_cache_path_check_result_v1.json"),
    ("model_file_existence_check_result", "model_file_existence_check_result_v1.json"),
    ("model_file_hash_check_result", "model_file_hash_check_result_v1.json"),
    ("provider_import_check_result", "provider_import_check_result_v1.json"),
    ("execution_boundary_audit", "execution_boundary_audit_v1.json"),
    ("execution_failure_route_result", "execution_failure_route_result_v1.json"),
    ("execution_rollback_result", "execution_rollback_result_v1.json"),
    ("execution_evidence_package", "execution_evidence_package_v1.json"),
    ("execution_non_claims_register", "execution_non_claims_register_v1.json"),
    ("real_minimal_controlled_execution_decision", "real_minimal_controlled_execution_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--final-ready-check-root", default=DEFAULT_READY)
    p.add_argument("--authorization-decision-root", default=DEFAULT_AUTH)
    p.add_argument("--minimal-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    args = p.parse_args()

    result = run_ocr_real_dependency_real_minimal_controlled_execution_v1(
        ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root=args.final_ready_check_root,
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
                "execution_completed": sm.get("execution_completed"),
                "checks_passed": sm.get("checks_passed"),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "failure_routes": sm.get("failure_routes_triggered"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("execution_completed") and sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
