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

from capabilities.midplatform.ocr_manager.module.ocr_manager_module_api_v1 import (
    run_ocr_manager_module_v1,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "request_id": f"ocr_mgr_req_{case_id}",
        "capability": "luna.ocr_manager",
        "request_type": "task_ocr_request",
        "source_ref": f"synthetic_source_{case_id}",
        "source_kind": "synthetic_fixture",
        "frame_ref": f"frame_{case_id}",
        "task_ocr_request": {
            "task_id": f"task_{case_id}",
            "scope": "text_region",
            "preferred_engine": "rapidocr",
        },
        "visual_region_candidates": [
            {"region_id": "region_text_0", "region_type": "text_region"},
            {"region_id": "poster_region_0", "region_type": "poster_region"},
        ],
        "poster_region_candidates": [],
        "human_correction_input": [],
        "synthetic_integration_fixture": {
            "text_items": [
                {
                    "raw_text": "EXIT 2F",
                    "normalized_text_candidate": "EXIT 2F",
                    "confidence": 0.92,
                    "language": "en",
                    "bbox": {"x1": 20, "y1": 10, "x2": 180, "y2": 40},
                    "region_ref": "region_text_0",
                    "line_ref": "line_0",
                }
            ]
        },
        "crossmodal_context": {
            "expected_text": "EXIT",
            "known_entity_candidate": "exit",
        },
    }


def _assert_boundary_flags(result: Mapping[str, Any]) -> bool:
    required_false = (
        "fact_admission_executed",
        "state_mutation_executed",
        "action_execution_executed",
        "navigation_decision_executed",
        "speech_output_executed",
        "database_write_executed",
        "provider_recall_executed",
        "external_lookup_executed",
        "model_training_executed",
        "production_runtime_executed",
    )
    return all(bool(result.get(flag)) is False for flag in required_false)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    scenarios["valid_raw_text_evidence"] = _base_payload("valid_raw_text_evidence")

    no_text = _base_payload("no_text_detected")
    no_text["synthetic_integration_fixture"] = {"text_items": []}
    scenarios["no_text_detected"] = no_text

    missing_source = _base_payload("missing_source_ref")
    missing_source["source_ref"] = ""
    scenarios["missing_source_ref"] = missing_source

    invalid_region = _base_payload("invalid_region")
    invalid_region["task_ocr_request"] = {
        "task_id": "task_invalid_region",
        "scope": "invalid_scope",
    }
    scenarios["invalid_region"] = invalid_region

    engine_unavailable = _base_payload("engine_unavailable")
    engine_unavailable["synthetic_integration_fixture"]["force_engine_unavailable"] = (
        True
    )
    scenarios["engine_unavailable"] = engine_unavailable

    low_conf = _base_payload("low_confidence_text")
    low_conf["synthetic_integration_fixture"]["text_items"][0]["confidence"] = 0.2
    scenarios["low_confidence_text"] = low_conf

    stylized = _base_payload("stylized_text_candidate")
    stylized["synthetic_integration_fixture"]["text_items"][0]["raw_text"] = "S*LE"
    scenarios["stylized_text_candidate"] = stylized

    mixed_lang = _base_payload("mixed_language_candidate")
    mixed_lang["synthetic_integration_fixture"]["text_items"][0]["raw_text"] = (
        "出口 EXIT"
    )
    mixed_lang["synthetic_integration_fixture"]["text_items"][0]["language"] = "zh-en"
    scenarios["mixed_language_candidate"] = mixed_lang

    punctuation = _base_payload("punctuation_ambiguity")
    punctuation["synthetic_integration_fixture"]["text_items"][0]["raw_text"] = (
        "Floor 2"
    )
    scenarios["punctuation_ambiguity"] = punctuation

    occlusion = _base_payload("occlusion_completion_candidate")
    occlusion["synthetic_integration_fixture"]["text_items"][0]["raw_text"] = "RO?M 21"
    scenarios["occlusion_completion_candidate"] = occlusion

    multi_region = _base_payload("multi_region_attribution")
    multi_region["synthetic_integration_fixture"]["text_items"].append(
        {
            "raw_text": "Lobby",
            "normalized_text_candidate": "Lobby",
            "confidence": 0.75,
            "language": "en",
            "bbox": {"x1": 30, "y1": 70, "x2": 120, "y2": 95},
            "region_ref": "poster_region_0",
            "line_ref": "line_1",
        }
    )
    scenarios["multi_region_attribution"] = multi_region

    unresolved_region = _base_payload("unresolved_region_attribution")
    unresolved_region["synthetic_integration_fixture"]["text_items"][0][
        "region_ref"
    ] = "region_unknown"
    scenarios["unresolved_region_attribution"] = unresolved_region

    normal_order = _base_payload("normal_reading_order")
    scenarios["normal_reading_order"] = normal_order

    ambiguous_order = _base_payload("ambiguous_reading_order")
    ambiguous_order["synthetic_integration_fixture"]["text_items"].append(
        {
            "raw_text": "Gate B",
            "normalized_text_candidate": "Gate B",
            "confidence": 0.8,
            "language": "en",
            "bbox": {"x1": 220, "y1": 10, "x2": 360, "y2": 45},
            "region_ref": "region_text_0",
            "line_ref": "line_1",
        }
    )
    scenarios["ambiguous_reading_order"] = ambiguous_order

    crossmodal_ok = _base_payload("crossmodal_consistent")
    crossmodal_ok["crossmodal_context"] = {
        "expected_text": "exit",
        "known_entity_candidate": "exit",
    }
    scenarios["crossmodal_consistent"] = crossmodal_ok

    crossmodal_conflict = _base_payload("crossmodal_conflict")
    crossmodal_conflict["crossmodal_context"] = {
        "expected_text": "bank",
        "known_entity_candidate": "bank",
    }
    scenarios["crossmodal_conflict"] = crossmodal_conflict

    correction = _base_payload("human_correction_candidate")
    correction["human_correction_input"] = [
        {
            "original_ocr_ref": "ocr_raw_ocr_mgr_req_human_correction_candidate_0",
            "correction_target": "text_block",
            "correction_type": "manual_text_update",
            "corrected_text_candidate": "EXIT 2F WEST",
            "user_correction_source": "review_ui",
            "reviewer_candidate": "operator_1",
            "correction_confidence": 0.93,
        }
    ]
    scenarios["human_correction_candidate"] = correction

    deterministic = _base_payload("deterministic_replay")
    scenarios["deterministic_replay"] = deterministic

    rows = []
    failed_cases = []
    deterministic_replay = True
    evidence_envelope_present_all = True
    trace_present_all = True
    replay_present_all = True
    raw_evidence_preserved = True
    boundary_preserved = True

    deterministic_trace = None
    deterministic_replay_key = None
    for case_id, payload in scenarios.items():
        result = run_ocr_manager_module_v1(payload)
        if case_id == "deterministic_replay":
            second = run_ocr_manager_module_v1(payload)
            deterministic_trace = result.get("trace_ref")
            deterministic_replay_key = result.get("replay_key")
            deterministic_replay = (
                deterministic_replay
                and deterministic_trace == second.get("trace_ref")
                and deterministic_replay_key == second.get("replay_key")
            )

        case_pass = True
        if not isinstance(result.get("evidence_envelope"), dict):
            case_pass = False
            evidence_envelope_present_all = False
        if not str(result.get("trace_ref") or ""):
            case_pass = False
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            case_pass = False
            replay_present_all = False
        if len(result.get("raw_evidence") or []) > 0:
            if any(
                not str(item.get("raw_text") or "")
                for item in (result.get("raw_evidence") or [])
            ):
                case_pass = False
                raw_evidence_preserved = False
        if not _assert_boundary_flags(result):
            case_pass = False
            boundary_preserved = False

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "module_status": result.get("module_status"),
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-OCR-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "deterministic_replay": deterministic_replay,
        "evidence_envelope_present_all": evidence_envelope_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "raw_evidence_preserved": raw_evidence_preserved,
        "boundary_preserved": boundary_preserved,
        "rows": rows,
        "deterministic_trace_ref": deterministic_trace,
        "deterministic_replay_key": deterministic_replay_key,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and deterministic_replay
        and evidence_envelope_present_all
        and trace_present_all
        and replay_present_all
        and raw_evidence_preserved
        and boundary_preserved,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/ocr_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "ocr_manager_module_integration_v1.json"
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
                "deterministic_replay": report["deterministic_replay"],
                "evidence_envelope_present_all": report[
                    "evidence_envelope_present_all"
                ],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "raw_evidence_preserved": report["raw_evidence_preserved"],
                "boundary_preserved": report["boundary_preserved"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
