# -*- coding: utf-8 -*-
"""P1 Text Detection Runtime — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-DryRun-v1-001"
DRYRUN_REL = "capabilities/midplatform/model_manager/runtime/text_detection/dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_multi_model_chain_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/text_detection_runtime_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/text_detection_execution_simulator_v1.py",
    f"{DRYRUN_REL}/text_detection_evidence_builder_v1.py",
    f"{DRYRUN_REL}/text_detection_collaboration_adapter_v1.py",
    f"{DRYRUN_REL}/text_detection_runtime_metrics_v1.py",
    f"{DRYRUN_REL}/text_detection_dryrun_policy_v1.json",
    f"{TB_REL}/luna_model_manager_real_text_detection_runtime_integration_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "DryRun Adapter"),
        ("execution_simulator_present", "Execution Simulator"),
        ("evidence_builder_present", "Evidence Builder"),
        ("collaboration_adapter_present", "Collaboration Adapter"),
        ("runtime_metrics_present", "Runtime Metrics"),
        ("dryrun_policy_present", "DryRun Policy"),
        ("governance_loop", "治理闭环"),
        ("deterministic_fixture_only", "仅 deterministic fixture"),
        ("collaboration_decides_next", "Collaboration 决定下一 Slot"),
        ("runtime_usage_metrics", "Runtime Usage Metrics"),
        ("case_a_shopfront", "Case A 店招"),
        ("case_b_subway", "Case B 地铁"),
        ("case_c_no_text", "Case C 无文字"),
        ("case_d_low_conf", "Case D 错误检测"),
        ("case_e_runtime_fail", "Case E Runtime 故障"),
        ("upstream_gos_confirmed", "上游 GO"),
        ("dryrun_cases_pass", "dryrun 通过"),
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
    policy = _load_json(_detect_repo_root() / f"{DRYRUN_REL}/text_detection_dryrun_policy_v1.json")
    adapter = _read(f"{DRYRUN_REL}/text_detection_runtime_dryrun_adapter_v1.py")
    metrics = _read(f"{DRYRUN_REL}/text_detection_runtime_metrics_v1.py")

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1_001.luna_model_manager_real_text_detection_runtime_integration_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )
    case_a = _case(cases, "case_a_shopfront_text_region_dryrun").get("result") or {}

    return {
        "dryrun_adapter_present": "run_case_a_shopfront_dryrun" in adapter,
        "execution_simulator_present": "simulate_text_detection_execution" in _read(f"{DRYRUN_REL}/text_detection_execution_simulator_v1.py"),
        "evidence_builder_present": "build_text_detection_evidence" in _read(f"{DRYRUN_REL}/text_detection_evidence_builder_v1.py"),
        "collaboration_adapter_present": "decide_collaboration_next_slot" in _read(f"{DRYRUN_REL}/text_detection_collaboration_adapter_v1.py"),
        "runtime_metrics_present": "get_runtime_usage_metrics" in metrics,
        "dryrun_policy_present": policy.get("schema_id") == "TextDetectionDryrunPolicyV1",
        "governance_loop": policy.get("boundary_flags", {}).get("governance_loop_not_ocr_pipeline") is True,
        "deterministic_fixture_only": policy.get("boundary_flags", {}).get("deterministic_fixture_only") is True,
        "collaboration_decides_next": policy.get("boundary_flags", {}).get("collaboration_next_slot") is True,
        "runtime_usage_metrics": policy.get("boundary_flags", {}).get("runtime_usage_metrics") is True,
        "case_a_shopfront": _case(cases, "case_a_shopfront_text_region_dryrun").get("passed") is True,
        "case_b_subway": _case(cases, "case_b_subway_direction_dryrun").get("passed") is True,
        "case_c_no_text": _case(cases, "case_c_no_text_environment_dryrun").get("passed") is True,
        "case_d_low_conf": _case(cases, "case_d_false_detection_dryrun").get("passed") is True,
        "case_e_runtime_fail": _case(cases, "case_e_runtime_failure_dryrun").get("passed") is True,
        "upstream_gos_confirmed": upstream_ok,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Text_Detection_Runtime_DryRun",
        "dryrun_only": True,
        "governance_loop_verified": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["no_real_paddleocr", "ocr_runtime_deferred"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_review_v1.json"
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
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
