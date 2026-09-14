# -*- coding: utf-8 -*-
"""OCR Module Model Profile + Governance Binding Planning v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as STACK_STD_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as BINDING_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    DECISION_CENTER_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_MODE,
)

PHASE_ID = "Phase-OCR-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "ocr_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "ocr_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "OCR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

MODULE_ID = "ocr_text_reading_module"
MODULE_LOCAL_PROFILE_ID = "ocr_text_reading_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "ocr_text_reading_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "ocr_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "ocr_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "ocr_text_reading_capability_bus_contract_v1"

OCR_REGISTRY_REFS: Tuple[str, ...] = (
    "rapidocr_candidate",
    "paddleocr_candidate",
    "ocr_placeholder_candidate",
)
OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID = "other_ocr_provider_placeholder"

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Model Profile Registry",
    "Module-Local Model Profile Standard",
    "Midplatform Model Governance Binding Standard",
    "Dual Validation Mechanism",
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Luna Gate Chain / Enforcement Gate System",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact",
    "direct_action",
    "direct_navigation_action",
    "direct_user_output",
    "direct_memory_write",
    "direct_worldmodel_write",
    "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "OCR Module Planning GO ≠ RapidOCR/PaddleOCR selected",
    "OCR candidate ref ≠ OCR runtime",
    "OCR output contract planned ≠ OCR fact generation",
    "OCR module binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next DryRunAndReview ≠ model benchmark/runtime",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
)

QUALIFICATION_FIELDS: Dict[str, bool] = {
    "qualification_check_only": True,
    "full_integration_certification_now": False,
    "constitution_binding_feasible": True,
    "oversight_binding_feasible": True,
    "constitution_effectiveness_quantified_now": False,
    "health_metrics_finalized_now": False,
    "supervision_metrics_finalized_now": False,
    "module_constitution_fully_integrated_now": False,
    "module_oversight_fully_integrated_now": False,
    "health_metric_detail_defined_now": False,
    "supervision_metric_detail_defined_now": False,
}

CLOSURE_CAN_SAY: Tuple[str, ...] = (
    "OCR module can reference Registry",
    "OCR module can bind Module-local Profile Standard",
    "OCR module can bind Midplatform Governance Standard",
    "OCR module can preserve candidate-only OCR outputs",
    "OCR module can attach Health/Oversight refs later",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "OCR runtime is ready",
    "RapidOCR/PaddleOCR selected or invoked",
    "OCR quality is benchmarked",
    "OCR is fully integrated with Constitution",
    "OCR is fully integrated with Health/Oversight",
    "health/supervision metrics finalized",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "ocr_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_module_runtime_enabled_now",
    "real_ocr_executed_now",
    "ocr_provider_invoked_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "ocr_fact_generated_now",
    "ocr_action_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "constitution_effectiveness_quantified_now",
    "health_metrics_finalized_now",
    "supervision_metrics_finalized_now",
    "module_constitution_fully_integrated_now",
    "module_oversight_fully_integrated_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_module_model_profile_governance_binding_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "runtime_enabled_now": False,
        "provider_invoked_now": False,
        "real_ocr_executed_now": False,
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


def _ocr_registry_ids_from_seeds(ocr_seeds: Dict[str, Any]) -> List[str]:
    return [c.get("model_profile_id") for c in (ocr_seeds.get("candidates") or []) if c.get("model_profile_id")]


def run_ocr_module_model_profile_governance_binding_planning_v1(
    *,
    vision_module_model_profile_governance_binding_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    vision_dr_root = Path(
        vision_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    binding_dr_root = Path(
        midplatform_model_governance_binding_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    registry_plan_root = registry_dr_root.parent / "model_profile_registry_planning"
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    vision_dr_vr = _try_read_json(vision_dr_root / "verifier_report.json") or {}
    vision_dr_sm = _try_read_json(vision_dr_root / "summary.json") or {}
    binding_dr_vr = _try_read_json(binding_dr_root / "verifier_report.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    ocr_seeds = _try_read_json(registry_plan_root / "ocr_model_profile_seed_candidates_v1.json") or {}
    ocr_seeds_review = _try_read_json(registry_dr_root / "ocr_model_profile_seed_candidates_review_v1.json") or {}
    ocr_registry_ids = _ocr_registry_ids_from_seeds(ocr_seeds)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if vision_dr_vr.get("verifier") != "GO":
        blockers.append("Vision Module DryRunAndReview must be GO")
    if vision_dr_sm.get("final_decision") != VISION_DR_FINAL_GO:
        blockers.append("Vision DryRun final_decision mismatch")
    if binding_dr_vr.get("verifier") != "GO":
        blockers.append("Midplatform Binding DryRunAndReview must be GO")
    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local DryRunAndReview must be GO")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRun final_decision mismatch")
    if stack_vr.get("verifier") != "GO":
        blockers.append("Layered Capability Stack Standard must be GO")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    if "rapidocr_candidate" not in SEED_CANDIDATE_IDS:
        blockers.append("rapidocr_candidate must exist in registry seed list")
    if "paddleocr_candidate" not in SEED_CANDIDATE_IDS:
        blockers.append("paddleocr_candidate must exist in registry seed list")
    if OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID not in ocr_registry_ids:
        if not ocr_seeds_review.get("review_pass"):
            blockers.append("ocr placeholder must be explicitly registered in registry OCR seeds")
        else:
            placeholder_ok = any(
                c.get("check_id") == "placeholder" and c.get("pass")
                for c in (ocr_seeds_review.get("checks") or [])
            )
            if not placeholder_ok:
                blockers.append("ocr placeholder review must pass")

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_vision_module_input_review_v1",
        "vision_dryrun_verifier": vision_dr_vr.get("verifier"),
        "vision_dryrun_final_decision": vision_dr_sm.get("final_decision"),
        "binding_dryrun_verifier": binding_dr_vr.get("verifier"),
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "ocr_module_qualification_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "ocr_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "OCR / Text Recognition / Reading",
        "primary_goal": "text_region_and_ocr_candidate_generation",
        "related_goal": "current_scene_understanding_support",
        "later_goal": "reading_application_layer",
        "registry_ref": REGISTRY_REF,
        "runtime_enabled_now": False,
        "provider_invoked_now": False,
        "real_ocr_executed_now": False,
        "candidate_only": True,
        "confirmations": [
            "OCR module does not directly output fact",
            "OCR module does not directly trigger navigation action",
            "OCR module does not generate user_output",
            "OCR module does not write Memory/WorldModel",
            "OCR outputs enter Information Integration",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_text_region_detection": {
                "outputs": ["text_region_candidate", "readable_region_candidate", "text_presence_candidate"],
                "status": "primary_now",
            },
            "layer_2_ocr_reading_candidate": {
                "outputs": [
                    "ocr_result_candidate", "recognized_text_candidate",
                    "language_hint_candidate", "confidence_candidate",
                ],
                "status": "primary_now",
            },
            "layer_3_text_structure_signage_context_later": {
                "outputs": ["signage_context_candidate", "text_structure_candidate", "reading_order_candidate"],
                "status": "later",
            },
            "layer_4_reading_application_later": {
                "outputs": [
                    "reading_candidate", "document_understanding_candidate",
                    "instruction_text_context_candidate",
                ],
                "status": "later",
            },
        },
        "forbidden": ["no direct fact", "no navigation action", "no user_output", "no Memory/WorldModel write"],
        **meta,
    }

    layered_governance = {
        "mapping_id": LAYERED_GOV_MAPPING_ID,
        "module_id": MODULE_ID,
        "universal_mapping_ref": ADDENDUM_ID,
        "layers": {
            "L1": {"requirements": ["source_chain", "region_ref", "confidence", "ttl", "candidate_only", "not_fact"]},
            "L2": {"requirements": ["OCR confidence", "text uncertainty", "validation_required", "evidence chain"]},
            "L3": {
                "requirements": [
                    "signage / meaning as candidate", "freshness / ambiguity / conflict",
                    "Information Integration handoff",
                ],
            },
            "L4": {
                "requirements": [
                    "reading application later", "Memory/WorldModel admission if storing",
                    "privacy/sensitive text checks later",
                ],
            },
        },
        "confirmations": [
            "governance principles consistent",
            "execution intensity layered",
            "no all-rules-to-all-layers overload",
            "no weakened constitution by layer",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "OCR / Text Recognition / Reading",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(OCR_REGISTRY_REFS),
        "registry_placeholder_alias": {
            "ocr_placeholder_candidate": OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID,
        },
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": {
            "rapidocr_candidate": "text_region_detection_candidate",
            "paddleocr_candidate": "ocr_reading_candidate",
            "ocr_placeholder_candidate": "text_structure_candidate_later",
        },
        "model_source_strategy": "A_direct_open_source_or_external_provider",
        "candidate_output_type": "ocr_candidate/evidence/context",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "ocr_whitebox_trace_requirement_v1",
        "quality_acceptance_ref": "ocr_quality_acceptance_plan_v1",
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_fact_action_output": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "ocr_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(OCR_REGISTRY_REFS),
        "registry_placeholder_registry_id": OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID,
        "seed_candidates_in_registry": [
            {"ref": "rapidocr_candidate", "in_seed_list": "rapidocr_candidate" in SEED_CANDIDATE_IDS,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
            {"ref": "paddleocr_candidate", "in_seed_list": "paddleocr_candidate" in SEED_CANDIDATE_IDS,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
            {"ref": "ocr_placeholder_candidate", "registry_id": OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID,
             "explicitly_registered": OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID in ocr_registry_ids,
             "candidate_only": True, "selected_now": False, "invoked_now": False},
        ],
        "confirmations": [
            "rapidocr_candidate exists in luna_model_profile_registry_v1",
            "paddleocr_candidate exists in luna_model_profile_registry_v1",
            "ocr_placeholder_candidate maps to explicitly registered placeholder ref",
            "all refs are candidate only",
            "none selected_now",
            "none invoked_now",
            "license/version/profile completeness later",
            "OCR provider readiness later required",
        ],
        "review_pass": (
            "rapidocr_candidate" in SEED_CANDIDATE_IDS
            and "paddleocr_candidate" in SEED_CANDIDATE_IDS
            and (
                OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID in ocr_registry_ids
                or ocr_seeds_review.get("review_pass") is True
            )
        ),
        **meta,
    }

    role_assignment = {
        "plan_id": "ocr_model_role_assignment_plan_v1",
        "assignments": [
            {"registry_ref": "rapidocr_candidate", "role": "OCR reading candidate", "status": "primary_candidate_now"},
            {"registry_ref": "paddleocr_candidate", "role": "OCR reading candidate / text detection candidate",
             "status": "primary_candidate_now"},
            {"registry_ref": "ocr_placeholder_candidate", "role": "future provider role", "status": "placeholder_later"},
        ],
        "confirmations": [
            "RapidOCR maps to OCR reading candidate role",
            "PaddleOCR maps to OCR reading candidate / text detection candidate role",
            "OCR placeholder maps to future provider role",
            "no single OCR model owns full reading capability",
            "reading application remains later",
            "OCR result does not become fact by itself",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "ocr_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "visual_region_candidate", "text_region_candidate", "readable_region_candidate",
            "roi_candidate_later", "frame_candidate_later", "task_intent_candidate",
            "required_observation_candidate", "provider_context_candidate_later",
        ],
        "confirmations": [
            "real frame input not allowed now",
            "OCR provider input not invoked now",
            "frame_candidate_later requires Controlled Runtime later",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "ocr_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "text_region_candidate", "ocr_result_candidate", "recognized_text_candidate",
            "language_hint_candidate", "signage_context_candidate", "text_structure_candidate_later",
            "reading_candidate_later", "ocr_evidence_candidate",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        "handoff_target": INFORMATION_INTEGRATION_REF,
        **meta,
    }

    quality_plan = {
        "plan_id": "ocr_quality_acceptance_plan_v1",
        "requirements": [
            "ocr_accuracy_target_later", "text_detection_precision_target_later",
            "false_text_positive_control_requirement", "missed_text_false_negative_control_requirement",
            "latency_budget_later", "resource_budget_later", "confidence_calibration_required",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "ocr_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "ocr_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "evidence_refs_required": True,
        "failure_route_required": True,
        "issue_trace_required": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "scope_note": "ref slots only; metric detail deferred",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "ocr_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "real OCR execution requires Controlled Runtime later",
            "OCR runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "ocr_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(OCR_REGISTRY_REFS),
        "replacement_conditions": [
            "quality_regression", "provider_unavailable", "license_risk", "latency_budget_failure",
            "hardware_incompatibility", "high_false_positive_text_risk", "high_false_negative_text_risk",
        ],
        "hold_instead_of_fallback_when": "safety/privacy/licensing risk exists",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "ocr_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "OCR 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 OCR runtime",
            "自检不选择 RapidOCR/PaddleOCR",
            "自检不调用 OCR provider",
            "自检不写 Memory / WorldModel",
            "自检不生成 OCR fact / action / user output",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "ocr_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "OCR 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 OCR runtime 授权",
            "中台检验不等于模型选择",
            "中台检验不等于 OCR provider invocation",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(OCR_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "ocr_whitebox_trace_requirement_v1",
        "information_integration_consumption_policy_ref": "ocr_information_integration_handoff_plan_v1",
        "decision_center_consumption_policy_ref": "ocr_decision_center_handoff_plan_v1",
        "gate_chain_requirement_ref_later": GATE_CHAIN_SYSTEM_ID,
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "memory_admission_requirement_ref_later": "memory_admission_gate_later",
        "worldmodel_admission_requirement_ref_later": "worldmodel_admission_gate_later",
        "source_chain_requirement_ref": "ocr_source_chain_requirement_v1",
        "evidence_requirement_ref": "ocr_evidence_requirement_v1",
        "issue_trace_requirement_ref": "ocr_issue_trace_requirement_v1",
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    ii_handoff = {
        "plan_id": "ocr_information_integration_handoff_plan_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "consumes": [
            "text_region_candidate", "ocr_result_candidate", "recognized_text_candidate",
            "signage_context_candidate", "ocr_evidence_candidate",
        ],
        "confirmations": [
            "OCR outputs go to Information Integration as candidate/context/evidence",
            "OCR module cannot bypass Information Integration to Decision Center unless explicit policy later",
            "no integrated_context generated now",
        ],
        **meta,
    }

    decision_handoff = {
        "plan_id": "ocr_decision_center_handoff_plan_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "handoff_via": ["integrated_context", "decision_request"],
        "confirmations": [
            "decision-relevant OCR outputs reach Decision Center only through "
            "integrated_context / decision_request",
            "OCR module cannot emit decision",
            "OCR text cannot directly trigger navigation action",
            "no decision generated now",
        ],
        **meta,
    }

    gate_chain_boundary = {
        "plan_id": "ocr_gate_chain_boundary_plan_v1",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "output_capable_now": False,
        "confirmations": [
            "OCR module not user-output-capable now",
            "if OCR reading result becomes user-facing later, Output/Gate chain required",
            "privacy gate later for sensitive text",
            "no user_output now",
        ],
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "ocr_memory_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "OCR module cannot write Memory",
            "OCR module cannot write WorldModel",
            "OCR evidence may be admission candidate later",
            "text fact admission later required",
            "reading/storage later requires Memory/WorldModel Admission",
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "ocr_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    qualification_check = {
        "check_id": "ocr_module_qualification_check_v1",
        "qualification_mode": QUALIFICATION_MODE,
        "criteria": list(QUALIFICATION_CHECK_CRITERIA),
        "criteria_count": len(QUALIFICATION_CHECK_CRITERIA),
        "qualification_fields": dict(QUALIFICATION_FIELDS),
        "can_say": list(CLOSURE_CAN_SAY),
        "cannot_say": list(CLOSURE_CANNOT_SAY),
        "qualification_pass": input_ok and registry_refs_review.get("review_pass"),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "ocr_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify OCR module sample is compliant",
            "verify registry / module-local standard / midplatform binding refs",
            "verify RapidOCR / PaddleOCR / placeholder role assignment",
            "verify dual validation plans",
            "no health/supervision metric detail expansion",
            "no model select/download/invoke/benchmark",
            "no OCR runtime enable",
        ],
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "ocr_module_model_profile_governance_binding_planning_decision_v1",
        "planning_pass": planning_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    policy = {
        "policy_id": "ocr_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "ocr_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "OCR module model profile + governance binding qualification planning confirmation only. "
            "No health/supervision metric expansion. No RapidOCR/PaddleOCR selection or OCR runtime."
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "module_id": MODULE_ID,
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_ref_count": len(OCR_REGISTRY_REFS),
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "ocr_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_vision_module_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "ocr_module_definition": module_definition,
        "ocr_capability_stack_definition": capability_stack,
        "ocr_layered_governance_mapping": layered_governance,
        "ocr_module_local_model_profile": module_local_profile,
        "ocr_model_profile_registry_refs_review": registry_refs_review,
        "ocr_model_role_assignment_plan": role_assignment,
        "ocr_input_contract": input_contract,
        "ocr_output_contract": output_contract,
        "ocr_quality_acceptance_plan": quality_plan,
        "ocr_health_validation_whitebox_plan": health_validation_whitebox,
        "ocr_provider_runtime_boundary_plan": provider_runtime_boundary,
        "ocr_fallback_replacement_plan": fallback_plan,
        "ocr_module_internal_self_check_plan": self_check_plan,
        "ocr_midplatform_interaction_check_plan": interaction_check_plan,
        "ocr_midplatform_governance_binding": midplatform_binding,
        "ocr_information_integration_handoff_plan": ii_handoff,
        "ocr_decision_center_handoff_plan": decision_handoff,
        "ocr_gate_chain_boundary_plan": gate_chain_boundary,
        "ocr_memory_worldmodel_admission_boundary_plan": memory_wm_boundary,
        "ocr_module_qualification_check": qualification_check,
        "ocr_non_runtime_boundary_matrix": boundary_matrix,
        "ocr_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "ocr_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
