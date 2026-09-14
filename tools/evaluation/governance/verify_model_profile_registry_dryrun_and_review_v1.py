#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Profile Registry DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    IO_FORBIDDEN,
    IO_INPUT_TYPES,
    IO_OUTPUT_TYPES,
    LAYER_BINDING_FIELDS,
    LICENSE_METADATA_FIELDS,
    LIFECYCLE_STATES,
    MODEL_PROFILE_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
    SEED_CANDIDATE_IDS,
    STATUS_TAXONOMY,
)
from capabilities.governance.model_profile_registry_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    PHASE_ID as PLANNING_PHASE_ID,
)

MIN_CHECKS = 170

REQUIRED = (
    "model_profile_registry_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "model_profile_registry_candidate_v1.json",
    "model_profile_schema_review_v1.json",
    "model_profile_lifecycle_policy_review_v1.json",
    "model_profile_status_taxonomy_review_v1.json",
    "source_license_metadata_schema_review_v1.json",
    "capability_layer_binding_schema_review_v1.json",
    "model_input_output_profile_schema_review_v1.json",
    "model_quality_acceptance_profile_schema_review_v1.json",
    "health_validation_whitebox_profile_schema_review_v1.json",
    "provider_runtime_binding_profile_schema_review_v1.json",
    "version_update_replacement_profile_schema_review_v1.json",
    "registry_domain_index_review_v1.json",
    "seed_model_profile_candidates_review_v1.json",
    "vision_model_profile_seed_candidates_review_v1.json",
    "ocr_model_profile_seed_candidates_review_v1.json",
    "tts_model_profile_seed_candidates_review_v1.json",
    "asr_model_profile_seed_candidates_review_v1.json",
    "map_navigation_model_profile_seed_candidates_review_v1.json",
    "world_continuity_model_profile_seed_candidates_review_v1.json",
    "memory_emotion_evolution_model_profile_seed_candidates_review_v1.json",
    "module_local_binding_review_v1.json",
    "midplatform_governance_binding_review_v1.json",
    "registry_non_runtime_boundary_audit_v1.json",
    "registry_blocked_path_result_v1.json",
    "registry_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review",
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning",
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
    ok("upstream.seeds14", plan_sm.get("seed_candidate_count") == 14)

    summary = _load(root / "summary.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    candidate = _load(root / "model_profile_registry_candidate_v1.json")
    schema_r = _load(root / "model_profile_schema_review_v1.json")
    lifecycle_r = _load(root / "model_profile_lifecycle_policy_review_v1.json")
    status_r = _load(root / "model_profile_status_taxonomy_review_v1.json")
    seeds_r = _load(root / "seed_model_profile_candidates_review_v1.json")
    module_r = _load(root / "module_local_binding_review_v1.json")
    mid_r = _load(root / "midplatform_governance_binding_review_v1.json")
    boundary = _load(root / "registry_non_runtime_boundary_audit_v1.json")
    blocked = _load(root / "registry_blocked_path_result_v1.json")
    closure = _load(root / "registry_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.seeds14", summary.get("seed_candidate_count") == 14)
    ok("summary.schemas8", summary.get("schema_count") >= 8)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.reuse_rule", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("summary.new_need_false", summary.get("new_governance_need_proven") is False)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("gov_reuse.pass", gov_reuse.get("review_pass") is True)
    ok("gov_reuse.ref", gov_reuse.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("gov_reuse.rule", gov_reuse.get("phase_governance_standard_reuse_rule") is True)
    ok("gov_reuse.new_false", gov_reuse.get("new_governance_need_proven") is False)
    ok("gov_reuse.no_parallel", gov_reuse.get("no_parallel_duplicate_governance_standard") is True)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("candidate.registry_id", candidate.get("registry_id") == "luna_model_profile_registry_v1")
    ok("candidate.source", candidate.get("planning_source_phase") == PLANNING_PHASE_ID)
    ok("candidate.seeds14", candidate.get("seed_candidate_count") == 14)
    ok("candidate.schemas8", candidate.get("schema_count") >= 8)
    ok("candidate.no_runtime", candidate.get("registry_runtime_enabled_now") is False)
    ok("candidate.constraints", candidate.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("schema_r.pass", schema_r.get("review_pass") is True)
    ok("schema_r.fields31", schema_r.get("field_count") == len(MODEL_PROFILE_SCHEMA_FIELDS))

    ok("lifecycle_r.pass", lifecycle_r.get("review_pass") is True)
    ok("status_r.pass", status_r.get("review_pass") is True)
    ok("status_r.count11", len(STATUS_TAXONOMY) == 11)

    for review_name in (
        "source_license_metadata_schema_review_v1.json",
        "capability_layer_binding_schema_review_v1.json",
        "model_input_output_profile_schema_review_v1.json",
        "model_quality_acceptance_profile_schema_review_v1.json",
        "health_validation_whitebox_profile_schema_review_v1.json",
        "provider_runtime_binding_profile_schema_review_v1.json",
        "version_update_replacement_profile_schema_review_v1.json",
        "registry_domain_index_review_v1.json",
    ):
        ok(f"{review_name[:20]}.pass", _load(root / review_name).get("review_pass") is True)

    ok("seeds_r.pass", seeds_r.get("review_pass") is True)
    for sid in SEED_CANDIDATE_IDS:
        ok(f"seed.{sid[:18]}", seeds_r.get("review_pass") is True)

    for domain_review in (
        "vision_model_profile_seed_candidates_review_v1.json",
        "ocr_model_profile_seed_candidates_review_v1.json",
        "tts_model_profile_seed_candidates_review_v1.json",
        "asr_model_profile_seed_candidates_review_v1.json",
        "map_navigation_model_profile_seed_candidates_review_v1.json",
        "world_continuity_model_profile_seed_candidates_review_v1.json",
        "memory_emotion_evolution_model_profile_seed_candidates_review_v1.json",
    ):
        ok(f"{domain_review[:20]}.pass", _load(root / domain_review).get("review_pass") is True)

    ok("module_r.pass", module_r.get("review_pass") is True)
    ok("mid_r.pass", mid_r.get("review_pass") is True)

    ok("boundary.audit", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == 18)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("next.ready", next_route.get("ready_for_module_local_model_profile_standardization_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

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
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
