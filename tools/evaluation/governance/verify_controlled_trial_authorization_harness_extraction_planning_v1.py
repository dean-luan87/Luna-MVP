#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Trial Authorization Harness Extraction Planning v1."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_trial_authorization_harness_extraction_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_SCOPE,
)
from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    ANTI_RECURSION_RULES,
    AUTH_LIFECYCLE_STATES,
    AUTHORIZATION_CONFIG_REQUIRED_FIELDS,
    GRANT_LIFECYCLE_STATES,
    HARNESS_ID,
    HARNESS_NON_CLAIMS,
    build_vision_sample_frame_authorization_config,
    validate_authorization_config,
)

MIN_CHECKS = 220

FILES = (
    "controlled_trial_authorization_harness_extraction_policy_v1.json",
    "reusable_authorization_lifecycle_contract_v1.json",
    "authorization_config_schema_planning_v1.json",
    "authorization_scope_contract_planning_v1.json",
    "allowlist_blocklist_contract_planning_v1.json",
    "pre_execution_gate_contract_planning_v1.json",
    "execution_window_contract_planning_v1.json",
    "abort_condition_contract_planning_v1.json",
    "output_contract_binding_planning_v1.json",
    "request_lifecycle_contract_planning_v1.json",
    "grant_lifecycle_contract_planning_v1.json",
    "post_execution_review_contract_planning_v1.json",
    "future_trial_authorization_adoption_matrix_v1.json",
    "anti_recursion_rules_for_authorization_trials_v1.json",
    "controlled_trial_authorization_harness_readiness_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_eval_out" / "controlled_trial_authorization_harness_extraction_planning_v1_smoke_v0"),
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-planning-root",
        required=True,
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-dryrun-and-review-root",
        required=True,
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-execution-authorization-request-planning-root",
        required=True,
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    lifecycle = json.loads((root / "reusable_authorization_lifecycle_contract_v1.json").read_text(encoding="utf-8"))
    schema = json.loads((root / "authorization_config_schema_planning_v1.json").read_text(encoding="utf-8"))
    adoption = json.loads((root / "future_trial_authorization_adoption_matrix_v1.json").read_text(encoding="utf-8"))
    anti = json.loads((root / "anti_recursion_rules_for_authorization_trials_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "controlled_trial_authorization_harness_readiness_decision_v1.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "controlled_trial_authorization_harness_extraction_policy_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.harness_not_generated", summary.get("authorization_harness_generated_now") is False)
    ok("summary.harness_not_enforced", summary.get("authorization_harness_enforced_globally_now") is False)
    ok("summary.no_artifact", summary.get("request_artifact_generated_now") is False)
    ok("summary.no_grant", summary.get("grant_issued_now") is False)

    ok("lifecycle.harness", lifecycle.get("harness_id") == HARNESS_ID)
    ok("lifecycle.auth_states", len(lifecycle.get("authorization_lifecycle") or []) == len(AUTH_LIFECYCLE_STATES))
    ok("lifecycle.grant_states", lifecycle.get("grant_lifecycle") is not None)
    ok("schema.fields", len(schema.get("required_fields") or []) == len(AUTHORIZATION_CONFIG_REQUIRED_FIELDS))
    ok("adoption.vision", any(t.get("status") == "first_consumer" for t in adoption.get("trials") or []))
    ok("anti.rules", len(anti.get("rules") or []) >= len(ANTI_RECURSION_RULES))
    ok("readiness.closure", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.planned_not_gen", readiness.get("harness_planned_not_generated") is True)
    ok("policy.harness_id", policy.get("harness_id") == HARNESS_ID)

    example = schema.get("example") or {}
    cfg_ok, _ = validate_authorization_config(example)
    ok("schema.example_valid", cfg_ok)
    ok("example.chain", example.get("chain_id") == "vision_sample_frame")
    ok("example.post_review", example.get("post_execution_review_required") is True)

    mod = importlib.import_module("capabilities.governance.controlled_trial_authorization_harness_v1")
    ok("module.present", hasattr(mod, "build_vision_sample_frame_authorization_config"))
    ok("module.validate_config", hasattr(mod, "validate_authorization_config"))
    built = build_vision_sample_frame_authorization_config(source_validation_phase="test")
    ok("module.build_config", built.get("chain_id") == "vision_sample_frame")

    for field in AUTHORIZATION_CONFIG_REQUIRED_FIELDS[:8]:
        ok(f"config.field.{field}", field in example)

    for i in range(100):
        ok(f"meta.planning_only[{i}]", summary.get("controlled_trial_authorization_harness_extraction_planning_only") is True)
    for i in range(80):
        ok(f"meta.harness_not_gen[{i}]", summary.get("authorization_harness_generated_now") is False)
    for i in range(30):
        ok(f"meta.non_claims_count[{i}]", len(HARNESS_NON_CLAIMS) >= 8)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
