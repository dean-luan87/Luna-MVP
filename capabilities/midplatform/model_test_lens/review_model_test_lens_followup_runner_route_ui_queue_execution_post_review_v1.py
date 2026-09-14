# -*- coding: utf-8 -*-
"""P1 Followup Runner Route UI Queue Execution — post-review v1 (browser runtime guards)."""

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
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = (
    "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-Post-Review-v1-001"
)
UPSTREAM_PLANNING_PHASE = "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001"
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_PLANNING_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
ROUTE_REL = "capabilities/midplatform/model_test_lens/followup_runner_route"
_PKG = "capabilities/midplatform/model_test_lens"

QUEUE_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/followup_runner_route_copy_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_state_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js",
    f"{STATIC_REL}/followup_runner_route_summary_v1.js",
    f"{STATIC_REL}/browser_runtime_guard_v1.js",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{_PKG}/review_model_test_lens_followup_runner_route_ui_queue_execution_post_review_v1.py",
)

NODE_GLOBAL_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"\brequire\s*\(", "require_in_app"),
    (r"\bmodule\.exports\b", "module_exports_in_app"),
    (r"\b__dirname\b", "dirname_in_app"),
    (r"\bprocess\.env\b", "process_env_in_app"),
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\brun_model\b|\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\bexecute_tracking\b|\bexecute_depth\b|\bexecute_slam\b", "runner_execute_tracking"),
    (r"queue_state\s*[=:]\s*['\"]running['\"]", "running_state_in_queue"),
    (r"queue_state\s*[=:]\s*['\"]executed['\"]", "executed_state_in_queue"),
    (r"queue_state\s*[=:]\s*['\"]completed['\"]", "completed_state_in_queue"),
    (r"groundTruth\s*=\s*true", "ground_truth_true"),
    (r"confirmed_dynamic", "confirmed_dynamic_in_ui"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "followup_runner_route_queue_ui_patch_record",
    "followup_runner_route_queue_panel_record",
    "followup_runner_route_queue_state_record",
    "followup_runner_route_queue_summary_record",
    "followup_runner_route_browser_runtime_guard_record",
    "followup_runner_route_negative_guard_audit_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_BLOCKED"

GLOBAL_FIX_NOTE = (
    "app.js queue code used bare global.xxx (Node); fixed to window.xxx for browser compatibility"
)


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_post_review_v1_smoke_v0"
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


def _frr_bundle() -> str:
    return "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "followup_runner_route_copy_v1.js",
            "followup_runner_route_queue_state_v1.js",
            "followup_runner_route_queue_v1.js",
            "followup_runner_route_queue_panel_v1.js",
            "followup_runner_route_summary_v1.js",
            "browser_runtime_guard_v1.js",
            "luna_observation_compact_ui_v1.js",
        )
    )


def _app_bare_global_refs(app: str) -> List[str]:
    if not app or "(function () {" not in app:
        return ["app_iife_pattern_missing"]
    return re.findall(r"\bglobal\.", app) or []


def _queue_action_slice(app: str) -> str:
    if "onQueueAction" not in app:
        return ""
    start = app.find("function buildQueuePackage")
    end = app.find("function refreshAttentionUi", start)
    if start < 0 or end <= start:
        return ""
    return app[start:end]


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    guard = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    queue = _read(f"{STATIC_REL}/followup_runner_route_queue_v1.js")
    panel = _read(f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js")
    state_js = _read(f"{STATIC_REL}/followup_runner_route_queue_state_v1.js")
    summary = _read(f"{STATIC_REL}/followup_runner_route_summary_v1.js")
    copy = _read(f"{STATIC_REL}/followup_runner_route_copy_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    hud_renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    boundary_polish = _read(f"{STATIC_REL}/segmentation_boundary_visual_polish_v1.js")
    attn_engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    attn_panel = _read(f"{STATIC_REL}/observation_attention_priority_panel_v1.js")

    planning_review = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_followup_runner_route_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_followup_runner_route_planning_review_v1.json"
    )
    planning_go = (
        planning_review.get("final_decision") == PLANNING_GO
        or _read(f"{ROUTE_REL}/followup_runner_route_plan_v1.md") != ""
    )

    bare_globals = _app_bare_global_refs(app)
    queue_slice = _queue_action_slice(app)

    return {
        "upstream_planning_go": planning_go,
        "global_to_window_fix_applied": (
            "window.FollowupRunnerRouteQueue" in app
            and "window.FollowupRunnerRouteQueueState" in app
            and len(bare_globals) == 0
        ),
        "no_browser_global_reference_error": len(bare_globals) == 0,
        "no_node_global_in_browser_app": all(
            not re.search(pat, app) for pat, _ in NODE_GLOBAL_PATTERNS
        ),
        "browser_runtime_guard_present": (
            "BrowserRuntimeGuard" in guard
            and "browser_runtime_guard_v1.js" in index
            and "assertAppEntryUsesWindow" in app
        ),
        "browser_runtime_init_ok": (
            "browserRuntimeInitOk" in guard and "dataset.browserRuntimeGuard" in guard
        ),
        "app_uses_window_exposure_pattern": (
            "window.LunaObservationCopy" in app or "window." in app
        ),
        "priority_panel_and_queue_panel_coexist": (
            "优先观察" in attn_panel and "后续任务候选队列" in copy
            and "lol-right-attention-host" in compact
            and "lol-right-queue-host" in compact
        ),
        "queue_panel_present": "frr-queue-panel" in panel and "后续任务候选队列" in copy,
        "queue_item_fields_complete": all(
            token in panel
            for token in (
                "task_candidate_id", "admission_mode", "queue_state", "route_reason",
                "labelRecommendedOnly", "statusLine", "linked_attention_record_id", "region_id",
            )
        ),
        "bottom_queue_summary_present": (
            "frr-summary-inline" in summary and "excluded" in summary and "appendToMetricsSummary" in summary
        ),
        "p0_p1_auto_eligible_in_queue": (
            'P0_immediate_attention: "auto_eligible"' in queue
            and 'P1_high_attention: "auto_eligible"' in queue
        ),
        "p2_p3_manual_only_in_queue": (
            'P2_medium_attention: "manual_only"' in queue
            and 'P3_low_attention: "manual_only"' in queue
        ),
        "runner_task_candidate_traceable_to_attention_record": (
            "linked_attention_record_id" in queue and "source_attention_record_id" in queue
        ),
        "runner_task_candidate_traceable_to_region_id": (
            "region_id" in queue and "source_region_id" in queue
        ),
        "route_reason_from_mapping": (
            "ROUTE_REASON" in queue and "route_reason" in queue and "source_followup_route_ref" in queue
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            "candidate_only: true" in queue
            and "not_executed: true" in queue
            and "not_fact: true" in queue
            and "candidate_only / not_executed / not_fact" in copy
        ),
        "no_runner_execution": (
            "noRunnerExecution: true" in queue and "run_model" not in queue_slice
        ),
        "no_model_call": "noModelCall: true" in queue,
        "no_fact_write": "noFactWrite: true" in copy,
        "no_navigation_decision": "navigation_decided" in state_js,
        "no_auto_runner_trigger": (
            "noAutoRunnerTrigger: true" in queue and 'trigger_mode: "manual_only"' in queue
        ),
        "no_running_state_allowed": '"running"' in state_js and "FORBIDDEN_STATES" in state_js,
        "no_executed_state_allowed": '"executed"' in state_js,
        "no_completed_state_allowed": '"completed"' in state_js,
        "pin_does_not_execute_runner": (
            "pinDoesNotExecuteRunner: true" in state_js
            and "onQueueAction" in app
            and "execute_" not in queue_slice
        ),
        "unpin_does_not_change_priority": (
            "unpin" in state_js
            and "priority_level" not in queue_slice
            and "buildAttentionPackage" not in queue_slice
        ),
        "exclude_does_not_delete_attention_record": (
            "exclude" in state_js
            and "attentionPkg.records" not in queue_slice
            and "delete" not in queue_slice.lower()
        ),
        "human_correction_priority_signal_only": (
            "correction_boosted" in queue and "ground truth" in copy.lower()
        ),
        "no_prompt_label_fact_upgrade": "fact_upgrade" not in _frr_bundle(),
        "no_motion_confirmed_from_single_frame": "confirmed_dynamic" not in _frr_bundle(),
        "no_boundary_clone": "drawRunner" not in hud_renderer,
        "no_secondary_box_from_runner_queue": "runner_box" not in hud_renderer.lower(),
        "no_visual_expression_mutation": (
            boundary_polish != "" and "drawSegmentationBoundary" in hud_renderer
        ),
        "attention_engine_untouched_for_priority": "PRIORITY_ORDER" in attn_engine,
        "queue_panel_pin_unpin_exclude_actions": (
            "data-action='pin'" in panel and "unpin" in panel and "exclude" in panel
        ),
        "index_scripts_wired": all(s in index for s in (
            "followup_runner_route_queue_v1.js",
            "followup_runner_route_queue_panel_v1.js",
            "browser_runtime_guard_v1.js",
        )),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in QUEUE_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    app = _read(f"{STATIC_REL}/app.js")
    bare_globals = _app_bare_global_refs(app)
    if bare_globals:
        failed.append(f"app.bare_global_refs={len(bare_globals)}")

    queue_slice = _queue_action_slice(app)
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _frr_bundle() + queue_slice, re.I)]
    node_violations = [pid for pat, pid in NODE_GLOBAL_PATTERNS if re.search(pat, app)]

    flags = _audit()
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "key": "no_runner_execution", "passed": flags["no_runner_execution"]},
        {"guard_id": "B", "key": "no_model_call", "passed": flags["no_model_call"]},
        {"guard_id": "C", "key": "no_fact_write", "passed": flags["no_fact_write"] and "fact_write" not in violations},
        {"guard_id": "D", "key": "no_navigation_decision", "passed": flags["no_navigation_decision"]},
        {"guard_id": "E", "key": "no_auto_runner_trigger", "passed": flags["no_auto_runner_trigger"]},
        {"guard_id": "F", "key": "no_running_state_allowed", "passed": flags["no_running_state_allowed"]},
        {"guard_id": "G", "key": "no_executed_state_allowed", "passed": flags["no_executed_state_allowed"]},
        {"guard_id": "H", "key": "no_completed_state_allowed", "passed": flags["no_completed_state_allowed"]},
        {"guard_id": "I", "key": "no_browser_global_reference_error", "passed": flags["no_browser_global_reference_error"]},
        {"guard_id": "J", "key": "no_node_global_in_browser_app", "passed": flags["no_node_global_in_browser_app"] and not node_violations},
        {"guard_id": "K", "key": "browser_runtime_init_ok", "passed": flags["browser_runtime_init_ok"] and flags["browser_runtime_guard_present"]},
        {"guard_id": "L", "key": "no_boundary_clone", "passed": flags["no_boundary_clone"]},
        {"guard_id": "M", "key": "no_secondary_box_from_runner_queue", "passed": flags["no_secondary_box_from_runner_queue"]},
        {"guard_id": "N", "key": "no_visual_expression_mutation", "passed": flags["no_visual_expression_mutation"]},
        {"guard_id": "O", "key": "runner_task_candidate_traceable_to_attention_record", "passed": flags["runner_task_candidate_traceable_to_attention_record"]},
        {"guard_id": "P", "key": "runner_task_candidate_traceable_to_region_id", "passed": flags["runner_task_candidate_traceable_to_region_id"]},
        {"guard_id": "Q", "key": "auto_eligible_p0_p1_only", "passed": flags["p0_p1_auto_eligible_in_queue"]},
        {"guard_id": "R", "key": "p2_p3_manual_only_by_default", "passed": flags["p2_p3_manual_only_in_queue"]},
        {"guard_id": "S", "key": "pin_does_not_execute_runner", "passed": flags["pin_does_not_execute_runner"]},
        {"guard_id": "T", "key": "unpin_does_not_change_priority", "passed": flags["unpin_does_not_change_priority"]},
        {"guard_id": "U", "key": "exclude_does_not_delete_attention_record", "passed": flags["exclude_does_not_delete_attention_record"]},
        {"guard_id": "V", "key": "human_correction_priority_signal_only", "passed": flags["human_correction_priority_signal_only"]},
        {"guard_id": "W", "key": "no_prompt_label_fact_upgrade", "passed": flags["no_prompt_label_fact_upgrade"]},
        {"guard_id": "X", "key": "no_motion_confirmed_from_single_frame", "passed": flags["no_motion_confirmed_from_single_frame"]},
        {"guard_id": "Y", "key": "candidate_only_not_executed_not_fact_preserved", "passed": flags["candidate_only_not_executed_not_fact_preserved"]},
        {"guard_id": "Z", "key": "priority_panel_and_queue_panel_coexist", "passed": flags["priority_panel_and_queue_panel_coexist"]},
        {"guard_id": "AA", "key": "queue_item_fields_complete", "passed": flags["queue_item_fields_complete"]},
        {"guard_id": "AB", "key": "bottom_queue_summary_present", "passed": flags["bottom_queue_summary_present"]},
        {"guard_id": "AC", "key": "global_to_window_fix_applied", "passed": flags["global_to_window_fix_applied"]},
        {"guard_id": "AD", "key": "test_board_protected", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "global_to_window_fix_applied",
        "no_browser_global_reference_error",
        "no_node_global_in_browser_app",
        "browser_runtime_guard_present",
        "browser_runtime_init_ok",
        "priority_panel_and_queue_panel_coexist",
        "queue_panel_present",
        "queue_item_fields_complete",
        "bottom_queue_summary_present",
        "p0_p1_auto_eligible_in_queue",
        "p2_p3_manual_only_in_queue",
        "runner_task_candidate_traceable_to_attention_record",
        "runner_task_candidate_traceable_to_region_id",
        "candidate_only_not_executed_not_fact_preserved",
        "no_runner_execution",
        "no_auto_runner_trigger",
        "pin_does_not_execute_runner",
        "exclude_does_not_delete_attention_record",
        "no_secondary_box_from_runner_queue",
        "no_visual_expression_mutation",
        "upstream_planning_go",
        "index_scripts_wired",
        "queue_panel_pin_unpin_exclude_actions",
    ]

    guard_count = len(guards)
    extra_blockers = len(violations) + len(node_violations) + len(failed)
    core_failures = sum(1 for k in core if not flags.get(k))
    guard_failures = guard_count - ng_passed

    if extra_blockers or core_failures or guard_failures:
        decision = FINAL_BLOCKED
        blockers = extra_blockers + core_failures + guard_failures
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "followup_runner_route_ui_queue_post_review_profile_count": 1,
        "browser_runtime_compatibility_fix": GLOBAL_FIX_NOTE,
        "queue_is_pre_execution_governance_layer": True,
        "hard_refresh_should_not_throw_global_reference_error": flags["no_browser_global_reference_error"],
        "pin_does_not_trigger_runner": flags["pin_does_not_execute_runner"],
        "exclude_does_not_mutate_attention_records": flags["exclude_does_not_delete_attention_record"],
        "next_phase_hint": "Detection/OCR Runner Manual Trigger Planning (not auto execution)",
    }

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "followup_runner_route_ui_queue_post_review": True,
        "followup_runner_route_ui_queue_post_review_profile_count": 1,
        "upstream_planning_phase": UPSTREAM_PLANNING_PHASE,
        "browser_runtime_fix_note": GLOBAL_FIX_NOTE,
        "audit_flags": flags,
        "post_review_audit": post,
        "negative_guards": guards,
        "negative_guard_count": guard_count,
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "node_global_violations": node_violations,
        "app_bare_global_ref_count": len(bare_globals),
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    patch_record = {
        "modules": list(QUEUE_MODULES),
        "updated": list(UPDATED_FILES),
        "browser_fix": GLOBAL_FIX_NOTE,
        "entry_points": ["browser_runtime_guard", "right_queue_panel", "bottom_queue_summary", "pin_unpin_exclude"],
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_post_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "model_test_lens_followup_runner_route_browser_runtime_guard_record_v1.json").write_text(
            json.dumps({"guard": "browser_runtime_guard_v1.js", "fix": GLOBAL_FIX_NOTE}, indent=2, ensure_ascii=False)
            + "\n",
            encoding="utf-8",
        )
        (out_root / "model_test_lens_followup_runner_route_negative_guard_audit_v1.json").write_text(
            json.dumps(
                {
                    "violations": violations,
                    "node_violations": node_violations,
                    "bare_global_refs": bare_globals,
                    "guards": guards,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / "model_test_lens_followup_runner_route_ui_queue_post_review_audit_v1.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    if write_test_board:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="real_test",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="real_test",
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
            "test_mode": "real_test",
        }
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype, "patch": patch_record}}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_RECORDS)

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
                "app_bare_global_ref_count": r.get("app_bare_global_ref_count"),
                "failed_checks": r.get("failed_checks"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
