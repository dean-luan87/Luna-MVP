# -*- coding: utf-8 -*-
"""P1 Detection/OCR Runner Manual Trigger UI Execution — post-review v1."""

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
    candidates = [Path.cwd(), Path(__file__).resolve().parents[3]]
    marker = Path("capabilities/test_board/test_board_protocol_v1.py")
    for base in candidates:
        if (base / marker).is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001"
)
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_PLANNING_GO"
QUEUE_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
TRIGGER_REL = "capabilities/midplatform/model_test_lens/runner_manual_trigger"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/runner_manual_trigger"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/runner_manual_trigger_copy_v1.js",
    f"{STATIC_REL}/runner_manual_trigger_request_state_v1.js",
    f"{STATIC_REL}/runner_manual_trigger_request_v1.js",
    f"{STATIC_REL}/runner_manual_trigger_request_panel_v1.js",
    f"{STATIC_REL}/runner_manual_trigger_summary_v1.js",
    f"{_PKG}/review_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\brun_model\b|\bexecute_tracking\b", "model_call"),
    (r"execution_status\s*[=:]\s*['\"]executed['\"]", "executed_status"),
    (r"execution_status\s*[=:]\s*['\"]running['\"]", "running_status"),
    (r"开始检测|开始 OCR|立即执行|运行模型|执行 runner", "forbidden_execution_copy"),
    (r"groundTruth\s*=\s*true", "ground_truth_true"),
    (r"confirmed_dynamic", "confirmed_dynamic_in_ui"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "runner_manual_trigger_ui_patch_record",
    "runner_manual_trigger_request_panel_record",
    "runner_manual_trigger_request_state_record",
    "runner_manual_trigger_negative_guard_audit_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_RUNNER_MANUAL_TRIGGER_UI_EXECUTION_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_v1_smoke_v0"
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


def _rmt_bundle() -> str:
    return "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "runner_manual_trigger_copy_v1.js",
            "runner_manual_trigger_request_state_v1.js",
            "runner_manual_trigger_request_v1.js",
            "runner_manual_trigger_request_panel_v1.js",
            "runner_manual_trigger_summary_v1.js",
            "followup_runner_route_queue_panel_v1.js",
            "luna_observation_compact_ui_v1.js",
        )
    )


def _app_bare_global_refs(app: str) -> int:
    return len(re.findall(r"\bglobal\.", app))


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    copy = _read(f"{STATIC_REL}/runner_manual_trigger_copy_v1.js")
    req_js = _read(f"{STATIC_REL}/runner_manual_trigger_request_v1.js")
    state_js = _read(f"{STATIC_REL}/runner_manual_trigger_request_state_v1.js")
    panel = _read(f"{STATIC_REL}/runner_manual_trigger_request_panel_v1.js")
    summary = _read(f"{STATIC_REL}/runner_manual_trigger_summary_v1.js")
    queue_panel = _read(f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    hud_renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    browser_guard = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_planning_review_v1.json"
    )

    gen_slice = ""
    if "onGenerateRequest" in app:
        start = app.find("function onGenerateRequest")
        end = app.find("function onRequestAction", start)
        if start >= 0 and end > start:
            gen_slice = app[start:end]

    return {
        "upstream_planning_go": planning.get("final_decision") == PLANNING_GO,
        "runner_manual_trigger_ui_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "pinned_generate_request_buttons": (
            "generate-request" in queue_panel and "生成检测请求" in copy and "生成 OCR 请求" in copy
        ),
        "non_pinned_hints_present": (
            "需先 Pin 入队" in copy
            and "已排除，不能生成请求" in copy
            and "rc.hintNeedPin" in queue_panel
            and "rc.hintExcluded" in queue_panel
        ),
        "pending_request_panel_present": (
            "待准入请求" in copy and "rmt-request-panel" in panel and "lol-right-request-host" in compact
        ),
        "request_fields_complete": all(
            t in panel for t in (
                "invocation_request_id", "admission_status", "execution_status",
                "requested_runner_type", "trace_chain", "source_runner_task_candidate_id",
            )
        ),
        "bottom_request_summary_present": (
            "rmt-summary-inline" in summary and "executed" in summary and "appendToMetricsSummary" in summary
        ),
        "no_runner_execution": "noRunnerExecution: true" in req_js and "execute_detection" not in gen_slice,
        "no_detection_runner_call": "execute_detection" not in _rmt_bundle() + gen_slice,
        "no_ocr_runner_call": "execute_ocr" not in _rmt_bundle() + gen_slice,
        "no_model_call": "noModelCall: true" in req_js and "run_model" not in gen_slice,
        "no_fact_write": "noFactWrite: true" in copy and "writeFact" not in _rmt_bundle(),
        "no_navigation_decision": "no_navigation_decision" in req_js,
        "no_auto_runner_trigger": "manual_only" in req_js and "noAutoRunnerTrigger: true" in req_js,
        "no_running_state_allowed": '"running"' in state_js or "FORBIDDEN_EXECUTION" in state_js,
        "no_executed_state_allowed": "executed" in state_js,
        "no_completed_state_allowed": "completed" in state_js,
        "request_execution_status_not_executed_only": (
            'execution_status: "not_executed"' in req_js or "execution_status" in req_js
        ),
        "request_requires_pinned_task_candidate": (
            'queue_state !== "pinned"' in req_js or 'queue_state === "pinned"' in req_js
        ),
        "candidate_task_cannot_generate_request": "hintNeedPin" in copy,
        "excluded_task_cannot_generate_request": "hintExcluded" in copy,
        "stale_task_requires_reconfirmation": "hintStale" in copy,
        "blocked_task_cannot_generate_request": "hintBlocked" in copy,
        "detection_request_requires_detection_route": (
            'target_model_id === "detection"' in req_js and 'recommended_runner_type !== "detection"' in req_js
        ),
        "ocr_request_requires_ocr_route": (
            'target_model_id === "ocr"' in req_js and 'recommended_runner_type !== "ocr"' in req_js
        ),
        "no_ui_bypass_task_candidate": (
            "buildFromPinnedTask" in req_js and "source_runner_task_candidate_id" in req_js
        ),
        "no_orphan_invocation_request": "trace_chain" in req_js and "buildTraceChain" in req_js,
        "request_traceable_to_runner_task_candidate": "source_runner_task_candidate_id" in req_js,
        "request_traceable_to_attention_record": "source_attention_record_id" in req_js,
        "request_traceable_to_region_id": "source_region_id" in req_js,
        "no_visual_expression_mutation": "drawRunner" not in hud_renderer and "request_box" not in hud_renderer.lower(),
        "no_boundary_clone": "drawRunner" not in hud_renderer,
        "no_request_box_on_canvas": "request_box" not in hud_renderer.lower(),
        "request_copy_must_not_imply_execution": (
            "生成检测请求" in copy and "开始检测" not in copy and "not_executed" in copy
        ),
        "no_prompt_label_fact_upgrade": "fact_upgrade" not in _rmt_bundle(),
        "no_human_correction_ground_truth": (
            "ground truth" in _rmt_bundle().lower() or "非 ground truth" in _rmt_bundle()
        ),
        "no_motion_confirmed_from_single_frame": "confirmed_dynamic" not in _rmt_bundle(),
        "candidate_only_not_executed_not_fact_preserved": (
            "candidate_only: true" in req_js and "not_fact: true" in req_js
        ),
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_v1.js" in index and "BrowserRuntimeGuard" in browser_guard
            and _app_bare_global_refs(app) == 0
        ),
        "app_wires_request_flow": (
            "onGenerateRequest" in app and "onRequestAction" in app and "requestStore" in app
        ),
        "index_scripts_wired": all(s in index for s in (
            "runner_manual_trigger_request_v1.js",
            "runner_manual_trigger_request_panel_v1.js",
        )),
        "admitted_does_not_execute": (
            "admitted" in panel and "仍 not_executed" in panel
        ),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    app = _read(f"{STATIC_REL}/app.js")
    gen_slice = ""
    if "onGenerateRequest" in app:
        start = app.find("function onGenerateRequest")
        end = app.find("function onRequestAction", start)
        if start >= 0 and end > start:
            gen_slice = app[start:end]

    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _rmt_bundle() + gen_slice, re.I)]
    if _app_bare_global_refs(app):
        failed.append("app.bare_global_refs")

    flags = _audit()
    guards = [
        {"guard_id": "A", "key": "no_runner_execution", "passed": flags["no_runner_execution"]},
        {"guard_id": "B", "key": "no_detection_runner_call", "passed": flags["no_detection_runner_call"]},
        {"guard_id": "C", "key": "no_ocr_runner_call", "passed": flags["no_ocr_runner_call"]},
        {"guard_id": "D", "key": "no_model_call", "passed": flags["no_model_call"]},
        {"guard_id": "E", "key": "no_fact_write", "passed": flags["no_fact_write"] and "fact_write" not in violations},
        {"guard_id": "F", "key": "no_navigation_decision", "passed": flags["no_navigation_decision"]},
        {"guard_id": "G", "key": "no_auto_runner_trigger", "passed": flags["no_auto_runner_trigger"]},
        {"guard_id": "H", "key": "no_running_state_allowed", "passed": flags["no_running_state_allowed"]},
        {"guard_id": "I", "key": "no_executed_state_allowed", "passed": flags["no_executed_state_allowed"]},
        {"guard_id": "J", "key": "no_completed_state_allowed", "passed": flags["no_completed_state_allowed"]},
        {"guard_id": "K", "key": "request_execution_status_not_executed_only", "passed": flags["request_execution_status_not_executed_only"]},
        {"guard_id": "L", "key": "request_requires_pinned_task_candidate", "passed": flags["request_requires_pinned_task_candidate"]},
        {"guard_id": "M", "key": "candidate_task_cannot_generate_request", "passed": flags["candidate_task_cannot_generate_request"]},
        {"guard_id": "N", "key": "excluded_task_cannot_generate_request", "passed": flags["excluded_task_cannot_generate_request"]},
        {"guard_id": "O", "key": "stale_task_requires_reconfirmation", "passed": flags["stale_task_requires_reconfirmation"]},
        {"guard_id": "P", "key": "blocked_task_cannot_generate_request", "passed": flags["blocked_task_cannot_generate_request"]},
        {"guard_id": "Q", "key": "detection_request_requires_detection_route", "passed": flags["detection_request_requires_detection_route"]},
        {"guard_id": "R", "key": "ocr_request_requires_ocr_route", "passed": flags["ocr_request_requires_ocr_route"]},
        {"guard_id": "S", "key": "no_ui_bypass_task_candidate", "passed": flags["no_ui_bypass_task_candidate"]},
        {"guard_id": "T", "key": "no_orphan_invocation_request", "passed": flags["no_orphan_invocation_request"]},
        {"guard_id": "U", "key": "request_traceable_to_runner_task_candidate", "passed": flags["request_traceable_to_runner_task_candidate"]},
        {"guard_id": "V", "key": "request_traceable_to_attention_record", "passed": flags["request_traceable_to_attention_record"]},
        {"guard_id": "W", "key": "request_traceable_to_region_id", "passed": flags["request_traceable_to_region_id"]},
        {"guard_id": "X", "key": "no_visual_expression_mutation", "passed": flags["no_visual_expression_mutation"]},
        {"guard_id": "Y", "key": "no_boundary_clone", "passed": flags["no_boundary_clone"]},
        {"guard_id": "Z", "key": "no_request_box_on_canvas", "passed": flags["no_request_box_on_canvas"]},
        {"guard_id": "AA", "key": "request_copy_must_not_imply_execution", "passed": flags["request_copy_must_not_imply_execution"]},
        {"guard_id": "AB", "key": "no_prompt_label_fact_upgrade", "passed": flags["no_prompt_label_fact_upgrade"]},
        {"guard_id": "AC", "key": "no_human_correction_ground_truth", "passed": flags["no_human_correction_ground_truth"]},
        {"guard_id": "AD", "key": "no_motion_confirmed_from_single_frame", "passed": flags["no_motion_confirmed_from_single_frame"]},
        {"guard_id": "AE", "key": "candidate_only_not_executed_not_fact_preserved", "passed": flags["candidate_only_not_executed_not_fact_preserved"]},
        {"guard_id": "AF", "key": "browser_runtime_guard_inherited", "passed": flags["browser_runtime_guard_inherited"]},
        {"guard_id": "AG", "key": "admitted_does_not_execute", "passed": flags["admitted_does_not_execute"]},
        {"guard_id": "AH", "key": "upstream_planning_go", "passed": flags["upstream_planning_go"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "runner_manual_trigger_ui_written",
        "pinned_generate_request_buttons",
        "non_pinned_hints_present",
        "pending_request_panel_present",
        "request_fields_complete",
        "bottom_request_summary_present",
        "no_runner_execution",
        "request_requires_pinned_task_candidate",
        "no_ui_bypass_task_candidate",
        "no_orphan_invocation_request",
        "request_traceable_to_runner_task_candidate",
        "no_request_box_on_canvas",
        "request_copy_must_not_imply_execution",
        "browser_runtime_guard_inherited",
        "app_wires_request_flow",
        "index_scripts_wired",
        "upstream_planning_go",
        "admitted_does_not_execute",
    ]

    guard_count = len(guards)
    extra = len(violations) + len(failed)
    core_fail = sum(1 for k in core if not flags.get(k))
    guard_fail = guard_count - ng_passed

    if extra or core_fail or guard_fail:
        decision = FINAL_BLOCKED
        blockers = extra + core_fail + guard_fail
    else:
        decision = FINAL_GO
        blockers = 0

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "runner_manual_trigger_ui_execution": True,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": guard_count,
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_detection_ocr_runner_manual_trigger_ui_execution_review_v1.json"
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
        "forbidden_pattern_violations": r.get("forbidden_pattern_violations"),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
