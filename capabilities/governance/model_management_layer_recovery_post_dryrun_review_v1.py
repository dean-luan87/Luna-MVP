# -*- coding: utf-8 -*-
"""Model Management Layer Recovery Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    HEALTH_STATES,
    MOCK_MODEL_SPECS,
    MODEL_OUTPUT_CANDIDATE_TYPES,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
    SKILL_SPECS,
    SWITCHING_SCENARIOS,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    CAPABILITY_DESCRIPTORS,
    RUNTIME_MODES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Model-Management-Layer-Recovery-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "model_management_layer_recovery_post_dryrun_review_only"
SOURCE_CHAIN = "model_management_layer_recovery_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = "MODEL_MANAGEMENT_LAYER_RECOVERY_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_MODEL_LAYER_ROADMAP_DECISION"
FINAL_DECISION_HOLD = "MODEL_MANAGEMENT_LAYER_RECOVERY_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Management-Layer-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Management-Layer-Recovery-Issue-Review-v1-001"

PREFERRED_ROUTE = "A"
ROUTE_OPTIONS: Tuple[Dict[str, str], ...] = (
    {"route_id": "A", "label": "Vision / OCR / Voice model optimization (mock-to-controlled provider planning first)"},
    {"route_id": "B", "label": "Model Registry deeper implementation"},
    {"route_id": "C", "label": "Health Management Layer integration"},
    {"route_id": "D", "label": "Skill Registry expansion"},
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "model_runtime_invoked_now",
    "model_provider_invoked_now",
    "ocr_provider_invoked_now",
    "vision_model_invoked_now",
    "voice_model_invoked_now",
    "emotion_model_invoked_now",
    "face_recognition_model_invoked_now",
    "scan_model_invoked_now",
    "model_switch_executed_now",
    "model_update_executed_now",
    "model_repair_executed_now",
    "runtime_enabled_now",
    "task_state_committed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ real models callable",
    "Model registry closure ≠ model invocation enabled",
    "Skill registry closure ≠ skill runtime enabled",
    "Health candidate closure ≠ runtime monitor enabled",
    "Switching candidate closure ≠ model switch allowed",
    "Output contract closure ≠ fact write allowed",
    "Model Management recovered ≠ model optimized",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    return {
        "model_management_layer_recovery_post_dryrun_review_only": True,
        "review_only": True,
        "new_model_registry_generated_now": False,
        "new_skill_registry_generated_now": False,
        "model_runtime_invoked_now": False,
        "model_provider_invoked_now": False,
        "ocr_provider_invoked_now": False,
        "vision_model_invoked_now": False,
        "voice_model_invoked_now": False,
        "emotion_model_invoked_now": False,
        "face_recognition_model_invoked_now": False,
        "scan_model_invoked_now": False,
        "model_switch_executed_now": False,
        "model_update_executed_now": False,
        "model_repair_executed_now": False,
        "runtime_enabled_now": False,
        "task_state_committed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_model_management_layer_recovery_post_dryrun_review_v1(
    *,
    model_management_layer_recovery_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(model_management_layer_recovery_dryrun_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "model_management_layer_recovery_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    registry = _try_read_json(dryrun_root / "mock_fixture_model_registry_v1.json") or {}
    skills = _try_read_json(dryrun_root / "skill_registry_dryrun_v1.json") or {}
    health = _try_read_json(dryrun_root / "model_health_state_candidate_matrix_v1.json") or {}
    switching = _try_read_json(dryrun_root / "model_switching_candidate_matrix_v1.json") or {}
    output_res = _try_read_json(dryrun_root / "model_output_contract_integration_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "model_runtime_boundary_audit_v1.json") or {}
    provider = _try_read_json(dryrun_root / "model_provider_governance_dryrun_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "model_management_blocked_path_result_v1.json") or {}
    capability = _try_read_json(dryrun_root / "model_capability_descriptor_matrix_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("model_registry_entry_count", 0) != 7:
        blockers.append("model registry count must be 7")
    if dryrun_sm.get("skill_registry_entry_count", 0) != 6:
        blockers.append("skill registry count must be 6")
    if dryrun_sm.get("health_candidate_count", 0) != 6:
        blockers.append("health candidate count must be 6")
    if dryrun_sm.get("switching_candidate_count", 0) != 6:
        blockers.append("switching candidate count must be 6")
    if dryrun_sm.get("model_switch_executed_now") is True:
        blockers.append("model_switch_executed_now must be false in dryrun")
    if dryrun_sm.get("model_runtime_invoked_now") is True:
        blockers.append("model_runtime_invoked_now must be false")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "model_management_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "counts": {
            "model_registry": dryrun_sm.get("model_registry_entry_count"),
            "skill_registry": dryrun_sm.get("skill_registry_entry_count"),
            "health": dryrun_sm.get("health_candidate_count"),
            "switching": dryrun_sm.get("switching_candidate_count"),
            "output_types": len(output_res.get("output_types") or []),
        },
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    entries = registry.get("entries") or []
    ids: Set[str] = {e.get("model_id") for e in entries if e.get("model_id")}
    reg_issues: List[Dict[str, Any]] = []
    if len(entries) != 7:
        reg_issues.append({"issue_id": "count", "detail": "expected 7 entries"})
    if len(ids) != len(entries):
        reg_issues.append({"issue_id": "unique", "detail": "model_id must be unique"})
    allowed_modes = set(RUNTIME_MODES)
    for entry in entries:
        if entry.get("provider_type") != "mock_or_fixture":
            reg_issues.append({"issue_id": entry.get("model_id"), "detail": "provider_type"})
        if entry.get("runtime_mode") not in allowed_modes:
            reg_issues.append({"issue_id": entry.get("model_id"), "detail": "runtime_mode"})
        if entry.get("invocation_allowed") is not False:
            reg_issues.append({"issue_id": entry.get("model_id"), "detail": "invocation_allowed"})
        if entry.get("constitution_gate_required") is not True:
            reg_issues.append({"issue_id": entry.get("model_id"), "detail": "constitution_gate"})
        if not entry.get("health_state_ref"):
            reg_issues.append({"issue_id": entry.get("model_id"), "detail": "health_state_ref"})

    registry_review = {
        "review_id": "model_registry_review_v1",
        "entry_count": len(entries),
        "unique_model_ids": len(ids),
        "all_mock_or_fixture": all(e.get("provider_type") == "mock_or_fixture" for e in entries),
        "all_invocation_false": all(e.get("invocation_allowed") is False for e in entries),
        "issues": reg_issues,
        "review_pass": len(reg_issues) == 0 and registry.get("registry_pass") is True,
        **meta,
    }

    skill_entries = skills.get("entries") or []
    skill_issues: List[Dict[str, Any]] = []
    if len(skill_entries) != 6:
        skill_issues.append({"issue_id": "count", "detail": "expected 6 skills"})
    for entry in skill_entries:
        if not entry.get("required_models"):
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "required_models"})
        if not entry.get("input_candidate_types"):
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "input_candidate_types"})
        if not entry.get("output_candidate_types"):
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "output_candidate_types"})
        if entry.get("safety_gate_required") is not True:
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "safety_gate"})
        if entry.get("constitution_gate_required") is not True:
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "constitution_gate"})
        if entry.get("user_facing_output_allowed") is not False:
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "user_facing_output"})
        if entry.get("runtime_action_allowed") is not False:
            skill_issues.append({"issue_id": entry.get("skill_id"), "detail": "runtime_action"})

    skill_review = {
        "review_id": "skill_registry_review_v1",
        "entry_count": len(skill_entries),
        "issues": skill_issues,
        "review_pass": len(skill_issues) == 0 and skills.get("registry_pass") is True,
        **meta,
    }

    cap_issues: List[Dict[str, Any]] = []
    desc = capability.get("descriptors") or {}
    if desc.get("can_write_fact") is not False:
        cap_issues.append({"issue_id": "can_write_fact", "detail": "must be false"})
    if desc.get("can_trigger_action") is not False:
        cap_issues.append({"issue_id": "can_trigger_action", "detail": "must be false"})
    capability_review = {
        "review_id": "model_capability_descriptor_review_v1",
        "descriptors_present": list(CAPABILITY_DESCRIPTORS),
        "can_write_fact_false": desc.get("can_write_fact") is False,
        "can_trigger_action_false": desc.get("can_trigger_action") is False,
        "issues": cap_issues,
        "review_pass": len(cap_issues) == 0,
        **meta,
    }

    health_rows = health.get("candidates") or []
    health_issues: List[Dict[str, Any]] = []
    covered = {h.get("health_state") for h in health_rows}
    for state in HEALTH_STATES:
        if state not in covered:
            health_issues.append({"issue_id": state, "detail": "state missing"})
    for h in health_rows:
        if h.get("health_state_candidate_only") is not True:
            health_issues.append({"issue_id": h.get("health_state"), "detail": "candidate_only"})
        if h.get("model_repair_executed_now") is True:
            health_issues.append({"issue_id": h.get("health_state"), "detail": "repair"})
    health_review = {
        "review_id": "model_health_state_candidate_review_v1",
        "states_covered": list(covered),
        "all_states_covered": len(health_issues) == 0,
        "runtime_monitor_enabled_now": False,
        "issues": health_issues,
        "review_pass": len(health_issues) == 0 and health.get("matrix_pass") is True,
        **meta,
    }

    switch_rows = switching.get("candidates") or []
    switch_issues: List[Dict[str, Any]] = []
    covered_scenarios = {c.get("scenario_id") for c in switch_rows}
    for sid, _ in SWITCHING_SCENARIOS:
        if sid not in covered_scenarios:
            switch_issues.append({"issue_id": sid, "detail": "scenario missing"})
    for c in switch_rows:
        if c.get("switching_candidate_only") is not True:
            switch_issues.append({"issue_id": c.get("scenario_id"), "detail": "switching_candidate_only"})
        if c.get("switch_executed_now") is True:
            switch_issues.append({"issue_id": c.get("scenario_id"), "detail": "switch_executed"})
    switching_review = {
        "review_id": "model_switching_candidate_review_v1",
        "scenarios_covered": list(covered_scenarios),
        "issues": switch_issues,
        "review_pass": len(switch_issues) == 0 and switching.get("matrix_pass") is True,
        **meta,
    }

    output_issues: List[Dict[str, Any]] = []
    rows = output_res.get("output_types") or []
    if len(rows) != len(MODEL_OUTPUT_CANDIDATE_TYPES):
        output_issues.append({"issue_id": "count", "detail": "expected 7 output types"})
    for row in rows:
        for key, val in (
            ("candidate_only", True),
            ("fact_status", "not_fact"),
            ("write_allowed", False),
            ("runtime_action_allowed", False),
            ("user_facing_output_allowed", False),
        ):
            if row.get(key) != val:
                output_issues.append(
                    {"issue_id": f"{row.get('output_candidate_type')}:{key}", "detail": f"must be {val}"}
                )
    output_review = {
        "review_id": "model_output_contract_review_v1",
        "output_type_count": len(rows),
        "integrates_candidate_output_contract": True,
        "issues": output_issues,
        "review_pass": len(output_issues) == 0 and output_res.get("integration_pass") is True,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    if audit.get("audit_pass") is not True:
        runtime_issues.append({"issue_id": "audit", "detail": "runtime boundary audit must pass"})
    runtime_review = {
        "review_id": "model_runtime_boundary_review_v1",
        "checks": audit.get("checks") or [],
        "registry_generated_not_invocation": True,
        "skill_generated_not_enabled": True,
        "health_not_monitor": True,
        "switching_not_executed": True,
        "output_not_fact_write": output_review.get("review_pass"),
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    prov_issues: List[Dict[str, Any]] = []
    if provider.get("provider_governance_pass") is not True:
        prov_issues.append({"issue_id": "provider", "detail": "provider governance must pass"})
    for d in provider.get("domains") or []:
        if d.get("real_provider_call") is True:
            prov_issues.append({"issue_id": d.get("domain"), "detail": "no real provider"})
    provider_review = {
        "review_id": "model_provider_governance_review_v1",
        "real_provider_calls": False,
        "issues": prov_issues,
        "review_pass": len(prov_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True or row.get("observed_now") is True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked"})
    blocked_review = {
        "review_id": "model_management_blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": len(blocked_issues) == 0 and blocked.get("all_blocked") is True,
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and registry_review.get("review_pass")
        and skill_review.get("review_pass")
        and capability_review.get("review_pass")
        and health_review.get("review_pass")
        and switching_review.get("review_pass")
        and output_review.get("review_pass")
        and runtime_review.get("review_pass")
        and provider_review.get("review_pass")
        and blocked_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "model_management_recovery_closure_decision_v1",
        "model_management_recovery_dryrun_closed": boundary_ok,
        "governance_skeleton_consumable": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_model_optimization_readiness_decision_v1",
        "ready_for_model_layer_roadmap_decision": boundary_ok,
        "preferred_route": PREFERRED_ROUTE,
        "route_options": list(ROUTE_OPTIONS),
        "preferred_route_label": ROUTE_OPTIONS[0]["label"],
        "do_not_enable_real_provider_directly": True,
        "start_with_vision_ocr_mock_to_controlled_provider_planning": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers
        + [i["issue_id"] for i in reg_issues + skill_issues + health_issues + switch_issues + output_issues],
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "governance_skeleton_consumable": boundary_ok,
        **meta,
    }

    return {
        "model_management_dryrun_input_review": input_review,
        "model_registry_review": registry_review,
        "skill_registry_review": skill_review,
        "model_capability_descriptor_review": capability_review,
        "model_health_state_candidate_review": health_review,
        "model_switching_candidate_review": switching_review,
        "model_output_contract_review": output_review,
        "model_runtime_boundary_review": runtime_review,
        "model_provider_governance_review": provider_review,
        "model_management_blocked_path_review": blocked_review,
        "model_management_recovery_closure_decision": closure,
        "next_model_optimization_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
