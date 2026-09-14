# -*- coding: utf-8 -*-
"""P1 Detection/OCR Controlled Runner Execution — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-Planning-v1-001"
)
PLANNING_ONLY = True
EXEC_REL = "capabilities/midplatform/model_test_lens/controlled_runner_execution"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/controlled_runner_execution"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

ADMISSION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_RUNNER_INVOCATION_ADMISSION_EXECUTION_GO"
MANUAL_TRIGGER_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_UI_EXECUTION_GO"

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{EXEC_REL}/controlled_runner_execution_plan_v1.md",
    f"{EXEC_REL}/controlled_runner_execution_types_v1.py",
    f"{SCHEMA_REL}/controlled_runner_execution_candidate_schema_v1.json",
    f"{SCHEMA_REL}/detection_controlled_execution_input_policy_v1.json",
    f"{SCHEMA_REL}/ocr_controlled_execution_input_policy_v1.json",
    f"{SCHEMA_REL}/runner_output_envelope_policy_v1.json",
    f"{SCHEMA_REL}/runner_error_policy_v1.json",
    f"{GOV_REL}/controlled_runner_execution_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_detection_ocr_controlled_runner_execution_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "controlled_runner_execution_candidate_schema_record",
    "detection_controlled_execution_input_policy_record",
    "ocr_controlled_execution_input_policy_record",
    "runner_output_envelope_policy_record",
    "runner_error_policy_record",
    "controlled_runner_execution_plan_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001"
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_detection_runner_call", "desc": "不调用 Detection runner"},
    {"guard_id": "C", "key": "no_ocr_runner_call", "desc": "不调用 OCR runner"},
    {"guard_id": "D", "key": "no_model_call", "desc": "不调用模型"},
    {"guard_id": "E", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "F", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "G", "key": "no_auto_runner_trigger", "desc": "不自动触发 runner"},
    {"guard_id": "H", "key": "admitted_does_not_execute_runner", "desc": "admitted 不执行 runner"},
    {"guard_id": "I", "key": "execution_candidate_not_runner_execution", "desc": "execution candidate ≠ 执行"},
    {"guard_id": "J", "key": "execution_candidate_requires_admitted_request", "desc": "须 admitted request"},
    {"guard_id": "K", "key": "rejected_request_cannot_generate_execution_candidate", "desc": "rejected 不可生成"},
    {"guard_id": "L", "key": "pending_request_cannot_generate_execution_candidate", "desc": "pending 不可生成"},
    {"guard_id": "M", "key": "cancelled_request_cannot_generate_execution_candidate", "desc": "cancelled 不可生成"},
    {"guard_id": "N", "key": "no_orphan_execution_candidate", "desc": "禁止 orphan"},
    {"guard_id": "O", "key": "execution_candidate_traceable_to_invocation_request", "desc": "可追溯 request"},
    {"guard_id": "P", "key": "execution_candidate_traceable_to_admission_result", "desc": "可追溯 admission"},
    {"guard_id": "Q", "key": "execution_candidate_traceable_to_task_candidate", "desc": "可追溯 task"},
    {"guard_id": "R", "key": "execution_candidate_traceable_to_attention_record", "desc": "可追溯 attention"},
    {"guard_id": "S", "key": "execution_candidate_traceable_to_region_id", "desc": "可追溯 region"},
    {"guard_id": "T", "key": "detection_input_does_not_contain_fact_label", "desc": "Detection 输入无 fact label"},
    {"guard_id": "U", "key": "ocr_input_does_not_contain_fact_text", "desc": "OCR 输入无 fact text"},
    {"guard_id": "V", "key": "no_prompt_label_fact_upgrade", "desc": "prompt_label 不升级 fact"},
    {"guard_id": "W", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "X", "key": "no_motion_confirmed_from_single_frame", "desc": "单帧不 confirmed_dynamic"},
    {"guard_id": "Y", "key": "runner_output_requires_envelope", "desc": "输出须 envelope"},
    {"guard_id": "Z", "key": "runner_output_requires_fact_admission_before_fact_write", "desc": "fact 须 admission"},
    {"guard_id": "AA", "key": "runner_error_does_not_write_fact", "desc": "错误不写 fact"},
    {"guard_id": "AB", "key": "no_visual_expression_mutation", "desc": "不改变 Visual Expression"},
    {"guard_id": "AC", "key": "no_boundary_clone", "desc": "不克隆 boundary"},
    {"guard_id": "AD", "key": "no_execution_box_on_canvas", "desc": "主图无 execution box"},
    {"guard_id": "AE", "key": "candidate_only_not_executed_not_fact_preserved", "desc": "candidate 边界保留"},
    {"guard_id": "AF", "key": "browser_runtime_guard_inherited", "desc": "浏览器守卫继承"},
    {"guard_id": "AG", "key": "planning_only", "desc": "仅规划不执行"},
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
    plan = _read(f"{EXEC_REL}/controlled_runner_execution_plan_v1.md")
    types_py = _read(f"{EXEC_REL}/controlled_runner_execution_types_v1.py")
    cand = _load_json(f"{SCHEMA_REL}/controlled_runner_execution_candidate_schema_v1.json")
    det_in = _load_json(f"{SCHEMA_REL}/detection_controlled_execution_input_policy_v1.json")
    ocr_in = _load_json(f"{SCHEMA_REL}/ocr_controlled_execution_input_policy_v1.json")
    out_env = _load_json(f"{SCHEMA_REL}/runner_output_envelope_policy_v1.json")
    err_pol = _load_json(f"{SCHEMA_REL}/runner_error_policy_v1.json")
    gov = _read(f"{GOV_REL}/controlled_runner_execution_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    admission = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_runner_invocation_admission_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_runner_invocation_admission_execution_review_v1.json"
    )
    manual_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_review_v1.json"
    )

    forbidden_req = cand.get("forbidden_interpretations", [])

    return {
        "controlled_runner_execution_plan_defined": (
            "controlled_runner_execution_candidate" in plan and "五层关系" in plan
        ),
        "controlled_runner_execution_types_defined": "CONTROLLED_RUNNER_EXECUTION_SYSTEM_ID" in types_py,
        "execution_candidate_schema_defined": cand.get("schema_id") == "ControlledRunnerExecutionCandidateSchemaV1",
        "detection_input_policy_defined": det_in.get("schema_id") == "DetectionControlledExecutionInputPolicyV1",
        "ocr_input_policy_defined": ocr_in.get("schema_id") == "OcrControlledExecutionInputPolicyV1",
        "runner_output_envelope_policy_defined": out_env.get("schema_id") == "RunnerOutputEnvelopePolicyV1",
        "runner_error_policy_defined": err_pol.get("schema_id") == "RunnerErrorPolicyV1",
        "governance_standard_defined": "ControlledRunnerExecutionGovernanceStandardV1" in gov,
        "upstream_admission_execution_go": admission.get("final_decision") == ADMISSION_GO,
        "upstream_manual_trigger_ui_go": manual_ui.get("final_decision") == MANUAL_TRIGGER_UI_GO,
        "five_layer_model_defined": "FIVE_LAYER_MODEL" in types_py and "controlled_runner_execution_candidate" in plan,
        "no_runner_execution": (
            cand.get("boundary_flags", {}).get("not_runner_execution") is True
            and "no_runner_execution" in types_py
        ),
        "no_detection_runner_call": "execute_detection" not in plan and "execute_detection" not in types_py,
        "no_ocr_runner_call": "execute_ocr" not in plan and "execute_ocr" not in types_py,
        "no_model_call": "model_call" in json.dumps(cand.get("forbidden_interpretations", [])) or "no_model_call" in types_py,
        "no_fact_write": (
            cand.get("boundary_flags", {}).get("not_fact") is True
            and out_env.get("runner_output_not_fact") is True
        ),
        "no_navigation_decision": (
            cand.get("field_definitions", {}).get("no_navigation_decision", {}).get("const") is True
        ),
        "no_auto_runner_trigger": cand.get("boundary_flags", {}).get("not_auto_runner_trigger") is True,
        "admitted_does_not_execute_runner": (
            "admitted request 只是允许" in plan or "admitted_does_not_execute_runner" in types_py
        ),
        "execution_candidate_not_runner_execution": (
            cand.get("boundary_flags", {}).get("execution_candidate_only") is True
            and "execution_candidate_not_runner_execution" in types_py
        ),
        "execution_candidate_requires_admitted_request": (
            cand.get("field_definitions", {}).get("admission_decision_at_create", {}).get("const") == "admitted"
            and "admitted_request_required" in types_py
        ),
        "rejected_request_cannot_generate_execution_candidate": (
            "rejected" in plan and "rejected_request_cannot_generate_execution_candidate" in types_py
        ),
        "pending_request_cannot_generate_execution_candidate": (
            "pending" in plan and "pending_request_cannot_generate_execution_candidate" in types_py
        ),
        "cancelled_request_cannot_generate_execution_candidate": (
            "cancelled" in plan and "cancelled_request_cannot_generate_execution_candidate" in types_py
        ),
        "no_orphan_execution_candidate": (
            "orphan" in json.dumps(forbidden_req) and "no_orphan_execution_candidate" in types_py
        ),
        "execution_candidate_traceable_to_invocation_request": (
            "source_invocation_request_id" in cand.get("required_fields", [])
        ),
        "execution_candidate_traceable_to_admission_result": (
            "source_admission_result_id" in cand.get("required_fields", [])
        ),
        "execution_candidate_traceable_to_task_candidate": (
            "source_runner_task_candidate_id" in cand.get("required_fields", [])
        ),
        "execution_candidate_traceable_to_attention_record": (
            "source_attention_record_id" in cand.get("required_fields", [])
        ),
        "execution_candidate_traceable_to_region_id": "source_region_id" in cand.get("required_fields", []),
        "detection_input_does_not_contain_fact_label": (
            det_in.get("boundary_flags", {}).get("detection_input_does_not_contain_fact_label") is True
            and "fact_label" in json.dumps(det_in.get("forbidden_inputs", []))
        ),
        "ocr_input_does_not_contain_fact_text": (
            ocr_in.get("boundary_flags", {}).get("ocr_input_does_not_contain_fact_text") is True
            and "fact_text" in json.dumps(ocr_in.get("forbidden_inputs", []))
        ),
        "no_prompt_label_fact_upgrade": (
            "prompt_label_as_truth" in json.dumps(det_in)
            or "no_prompt_label_fact_upgrade" in types_py
        ),
        "no_human_correction_ground_truth": (
            "ground_truth" in gov.lower() or "human_correction_as" in json.dumps(ocr_in)
        ),
        "no_motion_confirmed_from_single_frame": (
            "confirmed_dynamic" in json.dumps(det_in.get("input_field_rules", {}))
            or "no_motion_confirmed_from_single_frame" in types_py
        ),
        "runner_output_requires_envelope": (
            out_env.get("boundary_flags", {}).get("runner_output_requires_envelope") is True
            and "output_envelope_schema_ref" in cand.get("required_fields", [])
        ),
        "runner_output_requires_fact_admission_before_fact_write": (
            out_env.get("fact_admission_required_before_fact_write") is True
            and cand.get("field_definitions", {}).get("needs_fact_admission_for_any_fact_write", {}).get("const") is True
        ),
        "runner_error_does_not_write_fact": (
            err_pol.get("boundary_flags", {}).get("runner_error_does_not_write_fact") is True
            and err_pol.get("error_handling_rules", {}).get("no_fact_write_on_error") is True
        ),
        "no_visual_expression_mutation": (
            out_env.get("visual_expression_rules", {}).get("must_not_override_segmentation_boundary") is True
            and "visual_expression_system_frozen" in types_py
        ),
        "no_boundary_clone": "boundary_clone" not in plan,
        "no_execution_box_on_canvas": (
            out_env.get("visual_expression_rules", {}).get("no_execution_box_on_canvas") is True
            and "no_execution_box_on_canvas" in plan
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            cand.get("field_definitions", {}).get("candidate_only", {}).get("const") is True
            and cand.get("field_definitions", {}).get("not_executed", {}).get("const") is True
        ),
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_inherited" in types_py and "BrowserRuntimeGuard" in browser
        ),
        "ui_future_copy_no_execution_misleading": (
            "生成受控执行候选" in plan and "开始检测" in plan and "禁止" in plan
        ),
        "error_isolation_defined": len(err_pol.get("error_types", [])) >= 8,
        "planning_only": PLANNING_ONLY and cand.get("boundary_flags", {}).get("planning_only") is True,
        "recommended_next_execution_defined": NEXT_EXECUTION in plan or NEXT_EXECUTION in json.dumps(cand),
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
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

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "recommended_execution_phase": NEXT_EXECUTION,
        "five_layer_model": {
            "runner_task_candidate": "what_could_be_considered",
            "runner_invocation_request": "prepared_application_to_execute",
            "runner_invocation_admission": "allowed_into_execution_preparation",
            "controlled_runner_execution_candidate": "how_to_execute_in_controlled_sandbox",
            "runner_execution": "actual_model_run_forbidden",
        },
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "test_mode": "planning", "planning_only": True,
        }
        payloads = {
            "controlled_runner_execution_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/controlled_runner_execution_candidate_schema_v1.json"
            ),
            "detection_controlled_execution_input_policy_record": _load_json(
                f"{SCHEMA_REL}/detection_controlled_execution_input_policy_v1.json"
            ),
            "ocr_controlled_execution_input_policy_record": _load_json(
                f"{SCHEMA_REL}/ocr_controlled_execution_input_policy_v1.json"
            ),
            "runner_output_envelope_policy_record": _load_json(
                f"{SCHEMA_REL}/runner_output_envelope_policy_v1.json"
            ),
            "runner_error_policy_record": _load_json(f"{SCHEMA_REL}/runner_error_policy_v1.json"),
            "controlled_runner_execution_plan_record": {
                "plan_ref": f"{EXEC_REL}/controlled_runner_execution_plan_v1.md"
            },
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(
        json.dumps(
            {
                "final_decision": r["final_decision"],
                "blocker_count": r["blocker_count"],
                "negative_guard_passed": r["negative_guard_passed"],
                "negative_guard_count": r["negative_guard_count"],
                "recommended_execution_phase": r["recommended_execution_phase"],
                "failed_checks": r.get("failed_checks", []),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
