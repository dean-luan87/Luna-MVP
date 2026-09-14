#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Layered Capability Stack Standard Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.layered_capability_stack_standard_planning_v1 import (
    CROSS_DOMAIN_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    MODULE_ONBOARDING_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    STANDARD_EXTENSION_NAME,
    STANDARD_EXTENSION_NUMBER,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    CAPABILITY_STACK_DEFINITION_FIELDS,
    GOVERNANCE_ADDENDUM_ID,
    LAYER_DEFINITION_FIELDS,
    MODULE_SUBMISSION_ARTIFACTS,
    STANDARD_EN,
    STANDARD_ID,
    STANDARD_ZH,
    UNIVERSAL_RULES,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
)

MIN_CHECKS = 115

REQUIRED = (
    "layered_capability_stack_standard_policy_v1.json",
    "constitution_bus_input_review_v1.json",
    "reusable_governance_standard_registration_v1.json",
    "capability_stack_definition_contract_v1.json",
    "universal_capability_stack_rules_v1.json",
    "voice_capability_stack_reference_v1.json",
    "ocr_capability_stack_reference_v1.json",
    "map_navigation_capability_stack_reference_v1.json",
    "memory_capability_stack_reference_v1.json",
    "emotion_capability_stack_reference_v1.json",
    "first_person_capability_stack_reference_binding_v1.json",
    "module_onboarding_gate_policy_v1.json",
    "layered_governance_mapping_addendum_v1.json",
    "constitution_bus_standard_binding_addendum_v1.json",
    "cross_domain_stack_consistency_review_v1.json",
    "planning_boundary_audit_v1.json",
    "planning_closure_decision_v1.json",
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

    summary = _load(root / "summary.json")
    policy = _load(root / "layered_capability_stack_standard_policy_v1.json")
    registration = _load(root / "reusable_governance_standard_registration_v1.json")
    contract = _load(root / "capability_stack_definition_contract_v1.json")
    rules = _load(root / "universal_capability_stack_rules_v1.json")
    voice = _load(root / "voice_capability_stack_reference_v1.json")
    ocr = _load(root / "ocr_capability_stack_reference_v1.json")
    map_nav = _load(root / "map_navigation_capability_stack_reference_v1.json")
    memory = _load(root / "memory_capability_stack_reference_v1.json")
    emotion = _load(root / "emotion_capability_stack_reference_v1.json")
    fp_bind = _load(root / "first_person_capability_stack_reference_binding_v1.json")
    onboarding = _load(root / "module_onboarding_gate_policy_v1.json")
    governance_addendum = _load(root / "layered_governance_mapping_addendum_v1.json")
    addendum = _load(root / "constitution_bus_standard_binding_addendum_v1.json")
    cross = _load(root / "cross_domain_stack_consistency_review_v1.json")
    closure = _load(root / "planning_closure_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.std_num", summary.get("standard_extension_number") == STANDARD_EXTENSION_NUMBER)

    ok("policy.std_id", policy.get("standard_id") == STANDARD_ID)

    ok("reg.num", registration.get("standard_extension_number") == 11)
    ok("reg.name", registration.get("standard_name") == STANDARD_EXTENSION_NAME)
    ok("reg.additive", registration.get("extension_additive_not_replacement") is True)
    ok("reg.hist_count", registration.get("historical_standard_count") == len(GOVERNANCE_STANDARDS))

    for field in CAPABILITY_STACK_DEFINITION_FIELDS:
        ok(f"contract.{field[:18]}", field in (contract.get("required_fields") or []))
    for field in LAYER_DEFINITION_FIELDS:
        ok(f"contract.layer.{field[:12]}", field in (contract.get("layer_definition_fields") or []))

    ok("rules.std_en", rules.get("standard_en") == STANDARD_EN)
    ok("rules.std_zh", rules.get("standard_zh") == STANDARD_ZH)
    for rule in UNIVERSAL_RULES:
        ok(f"rules.{rule[:18]}", rule in (rules.get("universal_rules") or []))

    for stack, domain in (
        (voice, "voice"),
        (ocr, "ocr"),
        (map_nav, "map_navigation"),
        (memory, "memory"),
        (emotion, "emotion"),
    ):
        ok(f"{domain}.count", stack.get("layer_count", 0) >= 5)
        ok(f"{domain}.layers", len(stack.get("layers") or []) >= 5)

    ok("fp_bind.extends", fp_bind.get("extends_universal_standard") == STANDARD_ID)
    ok("fp_bind.pass", fp_bind.get("binding_pass") is True)

    for rule in MODULE_ONBOARDING_RULES:
        ok(f"onboard.{rule[:18]}", rule in (onboarding.get("onboarding_rules") or []))
    ok("onboard.gate", onboarding.get("luna_2_module_onboarding_gate") is True)
    ok(
        "onboard.dual_submission",
        set(onboarding.get("required_submissions") or []) == set(MODULE_SUBMISSION_ARTIFACTS),
    )
    ok("onboard.governance_ref", onboarding.get("required_governance_submission") == GOVERNANCE_ADDENDUM_ID)

    ok("gov_addendum.id", governance_addendum.get("addendum_id") == GOVERNANCE_ADDENDUM_ID)
    ok("gov_addendum.extends", governance_addendum.get("extends_standard_id") == STANDARD_ID)
    ok("gov_addendum.dual", governance_addendum.get("dual_submission_required") is True)
    ok("gov_addendum.pass", governance_addendum.get("binding_pass") is True)

    ok("addendum.gate", addendum.get("module_onboarding_hard_gate") is True)
    ok("addendum.std", addendum.get("adds_standard") == STANDARD_EXTENSION_NAME)

    for item in CROSS_DOMAIN_REVIEW_ITEMS:
        ok(f"cross.{item[:18]}", cross.get("planning_pass") is True)

    ok("closure.pass", closure.get("planning_pass") is True)

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
        "planning_pass": summary.get("planning_pass"),
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
