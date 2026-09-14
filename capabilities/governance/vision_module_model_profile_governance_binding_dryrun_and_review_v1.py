# -*- coding: utf-8 -*-
"""Vision Module Model Profile + Governance Binding DryRunAndReview v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    DUAL_VALIDATION_MECHANISM_ID,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    VISION_REGISTRY_REFS,
)

PHASE_ID = "Phase-Vision-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
SCOPE = "vision_module_model_profile_governance_binding_dryrun_and_review_only"
SOURCE_CHAIN = "vision_module_model_profile_governance_binding_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "VISION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_OCR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING"
)
FINAL_DECISION_HOLD = (
    "VISION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Module-Model-Profile-Governance-Binding-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Vision Module Binding DryRun GO ≠ YOLO selected",
    "Vision Module Binding GO ≠ health metrics finalized",
    "Vision Module Binding GO ≠ supervision metrics finalized",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Health/Oversight ref attached ≠ health metrics finalized",
    "Supervision ref attached ≠ supervision metrics finalized",
    "qualification pass ≠ runtime ready",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "vision_module_model_profile_governance_binding_dryrun_and_review_only",
    "qualification_check_only",
    "simulated",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "vision_module_runtime_enabled_now",
    "camera_invoked_now",
    "real_frame_read_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "visual_fact_generated_now",
    "visual_action_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "qualification_mode": QUALIFICATION_MODE,
        **QUALIFICATION_FIELDS,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def run_vision_module_model_profile_governance_binding_dryrun_and_review_v1(
    *,
    vision_module_model_profile_governance_binding_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(vision_module_model_profile_governance_binding_planning_root).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    qual_plan = _try_read_json(plan_root / "vision_module_qualification_check_v1.json") or {}
    profile = _try_read_json(plan_root / "vision_module_local_model_profile_v1.json") or {}
    binding = _try_read_json(plan_root / "vision_midplatform_governance_binding_v1.json") or {}
    self_check = _try_read_json(plan_root / "vision_module_internal_self_check_plan_v1.json") or {}
    interaction = _try_read_json(plan_root / "vision_midplatform_interaction_check_plan_v1.json") or {}
    health = _try_read_json(plan_root / "vision_health_validation_whitebox_plan_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root), "upstream_planning_root": str(plan_root)}

    if plan_vr.get("verifier") != "GO":
        blockers.append("Vision Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if not plan_sm.get("qualification_check_only"):
        blockers.append("Planning must be qualification_check_only")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "qualification_mode": plan_sm.get("qualification_mode"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    registry_qual = _review_from_checks([
        ("registry_ref", profile.get("registry_ref") == REGISTRY_REF),
        ("refs_count4", len(profile.get("registry_model_profile_refs") or []) == 4),
        *(("ref." + ref[:12], ref in (profile.get("registry_model_profile_refs") or [])) for ref in VISION_REGISTRY_REFS),
    ])

    ml_std_qual = _review_from_checks([
        ("profile_id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID),
        ("module_id", profile.get("module_id") == MODULE_ID),
        ("no_override", profile.get("no_registry_override") is True),
        ("no_select", profile.get("no_model_selection_by_module") is True),
        ("no_invoke", profile.get("no_model_invocation_by_profile") is True),
        ("no_fact", profile.get("no_direct_fact_action_output") is True),
        ("ml_std_ref", plan_sm.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF),
    ])

    binding_qual = _review_from_checks([
        ("binding_id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID),
        ("profile_ref", binding.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID),
        ("constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
        ("provider", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
        ("controlled_runtime", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
        ("gate_later", binding.get("gate_chain_requirement_ref_later") == GATE_CHAIN_SYSTEM_ID),
        ("no_select", binding.get("model_selected_now") is False),
        ("no_invoke", binding.get("model_invoked_now") is False),
        ("no_runtime", binding.get("runtime_enabled_now") is False),
        ("binding_std", plan_sm.get("midplatform_binding_standard_ref") == MIDPLATFORM_BINDING_STANDARD_ID),
    ])

    self_check_qual = _review_from_checks(
        [("plan_exists", bool(self_check.get("plan_id")))]
        + [(c[:16], c in (self_check.get("self_check_coverage") or [])) for c in MODULE_INTERNAL_SELF_CHECK_COVERAGE]
    )

    interaction_qual = _review_from_checks(
        [("plan_exists", bool(interaction.get("plan_id")))]
        + [(c[:16], c in (interaction.get("interaction_check_coverage") or []))
           for c in MIDPLATFORM_INTERACTION_CHECK_COVERAGE]
    )

    candidate_only_qual = _review_from_checks([
        ("candidate_only", plan_sm.get("candidate_only") is True),
        ("model_selected", meta.get("model_selected_now") is False),
        ("model_invoked", meta.get("model_invoked_now") is False),
        ("runtime", meta.get("vision_module_runtime_enabled_now") is False),
        ("camera", meta.get("camera_invoked_now") is False),
    ])

    no_bypass_qual = _review_from_checks([
        ("constitution_ref", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
        ("provider_ref", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
        ("health_ref", binding.get("health_requirement_ref") == "required_later"),
        ("validation_ref", binding.get("validation_requirement_ref") == "required_later"),
        ("whitebox_ref", bool(binding.get("whitebox_trace_requirement_ref"))),
        ("gate_ref", bool(binding.get("gate_chain_requirement_ref_later"))),
        ("cr_ref", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
    ])

    health_supervision_qual = _review_from_checks([
        ("health_later", health.get("health_requirement_ref") == "required_later"),
        ("supervision_later", health.get("supervision_metric_ref") == "required_later"),
        ("health_detail_false", health.get("health_metric_detail_defined_now") is False),
        ("supervision_detail_false", health.get("supervision_metric_detail_defined_now") is False),
        ("metrics_not_finalized", meta.get("health_metrics_finalized_now") is False),
        ("supervision_not_finalized", meta.get("supervision_metrics_finalized_now") is False),
    ])

    all_reviews = [
        registry_qual, ml_std_qual, binding_qual, self_check_qual, interaction_qual,
        candidate_only_qual, no_bypass_qual, health_supervision_qual,
    ]
    qualification_pass = (
        input_ok
        and qual_plan.get("qualification_pass") is True
        and all(r.get("review_pass") for r in all_reviews)
    )

    candidate = {
        "candidate_id": "vision_module_model_profile_governance_binding_candidate_v1",
        "module_id": MODULE_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_pass": qualification_pass,
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(VISION_REGISTRY_REFS),
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        **meta,
    }

    qualification_check = {
        "check_id": "vision_module_qualification_check_v1",
        "qualification_mode": QUALIFICATION_MODE,
        "criteria": list(QUALIFICATION_CHECK_CRITERIA),
        "criteria_count": len(QUALIFICATION_CHECK_CRITERIA),
        "qualification_fields": dict(QUALIFICATION_FIELDS),
        "can_say": list(CLOSURE_CAN_SAY),
        "cannot_say": list(CLOSURE_CANNOT_SAY),
        "qualification_pass": qualification_pass,
        "review_results": {
            "registry": registry_qual.get("review_pass"),
            "module_local_standard": ml_std_qual.get("review_pass"),
            "midplatform_binding": binding_qual.get("review_pass"),
            "self_check": self_check_qual.get("review_pass"),
            "interaction_check": interaction_qual.get("review_pass"),
            "candidate_only": candidate_only_qual.get("review_pass"),
            "no_bypass": no_bypass_qual.get("review_pass"),
            "health_supervision_refs_only": health_supervision_qual.get("review_pass"),
        },
        **meta,
    }

    closure_decision = {
        "decision_id": "vision_module_qualification_closure_decision_v1",
        "dryrun_and_review_pass": qualification_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if qualification_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_module_model_profile_governance_binding_planning": qualification_pass,
        "selected_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "vision_module_model_profile_governance_binding_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "qualification_check_only": True,
        "phase_goal": "Qualification verification only. No health/supervision metric expansion.",
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": qualification_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "module_id": MODULE_ID,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_module_model_profile_governance_binding_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "vision_module_model_profile_governance_binding_candidate": candidate,
        "vision_module_registry_qualification_review": {**registry_qual, "review_id": "vision_module_registry_qualification_review_v1", **meta},
        "vision_module_local_standard_qualification_review": {**ml_std_qual, "review_id": "vision_module_local_standard_qualification_review_v1", **meta},
        "vision_midplatform_binding_qualification_review": {**binding_qual, "review_id": "vision_midplatform_binding_qualification_review_v1", **meta},
        "vision_self_check_qualification_review": {**self_check_qual, "review_id": "vision_self_check_qualification_review_v1", **meta},
        "vision_interaction_check_qualification_review": {**interaction_qual, "review_id": "vision_interaction_check_qualification_review_v1", **meta},
        "vision_candidate_only_qualification_review": {**candidate_only_qual, "review_id": "vision_candidate_only_qualification_review_v1", **meta},
        "vision_no_bypass_qualification_review": {**no_bypass_qual, "review_id": "vision_no_bypass_qualification_review_v1", **meta},
        "vision_health_supervision_refs_qualification_review": {**health_supervision_qual, "review_id": "vision_health_supervision_refs_qualification_review_v1", **meta},
        "vision_module_qualification_check": qualification_check,
        "vision_module_qualification_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
