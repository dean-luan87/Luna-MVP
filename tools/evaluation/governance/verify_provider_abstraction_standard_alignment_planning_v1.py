#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Provider Abstraction Standard Alignment Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    BOUNDARY_MATRIX_FALSE,
    CONSISTENCY_FIELDS,
    DOMAIN_LIST,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    STANDARD_ID,
)
from capabilities.governance.midplatform_post_output_chain_simulation_roadmap_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_ROADMAP_FINAL_GO,
    ROUTE_A as ROUTE_A_LABEL,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)

MIN_CHECKS = 128

REQUIRED = (
    "provider_abstraction_standard_alignment_policy_v1.json",
    "post_output_chain_roadmap_input_review_v1.json",
    "provider_abstraction_standard_v1.json",
    "provider_candidate_contract_v1.json",
    "provider_adapter_boundary_contract_v1.json",
    "provider_readiness_binding_contract_v1.json",
    "provider_selection_authorization_policy_v1.json",
    "provider_switch_policy_v1.json",
    "domain_provider_alignment_matrix_v1.json",
    "ocr_provider_alignment_plan_v1.json",
    "vision_provider_alignment_plan_v1.json",
    "voice_asr_provider_alignment_plan_v1.json",
    "voice_tts_provider_alignment_plan_v1.json",
    "map_provider_alignment_plan_v1.json",
    "library_hive_memory_provider_alignment_plan_v1.json",
    "legacy_provider_reference_absorption_plan_v1.json",
    "provider_abstraction_consistency_rule_matrix_v1.json",
    "provider_abstraction_boundary_matrix_v1.json",
    "provider_abstraction_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "provider_abstraction_standard_alignment_planning_decision_v1.json",
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
            "provider_abstraction_standard_alignment_planning"
        ),
    )
    p.add_argument(
        "--roadmap-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_post_output_chain_simulation_roadmap_decision"
        ),
    )
    p.add_argument(
        "--tts-planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.roadmap_root)
    tts_plan_root = Path(args.tts_planning_root)

    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    tts_provider_register = _load(tts_plan_root / "current_tts_provider_candidate_register_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "provider_abstraction_standard_alignment_policy_v1.json")
    input_review = _load(root / "post_output_chain_roadmap_input_review_v1.json")
    standard = _load(root / "provider_abstraction_standard_v1.json")
    candidate_contract = _load(root / "provider_candidate_contract_v1.json")
    adapter_contract = _load(root / "provider_adapter_boundary_contract_v1.json")
    readiness = _load(root / "provider_readiness_binding_contract_v1.json")
    selection = _load(root / "provider_selection_authorization_policy_v1.json")
    switch = _load(root / "provider_switch_policy_v1.json")
    matrix = _load(root / "domain_provider_alignment_matrix_v1.json")
    legacy = _load(root / "legacy_provider_reference_absorption_plan_v1.json")
    consistency = _load(root / "provider_abstraction_consistency_rule_matrix_v1.json")
    boundary = _load(root / "provider_abstraction_boundary_matrix_v1.json")
    decision = _load(root / "provider_abstraction_standard_alignment_planning_decision_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == UPSTREAM_ROADMAP_FINAL_GO)
    ok("upstream.route_a", roadmap_sm.get("selected_route") == ROUTE_A_LABEL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("provider_abstraction_standard_alignment_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for f in BOUNDARY_MATRIX_FALSE:
        ok(f"boundary_false.{f[:18]}", summary.get(f) is False)

    ok("policy.phase", policy.get("phase") == PHASE_ID)
    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.standard_id", policy.get("standard_id") == STANDARD_ID)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.route", input_review.get("selected_route") == ROUTE_A_LABEL)
    ok("input.roadmap_final", input_review.get("roadmap_final_decision") == UPSTREAM_ROADMAP_FINAL_GO)
    ok("input.qianwen_ok", input_review.get("qianwen_registered_not_invoked") is True)

    ok("standard.id", standard.get("standard_id") == STANDARD_ID)
    ok("standard.runtime_abstract", standard.get("runtime_core_is_abstract") is True)
    ok("standard.candidate_machine", standard.get("provider_candidate_is_pluggable_machine") is True)
    ok("standard.adapter_boundary", standard.get("provider_adapter_is_boundary_layer") is True)
    ok("standard.readiness", standard.get("provider_readiness_required") is True)
    ok("standard.selection_auth", standard.get("provider_selection_requires_authorization") is True)
    ok("standard.invocation_window", standard.get("provider_invocation_requires_execution_window") is True)
    ok("standard.switch_policy", standard.get("provider_switch_requires_policy") is True)
    ok("standard.legacy_absorb", standard.get("historical_provider_specific_refs_are_absorbed_not_deleted") is True)

    ok("candidate.defaults", (candidate_contract.get("defaults") or {}).get("candidate_only") is True)
    ok("adapter.rules7", len(adapter_contract.get("rules") or []) >= 7)
    ok("readiness.harness_ref", readiness.get("controlled_provider_readiness_harness_ref") == "controlled_provider_readiness_harness_v1")
    ok("selection.rules6", len(selection.get("rules") or []) >= 6)
    ok("switch.auto_false", switch.get("provider_auto_switch_executed_now") is False)

    ok("matrix.domains8", matrix.get("domain_count") == 8)
    for d in DOMAIN_LIST:
        ok(f"matrix.domain.{d[:10]}", d in (matrix.get("domains") or []))

    markers = legacy.get("markers") or {}
    ok("legacy.absorbed_by", markers.get("absorbed_by") == STANDARD_ID)
    ok("legacy.read_only", markers.get("read_only_evidence_source") is True)
    ok("legacy.no_rewrite", markers.get("physical_rewrite_required") is False)
    ok("legacy.verdict_preserved", markers.get("historical_verdict_preserved") is True)
    ok("legacy.future_enforced", markers.get("future_new_phase_must_use_provider_abstraction") is True)

    ok("consistency.count", consistency.get("field_count") == len(CONSISTENCY_FIELDS))
    for f in CONSISTENCY_FIELDS:
        ok(f"consistency.{f[:18]}", f in (consistency.get("fields") or []))

    ok("boundary.all_false", boundary.get("all_false") is True)
    for f in BOUNDARY_MATRIX_FALSE:
        ok(f"boundary.{f[:18]}", boundary.get("matrix", {}).get(f) is False)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok(
        "qianwen_registered",
        any(
            x.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
            for x in (tts_provider_register.get("provider_candidates") or [])
        ),
    )

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    pass_all = summary.get("planning_pass") is True
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())

