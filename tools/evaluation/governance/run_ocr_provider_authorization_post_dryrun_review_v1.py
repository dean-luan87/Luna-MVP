#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_post_dryrun_review_v1 import (
    run_ocr_provider_authorization_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun"
)
DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_provider_authorization_dryrun_input_review",
        "ocr_provider_authorization_dryrun_input_review_v1.json",
    ),
    ("authorization_request_candidate_review", "authorization_request_candidate_review_v1.json"),
    ("grant_candidate_review", "grant_candidate_review_v1.json"),
    ("execution_window_candidate_review", "execution_window_candidate_review_v1.json"),
    ("sandbox_boundary_candidate_review", "sandbox_boundary_candidate_review_v1.json"),
    ("rollback_candidate_review", "rollback_candidate_review_v1.json"),
    ("evidence_requirement_candidate_review", "evidence_requirement_candidate_review_v1.json"),
    ("owner_operator_approval_review", "owner_operator_approval_review_v1.json"),
    ("provider_selection_binding_review", "provider_selection_binding_review_v1.json"),
    ("authorization_lifecycle_review", "authorization_lifecycle_review_v1.json"),
    ("authorization_boundary_guard_review", "authorization_boundary_guard_review_v1.json"),
    ("authorization_blocked_path_review", "authorization_blocked_path_review_v1.json"),
    ("authorization_closure_decision", "authorization_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-provider-authorization-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--ocr-provider-authorization-planning-root", default=DEFAULT_PLANNING)
    args = p.parse_args()

    result = run_ocr_provider_authorization_post_dryrun_review_v1(
        ocr_provider_authorization_dryrun_root=args.ocr_provider_authorization_dryrun_root,
        ocr_provider_authorization_planning_root=args.ocr_provider_authorization_planning_root,
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
                "ocr_provider_authorization_dryrun_closed": sm.get("ocr_provider_authorization_dryrun_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
