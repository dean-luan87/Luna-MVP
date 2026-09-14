#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_handoff_api_v1 import (  # noqa: E402
    run_field_perception_visual_handoff_integration_v1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_visual_invocation_contract_v1 import (  # noqa: E402
    BOUNDARY_FALSE_FIELDS,
)


def _base_request(case_id: str) -> Dict[str, Any]:
    return {
        "field_perception_visual_handoff_request": {
            "handoff_request_id": f"handoff_req_{case_id}",
            "field_perception_plan": {
                "plan_id": f"fp_plan_{case_id}",
                "task_id": f"task_{case_id}",
                "field_snapshot_ref": f"field_snapshot_{case_id}",
                "observation_goal": "confirm_navigable_space_ahead",
                "information_gap": ("front_space_unknown",),
                "target_region": "front_corridor",
                "target_entity_types": ("obstacle", "walkable_surface"),
                "requested_visual_capabilities": (
                    "detection",
                    "segmentation",
                    "depth",
                ),
                "preferred_model_candidates": ("vision_general_v2",),
                "fallback_model_candidates": ("seg_depth_v1",),
                "resolution_level": "standard",
                "temporal_window": "normal",
                "observation_priority": "normal",
                "confidence_requirement": 0.82,
                "stop_condition": {"rule": "min_sufficient_evidence"},
                "reobserve_condition": {"rule": "on_stale_or_conflict"},
                "expected_evidence_types": (
                    "detection_box",
                    "segmentation_mask",
                    "depth_hint",
                ),
            },
            "task_context": {"task_id": f"task_{case_id}"},
            "field_snapshot_ref": f"field_snapshot_{case_id}",
            "information_gap_ref": f"gap_ref_{case_id}",
            "observation_goal": "confirm_navigable_space_ahead",
            "target_region": "front_corridor",
            "target_entity_types": ("obstacle", "walkable_surface"),
            "requested_visual_capabilities": ("detection", "segmentation", "depth"),
            "preferred_model_candidates": ("vision_general_v2",),
            "fallback_model_candidates": ("seg_depth_v1",),
            "resolution_level": "standard",
            "temporal_window": "normal",
            "observation_priority": "normal",
            "confidence_requirement": 0.82,
            "expected_evidence_types": (
                "detection_box",
                "segmentation_mask",
                "depth_hint",
            ),
            "stop_condition": {"rule": "min_sufficient_evidence"},
            "reobserve_condition": {"rule": "on_stale_or_conflict"},
            "available_visual_capabilities": (
                "detection",
                "segmentation",
                "depth",
                "ocr",
                "tracking",
            ),
            "available_model_assets": (
                {
                    "model_id": "vision_general_v2",
                    "supports": ("detection", "tracking"),
                },
                {"model_id": "seg_depth_v1", "supports": ("segmentation", "depth")},
                {"model_id": "ocr_reader_v1", "supports": ("ocr",)},
            ),
            "model_manager_snapshot": {"source": "model_manager_module_v1"},
            "resource_budget": {
                "latency_budget_ms": 1500,
                "memory_budget_mb": 2048,
                "compute_budget_units": 2,
                "power_budget": 2,
                "concurrent_invocation_limit": 2,
                "preferred_model_classes": ("teacher", "tool"),
                "fallback_model_classes": ("tool",),
            },
            "invocation_history": tuple(),
            "permission_context": {"request_rejected": False, "conflicted": False},
            "version_snapshot": {"capability": "v1"},
            "trace_context": {"phase": "field_perception_visual_handoff"},
            "vision_required": True,
        }
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(field) is False for field in BOUNDARY_FALSE_FIELDS)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    c1 = _base_request("sufficient_no_visual")
    c1["field_perception_visual_handoff_request"]["vision_required"] = False
    scenarios["sufficient_field_information_no_visual_request"] = c1

    c2 = _base_request("stale_obstacle")
    scenarios["stale_obstacle_evidence_detection_request"] = c2

    c3 = _base_request("find_entrance")
    c3["field_perception_visual_handoff_request"]["observation_goal"] = (
        "locate_entrance"
    )
    c3["field_perception_visual_handoff_request"]["requested_visual_capabilities"] = (
        "detection",
        "ocr",
    )
    scenarios["find_entrance_detection_and_ocr"] = c3

    c4 = _base_request("read_notice")
    c4["field_perception_visual_handoff_request"]["observation_goal"] = (
        "read_text_notice"
    )
    c4["field_perception_visual_handoff_request"]["requested_visual_capabilities"] = (
        "ocr",
    )
    scenarios["read_notice_ocr_only"] = c4

    c5 = _base_request("traffic_unknown")
    c5["field_perception_visual_handoff_request"]["observation_goal"] = (
        "confirm_traffic_light_state"
    )
    c5["field_perception_visual_handoff_request"]["requested_visual_capabilities"] = (
        "detection",
        "tracking",
    )
    scenarios["unknown_traffic_light_detection_tracking"] = c5

    c6 = _base_request("dup_active")
    c6["field_perception_visual_handoff_request"]["invocation_history"] = (
        {
            "handoff_id": "handoff_old_active",
            "task_id": c6["field_perception_visual_handoff_request"]["task_context"][
                "task_id"
            ],
            "field_snapshot_ref": c6["field_perception_visual_handoff_request"][
                "field_snapshot_ref"
            ],
            "information_gap_ref": c6["field_perception_visual_handoff_request"][
                "information_gap_ref"
            ],
            "observation_goal": c6["field_perception_visual_handoff_request"][
                "observation_goal"
            ],
            "target_region": c6["field_perception_visual_handoff_request"][
                "target_region"
            ],
            "requested_visual_capabilities": c6[
                "field_perception_visual_handoff_request"
            ]["requested_visual_capabilities"],
            "active": True,
            "fresh_evidence_available": False,
        },
    )
    scenarios["duplicate_active_invocation_suppressed"] = c6

    c7 = _base_request("fresh_reuse")
    c7["field_perception_visual_handoff_request"]["invocation_history"] = (
        {
            "handoff_id": "handoff_old_fresh",
            "task_id": c7["field_perception_visual_handoff_request"]["task_context"][
                "task_id"
            ],
            "field_snapshot_ref": c7["field_perception_visual_handoff_request"][
                "field_snapshot_ref"
            ],
            "information_gap_ref": c7["field_perception_visual_handoff_request"][
                "information_gap_ref"
            ],
            "observation_goal": c7["field_perception_visual_handoff_request"][
                "observation_goal"
            ],
            "target_region": c7["field_perception_visual_handoff_request"][
                "target_region"
            ],
            "requested_visual_capabilities": c7[
                "field_perception_visual_handoff_request"
            ]["requested_visual_capabilities"],
            "active": False,
            "fresh_evidence_available": True,
        },
    )
    scenarios["fresh_evidence_reused"] = c7

    c8 = _base_request("constrained_budget")
    c8["field_perception_visual_handoff_request"]["resource_budget"].update(
        {
            "memory_budget_mb": 1200,
            "compute_budget_units": 1,
            "concurrent_invocation_limit": 1,
        }
    )
    scenarios["constrained_budget_degradation"] = c8

    c9 = _base_request("critical_budget")
    c9["field_perception_visual_handoff_request"]["resource_budget"].update(
        {
            "memory_budget_mb": 512,
            "compute_budget_units": 0,
            "power_budget": 0,
            "concurrent_invocation_limit": 0,
        }
    )
    scenarios["critical_budget_minimum_safety_plan"] = c9

    c10 = _base_request("high_risk_priority")
    c10["field_perception_visual_handoff_request"]["observation_priority"] = "high"
    scenarios["high_risk_priority_escalation"] = c10

    c11 = _base_request("no_eligible_model")
    c11["field_perception_visual_handoff_request"]["resource_budget"].update(
        {"preferred_model_classes": ("non_existing_class",)}
    )
    scenarios["no_eligible_model"] = c11

    c12 = _base_request("not_admitted")
    c12["field_perception_visual_handoff_request"]["resource_budget"].update(
        {"forbidden_model_ids": ("detection_v1", "ocr_v1", "slam_v1", "qwen_vl")}
    )
    scenarios["model_not_admitted_rejected"] = c12

    c13 = _base_request("roi_missing_global")
    c13["field_perception_visual_handoff_request"]["target_region"] = ""
    scenarios["roi_missing_global_observation_candidate"] = c13

    c14 = _base_request("ocr_ownership")
    c14["field_perception_visual_handoff_request"]["observation_goal"] = (
        "read_text_notice"
    )
    c14["field_perception_visual_handoff_request"]["requested_visual_capabilities"] = (
        "ocr",
    )
    c14["field_perception_visual_handoff_request"]["expected_evidence_types"] = (
        "ocr_text",
    )
    scenarios["ocr_region_ownership_supplement"] = c14

    c15 = _base_request("obs_ready")
    scenarios["observation_manager_handoff_ready"] = c15

    c16 = _base_request("deterministic")
    scenarios["deterministic_replay"] = c16

    failed_cases = []
    rows = []

    no_visual_request_when_not_required = True
    vision_request_present_when_expected = True
    model_requirement_present_when_expected = True
    eligible_model_binding_correct = True
    rejected_model_binding_correct = True
    deduplication_correct = True
    budget_degradation_correct = True
    observation_request_present_when_expected = True
    result_link_contract_present_when_expected = True
    field_snapshot_ref_preserved_all = True
    information_gap_ref_preserved_all = True
    diagnostics_present_all = True
    trace_present_all = True
    replay_present_all = True
    deterministic_replay = True
    boundary_preserved = True
    unhandled_exceptions = 0

    expect_no_visual = {"sufficient_field_information_no_visual_request"}
    expect_dedup_suppressed = {"duplicate_active_invocation_suppressed"}
    expect_fresh_reuse = {"fresh_evidence_reused"}
    expect_budget_degraded = {
        "constrained_budget_degradation",
        "critical_budget_minimum_safety_plan",
    }
    expect_no_eligible = {"no_eligible_model", "model_not_admitted_rejected"}

    for case_id, payload in scenarios.items():
        result = run_field_perception_visual_handoff_integration_v1(payload)
        if bool(result.get("unhandled_exception", False)):
            unhandled_exceptions += 1

        integration_status = str(result.get("integration_status") or "")
        vision_request = result.get("vision_request_candidate")
        model_requirement = result.get("model_requirement_candidate")
        eligible_models = tuple(result.get("eligible_model_candidates") or ())
        rejected_models = tuple(result.get("rejected_model_candidates") or ())
        obs_req = result.get("observation_request_candidate")
        dedup = dict(result.get("deduplication_result") or {})
        budget = dict(result.get("budget_decision") or {})
        result_link = result.get("result_link_contract")

        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False
        if str(result.get("field_snapshot_ref") or "") != str(
            payload["field_perception_visual_handoff_request"].get("field_snapshot_ref")
            or ""
        ):
            field_snapshot_ref_preserved_all = False
        if str(result.get("information_gap_ref") or "") != str(
            payload["field_perception_visual_handoff_request"].get(
                "information_gap_ref"
            )
            or ""
        ):
            information_gap_ref_preserved_all = False

        if case_id in expect_no_visual:
            if (
                integration_status != "no_visual_invocation_required"
                or vision_request is not None
            ):
                no_visual_request_when_not_required = False
        else:
            if (
                integration_status
                not in {
                    "duplicate_suppressed",
                    "fresh_evidence_reused",
                    "no_eligible_model",
                    "budget_degraded",
                    "handoff_ready",
                }
                and vision_request is None
            ):
                vision_request_present_when_expected = False

        if (
            case_id
            not in expect_no_visual | expect_dedup_suppressed | expect_fresh_reuse
        ):
            if not isinstance(model_requirement, dict):
                model_requirement_present_when_expected = False

        if case_id in expect_no_eligible:
            if integration_status != "no_eligible_model":
                eligible_model_binding_correct = False
            if len(eligible_models) != 0 or len(rejected_models) == 0:
                rejected_model_binding_correct = False
        elif (
            case_id
            not in expect_no_visual | expect_dedup_suppressed | expect_fresh_reuse
        ):
            if len(eligible_models) == 0:
                eligible_model_binding_correct = False

        if case_id in expect_dedup_suppressed:
            if (
                integration_status != "duplicate_suppressed"
                or str(dedup.get("deduplication_status") or "")
                != "duplicate_active_request"
            ):
                deduplication_correct = False
        if case_id in expect_fresh_reuse:
            if (
                integration_status != "fresh_evidence_reused"
                or str(dedup.get("deduplication_status") or "")
                != "fresh_evidence_reuse"
            ):
                deduplication_correct = False

        if case_id in expect_budget_degraded:
            if integration_status != "budget_degraded":
                budget_degradation_correct = False
            if str(
                (budget.get("budget_decision") or {}).get("budget_level") or ""
            ) not in {"constrained", "critical"}:
                budget_degradation_correct = False

        if (
            case_id
            not in expect_no_visual
            | expect_dedup_suppressed
            | expect_fresh_reuse
            | expect_no_eligible
        ):
            if not isinstance(obs_req, dict):
                observation_request_present_when_expected = False
            if not isinstance(result_link, dict):
                result_link_contract_present_when_expected = False

        case_pass = True
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)

        if case_id in expect_no_visual:
            case_pass = (
                case_pass and integration_status == "no_visual_invocation_required"
            )
        if case_id in expect_dedup_suppressed:
            case_pass = case_pass and integration_status == "duplicate_suppressed"
        if case_id in expect_fresh_reuse:
            case_pass = case_pass and integration_status == "fresh_evidence_reused"
        if case_id in expect_no_eligible:
            case_pass = case_pass and integration_status == "no_eligible_model"
        if case_id in expect_budget_degraded:
            case_pass = case_pass and integration_status == "budget_degraded"
        if case_id == "observation_manager_handoff_ready":
            case_pass = case_pass and integration_status == "handoff_ready"

        if case_id == "deterministic_replay":
            rerun = run_field_perception_visual_handoff_integration_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("trace_ref") == rerun.get("trace_ref")
                and result.get("replay_key") == rerun.get("replay_key")
                and result.get("integration_status") == rerun.get("integration_status")
            )
            case_pass = case_pass and deterministic_replay

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "integration_status": integration_status,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    report = {
        "phase": "Phase-Luna-Field-Perception-Orchestrator-Controlled-Visual-Invocation-Handoff-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "no_visual_request_when_not_required": no_visual_request_when_not_required,
        "vision_request_present_when_expected": vision_request_present_when_expected,
        "model_requirement_present_when_expected": model_requirement_present_when_expected,
        "eligible_model_binding_correct": eligible_model_binding_correct,
        "rejected_model_binding_correct": rejected_model_binding_correct,
        "deduplication_correct": deduplication_correct,
        "budget_degradation_correct": budget_degradation_correct,
        "observation_request_present_when_expected": observation_request_present_when_expected,
        "result_link_contract_present_when_expected": result_link_contract_present_when_expected,
        "field_snapshot_ref_preserved_all": field_snapshot_ref_preserved_all,
        "information_gap_ref_preserved_all": information_gap_ref_preserved_all,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "deterministic_replay": deterministic_replay,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
    }
    report["integration_pass"] = (
        report["total_cases"] == 16
        and report["passed_cases"] == 16
        and report["failed_cases"] == []
        and report["deterministic_replay"] is True
        and report["diagnostics_present_all"] is True
        and report["trace_present_all"] is True
        and report["replay_present_all"] is True
        and report["boundary_preserved"] is True
        and report["unhandled_exceptions"] == 0
    )
    return report


def main() -> int:
    report = run_integration()
    out_dir = Path(
        "_tmp_eval_out/field_perception_visual_handoff_integration_v1_smoke_v0"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "field_perception_visual_handoff_integration_v1.json"
    out_file.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "deterministic_replay": report["deterministic_replay"],
                "diagnostics_present_all": report["diagnostics_present_all"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "boundary_preserved": report["boundary_preserved"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(out_file.resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
