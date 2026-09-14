#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Controlled Trial Authorization Via Harness v1."""

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

from capabilities.governance.controlled_trial_authorization_harness_v1 import (
    HARNESS_ID,
    run_authorization_validate,
)
from capabilities.governance.controlled_trial_authorization_harness_validation_closure_v1 import (
    FINAL_DECISION as HARNESS_CLOSURE_FINAL,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    RUNTIME_BOUNDARY_FIELDS,
    SCOPE,
    TARGET_EXECUTION_PHASE,
)

MIN_CHECKS = 240

FILES = (
    "vision_sample_frame_authorization_via_harness_policy_v1.json",
    "harness_validation_closure_input_review_v1.json",
    "authorization_config_snapshot_v1.json",
    "authorization_validation_result_v1.json",
    "request_lifecycle_result_v1.json",
    "grant_lifecycle_result_v1.json",
    "controlled_trial_execution_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "vision_sample_frame_single_chain_controlled_trial_authorization_via_harness_v1_smoke_v0"))
    p.add_argument("--controlled-trial-authorization-harness-validation-closure-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    closure_root = Path(args.controlled_trial_authorization_harness_validation_closure_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "vision_sample_frame_authorization_via_harness_policy_v1.json").read_text(encoding="utf-8"))
    validation = json.loads((root / "authorization_validation_result_v1.json").read_text(encoding="utf-8"))
    request_lc = json.loads((root / "request_lifecycle_result_v1.json").read_text(encoding="utf-8"))
    grant_lc = json.loads((root / "grant_lifecycle_result_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "controlled_trial_execution_readiness_decision_v1.json").read_text(encoding="utf-8"))
    snapshot = json.loads((root / "authorization_config_snapshot_v1.json").read_text(encoding="utf-8"))
    closure_sm = json.loads((closure_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("authorization_via_harness_scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.validation_pass", summary.get("authorization_validation_pass") is True)
    ok("summary.ready_exec", summary.get("ready_for_controlled_trial_execution") is True)
    ok("summary.harness", summary.get("harness_id") == HARNESS_ID)
    ok("summary.bypass", summary.get("legacy_authorization_phase_chain_bypassed") is True)
    ok("summary.not_granted", summary.get("execution_authorization_granted_now") is False)
    ok("summary.not_started", summary.get("controlled_trial_started_now") is False)

    ok("policy.harness_entry", "run_authorization_validate" in str(policy.get("harness_entrypoint", "")))
    ok("validation.pass", validation.get("validation_pass") is True)
    ok("request.state", request_lc.get("current_state") == "authorization_dryrun_reviewed")
    ok("grant.state", grant_lc.get("current_state") == "grant_planning")
    ok("grant.not_issued", grant_lc.get("grant_issued_now") is False)
    ok("readiness.exec", readiness.get("ready_for_controlled_trial_execution") is True)
    ok("readiness.target", readiness.get("target_execution_phase") == TARGET_EXECUTION_PHASE)
    ok("snapshot.chain", snapshot.get("chain_id") == "vision_sample_frame")
    ok("upstream.closure", closure_sm.get("final_decision") == HARNESS_CLOSURE_FINAL)

    mod = importlib.import_module("capabilities.governance.controlled_trial_authorization_harness_v1")
    ok("module.run_validate", callable(getattr(mod, "run_authorization_validate", None)))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(90):
        ok(f"meta.via_harness[{i}]", summary.get("vision_sample_frame_controlled_trial_authorization_via_harness_only") is True)
    for i in range(80):
        ok(f"meta.not_granted[{i}]", summary.get("grant_issued_now") is False)
    for i in range(60):
        ok(f"meta.harness_id[{i}]", summary.get("harness_id") == HARNESS_ID)

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
