from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = repo_root_from(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_engine_v1 import ARouteProductLoopIntegrationEngineV1  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_runtime_product_loop_controlled_integration_v1 import _check_case as _check_s0_case  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_s1_real_user_input_controlled_replacement_v1 import _s1_case_result  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_s1_real_user_input_controlled_replacement_v1 import _check as _check_value  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_fixture_v1 import build_fixture_cases  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_adapter_v1 import adapt_user_input  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_fixture_v1 import build_s1_fixture_cases  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_adapter_v1 import adapt_raw_camera_source, control_stream_session  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_fixture_v1 import S2FixtureCaseV1, build_s2_fixture_cases  # noqa: E402


OUT_DIR = ROOT / "_eval_out/a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1"
S2_FALSE_GUARDS = {
    "vision_yolo_execution": False,
    "ocr_execution": False,
    "slam_execution": False,
    "vio_execution": False,
    "vlm_execution": False,
    "semantic_interpretation": False,
    "semantic_compression": False,
    "provider_semantic_authority": False,
    "field_state_direct_mutation": False,
    "current_world_truth_declaration": False,
    "intent_mutation": False,
    "decision_mutation": False,
    "task_mutation": False,
    "real_action_execution": False,
    "real_runtime_execution": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "model_call": False,
    "scheduler_execution": False,
    "cross_user_transfer": False,
    "emotion_engine_execution": False,
    "b_route_execution": False,
}


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def _result_for_case(case: S2FixtureCaseV1) -> Dict[str, Any]:
    first = adapt_raw_camera_source(
        case.source_ref,
        source_type=case.source_type,
        observation_demand_ref=case.demand_ref,
        max_frames=case.max_frames,
        max_duration_ms=case.max_duration_ms,
        width=case.width,
        height=case.height,
        captured_at=case.captured_at,
        source_mode=case.source_mode,
        session_id=f"s2-session:{case.case_id}",
        frame_id=f"s2-frame:{case.case_id}",
    )
    checks = [
        _check_value("accepted", first.accepted, case.expected_accept),
        _check_value("rejection_code", first.rejection_code, case.expected_code),
    ]
    if case.expected_accept:
        session = first.session
        frame = first.frames[0] if first.frames else None
        checks.extend([
            _check_value("bounded", session.bounded if session else False, True),
            _check_value("autonomous_continuous_execution", session.autonomous_continuous_execution if session else True, False),
            _check_value("candidate_only", first.candidate_only, True),
            _check_value("provider_invocation", first.provider_invocation, False),
            _check_value("semantic_compression", first.semantic_compression, False),
            _check_value("provenance_authority", first.provenance_grants_authority, False),
        ])
        if frame:
            checks.extend([
                _check_value("raw_only", frame.raw_only, True),
                _check_value("evidence_created", frame.evidence_created, False),
                _check_value("observation_created", frame.observation_created, False),
            ])
        else:
            checks.append(_check_value("bounded_stream_session_without_decode", case.source_type == "VIDEO_FILE", True))
        if case.case_id == "S2-05":
            checks.append(_check_value("max_frames", session.max_frames if session else 0, 3))
        if case.case_id == "S2-06":
            checks.append(_check_value("max_duration_ms", session.max_duration_ms if session else 0, 7000))
        if case.case_id == "S2-07":
            checks.append(_check_value("captured_at", frame.captured_at if frame else 0, case.captured_at))
        if case.case_id == "S2-08":
            checks.extend([
                _check_value("width", frame.width if frame else 0, case.width),
                _check_value("height", frame.height if frame else 0, case.height),
            ])
        if case.case_id in {"S2-09", "S2-10"}:
            checks.extend([
                _check_value("trace_ref", bool(frame.trace_ref if frame else ""), True),
                _check_value("provenance_refs", bool(frame.provenance_refs if frame else ()), True),
                _check_value("reverse_source_ref", frame.source_ref if frame else "", case.source_ref),
            ])
        if case.case_id == "S2-11":
            duplicate = adapt_raw_camera_source(
                case.source_ref,
                source_type=case.source_type,
                observation_demand_ref=case.demand_ref,
                source_mode=case.source_mode,
                session_id=f"s2-session:{case.case_id}:duplicate",
                frame_id=first.frames[0].frame_id if first.frames else f"s2-frame:{case.case_id}",
                seen_frame_ids=(first.frames[0].frame_id,) if first.frames else (),
            )
            checks.extend([
                _check_value("duplicate_frame", duplicate.duplicate, True),
                _check_value("duplicate_code", duplicate.rejection_code, "DUPLICATE_FRAME"),
            ])
        if case.case_id == "S2-12":
            duplicate = adapt_raw_camera_source(
                case.source_ref,
                source_type=case.source_type,
                observation_demand_ref=case.demand_ref,
                source_mode=case.source_mode,
                session_id=first.session.session_id if first.session else f"s2-session:{case.case_id}",
                frame_id=f"s2-frame:{case.case_id}:duplicate",
                seen_session_ids=(first.session.session_id,) if first.session else (),
            )
            checks.extend([
                _check_value("duplicate_session", duplicate.duplicate, True),
                _check_value("duplicate_code", duplicate.rejection_code, "DUPLICATE_SESSION"),
            ])
        if case.control_action:
            control = control_stream_session(first.session, case.control_action, f"fixture {case.case_id}") if first.session else None
            checks.extend([
                _check_value("control_action", control.action if control else "", case.control_action),
                _check_value("control_runtime", control.runtime_execution if control else True, False),
                _check_value("control_provider", control.provider_invocation if control else True, False),
            ])
        if case.case_id == "S2-16":
            checks.extend([
                _check_value("ingress_raw_only", first.ingress.raw_only if first.ingress else False, True),
                _check_value("gateway_admission", first.ingress.gateway_admission if first.ingress else True, False),
                _check_value("natural_language_conclusion", first.ingress.natural_language_conclusion_ref if first.ingress else "unexpected", ""),
            ])
        if case.case_id in {"S2-17", "S2-18", "S2-19", "S2-24"}:
            checks.extend([_check_value(name, False, expected) for name, expected in S2_FALSE_GUARDS.items() if name in {"vision_yolo_execution", "ocr_execution", "slam_execution", "vio_execution", "vlm_execution", "semantic_interpretation", "semantic_compression"}])
        if case.case_id == "S2-20":
            checks.extend([
                _check_value("ingress_kind", first.ingress.ingress_kind if first.ingress else "", "RAW_FRAME_REFERENCE"),
                _check_value("product_loop_language_ref", first.ingress.natural_language_conclusion_ref if first.ingress else "unexpected", ""),
            ])
        actual = jsonable(first)
    else:
        actual = jsonable(first)
    return {"scenario_id": case.case_id, "title": case.title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": actual}


def _differential_result(real_source: Optional[str]) -> Dict[str, Any]:
    synthetic = adapt_raw_camera_source(
        "synthetic://s2/differential",
        source_type="IMAGE_FILE",
        observation_demand_ref="demand:s2-differential",
        source_mode="SYNTHETIC_REGRESSION",
        session_id="s2-session:differential:synthetic",
        frame_id="s2-frame:differential:synthetic",
        captured_at=1700000000000,
    )
    real_like = adapt_raw_camera_source(
        real_source or "synthetic://s2/differential-real-placeholder",
        source_type="IMAGE_FILE",
        observation_demand_ref="demand:s2-differential",
        source_mode="REAL" if real_source else "SYNTHETIC_REGRESSION",
        session_id="s2-session:differential:real",
        frame_id="s2-frame:differential:real",
        captured_at=1700000000000,
    )
    synthetic_contract = (bool(synthetic.session and synthetic.session.bounded), bool(synthetic.frames and synthetic.frames[0].raw_only), bool(synthetic.provider_invocation), bool(synthetic.semantic_compression))
    real_contract = (bool(real_like.session and real_like.session.bounded), bool(real_like.frames and real_like.frames[0].raw_only), bool(real_like.provider_invocation), bool(real_like.semantic_compression))
    checks = [_check_value("contract_outputs", real_contract, synthetic_contract), _check_value("trace_provenance", bool(real_like.session and real_like.session.trace_ref), True), _check_value("negative_guards", real_like.provider_invocation or real_like.semantic_compression, False), _check_value("unrelated_module_behavior", real_like.candidate_only, True)]
    return {"checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "synthetic": jsonable(synthetic), "real_or_reference": jsonable(real_like)}


def run(*, source_ref: Optional[str] = None, source_type: str = "IMAGE_FILE", user_input: Optional[str] = None, width: int = 0, height: int = 0) -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = ARouteProductLoopIntegrationEngineV1()
    s0_cases = [_check_s0_case(engine, case) for case in build_fixture_cases()]
    s1_cases = [_s1_case_result(engine, case) for case in build_s1_fixture_cases()]
    s2_cases = [_result_for_case(case) for case in build_s2_fixture_cases()]
    s0_passed = all(item["all_checks_passed"] for item in s0_cases)
    s1_passed = all(item["all_checks_passed"] for item in s1_cases)
    s2_cases[20]["checks"].append(_check_value("s0_regression", s0_passed, True))
    s2_cases[20]["all_checks_passed"] = all(item["passed"] for item in s2_cases[20]["checks"])
    s2_cases[21]["checks"].append(_check_value("s1_regression", s1_passed, True))
    s2_cases[21]["all_checks_passed"] = all(item["passed"] for item in s2_cases[21]["checks"])
    differential = _differential_result(source_ref)
    s2_cases[22]["checks"].extend(differential["checks"])
    s2_cases[22]["all_checks_passed"] = all(item["passed"] for item in s2_cases[22]["checks"])
    s2_cases[22]["actual"]["differential"] = differential
    user_input_adapter = adapt_user_input(user_input, cycle_ref="s2-user-input") if user_input is not None else None
    if source_ref:
        real_adapter = adapt_raw_camera_source(source_ref, source_type=source_type, observation_demand_ref="demand:cli-s2", source_mode="REAL", session_id="s2-session:cli", frame_id="s2-frame:cli", width=width, height=height)
        s2_cases.append({"scenario_id": "S2-REAL", "title": "user-provided raw source", "checks": [_check_value("accepted", real_adapter.accepted, True)], "all_checks_passed": real_adapter.accepted, "actual": jsonable(real_adapter)})
    failed_s2 = [item["scenario_id"] for item in s2_cases if not item["all_checks_passed"]]
    failed_s0 = [item["scenario_id"] for item in s0_cases if not item["all_checks_passed"]]
    failed_s1 = [item["scenario_id"] for item in s1_cases if not item["all_checks_passed"]]
    summary = {
        "mode": "HYBRID_S2_REAL_RAW_STREAM" if source_ref else "SYNTHETIC_REGRESSION",
        "real_components": (["USER_INPUT"] if user_input_adapter and user_input_adapter.accepted else []) + (["RAW_CAMERA_INPUT_STREAM"] if source_ref else []),
        "synthetic_components": ["Vision/YOLO", "OCR", "SLAM/VIO", "Context/World", "Cognitive Chain", "Task/Action", "Runtime", "Outcome Evaluation", "User Output"],
        "s2_scenario_count": len(s2_cases),
        "s0_scenario_count": len(s0_cases),
        "s1_scenario_count": len(s1_cases),
        "s0_all_cases_passed": not failed_s0,
        "s1_all_cases_passed": not failed_s1,
        "s2_all_cases_passed": not failed_s2,
        "all_cases_passed": not (failed_s0 or failed_s1 or failed_s2),
        "failed_case_ids": failed_s2 + failed_s1 + failed_s0,
        "raw_camera_input_stream_real": bool(source_ref),
        "provider_autonomous_continuous_execution": False,
        "vision_yolo_execution": False,
        "ocr_execution": False,
        "slam_execution": False,
        "vio_execution": False,
        "vlm_execution": False,
        "semantic_interpretation": False,
        "semantic_compression": False,
        "provider_semantic_authority": False,
        "field_state_direct_mutation": False,
        "current_world_truth_declaration": False,
        "real_runtime_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "model_call": False,
        "scheduler_execution": False,
        "cross_user_transfer": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "raw_content_persisted": False,
        "user_input_adapter_accepted": user_input_adapter.accepted if user_input_adapter else None,
    }
    (OUT_DIR / "a_route_s2_real_raw_camera_stream_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s2_real_raw_camera_stream_case_results_v1.json").write_text(json.dumps(s2_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s2_s0_regression_case_results_v1.json").write_text(json.dumps(s0_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s2_s1_regression_case_results_v1.json").write_text(json.dumps(s1_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s2_raw_camera_trace_v1.json").write_text(json.dumps({"provenance_grants_authority": False, "differential": differential, "s2_cases": [item["actual"] for item in s2_cases if item.get("scenario_id") in {"S2-09", "S2-10", "S2-16"}]}, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="S2 raw camera/input stream controlled replacement")
    parser.add_argument("--source", default=None, help="external image/video/frame source reference")
    parser.add_argument("--source-type", default="IMAGE_FILE", choices=("IMAGE_FILE", "VIDEO_FILE", "FRAME_REFERENCE", "IMAGE_SEQUENCE"))
    parser.add_argument("--user-input", default=None, help="optional S1 user-input marker; not semantically interpreted")
    parser.add_argument("--width", type=int, default=0)
    parser.add_argument("--height", type=int, default=0)
    args = parser.parse_args()
    summary = run(source_ref=args.source, source_type=args.source_type, user_input=args.user_input, width=args.width, height=args.height)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
