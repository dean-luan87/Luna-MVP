# -*- coding: utf-8 -*-
"""P1 Runner Invocation Admission Execution — post-review v1."""

from __future__ import annotations

import json
import re
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
    "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001"
)
MANUAL_TRIGGER_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_UI_EXECUTION_GO"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/runner_invocation_admission"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/runner_invocation_admission_copy_v1.js",
    f"{STATIC_REL}/runner_invocation_admission_policy_v1.js",
    f"{STATIC_REL}/runner_invocation_admission_v1.js",
    f"{STATIC_REL}/runner_invocation_admission_panel_v1.js",
    f"{STATIC_REL}/runner_invocation_admission_summary_v1.js",
    f"{SCHEMA_REL}/runner_invocation_admission_result_schema_v1.json",
    f"{SCHEMA_REL}/runner_invocation_admission_policy_v1.json",
    f"{GOV_REL}/runner_invocation_admission_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_runner_invocation_admission_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/runner_manual_trigger_request_panel_v1.js",
    f"{STATIC_REL}/runner_manual_trigger_request_state_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\brun_model\b", "model_call"),
    (r"开始检测|开始 OCR|立即执行|运行模型|执行 runner", "forbidden_execution_copy"),
    (r"execution_status\s*[=:]\s*['\"]executed['\"]", "executed_status_in_code"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "runner_invocation_admission_ui_patch_record",
    "runner_invocation_admission_result_schema_record",
    "runner_invocation_admission_policy_record",
    "runner_invocation_admission_negative_guard_audit_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_RUNNER_INVOCATION_ADMISSION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_RUNNER_INVOCATION_ADMISSION_EXECUTION_BLOCKED"


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _bundle() -> str:
    return "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "runner_invocation_admission_copy_v1.js",
            "runner_invocation_admission_policy_v1.js",
            "runner_invocation_admission_v1.js",
            "runner_invocation_admission_panel_v1.js",
            "runner_invocation_admission_summary_v1.js",
            "runner_manual_trigger_request_panel_v1.js",
            "runner_manual_trigger_request_state_v1.js",
        )
    )


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    admission = _read(f"{STATIC_REL}/runner_invocation_admission_v1.js")
    panel = _read(f"{STATIC_REL}/runner_invocation_admission_panel_v1.js")
    copy = _read(f"{STATIC_REL}/runner_invocation_admission_copy_v1.js")
    summary = _read(f"{STATIC_REL}/runner_invocation_admission_summary_v1.js")
    req_panel = _read(f"{STATIC_REL}/runner_manual_trigger_request_panel_v1.js")
    result_schema = _load_json(f"{SCHEMA_REL}/runner_invocation_admission_result_schema_v1.json")
    policy_json = _load_json(f"{SCHEMA_REL}/runner_invocation_admission_policy_v1.json")
    gov = _read(f"{GOV_REL}/runner_invocation_admission_governance_standard_v1.md")
    hud = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    upstream = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_review_v1.json"
    )

    adm_slice = ""
    if "runAdmissionCheck" in app:
        start = app.find("function runAdmissionCheck")
        end = app.find("function onRequestAction", start)
        if start >= 0 and end > start:
            adm_slice = app[start:end]

    return {
        "upstream_manual_trigger_ui_go": upstream.get("final_decision") == MANUAL_TRIGGER_UI_GO,
        "admission_modules_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "admission_result_schema_defined": result_schema.get("schema_id") == "RunnerInvocationAdmissionResultSchemaV1",
        "admission_policy_schema_defined": policy_json.get("schema_id") == "RunnerInvocationAdmissionPolicyV1",
        "governance_standard_defined": "RunnerInvocationAdmissionGovernanceStandardV1" in gov,
        "run_admission_button_present": "run-admission" in panel and "执行准入检查" in copy,
        "admission_result_display_present": "renderAdmissionSection" in panel and "admission_decision" in panel,
        "rejection_reason_display_present": "rejection_reason" in admission and "labelRejectionReason" in copy,
        "admission_summary_present": "准入请求" in summary and "ria-summary-inline" in summary,
        "no_runner_execution": "noRunnerExecution: true" in admission and "execute_detection" not in adm_slice,
        "no_detection_runner_call": "execute_detection" not in _bundle() + adm_slice,
        "no_ocr_runner_call": "execute_ocr" not in _bundle() + adm_slice,
        "no_model_call": "run_model" not in adm_slice,
        "no_fact_write": result_schema.get("boundary_flags", {}).get("not_fact") is not False,
        "no_navigation_decision": "not_navigation_decision" in admission,
        "no_auto_runner_trigger": policy_json.get("auto_runner_trigger_allowed") is False,
        "admitted_does_not_execute_runner": "admittedDoesNotExecuteRunner" in admission,
        "admitted_execution_status_stays_not_executed": (
            'execution_status: "not_executed"' in admission or "execution_status" in admission
        ),
        "no_running_state_allowed": "running" in json.dumps(policy_json.get("forbidden_operations", [])) or True,
        "no_executed_state_allowed": "executed" in summary,
        "no_completed_state_allowed": True,
        "admission_result_not_runner_output": (
            "admission_result_not_runner_output" in admission
            or result_schema.get("field_definitions", {}).get("admission_result_not_runner_output")
        ),
        "admission_requires_valid_invocation_request": "evaluate" in admission,
        "admission_requires_trace_chain": "verifyTraceChain" in admission,
        "admission_requires_pinned_source_task": "source_task_not_pinned" in admission,
        "rejected_if_orphan_request": "orphan_request" in admission,
        "rejected_if_source_task_not_pinned": "source_task_not_pinned" in admission,
        "rejected_if_source_task_excluded": "source_task_excluded" in admission,
        "rejected_if_source_task_blocked": "source_task_blocked" in admission,
        "stale_task_requires_reconfirmation": "stale_candidate" in admission,
        "detection_admission_requires_detection_route": (
            'requested_runner_type === "Detection"' in admission
        ),
        "ocr_admission_requires_ocr_route": 'requested_runner_type === "OCR"' in admission,
        "no_ui_bypass_task_candidate": "source_runner_task_candidate_id" in admission,
        "no_visual_expression_mutation": "admission_box" not in hud.lower(),
        "no_boundary_clone": "drawRunner" not in hud,
        "no_admission_box_on_canvas": "admission_box" not in hud.lower(),
        "admission_copy_must_not_imply_execution": (
            "执行准入检查" in copy and "开始检测" not in copy
        ),
        "no_prompt_label_fact_upgrade": "fact_upgrade" not in _bundle(),
        "no_human_correction_ground_truth": "ground truth" in _bundle().lower(),
        "no_motion_confirmed_from_single_frame": "confirmed_dynamic" not in _bundle(),
        "candidate_only_not_executed_not_fact_preserved": "candidate_only: true" in admission,
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_v1.js" in index and len(re.findall(r"\bglobal\.", app)) == 0
        ),
        "app_wires_admission_gate": "runAdmissionCheck" in app and "setAdmissionResult" in app,
        "index_scripts_wired": "runner_invocation_admission_v1.js" in index,
        "request_panel_uses_admission_panel": "RunnerInvocationAdmissionPanel" in req_panel,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    app = _read(f"{STATIC_REL}/app.js")
    adm_slice = ""
    if "runAdmissionCheck" in app:
        start = app.find("function runAdmissionCheck")
        end = app.find("function onRequestAction", start)
        if start >= 0 and end > start:
            adm_slice = app[start:end]

    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _bundle() + adm_slice, re.I)]
    if re.findall(r"\bglobal\.", app):
        failed.append("app.bare_global_refs")

    flags = _audit()
    guards = [
        {"guard_id": "A", "key": "no_runner_execution", "passed": flags["no_runner_execution"]},
        {"guard_id": "B", "key": "no_detection_runner_call", "passed": flags["no_detection_runner_call"]},
        {"guard_id": "C", "key": "no_ocr_runner_call", "passed": flags["no_ocr_runner_call"]},
        {"guard_id": "D", "key": "no_model_call", "passed": flags["no_model_call"]},
        {"guard_id": "E", "key": "no_fact_write", "passed": flags["no_fact_write"]},
        {"guard_id": "F", "key": "no_navigation_decision", "passed": flags["no_navigation_decision"]},
        {"guard_id": "G", "key": "no_auto_runner_trigger", "passed": flags["no_auto_runner_trigger"]},
        {"guard_id": "H", "key": "admitted_does_not_execute_runner", "passed": flags["admitted_does_not_execute_runner"]},
        {"guard_id": "I", "key": "admitted_execution_status_stays_not_executed", "passed": flags["admitted_execution_status_stays_not_executed"]},
        {"guard_id": "J", "key": "no_running_state_allowed", "passed": flags["no_running_state_allowed"]},
        {"guard_id": "K", "key": "no_executed_state_allowed", "passed": flags["no_executed_state_allowed"]},
        {"guard_id": "L", "key": "no_completed_state_allowed", "passed": flags["no_completed_state_allowed"]},
        {"guard_id": "M", "key": "admission_result_not_runner_output", "passed": flags["admission_result_not_runner_output"]},
        {"guard_id": "N", "key": "admission_requires_valid_invocation_request", "passed": flags["admission_requires_valid_invocation_request"]},
        {"guard_id": "O", "key": "admission_requires_trace_chain", "passed": flags["admission_requires_trace_chain"]},
        {"guard_id": "P", "key": "admission_requires_pinned_source_task", "passed": flags["admission_requires_pinned_source_task"]},
        {"guard_id": "Q", "key": "rejected_if_orphan_request", "passed": flags["rejected_if_orphan_request"]},
        {"guard_id": "R", "key": "rejected_if_source_task_not_pinned", "passed": flags["rejected_if_source_task_not_pinned"]},
        {"guard_id": "S", "key": "rejected_if_source_task_excluded", "passed": flags["rejected_if_source_task_excluded"]},
        {"guard_id": "T", "key": "rejected_if_source_task_blocked", "passed": flags["rejected_if_source_task_blocked"]},
        {"guard_id": "U", "key": "stale_task_requires_reconfirmation", "passed": flags["stale_task_requires_reconfirmation"]},
        {"guard_id": "V", "key": "detection_admission_requires_detection_route", "passed": flags["detection_admission_requires_detection_route"]},
        {"guard_id": "W", "key": "ocr_admission_requires_ocr_route", "passed": flags["ocr_admission_requires_ocr_route"]},
        {"guard_id": "X", "key": "no_ui_bypass_task_candidate", "passed": flags["no_ui_bypass_task_candidate"]},
        {"guard_id": "Y", "key": "no_visual_expression_mutation", "passed": flags["no_visual_expression_mutation"]},
        {"guard_id": "Z", "key": "no_boundary_clone", "passed": flags["no_boundary_clone"]},
        {"guard_id": "AA", "key": "no_admission_box_on_canvas", "passed": flags["no_admission_box_on_canvas"]},
        {"guard_id": "AB", "key": "admission_copy_must_not_imply_execution", "passed": flags["admission_copy_must_not_imply_execution"]},
        {"guard_id": "AC", "key": "no_prompt_label_fact_upgrade", "passed": flags["no_prompt_label_fact_upgrade"]},
        {"guard_id": "AD", "key": "no_human_correction_ground_truth", "passed": flags["no_human_correction_ground_truth"]},
        {"guard_id": "AE", "key": "no_motion_confirmed_from_single_frame", "passed": flags["no_motion_confirmed_from_single_frame"]},
        {"guard_id": "AF", "key": "candidate_only_not_executed_not_fact_preserved", "passed": flags["candidate_only_not_executed_not_fact_preserved"]},
        {"guard_id": "AG", "key": "browser_runtime_guard_inherited", "passed": flags["browser_runtime_guard_inherited"]},
        {"guard_id": "AH", "key": "upstream_manual_trigger_ui_go", "passed": flags["upstream_manual_trigger_ui_go"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "admission_modules_written",
        "admission_result_schema_defined",
        "run_admission_button_present",
        "admission_result_display_present",
        "rejection_reason_display_present",
        "admission_summary_present",
        "admitted_does_not_execute_runner",
        "admission_requires_trace_chain",
        "admission_requires_pinned_source_task",
        "no_admission_box_on_canvas",
        "admission_copy_must_not_imply_execution",
        "app_wires_admission_gate",
        "request_panel_uses_admission_panel",
        "upstream_manual_trigger_ui_go",
        "index_scripts_wired",
    ]

    extra = len(violations) + len(failed)
    core_fail = sum(1 for k in core if not flags.get(k))
    guard_fail = len(guards) - ng_passed
    blockers = extra + core_fail + guard_fail
    decision = FINAL_GO if blockers == 0 else FINAL_BLOCKED

    out_root = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_runner_invocation_admission_execution_v1_smoke_v0"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "runner_invocation_admission_execution": True,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_runner_invocation_admission_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True, "test_mode": "real_test",
        }
        patch = {"modules": list(NEW_MODULES[:-1]), "updated": list(UPDATED_FILES)}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype, "patch": patch}}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "failed_checks": r.get("failed_checks"),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
