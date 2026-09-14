#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Minimal Execution Authorization Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_real_minimal_execution_authorization_decision_v1 import (
    run_ocr_real_dependency_real_minimal_execution_authorization_decision_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)
DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_planning"
)
DEFAULT_PREFLIGHT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_final_preflight"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_execution_authorization_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("real_minimal_execution_authorization_decision_policy", "real_minimal_execution_authorization_decision_policy_v1.json"),
    ("minimal_execution_dryrun_input_review", "minimal_execution_dryrun_input_review_v1.json"),
    ("real_execution_readiness_review", "real_execution_readiness_review_v1.json"),
    ("allowed_scope_authorization_review", "allowed_scope_authorization_review_v1.json"),
    ("forbidden_action_authorization_review", "forbidden_action_authorization_review_v1.json"),
    ("evidence_rollback_postreview_readiness_review", "evidence_rollback_postreview_readiness_review_v1.json"),
    ("execution_risk_boundary_review", "execution_risk_boundary_review_v1.json"),
    ("route_a_authorize_real_minimal_execution_assessment", "route_a_authorize_real_minimal_execution_assessment_v1.json"),
    ("route_b_hold_for_owner_confirmation_assessment", "route_b_hold_for_owner_confirmation_assessment_v1.json"),
    ("route_c_hold_for_environment_precheck_assessment", "route_c_hold_for_environment_precheck_assessment_v1.json"),
    ("route_d_defer_and_return_to_provider_selection_assessment", "route_d_defer_and_return_to_provider_selection_assessment_v1.json"),
    ("real_minimal_execution_authorization_route_selection_matrix", "real_minimal_execution_authorization_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--planning-root", default=DEFAULT_PLAN)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    p.add_argument("--ocr-via-factory-dryrun-root", default=DEFAULT_OCR_DR)
    args = p.parse_args()

    result = run_ocr_real_dependency_real_minimal_execution_authorization_decision_v1(
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root=args.dryrun_root,
        ocr_real_dependency_minimal_controlled_execution_planning_root=args.planning_root,
        ocr_real_dependency_execution_final_preflight_root=args.final_preflight_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_via_factory_dryrun_root,
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
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "selected_route": sm.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
