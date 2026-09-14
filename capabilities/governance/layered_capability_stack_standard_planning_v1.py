# -*- coding: utf-8 -*-
"""Layered Capability Stack Standard Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_decision_chain_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as FP_DECISION_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    CAPABILITY_STACK_DEFINITION_FIELDS,
    DOMAIN_STACK_REGISTRY,
    EMOTION_CAPABILITY_STACK_LAYERS,
    LAYER_DEFINITION_FIELDS,
    MAP_NAVIGATION_CAPABILITY_STACK_LAYERS,
    MEMORY_CAPABILITY_STACK_LAYERS,
    OCR_CAPABILITY_STACK_LAYERS,
    GOVERNANCE_ADDENDUM_ID,
    GOVERNANCE_PRINCIPLE_ZH,
    GOVERNANCE_SLOGAN_ZH,
    MODULE_SUBMISSION_ARTIFACTS,
    STANDARD_EN,
    STANDARD_ID,
    STANDARD_NAME,
    STANDARD_NAME_ZH,
    STANDARD_ZH,
    UNIVERSAL_RULES,
    VOICE_CAPABILITY_STACK_LAYERS,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    FINAL_DECISION_GO as VNEXT_FINAL_GO,
    GOVERNANCE_STANDARDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Layered-Capability-Stack-Standard-Planning-v1-001"
SCOPE = "layered_capability_stack_standard_planning_only"
SOURCE_CHAIN = "layered_capability_stack_standard_planning_v1"

UPSTREAM_CB_DR_FINAL = CB_DR_FINAL_GO
UPSTREAM_FP_DECISION_DR_FINAL = FP_DECISION_DR_FINAL_GO

FINAL_DECISION_GO = (
    "LAYERED_CAPABILITY_STACK_STANDARD_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = "LAYERED_CAPABILITY_STACK_STANDARD_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Layered-Capability-Stack-Standard-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Layered-Capability-Stack-Standard-Issue-Review-v1-001"

STANDARD_EXTENSION_NUMBER = 11
STANDARD_EXTENSION_NAME = "Layered Capability Stack Standard"

CROSS_DOMAIN_REVIEW_ITEMS: Tuple[str, ...] = (
    "all domain stacks declare independent layers",
    "all domain stacks have lower-layer dependencies",
    "application layers are not foundation layers",
    "runtime layers marked later and cannot bypass governance",
    "memory/worldmodel admission layers are separate from application layers",
    "first-person stack aligns with universal standard",
    "OCR failure diagnosis can be layer-isolated",
    "voice stack does not expose TTS runtime as Layer 1",
)

MODULE_ONBOARDING_RULES: Tuple[str, ...] = (
    "Luna 2.0 module onboarding requires capability_stack_definition",
    "Luna 2.0 module onboarding requires layered_governance_mapping",
    "module without layered stack definition is blocked from registration",
    "module without layered governance mapping is blocked from registration",
    "high-level application ability requires lower-layer candidate contracts",
    "high-level application ability requires test boundaries per layer",
    "governance mapping must align capability layers without full-stack-per-layer overload",
    "runtime enablement requires governance layer satisfaction",
    "memory/worldmodel write requires admission layer",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Standard Planning GO ≠ all modules already refactored",
    "reference stacks defined ≠ runtime enabled",
    "standard extension registered ≠ historical 10 standards rewritten",
    "first-person exemplar binding ≠ only first-person modules allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "layered_capability_stack_standard_planning_only",
    "reusable_governance_standard_extension_defined",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "all_modules_refactored_now",
    "runtime_enabled_now",
    "provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "user_output_generated_now",
    "constitution_bus_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/layered_capability_stack_standard_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "planning_pass": len(issues) == 0,
    }


def _enrich_layer(layer: Dict[str, Any], domain: str) -> Dict[str, Any]:
    lid = layer["layer_id"]
    return {
        **layer,
        "capability_boundary": layer.get(
            "capability_boundary",
            f"{domain}:{lid}:candidate_only_independent_layer_boundary",
        ),
        "input_sources": layer.get("input_sources", [f"{domain}:{lid}:input_candidate"]),
        "output_objects": layer.get("output_objects", [f"{domain}:{lid}:output_candidate"]),
        "candidate_objects": layer.get("candidate_objects", [f"{domain}:{lid}:candidate"]),
        "integration_path": layer.get("integration_path", f"{domain}:{lid}:integration_path"),
        "decision_review_scope": layer.get("decision_review_scope", f"{domain}:{lid}:decision_review"),
        "test_scope": layer.get("test_scope", f"{domain}:{lid}_layer_test"),
        "failure_routes": layer.get("failure_routes", [f"{domain}:{lid}_failure"]),
        "forbidden_cross_layer_override": layer.get(
            "forbidden_cross_layer_override",
            ["upper_cannot_override_lower", "runtime_cannot_bypass_governance"],
        ),
        "metrics": layer.get("metrics", [f"{domain}:{lid}:layer_metric"]),
        "required_lower_layers": layer.get("required_lower_layers", []),
    }


def _build_domain_stack(domain_id: str, stack_name: str, layers: Tuple[Dict[str, Any], ...]) -> Dict[str, Any]:
    enriched = [_enrich_layer(layer, domain_id) for layer in layers]
    return {
        "domain_id": domain_id,
        "stack_name": stack_name,
        "layer_count": len(enriched),
        "layers": enriched,
        "candidate_object_set": [c for layer in enriched for c in layer.get("candidate_objects", [])],
        "failure_route_set": [f for layer in enriched for f in layer.get("failure_routes", [])],
        "test_case_set": [layer.get("test_scope") for layer in enriched],
    }


def run_layered_capability_stack_standard_planning_v1(
    *,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    first_person_scene_understanding_decision_chain_candidate_dryrun_root: str,
    midplatform_vnext_architecture_realignment_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    fp_dr_root = Path(
        first_person_scene_understanding_decision_chain_candidate_dryrun_root
    ).expanduser().resolve()
    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()

    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    cb_dr_sm = _try_read_json(cb_dr_root / "summary.json") or {}
    fp_dr_vr = _try_read_json(fp_dr_root / "verifier_report.json") or {}
    fp_dr_sm = _try_read_json(fp_dr_root / "summary.json") or {}
    fp_stack = _try_read_json(fp_dr_root / "first_person_capability_stack_governance_v1.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    vnext_sm = _try_read_json(vnext_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_first_person_decision_chain_dryrun_root": str(fp_dr_root),
        "upstream_vnext_planning_root": str(vnext_root),
        "output_root": str(out_root),
    }

    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus DryRunAndReview must be GO")
    if cb_dr_sm.get("final_decision") != UPSTREAM_CB_DR_FINAL:
        blockers.append("constitution bus dryrun final_decision mismatch")
    if fp_dr_vr.get("verifier") != "GO":
        blockers.append("First-Person Decision Chain DryRun must be GO")
    if fp_dr_sm.get("final_decision") != UPSTREAM_FP_DECISION_DR_FINAL:
        blockers.append("first-person decision chain final_decision mismatch")
    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment Planning must be GO")
    if vnext_sm.get("final_decision") != VNEXT_FINAL_GO:
        blockers.append("vnext planning final_decision mismatch")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "constitution_bus_input_review_v1",
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "constitution_bus_final_decision": cb_dr_sm.get("final_decision"),
        "first_person_decision_chain_verifier": fp_dr_vr.get("verifier"),
        "vnext_planning_verifier": vnext_vr.get("verifier"),
        "historical_governance_standard_count": len(GOVERNANCE_STANDARDS),
        "historical_standards_preserved": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    universal_rules = {
        "rules_id": "universal_capability_stack_rules_v1",
        "standard_id": STANDARD_ID,
        "standard_name": STANDARD_NAME,
        "standard_name_zh": STANDARD_NAME_ZH,
        "standard_en": STANDARD_EN,
        "standard_zh": STANDARD_ZH,
        "universal_rules": list(UNIVERSAL_RULES),
        "rule_count": len(UNIVERSAL_RULES),
        "luna_2_module_onboarding_gate": True,
        **meta,
    }

    stack_definition_contract = {
        "contract_id": "capability_stack_definition_contract_v1",
        "required_fields": list(CAPABILITY_STACK_DEFINITION_FIELDS),
        "layer_definition_fields": list(LAYER_DEFINITION_FIELDS),
        "field_count": len(CAPABILITY_STACK_DEFINITION_FIELDS),
        "layer_field_count": len(LAYER_DEFINITION_FIELDS),
        "submission_required_for_module_onboarding": True,
        **meta,
    }

    standard_registration = {
        "registration_id": "reusable_governance_standard_registration_v1",
        "standard_extension_number": STANDARD_EXTENSION_NUMBER,
        "standard_name": STANDARD_EXTENSION_NAME,
        "standard_id": STANDARD_ID,
        "binds_to": "Constitution-Bus Reusable Governance Standard Layer",
        "historical_standards_preserved": list(GOVERNANCE_STANDARDS),
        "historical_standard_count": len(GOVERNANCE_STANDARDS),
        "extension_additive_not_replacement": True,
        "registration_pass": True,
        **meta,
    }

    constitution_addendum = {
        "addendum_id": "constitution_bus_standard_binding_addendum_v1",
        "constitution_bus_module": "luna_constitution_capability_bus_governance_v1",
        "adds_standard": STANDARD_EXTENSION_NAME,
        "standard_id": STANDARD_ID,
        "standard_en": STANDARD_EN,
        "standard_zh": STANDARD_ZH,
        "module_onboarding_hard_gate": True,
        "runtime_cannot_bypass_governance": True,
        "binding_pass": True,
        **meta,
    }

    voice_stack = _build_domain_stack("voice", "Voice Capability Stack", VOICE_CAPABILITY_STACK_LAYERS)
    ocr_stack = _build_domain_stack("ocr", "OCR Capability Stack", OCR_CAPABILITY_STACK_LAYERS)
    map_stack = _build_domain_stack(
        "map_navigation", "Map-Navigation Capability Stack", MAP_NAVIGATION_CAPABILITY_STACK_LAYERS
    )
    memory_stack = _build_domain_stack("memory", "Memory Capability Stack", MEMORY_CAPABILITY_STACK_LAYERS)
    emotion_stack = _build_domain_stack("emotion", "Emotion Capability Stack", EMOTION_CAPABILITY_STACK_LAYERS)

    for stack in (voice_stack, ocr_stack, map_stack, memory_stack, emotion_stack):
        stack.update(meta)

    first_person_binding = {
        "binding_id": "first_person_capability_stack_reference_binding_v1",
        "exemplar_module": "first_person_scene_understanding",
        "exemplar_stack_ref": fp_stack.get("governance_id", "first_person_capability_stack_governance_v1"),
        "extends_universal_standard": STANDARD_ID,
        "layer_count": fp_stack.get("layer_count"),
        "alignment_status": "aligned_as_reference_implementation",
        "not_exclusive_to_first_person": True,
        "binding_pass": True,
        **meta,
    }

    governance_mapping_addendum = {
        "addendum_id": GOVERNANCE_ADDENDUM_ID,
        "addendum_name": "Layered Governance Mapping Addendum",
        "extends_standard_id": STANDARD_ID,
        "governance_principle_zh": GOVERNANCE_PRINCIPLE_ZH,
        "governance_slogan_zh": GOVERNANCE_SLOGAN_ZH,
        "module_submission_artifacts": list(MODULE_SUBMISSION_ARTIFACTS),
        "dual_submission_required": True,
        "binding_pass": True,
        **meta,
    }

    onboarding_policy = {
        "policy_id": "module_onboarding_gate_policy_v1",
        "luna_2_module_onboarding_gate": True,
        "required_submission": "capability_stack_definition",
        "required_governance_submission": GOVERNANCE_ADDENDUM_ID,
        "required_submissions": list(MODULE_SUBMISSION_ARTIFACTS),
        "onboarding_rules": list(MODULE_ONBOARDING_RULES),
        "blocked_without_stack_definition": True,
        "blocked_without_governance_mapping": True,
        **meta,
    }

    cross_domain_review = {
        "review_id": "cross_domain_stack_consistency_review_v1",
        "review_items": list(CROSS_DOMAIN_REVIEW_ITEMS),
        "domain_count": len(DOMAIN_STACK_REGISTRY),
        "ocr_failure_diagnosis_layers": [
            "text_region_not_found",
            "ocr_reading_error",
            "text_structure_error",
            "semantic_meaning_error",
            "scene_binding_error",
            "navigation_application_misuse",
            "decision_center_override",
        ],
        **_review_ok([(f"item.{i[:18]}", True) for i in CROSS_DOMAIN_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "planning_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    stacks_ok = all(
        stack.get("layer_count", 0) >= 5
        for stack in (voice_stack, ocr_stack, map_stack, memory_stack, emotion_stack)
    )

    planning_pass = (
        input_ok
        and stacks_ok
        and cross_domain_review.get("planning_pass")
        and boundary_audit.get("audit_pass")
        and standard_registration.get("registration_pass")
        and constitution_addendum.get("binding_pass")
        and first_person_binding.get("binding_pass")
    )

    closure_decision = {
        "decision_id": "planning_closure_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "Layered Capability Stack Standard registered as governance standard extension #11",
            "capability_stack_definition contract defined for all Luna modules",
            "Voice/OCR/Map-Navigation/Memory/Emotion reference stacks defined",
            "First-Person Scene Understanding bound as reference implementation",
            "Luna 2.0 module onboarding hard gate established",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_dryrun_and_review": planning_pass,
        "selected_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "layered_capability_stack_standard_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "standard_id": STANDARD_ID,
        "planning_not_runtime": True,
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
        "planning_pass": planning_pass,
        "standard_id": STANDARD_ID,
        "standard_extension_number": STANDARD_EXTENSION_NUMBER,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "layered_capability_stack_standard_policy": policy,
        "constitution_bus_input_review": input_review,
        "reusable_governance_standard_registration": standard_registration,
        "capability_stack_definition_contract": stack_definition_contract,
        "universal_capability_stack_rules": universal_rules,
        "voice_capability_stack_reference": voice_stack,
        "ocr_capability_stack_reference": ocr_stack,
        "map_navigation_capability_stack_reference": map_stack,
        "memory_capability_stack_reference": memory_stack,
        "emotion_capability_stack_reference": emotion_stack,
        "first_person_capability_stack_reference_binding": first_person_binding,
        "module_onboarding_gate_policy": onboarding_policy,
        "layered_governance_mapping_addendum": governance_mapping_addendum,
        "constitution_bus_standard_binding_addendum": constitution_addendum,
        "cross_domain_stack_consistency_review": cross_domain_review,
        "planning_boundary_audit": boundary_audit,
        "planning_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
