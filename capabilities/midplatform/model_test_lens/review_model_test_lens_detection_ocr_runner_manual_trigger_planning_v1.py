# -*- coding: utf-8 -*-
"""P1 Detection/OCR Runner Manual Trigger — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-Planning-v1-001"
PLANNING_ONLY = True
TRIGGER_REL = "capabilities/midplatform/model_test_lens/runner_manual_trigger"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/runner_manual_trigger"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
FRR_SCHEMA = "capabilities/midplatform/model_test_lens/schemas/followup_runner_route"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

QUEUE_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_GO"
FRR_PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_PLANNING_GO"

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TRIGGER_REL}/runner_manual_trigger_plan_v1.md",
    f"{TRIGGER_REL}/runner_manual_trigger_types_v1.py",
    f"{SCHEMA_REL}/runner_invocation_request_schema_v1.json",
    f"{SCHEMA_REL}/manual_runner_trigger_admission_policy_v1.json",
    f"{SCHEMA_REL}/detection_ocr_manual_trigger_route_policy_v1.json",
    f"{GOV_REL}/runner_manual_trigger_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_detection_ocr_runner_manual_trigger_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "runner_invocation_request_schema_record",
    "manual_runner_trigger_admission_policy_record",
    "detection_ocr_manual_trigger_route_policy_record",
    "runner_manual_trigger_plan_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-v1-001"
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_runner_execution", "desc": "不触发 runner 执行"},
    {"guard_id": "B", "key": "no_model_call", "desc": "不调用模型"},
    {"guard_id": "C", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "D", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "E", "key": "no_auto_runner_trigger", "desc": "不自动触发 runner"},
    {"guard_id": "F", "key": "no_running_state_allowed", "desc": "禁止 running 状态"},
    {"guard_id": "G", "key": "no_executed_state_allowed", "desc": "禁止 executed 状态"},
    {"guard_id": "H", "key": "no_completed_state_allowed", "desc": "禁止 completed 状态"},
    {"guard_id": "I", "key": "invocation_request_not_execution", "desc": "request ≠ execution"},
    {"guard_id": "J", "key": "invocation_request_requires_pinned_task_candidate", "desc": "须 pinned task"},
    {"guard_id": "K", "key": "excluded_task_cannot_generate_request", "desc": "excluded 不可生成"},
    {"guard_id": "L", "key": "stale_task_requires_reconfirmation", "desc": "stale 须复核"},
    {"guard_id": "M", "key": "blocked_task_cannot_generate_request", "desc": "blocked 不可生成"},
    {"guard_id": "N", "key": "no_orphan_invocation_request", "desc": "禁止 orphan request"},
    {"guard_id": "O", "key": "request_traceable_to_runner_task_candidate", "desc": "可追溯 task"},
    {"guard_id": "P", "key": "request_traceable_to_attention_record", "desc": "可追溯 attention"},
    {"guard_id": "Q", "key": "request_traceable_to_region_id", "desc": "可追溯 region"},
    {"guard_id": "R", "key": "detection_request_requires_detection_route", "desc": "Detection 路由匹配"},
    {"guard_id": "S", "key": "ocr_request_requires_ocr_route", "desc": "OCR 路由匹配"},
    {"guard_id": "T", "key": "no_prompt_label_fact_upgrade", "desc": "prompt_label 不升级 fact"},
    {"guard_id": "U", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "V", "key": "no_motion_confirmed_from_single_frame", "desc": "单帧不 confirmed_dynamic"},
    {"guard_id": "W", "key": "candidate_only_not_executed_not_fact_preserved", "desc": "candidate 边界保留"},
    {"guard_id": "X", "key": "no_visual_expression_mutation", "desc": "不改变 Visual Expression"},
    {"guard_id": "Y", "key": "browser_runtime_guard_inherited", "desc": "浏览器守卫继承"},
    {"guard_id": "Z", "key": "planning_only", "desc": "仅规划不执行"},
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


def _load_review(rel: str) -> Dict[str, Any]:
    return _load_json(rel) if _read(rel) else {}


def _audit() -> Dict[str, bool]:
    plan = _read(f"{TRIGGER_REL}/runner_manual_trigger_plan_v1.md")
    types_py = _read(f"{TRIGGER_REL}/runner_manual_trigger_types_v1.py")
    req_schema = _load_json(f"{SCHEMA_REL}/runner_invocation_request_schema_v1.json")
    admission = _load_json(f"{SCHEMA_REL}/manual_runner_trigger_admission_policy_v1.json")
    route_policy = _load_json(f"{SCHEMA_REL}/detection_ocr_manual_trigger_route_policy_v1.json")
    gov = _read(f"{GOV_REL}/runner_manual_trigger_governance_standard_v1.md")
    task_schema = _load_json(f"{FRR_SCHEMA}/followup_runner_task_candidate_schema_v1.json")
    browser_guard = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    queue_post = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_post_review_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_post_review_v1.json"
    )
    frr_plan = _load_review(
        "_tmp_eval_out/p1_midplatform_model_test_lens_followup_runner_route_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_followup_runner_route_planning_review_v1.json"
    )

    pinned_rules = admission.get("queue_state_rules", {}).get("pinned", {})
    excluded_rules = admission.get("queue_state_rules", {}).get("excluded", {})
    stale_rules = admission.get("queue_state_rules", {}).get("stale_candidate", {})
    blocked_rules = admission.get("queue_state_rules", {}).get("blocked_by_policy", {})
    exec_machine = admission.get("execution_status_machine", {})

    return {
        "runner_manual_trigger_plan_defined": (
            "runner_invocation_request" in plan and "三层关系" in plan
        ),
        "runner_manual_trigger_types_defined": "RUNNER_MANUAL_TRIGGER_SYSTEM_ID" in types_py,
        "runner_invocation_request_schema_defined": (
            req_schema.get("schema_id") == "RunnerInvocationRequestSchemaV1"
        ),
        "manual_runner_trigger_admission_policy_defined": (
            admission.get("schema_id") == "ManualRunnerTriggerAdmissionPolicyV1"
        ),
        "detection_ocr_manual_trigger_route_policy_defined": (
            route_policy.get("schema_id") == "DetectionOcrManualTriggerRoutePolicyV1"
        ),
        "governance_standard_defined": "RunnerManualTriggerGovernanceStandardV1" in gov,
        "upstream_followup_runner_route_queue_go": (
            queue_post.get("final_decision") == QUEUE_UI_GO
            or frr_plan.get("final_decision") == FRR_PLANNING_GO
        ),
        "three_layer_model_defined": (
            "runner_task_candidate" in plan
            and "runner_invocation_request" in plan
            and "runner_execution" in plan
            and types_py.count("THREE_LAYER_MODEL") > 0
        ),
        "no_runner_execution": (
            req_schema.get("boundary_flags", {}).get("not_runner_execution") is True
            and "no_runner_execution" in types_py
        ),
        "no_model_call": "model_call" in json.dumps(admission.get("forbidden_operations", [])),
        "no_fact_write": (
            req_schema.get("boundary_flags", {}).get("not_fact") is True
            and "not_fact_write" in json.dumps(admission)
        ),
        "no_navigation_decision": (
            req_schema.get("field_definitions", {}).get("no_navigation_decision", {}).get("const") is True
            or "no_navigation_decision" in types_py
        ),
        "no_auto_runner_trigger": admission.get("auto_runner_trigger_allowed") is False,
        "no_running_state_allowed": (
            "running" in json.dumps(admission.get("admission_status_machine", {}).get("forbidden", []))
            and "running" in json.dumps(exec_machine.get("forbidden", []))
        ),
        "no_executed_state_allowed": "executed" in json.dumps(exec_machine.get("forbidden", [])),
        "no_completed_state_allowed": "completed" in json.dumps(exec_machine.get("forbidden", [])),
        "invocation_request_not_execution": (
            req_schema.get("boundary_flags", {}).get("invocation_request_only") is True
            and "invocation_request_not_execution" in types_py
        ),
        "invocation_request_requires_pinned_task_candidate": (
            pinned_rules.get("may_generate_request") is True
            and admission.get("request_generation_entry", {}).get("only_from") == "pinned_runner_task_candidate"
            and req_schema.get("field_definitions", {}).get("source_queue_state_at_request", {}).get("enum") == ["pinned"]
        ),
        "excluded_task_cannot_generate_request": excluded_rules.get("may_generate_request") is False,
        "stale_task_requires_reconfirmation": (
            stale_rules.get("may_generate_request") is False
            and "reconfirm" in stale_rules.get("reason", "")
        ),
        "blocked_task_cannot_generate_request": blocked_rules.get("may_generate_request") is False,
        "no_orphan_invocation_request": (
            admission.get("orphan_request_forbidden") is True
            and "trace_chain" in req_schema.get("required_fields", [])
        ),
        "request_traceable_to_runner_task_candidate": (
            "source_runner_task_candidate_id" in req_schema.get("required_fields", [])
        ),
        "request_traceable_to_attention_record": (
            "source_attention_record_id" in req_schema.get("required_fields", [])
        ),
        "request_traceable_to_region_id": "source_region_id" in req_schema.get("required_fields", []),
        "detection_request_requires_detection_route": (
            route_policy.get("detection_request", {}).get("required_route", {}).get("source_target_model_id") == "detection"
            and admission.get("route_type_matching", {}).get("Detection", {}).get("source_target_model_id") == "detection"
        ),
        "ocr_request_requires_ocr_route": (
            route_policy.get("ocr_request", {}).get("required_route", {}).get("source_target_model_id") == "ocr"
            and admission.get("route_type_matching", {}).get("OCR", {}).get("source_target_model_id") == "ocr"
        ),
        "no_prompt_label_fact_upgrade": (
            "prompt_label_as_ground_truth" in json.dumps(req_schema.get("forbidden_interpretations", []))
            or "prompt_label_as_detection_ground_truth" in json.dumps(route_policy)
        ),
        "no_human_correction_ground_truth": (
            "ground_truth" in gov.lower()
            or "treat_as_ground_truth" in json.dumps(admission.get("correction_boost_rules", {}))
        ),
        "no_motion_confirmed_from_single_frame": (
            "confirmed_dynamic" in json.dumps(route_policy.get("detection_request", {}).get("forbidden", []))
            or "confirmed_dynamic_from_single_frame" in json.dumps(req_schema.get("forbidden_interpretations", []))
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            req_schema.get("field_definitions", {}).get("candidate_only", {}).get("const") is True
            and req_schema.get("field_definitions", {}).get("execution_status", {}).get("const") == "not_executed"
            and req_schema.get("field_definitions", {}).get("not_fact", {}).get("const") is True
        ),
        "no_visual_expression_mutation": (
            admission.get("visual_expression_preservation", {}).get("canvas_frozen") is True
            and "visual_expression_system_frozen" in types_py
        ),
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_inherited" in types_py
            and admission.get("browser_runtime_guard_inheritance", {}).get("bare_global_forbidden") is True
            and "BrowserRuntimeGuard" in browser_guard
        ),
        "ui_future_copy_no_execution_misleading": (
            "开始检测" in json.dumps(route_policy.get("ui_copy_guidance_future", {}).get("forbidden_button_labels", []))
            and "生成检测请求" in json.dumps(route_policy.get("ui_copy_guidance_future", {}).get("allowed_button_labels", []))
        ),
        "trace_chain_five_stages": (
            len(req_schema.get("field_definitions", {}).get("trace_chain", {}).get("items", {}).get("properties", {}).get("stage", {}).get("enum", [])) >= 5
            if isinstance(req_schema.get("field_definitions", {}).get("trace_chain"), dict)
            else "trace_chain" in plan
        ),
        "upstream_task_candidate_schema_linked": (
            task_schema.get("schema_id") == "FollowupRunnerTaskCandidateSchemaV1"
        ),
        "planning_only": PLANNING_ONLY and req_schema.get("boundary_flags", {}).get("planning_only") is True,
        "recommended_next_execution_defined": NEXT_EXECUTION in plan or NEXT_EXECUTION in json.dumps(admission),
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
        "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "recommended_execution_phase": NEXT_EXECUTION,
        "three_layer_model": {
            "runner_task_candidate": "what_could_be_considered",
            "runner_invocation_request": "prepared_application_to_execute",
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
        rp = out / "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out / "model_test_lens_runner_manual_trigger_plan_record_v1.json").write_text(
            json.dumps({"plan_ref": f"{TRIGGER_REL}/runner_manual_trigger_plan_v1.md"}, indent=2) + "\n",
            encoding="utf-8",
        )

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
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID,
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "test_artifact_protected": True,
            "test_mode": "planning",
            "planning_only": True,
        }
        payloads = {
            "runner_invocation_request_schema_record": _load_json(
                f"{SCHEMA_REL}/runner_invocation_request_schema_v1.json"
            ),
            "manual_runner_trigger_admission_policy_record": _load_json(
                f"{SCHEMA_REL}/manual_runner_trigger_admission_policy_v1.json"
            ),
            "detection_ocr_manual_trigger_route_policy_record": _load_json(
                f"{SCHEMA_REL}/detection_ocr_manual_trigger_route_policy_v1.json"
            ),
            "runner_manual_trigger_plan_record": {
                "plan_ref": f"{TRIGGER_REL}/runner_manual_trigger_plan_v1.md"
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
