from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_arrival_resolver_v1 import (
    build_navigation_arrival_candidate_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_crossing_governance_v1 import (
    build_navigation_crossing_assessment_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_deviation_resolver_v1 import (
    build_navigation_deviation_assessment_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_diagnostics_v1 import (
    build_navigation_manager_diagnostics_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_evidence_adapter_v1 import (
    build_navigation_evidence_state_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_guidance_candidate_builder_v1 import (
    build_navigation_guidance_candidate_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_landmark_resolver_v1 import (
    build_navigation_landmark_assessment_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_module_input_adapter_v1 import (
    adapt_navigation_manager_input_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_module_output_builder_v1 import (
    build_navigation_manager_module_output_v1,
    resolve_navigation_manager_module_status_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_obstacle_risk_v1 import (
    build_navigation_obstacle_risk_assessment_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_progress_resolver_v1 import (
    build_navigation_progress_state_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_request_classifier_v1 import (
    build_navigation_request_classification_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_route_adapter_v1 import (
    build_navigation_route_state_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_route_memory_v1 import (
    build_navigation_route_memory_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_speech_handoff_v1 import (
    build_navigation_speech_handoff_candidate_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_task_handoff_v1 import (
    build_navigation_task_handoff_candidate_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_trace_replay_v1 import (
    build_navigation_manager_trace_replay_v1,
)


def run_navigation_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    try:
        input_candidate = adapt_navigation_manager_input_v1(payload)
        request_classification = build_navigation_request_classification_v1(
            input_candidate
        )
        route_state = build_navigation_route_state_v1(input_candidate)
        route_memory = build_navigation_route_memory_v1(input_candidate, route_state)
        progress_state = build_navigation_progress_state_v1(input_candidate)
        evidence_state = build_navigation_evidence_state_v1(input_candidate)
        landmark_assessment = build_navigation_landmark_assessment_v1(
            input_candidate, evidence_state
        )
        crossing_assessment = build_navigation_crossing_assessment_v1(input_candidate)
        obstacle_assessment = build_navigation_obstacle_risk_assessment_v1(
            input_candidate
        )
        deviation_assessment = build_navigation_deviation_assessment_v1(
            input_candidate, progress_state
        )
        guidance_candidate = build_navigation_guidance_candidate_v1(
            input_candidate,
            crossing_assessment,
            obstacle_assessment,
            deviation_assessment,
        )
        arrival_candidate = build_navigation_arrival_candidate_v1(
            input_candidate, progress_state
        )
        task_handoff = build_navigation_task_handoff_candidate_v1(
            input_candidate,
            route_state,
            progress_state,
            arrival_candidate,
        )
        speech_handoff = build_navigation_speech_handoff_candidate_v1(
            input_candidate, guidance_candidate
        )

        module_status = resolve_navigation_manager_module_status_v1(
            input_candidate,
            request_classification,
            route_state,
            route_memory,
            evidence_state,
            crossing_assessment,
            obstacle_assessment,
            deviation_assessment,
            arrival_candidate,
        )
        trace_replay = build_navigation_manager_trace_replay_v1(
            input_candidate, module_status
        )
        rejection_reasons: list[str] = []
        if module_status in {
            "invalid_input",
            "request_rejected",
            "route_unavailable",
            "insufficient_evidence",
            "conflicted",
        }:
            rejection_reasons.append(module_status)

        diagnostics = build_navigation_manager_diagnostics_v1(
            input_candidate,
            module_status,
            evidence_state,
            deviation_assessment,
        )
        output = build_navigation_manager_module_output_v1(
            input_candidate,
            module_status,
            route_state,
            route_memory,
            progress_state,
            landmark_assessment,
            crossing_assessment,
            obstacle_assessment,
            deviation_assessment,
            guidance_candidate,
            arrival_candidate,
            task_handoff,
            speech_handoff,
            diagnostics,
            str(trace_replay.get("trace_ref") or ""),
            str(trace_replay.get("replay_key") or ""),
            tuple(rejection_reasons),
        )
        output.update(
            {
                "request_classification": request_classification,
                "trace_replay": trace_replay,
                "unhandled_exception": False,
            }
        )
        return output
    except Exception:  # noqa: BLE001
        return {
            "capability_id": "luna.navigation_manager",
            "module_status": "internal_error",
            "navigation_request_id": "",
            "task_id": "",
            "navigation_mode": "",
            "route_state": {},
            "route_progress_candidate": {},
            "current_position_candidate": {},
            "landmark_assessment": {},
            "crossing_assessment": {},
            "obstacle_risk_assessment": {},
            "deviation_assessment": {},
            "guidance_candidate": None,
            "arrival_candidate": None,
            "task_handoff_candidate": None,
            "speech_handoff_candidate": None,
            "diagnostics": {
                "schema_version": "navigation_manager_diagnostics_v1",
                "module_status": "internal_error",
            },
            "trace_ref": "",
            "replay_key": "",
            "rejection_reasons": ("internal_error",),
            "boundary_flags": {},
            "unhandled_exception": True,
        }
