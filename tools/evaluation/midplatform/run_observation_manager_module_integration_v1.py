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

from capabilities.midplatform.observation_manager.module.observation_manager_module_api_v1 import (
    run_observation_manager_module_v1,
)
from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "observation_request_id": f"obs_req_{case_id}",
        "request_type": "task_driven",
        "task_id": f"task_{case_id}",
        "task_context": {
            "task_context_ref": f"task_ctx_{case_id}",
            "subject_ref": "operator_a",
            "subject_refs": ["operator_a"],
        },
        "scene_context": {
            "scene_context_ref": f"scene_ctx_{case_id}",
            "scene_id": f"scene_{case_id}",
        },
        "attention_targets": ["front_path", "text_zone"],
        "region_hints": ["region_front", "region_sign"],
        "temporal_snapshot": {
            "temporal_snapshot_ref": f"ts_{case_id}",
            "frame_time": "2026-07-16T10:00:00Z",
        },
        "source_constraints": {
            "evidence_sufficient": True,
            "conflicting_evidence": False,
        },
        "vision_requested": True,
        "ocr_requested": True,
        "human_correction_refs": [],
        "permission_context": {
            "owner_ref": "observation_manager",
            "consent_ref": {"status": "granted"},
            "policy_snapshot": {},
            "risk_context": {},
        },
        "version_snapshot": {"observation_manager": "v1"},
        "trace_context": {"case_id": case_id},
        "vision_evidence_refs": [f"vision_ev_{case_id}"],
        "ocr_evidence_refs": [f"ocr_ev_{case_id}"],
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(k) is False for k in BOUNDARY_FALSE_FIELDS)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    b1 = _base_payload("baseline_safety_visual_request")
    b1["request_type"] = "baseline_safety"
    scenarios["baseline_safety_visual_request"] = b1

    b2 = _base_payload("task_driven_visual_request")
    b2["request_type"] = "task_driven"
    scenarios["task_driven_visual_request"] = b2

    b3 = _base_payload("navigation_support_request")
    b3["request_type"] = "navigation_support"
    scenarios["navigation_support_request"] = b3

    b4 = _base_payload("find_object_request")
    b4["request_type"] = "find_object"
    scenarios["find_object_request"] = b4

    b5 = _base_payload("find_text_request")
    b5["request_type"] = "find_text"
    scenarios["find_text_request"] = b5

    b6 = _base_payload("read_text_request")
    b6["request_type"] = "read_text"
    scenarios["read_text_request"] = b6

    b7 = _base_payload("scene_understanding_request")
    b7["request_type"] = "scene_understanding"
    scenarios["scene_understanding_request"] = b7

    b8 = _base_payload("passive_observation_request")
    b8["request_type"] = "passive_observation"
    b8["attention_targets"] = []
    b8["vision_requested"] = False
    b8["ocr_requested"] = False
    b8["vision_evidence_refs"] = []
    b8["ocr_evidence_refs"] = []
    scenarios["passive_observation_request"] = b8

    b9 = _base_payload("verification_observation_request")
    b9["request_type"] = "verification_observation"
    scenarios["verification_observation_request"] = b9

    b10 = _base_payload("human_correction_review_request")
    b10["request_type"] = "human_correction_review"
    b10["human_correction_refs"] = ["hc_001"]
    scenarios["human_correction_review_request"] = b10

    b11 = _base_payload("vision_only_evidence")
    b11["ocr_requested"] = False
    b11["ocr_evidence_refs"] = []
    scenarios["vision_only_evidence"] = b11

    b12 = _base_payload("ocr_only_evidence")
    b12["vision_requested"] = False
    b12["vision_evidence_refs"] = []
    scenarios["ocr_only_evidence"] = b12

    b13 = _base_payload("vision_ocr_crossmodal_evidence")
    scenarios["vision_ocr_crossmodal_evidence"] = b13

    b14 = _base_payload("partial_evidence")
    b14["vision_evidence_refs"] = []
    scenarios["partial_evidence"] = b14

    b15 = _base_payload("insufficient_evidence")
    b15["vision_evidence_refs"] = []
    b15["ocr_evidence_refs"] = []
    b15["source_constraints"] = {"evidence_sufficient": False}
    scenarios["insufficient_evidence"] = b15

    b16 = _base_payload("conflicting_evidence")
    b16["source_constraints"] = {
        "conflicting_evidence": True,
        "evidence_sufficient": True,
    }
    scenarios["conflicting_evidence"] = b16

    b17 = _base_payload("missing_task_context")
    b17["task_context"] = {}
    scenarios["missing_task_context"] = b17

    b18 = _base_payload("missing_temporal_snapshot")
    b18["temporal_snapshot"] = {}
    scenarios["missing_temporal_snapshot"] = b18

    b19 = _base_payload("invalid_request_type")
    b19["request_type"] = "unknown_observation"
    scenarios["invalid_request_type"] = b19

    b20 = _base_payload("deterministic_replay")
    scenarios["deterministic_replay"] = b20

    expected_status = {
        "baseline_safety_visual_request": "admission_handoff_ready",
        "task_driven_visual_request": "admission_handoff_ready",
        "navigation_support_request": "admission_handoff_ready",
        "find_object_request": "admission_handoff_ready",
        "find_text_request": "admission_handoff_ready",
        "read_text_request": "admission_handoff_ready",
        "scene_understanding_request": "admission_handoff_ready",
        "passive_observation_request": "no_observation_required",
        "verification_observation_request": "admission_handoff_ready",
        "human_correction_review_request": "admission_handoff_ready",
        "vision_only_evidence": "admission_handoff_ready",
        "ocr_only_evidence": "admission_handoff_ready",
        "vision_ocr_crossmodal_evidence": "admission_handoff_ready",
        "partial_evidence": "evidence_partial",
        "insufficient_evidence": "evidence_insufficient",
        "conflicting_evidence": "evidence_conflicted",
        "missing_task_context": "context_incomplete",
        "missing_temporal_snapshot": "context_incomplete",
        "invalid_request_type": "invalid_input",
        "deterministic_replay": "admission_handoff_ready",
    }

    observation_candidate_expected = {
        "baseline_safety_visual_request",
        "task_driven_visual_request",
        "navigation_support_request",
        "find_object_request",
        "find_text_request",
        "read_text_request",
        "scene_understanding_request",
        "verification_observation_request",
        "human_correction_review_request",
        "vision_only_evidence",
        "ocr_only_evidence",
        "vision_ocr_crossmodal_evidence",
        "deterministic_replay",
    }

    rows = []
    failed_cases = []
    diagnostics_present_all = True
    trace_present_all = True
    replay_present_all = True
    boundary_preserved = True
    deterministic_replay = True
    unhandled_exceptions = 0
    observation_candidate_present_when_expected = True
    attention_plan_present_when_expected = True
    vision_request_candidate_present_when_expected = True
    ocr_request_candidate_present_when_expected = True
    crossmodal_association_present_when_expected = True
    admission_handoff_present_when_expected = True

    for case_id, payload in scenarios.items():
        try:
            result = run_observation_manager_module_v1(payload)
        except Exception:  # noqa: BLE001
            result = {"module_status": "internal_error"}
            unhandled_exceptions += 1

        module_status = str(result.get("module_status") or "")
        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        if case_id in observation_candidate_expected and not isinstance(
            result.get("observation_candidate"), dict
        ):
            observation_candidate_present_when_expected = False
        if case_id in {
            "baseline_safety_visual_request",
            "task_driven_visual_request",
            "navigation_support_request",
            "find_object_request",
            "find_text_request",
            "read_text_request",
            "scene_understanding_request",
            "verification_observation_request",
        } and not isinstance(result.get("attention_plan"), dict):
            attention_plan_present_when_expected = False

        if (
            case_id in observation_candidate_expected
            and case_id != "ocr_only_evidence"
            and not isinstance(result.get("vision_request_candidate"), dict)
        ):
            vision_request_candidate_present_when_expected = False
        if (
            case_id in observation_candidate_expected
            and case_id != "vision_only_evidence"
            and not isinstance(result.get("ocr_request_candidate"), dict)
        ):
            ocr_request_candidate_present_when_expected = False

        if case_id in {
            "vision_ocr_crossmodal_evidence",
            "deterministic_replay",
        } and not (
            isinstance(result.get("crossmodal_associations"), tuple)
            and len(result.get("crossmodal_associations") or ()) > 0
        ):
            crossmodal_association_present_when_expected = False

        if case_id in observation_candidate_expected and not isinstance(
            result.get("permission_admission_handoff_candidate"), dict
        ):
            admission_handoff_present_when_expected = False

        case_pass = module_status == expected_status[case_id]
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)

        if case_id == "deterministic_replay":
            rerun = run_observation_manager_module_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("trace_ref") == rerun.get("trace_ref")
                and result.get("replay_key") == rerun.get("replay_key")
                and result.get("module_status") == rerun.get("module_status")
            )
            case_pass = case_pass and deterministic_replay

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "expected_status": expected_status[case_id],
                "module_status": module_status,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-Observation-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "observation_candidate_present_when_expected": observation_candidate_present_when_expected,
        "attention_plan_present_when_expected": attention_plan_present_when_expected,
        "vision_request_candidate_present_when_expected": vision_request_candidate_present_when_expected,
        "ocr_request_candidate_present_when_expected": ocr_request_candidate_present_when_expected,
        "crossmodal_association_present_when_expected": crossmodal_association_present_when_expected,
        "admission_handoff_present_when_expected": admission_handoff_present_when_expected,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "deterministic_replay": deterministic_replay,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and observation_candidate_present_when_expected
        and attention_plan_present_when_expected
        and vision_request_candidate_present_when_expected
        and ocr_request_candidate_present_when_expected
        and crossmodal_association_present_when_expected
        and admission_handoff_present_when_expected
        and diagnostics_present_all
        and trace_present_all
        and replay_present_all
        and deterministic_replay
        and boundary_preserved
        and unhandled_exceptions == 0,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/observation_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "observation_manager_module_integration_v1.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "observation_candidate_present_when_expected": report[
                    "observation_candidate_present_when_expected"
                ],
                "attention_plan_present_when_expected": report[
                    "attention_plan_present_when_expected"
                ],
                "vision_request_candidate_present_when_expected": report[
                    "vision_request_candidate_present_when_expected"
                ],
                "ocr_request_candidate_present_when_expected": report[
                    "ocr_request_candidate_present_when_expected"
                ],
                "crossmodal_association_present_when_expected": report[
                    "crossmodal_association_present_when_expected"
                ],
                "admission_handoff_present_when_expected": report[
                    "admission_handoff_present_when_expected"
                ],
                "diagnostics_present_all": report["diagnostics_present_all"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "deterministic_replay": report["deterministic_replay"],
                "boundary_preserved": report["boundary_preserved"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
