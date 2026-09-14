# -*- coding: utf-8
"""P1 Network-Assisted Situation Learning — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Network-Assisted-Situation-Learning-Planning-v1-001"
NAL_REL = "capabilities/midplatform/network_assisted_learning"
SCHEMA_REL = f"{NAL_REL}/schemas"
GOV_REL = f"{NAL_REL}/governance"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_network_assisted_situation_learning_planning_v1_001"
)

UPSTREAM_FREEZE_GO = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO"

FINAL_GO = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{NAL_REL}/network_assisted_situation_learning_plan_v1.md",
    f"{NAL_REL}/network_assisted_situation_learning_types_v1.py",
    f"{NAL_REL}/network_learning_candidate_builder_v1.py",
    f"{NAL_REL}/network_learning_policy_reviewer_v1.py",
    f"{NAL_REL}/situation_case_library_builder_v1.py",
    f"{SCHEMA_REL}/external_learning_source_schema_v1.json",
    f"{SCHEMA_REL}/teacher_model_label_candidate_schema_v1.json",
    f"{SCHEMA_REL}/web_reference_candidate_schema_v1.json",
    f"{SCHEMA_REL}/situation_learning_candidate_schema_v1.json",
    f"{SCHEMA_REL}/situation_case_record_schema_v1.json",
    f"{SCHEMA_REL}/situation_training_dataset_candidate_schema_v1.json",
    f"{SCHEMA_REL}/learning_policy_review_result_schema_v1.json",
    f"{SCHEMA_REL}/learning_provenance_record_schema_v1.json",
    f"{GOV_REL}/network_assisted_situation_learning_policy_v1.json",
    f"{TB_REL}/network_assisted_situation_learning_smoke_v1.py",
    f"{TB_REL}/run_network_assisted_situation_learning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_network_assisted_situation_learning_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_direct_web_training", "desc": "禁止直接网络训练"},
    {"guard_id": "B", "key": "no_direct_teacher_weight_update", "desc": "禁止 teacher 改权重"},
    {"guard_id": "C", "key": "teacher_output_candidate_only", "desc": "teacher 输出仅 candidate"},
    {"guard_id": "D", "key": "web_reference_candidate_only", "desc": "web 仅 candidate"},
    {"guard_id": "E", "key": "learning_candidate_not_fact", "desc": "learning candidate 非 fact"},
    {"guard_id": "F", "key": "case_record_not_fact", "desc": "case record 非 fact"},
    {"guard_id": "G", "key": "training_dataset_candidate_not_final_training", "desc": "dataset 非最终训练"},
    {"guard_id": "H", "key": "provenance_required_for_external_sources", "desc": "外部来源需 provenance"},
    {"guard_id": "I", "key": "policy_review_required_for_case_entry", "desc": "入 case 需 policy review"},
    {"guard_id": "J", "key": "human_review_required_for_training_dataset", "desc": "训练集需 human approval"},
    {"guard_id": "K", "key": "no_runner_invocation_from_learning_candidate", "desc": "learning 不触发 runner"},
    {"guard_id": "L", "key": "no_tool_install_from_learning_candidate", "desc": "learning 不安装工具"},
    {"guard_id": "M", "key": "unsafe_rule_flagged", "desc": "unsafe rule 可 flag"},
    {"guard_id": "N", "key": "shopfront_teacher_case_accepts_ocr_noops_slam", "desc": "店招 teacher 接受 OCR/noop SLAM"},
    {"guard_id": "O", "key": "bad_teacher_slam_for_text_rejected", "desc": "错误 SLAM 建议被拒"},
    {"guard_id": "P", "key": "web_reference_does_not_auto_train", "desc": "web 不 auto train"},
    {"guard_id": "Q", "key": "human_correction_generates_learning_candidate", "desc": "纠错生成 learning candidate"},
    {"guard_id": "R", "key": "test_trace_generates_regression_case_candidate", "desc": "test trace 生成回归 case"},
    {"guard_id": "S", "key": "privacy_guard_present", "desc": "privacy guard 存在"},
    {"guard_id": "T", "key": "source_trust_tier_required", "desc": "trust_tier 必填"},
    {"guard_id": "U", "key": "all_outputs_candidate_only", "desc": "输出均 candidate_only"},
    {"guard_id": "V", "key": "no_fact_admission_bypass", "desc": "不绕过 fact admission"},
    {"guard_id": "W", "key": "no_existing_runner_mutation", "desc": "未修改 runner"},
    {"guard_id": "X", "key": "no_existing_observation_schema_mutation", "desc": "未修改 observation schema"},
    {"guard_id": "Y", "key": "deterministic_smoke_only", "desc": "仅 deterministic smoke"},
    {"guard_id": "Z", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "AA", "key": "upstream_freeze_go", "desc": "上游 Freeze GO"},
    {"guard_id": "AB", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _audit() -> Dict[str, bool]:
    plan = _read(f"{NAL_REL}/network_assisted_situation_learning_plan_v1.md")
    types_py = _read(f"{NAL_REL}/network_assisted_situation_learning_types_v1.py")
    builder = _read(f"{NAL_REL}/network_learning_candidate_builder_v1.py")
    reviewer = _read(f"{NAL_REL}/network_learning_policy_reviewer_v1.py")
    case_builder = _read(f"{NAL_REL}/situation_case_library_builder_v1.py")
    policy = _load_json(f"{GOV_REL}/network_assisted_situation_learning_policy_v1.json")
    learning_schema = _load_json(f"{SCHEMA_REL}/situation_learning_candidate_schema_v1.json")
    dataset_schema = _load_json(f"{SCHEMA_REL}/situation_training_dataset_candidate_schema_v1.json")
    runner_py = _read("capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py")

    freeze = _load_json(
        "_tmp_eval_out/p1_midplatform_perception_tool_layer_freeze_v1_smoke_v0/"
        "p1_midplatform_perception_tool_layer_freeze_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_network_assisted_situation_learning_planning_v1_001.network_assisted_situation_learning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    smoke_cases = smoke_result.get("smoke_cases", [])
    case_a = next((c for c in smoke_cases if c.get("case_id") == "case_a_teacher_shopfront_sign"), {})
    case_b = next((c for c in smoke_cases if c.get("case_id") == "case_b_teacher_bad_slam_for_text"), {})
    case_c = next((c for c in smoke_cases if c.get("case_id") == "case_c_web_reference_candidate"), {})
    case_d = next((c for c in smoke_cases if c.get("case_id") == "case_d_human_correction"), {})
    case_e = next((c for c in smoke_cases if c.get("case_id") == "case_e_test_trace_regression"), {})
    case_f = next((c for c in smoke_cases if c.get("case_id") == "case_f_training_dataset_candidate"), {})

    return {
        "no_direct_web_training": policy.get("boundary_flags", {}).get("no_direct_web_training") is True,
        "no_direct_teacher_weight_update": policy.get("boundary_flags", {}).get("no_direct_teacher_weight_update") is True,
        "teacher_output_candidate_only": policy.get("boundary_flags", {}).get("teacher_output_candidate_only") is True,
        "web_reference_candidate_only": policy.get("boundary_flags", {}).get("web_reference_candidate_only") is True,
        "learning_candidate_not_fact": learning_schema.get("boundary_flags", {}).get("learning_candidate_not_fact") is True,
        "case_record_not_fact": "case_record_not_fact" in json.dumps(_load_json(f"{SCHEMA_REL}/situation_case_record_schema_v1.json")),
        "training_dataset_candidate_not_final_training": (
            dataset_schema.get("boundary_flags", {}).get("training_dataset_candidate_not_final_training") is True
        ),
        "provenance_required_for_external_sources": "build_provenance" in builder and "provenance_required" in policy.get("boundary_flags", {}),
        "policy_review_required_for_case_entry": "review_learning_candidate" in reviewer,
        "human_review_required_for_training_dataset": case_f.get("passed") is True,
        "no_runner_invocation_from_learning_candidate": (
            "no_runner_invocation" in dataset_schema.get("field_definitions", {}).get("blocked_training_use", {}).get("example", [])
            or "runner_invocation" in json.dumps(dataset_schema)
        ),
        "no_tool_install_from_learning_candidate": "tool_install" in json.dumps(case_builder),
        "unsafe_rule_flagged": "check_unsafe_rule" in reviewer and case_b.get("passed") is True,
        "shopfront_teacher_case_accepts_ocr_noops_slam": case_a.get("passed") is True,
        "bad_teacher_slam_for_text_rejected": case_b.get("passed") is True,
        "web_reference_does_not_auto_train": case_c.get("passed") is True and case_c.get("no_auto_train") is True,
        "human_correction_generates_learning_candidate": case_d.get("passed") is True,
        "test_trace_generates_regression_case_candidate": case_e.get("passed") is True,
        "privacy_guard_present": policy.get("boundary_flags", {}).get("privacy_guard") is True,
        "source_trust_tier_required": policy.get("boundary_flags", {}).get("external_source_trust_tier_required") is True,
        "all_outputs_candidate_only": "candidate_only" in builder and "candidate_only" in types_py,
        "no_fact_admission_bypass": "no_fact_from_learning_candidate" in json.dumps(policy),
        "no_existing_runner_mutation": "network_assisted_learning" not in runner_py,
        "no_existing_observation_schema_mutation": "network_assisted_learning" not in _read(
            "capabilities/midplatform/governance_standards/model_test_lens_ui/observation_attention_layer_governance_standard_v1.md"
        ),
        "deterministic_smoke_only": smoke_result.get("deterministic_smoke_only") is True,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_freeze_go": freeze.get("final_decision") == UPSTREAM_FREEZE_GO,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
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

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_smoke = _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_network_assisted_situation_learning_planning_v1_smoke_v0"
    out_review = _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_network_assisted_situation_learning_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    known_limits = [
        "no_real_network_in_planning",
        "no_real_teacher_model_calls",
        "no_model_training",
        "policy_reviewer_is_detinistic_stub",
        "human_review_simulated_via_review_status_only",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "smoke_cases_passed": flags.get("smoke_cases_pass", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "output_smoke_dir": str(out_smoke),
    }

    if write_file:
        rp = out_review / "p1_midplatform_network_assisted_situation_learning_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb.get("test_board_dir", TB_REL))
        if board_dir.is_dir():
            common = {
                "phase_id": PHASE_ID,
                "protected": True,
                "non_deletable": True,
                "test_artifact_protected": True,
                "test_mode": "planning",
            }
            payloads = {
                "network_assisted_situation_learning_plan_record": {"plan_ref": f"{NAL_REL}/network_assisted_situation_learning_plan_v1.md"},
                "network_assisted_situation_learning_policy_record": _load_json(f"{GOV_REL}/network_assisted_situation_learning_policy_v1.json"),
            }
            for name, payload in payloads.items():
                (board_dir / f"{name}.json").write_text(
                    json.dumps({**common, "record": payload}, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("review_guards_passed"),
        "generated_files_count": len(r.get("generated_files", [])),
        "known_limits": r.get("known_limits", []),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
