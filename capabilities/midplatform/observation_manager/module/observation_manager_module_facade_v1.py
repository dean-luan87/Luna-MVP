from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_admission_handoff_v1 import (
    build_observation_admission_handoff_candidate_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_attention_coordinator_v1 import (
    build_observation_attention_plan_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_candidate_builder_v1 import (
    build_observation_candidate_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_crossmodal_association_v1 import (
    build_observation_crossmodal_association_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_diagnostics_v1 import (
    build_observation_manager_diagnostics_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_evidence_intake_v1 import (
    build_observation_evidence_intake_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_evidence_quality_v1 import (
    build_observation_evidence_quality_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_module_input_adapter_v1 import (
    adapt_observation_manager_input_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_module_output_builder_v1 import (
    build_observation_manager_module_output_v1,
    resolve_observation_manager_module_status_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_ocr_adapter_v1 import (
    build_observation_ocr_request_candidate_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_region_coordinator_v1 import (
    build_observation_region_plan_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_request_classifier_v1 import (
    build_observation_request_classification_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_scene_context_binder_v1 import (
    bind_observation_scene_context_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_task_context_binder_v1 import (
    bind_observation_task_context_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_temporal_snapshot_v1 import (
    build_observation_temporal_snapshot_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_trace_replay_v1 import (
    build_observation_manager_trace_replay_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_vision_adapter_v1 import (
    build_observation_vision_request_candidate_v1,
)


def run_observation_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    try:
        input_candidate = adapt_observation_manager_input_v1(payload)
        request_classification = build_observation_request_classification_v1(
            input_candidate
        )
        task_context = bind_observation_task_context_v1(input_candidate)
        scene_context = bind_observation_scene_context_v1(input_candidate)
        attention_plan = build_observation_attention_plan_v1(input_candidate)
        region_plan = build_observation_region_plan_v1(input_candidate, attention_plan)
        temporal_snapshot = build_observation_temporal_snapshot_v1(input_candidate)
        vision_adapter = build_observation_vision_request_candidate_v1(
            input_candidate,
            task_context,
            scene_context,
            attention_plan,
            region_plan,
        )
        ocr_adapter = build_observation_ocr_request_candidate_v1(
            input_candidate,
            task_context,
            scene_context,
            region_plan,
        )
        evidence_intake = build_observation_evidence_intake_v1(input_candidate)
        crossmodal = build_observation_crossmodal_association_v1(evidence_intake)
        evidence_quality = build_observation_evidence_quality_v1(
            input_candidate,
            evidence_intake,
            crossmodal,
        )

        module_status = resolve_observation_manager_module_status_v1(
            input_candidate,
            request_classification,
            task_context,
            temporal_snapshot,
            vision_adapter,
            ocr_adapter,
            evidence_intake,
            evidence_quality,
        )
        trace_replay = build_observation_manager_trace_replay_v1(
            input_candidate, module_status
        )

        observation_candidate = None
        admission_handoff = None
        rejection_reasons: list[str] = []

        if module_status in {
            "observation_candidate_ready",
            "degraded",
            "attention_plan_ready",
        }:
            observation_candidate = build_observation_candidate_v1(
                input_candidate,
                scene_context,
                region_plan,
                evidence_intake,
                crossmodal,
                temporal_snapshot,
                evidence_quality,
                str(trace_replay.get("trace_ref") or ""),
                str(trace_replay.get("replay_key") or ""),
            )
            admission_handoff = build_observation_admission_handoff_candidate_v1(
                input_candidate,
                observation_candidate,
                str(trace_replay.get("trace_ref") or ""),
            )
            module_status = "admission_handoff_ready"
        else:
            if module_status != "admission_handoff_ready":
                rejection_reasons.append(module_status)

        diagnostics = build_observation_manager_diagnostics_v1(
            input_candidate,
            module_status,
            evidence_intake,
            crossmodal,
            evidence_quality,
        )
        output = build_observation_manager_module_output_v1(
            input_candidate,
            module_status,
            task_context,
            scene_context,
            attention_plan,
            region_plan,
            vision_adapter,
            ocr_adapter,
            evidence_intake,
            crossmodal,
            temporal_snapshot,
            evidence_quality,
            observation_candidate,
            admission_handoff,
            diagnostics,
            str(trace_replay.get("trace_ref") or ""),
            str(trace_replay.get("replay_key") or ""),
            tuple(rejection_reasons),
        )
        output.update(
            {
                "request_classification": request_classification,
                "task_context": task_context,
                "scene_context": scene_context,
                "trace_replay": trace_replay,
                "unhandled_exception": False,
            }
        )
        return output
    except Exception:  # noqa: BLE001
        return {
            "capability_id": "luna.observation_manager",
            "module_status": "internal_error",
            "observation_request_id": "",
            "request_type": "",
            "task_context_ref": "",
            "scene_context_ref": "",
            "attention_plan": None,
            "region_plan": None,
            "vision_request_candidate": None,
            "ocr_request_candidate": None,
            "vision_evidence_refs": (),
            "ocr_evidence_refs": (),
            "crossmodal_associations": (),
            "temporal_snapshot": {},
            "evidence_quality": {},
            "observation_candidate": None,
            "permission_admission_handoff_candidate": None,
            "diagnostics": {
                "schema_version": "observation_manager_diagnostics_v1",
                "module_status": "internal_error",
            },
            "trace_ref": "",
            "replay_key": "",
            "rejection_reasons": ("internal_error",),
            "boundary_flags": {},
            "unhandled_exception": True,
        }
