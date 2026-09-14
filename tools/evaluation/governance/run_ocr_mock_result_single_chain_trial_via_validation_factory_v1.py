#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Mock Result Single-Chain Trial Via Validation Factory v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    run_ocr_mock_result_single_chain_trial_via_validation_factory_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_mock_result_single_chain_trial_via_validation_factory"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_mock_chain_config", "ocr_mock_chain_config_v1.json"),
    ("ocr_mock_chain_validation_result", "ocr_mock_chain_validation_result_v1.json"),
    ("ocr_mock_authorization_config", "ocr_mock_authorization_config_v1.json"),
    ("ocr_mock_authorization_validation_result", "ocr_mock_authorization_validation_result_v1.json"),
    ("ocr_mock_controlled_trial_execution_result", "ocr_mock_controlled_trial_execution_result_v1.json"),
    ("ocr_mock_post_execution_review_result", "ocr_mock_post_execution_review_result_v1.json"),
    ("ocr_mock_candidate_output_contract_review", "ocr_mock_candidate_output_contract_review_v1.json"),
    ("ocr_mock_no_runtime_boundary_audit", "ocr_mock_no_runtime_boundary_audit_v1.json"),
    ("ocr_mock_trial_closure_decision", "ocr_mock_trial_closure_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-post-execution-review-root",
        required=True,
    )
    p.add_argument("--luna-validation-factory-consolidation-root", required=True)
    args = p.parse_args()

    result = run_ocr_mock_result_single_chain_trial_via_validation_factory_v1(
        vision_sample_frame_single_chain_controlled_trial_post_execution_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_post_execution_review_root
        ),
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
