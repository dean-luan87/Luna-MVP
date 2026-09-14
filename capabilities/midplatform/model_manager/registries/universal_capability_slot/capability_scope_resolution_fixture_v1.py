"""Controlled scope/resolution/invocation reference chains."""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable, List, Tuple

from .universal_capability_slot_governance_v1 import (
    assess_official_module_admission,
    assess_slot_compatibility,
    build_binding_candidate,
    build_capability_self_view,
    govern_binding,
)
from .universal_capability_slot_resolution_v1 import (
    build_scoped_invocation_candidate,
    resolve_scoped_capability_requirement,
)
from .universal_capability_slot_types_v1 import (
    CapabilityModuleV1,
    CapabilityRequirementV1,
    OfficialCapabilityModuleV1,
    UniversalCapabilitySlotV1,
)


def _module(
    module_id: str,
    purpose: str,
    problem_classes: Tuple[str, ...],
    requirement_types: Tuple[str, ...],
    operations: Tuple[str, ...],
    *,
    input_refs: Tuple[str, ...] = ("image_evidence",),
    output_refs: Tuple[str, ...] = ("evidence_candidate",),
    lifecycle_state: str = "ACTIVE",
) -> OfficialCapabilityModuleV1:
    return OfficialCapabilityModuleV1(
        module_id=module_id,
        capability_purpose=purpose,
        problem_classes=problem_classes,
        origin="OFFICIAL",
        requirement_class="OPTIONAL",
        module_version="v1",
        lifecycle_state=lifecycle_state,
        implementation_refs=(f"implementation:{module_id}",),
        input_contract_refs=input_refs,
        output_contract_refs=output_refs,
        provider_contract_refs=(f"provider:{module_id}",),
        model_asset_refs=(f"model:{module_id}",),
        resource_refs=(f"resource:{module_id}",),
        permission_refs=("permission:capability-governance",),
        compatibility_refs=("compatibility:universal-slot-v1",),
        integrity_refs=(f"integrity:{module_id}",),
        provenance_refs=(f"provenance:{module_id}",),
        degradation_policy_refs=(f"degradation:{module_id}",),
        rollback_refs=(f"rollback:{module_id}",),
        self_visibility=f"self:{module_id}",
        capability_semantic_annotation_ref=f"csa:{module_id}:v1",
        accepted_requirement_types=requirement_types,
        accepted_input_contract_refs=input_refs,
        produced_output_contract_refs=output_refs,
        supported_operation_refs=operations,
        explicit_boundary_refs=(f"boundary:{module_id}:evidence-only",),
        known_non_capability_refs=("world_truth", "action_authority"),
        authority_boundary_refs=("EVIDENCE_ONLY",),
        execution_boundary_refs=("Observation Gateway / FPO",),
    )


def build_scope_modules() -> Tuple[CapabilityModuleV1, ...]:
    return (
        _module("text_recognition", "text_recognition", ("text_content", "sign_text"), ("TEXT_READ",), ("READ_TEXT",), output_refs=("text_candidate",)),
        _module("precise_ocr", "precise_ocr", ("precise_ocr", "text_content"), ("TEXT_READ", "PRECISE_TEXT_READ"), ("READ_TEXT", "READ_PRECISE_TEXT"), input_refs=("image_evidence", "visual_region_candidate"), output_refs=("text_candidate",)),
        _module("object_detection", "object_detection", ("object_presence", "vehicle_presence", "object_region"), ("OBJECT_DETECTION",), ("DETECT_OBJECT", "DETECT_REGION"), output_refs=("object_candidate", "region_candidate")),
        _module("spatial_mapping", "spatial_mapping", ("spatial_structure", "spatial_anchor"), ("SPATIAL_MAP",), ("PROVIDE_SPATIAL_STRUCTURE",), input_refs=("image_evidence", "pose_candidate"), output_refs=("spatial_map_candidate", "anchor_candidate")),
    )


def _slot(slot_id: str, state: str = "EMPTY") -> UniversalCapabilitySlotV1:
    return UniversalCapabilitySlotV1(
        slot_id=slot_id,
        slot_version="v1",
        lifecycle_state=state,
        current_module_binding=None,
        compatibility_refs=("compatibility:universal-slot-v1",),
        resource_refs=("resource:controlled",),
        permission_refs=("permission:capability-governance",),
        health_refs=(f"health:{slot_id}",),
        provenance_refs=(f"provenance:{slot_id}",),
        history_refs=(),
        recovery_refs=(),
        trace_refs=(f"trace:{slot_id}",),
        self_visibility="EMPTY",
    )


def _bind(module: CapabilityModuleV1, slot: UniversalCapabilitySlotV1) -> UniversalCapabilitySlotV1:
    admission = assess_official_module_admission(module)
    assessment = assess_slot_compatibility(slot, module, admission)
    candidate = build_binding_candidate(slot, module, admission, assessment)
    return govern_binding(slot, module, candidate).projected_slot


def _requirement(
    requirement_id: str,
    module_id: str,
    problem_class: str,
    operation: str,
    input_ref: str,
    output_ref: str,
    *,
    requirement_type: str,
    authority: str = "EVIDENCE_ONLY",
    technical_hints: Tuple[str, ...] = (),
) -> CapabilityRequirementV1:
    return CapabilityRequirementV1(
        requirement_id=requirement_id,
        requested_module_id=module_id,
        purpose=problem_class,
        task_context="controlled-scope-reference-chain",
        required_semantic_depth="MINIMAL",
        permission_refs=("permission:capability-governance",),
        resource_refs=("resource:controlled",),
        execution_boundary_ref="Observation Gateway / FPO",
        requester_ref="brain:need-candidate",
        requirement_type=requirement_type,
        problem_class=problem_class,
        requested_operation=operation,
        input_contract_ref=input_ref,
        expected_output_contract_ref=output_ref,
        required_authority=authority,
        task_context_refs=("task:controlled", "context:controlled"),
        trace_ref=f"trace:{requirement_id}",
        technical_hints=technical_hints,
    )


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def build_case_results() -> List[Dict[str, object]]:
    modules = build_scope_modules()
    text, precise, object_detection, spatial = modules
    text_slot = _bind(text, _slot("slot:text"))
    precise_slot = _bind(precise, _slot("slot:precise"))
    object_slot = _bind(object_detection, _slot("slot:object"))
    spatial_slot = _bind(spatial, _slot("slot:spatial"))
    bound_slots = (text_slot, precise_slot, object_slot, spatial_slot)

    read_text = _requirement("req:text-read", "text_recognition", "text_content", "READ_TEXT", "image_evidence", "text_candidate", requirement_type="TEXT_READ")
    precise_read = _requirement("req:precise-read", "precise_ocr", "precise_ocr", "READ_PRECISE_TEXT", "visual_region_candidate", "text_candidate", requirement_type="PRECISE_TEXT_READ")
    field_rule = _requirement("req:field-rule", "text_recognition", "effective_field_rule", "DETERMINE_EFFECTIVE_FIELD_RULE", "image_evidence", "field_rule_candidate", requirement_type="TEXT_READ", authority="FIELD_RULE")
    mandatory_action = _requirement("req:mandatory-action", "text_recognition", "sign_text", "DETERMINE_MANDATORY_ACTION", "image_evidence", "action_candidate", requirement_type="TEXT_READ", authority="ACTION")
    vehicle = _requirement("req:vehicle", "object_detection", "vehicle_presence", "DETECT_OBJECT", "image_evidence", "object_candidate", requirement_type="OBJECT_DETECTION")
    identity = _requirement("req:identity", "object_detection", "person_identity", "IDENTIFY_PERSON", "image_evidence", "identity_candidate", requirement_type="OBJECT_DETECTION")
    danger = _requirement("req:danger", "object_detection", "person_danger_intent", "CLASSIFY_DANGER_INTENT", "image_evidence", "danger_candidate", requirement_type="OBJECT_DETECTION")
    map_need = _requirement("req:map", "spatial_mapping", "spatial_structure", "PROVIDE_SPATIAL_STRUCTURE", "pose_candidate", "spatial_map_candidate", requirement_type="SPATIAL_MAP")
    map_ocr = _requirement("req:map-ocr", "spatial_mapping", "text_content", "READ_TEXT", "image_evidence", "text_candidate", requirement_type="SPATIAL_MAP")
    unknown = _requirement("req:unknown", "text_recognition", "unknown_problem", "UNKNOWN_OPERATION", "image_evidence", "unknown_output", requirement_type="UNKNOWN")
    bad_operation = _requirement("req:bad-operation", "text_recognition", "text_content", "DETERMINE_EFFECTIVE_FIELD_RULE", "image_evidence", "text_candidate", requirement_type="TEXT_READ")
    bad_input = _requirement("req:bad-input", "text_recognition", "text_content", "READ_TEXT", "audio_stream", "text_candidate", requirement_type="TEXT_READ")
    bad_output = _requirement("req:bad-output", "text_recognition", "text_content", "READ_TEXT", "image_evidence", "field_rule_candidate", requirement_type="TEXT_READ")
    provider_overreach = replace(identity, technical_hints=("provider:advertised-person-identity",))
    model_overreach = replace(identity, technical_hints=("model:metadata-person-identity",))
    csa_overreach = replace(identity, technical_hints=("csa:object_detection:v1:expanded",))
    safety_priority = replace(vehicle, required_authority="ACTION", technical_hints=("safety:urgent",))

    text_assessment, text_resolution, text_gap = resolve_scoped_capability_requirement(read_text, modules, bound_slots)
    precise_assessment, precise_resolution, precise_gap = resolve_scoped_capability_requirement(precise_read, modules, bound_slots)
    field_assessment, field_resolution, field_gap = resolve_scoped_capability_requirement(field_rule, modules, bound_slots)
    action_assessment, action_resolution, action_gap = resolve_scoped_capability_requirement(mandatory_action, modules, bound_slots)
    vehicle_assessment, vehicle_resolution, vehicle_gap = resolve_scoped_capability_requirement(vehicle, modules, bound_slots)
    identity_assessment, identity_resolution, identity_gap = resolve_scoped_capability_requirement(identity, modules, bound_slots)
    danger_assessment, danger_resolution, danger_gap = resolve_scoped_capability_requirement(danger, modules, bound_slots)
    map_assessment, map_resolution, map_gap = resolve_scoped_capability_requirement(map_need, modules, bound_slots)
    map_ocr_assessment, map_ocr_resolution, map_ocr_gap = resolve_scoped_capability_requirement(map_ocr, modules, bound_slots)
    unknown_assessment, unknown_resolution, unknown_gap = resolve_scoped_capability_requirement(unknown, modules, bound_slots)
    operation_assessment, operation_resolution, operation_gap = resolve_scoped_capability_requirement(bad_operation, modules, bound_slots)
    input_assessment, input_resolution, input_gap = resolve_scoped_capability_requirement(bad_input, modules, bound_slots)
    output_assessment, output_resolution, output_gap = resolve_scoped_capability_requirement(bad_output, modules, bound_slots)
    provider_assessment, provider_resolution, provider_gap = resolve_scoped_capability_requirement(provider_overreach, modules, bound_slots)
    model_assessment, model_resolution, model_gap = resolve_scoped_capability_requirement(model_overreach, modules, bound_slots)
    csa_assessment, csa_resolution, csa_gap = resolve_scoped_capability_requirement(csa_overreach, modules, bound_slots)
    safety_assessment, safety_resolution, safety_gap = resolve_scoped_capability_requirement(safety_priority, modules, bound_slots)

    unbound_text_assessment, unbound_text_resolution, _ = resolve_scoped_capability_requirement(read_text, modules, (_slot("slot:unbound"),))
    degraded_text = replace(text, lifecycle_state="DEGRADED")
    degraded_assessment, degraded_resolution, _ = resolve_scoped_capability_requirement(read_text, (degraded_text,), (replace(text_slot, lifecycle_state="DEGRADED"),))
    permission_assessment, permission_resolution, _ = resolve_scoped_capability_requirement(read_text, modules, bound_slots, permission_granted=False)
    resource_assessment, resource_resolution, _ = resolve_scoped_capability_requirement(read_text, modules, bound_slots, resource_ready=False)
    missing_impl = replace(text, implementation_refs=())
    missing_assessment, missing_resolution, _ = resolve_scoped_capability_requirement(read_text, (missing_impl,), (text_slot,))
    self_view = build_capability_self_view(modules, bound_slots)
    invocation = build_scoped_invocation_candidate(read_text, text_assessment, text_resolution, invocation_id="invoke:text", module=text, gateway_refs=("Observation Gateway", "FPO / Active Observation Control"), trace_refs=("trace:req:text-read",))
    blocked_invocation = build_scoped_invocation_candidate(field_rule, field_assessment, field_resolution, invocation_id="invoke:field-rule", module=text, gateway_refs=("Observation Gateway",))

    cases = [
        _case("CSR-01", "text reading requirement in scope", text_assessment.in_scope, {"scope_result": text_assessment.scope_result}),
        _case("CSR-02", "text recognition ready", text_resolution.status == "READY_CANDIDATE", {"status": text_resolution.status}),
        _case("CSR-03", "precise OCR requirement in scope", precise_assessment.in_scope and precise_resolution.status == "READY_CANDIDATE", {"scope_result": precise_assessment.scope_result}),
        _case("CSR-04", "OCR cannot determine effective Field Rule", field_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and field_gap is not None, {"reason": field_assessment.reason}),
        _case("CSR-05", "OCR cannot declare mandatory action", action_assessment.scope_result == "OPERATION_UNSUPPORTED" and action_gap is not None, {"reason": action_assessment.reason}),
        _case("CSR-06", "object detection in scope", vehicle_assessment.in_scope and vehicle_resolution.status == "READY_CANDIDATE", {"status": vehicle_resolution.status}),
        _case("CSR-07", "object detection cannot identify person identity", identity_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED", {"reason": identity_assessment.reason}),
        _case("CSR-08", "object detection cannot declare danger intent", danger_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED", {"reason": danger_assessment.reason}),
        _case("CSR-09", "spatial mapping in scope", map_assessment.in_scope and map_resolution.status == "READY_CANDIDATE", {"status": map_resolution.status}),
        _case("CSR-10", "spatial mapping cannot perform OCR", map_ocr_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED", {"reason": map_ocr_assessment.reason}),
        _case("CSR-11", "unknown problem class rejected", unknown_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED", {"reason": unknown_assessment.reason}),
        _case("CSR-12", "unsupported operation rejected", operation_assessment.scope_result == "OPERATION_UNSUPPORTED", {"reason": operation_assessment.reason}),
        _case("CSR-13", "unsupported input contract rejected", input_assessment.scope_result == "INPUT_CONTRACT_UNSUPPORTED", {"reason": input_assessment.reason}),
        _case("CSR-14", "unsupported output contract rejected", output_assessment.scope_result == "OUTPUT_CONTRACT_UNSUPPORTED", {"reason": output_assessment.reason}),
        _case("CSR-15", "authority escalation rejected", safety_assessment.scope_result == "AUTHORITY_NOT_ALLOWED", {"reason": safety_assessment.reason}),
        _case("CSR-16", "scope rejection occurs before invocation", not blocked_invocation.accepted and blocked_invocation.scope_assessment_ref == "scope:req:field-rule", {"reason": blocked_invocation.reason}),
        _case("CSR-17", "provider advertised feature cannot extend Module scope", provider_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and provider_gap is not None, {"technical_hints": provider_overreach.technical_hints}),
        _case("CSR-18", "model metadata cannot extend Module scope", model_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and model_gap is not None, {"technical_hints": model_overreach.technical_hints}),
        _case("CSR-19", "CSA cannot extend Module scope", csa_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and csa_gap is not None, {"technical_hints": csa_overreach.technical_hints}),
        _case("CSR-20", "ready capability forms invocation candidate", invocation.accepted and invocation.scope_assessment_ref == "scope:req:text-read" and invocation.execution_boundary_ref == "Observation Gateway / FPO", {"module_ref": invocation.module_ref}),
        _case("CSR-21", "unavailable capability does not form ready invocation", unbound_text_resolution.status == "UNAVAILABLE_CANDIDATE" and not build_scoped_invocation_candidate(read_text, unbound_text_assessment, unbound_text_resolution, invocation_id="invoke:unbound", module=text).accepted, {"reason": unbound_text_resolution.reason}),
        _case("CSR-22", "degraded capability preserves degraded result", degraded_resolution.status == "DEGRADED_CANDIDATE", {"status": degraded_resolution.status}),
        _case("CSR-23", "permission blocked", permission_resolution.reason == "PERMISSION_BLOCKED" and permission_assessment.in_scope, {"reason": permission_resolution.reason}),
        _case("CSR-24", "resource blocked", resource_resolution.reason == "RESOURCE_BLOCKED" and resource_assessment.in_scope, {"reason": resource_resolution.reason}),
        _case("CSR-25", "implementation missing", missing_resolution.reason == "IMPLEMENTATION_REFERENCE_MISSING" and missing_assessment.in_scope, {"reason": missing_resolution.reason}),
        _case("CSR-26", "unbound Slot", unbound_text_resolution.reason == "MODULE_NOT_BOUND_TO_SLOT", {"reason": unbound_text_resolution.reason}),
        _case("CSR-27", "Capability Self exposes scope", "text_content" in self_view.scope_problem_class_refs and "READ_TEXT" in self_view.scope_operation_refs and self_view.semantic_annotation_refs, {"scope_operations": self_view.scope_operation_refs}),
        _case("CSR-28", "Capability Self cannot mutate scope", self_view.candidate_only and not self_view.self_is_lifecycle_owner, {"self_is_lifecycle_owner": self_view.self_is_lifecycle_owner}),
        _case("CSR-29", "Capability Gap Candidate is non-executing", field_gap is not None and field_gap.candidate_only, {"gap_id": field_gap.gap_id if field_gap else None}),
        _case("CSR-30", "gap does not trigger acquisition", field_gap is not None and field_gap.candidate_only and not hasattr(field_gap, "automatic_acquisition"), {}),
        _case("CSR-31", "gap does not trigger Learning", field_gap is not None and not hasattr(field_gap, "learning_execution"), {}),
        _case("CSR-32", "Safety priority does not bypass scope", safety_assessment.scope_result == "AUTHORITY_NOT_ALLOWED" and safety_gap is not None, {"reason": safety_assessment.reason}),
        _case("CSR-33", "visual invocation preserves FPO/Gateway boundary", invocation.gateway_refs == ("Observation Gateway", "FPO / Active Observation Control") and not invocation.observation_gateway_bypass, {"gateway_refs": invocation.gateway_refs}),
        _case("CSR-34", "Slot has no semantic authority", all(not slot.slot_semantic_authority for slot in bound_slots), {}),
        _case("CSR-35", "Module has no World Truth authority", all(not module.module_world_truth_authority for module in modules), {}),
    ]
    return cases


def build_runner_result() -> Dict[str, object]:
    cases = build_case_results()
    failed = [item["case_id"] for item in cases if not item["passed"]]
    return {
        "phase": "Phase-Luna-Official-Capability-Resolution-Scope-And-Invocation-Bridge-Controlled-Implementation-v1-001",
        "mode": "CONTROLLED_CANDIDATE_ONLY",
        "owner": "Capability Registry / Capability Governance / Universal Slot Resolution Surface",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "scope_validation_before_invocation": True,
        "capability_gap_candidate_supported": True,
        "capability_self_scope_awareness": True,
        "runtime_execution": False,
        "real_provider_invocation": False,
        "provider_invocation": False,
        "model_inference": False,
        "camera_activation": False,
        "real_download": False,
        "real_install": False,
        "real_activation": False,
        "real_upgrade": False,
        "real_rollback": False,
        "brain_direct_capability_mutation": False,
        "user_direct_capability_mutation": False,
        "brain_out_of_scope_capability_request": False,
        "capability_scope_bypass": False,
        "capability_contract_overreach": False,
        "capability_output_authority_escalation": False,
        "provider_extends_module_scope": False,
        "model_metadata_extends_module_scope": False,
        "csa_extends_module_scope": False,
        "slot_semantic_authority": False,
        "slot_world_truth_authority": False,
        "module_world_truth_authority": False,
        "safety_scope_bypass": False,
        "safety_baseline_bypass": False,
        "automatic_capability_acquisition": False,
        "automatic_capability_uninstall": False,
        "automatic_capability_optimization": False,
        "capability_value_scoring": False,
        "learning_execution": False,
        "memory_mutation": False,
        "knowledge_implementation": False,
        "srsk_implementation": False,
        "semantic_folding_execution": False,
        "semantic_expansion_execution": False,
        "market_capability_implementation": False,
        "parallel_capability_registry": False,
        "parallel_capability_resolver": False,
        "parallel_model_manager": False,
        "parallel_capability_self_owner": False,
        "candidate_only": True,
        "cases": cases,
    }
