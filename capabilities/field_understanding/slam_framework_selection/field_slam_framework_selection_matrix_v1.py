# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — evidence-based matrix v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    validate_framework_selection_matrix_v1,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_types_v1 import (
    FINAL_DECISION_MATRIX_READY,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SELECTION_STRATEGY_NOTE,
    SELECTION_STRATEGY_NOTE_ZH,
    SLAMFrameworkCandidate,
    SLAMFrameworkEvaluation,
    SLAMFrameworkSelectionDecision,
    candidate_to_dict,
)

_STUB = ("framework_matrix_stub_v1",)


def build_framework_candidates_v1() -> Tuple[SLAMFrameworkCandidate, ...]:
    return (
        SLAMFrameworkCandidate(
            framework_ref="openvins",
            framework_name="OpenVINS",
            framework_group="vio_pose_first",
            open_source_status="open_source",
            license_type="gpl_3",
            license_risk="high",
            commercial_modification_risk="high",
            primary_role_for_luna="Pose / Motion / Health technical baseline",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="p0",
            observation_priority="p0",
            source_refs=_STUB + ("openvins_repo_ref",),
            notes=(
                "Internal technical reference for PoseCandidate and MotionCandidate.",
                "GPL license blocks commercial_runtime_candidate without license gate.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="vins_fusion",
            framework_name="VINS-Fusion",
            framework_group="vio_pose_first",
            open_source_status="open_source",
            license_type="gpl_v3",
            license_risk="high",
            commercial_modification_risk="high",
            primary_role_for_luna="Multi-sensor VIO technical reference",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="p0",
            observation_priority="p0",
            source_refs=_STUB + ("vins_fusion_repo_ref",),
            notes=(
                "Multi-sensor VIO reference; complements OpenVINS for fusion patterns.",
                "Not a commercial runtime candidate under current license posture.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="orb_slam3",
            framework_name="ORB-SLAM3",
            framework_group="visual_inertial_slam",
            open_source_status="open_source",
            license_type="gpl_v3",
            license_risk="high",
            commercial_modification_risk="high",
            primary_role_for_luna="Relocalization / LocalMap / Multi-map reference",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="p1",
            observation_priority="p1",
            source_refs=_STUB + ("orb_slam3_repo_ref",),
            notes=(
                "Strong relocalization and local map reference; P1 not P0 due to mapping weight vs pose-first need.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="rtab_map",
            framework_name="RTAB-Map",
            framework_group="graph_rgbd_slam",
            open_source_status="open_source",
            license_type="bsd_conditional",
            license_risk="medium",
            commercial_modification_risk="medium",
            primary_role_for_luna="RGB-D / graph-based local map reference",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="p2",
            observation_priority="p2",
            source_refs=_STUB + ("rtab_map_repo_ref",),
            notes=(
                "Graph RGB-D local map reference; P2 due to mapping-first profile.",
                "License more permissive but still not auto commercial runtime.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="kimera",
            framework_name="Kimera",
            framework_group="metric_semantic_slam",
            open_source_status="open_source",
            license_type="bsd",
            license_risk="low",
            commercial_modification_risk="medium",
            primary_role_for_luna="Metric-semantic map / semantic mesh observation",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="observation",
            observation_priority="p1",
            source_refs=_STUB + ("kimera_repo_ref",),
            notes=(
                "Permissive license but engineering-heavy; observation line not runtime P0.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="hydra",
            framework_name="Hydra",
            framework_group="metric_semantic_scene_graph",
            open_source_status="open_source",
            license_type="bsd_2_clause",
            license_risk="low",
            commercial_modification_risk="medium",
            primary_role_for_luna="Real-time 3D scene graph / Field Graph reference",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="observation",
            observation_priority="p1",
            source_refs=_STUB + ("hydra_repo_ref",),
            notes=(
                "Scene graph reference for Field Graph alignment; not runtime SLAM substitute.",
            ),
        ),
        SLAMFrameworkCandidate(
            framework_ref="grapheqa",
            framework_name="GraphEQA",
            framework_group="embodied_scene_graph_qa",
            open_source_status="paper_with_code",
            license_type="unknown",
            license_risk="unknown",
            commercial_modification_risk="unknown",
            primary_role_for_luna="Metric-semantic scene graph + task memory observation",
            technical_reference_candidate=True,
            commercial_runtime_candidate=False,
            runtime_priority="observation",
            observation_priority="p1",
            source_refs=_STUB + ("grapheqa_paper_ref",),
            notes=(
                "Observation line only; must not enter runtime SLAM framework selection.",
            ),
        ),
    )


def build_framework_evaluations_v1() -> Tuple[SLAMFrameworkEvaluation, ...]:
    return (
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_openvins",
            framework_ref="openvins",
            pose_candidate_fit="high",
            motion_candidate_fit="high",
            spatial_anchor_fit="medium",
            local_map_fit="low",
            slam_health_fit="high",
            map_drift_fit="medium",
            relocalization_fit="medium",
            field_synthesis_fit="high",
            wearable_fit="high",
            runtime_weight="light",
            engineering_risk="medium",
            semantic_extension_fit="low",
            static_dynamic_split_fit="medium",
            action_semantic_map_fit="low",
            recommended_priority="p0",
            rationale=(
                "Best P0 technical fit for Pose/Motion/Health evidence chain.",
                "Lightweight enough for wearable-first Luna profile.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_vins_fusion",
            framework_ref="vins_fusion",
            pose_candidate_fit="high",
            motion_candidate_fit="high",
            spatial_anchor_fit="medium",
            local_map_fit="low",
            slam_health_fit="high",
            map_drift_fit="medium",
            relocalization_fit="medium",
            field_synthesis_fit="high",
            wearable_fit="medium",
            runtime_weight="medium",
            engineering_risk="medium",
            semantic_extension_fit="low",
            static_dynamic_split_fit="medium",
            action_semantic_map_fit="low",
            recommended_priority="p0",
            rationale=(
                "Strong multi-sensor VIO reference for Motion and Health candidates.",
                "P0 technical alongside OpenVINS; not mapping-first selection.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_orb_slam3",
            framework_ref="orb_slam3",
            pose_candidate_fit="medium",
            motion_candidate_fit="medium",
            spatial_anchor_fit="medium",
            local_map_fit="high",
            slam_health_fit="medium",
            map_drift_fit="high",
            relocalization_fit="high",
            field_synthesis_fit="medium",
            wearable_fit="low",
            runtime_weight="heavy",
            engineering_risk="high",
            semantic_extension_fit="low",
            static_dynamic_split_fit="medium",
            action_semantic_map_fit="low",
            recommended_priority="p1",
            rationale=(
                "Strong LocalMap and Relocalization reference; P1 not P0.",
                "Selected for relocalization patterns, not as primary pose baseline.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_rtab_map",
            framework_ref="rtab_map",
            pose_candidate_fit="medium",
            motion_candidate_fit="low",
            spatial_anchor_fit="medium",
            local_map_fit="high",
            slam_health_fit="medium",
            map_drift_fit="high",
            relocalization_fit="medium",
            field_synthesis_fit="medium",
            wearable_fit="low",
            runtime_weight="heavy",
            engineering_risk="medium",
            semantic_extension_fit="medium",
            static_dynamic_split_fit="high",
            action_semantic_map_fit="medium",
            recommended_priority="p2",
            rationale=(
                "Graph RGB-D local map reference; P2 mapping profile.",
                "Not P0 because Luna P0 needs pose/motion evidence first.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_kimera",
            framework_ref="kimera",
            pose_candidate_fit="medium",
            motion_candidate_fit="medium",
            spatial_anchor_fit="medium",
            local_map_fit="high",
            slam_health_fit="medium",
            map_drift_fit="medium",
            relocalization_fit="medium",
            field_synthesis_fit="medium",
            wearable_fit="low",
            runtime_weight="heavy",
            engineering_risk="high",
            semantic_extension_fit="high",
            static_dynamic_split_fit="high",
            action_semantic_map_fit="high",
            recommended_priority="observation",
            rationale=(
                "Metric-semantic observation for action-semantic map research.",
                "Permissive license but too heavy for P0 runtime binding.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_hydra",
            framework_ref="hydra",
            pose_candidate_fit="low",
            motion_candidate_fit="low",
            spatial_anchor_fit="medium",
            local_map_fit="medium",
            slam_health_fit="low",
            map_drift_fit="medium",
            relocalization_fit="medium",
            field_synthesis_fit="high",
            wearable_fit="low",
            runtime_weight="heavy",
            engineering_risk="high",
            semantic_extension_fit="high",
            static_dynamic_split_fit="high",
            action_semantic_map_fit="high",
            recommended_priority="observation",
            rationale=(
                "Real-time scene graph reference for Field Graph alignment.",
                "Observation line; not a substitute for Pose/Motion evidence provider.",
            ),
        ),
        SLAMFrameworkEvaluation(
            evaluation_ref="eval_grapheqa",
            framework_ref="grapheqa",
            pose_candidate_fit="low",
            motion_candidate_fit="low",
            spatial_anchor_fit="medium",
            local_map_fit="medium",
            slam_health_fit="not_applicable",
            map_drift_fit="not_applicable",
            relocalization_fit="low",
            field_synthesis_fit="medium",
            wearable_fit="unknown",
            runtime_weight="unknown",
            engineering_risk="unknown",
            semantic_extension_fit="high",
            static_dynamic_split_fit="medium",
            action_semantic_map_fit="high",
            recommended_priority="observation",
            rationale=(
                "Embodied scene graph QA observation for metric-semantic binding research.",
                "Must not be treated as runtime SLAM framework.",
            ),
        ),
    )


def build_framework_selection_decision_v1() -> SLAMFrameworkSelectionDecision:
    return SLAMFrameworkSelectionDecision(
        decision_ref="slam_framework_selection_decision_v1",
        recommended_p0_technical=("openvins", "vins_fusion"),
        recommended_p0_commercial_safe=(),
        recommended_p1=("orb_slam3",),
        recommended_p2=("rtab_map",),
        recommended_observation=("kimera", "hydra", "grapheqa"),
        deferred=(),
        blocked=(),
        rationale_refs=(
            "eval_openvins",
            "eval_vins_fusion",
            "eval_orb_slam3",
            "eval_rtab_map",
            "eval_kimera",
            "eval_hydra",
            "eval_grapheqa",
        ),
        license_gate_required=True,
        adapter_contract_required=True,
        final_decision=FINAL_DECISION_MATRIX_READY,
    )


def build_framework_selection_matrix_v1() -> Dict[str, Any]:
    frameworks = build_framework_candidates_v1()
    evaluations = build_framework_evaluations_v1()
    decision = build_framework_selection_decision_v1()
    return {
        "frameworks": [candidate_to_dict(f) for f in frameworks],
        "evaluations": [candidate_to_dict(e) for e in evaluations],
        "decision": candidate_to_dict(decision),
    }


def summarize_framework_selection_matrix_v1() -> Dict[str, Any]:
    matrix = build_framework_selection_matrix_v1()
    matrix_ok, matrix_issues = validate_framework_selection_matrix_v1(matrix)
    decision = matrix["decision"]

    gpl_commercial_blocked = all(
        not f.get("commercial_runtime_candidate")
        for f in matrix["frameworks"]
        if f.get("license_type") in ("gpl_3", "gpl_v3")
    )
    grapheqa = next(f for f in matrix["frameworks"] if f["framework_ref"] == "grapheqa")
    grapheqa_runtime_blocked = (
        grapheqa.get("runtime_priority") == "observation"
        and grapheqa.get("commercial_runtime_candidate") is False
    )
    p0_technical = list(decision.get("recommended_p0_technical") or ())
    p0_commercial_safe = list(decision.get("recommended_p0_commercial_safe") or ())
    p0_technical_ok = p0_technical == ["openvins", "vins_fusion"]
    p0_commercial_safe_empty_ok = len(p0_commercial_safe) == 0

    import_ok = True
    try:
        framework_count = len(matrix["frameworks"])
        evaluation_count = len(matrix["evaluations"])
    except Exception:
        import_ok = False
        framework_count = 0
        evaluation_count = 0

    decision_ok = (
        matrix_ok
        and decision.get("final_decision") == FINAL_DECISION_MATRIX_READY
        and decision.get("license_gate_required") is True
        and decision.get("adapter_contract_required") is True
    )

    ready = (
        import_ok
        and framework_count == 7
        and evaluation_count == 7
        and len(VALIDATOR_RULE_IDS) == 15
        and matrix_ok
        and gpl_commercial_blocked
        and grapheqa_runtime_blocked
        and p0_technical_ok
        and p0_commercial_safe_empty_ok
        and decision_ok
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Evidence-Based Framework Matrix",
        "selection_strategy_note": SELECTION_STRATEGY_NOTE,
        "selection_strategy_note_zh": SELECTION_STRATEGY_NOTE_ZH,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "import_ok": import_ok,
        "framework_count": framework_count,
        "evaluation_count": evaluation_count,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "matrix_validation_ok": matrix_ok,
        "matrix_validation_issues": matrix_issues,
        "gpl_runtime_blocked": gpl_commercial_blocked,
        "grapheqa_runtime_blocked": grapheqa_runtime_blocked,
        "p0_technical_ok": p0_technical_ok,
        "p0_commercial_safe_empty_ok": p0_commercial_safe_empty_ok,
        "decision_ok": decision_ok,
        "recommended_p0_technical": p0_technical,
        "recommended_p0_commercial_safe": p0_commercial_safe,
        "recommended_p1": list(decision.get("recommended_p1") or ()),
        "recommended_p2": list(decision.get("recommended_p2") or ()),
        "recommended_observation": list(decision.get("recommended_observation") or ()),
        "license_gate_required": decision.get("license_gate_required"),
        "adapter_contract_required": decision.get("adapter_contract_required"),
        "final_decision": FINAL_DECISION_MATRIX_READY if ready else "FIELD_SLAM_FRAMEWORK_SELECTION_MATRIX_BLOCKED",
    }


def main() -> int:
    summary = summarize_framework_selection_matrix_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["final_decision"] == FINAL_DECISION_MATRIX_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
