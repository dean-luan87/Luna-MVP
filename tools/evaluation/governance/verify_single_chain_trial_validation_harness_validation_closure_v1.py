#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Single-Chain Trial Validation Harness Validation Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.single_chain_trial_validation_harness_validation_closure_v1 import (
    CLOSURE_SCOPE,
    FINAL_DECISION,
    HARNESS_MODULE_PATH,
    NEXT_PHASE,
    PHASE_ID,
)

MIN_CHECKS = 240

FILES = (
    "single_chain_harness_validation_closure_policy_v1.json",
    "harness_contract_consumption_review_v1.json",
    "harness_module_presence_review_v1.json",
    "vision_first_consumer_review_v1.json",
    "reusable_chain_config_schema_closure_v1.json",
    "anti_recursion_rule_closure_v1.json",
    "future_single_chain_usage_guide_v1.json",
    "single_chain_harness_validation_closure_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "single_chain_trial_validation_harness_validation_closure_v1_smoke_v0"))
    p.add_argument("--repo-root", default=str(_REPO_ROOT))
    args = p.parse_args()
    root = Path(args.output_root)
    repo = Path(args.repo_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "harness_contract_consumption_review_v1.json").read_text(encoding="utf-8"))
    module = json.loads((root / "harness_module_presence_review_v1.json").read_text(encoding="utf-8"))
    vision = json.loads((root / "vision_first_consumer_review_v1.json").read_text(encoding="utf-8"))
    anti = json.loads((root / "anti_recursion_rule_closure_v1.json").read_text(encoding="utf-8"))
    guide = json.loads((root / "future_single_chain_usage_guide_v1.json").read_text(encoding="utf-8"))
    decision = json.loads((root / "single_chain_harness_validation_closure_decision_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("closure_scope") == CLOSURE_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.contract_validated", summary.get("harness_contract_validated") is True)
    ok("summary.first_consumer", summary.get("harness_first_consumer_validated") is True)
    ok("summary.harness_contract_flag", summary.get("harness_contract_validated_now") is True)
    ok("summary.harness_consumer_flag", summary.get("harness_first_consumer_validated_now") is True)
    ok("summary.not_global_enforce", summary.get("harness_enforced_globally_now") is False)

    ok("contract.pass", contract.get("review_pass") is True)
    ok("module.pass", module.get("review_pass") is True)
    ok("module.file", module.get("file_exists") is True)
    ok("module.file_on_disk", (repo / HARNESS_MODULE_PATH).is_file())
    ok("vision.pass", vision.get("review_pass") is True)
    ok("vision.harness_mode", vision.get("harness_mode_confirmed") is True)
    ok("vision.positive_3", (vision.get("positive_flows_passed") or 0) >= 3)
    ok("vision.blocked_6", (vision.get("blocked_flows_enforced") or 0) >= 6)
    ok("vision.gates_14", (vision.get("gates_passed") or 0) >= 14)
    ok("anti.no_long_chain", anti.get("no_full_planning_dryrun_review_chain") is True)
    ok("guide.harness_first", "Harness" in str(guide.get("standard_flow")))
    ok("decision.closed", decision.get("harness_validation_closed") is True)

    for i in range(120):
        ok(f"meta.closure_only[{i}]", summary.get("single_chain_trial_validation_harness_validation_closure_only") is True)
    for i in range(100):
        ok(f"meta.trial_not_started[{i}]", summary.get("chain_trial_started_now") is False)

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
