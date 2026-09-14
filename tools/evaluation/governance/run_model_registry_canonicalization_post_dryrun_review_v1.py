#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Registry Canonicalization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    run_model_registry_canonicalization_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("canonicalization_dryrun_input_review", "canonicalization_dryrun_input_review_v1.json"),
    ("canonical_candidate_completeness_review", "canonical_candidate_completeness_review_v1.json"),
    ("schema_v0_compliance_review", "schema_v0_compliance_review_v1.json"),
    ("canonical_entry_validation_review", "canonical_entry_validation_review_v1.json"),
    ("taxonomy_validation_review", "taxonomy_validation_review_v1.json"),
    ("input_output_binding_review", "input_output_binding_review_v1.json"),
    ("health_fallback_binding_review", "health_fallback_binding_review_v1.json"),
    ("skill_relationship_review", "skill_relationship_review_v1.json"),
    ("candidate_output_contract_review", "candidate_output_contract_review_v1.json"),
    ("version_policy_review", "version_policy_review_v1.json"),
    ("runtime_boundary_review", "runtime_boundary_review_v1.json"),
    ("blocked_path_review", "blocked_path_review_v1.json"),
    ("canonical_registry_closure_decision", "canonical_registry_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--model-registry-canonicalization-dryrun-root", default=DEFAULT_DRYRUN)
    args = p.parse_args()

    result = run_model_registry_canonicalization_post_dryrun_review_v1(
        model_registry_canonicalization_dryrun_root=args.model_registry_canonicalization_dryrun_root,
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
                "b_lite_canonical_v0_baseline_closed": sm.get("b_lite_canonical_v0_baseline_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
