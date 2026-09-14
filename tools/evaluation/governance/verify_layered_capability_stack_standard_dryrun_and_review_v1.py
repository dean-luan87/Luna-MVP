#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Layered Capability Stack Standard DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    ADOPTION_REVIEW_ITEMS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    EXEMPLAR_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.layered_capability_stack_standard_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    CAPABILITY_STACK_DEFINITION_FIELDS,
    STANDARD_ID,
)

MIN_CHECKS = 70

REQUIRED = (
    "layered_capability_stack_standard_dryrun_policy_v1.json",
    "planning_input_review_v1.json",
    "sample_ocr_module_capability_stack_definition_v1.json",
    "standard_adoption_dryrun_review_v1.json",
    "exemplar_alignment_review_v1.json",
    "layer_dependency_validation_review_v1.json",
    "dryrun_blocked_path_result_v1.json",
    "dryrun_boundary_audit_v1.json",
    "dryrun_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "layered_capability_stack_standard_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "layered_capability_stack_standard_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    plan_sm = _load(Path(args.planning_root) / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)

    summary = _load(root / "summary.json")
    sample = _load(root / "sample_ocr_module_capability_stack_definition_v1.json")
    adoption = _load(root / "standard_adoption_dryrun_review_v1.json")
    exemplar = _load(root / "exemplar_alignment_review_v1.json")
    dep = _load(root / "layer_dependency_validation_review_v1.json")
    blocked = _load(root / "dryrun_blocked_path_result_v1.json")
    closure = _load(root / "dryrun_closure_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.std", summary.get("standard_id") == STANDARD_ID)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    for field in CAPABILITY_STACK_DEFINITION_FIELDS:
        ok(f"sample.{field[:18]}", field in sample)
    ok("sample.extends", sample.get("extends_standard_ref") == STANDARD_ID)
    ok("sample.domain", sample.get("capability_domain") == "ocr")
    ok("sample.layers6", sample.get("layer_count") == 6)

    for item in ADOPTION_REVIEW_ITEMS:
        ok(f"adoption.{item[:18]}", adoption.get("dryrun_and_review_pass") is True)
    for item in EXEMPLAR_REVIEW_ITEMS:
        ok(f"exemplar.{item[:18]}", exemplar.get("dryrun_and_review_pass") is True)

    ok("dep.valid", dep.get("dependency_chain_valid") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
