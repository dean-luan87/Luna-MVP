from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .a_route_product_loop_integration_core_types_v1 import ProductLoopInputV1


@dataclass(frozen=True)
class ProductLoopFixtureCaseV1:
    scenario_id: str
    title: str
    request: ProductLoopInputV1
    expected_state: str
    expected_output_kind: str
    expected_feedback_route: str
    expect_runtime_admission: bool = False
    expect_execution_result: bool = False
    expect_observation_reentry: bool = False
    expect_reconsideration: bool = False
    expect_next_cycle: bool = False
    expected_error_code: str = ""
    expected_full_chain: bool = False


def _case(sid: str, title: str, **kwargs) -> ProductLoopFixtureCaseV1:
    request_values = {
        "scenario_id": sid,
        "title": title,
        "ingress_kind": "USER_INPUT",
        "source_ref": f"source:{sid}",
    }
    request_values.update(kwargs.pop("request", {}))
    request = ProductLoopInputV1(**request_values)
    return ProductLoopFixtureCaseV1(sid, title, request, **kwargs)


def build_fixture_cases() -> Tuple[ProductLoopFixtureCaseV1, ...]:
    return (
        _case("L01", "user question, no observation needed", request={"requires_action": False}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L02", "visual observation required", request={"requires_observation": True, "requires_action": False, "observation_modality": "VISION"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L03", "task-scoped OCR", request={"requires_observation": True, "requires_action": False, "observation_modality": "OCR", "information_need": "task-scoped text"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L04", "spatial evidence / SLAM requirement", request={"requires_observation": True, "requires_action": False, "observation_modality": "SLAM_SPATIAL"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L05", "sufficient evidence stops observation", request={"requires_observation": True, "requires_action": False, "observation_sufficient": True}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L06", "insufficient evidence", request={"requires_observation": True, "observation_available": False}, expected_state="REOBSERVATION_REQUIRED", expected_output_kind="OBSERVATION_REQUIRED", expected_feedback_route="REOBSERVE", expect_observation_reentry=True),
        _case("L07", "contradiction", request={"requires_observation": True, "contradiction": True}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L08", "provider failure", request={"requires_observation": True, "provider_failure": True}, expected_state="DEFERRED", expected_output_kind="DEFERRED", expected_feedback_route="DEFER", expected_error_code="PROVIDER_FAILURE"),
        _case("L09", "execution success", expected_state="COMPLETED", expected_output_kind="TASK_COMPLETED", expected_feedback_route="COMPLETE", expect_runtime_admission=True, expect_execution_result=True),
        _case("L10", "partial success", request={"execution_status": "PARTIAL"}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L11", "execution failure", request={"execution_status": "FAILED"}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L12", "stale result", request={"stale_result": True}, expected_state="REOBSERVATION_REQUIRED", expected_output_kind="OBSERVATION_REQUIRED", expected_feedback_route="REOBSERVE", expect_runtime_admission=True, expect_execution_result=True, expect_observation_reentry=True),
        _case("L13", "user correction", request={"user_correction": True, "correction_ref": "correction:L13"}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L14", "task cancellation", request={"task_cancelled": True}, expected_state="ABORTED", expected_output_kind="STATUS", expected_feedback_route="NO_ROUTE", expected_error_code="TASK_CANCELLED"),
        _case("L15", "safety interruption", request={"ingress_kind": "SYSTEM_EVENT", "safety_interrupted": True}, expected_state="ABORTED", expected_output_kind="STATUS", expected_feedback_route="NO_ROUTE", expected_error_code="SAFETY_INTERRUPTION"),
        _case("L16", "duplicate input", request={"duplicate_kind": "input"}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="DUPLICATE_INPUT"),
        _case("L17", "duplicate task", request={"duplicate_kind": "task"}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="DUPLICATE_TASK"),
        _case("L18", "duplicate execution request", request={"duplicate_kind": "execution_request"}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="DUPLICATE_EXECUTION_REQUEST"),
        _case("L19", "duplicate result", request={"duplicate_kind": "execution_result"}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="DUPLICATE_RESULT"),
        _case("L20", "duplicate evaluation", request={"duplicate_kind": "evaluation"}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="DUPLICATE_EVALUATION"),
        _case("L21", "re-observation after evaluation", request={"ingress_kind": "OBSERVATION_FEEDBACK", "stale_result": True, "information_need": "result verification"}, expected_state="REOBSERVATION_REQUIRED", expected_output_kind="OBSERVATION_REQUIRED", expected_feedback_route="REOBSERVE", expect_runtime_admission=True, expect_execution_result=True, expect_observation_reentry=True),
        _case("L22", "learning signal candidate", request={"learning_signal": True, "next_cycle_requested": True}, expected_state="NEXT_CYCLE_READY", expected_output_kind="TASK_COMPLETED", expected_feedback_route="NEXT_CYCLE", expect_runtime_admission=True, expect_execution_result=True, expect_next_cycle=True),
        _case("L23", "completed-cycle immutability", request={"completed_cycle_probe": True}, expected_state="FAILED", expected_output_kind="TASK_FAILED", expected_feedback_route="NO_ROUTE", expected_error_code="COMPLETED_CYCLE_IMMUTABLE"),
        _case("L24", "session-local cycle resume", request={"ingress_kind": "TASK_CONTINUATION", "previous_cycle_id": "cycle:prior", "requires_action": False}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L25", "unresolved observation need", request={"requires_observation": True, "observation_available": False, "information_need": "unresolved target"}, expected_state="REOBSERVATION_REQUIRED", expected_output_kind="OBSERVATION_REQUIRED", expected_feedback_route="REOBSERVE", expect_observation_reentry=True),
        _case("L26", "unresolved hypothesis carryover", request={"unresolved_hypothesis": True}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L27", "resource constraint", request={"resource_constrained": True}, expected_state="DEFERRED", expected_output_kind="DEFERRED", expected_feedback_route="DEFER", expected_error_code="RUNTIME_NOT_ADMITTED"),
        _case("L28", "no provider available", request={"requires_observation": True, "provider_available": False}, expected_state="DEFERRED", expected_output_kind="DEFERRED", expected_feedback_route="DEFER", expected_error_code="PROVIDER_UNAVAILABLE"),
        _case("L29", "runtime adapter unavailable", request={"runtime_available": False}, expected_state="DEFERRED", expected_output_kind="DEFERRED", expected_feedback_route="DEFER", expected_error_code="RUNTIME_NOT_ADMITTED"),
        _case("L30", "controlled-only fallback", request={"requires_action": False, "controlled_only_fallback": True}, expected_state="DEFERRED", expected_output_kind="GUIDANCE", expected_feedback_route="DEFER", expected_error_code="CONTROLLED_ONLY_FALLBACK"),
        _case("L31", "product response candidate", request={"requires_action": False}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L32", "user interruption", request={"ingress_kind": "USER_CORRECTION", "task_cancelled": True}, expected_state="ABORTED", expected_output_kind="STATUS", expected_feedback_route="NO_ROUTE", expected_error_code="TASK_CANCELLED"),
        _case("L33", "next-cycle ingress", request={"next_cycle_requested": True}, expected_state="NEXT_CYCLE_READY", expected_output_kind="TASK_COMPLETED", expected_feedback_route="NEXT_CYCLE", expect_runtime_admission=True, expect_execution_result=True, expect_next_cycle=True),
        _case("L34", "trace reverse lookup", request={"requires_action": False}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L35", "no Emotion Engine", request={"requires_action": False, "deferred_workstream": "emotion_engine"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L36", "no B Route", request={"requires_action": False, "deferred_workstream": "b_route"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L37", "no semantic compression", request={"requires_action": False, "deferred_workstream": "semantic_compression"}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L38", "no hidden provider execution", request={"requires_action": False}, expected_state="COMPLETED", expected_output_kind="RESPONSE", expected_feedback_route="COMPLETE"),
        _case("L39", "no hidden retry", request={"execution_status": "FAILED", "no_hidden_retry_probe": True}, expected_state="RECONSIDERING", expected_output_kind="GUIDANCE", expected_feedback_route="RECONSIDER", expect_runtime_admission=True, expect_execution_result=True, expect_reconsideration=True),
        _case("L40", "full synthetic A Route product loop", request={"requires_observation": True, "observation_modality": "VISION", "information_need": "task goal", "requires_action": True}, expected_state="COMPLETED", expected_output_kind="TASK_COMPLETED", expected_feedback_route="COMPLETE", expect_runtime_admission=True, expect_execution_result=True, expected_full_chain=True),
    )
