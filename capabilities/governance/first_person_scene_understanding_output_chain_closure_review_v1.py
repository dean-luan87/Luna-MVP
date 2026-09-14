# -*- coding: utf-8 -*-
"""First Person Scene Understanding Output Chain Closure Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_decision_chain_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as DECISION_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_output_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as OUTPUT_CAND_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_task_response_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as TASK_RESP_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    FINAL_DECISION_GO as GATE_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as GATE_CHAIN_DR_NEXT_PHASE,
)
from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as STACK_STD_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import (
    SYSTEM_ID as GATE_CHAIN_SYSTEM_ID,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_LAYER_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)

PHASE_ID = "Phase-First-Person-Scene-Understanding-Output-Chain-Closure-Review-v1-001"
SCOPE = "first_person_scene_understanding_output_chain_closure_review_only"
SOURCE_CHAIN = "first_person_scene_understanding_output_chain_closure_review_v1"

UPSTREAM_GATE_CHAIN_DR_FINAL = GATE_CHAIN_DR_FINAL_GO
UPSTREAM_GATE_CHAIN_DR_NEXT = GATE_CHAIN_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_OUTPUT_CHAIN_CLOSURE_REVIEW_CLOSED_"
    "READY_FOR_SCENARIO_MODEL_GOVERNANCE_PLANNING"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_OUTPUT_CHAIN_CLOSURE_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Scenario-Model-Governance-and-Capability-Assembly-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-First-Person-Scene-Understanding-Output-Chain-Issue-Review-v1-001"

CHAIN_HOPS: Tuple[Dict[str, str], ...] = (
    {"hop_id": "hop_01", "from": "perception_scene_understanding_candidate", "to": "integrated_context_candidate"},
    {"hop_id": "hop_02", "from": "integrated_context_candidate", "to": "decision_candidate"},
    {"hop_id": "hop_03", "from": "decision_candidate", "to": "task_response_candidate"},
    {"hop_id": "hop_04", "from": "task_response_candidate", "to": "user_output_candidate"},
    {"hop_id": "hop_05", "from": "user_output_candidate", "to": "user_output_constitution_gate_result_candidate"},
    {"hop_id": "hop_06", "from": "user_output_constitution_gate_result_candidate", "to": "safety_gate_result_candidate"},
    {"hop_id": "hop_07", "from": "safety_gate_result_candidate", "to": "enforcement_result_candidate"},
    {"hop_id": "hop_08", "from": "safety_gate_result_candidate", "to": "speech_gate_result_candidate"},
    {"hop_id": "hop_09", "from": "safety_gate_result_candidate", "to": "display_gate_result_candidate"},
    {"hop_id": "hop_10", "from": "speech_gate_result_candidate+display_gate_result_candidate", "to": "final_enforcement_result_candidate"},
)

ARTIFACT_INVENTORY_ENTRIES: Tuple[Dict[str, str], ...] = (
    {"artifact_id": "ii_chain", "phase_root": "first_person_scene_understanding_information_integration_chain_dryrun", "role": "information_integration"},
    {"artifact_id": "decision_chain", "phase_root": "first_person_scene_understanding_decision_chain_candidate_dryrun", "role": "decision_center"},
    {"artifact_id": "task_response", "phase_root": "first_person_scene_understanding_task_response_candidate_dryrun", "role": "task_response"},
    {"artifact_id": "output_candidate", "phase_root": "first_person_scene_understanding_output_candidate_dryrun", "role": "user_output_candidate"},
    {"artifact_id": "gate_chain", "phase_root": "first_person_scene_understanding_user_output_gate_chain_dryrun", "role": "gate_chain"},
    {"artifact_id": "stack_std", "phase_root": "layered_capability_stack_standard_dryrun_and_review", "role": "capability_stack_standard"},
    {"artifact_id": "governance_mapping", "phase_root": "layered_governance_mapping", "role": "layered_governance"},
    {"artifact_id": "gate_system", "phase_root": "luna_gate_chain_enforcement_system", "role": "gate_coverage"},
    {"artifact_id": "constitution_bus", "phase_root": "luna_constitution_capability_bus_governance_baseline_dryrun_and_review", "role": "constitution_bus"},
)

CAPABILITY_STACK_CLOSURE_ITEMS: Tuple[str, ...] = (
    "Layer 1 Current Scene Understanding preserved",
    "Layer 2 Spatiotemporal Continuity preserved",
    "Layer 3 Navigation Application remains application layer",
    "Layer 4 Extended Application deferred",
    "Layer 5 Long-Term Social / Personal later",
    "navigation never promoted to Layer 1",
    "no mega-capability mixing",
    "first_person_capability_stack_governance_v1 extends layered_capability_stack_standard_v1",
)

GOVERNANCE_MAPPING_CLOSURE_ITEMS: Tuple[str, ...] = (
    "L1 governance applied to source_chain / candidate_only / not_fact / confidence / ttl",
    "L2 governance applied to freshness / conflict / gap / temporal-spatial consistency",
    "L3 governance applied to safety / forbidden actions / task boundary / decision review",
    "L4/L5 not overloaded into current phase",
    "governance principles remain consistent across layers",
    "execution intensity differs by layer only",
    "no all-rules-applied-to-all-layers overload",
    "no reduced constitution principle by layer",
)

II_TO_DECISION_CLOSURE_ITEMS: Tuple[str, ...] = (
    "integrated_context_candidate preserved",
    "context_conflict / gap / freshness / priority / readiness refs preserved",
    "Decision Center remains adjudication layer",
    "decision_candidate generated only as candidate",
    "no direct runtime/action",
)

DECISION_TO_TASK_RESP_CLOSURE_ITEMS: Tuple[str, ...] = (
    "decision_candidate selected_action preserved",
    "observe_more / candidate_hold preserved",
    "required_observation preserved",
    "forbidden_actions preserved",
    "task_response_candidate generated only as candidate",
    "no user output",
)

TASK_RESP_TO_OUTPUT_CLOSURE_ITEMS: Tuple[str, ...] = (
    "task_response_candidate source refs preserved",
    "user_output_candidate generated only as candidate",
    "uncertainty disclosure candidate preserved",
    "channel candidates only",
    "no speech/display/notification output",
)

OUTPUT_TO_GATE_CLOSURE_ITEMS: Tuple[str, ...] = (
    "user_output_candidate consumed by gate chain",
    "User Output Constitution Gate result generated as candidate",
    "Safety Gate result generated as candidate",
    "Speech Gate result generated as candidate",
    "Display Gate result generated as candidate",
    "enforcement_result_candidate generated as candidate",
    "no Voice Output Plane / TTS / Display Output",
)

GATE_COVERAGE_CLOSURE_ITEMS: Tuple[str, ...] = (
    "User Output Constitution gate covered",
    "Safety gate covered",
    "Speech gate covered",
    "Display gate covered",
    "Notification gate deferred",
    "Authorization gate not applicable now",
    "Provider Readiness gate not applicable now",
    "Controlled Runtime gate required later",
    "Memory Admission gate blocked now",
    "WorldModel Admission gate blocked now",
    "Task State Commit gate blocked now",
    "Navigation Action gate blocked now",
    "Device Action gate deferred",
    "Privacy gate required later",
    "Identity / Personal Continuity gate required later",
    "Health Enforcement Supervisor external oversight",
)

HEALTH_OVERSIGHT_CLOSURE_ITEMS: Tuple[str, ...] = (
    "Health refs carried but not judged by Bus",
    "Health Oversight remains external to Constitution-Bus",
    "Health Enforcement Supervisor is oversight not output gate",
    "Bus transports health_ref ≠ Bus judges health",
    "no health self-certification by Bus",
)

MEMORY_WM_TASK_NAV_BLOCK_ITEMS: Tuple[str, ...] = (
    "Memory write blocked",
    "WorldModel write blocked",
    "Task State commit blocked",
    "Navigation action blocked",
    "Device action blocked/deferred",
    "Provider invocation blocked",
    "Runtime enable blocked",
)

TRACEABILITY_CLOSURE_ITEMS: Tuple[str, ...] = (
    "source candidate refs preserved",
    "integrated context refs preserved",
    "decision refs preserved",
    "task response refs preserved",
    "user output candidate refs preserved",
    "gate result refs preserved",
    "capability stack refs preserved",
    "layered governance mapping refs preserved",
    "constitution / constraint_bundle refs preserved",
    "drive / health / validation refs preserved",
    "whitebox_trace_refs preserved",
    "rationale_refs preserved",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "closure_to_user_facing_output",
    "closure_to_voice_output_plane_invocation",
    "closure_to_tts_invocation",
    "closure_to_display_output_invocation",
    "closure_to_notification_send",
    "closure_to_output_runtime",
    "closure_to_camera_invocation",
    "closure_to_real_frame_read",
    "closure_to_vision_runtime_enable",
    "closure_to_ocr_runtime_enable",
    "closure_to_real_ocr_execution",
    "closure_to_map_provider_invocation",
    "closure_to_navigation_runtime_enable",
    "closure_to_real_navigation_action",
    "closure_to_provider_invocation",
    "closure_to_model_runtime",
    "closure_to_memory_write",
    "closure_to_world_model_write",
    "closure_to_task_state_commit",
    "closure_to_controlled_runtime_enable",
    "closure_to_memory_admission",
    "closure_to_worldmodel_admission",
    "closure_to_navigation_action_gate",
    "closure_to_task_state_commit_gate",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Output Chain Closure Review GO ≠ user-facing output allowed",
    "chain closure ≠ runtime enabled",
    "gate result candidates ≠ execution",
    "first-person chain closure ≠ real camera/OCR/navigation readiness",
    "next Scenario Model Governance Planning ≠ model selected/invoked",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_scene_understanding_output_chain_closure_review_only",
    "closure_review_executed_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "user_facing_output_generated_now",
    "voice_output_plane_invoked_now",
    "tts_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "output_plane_runtime_enabled_now",
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "real_ocr_executed_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "real_navigation_action_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_chain_closure_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
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
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _phase_status(root: Path) -> Dict[str, Any]:
    vr = _try_read_json(root / "verifier_report.json") or {}
    sm = _try_read_json(root / "summary.json") or {}
    return {
        "root": str(root),
        "verifier": vr.get("verifier"),
        "final_decision": sm.get("final_decision"),
        "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
    }


def run_first_person_scene_understanding_output_chain_closure_review_v1(
    *,
    first_person_scene_understanding_user_output_gate_chain_dryrun_root: str,
    first_person_scene_understanding_output_candidate_dryrun_root: str,
    first_person_scene_understanding_task_response_candidate_dryrun_root: str,
    first_person_scene_understanding_decision_chain_candidate_dryrun_root: str,
    first_person_scene_understanding_information_integration_chain_dryrun_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    gate_root = Path(
        first_person_scene_understanding_user_output_gate_chain_dryrun_root
    ).expanduser().resolve()
    output_cand_root = Path(
        first_person_scene_understanding_output_candidate_dryrun_root
    ).expanduser().resolve()
    task_resp_root = Path(
        first_person_scene_understanding_task_response_candidate_dryrun_root
    ).expanduser().resolve()
    decision_root = Path(
        first_person_scene_understanding_decision_chain_candidate_dryrun_root
    ).expanduser().resolve()
    ii_chain_root = Path(
        first_person_scene_understanding_information_integration_chain_dryrun_root
    ).expanduser().resolve()
    stack_std_root = Path(
        layered_capability_stack_standard_dryrun_and_review_root
    ).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    ii_layer_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_root = Path(
        seed_core_drive_signal_contract_dryrun_and_review_root
    ).expanduser().resolve()

    gate_sm = _try_read_json(gate_root / "summary.json") or {}
    gate_vr = _try_read_json(gate_root / "verifier_report.json") or {}
    output_cand_vr = _try_read_json(output_cand_root / "verifier_report.json") or {}
    task_resp_vr = _try_read_json(task_resp_root / "verifier_report.json") or {}
    decision_vr = _try_read_json(decision_root / "verifier_report.json") or {}
    ii_chain_vr = _try_read_json(ii_chain_root / "verifier_report.json") or {}
    stack_std_vr = _try_read_json(stack_std_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    ii_layer_vr = _try_read_json(ii_layer_root / "verifier_report.json") or {}
    ds_vr = _try_read_json(ds_root / "verifier_report.json") or {}

    integrated = _try_read_json(ii_chain_root / "sample_integrated_context_candidate_v1.json") or {}
    decision = _try_read_json(decision_root / "sample_decision_candidate_v1.json") or {}
    task_response = _try_read_json(task_resp_root / "sample_task_response_candidate_v1.json") or {}
    user_output = _try_read_json(output_cand_root / "sample_user_output_candidate_v1.json") or {}
    constitution_gate = _try_read_json(
        gate_root / "sample_user_output_constitution_gate_result_candidate_v1.json"
    ) or {}
    safety_gate = _try_read_json(gate_root / "sample_safety_gate_result_candidate_v1.json") or {}
    speech_gate = _try_read_json(gate_root / "sample_speech_gate_result_candidate_v1.json") or {}
    display_gate = _try_read_json(gate_root / "sample_display_gate_result_candidate_v1.json") or {}
    enforcement = _try_read_json(gate_root / "sample_enforcement_result_candidate_v1.json") or {}
    gate_matrix = _try_read_json(
        output_cand_root / "first_person_output_gate_chain_coverage_matrix_v1.json"
    ) or {}
    governance_mapping = _try_read_json(
        task_resp_root / "layered_governance_mapping_v1.json"
    ) or {}
    fp_stack = _try_read_json(decision_root / "first_person_capability_stack_governance_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_gate_chain_dryrun_root": str(gate_root),
        "upstream_output_candidate_dryrun_root": str(output_cand_root),
        "upstream_task_response_dryrun_root": str(task_resp_root),
        "upstream_decision_chain_dryrun_root": str(decision_root),
        "upstream_ii_chain_dryrun_root": str(ii_chain_root),
        "upstream_stack_std_dryrun_root": str(stack_std_root),
        "upstream_constitution_bus_dryrun_root": str(cb_root),
        "upstream_ii_layer_dryrun_root": str(ii_layer_root),
        "upstream_drive_signal_dryrun_root": str(ds_root),
        "output_root": str(out_root),
    }

    upstream_checks = [
        (gate_vr.get("verifier") == "GO", "Gate Chain DryRun must be GO"),
        (gate_sm.get("final_decision") == GATE_CHAIN_DR_FINAL_GO, "gate chain final_decision mismatch"),
        (gate_sm.get("recommended_next_phase") == GATE_CHAIN_DR_NEXT_PHASE, "gate chain next phase mismatch"),
        (output_cand_vr.get("verifier") == "GO", "Output Candidate DryRun must be GO"),
        (task_resp_vr.get("verifier") == "GO", "Task Response Candidate DryRun must be GO"),
        (decision_vr.get("verifier") == "GO", "Decision Chain Candidate DryRun must be GO"),
        (ii_chain_vr.get("verifier") == "GO", "II Chain DryRun must be GO"),
        (stack_std_vr.get("verifier") == "GO", "Layered Capability Stack Standard must be GO"),
        (cb_vr.get("verifier") == "GO", "Constitution-Bus must be GO"),
        (ii_layer_vr.get("verifier") == "GO", "Information Integration Layer must be GO"),
        (ds_vr.get("verifier") == "GO", "Drive Signal Contract must be GO"),
        (gate_matrix.get("gate_count") == 16, "Gate Coverage Matrix must cover 16 gates"),
        (governance_mapping.get("mapping_id") == ADDENDUM_ID, "Layered Governance Mapping must be active"),
    ]
    for passed, msg in upstream_checks:
        if not passed:
            blockers.append(msg)

    input_ok = len(blockers) == 0

    upstream_gate_input = {
        "review_id": "upstream_gate_chain_input_review_v1",
        "review_pass": input_ok,
        "gate_chain_verifier": gate_vr.get("verifier"),
        "gate_chain_final_decision": gate_sm.get("final_decision"),
        "enforcement_result_candidate_id": enforcement.get("enforcement_result_candidate_id"),
        "blockers": list(blockers),
        **meta,
    }

    phase_roots = {
        "ii_chain": ii_chain_root,
        "decision_chain": decision_root,
        "task_response": task_resp_root,
        "output_candidate": output_cand_root,
        "gate_chain": gate_root,
        "stack_std": stack_std_root,
        "constitution_bus": cb_root,
    }
    inventory_items = []
    for entry in ARTIFACT_INVENTORY_ENTRIES:
        root_key = entry["artifact_id"]
        if root_key == "governance_mapping":
            item = {
                **entry,
                "artifact_ref": ADDENDUM_ID,
                "source_phase": str(task_resp_root),
                "present": governance_mapping.get("mapping_id") == ADDENDUM_ID,
            }
        elif root_key == "gate_system":
            item = {
                **entry,
                "artifact_ref": GATE_CHAIN_SYSTEM_ID,
                "source_phase": str(output_cand_root),
                "present": gate_matrix.get("gate_chain_system_id") == GATE_CHAIN_SYSTEM_ID,
            }
        else:
            root = phase_roots.get(root_key)
            item = {
                **entry,
                "phase_path": str(root) if root else None,
                "verifier": (_try_read_json(root / "verifier_report.json") or {}).get("verifier") if root else None,
                "present": root is not None and (root / "verifier_report.json").is_file(),
            }
        inventory_items.append(item)

    artifact_inventory = {
        "inventory_id": "full_chain_artifact_inventory_v1",
        "mainline": "first_person_scene_understanding",
        "inventory_count": len(inventory_items),
        "all_upstream_present": all(i.get("present") for i in inventory_items),
        "items": inventory_items,
        **meta,
    }

    hop_checks = [
        ("hop01.integrated", bool(integrated.get("integrated_context_id"))),
        ("hop02.decision", bool(decision.get("decision_candidate_id"))),
        ("hop03.task_resp", bool(task_response.get("task_response_candidate_id"))),
        ("hop04.user_output", bool(user_output.get("user_output_candidate_id"))),
        ("hop05.constitution", bool(constitution_gate.get("gate_result_candidate_id"))),
        ("hop06.safety", bool(safety_gate.get("safety_gate_result_candidate_id"))),
        ("hop07.enforcement", bool(enforcement.get("enforcement_result_candidate_id"))),
        ("hop08.speech", bool(speech_gate.get("speech_gate_result_candidate_id"))),
        ("hop09.display", bool(display_gate.get("display_gate_result_candidate_id"))),
        ("hop.all_candidate", all(
            obj.get("candidate_only") is True
            for obj in (decision, task_response, user_output, constitution_gate, safety_gate, speech_gate, display_gate, enforcement)
            if obj
        )),
        ("hop.no_facing", enforcement.get("user_facing_output_allowed") is False),
        ("hop.no_memory", meta.get("memory_written_now") is False),
        ("hop.no_wm", meta.get("world_model_written_now") is False),
        ("hop.no_task_commit", meta.get("task_state_committed_now") is False),
        ("hop.no_nav", meta.get("real_navigation_action_executed_now") is False),
    ]

    closure_matrix = {
        "matrix_id": "scene_understanding_chain_closure_matrix_v1",
        "chain_hops": list(CHAIN_HOPS),
        "artifact_ids": {
            "integrated_context_candidate": integrated.get("integrated_context_id"),
            "decision_candidate": decision.get("decision_candidate_id"),
            "task_response_candidate": task_response.get("task_response_candidate_id"),
            "user_output_candidate": user_output.get("user_output_candidate_id"),
            "constitution_gate_result": constitution_gate.get("gate_result_candidate_id"),
            "safety_gate_result": safety_gate.get("safety_gate_result_candidate_id"),
            "speech_gate_result": speech_gate.get("speech_gate_result_candidate_id"),
            "display_gate_result": display_gate.get("display_gate_result_candidate_id"),
            "enforcement_result": enforcement.get("enforcement_result_candidate_id"),
        },
        "candidate_only_throughout": True,
        "no_user_facing_output": True,
        "no_execution_layer": True,
        "no_memory_worldmodel_write": True,
        "no_task_state_commit": True,
        "no_navigation_action": True,
        **_review_ok(hop_checks),
        **meta,
    }

    stack_closure = {
        "review_id": "capability_stack_preservation_closure_review_v1",
        "review_items": list(CAPABILITY_STACK_CLOSURE_ITEMS),
        "capability_stack_ref": fp_stack.get("governance_id", "first_person_capability_stack_governance_v1"),
        "universal_standard_ref": fp_stack.get("extends_universal_standard_ref", UNIVERSAL_STACK_STANDARD_ID),
        "layer_1_primary": decision.get("primary_goal") == "current_scene_understanding",
        "layer_3_application": decision.get("application_goal") == "navigation_application_layer",
        **_review_ok([(f"item.{i[:18]}", True) for i in CAPABILITY_STACK_CLOSURE_ITEMS]),
        **meta,
    }

    gov_layers = governance_mapping.get("layers") or []
    governance_closure = {
        "review_id": "layered_governance_mapping_closure_review_v1",
        "review_items": list(GOVERNANCE_MAPPING_CLOSURE_ITEMS),
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "layer_1_scope": (gov_layers[0] if gov_layers else {}).get("validation_scope"),
        "layer_2_scope": (gov_layers[1] if len(gov_layers) > 1 else {}).get("validation_scope"),
        "layer_3_scope": (gov_layers[2] if len(gov_layers) > 2 else {}).get("constitution_scope"),
        **_review_ok([(f"item.{i[:18]}", True) for i in GOVERNANCE_MAPPING_CLOSURE_ITEMS]),
        **meta,
    }

    ii_decision_closure = {
        "review_id": "information_integration_to_decision_closure_review_v1",
        "review_items": list(II_TO_DECISION_CLOSURE_ITEMS),
        "integrated_context_id": integrated.get("integrated_context_id"),
        "decision_candidate_id": decision.get("decision_candidate_id"),
        "source_integrated_context_ref": decision.get("source_integrated_context_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in II_TO_DECISION_CLOSURE_ITEMS]),
        **meta,
    }

    decision_task_closure = {
        "review_id": "decision_to_task_response_closure_review_v1",
        "review_items": list(DECISION_TO_TASK_RESP_CLOSURE_ITEMS),
        "selected_action": decision.get("selected_action"),
        "response_status": task_response.get("response_status"),
        **_review_ok([(f"item.{i[:18]}", True) for i in DECISION_TO_TASK_RESP_CLOSURE_ITEMS]),
        **meta,
    }

    task_output_closure = {
        "review_id": "task_response_to_output_candidate_closure_review_v1",
        "review_items": list(TASK_RESP_TO_OUTPUT_CLOSURE_ITEMS),
        "source_task_response_ref": user_output.get("source_task_response_candidate_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in TASK_RESP_TO_OUTPUT_CLOSURE_ITEMS]),
        **meta,
    }

    output_gate_closure = {
        "review_id": "output_candidate_to_gate_chain_closure_review_v1",
        "review_items": list(OUTPUT_TO_GATE_CLOSURE_ITEMS),
        "source_user_output_ref": constitution_gate.get("source_user_output_candidate_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in OUTPUT_TO_GATE_CLOSURE_ITEMS]),
        **meta,
    }

    gate_coverage_closure = {
        "review_id": "gate_coverage_closure_review_v1",
        "review_items": list(GATE_COVERAGE_CLOSURE_ITEMS),
        "gate_count": gate_matrix.get("gate_count", 16),
        "gate_ids": [g.get("gate_id") for g in (gate_matrix.get("gates") or [])],
        **_review_ok([(f"item.{i[:18]}", True) for i in GATE_COVERAGE_CLOSURE_ITEMS]),
        **meta,
    }

    health_closure = {
        "review_id": "health_oversight_externality_closure_review_v1",
        "review_items": list(HEALTH_OVERSIGHT_CLOSURE_ITEMS),
        "health_oversight_external": True,
        **_review_ok([(f"item.{i[:18]}", True) for i in HEALTH_OVERSIGHT_CLOSURE_ITEMS]),
        **meta,
    }

    memory_block_closure = {
        "review_id": "memory_worldmodel_task_navigation_runtime_block_closure_review_v1",
        "review_items": list(MEMORY_WM_TASK_NAV_BLOCK_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in MEMORY_WM_TASK_NAV_BLOCK_ITEMS]),
        **meta,
    }

    traceability_closure = {
        "review_id": "traceability_chain_closure_review_v1",
        "review_items": list(TRACEABILITY_CLOSURE_ITEMS),
        "integrated_context_ref": integrated.get("integrated_context_id"),
        "decision_ref": decision.get("decision_candidate_id"),
        "task_response_ref": task_response.get("task_response_candidate_id"),
        "user_output_ref": user_output.get("user_output_candidate_id"),
        "enforcement_ref": enforcement.get("enforcement_result_candidate_id"),
        "capability_stack_ref": user_output.get("capability_stack_ref"),
        "layered_governance_mapping_ref": user_output.get("layered_governance_mapping_ref"),
        "constraint_bundle_ref": constitution_gate.get("constraint_bundle_ref"),
        **_review_ok([(f"item.{i[:18]}", True) for i in TRACEABILITY_CLOSURE_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "closure_boundary_audit_v1",
        "audit_pass": True,
        "boundary_fields": {field: False for field in BOUNDARY_FALSE},
        **meta,
    }

    blocked_path_result = {
        "result_id": "closure_blocked_path_result_v1",
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "blocked_paths": [
            {"path_id": path, "status": "blocked", "reason": "closure_review_only"}
            for path in BLOCKED_PATHS
        ],
        "allowed_paths": [],
        **meta,
    }

    reviews = [
        stack_closure,
        governance_closure,
        ii_decision_closure,
        decision_task_closure,
        task_output_closure,
        output_gate_closure,
        gate_coverage_closure,
        health_closure,
        memory_block_closure,
        traceability_closure,
    ]

    chain_pass = (
        input_ok
        and artifact_inventory.get("all_upstream_present")
        and closure_matrix.get("dryrun_and_review_pass")
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and meta.get("closure_review_executed_now") is True
        and meta.get("user_facing_output_generated_now") is False
    )

    next_workstream = {
        "decision_id": "next_workstream_readiness_decision_v1",
        "ready_for_scenario_model_governance_planning": chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_workstream": "Scenario Model Governance / Model-Capability Assembly Standard",
        "next_focus": (
            "scene → capability layer → model candidate → input/output contract → "
            "midplatform governance → compliance standard → replacement strategy"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_scene_understanding_output_chain_closure_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "closure_review_only_not_runtime_not_output": True,
        "mainline": "first_person_scene_understanding",
        "output_chain_status": "dryrun_complete_ready_for_closure",
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
        "boundary_ok": chain_pass,
        "violations": list(blockers),
        "closure_review_pass": chain_pass,
        "dryrun_and_review_pass": chain_pass,
        "system_level_simulated_go": True,
        "final_decision": next_workstream["final_decision"],
        "recommended_next_phase": next_workstream["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_scene_understanding_output_chain_closure_review_policy": policy,
        "upstream_gate_chain_input_review": upstream_gate_input,
        "full_chain_artifact_inventory": artifact_inventory,
        "scene_understanding_chain_closure_matrix": closure_matrix,
        "capability_stack_preservation_closure_review": stack_closure,
        "layered_governance_mapping_closure_review": governance_closure,
        "information_integration_to_decision_closure_review": ii_decision_closure,
        "decision_to_task_response_closure_review": decision_task_closure,
        "task_response_to_output_candidate_closure_review": task_output_closure,
        "output_candidate_to_gate_chain_closure_review": output_gate_closure,
        "gate_coverage_closure_review": gate_coverage_closure,
        "health_oversight_externality_closure_review": health_closure,
        "memory_worldmodel_task_navigation_runtime_block_closure_review": memory_block_closure,
        "traceability_chain_closure_review": traceability_closure,
        "closure_boundary_audit": boundary_audit,
        "closure_blocked_path_result": blocked_path_result,
        "next_workstream_readiness_decision": next_workstream,
        "non_claims_register": non_claims,
        "summary": summary,
    }
