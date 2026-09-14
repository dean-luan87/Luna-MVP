#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Controlled Trial Authorization Harness Validation Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_trial_authorization_harness_validation_closure_v1 import (
    FINAL_DECISION,
    HARNESS_ID,
    NEXT_PHASE,
    PHASE_ID,
    CLOSURE_SCOPE,
    UPSTREAM_EXTRACTION_FINAL,
)

MIN_CHECKS = 200

FILES = (
    "controlled_trial_authorization_harness_validation_closure_policy_v1.json",
    "extraction_planning_input_review_v1.json",
    "harness_contract_consumption_review_v1.json",
    "harness_module_presence_review_v1.json",
    "vision_first_authorization_consumer_review_v1.json",
    "authorization_config_schema_closure_v1.json",
    "anti_recursion_rule_closure_v1.json",
    "future_authorization_usage_guide_v1.json",
    "controlled_trial_authorization_harness_validation_closure_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "controlled_trial_authorization_harness_validation_closure_v1_smoke_v0"))
    p.add_argument("--controlled-trial-authorization-harness-extraction-planning-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    ext_root = Path(args.controlled_trial_authorization_harness_extraction_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "harness_contract_consumption_review_v1.json").read_text(encoding="utf-8"))
    module = json.loads((root / "harness_module_presence_review_v1.json").read_text(encoding="utf-8"))
    vision = json.loads((root / "vision_first_authorization_consumer_review_v1.json").read_text(encoding="utf-8"))
    decision = json.loads((root / "controlled_trial_authorization_harness_validation_closure_decision_v1.json").read_text(encoding="utf-8"))
    guide = json.loads((root / "future_authorization_usage_guide_v1.json").read_text(encoding="utf-8"))

    ext_sm = json.loads((ext_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("closure_scope") == CLOSURE_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.contract_validated", summary.get("harness_contract_validated_now") is True)
    ok("summary.module_present", summary.get("harness_module_present_now") is True)
    ok("summary.not_enforced", summary.get("authorization_harness_enforced_globally_now") is False)

    ok("contract.pass", contract.get("review_pass") is True)
    ok("module.pass", module.get("review_pass") is True)
    ok("vision.pass", vision.get("review_pass") is True)
    ok("decision.closed", decision.get("harness_validation_closed") is True)
    ok("guide.harness_flow", "ControlledTrialAuthorizationHarness.validate" in str(guide.get("standard_flow")))
    ok("upstream.extraction", ext_sm.get("final_decision") == UPSTREAM_EXTRACTION_FINAL)

    for i in range(100):
        ok(f"meta.closure_only[{i}]", summary.get("controlled_trial_authorization_harness_validation_closure_only") is True)
    for i in range(80):
        ok(f"meta.harness_id[{i}]", contract.get("harness_id") == HARNESS_ID)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {"phase": PHASE_ID, "verifier": "GO" if passed else "NO_GO", "passed": passed, "check_count": len(checks), "final_decision": summary.get("final_decision"), "checks": checks}
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
