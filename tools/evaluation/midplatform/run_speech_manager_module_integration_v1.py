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

from capabilities.midplatform.speech_manager.module.speech_manager_module_api_v1 import (
    run_speech_manager_module_v1,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "request_id": f"speech_mgr_req_{case_id}",
        "capability": "luna.speech_manager",
        "source_module": "luna.speech_manager",
        "source_ref": f"speech_source_{case_id}",
        "speech_text": "请先停稳，再继续。",
        "priority_level": "P2",
        "audio_input_kind": "text_candidate",
        "speaker_type": "registered_user",
        "speaker_identity_candidate": "speaker_001",
        "speech_gate_required": True,
        "asr_requested": True,
        "tts_requested": True,
        "vop_requested": True,
        "interruption_intent_type": "STOP",
        "resume_requested": False,
        "repeat_requested": False,
        "content_policy_ref": "speech_content_governance_v1",
        "trace_hint": f"trace_{case_id}",
        "replay_hint": f"replay_{case_id}",
        "context": {"scene_hash": f"scene_{case_id}"},
    }


def _boundary_flags_false(result: Mapping[str, Any]) -> bool:
    required_false = (
        "real_asr_invoked",
        "real_tts_invoked",
        "real_speech_gate_invoked",
        "real_vop_invoked",
    )
    return all(result.get(flag) is False for flag in required_false)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    scenarios["valid_candidate"] = _base_payload("valid_candidate")

    missing_text = _base_payload("missing_text")
    missing_text["speech_text"] = ""
    scenarios["missing_text"] = missing_text

    missing_request = _base_payload("missing_request")
    missing_request["request_id"] = ""
    scenarios["missing_request"] = missing_request

    safety = _base_payload("safety_priority")
    safety["priority_level"] = "P0"
    safety["interruption_intent_type"] = "EMERGENCY"
    scenarios["safety_priority"] = safety

    clarify = _base_payload("clarify_priority")
    clarify["priority_level"] = "P4"
    clarify["interruption_intent_type"] = "CLARIFY"
    scenarios["clarify_priority"] = clarify

    repeat_case = _base_payload("repeat_case")
    repeat_case["interruption_intent_type"] = "REPEAT"
    repeat_case["repeat_requested"] = True
    scenarios["repeat_case"] = repeat_case

    resume_case = _base_payload("resume_case")
    resume_case["interruption_intent_type"] = "RESUME"
    resume_case["resume_requested"] = True
    scenarios["resume_case"] = resume_case

    speaker_candidate = _base_payload("speaker_candidate")
    speaker_candidate["speaker_identity_candidate"] = "speaker_unconfirmed"
    speaker_candidate["speaker_type"] = "candidate_voice"
    scenarios["speaker_candidate"] = speaker_candidate

    asr_candidate = _base_payload("asr_candidate")
    asr_candidate["audio_input_kind"] = "audio_stream"
    asr_candidate["speech_text"] = "音频候选"
    scenarios["asr_candidate"] = asr_candidate

    tts_candidate = _base_payload("tts_candidate")
    tts_candidate["tts_requested"] = True
    tts_candidate["speech_text"] = "这是一条候选播报。"
    scenarios["tts_candidate"] = tts_candidate

    gate_required = _base_payload("gate_required")
    gate_required["speech_gate_required"] = True
    scenarios["gate_required"] = gate_required

    no_gate = _base_payload("no_gate")
    no_gate["speech_gate_required"] = False
    scenarios["no_gate"] = no_gate

    fact_risk = _base_payload("fact_risk")
    fact_risk["speech_text"] = "已经确认到达。"
    scenarios["fact_risk"] = fact_risk

    unknown_intent = _base_payload("unknown_intent")
    unknown_intent["interruption_intent_type"] = "UNKNOWN_OR_AMBIGUOUS"
    scenarios["unknown_intent"] = unknown_intent

    real_runtime_forbidden = _base_payload("real_runtime_forbidden")
    real_runtime_forbidden["requested_real_runtime"] = True
    scenarios["real_runtime_forbidden"] = real_runtime_forbidden

    real_tts_forbidden = _base_payload("real_tts_forbidden")
    real_tts_forbidden["requested_real_tts"] = True
    scenarios["real_tts_forbidden"] = real_tts_forbidden

    deterministic_a = _base_payload("deterministic_replay")
    scenarios["deterministic_replay"] = deterministic_a

    deterministic_b = _base_payload("deterministic_replay")
    scenarios["deterministic_replay_repeat"] = deterministic_b

    final_boundary = _base_payload("final_boundary")
    final_boundary["requested_real_vop"] = False
    final_boundary["requested_real_runtime"] = False
    scenarios["final_boundary"] = final_boundary

    rows = []
    failed_cases = []
    deterministic_replay = True
    trace_present_all = True
    replay_present_all = True
    boundary_preserved = True
    speaker_identity_auto_confirmed_false = True
    asr_candidate_auto_fact_false = True
    admitted_nonempty_text = True

    deterministic_trace_ref = None
    deterministic_replay_key = None
    first_deterministic_result = None

    for case_id, payload in scenarios.items():
        result = run_speech_manager_module_v1(payload)

        if case_id == "deterministic_replay":
            first_deterministic_result = result
        elif (
            case_id == "deterministic_replay_repeat"
            and first_deterministic_result is not None
        ):
            deterministic_replay = deterministic_replay and (
                first_deterministic_result.get("trace_ref") == result.get("trace_ref")
                and first_deterministic_result.get("replay_key")
                == result.get("replay_key")
            )
            deterministic_trace_ref = first_deterministic_result.get("trace_ref")
            deterministic_replay_key = first_deterministic_result.get("replay_key")

        if not result.get("trace_ref"):
            trace_present_all = False
        if not result.get("replay_key"):
            replay_present_all = False
        if not _boundary_flags_false(result):
            boundary_preserved = False

        diagnostics = result.get("diagnostics") or {}
        if diagnostics.get("speaker_identity_auto_confirmed") is True:
            speaker_identity_auto_confirmed_false = False
        if diagnostics.get("asr_candidate_auto_fact") is True:
            asr_candidate_auto_fact_false = False
        if case_id in {
            "valid_candidate",
            "safety_priority",
            "clarify_priority",
            "repeat_case",
            "resume_case",
            "speaker_candidate",
            "asr_candidate",
            "tts_candidate",
            "gate_required",
            "no_gate",
            "fact_risk",
            "unknown_intent",
            "final_boundary",
        }:
            if not result.get("governance", {}).get(
                "admitted", False
            ) and case_id not in {
                "missing_text",
                "missing_request",
                "real_runtime_forbidden",
                "real_tts_forbidden",
            }:
                admitted_nonempty_text = False

        case_pass = True
        if case_id in {
            "missing_text",
            "missing_request",
            "real_runtime_forbidden",
            "real_tts_forbidden",
        }:
            case_pass = result.get("governance", {}).get("admitted") is False
        else:
            case_pass = case_pass and bool(result.get("governance", {}).get("admitted"))
        if not result.get("result_summary"):
            case_pass = False
        if not result.get("module_status"):
            case_pass = False
        if not _boundary_flags_false(result):
            case_pass = False
        if not result.get("trace_ref") or not result.get("replay_key"):
            case_pass = False
        if case_id == "deterministic_replay_repeat" and not deterministic_replay:
            case_pass = False

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "module_status": result.get("module_status"),
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
                "admitted": result.get("governance", {}).get("admitted"),
                "selected_action_candidate": result.get("interruption_plan", {}).get(
                    "selected_action_candidate"
                ),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-Speech-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "deterministic_replay": deterministic_replay,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "boundary_preserved": boundary_preserved,
        "speaker_identity_auto_confirmed_false": speaker_identity_auto_confirmed_false,
        "asr_candidate_auto_fact_false": asr_candidate_auto_fact_false,
        "admitted_nonempty_text": admitted_nonempty_text,
        "rows": rows,
        "deterministic_trace_ref": deterministic_trace_ref,
        "deterministic_replay_key": deterministic_replay_key,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and deterministic_replay
        and trace_present_all
        and replay_present_all
        and boundary_preserved
        and speaker_identity_auto_confirmed_false
        and asr_candidate_auto_fact_false,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/speech_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "speech_manager_module_integration_v1.json"
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
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "boundary_preserved": report["boundary_preserved"],
                "speaker_identity_auto_confirmed_false": report[
                    "speaker_identity_auto_confirmed_false"
                ],
                "asr_candidate_auto_fact_false": report[
                    "asr_candidate_auto_fact_false"
                ],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
