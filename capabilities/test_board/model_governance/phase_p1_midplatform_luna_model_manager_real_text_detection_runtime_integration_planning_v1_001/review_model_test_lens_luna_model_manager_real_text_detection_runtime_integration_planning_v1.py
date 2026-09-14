# -*- coding: utf-8 -*-
"""P1 Luna Text Detection Runtime — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-Planning-v1-001"
TD_REL = "capabilities/midplatform/model_manager/runtime/text_detection"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TD_REL}/text_detection_runtime_plan_v1.md",
    f"{TD_REL}/text_detection_runtime_adapter_v1.py",
    f"{TD_REL}/text_detection_request_builder_v1.py",
    f"{TD_REL}/text_detection_response_parser_v1.py",
    f"{TD_REL}/text_detection_evidence_normalizer_v1.py",
    f"{TD_REL}/text_detection_runtime_policy_v1.json",
    f"{MM_REL}/luna_model_manager_text_detection_runtime_types_v1.py",
    f"{MM_REL}/luna_model_manager_text_detection_runtime_processor_v1.py",
    f"{TB_REL}/luna_model_manager_real_text_detection_runtime_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_real_text_detection_runtime_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_real_text_detection_runtime_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("runtime_plan_present", "Runtime 规划文档"),
        ("runtime_adapter_present", "Runtime Adapter"),
        ("request_builder_present", "Request Builder"),
        ("response_parser_present", "Response Parser"),
        ("evidence_normalizer_present", "Evidence Normalizer"),
        ("runtime_policy_present", "Runtime Policy"),
        ("single_runtime_only", "单 Runtime 接入"),
        ("text_detection_first", "Text Detection 优先于 OCR"),
        ("detector_not_task_aware", "Detector 不认识任务"),
        ("detector_not_auto_ocr", "Detector 不自动 OCR"),
        ("grounding_deferred", "Grounding DINO 暂缓"),
        ("case_a_shopfront", "Case A 店招"),
        ("case_b_metro", "Case B 地铁导视"),
        ("case_c_no_text", "Case C 无文字"),
        ("case_d_low_conf", "Case D 低置信度"),
        ("upstream_gos_confirmed", "上游 GO"),
        ("smoke_cases_passed", "smoke 通过"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    plan = _read(f"{TD_REL}/text_detection_runtime_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{TD_REL}/text_detection_runtime_policy_v1.json")
    adapter = _read(f"{TD_REL}/text_detection_runtime_adapter_v1.py")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_v1_001.luna_model_manager_real_text_detection_runtime_integration_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "runtime_plan_present": "Text Detection" in plan and "一次一个" in plan,
        "runtime_adapter_present": "run_text_detection_slot" in adapter,
        "request_builder_present": "build_text_detection_request" in _read(f"{TD_REL}/text_detection_request_builder_v1.py"),
        "response_parser_present": "parse_text_detection_response" in _read(f"{TD_REL}/text_detection_response_parser_v1.py"),
        "evidence_normalizer_present": "normalize_text_detection_evidence" in _read(f"{TD_REL}/text_detection_evidence_normalizer_v1.py"),
        "runtime_policy_present": policy.get("schema_id") == "TextDetectionRuntimePolicyV1",
        "single_runtime_only": policy.get("boundary_flags", {}).get("single_runtime_integration") is True,
        "text_detection_first": policy.get("boundary_flags", {}).get("text_detection_first") is True,
        "detector_not_task_aware": "detector_not_task_aware" in json.dumps(policy),
        "detector_not_auto_ocr": "detector_not_auto_ocr" in json.dumps(policy),
        "grounding_deferred": "grounding_dino" in json.dumps(policy.get("deferred_providers", [])),
        "case_a_shopfront": _case(cases, "case_a_shopfront_text_region").get("passed") is True,
        "case_b_metro": _case(cases, "case_b_metro_direction_region").get("passed") is True,
        "case_c_no_text": _case(cases, "case_c_no_text_image").get("passed") is True,
        "case_d_low_conf": _case(cases, "case_d_low_confidence_detection").get("passed") is True,
        "upstream_gos_confirmed": upstream_ok,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Text_Detection_Runtime_Planning",
        "planning_only": True,
        "single_runtime_text_detection": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["planning_fixture_not_real_paddleocr", "ocr_qwen_deferred"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
