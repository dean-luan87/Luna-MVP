# -*- coding: utf-8 -*-
"""Field Synthesis Map Place / Event Overlay Dry-Run — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.field_synthesis_map_place_event_overlay_dryrun.field_synthesis_map_place_event_overlay_dryrun_cases_v1 import (
    build_negative_cases_v1,
    build_positive_cases_v1,
    evaluate_positive_case,
    synthesize_field_decision_v1,
    validate_input_bundle_for_synthesis,
)
from capabilities.field_understanding.field_synthesis_map_place_event_overlay_dryrun.field_synthesis_map_place_event_overlay_dryrun_types_v1 import (
    DRYRUN_PRINCIPLE_ZH,
    FIELD_ALIGNMENT_REF,
    FIELD_DEFINITION_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_DRYRUN_BLOCKED,
    FINAL_DECISION_DRYRUN_GO,
    INTERFACE_LAYER_PROTOCOL_REF,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NEGATIVE_CASE_REFS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    SPATIAL_EVIDENCE_CHAIN_REF,
    SPATIAL_ODOMETRY_FUSION_REF,
    TARGET_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "field_synthesis_map_place_event_overlay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "field_synthesis_map_place_event_overlay_dryrun_run_and_review_v1.json"

_UPSTREAM_ARTIFACTS = (
    {
        "phase_ref": FIELD_ALIGNMENT_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_map_place_event_overlay_alignment_v1_smoke_v0/"
            "field_map_place_event_overlay_alignment_review_v1.json"
        ),
        "expected_go": "FIELD_MAP_PLACE_REALTIME_EVENT_OVERLAY_ALIGNMENT_READY_FOR_SYNTHESIS_DRYRUN",
    },
    {
        "phase_ref": SPATIAL_EVIDENCE_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
    },
)


def _verify_upstream_sealed() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for entry in _UPSTREAM_ARTIFACTS:
        path = _REPO_ROOT / entry["artifact_rel"]
        if not path.is_file():
            issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append(f"upstream_artifact_unreadable:{entry['phase_ref']}")
            continue
        if data.get("final_decision") != entry["expected_go"]:
            issues.append(
                f"upstream_go_mismatch:{entry['phase_ref']}:{data.get('final_decision')!r}"
            )
    return len(issues) == 0, issues


def run_and_review_field_synthesis_map_place_event_overlay_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    positive_cases = list(build_positive_cases_v1())
    negative_cases = list(build_negative_cases_v1())

    positive_traces: List[Dict[str, Any]] = []
    positive_results: List[Dict[str, Any]] = []
    positive_pass_count = 0

    for case in positive_cases:
        bundle = case["input_bundle"]
        trace = synthesize_field_decision_v1(bundle)
        ok, eval_issues = evaluate_positive_case(trace, case["case_ref"])
        positive_traces.append(trace)
        positive_results.append(
            {
                "case_ref": case["case_ref"],
                "synthesis_ok": trace.get("synthesis_ok"),
                "evaluation_ok": ok,
                "evaluation_issues": eval_issues,
            }
        )
        if ok:
            positive_pass_count += 1

    negative_results: List[Dict[str, Any]] = []
    invalid_expected_reject_count = 0

    for case in negative_cases:
        bundle = case["input_bundle"]
        valid, validation_issues = validate_input_bundle_for_synthesis(bundle)
        trace = synthesize_field_decision_v1(bundle)
        rejected = (not valid) or (not trace.get("synthesis_ok"))
        negative_results.append(
            {
                "case_ref": case["case_ref"],
                "validation_ok": valid,
                "validation_issues": validation_issues,
                "synthesis_ok": trace.get("synthesis_ok"),
                "rejected_as_expected": rejected,
            }
        )
        if rejected:
            invalid_expected_reject_count += 1

    upstream_ok, upstream_issues = _verify_upstream_sealed()

    traces_by_case = {t["case_ref"]: t for t in positive_traces}
    mall_trace = traces_by_case.get("mall_stable_map_place_with_slam") or {}
    subway_trace = traces_by_case.get("subway_station_indoor_gps_degraded") or {}
    stadium_trace = traces_by_case.get("stadium_concert_event_overlay") or {}
    plaza_trace = traces_by_case.get("plaza_temporary_market_realtime_overlay") or {}
    conflict_trace = traces_by_case.get("gps_slam_map_place_conflict") or {}

    review_checkpoints: Dict[str, Any] = {
        "positive_case_count": len(positive_cases),
        "negative_case_count": len(negative_cases),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "mall_stable_field_synthesized": (
            mall_trace.get("synthesis_ok") is True
            and (mall_trace.get("field_state_candidate") or {}).get("field_state")
            == "stable_map_place_field"
        ),
        "subway_gps_degraded_slam_local_field_ok": (
            subway_trace.get("synthesis_ok") is True
            and (subway_trace.get("field_candidate") or {}).get("gps_weight") == "degraded"
            and (subway_trace.get("field_candidate") or {}).get("slam_local_weight") == "high"
        ),
        "stadium_concert_event_overlay_label_ok": (
            stadium_trace.get("synthesis_ok") is True
            and (stadium_trace.get("field_interaction_label_candidate") or {}).get("field_label")
            == "演唱会现场"
            and (stadium_trace.get("field_interaction_label_candidate") or {}).get(
                "underlying_map_place_ref"
            )
            == "stadium_stub"
        ),
        "plaza_temporary_market_overlay_ok": (
            plaza_trace.get("synthesis_ok") is True
            and (plaza_trace.get("field_interaction_label_candidate") or {}).get("field_label")
            == "临时集市"
        ),
        "gps_slam_conflict_candidate_emitted": bool(
            conflict_trace.get("field_conflict_candidate")
        ),
        "event_overlay_does_not_rewrite_map_place": all(
            (t.get("field_candidate") or {}).get("underlying_map_place_ref")
            == (t.get("field_interaction_label_candidate") or {}).get("underlying_map_place_ref")
            for t in positive_traces
            if t.get("case_ref") in (
                "stadium_concert_event_overlay",
                "plaza_temporary_market_realtime_overlay",
            )
        ),
        "field_interaction_label_separated": all(
            (t.get("field_interaction_label_candidate") or {}).get("internal_field_state_ref")
            for t in positive_traces
        ),
        "spatial_evidence_binding_used": any(
            (t.get("field_candidate") or {}).get("spatial_binding_used") for t in positive_traces
        ),
        "candidate_only_enforced": all(
            (t.get("field_candidate") or {}).get("candidate_only") is True
            and (t.get("field_candidate") or {}).get("direct_action_allowed") is not True
            for t in positive_traces
        ),
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "real_map_api_connected": False,
        "real_gps_connected": False,
        "real_event_api_connected": False,
        "runtime_activation_allowed": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "upstream_sealed_verified": upstream_ok,
    }

    failed_checks: List[str] = []
    if not upstream_ok:
        failed_checks.extend(upstream_issues)
    if positive_pass_count != 5:
        failed_checks.append(f"positive_pass_count:{positive_pass_count}")
    if invalid_expected_reject_count != 4:
        failed_checks.append(f"invalid_expected_reject_count:{invalid_expected_reject_count}")

    go_flags = {
        "positive_case_count_eq_5": review_checkpoints["positive_case_count"] == 5,
        "negative_case_count_eq_4": review_checkpoints["negative_case_count"] == 4,
        "positive_pass_count_eq_5": review_checkpoints["positive_pass_count"] == 5,
        "invalid_expected_reject_count_eq_4": review_checkpoints[
            "invalid_expected_reject_count"
        ]
        == 4,
        "mall_stable_field_synthesized": review_checkpoints["mall_stable_field_synthesized"],
        "subway_gps_degraded_slam_local_field_ok": review_checkpoints[
            "subway_gps_degraded_slam_local_field_ok"
        ],
        "stadium_concert_event_overlay_label_ok": review_checkpoints[
            "stadium_concert_event_overlay_label_ok"
        ],
        "plaza_temporary_market_overlay_ok": review_checkpoints["plaza_temporary_market_overlay_ok"],
        "gps_slam_conflict_candidate_emitted": review_checkpoints[
            "gps_slam_conflict_candidate_emitted"
        ],
        "event_overlay_does_not_rewrite_map_place": review_checkpoints[
            "event_overlay_does_not_rewrite_map_place"
        ],
        "field_interaction_label_separated": review_checkpoints["field_interaction_label_separated"],
        "spatial_evidence_binding_used": review_checkpoints["spatial_evidence_binding_used"],
        "candidate_only_enforced": review_checkpoints["candidate_only_enforced"],
        "field_synthesis_entrypoint_locked": review_checkpoints["field_synthesis_entrypoint_locked"]
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "real_event_api_connected_false": review_checkpoints["real_event_api_connected"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
    }

    for key, ok in go_flags.items():
        if not ok:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Field Synthesis Map Place / Event Overlay Dry-Run Run + Review",
        "lifecycle_variant": "compressed_field_synthesis_dryrun_review",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "model_binding": {
            "target_entrypoint": TARGET_ENTRYPOINT,
            "field_alignment_ref": FIELD_ALIGNMENT_REF,
            "spatial_evidence_chain_ref": SPATIAL_EVIDENCE_CHAIN_REF,
            "spatial_odometry_fusion_ref": SPATIAL_ODOMETRY_FUSION_REF,
            "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
            "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
            "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
            "field_definition_ref": FIELD_DEFINITION_REF,
        },
        "pipeline": [
            "FieldSynthesisInputBundle",
            "field_synthesis_v1 (dry-run synthesizer)",
            "FieldCandidate",
            "FieldStateCandidate",
            "FieldInteractionLabelCandidate",
            "FieldConflictCandidate (when conflict)",
        ],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "positive_case_results": positive_results,
        "negative_case_results": negative_results,
        "positive_traces": positive_traces,
        "review_checkpoints": review_checkpoints,
        "go_conditions": go_flags,
        "conclusions": {
            "field_synthesis_dryrun_status": "go" if review_ok else "blocked",
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "typical_scenarios_synthesized": list(POSITIVE_CASE_REFS),
            "recommended_next_step": (
                "Field → Task alignment: prove field judgment serves entry finding, "
                "obstacle avoidance, station entry, ticket check, go-home tasks"
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "final_decision": FINAL_DECISION_DRYRUN_GO if review_ok else FINAL_DECISION_DRYRUN_BLOCKED,
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_field_synthesis_map_place_event_overlay_dryrun_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_pass_count": checkpoints["positive_pass_count"],
                "invalid_expected_reject_count": checkpoints["invalid_expected_reject_count"],
                "mall_stable_field_synthesized": checkpoints["mall_stable_field_synthesized"],
                "gps_slam_conflict_candidate_emitted": checkpoints[
                    "gps_slam_conflict_candidate_emitted"
                ],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_DRYRUN_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
