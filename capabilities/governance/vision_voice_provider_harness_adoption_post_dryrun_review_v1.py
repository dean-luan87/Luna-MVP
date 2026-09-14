# -*- coding: utf-8 -*-
"""Vision / Voice Provider Harness Adoption Post-DryRun Review v1 — closure only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_voice_provider_harness_adoption_dryrun_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.vision_voice_provider_harness_adoption_planning_v1 import (
    ADOPTION_BLOCKED_PATHS,
    HARNESS_SUB_CONTRACTS,
    VISION_CANDIDATES,
    VISION_FAILURE_ROUTES,
    VOICE_CANDIDATES,
    VOICE_FAILURE_ROUTES,
)

PHASE_ID = "Phase-Vision-Voice-Provider-Harness-Adoption-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "vision_voice_provider_harness_adoption_post_dryrun_review_only"
SOURCE_CHAIN = "vision_voice_provider_harness_adoption_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_PROVIDER_HARNESS_GENERALIZATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = (
    "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Provider-Harness-Generalization-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Voice-Provider-Harness-Adoption-Issue-Review-v1-001"

EXPECTED_VISION_FAMILIES: Set[str] = {c["provider_family"] for c in VISION_CANDIDATES}
EXPECTED_VOICE_FAMILIES: Set[str] = {c["provider_family"] for c in VOICE_CANDIDATES}
VOICE_OUTPUT_CONTRACTS: Set[str] = {"transcript_candidate", "speech_response_candidate"}

READINESS_BOOL_FLAGS: Tuple[Tuple[str, bool], ...] = (
    ("controlled_trial_required", True),
    ("dependency_check_required", True),
    ("environment_check_required", True),
    ("health_binding_required", True),
    ("constitution_gate_required", True),
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_vision_provider_readiness_candidate_generated_now",
    "new_voice_provider_readiness_candidate_generated_now",
    "harness_runtime_enforced_globally_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_vision_model_invoked_now",
    "live_camera_enabled_now",
    "image_read_executed_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "voice_output_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ Vision provider enabled",
    "Post-DryRun Review GO ≠ Voice provider enabled",
    "Harness adoption closure ≠ global runtime enforcement",
    "Vision readiness ≠ live camera allowed",
    "Voice readiness ≠ ASR/TTS allowed",
    "speech_response_candidate ≠ TTS output",
    "transcript_candidate ≠ task commit",
    "Harness generalization ≠ Map/Library/Hive/Memory adopted",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "vision_voice_provider_harness_adoption_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_vision_provider_readiness_candidate_generated_now"] = False
    meta["new_voice_provider_readiness_candidate_generated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_contract_matrix(matrix: Dict[str, Any], domain: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    issues: List[Dict[str, Any]] = []
    rows = matrix.get("rows") or []
    if matrix.get("row_count") != len(HARNESS_SUB_CONTRACTS) or len(rows) != len(HARNESS_SUB_CONTRACTS):
        issues.append({"issue_id": "count", "detail": f"expected {len(HARNESS_SUB_CONTRACTS)} contracts"})
    if matrix.get("all_mapped") is not True:
        issues.append({"issue_id": "all_mapped", "detail": "must be true"})
    for contract in HARNESS_SUB_CONTRACTS:
        row = next((r for r in rows if r.get("sub_contract") == contract), {})
        if row.get("mapped") is not True:
            issues.append({"issue_id": contract, "detail": "mapped must be true"})
        if row.get("domain_specific_required_fields_satisfied") is not True:
            issues.append({"issue_id": f"{contract}_fields", "detail": "domain fields required"})
        if row.get("ocr_specific_fields_required") is not False:
            issues.append({"issue_id": f"{contract}_ocr", "detail": "ocr fields must be false"})
    review = {
        "review_id": f"{domain}_harness_contract_consumption_review_v1",
        "provider_domain": domain,
        "row_count": matrix.get("row_count"),
        "all_mapped": matrix.get("all_mapped"),
        "issues": issues,
        "review_pass": len(issues) == 0,
    }
    return review, issues


def _review_failure_routes(
    failure_doc: Dict[str, Any],
    *,
    domain: str,
    expected_routes: Tuple[Dict[str, str], ...],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    issues: List[Dict[str, Any]] = []
    routes = failure_doc.get("routes") or []
    if failure_doc.get("route_count") != len(expected_routes) or len(routes) != len(expected_routes):
        issues.append({"issue_id": "count", "detail": f"expected {len(expected_routes)} routes"})
    route_map = {(r.get("trigger"), r.get("route")) for r in routes}
    for expected in expected_routes:
        pair = (expected["trigger"], expected["route"])
        if pair not in route_map:
            issues.append({"issue_id": expected["trigger"], "detail": f"missing route {expected['route']}"})
    for route in routes:
        if route.get("executed_now") is True:
            issues.append({"issue_id": route.get("trigger"), "detail": "executed_now must be false"})
    review = {
        "review_id": f"{domain}_failure_route_review_v1",
        "route_count": failure_doc.get("route_count"),
        "issues": issues,
        "review_pass": len(issues) == 0,
    }
    return review, issues


def run_vision_voice_provider_harness_adoption_post_dryrun_review_v1(
    *,
    vision_voice_provider_harness_adoption_dryrun_root: str,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(vision_voice_provider_harness_adoption_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or dryrun_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "vision_voice_provider_harness_adoption_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun simulated must be true")
    if dryrun_sm.get("vision_provider_readiness_candidate_generated_now") is not True:
        blockers.append("vision readiness candidate must have been generated in dryrun")
    if dryrun_sm.get("voice_provider_readiness_candidate_generated_now") is not True:
        blockers.append("voice readiness candidate must have been generated in dryrun")

    for field in BOUNDARY_FALSE:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    if harness_vr.get("verifier") != "GO":
        blockers.append("harness verifier should be GO")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")

    vision_ready = _try_read_json(dryrun_root / "vision_provider_readiness_candidate_v1.json") or {}
    voice_ready = _try_read_json(dryrun_root / "voice_provider_readiness_candidate_v1.json") or {}
    vision_matrix = _try_read_json(dryrun_root / "vision_harness_contract_consumption_matrix_v1.json") or {}
    voice_matrix = _try_read_json(dryrun_root / "voice_harness_contract_consumption_matrix_v1.json") or {}
    vision_failure = _try_read_json(dryrun_root / "vision_failure_route_dryrun_result_v1.json") or {}
    voice_failure = _try_read_json(dryrun_root / "voice_failure_route_dryrun_result_v1.json") or {}
    boundary_guard = _try_read_json(dryrun_root / "vision_voice_boundary_guard_dryrun_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "vision_voice_harness_adoption_blocked_path_result_v1.json") or {}
    generalization = _try_read_json(dryrun_root / "harness_generalization_dryrun_result_v1.json") or {}
    no_runtime = _try_read_json(dryrun_root / "vision_voice_no_runtime_audit_v1.json") or {}

    input_review = {
        "review_id": "vision_voice_harness_adoption_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "vision_candidate_count": vision_ready.get("candidate_count"),
        "voice_candidate_count": voice_ready.get("candidate_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    vision_issues: List[Dict[str, Any]] = []
    if vision_ready.get("provider_domain") != "vision":
        vision_issues.append({"issue_id": "domain", "detail": "must be vision"})
    families = {c.get("provider_family") for c in vision_ready.get("candidates") or []}
    if families != EXPECTED_VISION_FAMILIES:
        vision_issues.append({"issue_id": "families", "detail": f"expected {EXPECTED_VISION_FAMILIES}"})
    if vision_ready.get("candidate_count") != len(VISION_CANDIDATES):
        vision_issues.append({"issue_id": "count", "detail": "expected 4 candidates"})
    if vision_ready.get("output_contract") != "visual_observation_candidate":
        vision_issues.append({"issue_id": "output_contract", "detail": "visual_observation_candidate"})
    if vision_ready.get("evidence_pack") != "visual_evidence_pack_candidate_later":
        vision_issues.append({"issue_id": "evidence_pack", "detail": "visual_evidence_pack_candidate_later"})
    for flag, expected in (
        ("live_camera_allowed", False),
        ("image_read_allowed", False),
        ("invocation_allowed", False),
    ):
        val = vision_ready.get(flag)
        if val is not None and val is not expected:
            vision_issues.append({"issue_id": flag, "detail": f"expected {expected}"})
    for c in vision_ready.get("candidates") or []:
        if c.get("invocation_allowed") is not False:
            vision_issues.append({"issue_id": c.get("provider_family"), "detail": "invocation_allowed false"})
        for key, expected in READINESS_BOOL_FLAGS:
            if c.get(key) is not expected:
                vision_issues.append({"issue_id": f"{c.get('provider_family')}_{key}", "detail": f"expected {expected}"})

    vision_review = {
        "review_id": "vision_provider_readiness_candidate_review_v1",
        "provider_domain": vision_ready.get("provider_domain"),
        "candidate_count": vision_ready.get("candidate_count"),
        "output_contract": vision_ready.get("output_contract"),
        "evidence_pack": vision_ready.get("evidence_pack"),
        "issues": vision_issues,
        "review_pass": len(vision_issues) == 0,
        **meta,
    }

    voice_issues: List[Dict[str, Any]] = []
    if voice_ready.get("provider_domain") != "voice":
        voice_issues.append({"issue_id": "domain", "detail": "must be voice"})
    vfamilies = {c.get("provider_family") for c in voice_ready.get("candidates") or []}
    if vfamilies != EXPECTED_VOICE_FAMILIES:
        voice_issues.append({"issue_id": "families", "detail": f"expected {EXPECTED_VOICE_FAMILIES}"})
    if voice_ready.get("candidate_count") != len(VOICE_CANDIDATES):
        voice_issues.append({"issue_id": "count", "detail": "expected 5 candidates"})
    contracts = set(voice_ready.get("output_contracts") or [])
    if contracts != VOICE_OUTPUT_CONTRACTS:
        voice_issues.append({"issue_id": "output_contracts", "detail": str(VOICE_OUTPUT_CONTRACTS)})
    if voice_ready.get("evidence_pack") != "voice_evidence_pack_candidate_later":
        voice_issues.append({"issue_id": "evidence_pack", "detail": "voice_evidence_pack_candidate_later"})
    for flag, expected in (
        ("asr_runtime_allowed", False),
        ("tts_runtime_allowed", False),
        ("voice_output_allowed", False),
    ):
        if voice_ready.get(flag) is not expected:
            voice_issues.append({"issue_id": flag, "detail": f"expected {expected}"})
    for c in voice_ready.get("candidates") or []:
        for key, expected in READINESS_BOOL_FLAGS:
            if c.get(key) is not expected:
                voice_issues.append({"issue_id": f"{c.get('provider_family')}_{key}", "detail": f"expected {expected}"})

    voice_review = {
        "review_id": "voice_provider_readiness_candidate_review_v1",
        "provider_domain": voice_ready.get("provider_domain"),
        "candidate_count": voice_ready.get("candidate_count"),
        "output_contracts": voice_ready.get("output_contracts"),
        "issues": voice_issues,
        "review_pass": len(voice_issues) == 0,
        **meta,
    }

    vision_contract_review, vision_contract_issues = _review_contract_matrix(vision_matrix, "vision")
    vision_contract_review = {**vision_contract_review, **meta}
    voice_contract_review, voice_contract_issues = _review_contract_matrix(voice_matrix, "voice")
    voice_contract_review = {**voice_contract_review, **meta}

    vision_failure_review, vision_failure_issues = _review_failure_routes(
        vision_failure, domain="vision", expected_routes=VISION_FAILURE_ROUTES
    )
    vision_failure_review = {**vision_failure_review, **meta}
    voice_failure_review, voice_failure_issues = _review_failure_routes(
        voice_failure, domain="voice", expected_routes=VOICE_FAILURE_ROUTES
    )
    voice_failure_review = {**voice_failure_review, **meta}

    boundary_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in (boundary_guard.get("paths") or blocked.get("paths") or [])}
    if boundary_guard.get("all_blocked") is not True:
        boundary_issues.append({"issue_id": "all_blocked", "detail": "boundary guard must pass"})
    if blocked.get("all_blocked") is not True:
        boundary_issues.append({"issue_id": "blocked_all", "detail": "blocked paths must pass"})
    if len(paths) != len(ADOPTION_BLOCKED_PATHS):
        boundary_issues.append({"issue_id": "count", "detail": f"expected {len(ADOPTION_BLOCKED_PATHS)}"})
    for pid in ADOPTION_BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            boundary_issues.append({"issue_id": pid, "detail": "must be blocked=true"})

    boundary_review = {
        "review_id": "vision_voice_boundary_guard_review_v1",
        "path_count": len(ADOPTION_BLOCKED_PATHS),
        "all_blocked": boundary_guard.get("all_blocked") and blocked.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    blocked_review = {
        "review_id": "vision_voice_harness_adoption_blocked_path_review_v1",
        "paths_total": len(ADOPTION_BLOCKED_PATHS),
        "all_blocked": blocked.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    gen_issues: List[Dict[str, Any]] = []
    gen_checks = (
        ("ocr_first_consumer_validated", True),
        ("vision_second_consumer_dryrun_pass", True),
        ("voice_third_consumer_dryrun_pass", True),
        ("map_library_hive_memory_future_only", True),
        ("no_automatic_consumer_runtime_enablement", True),
        ("no_ocr_specific_fields_leak", True),
        ("domain_config_required", True),
        ("anti_recursion_preserved", True),
        ("generalization_pass", True),
    )
    for key, expected in gen_checks:
        if generalization.get(key) is not expected:
            gen_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    generalization_review = {
        "review_id": "harness_generalization_review_v1",
        "harness_generalization_established": len(gen_issues) == 0,
        "ocr_first_consumer_validated": generalization.get("ocr_first_consumer_validated"),
        "vision_second_consumer_dryrun_pass": generalization.get("vision_second_consumer_dryrun_pass"),
        "voice_third_consumer_dryrun_pass": generalization.get("voice_third_consumer_dryrun_pass"),
        "issues": gen_issues,
        "review_pass": len(gen_issues) == 0,
        **meta,
    }

    no_runtime_issues: List[Dict[str, Any]] = []
    if no_runtime.get("audit_pass") is not True:
        no_runtime_issues.append({"issue_id": "audit_pass", "detail": "must pass"})
    runtime_flags = (
        "real_vision_model_invoked_now",
        "live_camera_enabled_now",
        "image_read_executed_now",
        "asr_runtime_invoked_now",
        "tts_runtime_invoked_now",
        "voice_output_generated_now",
        "provider_imported_now",
        "harness_adoption_execution_started_now",
    )
    for flag in runtime_flags:
        if no_runtime.get(flag) is not False:
            no_runtime_issues.append({"issue_id": flag, "detail": "must be false"})

    no_runtime_review = {
        "review_id": "vision_voice_no_runtime_review_v1",
        "audit_pass": no_runtime.get("audit_pass"),
        "issues": no_runtime_issues,
        "review_pass": len(no_runtime_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and vision_review.get("review_pass")
        and voice_review.get("review_pass")
        and vision_contract_review.get("review_pass")
        and voice_contract_review.get("review_pass")
        and vision_failure_review.get("review_pass")
        and voice_failure_review.get("review_pass")
        and boundary_review.get("review_pass")
        and blocked_review.get("review_pass")
        and generalization_review.get("review_pass")
        and no_runtime_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "vision_voice_harness_adoption_closure_decision_v1",
        "vision_voice_provider_harness_adoption_dryrun_closed": boundary_ok,
        "harness_generalization_established": boundary_ok,
        "vision_provider_readiness_candidate_trusted": boundary_ok,
        "voice_provider_readiness_candidate_trusted": boundary_ok,
        "ocr_vision_voice_three_consumer_harness_validated": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_provider_harness_generalization_roadmap_decision": boundary_ok,
        "do_not_enable_vision_provider_now": True,
        "do_not_enable_voice_provider_now": True,
        "do_not_enforce_harness_runtime_globally_now": True,
        "do_not_import_provider_now": True,
        "do_not_invoke_provider_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After harness adoption dryrun closure, short roadmap decision on "
            "OCR authorization vs Validation Factory bus — no runtime enablement"
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    all_issue_ids = (
        blockers
        + [i["issue_id"] for i in vision_issues]
        + [i["issue_id"] for i in voice_issues]
        + [i["issue_id"] for i in vision_contract_issues]
        + [i["issue_id"] for i in voice_contract_issues]
        + [i["issue_id"] for i in vision_failure_issues]
        + [i["issue_id"] for i in voice_failure_issues]
        + [i["issue_id"] for i in boundary_issues]
        + [i["issue_id"] for i in gen_issues]
        + [i["issue_id"] for i in no_runtime_issues]
    )

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": all_issue_ids,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "vision_voice_provider_harness_adoption_dryrun_closed": boundary_ok,
        "harness_generalization_established": boundary_ok,
        "vision_provider_readiness_candidate_trusted": boundary_ok,
        "voice_provider_readiness_candidate_trusted": boundary_ok,
        **meta,
    }

    return {
        "vision_voice_harness_adoption_dryrun_input_review": input_review,
        "vision_provider_readiness_candidate_review": vision_review,
        "voice_provider_readiness_candidate_review": voice_review,
        "vision_harness_contract_consumption_review": vision_contract_review,
        "voice_harness_contract_consumption_review": voice_contract_review,
        "vision_failure_route_review": vision_failure_review,
        "voice_failure_route_review": voice_failure_review,
        "vision_voice_boundary_guard_review": boundary_review,
        "harness_generalization_review": generalization_review,
        "vision_voice_no_runtime_review": no_runtime_review,
        "vision_voice_harness_adoption_blocked_path_review": blocked_review,
        "vision_voice_harness_adoption_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
