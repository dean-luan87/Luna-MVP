#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Provider Abstraction Standard Alignment DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONSISTENCY_FIELDS,
    DOMAIN_LIST,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    STANDARD_ID,
    UNIFIED_PRINCIPLES,
)
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

MIN_CHECKS = 279

REQUIRED = (
    "provider_abstraction_standard_alignment_dryrun_review_policy_v1.json",
    "provider_abstraction_planning_input_review_v1.json",
    "provider_abstraction_standard_candidate_v1.json",
    "provider_candidate_contract_sample_v1.json",
    "provider_adapter_boundary_sample_v1.json",
    "provider_readiness_binding_sample_v1.json",
    "provider_selection_authorization_sample_v1.json",
    "provider_switch_policy_sample_v1.json",
    "domain_provider_alignment_matrix_candidate_v1.json",
    "ocr_provider_alignment_dryrun_review_v1.json",
    "vision_provider_alignment_dryrun_review_v1.json",
    "voice_asr_provider_alignment_dryrun_review_v1.json",
    "voice_tts_provider_alignment_dryrun_review_v1.json",
    "map_provider_alignment_dryrun_review_v1.json",
    "library_hive_memory_provider_alignment_dryrun_review_v1.json",
    "legacy_provider_reference_absorption_marker_v1.json",
    "provider_abstraction_consistency_rule_review_v1.json",
    "provider_abstraction_boundary_audit_v1.json",
    "provider_abstraction_blocked_path_result_v1.json",
    "provider_abstraction_closure_decision_v1.json",
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
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_planning"
        ),
    )
    p.add_argument(
        "--fmis-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_frontend_model_influence_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--tts-runtime-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.planning_root)
    fmis_root = Path(args.fmis_dryrun_root)
    tts_dr_root = Path(args.tts_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")
    fmis_vr = _load(fmis_root / "verifier_report.json")
    fmis_sm = _load(fmis_root / "summary.json")
    tts_dr_sm = _load(tts_dr_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "provider_abstraction_standard_alignment_dryrun_review_policy_v1.json")
    input_review = _load(root / "provider_abstraction_planning_input_review_v1.json")
    standard = _load(root / "provider_abstraction_standard_candidate_v1.json")
    candidate = _load(root / "provider_candidate_contract_sample_v1.json")
    adapter = _load(root / "provider_adapter_boundary_sample_v1.json")
    readiness = _load(root / "provider_readiness_binding_sample_v1.json")
    selection = _load(root / "provider_selection_authorization_sample_v1.json")
    switch = _load(root / "provider_switch_policy_sample_v1.json")
    matrix = _load(root / "domain_provider_alignment_matrix_candidate_v1.json")
    ocr = _load(root / "ocr_provider_alignment_dryrun_review_v1.json")
    vision = _load(root / "vision_provider_alignment_dryrun_review_v1.json")
    asr = _load(root / "voice_asr_provider_alignment_dryrun_review_v1.json")
    tts = _load(root / "voice_tts_provider_alignment_dryrun_review_v1.json")
    map_r = _load(root / "map_provider_alignment_dryrun_review_v1.json")
    lhm = _load(root / "library_hive_memory_provider_alignment_dryrun_review_v1.json")
    legacy = _load(root / "legacy_provider_reference_absorption_marker_v1.json")
    consistency = _load(root / "provider_abstraction_consistency_rule_review_v1.json")
    boundary = _load(root / "provider_abstraction_boundary_audit_v1.json")
    blocked = _load(root / "provider_abstraction_blocked_path_result_v1.json")
    closure = _load(root / "provider_abstraction_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)
    ok("upstream.fmis_go", fmis_vr.get("verifier") == "GO")
    ok("upstream.fmis_final", fmis_sm.get("final_decision") == FMIS_DR_FINAL_GO)
    ok("upstream.qianwen_not_invoked", tts_dr_sm.get("qianwen_tts_invoked_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("provider_abstraction_standard_alignment_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard", summary.get("standard_id") == STANDARD_ID)
    ok("summary.domains8", summary.get("domain_count") == 8)
    ok("summary.aligned8", summary.get("domains_aligned") == 8)

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:20]}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"summary.false.{field[:20]}", summary.get(field) is False)

    ok("policy.standard", policy.get("standard_id") == STANDARD_ID)
    ok("policy.sim_not_runtime", policy.get("simulated_not_runtime") is True)

    ok("input_review.pass", input_review.get("review_pass") is True)
    ok("input_review.standard", input_review.get("standard_id") == STANDARD_ID)
    ok("input_review.qianwen", input_review.get("qianwen_registered_not_invoked") is True)

    ok("standard.id", standard.get("standard_id") == STANDARD_ID)
    ok("standard.scope", standard.get("standard_scope") == "cross_domain_provider_type_modules")
    ok("standard.abstract", standard.get("runtime_core_is_abstract") is True)
    ok("standard.candidate_only", standard.get("candidate_only") is True)
    ok("standard.principles_pass", standard.get("unified_principles_all_pass") is True)
    for pr in UNIFIED_PRINCIPLES:
        ok(f"standard.pr.{pr[:16]}", pr in (standard.get("unified_principles") or []))

    ok("candidate.id", candidate.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("candidate.candidate_only", candidate.get("candidate_only") is True)
    ok("candidate.not_selected", candidate.get("selected_for_execution") is False)
    ok("candidate.not_invoked", candidate.get("invoked_now") is False)
    for field in (
        "provider_candidate_id",
        "provider_domain",
        "provider_type",
        "runtime_family",
        "adapter_ref",
        "capability_tags",
        "input_contract_ref",
        "output_contract_ref",
        "readiness_status",
        "selection_status",
        "invocation_status",
        "authorization_refs",
        "evidence_refs",
        "failure_route_refs",
        "fallback_candidate_refs",
        "boundary_status",
        "provider_specific_config_ref",
        "source_chain",
        "version_ref",
    ):
        ok(f"candidate.field.{field[:16]}", field in candidate)

    ok("adapter.pass", adapter.get("all_pass") is True)
    for key in adapter.get("checks", {}):
        ok(f"adapter.{key[:16]}", adapter["checks"][key] is True)

    ok("readiness.pass", readiness.get("all_pass") is True)
    for key in readiness.get("checks", {}):
        ok(f"readiness.{key[:16]}", readiness["checks"][key] is True)

    ok("selection.pass", selection.get("all_pass") is True)
    for key in selection.get("checks", {}):
        ok(f"selection.{key[:16]}", selection["checks"][key] is True)

    ok("switch.pass", switch.get("all_pass") is True)
    ok("switch.no_auto", switch.get("provider_auto_switch_executed_now") is False)
    for key in switch.get("checks", {}):
        ok(f"switch.{key[:16]}", switch["checks"][key] is True)

    ok("matrix.count8", matrix.get("domain_count") == 8)
    ok("matrix.all_aligned", matrix.get("all_domains_aligned") is True)
    ok("matrix.abstract", matrix.get("runtime_core_abstract_for_all_domains") is True)
    for domain in DOMAIN_LIST:
        ok(
            f"matrix.{domain[:10]}",
            any(e.get("provider_domain") == domain and e.get("alignment_pass") for e in (matrix.get("entries") or [])),
        )

    for review, name in (
        (ocr, "ocr"),
        (vision, "vision"),
        (asr, "asr"),
        (tts, "tts"),
        (map_r, "map"),
        (lhm, "lhm"),
    ):
        ok(f"{name}.pass", review.get("dryrun_review_pass") is True)
        for key, val in (review.get("checks") or {}).items():
            ok(f"{name}.{key[:14]}", val is True)
        for key, val in (review.get("boundary_checks") or {}).items():
            ok(f"{name}.boundary.{key[:12]}", val is False)

    ok("legacy.count5", legacy.get("marker_count") >= 5)
    for i, marker in enumerate(legacy.get("markers") or []):
        ok(f"legacy.{i}.absorbed", marker.get("absorbed_by") == STANDARD_ID)
        ok(f"legacy.{i}.readonly", marker.get("read_only_evidence_source") is True)
        ok(f"legacy.{i}.verdict", marker.get("historical_verdict_preserved") is True)
        ok(f"legacy.{i}.norewrite", marker.get("physical_rewrite_required") is False)

    ok("consistency.pass", consistency.get("dryrun_review_pass") is True)
    ok("consistency.fields14", consistency.get("field_count") == len(CONSISTENCY_FIELDS))
    for field in CONSISTENCY_FIELDS:
        ok(f"consistency.field.{field[:14]}", field in (consistency.get("fields") or []))

    ok("boundary.clear", boundary.get("all_boundaries_clear") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:16]}", boundary.get("boundary_checks", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count19", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:16]}",
            any(x.get("blocked_path") == bp and x.get("blocked") is True for x in (blocked.get("blocked_paths") or [])),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_display_gate_planning") is True)
    ok("next_route.go", next_route.get("provider_abstraction_simulated_go") is True)
    ok("next_route.next", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    for nc in NON_CLAIMS:
        ok(f"non_claims.{nc[:16]}", nc in (non_claims.get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    report = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "verifier": "GO" if passed == total and total > 0 else "HOLD",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "checks": checks,
        "non_claims": list(NON_CLAIMS),
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
