# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Foundation — dry-run review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-DryRun-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
DRYRUN_REL = f"{MM_REL}/model_manager_dryrun"
GOV_REL = f"{MM_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_foundation_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_foundation_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_decision_validation_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_decision_validation_layer_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Provider-Integration-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/luna_model_manager_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/model_selection_processor_v1.py",
    f"{DRYRUN_REL}/capability_matching_processor_v1.py",
    f"{DRYRUN_REL}/routing_score_calculator_v1.py",
    f"{GOV_REL}/luna_model_manager_dryrun_policy_v1.json",
    f"{MM_REL}/luna_model_manager_processor_v1.py",
    f"{MM_REL}/engines/model_routing_engine_v1.py",
    f"{MM_REL}/engines/model_evaluation_engine_v1.py",
    f"{TB_REL}/luna_model_manager_foundation_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_foundation_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_foundation_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("capability_matching_present", "capability matching processor"),
        ("routing_calculator_present", "routing score calculator"),
        ("selection_processor_present", "model selection processor"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("full_chain_present", "L1→L2→L2.5→MM→Handoff 链路"),
        ("capability_first_routing", "能力优先路由"),
        ("provider_candidate_not_decision", "provider_candidate 非决策"),
        ("model_manager_not_tool_os", "MM 不等于 Tool OS"),
        ("evaluation_no_auto_routing", "evaluation 不自动改路由"),
        ("admission_gate_present", "admission 门禁"),
        ("no_model_execution", "不执行模型"),
        ("no_auto_policy_update", "不自动更新策略"),
        ("no_fact_write", "不写 fact"),
        ("no_real_api", "无真实 API"),
        ("case_a_shopfront_ocr", "Case A 店招 OCR"),
        ("case_b_unknown_qwen_handoff", "Case B unknown Qwen handoff"),
        ("case_c_reliability_priority", "Case C reliability 优先"),
        ("case_d_ocr_unavailable", "Case D OCR 不可用"),
        ("case_e_gemini_admission", "Case E Gemini admission"),
        ("job_564f1aa93983_fixture", "店招 job fixture"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("dryrun_cases_pass", "dryrun cases 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
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
    adapter = _read(f"{DRYRUN_REL}/luna_model_manager_dryrun_adapter_v1.py")
    cap_match = _read(f"{DRYRUN_REL}/capability_matching_processor_v1.py")
    routing_calc = _read(f"{DRYRUN_REL}/routing_score_calculator_v1.py")
    selection = _read(f"{DRYRUN_REL}/model_selection_processor_v1.py")
    policy = _load_json(_detect_repo_root() / f"{GOV_REL}/luna_model_manager_dryrun_policy_v1.json")
    evaluation = _read(f"{MM_REL}/engines/model_evaluation_engine_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_foundation_dryrun_v1_001.luna_model_manager_foundation_dryrun_fixtures_v1 import (  # noqa: WPS433
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

    return {
        "dryrun_adapter_present": "run_model_manager_dryrun" in adapter,
        "capability_matching_present": "match_capability_need" in cap_match,
        "routing_calculator_present": "calculate_routing_scores" in routing_calc,
        "selection_processor_present": "select_provider_candidate" in selection,
        "dryrun_policy_present": policy.get("schema_id") == "LunaModelManagerDryrunPolicyV1",
        "full_chain_present": "capability_match_candidate" in adapter and "teacher_adapter_handoff_candidate" in adapter,
        "capability_first_routing": policy.get("boundary_flags", {}).get("capability_first_not_model_first") is True,
        "provider_candidate_not_decision": "produced_provider_candidate_not_decision" in selection,
        "model_manager_not_tool_os": policy.get("boundary_flags", {}).get("model_manager_not_tool_os") is True,
        "evaluation_no_auto_routing": "no_auto_policy_update" in evaluation,
        "admission_gate_present": "run_model_admission_pipeline" in adapter,
        "no_model_execution": policy.get("boundary_flags", {}).get("no_model_execution") is True,
        "no_auto_policy_update": policy.get("boundary_flags", {}).get("no_auto_policy_update") is True,
        "no_fact_write": policy.get("boundary_flags", {}).get("no_fact_write") is True,
        "no_real_api": policy.get("boundary_flags", {}).get("no_real_api_in_dryrun") is True,
        "case_a_shopfront_ocr": _case(cases, "case_a_shopfront_ocr_routing").get("passed") is True,
        "case_b_unknown_qwen_handoff": _case(cases, "case_b_unknown_scene_qwen_handoff").get("passed") is True,
        "case_c_reliability_priority": _case(cases, "case_c_reliability_priority_routing").get("passed") is True,
        "case_d_ocr_unavailable": _case(cases, "case_d_ocr_unavailable_fallback").get("passed") is True,
        "case_e_gemini_admission": _case(cases, "case_e_gemini_admission_gate").get("passed") is True,
        "job_564f1aa93983_fixture": "job_564f1aa93983" in _read(
            "capabilities/test_board/model_governance/"
            "phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001/"
            "luna_agent_planning_layer_dryrun_fixtures_v1.py"
        ),
        "no_existing_runner_mutation": "model_manager_dryrun" not in runner,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]
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

    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": [
            "dryrun_only_no_execution",
            "score_profiles_fixture_based",
            "gemini_gpt_not_live_integrated",
            "teacher_modules_frozen_as_prerequisites",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_foundation_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
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
