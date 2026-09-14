from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_plan_v1(
    input_candidate: Mapping[str, Any],
    field_snapshot: Mapping[str, Any],
    observation_goal: Mapping[str, Any],
    information_gap: Mapping[str, Any],
    region_plan: Mapping[str, Any],
    capability_plan: Mapping[str, Any],
    model_requirements: Mapping[str, Any],
    resource_plan: Mapping[str, Any],
    stop_condition: Mapping[str, Any],
    reobservation_policy: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    expected_types = tuple(
        dict.fromkeys(
            [
                "detection_box"
                if "detection"
                in tuple(
                    resource_plan.get("requested_visual_capabilities_budgeted") or ()
                )
                else "",
                "segmentation_mask"
                if "segmentation"
                in tuple(
                    resource_plan.get("requested_visual_capabilities_budgeted") or ()
                )
                else "",
                "depth_hint"
                if "depth"
                in tuple(
                    resource_plan.get("requested_visual_capabilities_budgeted") or ()
                )
                else "",
                "ocr_text"
                if "ocr"
                in tuple(
                    resource_plan.get("requested_visual_capabilities_budgeted") or ()
                )
                else "",
                "tracklet"
                if "tracking"
                in tuple(
                    resource_plan.get("requested_visual_capabilities_budgeted") or ()
                )
                else "",
            ]
        )
    )
    expected_types = tuple(x for x in expected_types if x)

    return {
        "plan_id": f"fp_plan::{input_candidate.get('task_id')}::{trace_ref[-6:] if trace_ref else 'na'}",
        "task_id": input_candidate.get("task_id"),
        "field_snapshot_ref": field_snapshot.get("field_snapshot_ref"),
        "observation_goal": observation_goal.get("observation_goal"),
        "information_gap": tuple(information_gap.get("information_gap") or ()),
        "target_region": region_plan.get("target_region"),
        "target_entity_types": tuple(region_plan.get("target_entity_types") or ()),
        "requested_visual_capabilities": tuple(
            resource_plan.get("requested_visual_capabilities_budgeted") or ()
        ),
        "preferred_model_candidates": tuple(
            model_requirements.get("preferred_model_candidates") or ()
        ),
        "fallback_model_candidates": tuple(
            model_requirements.get("fallback_model_candidates") or ()
        ),
        "resolution_level": resource_plan.get("resolution_level"),
        "temporal_window": resource_plan.get("temporal_window"),
        "observation_priority": resource_plan.get("observation_priority"),
        "confidence_requirement": (stop_condition.get("stop_condition") or {}).get(
            "confidence_requirement"
        ),
        "stop_condition": stop_condition.get("stop_condition"),
        "reobserve_condition": reobservation_policy.get("reobserve_condition"),
        "expected_evidence_types": expected_types,
        "reasoning_summary": f"goal={observation_goal.get('observation_goal')}; gap_count={len(tuple(information_gap.get('information_gap') or ()))}; caps={','.join(tuple(resource_plan.get('requested_visual_capabilities_budgeted') or ())) or 'none'}",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
    }
