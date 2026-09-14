from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .a_route_orchestration_core_types_v1 import ARouteIngressRefsV1, ARouteOrchestrationRequestV1


@dataclass(frozen=True)
class ARouteFixtureCaseV1:
    case_id: str
    title: str
    request: ARouteOrchestrationRequestV1
    expected_lifecycle_state: str
    expected_control_state: str
    expected_error_code: str = ""
    expected_runtime_handoff_status: str = "CONTROLLED_HANDOFF_READY"
    expected_next_cycle: bool = False
    expected_deferred_ref: str = ""


def _request(case_id: str, **overrides: object) -> ARouteOrchestrationRequestV1:
    values: Dict[str, object] = {
        "scenario_id": case_id,
        "ingress": ARouteIngressRefsV1(
            observation_refs=(f"observation:{case_id}",),
            perception_refs=(f"perception:{case_id}",),
            user_input_refs=(f"user-input:{case_id}",),
            field_refs=(f"field:{case_id}",),
        ),
        "context_ref": f"context:{case_id}",
        "pcn_ref": f"pcn:{case_id}",
        "intent_ref": f"intent:{case_id}",
        "cognitive_state_ref": f"state:{case_id}",
        "regulation_ref": f"regulation:{case_id}",
        "decision_ref": f"decision:{case_id}",
        "task_ref": f"task:{case_id}",
        "action_ref": f"action:{case_id}",
        "runtime_ref": f"runtime:{case_id}",
        "result_ref": f"result:{case_id}",
        "memory_experience_ref": f"experience:{case_id}",
        "learning_ref": f"learning:{case_id}",
        "self_ref": f"self:{case_id}",
        "personality_ref": f"personality:{case_id}",
    }
    values.update(overrides)
    return ARouteOrchestrationRequestV1(**values)


def get_a_route_orchestration_fixtures_v1() -> Tuple[ARouteFixtureCaseV1, ...]:
    definitions = (
        ("A01", "normal full A Route controlled cycle", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A02", "missing perception ingress", {"missing_ingress": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A03", "missing context", {"missing_context": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A04", "missing PCN", {"missing_pcn": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A05", "missing Intent", {"missing_intent": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A06", "cognitive state formation stop", {"missing_cognitive_state": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A07", "dynamic regulation stop", {"missing_regulation": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A08", "decision missing", {"missing_decision": True}, "STOPPED", "STOPPED", "MISSING_STAGE_INPUT", "BLOCKED", False, ""),
        ("A09", "task handoff deferred", {"defer_task": True}, "TASK_READY", "DEFERRED", "", "DEFERRED", False, "task_manager_product_lifecycle"),
        ("A10", "action handoff deferred", {"defer_action": True}, "ACTION_READY", "DEFERRED", "", "DEFERRED", False, "action_routing_product_admission"),
        ("A11", "runtime handoff deferred", {"defer_runtime": True}, "EXECUTION_READY", "DEFERRED", "", "DEFERRED", False, "runtime_executor_product_handoff"),
        ("A12", "result returned", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A13", "feedback path", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A14", "memory experience handoff", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A15", "learning evidence handoff", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A16", "self continuity handoff", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A17", "personality context handoff", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A18", "next cycle creation", {"previous_cycle_id": "cycle:A18:previous"}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A19", "duplicate cycle", {"duplicate_cycle": True}, "STOPPED", "STOPPED", "DUPLICATE_CYCLE_START", "BLOCKED", False, ""),
        ("A20", "duplicate handoff", {"duplicate_handoff": True}, "STOPPED", "STOPPED", "DUPLICATE_HANDOFF", "BLOCKED", False, ""),
        ("A21", "duplicate feedback", {"duplicate_feedback": True}, "STOPPED", "STOPPED", "DUPLICATE_RESULT_FEEDBACK", "CONTROLLED_HANDOFF_READY", False, ""),
        ("A22", "reconsideration", {"reconsideration_requested": True}, "COGNITIVE_STATE_READY", "RECONSIDERING", "RECONSIDERATION_REQUESTED", "BLOCKED", False, ""),
        ("A23", "reconsideration depth guard", {"reconsideration_requested": True, "reconsideration_depth": 3}, "FAILED", "FAILED", "RECONSIDERATION_DEPTH_EXCEEDED", "BLOCKED", False, ""),
        ("A24", "upstream contract mismatch", {"contract_mismatch": True}, "FAILED", "FAILED", "CONTRACT_MISMATCH", "BLOCKED", False, ""),
        ("A25", "version mismatch", {"version_mismatch": True}, "FAILED", "FAILED", "VERSION_MISMATCH", "BLOCKED", False, ""),
        ("A26", "owner authority violation", {"owner_authority_violation": True}, "FAILED", "FAILED", "OWNER_AUTHORITY_VIOLATION", "BLOCKED", False, ""),
        ("A27", "trace reverse lookup", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A28", "provenance preservation", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A29", "error propagation", {"missing_decision": True, "upstream_failure": True}, "STOPPED", "STOPPED", "UPSTREAM_FAILURE_PROPAGATION", "BLOCKED", False, ""),
        ("A30", "completed cycle immutability", {"completed_cycle_mutation_probe": True}, "STOPPED", "STOPPED", "COMPLETED_CYCLE_IMMUTABLE", "BLOCKED", False, ""),
        ("A31", "Emotion deferred", {"emotion_deferred": True}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A32", "B Route deferred", {"b_route_deferred": True}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A33", "semantic compression deferred", {"semantic_compression_deferred": True}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A34", "duplicate reconsideration request", {"reconsideration_requested": True, "duplicate_reconsideration": True}, "STOPPED", "STOPPED", "DUPLICATE_RECONSIDERATION", "BLOCKED", False, ""),
        ("A35", "repeated failure signature guard", {"repeated_failure_signature": True}, "STOPPED", "STOPPED", "REPEATED_FAILURE_SIGNATURE", "BLOCKED", False, ""),
        ("A36", "real perception ingress deferred", {"real_ingress_unavailable": True}, "IDLE", "DEFERRED", "", "DEFERRED", False, "DEFERRED_TO_PERCEPTION_OBSERVATION_GATEWAY"),
        ("A37", "typed ingress references accepted", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A38", "controlled runtime handoff remains non-runtime", {}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
        ("A39", "full lineage with previous cycle", {"previous_cycle_id": "cycle:A39:previous"}, "CYCLE_COMPLETE", "CYCLE_COMPLETE", "", "CONTROLLED_HANDOFF_READY", True, ""),
    )
    return tuple(
        ARouteFixtureCaseV1(
            case_id=case_id,
            title=title,
            request=_request(case_id, **overrides),
            expected_lifecycle_state=lifecycle,
            expected_control_state=control,
            expected_error_code=error,
            expected_runtime_handoff_status=runtime_status,
            expected_next_cycle=next_cycle,
            expected_deferred_ref=deferred,
        )
        for case_id, title, overrides, lifecycle, control, error, runtime_status, next_cycle, deferred in definitions
    )
