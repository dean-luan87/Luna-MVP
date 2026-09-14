#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Execution Final Preflight v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    run_ocr_real_dependency_execution_final_preflight_v1,
)

DEFAULT_AUTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
)
DEFAULT_FORMAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
)
DEFAULT_EXEC_AUTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_AUTH_EXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_final_preflight"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_real_dependency_execution_final_preflight_policy", "ocr_real_dependency_execution_final_preflight_policy_v1.json"),
    ("authorization_dryrun_input_review", "authorization_dryrun_input_review_v1.json"),
    ("formal_request_authorization_candidate_review", "formal_request_authorization_candidate_review_v1.json"),
    ("owner_operator_approval_precheck_review", "owner_operator_approval_precheck_review_v1.json"),
    ("evidence_readiness_review", "evidence_readiness_review_v1.json"),
    ("validation_gate_readiness_review", "validation_gate_readiness_review_v1.json"),
    ("sandbox_boundary_readiness_review", "sandbox_boundary_readiness_review_v1.json"),
    ("allowed_check_final_preflight_review", "allowed_check_final_preflight_review_v1.json"),
    ("forbidden_action_final_preflight_review", "forbidden_action_final_preflight_review_v1.json"),
    ("rollback_readiness_review", "rollback_readiness_review_v1.json"),
    ("provider_selection_non_finalize_review", "provider_selection_non_finalize_review_v1.json"),
    ("health_signal_reserved_boundary_review", "health_signal_reserved_boundary_review_v1.json"),
    ("no_runtime_boundary_final_audit", "no_runtime_boundary_final_audit_v1.json"),
    ("controlled_execution_minimal_scope_plan", "controlled_execution_minimal_scope_plan_v1.json"),
    ("final_preflight_blocked_path_result", "final_preflight_blocked_path_result_v1.json"),
    ("final_preflight_closure_decision", "final_preflight_closure_decision_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--authorization-dryrun-root", default=DEFAULT_AUTH_DR)
    p.add_argument("--formal-dryrun-root", default=DEFAULT_FORMAL_DR)
    p.add_argument("--execution-authorization-dryrun-root", default=DEFAULT_EXEC_AUTH_DR)
    p.add_argument("--ocr-via-factory-dryrun-root", default=DEFAULT_OCR_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    p.add_argument("--auth-standard-extension-dryrun-root", default=DEFAULT_AUTH_EXT)
    args = p.parse_args()

    result = run_ocr_real_dependency_execution_final_preflight_v1(
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root=args.authorization_dryrun_root,
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root=args.formal_dryrun_root,
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=args.execution_authorization_dryrun_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_via_factory_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        capability_factory_authorization_standard_extension_dryrun_and_review_root=args.auth_standard_extension_dryrun_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
