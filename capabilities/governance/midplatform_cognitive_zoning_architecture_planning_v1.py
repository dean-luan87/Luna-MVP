# -*- coding: utf-8 -*-
"""Midplatform Cognitive Zoning Architecture Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL_GO,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    COGNITIVE_ZONES,
    FINAL_DECISION_GO as VNEXT_FINAL_GO,
    GOVERNANCE_STANDARDS,
    NEXT_PHASE_GO as VNEXT_NEXT_PHASE,
    SEED_CORE_COMPONENTS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Cognitive-Zoning-Architecture-Planning-v1-001"
SCOPE = "cognitive_zoning_architecture_planning_only"
SOURCE_CHAIN = "midplatform_cognitive_zoning_architecture_planning_v1"

UPSTREAM_VNEXT_FINAL = VNEXT_FINAL_GO
UPSTREAM_VNEXT_NEXT = VNEXT_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_COGNITIVE_ZONING_ARCHITECTURE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_COGNITIVE_ZONING_ARCHITECTURE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Cognitive-Zoning-Architecture-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Cognitive-Zoning-Architecture-Issue-Review-v1-001"

LUNA_1_0_DEFINITION = "Monolithic Integration Validation Form"
LUNA_1_0_LABEL = "大集合验证形态"
LUNA_2_0_TARGET = "Modular Life Architecture"
LUNA_2_0_LABEL = "模块化生命体形态"

LUNA_1_0_VALIDATION_ITEMS: Tuple[str, ...] = (
    "Seed Core logic validity",
    "governance standards reusability",
    "cognitive zones separability",
    "candidate/evidence/enforcement/health/whitebox operability",
    "provider abstraction unification",
    "controlled runtime admission",
    "front model rule influence",
    "E2E output chain closure",
)

LUNA_2_0_DIRECTIONS: Tuple[str, ...] = (
    "module split",
    "standard interfaces",
    "capability bus",
    "module registration",
    "module discovery",
    "module hot-plug",
    "module health monitoring",
    "module permission governance",
    "module runtime admission",
    "module version compatibility",
)

MONOLITHIC_TO_MODULAR_CONFIRMATIONS: Tuple[str, ...] = (
    "Luna 1.0 = Monolithic Integration Validation Form",
    "Luna 1.0 purpose is validating whole architecture and chain logic",
    "Luna 2.0 target = Modular Life Architecture",
    "future work includes module split + capability bus + standardized interfaces",
    "current phase does not split files/modules",
    "current phase does not migrate runtime",
    "historical monolithic validation artifacts remain valid evidence",
)

CAPABILITY_BUS_RESPONSIBILITIES: Tuple[str, ...] = (
    "module_registration",
    "module_discovery",
    "capability_contract",
    "input_output_contract",
    "provider_candidate_binding",
    "health_status_sync",
    "resource_requirement_declare",
    "authorization_requirement",
    "runtime_candidate_binding",
    "evidence_output_channel",
    "failure_route",
    "version_compatibility",
)

CAPABILITY_BUS_CONFIRMATIONS: Tuple[str, ...] = (
    "Capability Bus is not runtime execution",
    "Capability Bus does not replace Seed Core",
    "Capability Bus does not replace Decision Center",
    "Capability Bus standardizes pluggable modules",
    "Capability Bus will be planned after Seed Core / Pluggable Layer Architecture",
)

NO_UNIVERSAL_BRAIN_RULES: Tuple[str, ...] = (
    "no single model owns perception + memory + drive + integration + decision + output + execution",
    "models produce candidates, not authority",
    "midplatform governs zones, contracts, routing, boundary, supervision",
    "information integration cannot become universal brain",
    "Seed Core cannot become monolithic model",
    "Decision Center cannot replace governance",
)

ZONE_COMMON_FIELDS: Tuple[str, ...] = (
    "zone_id",
    "zone_role",
    "upstream_inputs",
    "downstream_outputs",
    "allowed_object_types",
    "forbidden_object_types",
    "governance_dependencies",
    "seed_core_dependencies",
    "runtime_boundary",
    "candidate_only_outputs_by_default",
    "cannot_directly_execute",
)

COGNITIVE_ZONE_DEFINITIONS: Tuple[Dict[str, Any], ...] = (
    {
        "zone_id": "perception_zone",
        "zone_name": "Perception Zone",
        "zone_role": "Vision / OCR / ASR / Map / Sensor perception candidates",
        "upstream_inputs": ["sensor_input", "provider_candidate", "health_signal", "drive_signal"],
        "downstream_outputs": ["observation_candidate", "evidence_candidate"],
        "allowed_object_types": ["observation_candidate", "evidence_candidate", "perception_trace_ref"],
        "forbidden_object_types": ["fact", "worldmodel_fact", "user_output", "memory_write"],
        "governance_dependencies": [
            "Provider Abstraction Standard",
            "Candidate / Evidence Contract",
            "Input / Output Boundary Standard",
        ],
        "seed_core_dependencies": ["Survival Drive", "Task Drive", "Autonomous World Observation"],
        "runtime_boundary": "provider runtime via controlled runtime later only",
        "zone_rules": [
            "perception outputs observation_candidate / evidence_candidate",
            "perception does not write fact directly",
            "perception does not write WorldModel directly",
            "perception does not emit user output directly",
            "perception provider must use provider abstraction",
        ],
    },
    {
        "zone_id": "memory_worldmodel_zone",
        "zone_name": "Memory / WorldModel Zone",
        "zone_role": "memory retrieval, knowledge base, worldmodel candidate and write admission",
        "upstream_inputs": ["retrieval_query", "admission_request", "evidence_candidate"],
        "downstream_outputs": ["memory_candidate", "retrieval_evidence_candidate", "write_admission_result"],
        "allowed_object_types": ["memory_candidate", "retrieval_evidence_candidate", "history_candidate"],
        "forbidden_object_types": ["unadmitted_fact", "direct_worldmodel_write", "user_output"],
        "governance_dependencies": [
            "Candidate / Evidence Contract",
            "Validation Engineering Standard",
            "Gate / Enforcement Standard",
        ],
        "seed_core_dependencies": ["Health Management", "Resource Governance"],
        "runtime_boundary": "write requires admission; no direct fact commit",
        "zone_rules": [
            "memory retrieval output is candidate/evidence",
            "memory write requires admission",
            "worldmodel write requires fact admission",
            "stale info may be history candidate, not current action fact",
        ],
    },
    {
        "zone_id": "drive_zone",
        "zone_name": "Drive Zone",
        "zone_role": "Survival Drive / Task Drive / Exploration / Emotion Drive signals",
        "upstream_inputs": ["health_signal", "resource_status", "task_state_candidate", "observation_intent"],
        "downstream_outputs": ["drive_signal_candidate", "observation_intent_candidate"],
        "allowed_object_types": ["drive_signal_candidate", "observation_intent_candidate", "priority_hint"],
        "forbidden_object_types": ["action_execution", "user_output", "runtime_invocation"],
        "governance_dependencies": ["Health Supervision Standard", "Non-Claims Standard"],
        "seed_core_dependencies": [
            "Survival Drive",
            "Task Drive",
            "Resource Governance",
            "Autonomous World Observation",
        ],
        "runtime_boundary": "drive does not execute action",
        "zone_rules": [
            "drive outputs drive_signal_candidate",
            "drive does not execute action",
            "survival drive priority can influence integration/decision",
            "task drive tracks goal/progress/interrupt/resume",
            "autonomous world observation belongs under Survival Drive as observation_intent_candidate",
        ],
    },
    {
        "zone_id": "information_integration_zone",
        "zone_name": "Information Integration Zone",
        "zone_role": "multi-source context integration",
        "upstream_inputs": [
            "candidate",
            "evidence",
            "drive_signal",
            "health_signal",
            "task_context",
            "map_context",
            "memory_context",
        ],
        "downstream_outputs": ["integrated_context_candidate"],
        "allowed_object_types": ["integrated_context_candidate", "conflict_flag", "gap_flag", "freshness_flag"],
        "forbidden_object_types": ["final_decision", "runtime_command", "user_output"],
        "governance_dependencies": [
            "Candidate / Evidence Contract",
            "Whitebox Trace Standard",
            "Input / Output Boundary Standard",
        ],
        "seed_core_dependencies": ["Task Drive", "Health Management", "System Optimization"],
        "runtime_boundary": "does not make final decision; does not execute runtime",
        "zone_rules": [
            "consumes candidate/evidence/drive/health/task/map/memory context",
            "emits integrated_context_candidate",
            "flags conflict/gap/freshness/priority",
            "does not make final decision",
            "does not execute runtime",
        ],
    },
    {
        "zone_id": "decision_zone",
        "zone_name": "Decision Zone",
        "zone_role": "comprehensive decision arbitration",
        "upstream_inputs": [
            "integrated_context_candidate",
            "constitution_refs",
            "validation_result",
            "health_signal",
            "whitebox_trace",
        ],
        "downstream_outputs": ["decision_candidate"],
        "allowed_object_types": ["decision_candidate", "decision_rationale_ref"],
        "forbidden_object_types": ["provider_invocation", "runtime_enable", "gate_bypass"],
        "governance_dependencies": [
            "Gate / Enforcement Standard",
            "Validation Engineering Standard",
            "Health Supervision Standard",
            "Whitebox Trace Standard",
        ],
        "seed_core_dependencies": ["Task Drive", "Survival Drive", "Health Management"],
        "runtime_boundary": "does not invoke provider; does not bypass gates; does not execute runtime",
        "zone_rules": [
            "consumes integrated_context_candidate + constitution refs + validation + health + whitebox",
            "emits decision_candidate",
            "does not invoke provider",
            "does not bypass gates",
            "does not execute runtime",
        ],
    },
    {
        "zone_id": "language_output_zone",
        "zone_name": "Language / Output Zone",
        "zone_role": "task_response / user_output / speech/display gate intake",
        "upstream_inputs": ["decision_candidate", "enforcement_result_candidate", "user_output_candidate"],
        "downstream_outputs": [
            "task_response_candidate",
            "user_output_candidate",
            "speech_gate_result_candidate",
            "display_gate_result_candidate",
        ],
        "allowed_object_types": [
            "task_response_candidate",
            "user_output_candidate",
            "speech_gate_result_candidate",
            "display_gate_result_candidate",
        ],
        "forbidden_object_types": ["user_facing_output", "tts_audio", "display_output", "notification"],
        "governance_dependencies": [
            "Gate / Enforcement Standard",
            "Input / Output Boundary Standard",
            "Non-Claims Standard",
        ],
        "seed_core_dependencies": ["Task Drive", "Health Management"],
        "runtime_boundary": "output remains layered; candidates only",
        "zone_rules": [
            "output remains layered",
            "user_output_candidate ≠ user-facing output",
            "speech_request_candidate ≠ TTS",
            "display_gate_result_candidate ≠ Display Output",
        ],
    },
    {
        "zone_id": "execution_zone",
        "zone_name": "Execution Zone",
        "zone_role": "Voice Output Plane / TTS / Display / Notification / device action controlled runtime",
        "upstream_inputs": [
            "speech_gate_result_candidate",
            "display_gate_result_candidate",
            "controlled_runtime_authorization",
        ],
        "downstream_outputs": ["speech_request_candidate", "audio_artifact_candidate", "display_output_candidate"],
        "allowed_object_types": ["speech_request_candidate", "audio_artifact_candidate", "runtime_result_candidate"],
        "forbidden_object_types": ["raw_constitution", "gate_bypass", "self_authorization"],
        "governance_dependencies": [
            "Controlled Runtime Standard",
            "Gate / Enforcement Standard",
            "Provider Abstraction Standard",
        ],
        "seed_core_dependencies": ["Resource Governance", "Health Management"],
        "runtime_boundary": "execution requires controlled runtime; cannot self-authorize",
        "zone_rules": [
            "execution requires controlled runtime",
            "execution cannot read raw constitution",
            "execution cannot bypass enforcement",
            "execution cannot self-authorize",
        ],
        "cannot_directly_execute": False,
    },
    {
        "zone_id": "governance_zone",
        "zone_name": "Governance Zone",
        "zone_role": "Constitution / Resolver / Validation / Enforcement / Health / Whitebox / Provider / Controlled Runtime",
        "upstream_inputs": ["constitution_source", "candidate", "health_signal", "provider_status"],
        "downstream_outputs": [
            "constraint_bundle",
            "enforcement_result_candidate",
            "validation_result",
            "health_supervision_result_candidate",
            "whitebox_trace",
        ],
        "allowed_object_types": [
            "constraint_bundle",
            "enforcement_result_candidate",
            "gate_result_candidate",
            "health_supervision_result_candidate",
        ],
        "forbidden_object_types": ["raw_execution", "provider_invocation", "user_output"],
        "governance_dependencies": list(GOVERNANCE_STANDARDS),
        "seed_core_dependencies": ["Health Management", "Resource Governance"],
        "runtime_boundary": "governance emits constraints/results/trace, not raw execution",
        "zone_rules": [
            "governance standards reusable",
            "modules cannot create parallel governance",
            "governance emits constraints/gate results/health/trace, not raw execution",
        ],
    },
)

SEED_CORE_INFLUENCES: Tuple[Dict[str, str], ...] = (
    {"influence": "Perception observation priority", "via": "drive_signal / observation_intent"},
    {"influence": "Drive signals", "via": "drive_signal_candidate"},
    {"influence": "Resource allocation", "via": "resource_governance_hint"},
    {"influence": "Health pressure", "via": "health_signal_candidate"},
    {"influence": "System optimization", "via": "optimization_hint"},
    {"influence": "Autonomous observation intent", "via": "observation_intent_candidate"},
    {"influence": "Task priority", "via": "task_drive_signal"},
)

SEED_CORE_FORBIDDEN_DIRECT: Tuple[str, ...] = (
    "invoke perception provider",
    "write memory/worldmodel",
    "decide final action",
    "emit user output",
    "open runtime",
)

ZONE_GOVERNANCE_BINDINGS: Tuple[Dict[str, Any], ...] = tuple(
    {
        "zone_id": z["zone_id"],
        "zone_name": z["zone_name"],
        "governance_dependencies": list(z["governance_dependencies"]),
        "all_standards_accessible": True,
    }
    for z in COGNITIVE_ZONE_DEFINITIONS
)

ZONE_PLUGGABLE_BINDINGS: Tuple[Dict[str, str], ...] = (
    {"zone_id": "perception_zone", "pluggable_capabilities": "Vision/OCR/ASR/Map/Sensor providers"},
    {"zone_id": "memory_worldmodel_zone", "pluggable_capabilities": "Memory/Library/Hive adapters"},
    {"zone_id": "execution_zone", "pluggable_capabilities": "TTS/Display/Notification/Voice Output providers"},
    {"zone_id": "governance_zone", "pluggable_capabilities": "provider adapters under abstraction standard"},
)

HANDOFF_RULES: Tuple[str, ...] = (
    "zones communicate via candidate/signal/evidence/context/result contracts",
    "no zone directly mutates another zone state",
    "no zone bypasses Decision Center for action",
    "no zone bypasses Controlled Runtime for execution",
    "source_chain and version_ref required",
    "handoff must preserve traceability",
)

MODULE_SPLIT_PRINCIPLES: Tuple[str, ...] = (
    "split by zone responsibility",
    "split by capability domain",
    "split by provider abstraction boundary",
    "split by runtime authorization boundary",
    "split by hardware/product form boundary",
    "do not split governance standard into each module",
    "do not duplicate management logic",
    "module can own implementation, not governance sovereignty",
)

SIGNAL_CONTRACT_FIELDS: Tuple[str, ...] = (
    "signal_id",
    "source_zone_id",
    "target_zone_id",
    "signal_type",
    "payload_object_type",
    "source_chain",
    "version_ref",
    "candidate_only",
    "trace_refs",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Cognitive Zoning Planning GO ≠ modules split",
    "Capability Bus positioned ≠ bus implemented",
    "Luna 2.0 modular route planned ≠ current monolith removed",
    "Seed Core dependency planned ≠ Seed Core runtime enabled",
    "next DryRunAndReview ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("cognitive_zoning_architecture_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "module_split_executed_now",
    "capability_bus_runtime_enabled_now",
    "file_migration_started_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "seed_core_runtime_enabled_now",
    "information_integration_runtime_enabled_now",
)

UPSTREAM_RUNTIME_LEAKAGE_FIELDS: Tuple[str, ...] = (
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "controlled_runtime_enabled_now",
    "runtime_execution_window_opened_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_cognitive_zoning_architecture_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "luna_1_0": LUNA_1_0_DEFINITION,
        "luna_2_0_target": LUNA_2_0_TARGET,
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


def _zone_entry(defn: Dict[str, Any]) -> Dict[str, Any]:
    return {
        **{k: defn[k] for k in ZONE_COMMON_FIELDS if k in defn},
        "zone_id": defn["zone_id"],
        "zone_name": defn["zone_name"],
        "zone_role": defn["zone_role"],
        "upstream_inputs": list(defn["upstream_inputs"]),
        "downstream_outputs": list(defn["downstream_outputs"]),
        "allowed_object_types": list(defn["allowed_object_types"]),
        "forbidden_object_types": list(defn["forbidden_object_types"]),
        "governance_dependencies": list(defn["governance_dependencies"]),
        "seed_core_dependencies": list(defn["seed_core_dependencies"]),
        "runtime_boundary": defn["runtime_boundary"],
        "candidate_only_outputs_by_default": True,
        "cannot_directly_execute": defn.get("cannot_directly_execute", True),
        "zone_rules": list(defn.get("zone_rules") or []),
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_midplatform_cognitive_zoning_architecture_planning_v1(
    *,
    midplatform_vnext_architecture_realignment_planning_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    vnext_root = Path(midplatform_vnext_architecture_realignment_planning_root).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()

    vnext_sm = _try_read_json(vnext_root / "summary.json") or {}
    vnext_vr = _try_read_json(vnext_root / "verifier_report.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_vnext_realignment_root": str(vnext_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "output_root": str(out_root),
    }

    if vnext_vr.get("verifier") != "GO":
        blockers.append("vNext Architecture Realignment verifier must be GO")
    if vnext_sm.get("final_decision") != UPSTREAM_VNEXT_FINAL:
        blockers.append("vnext realignment final_decision mismatch")
    if vnext_sm.get("recommended_next_phase") != UPSTREAM_VNEXT_NEXT:
        blockers.append("vnext realignment recommended_next_phase mismatch")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("FMIS DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")

    leakage_issues: List[str] = []
    for label, sm in (
        ("vnext", vnext_sm),
        ("controlled_runtime_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
        ("provider", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    vnext_input_review = {
        "review_id": "vnext_architecture_input_review_v1",
        "vnext_realignment_verifier": vnext_vr.get("verifier"),
        "vnext_realignment_final_decision": vnext_sm.get("final_decision"),
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "cognitive_zoning_planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    zones = [_zone_entry(z) for z in COGNITIVE_ZONE_DEFINITIONS]
    zone_inventory = {
        "inventory_id": "cognitive_zone_inventory_v1",
        "zones": zones,
        "zone_count": len(zones),
        "zone_names": list(COGNITIVE_ZONES),
        **meta,
    }

    responsibility_matrix = {
        "matrix_id": "cognitive_zone_responsibility_matrix_v1",
        "entries": [
            {
                "zone_id": z["zone_id"],
                "zone_name": z["zone_name"],
                "zone_role": z["zone_role"],
                "downstream_outputs": z["downstream_outputs"],
                "cannot_directly_execute": z["cannot_directly_execute"],
            }
            for z in zones
        ],
        "entry_count": len(zones),
        **meta,
    }

    boundary_policy = {
        "policy_id": "cognitive_zone_boundary_policy_v1",
        "zones": [
            {
                "zone_id": z["zone_id"],
                "runtime_boundary": z["runtime_boundary"],
                "forbidden_object_types": z["forbidden_object_types"],
                "candidate_only_outputs_by_default": z["candidate_only_outputs_by_default"],
            }
            for z in zones
        ],
        "zone_rules_by_zone": {z["zone_id"]: z["zone_rules"] for z in zones},
        **meta,
    }

    signal_contract = {
        "contract_id": "cognitive_zone_signal_contract_v1",
        "required_fields": list(SIGNAL_CONTRACT_FIELDS),
        "communication_objects": [
            "candidate",
            "signal",
            "evidence",
            "context",
            "result",
            "trace_ref",
        ],
        "candidate_only_default": True,
        **meta,
    }

    no_universal_brain = {
        "policy_id": "no_universal_brain_zoning_policy_v1",
        "rules": list(NO_UNIVERSAL_BRAIN_RULES),
        "rule_count": len(NO_UNIVERSAL_BRAIN_RULES),
        **meta,
    }

    monolith_to_modular = {
        "plan_id": "monolithic_validation_form_to_modular_life_architecture_plan_v1",
        "luna_1_0_definition": LUNA_1_0_DEFINITION,
        "luna_1_0_label": LUNA_1_0_LABEL,
        "luna_2_0_target": LUNA_2_0_TARGET,
        "luna_2_0_label": LUNA_2_0_LABEL,
        "luna_1_0_validation_items": list(LUNA_1_0_VALIDATION_ITEMS),
        "luna_2_0_directions": list(LUNA_2_0_DIRECTIONS),
        "confirmations": list(MONOLITHIC_TO_MODULAR_CONFIRMATIONS),
        "pc_building_block_mode": True,
        **meta,
    }

    capability_bus = {
        "positioning_id": "luna_capability_bus_positioning_v1",
        "bus_name": "Luna Capability Bus",
        "responsibilities": list(CAPABILITY_BUS_RESPONSIBILITIES),
        "responsibility_count": len(CAPABILITY_BUS_RESPONSIBILITIES),
        "confirmations": list(CAPABILITY_BUS_CONFIRMATIONS),
        "planned_after": "Seed Core / Pluggable Layer Architecture Planning",
        **meta,
    }

    seed_dependency_matrix = {
        "matrix_id": "zone_to_seed_core_dependency_matrix_v1",
        "seed_core_components": list(SEED_CORE_COMPONENTS),
        "influences": list(SEED_CORE_INFLUENCES),
        "forbidden_direct_actions": list(SEED_CORE_FORBIDDEN_DIRECT),
        "zones": [
            {"zone_id": z["zone_id"], "seed_core_dependencies": z["seed_core_dependencies"]}
            for z in zones
        ],
        **meta,
    }

    governance_dependency_matrix = {
        "matrix_id": "zone_to_governance_standard_dependency_matrix_v1",
        "governance_standards": list(GOVERNANCE_STANDARDS),
        "zone_bindings": list(ZONE_GOVERNANCE_BINDINGS),
        "all_zones_bind_governance": True,
        **meta,
    }

    pluggable_dependency_matrix = {
        "matrix_id": "zone_to_pluggable_capability_dependency_matrix_v1",
        "bindings": list(ZONE_PLUGGABLE_BINDINGS),
        "pluggable_layer_required": True,
        **meta,
    }

    handoff_policy = {
        "policy_id": "zone_communication_and_handoff_policy_v1",
        "rules": list(HANDOFF_RULES),
        "rule_count": len(HANDOFF_RULES),
        **meta,
    }

    module_split = {
        "principle_id": "future_module_split_principle_v1",
        "principles": list(MODULE_SPLIT_PRINCIPLES),
        "principle_count": len(MODULE_SPLIT_PRINCIPLES),
        "split_executed_now": False,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "cognitive_zoning_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate cognitive_zoning_model_candidate",
            "verify 8 zone responsibility/boundary",
            "verify no universal brain policy",
            "verify Luna 1.0 monolithic validation → Luna 2.0 modular life architecture route",
            "verify Capability Bus positioning",
            "verify zone communication contract",
            "no runtime enabled",
            "no module split",
        ],
        **meta,
    }

    zones_ok = len(zones) == 8 and all(
        all(f in z for f in ZONE_COMMON_FIELDS) and z.get("candidate_only_outputs_by_default") is True
        for z in zones
    )
    planning_pass = input_ok and zones_ok

    planning_decision = {
        "decision_id": "cognitive_zoning_architecture_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            f"Luna 1.0 = {LUNA_1_0_DEFINITION} ({LUNA_1_0_LABEL})",
            f"Luna 2.0 target = {LUNA_2_0_TARGET} ({LUNA_2_0_LABEL})",
            "8 Cognitive Zones with contracts and boundaries",
            "Luna Capability Bus registered for future modular connection",
            "Fixed Seed Core + Reusable Governance + Zones + Pluggable + Controlled Runtime",
        ],
        **meta,
    }

    policy = {
        "policy_id": "cognitive_zoning_architecture_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "luna_1_0": LUNA_1_0_DEFINITION,
        "luna_2_0_target": LUNA_2_0_TARGET,
        "zone_count": 8,
        "planning_not_split_not_runtime": True,
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
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "cognitive_zoning_architecture_planning_policy": policy,
        "vnext_architecture_input_review": vnext_input_review,
        "cognitive_zone_inventory": zone_inventory,
        "cognitive_zone_responsibility_matrix": responsibility_matrix,
        "cognitive_zone_boundary_policy": boundary_policy,
        "cognitive_zone_signal_contract": signal_contract,
        "no_universal_brain_zoning_policy": no_universal_brain,
        "monolithic_validation_form_to_modular_life_architecture_plan": monolith_to_modular,
        "luna_capability_bus_positioning": capability_bus,
        "zone_to_seed_core_dependency_matrix": seed_dependency_matrix,
        "zone_to_governance_standard_dependency_matrix": governance_dependency_matrix,
        "zone_to_pluggable_capability_dependency_matrix": pluggable_dependency_matrix,
        "zone_communication_and_handoff_policy": handoff_policy,
        "future_module_split_principle": module_split,
        "cognitive_zoning_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "cognitive_zoning_architecture_planning_decision": planning_decision,
        "summary": summary,
    }
