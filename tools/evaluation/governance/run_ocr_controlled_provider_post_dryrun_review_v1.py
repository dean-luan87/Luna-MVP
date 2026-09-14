#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Controlled Provider Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_post_dryrun_review_v1 import (
    run_ocr_controlled_provider_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_controlled_provider_dryrun_input_review", "ocr_controlled_provider_dryrun_input_review_v1.json"),
    ("ocr_provider_readiness_review", "ocr_provider_readiness_review_v1.json"),
    ("ocr_request_candidate_review", "ocr_request_candidate_review_v1.json"),
    ("ocr_roi_candidate_review", "ocr_roi_candidate_review_v1.json"),
    ("ocr_result_candidate_review", "ocr_result_candidate_review_v1.json"),
    ("ocr_evidence_pack_candidate_review", "ocr_evidence_pack_candidate_review_v1.json"),
    ("ocr_candidate_chain_trace_review", "ocr_candidate_chain_trace_review_v1.json"),
    ("ocr_branch_review", "ocr_branch_review_v1.json"),
    ("ocr_health_binding_review", "ocr_health_binding_review_v1.json"),
    ("ocr_constitution_boundary_review", "ocr_constitution_boundary_review_v1.json"),
    ("ocr_no_runtime_boundary_review", "ocr_no_runtime_boundary_review_v1.json"),
    ("ocr_blocked_path_review", "ocr_blocked_path_review_v1.json"),
    ("ocr_controlled_provider_closure_decision", "ocr_controlled_provider_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-controlled-provider-dryrun-root", default=DEFAULT_DRYRUN)
    args = p.parse_args()

    result = run_ocr_controlled_provider_post_dryrun_review_v1(
        ocr_controlled_provider_dryrun_root=args.ocr_controlled_provider_dryrun_root,
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
                "ocr_controlled_provider_dryrun_closed": sm.get("ocr_controlled_provider_dryrun_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
