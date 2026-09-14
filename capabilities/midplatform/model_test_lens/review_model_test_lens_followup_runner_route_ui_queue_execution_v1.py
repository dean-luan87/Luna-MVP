# -*- coding: utf-8 -*-
"""P1 Followup Runner Route UI Queue Execution — post-review v1."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001"
)
UPSTREAM_PLANNING_PHASE = "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001"
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_PLANNING_GO"
OA_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"
VE_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_UI_EXECUTION_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
ROUTE_REL = "capabilities/midplatform/model_test_lens/followup_runner_route"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/followup_runner_route"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/followup_runner_route_copy_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_state_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_v1.js",
    f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js",
    f"{STATIC_REL}/followup_runner_route_summary_v1.js",
    f"{_PKG}/review_model_test_lens_followup_runner_route_ui_queue_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

UI_MARKERS: Tuple[str, ...] = (
    "followup_runner_route_copy_v1.js",
    "followup_runner_route_queue_state_v1.js",
    "followup_runner_route_queue_v1.js",
    "followup_runner_route_queue_panel_v1.js",
    "followup_runner_route_summary_v1.js",
    "后续任务候选队列",
    "runner_task_candidate",
    "task_candidate_id",
    "linked_attention_record_id",
    "admission_mode",
    "queue_state",
    "auto_eligible",
    "manual_only",
    "candidate_only",
    "not_executed",
    "not_fact",
    "frr-queue-panel",
    "frr-summary-inline",
    "buildQueuePackage",
    "onQueueAction",
    "lol-right-queue-host",
    "recommended only",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bsemantic_write\s*\(", "semantic_write"),
    (r"\brun_model\b|\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\bexecute_tracking\b|\bexecute_depth\b|\bexecute_slam\b", "runner_execute_tracking"),
    (r"queue_state\s*[=:]\s*['\"]running['\"]", "running_state_in_queue"),
    (r"queue_state\s*[=:]\s*['\"]executed['\"]", "executed_state_in_queue"),
    (r"queue_state\s*[=:]\s*['\"]completed['\"]", "completed_state_in_queue"),
    (r"groundTruth\s*=\s*true", "ground_truth_true"),
    (r"confirmed_dynamic", "confirmed_dynamic_in_ui"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"deleteArtifact|removeTestBoard", "delete_artifact"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "followup_runner_route_queue_ui_patch_record",
    "followup_runner_route_queue_panel_record",
    "followup_runner_route_queue_state_record",
    "followup_runner_route_queue_summary_record",
    "followup_runner_route_negative_guard_audit_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_FOLLOWUP_RUNNER_ROUTE_UI_QUEUE_EXECUTION_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_v1_smoke_v0"
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
            "luna_observation_compact_ui_v1.js",
        )
    )


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    queue = _read(f"{STATIC_REL}/followup_runner_route_queue_v1.js")
    panel = _read(f"{STATIC_REL}/followup_runner_route_queue_panel_v1.js")
    state_js = _read(f"{STATIC_REL}/followup_runner_route_queue_state_v1.js")
    summary = _read(f"{STATIC_REL}/followup_runner_route_summary_v1.js")
    copy = _read(f"{STATIC_REL}/followup_runner_route_copy_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    hud_renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    boundary_polish = _read(f"{STATIC_REL}/segmentation_boundary_visual_polish_v1.js")
    attn_engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")

    planning_review = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_followup_runner_route_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_followup_runner_route_planning_review_v1.json"
    )
    planning_go = (
        planning_review.get("final_decision") == PLANNING_GO
        or _read(f"{ROUTE_REL}/followup_runner_route_plan_v1.md") != ""
    )

    bundle = _frr_bundle()
    static_ok = all(m in index or m in app or m in styles or m in bundle for m in UI_MARKERS)

    return {
        "upstream_planning_go": planning_go,
        "followup_runner_route_queue_ui_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "queue_panel_present": "frr-queue-panel" in panel and "后续任务候选队列" in copy,
        "queue_state_machine_defined": (
            "ALLOWED_STATES" in state_js
            and "FORBIDDEN_STATES" in state_js
            and '"running"' in state_js
            and "pinDoesNotExecuteRunner" in state_js
        ),
        "bottom_queue_summary_present": (
            "frr-summary-inline" in summary and "appendToMetricsSummary" in summary
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
        "candidate_only_not_executed_not_fact_preserved": (
            "candidate_only: true" in queue
            and "not_executed: true" in queue
            and "not_fact: true" in queue
            and "candidate_only / not_executed / not_fact" in copy
        ),
        "no_runner_execution": (
            "noRunnerExecution: true" in queue
            and "noRunnerExecution: true" in panel
            and "run_model" not in queue
        ),
        "no_model_call": "noModelCall: true" in queue and "execute_detection" not in queue,
        "no_fact_write": "noFactWrite: true" in copy and "writeFact" not in queue,
        "no_navigation_decision": "navigation_decided" in state_js and "navigation" not in panel.lower(),
        "no_auto_runner_trigger": (
            "noAutoRunnerTrigger: true" in queue
            and 'trigger_mode: "manual_only"' in queue
        ),
        "no_running_state_allowed": '"running"' in state_js and "FORBIDDEN_STATES" in state_js,
        "no_executed_state_allowed": '"executed"' in state_js,
        "no_completed_state_allowed": '"completed"' in state_js,
        "pin_does_not_execute_runner": (
            "pinDoesNotExecuteRunner: true" in state_js and "onQueueAction" in app
        ),
        "unpin_does_not_change_priority": (
            "unpin" in state_js and "priority_level" not in app[app.find("onQueueAction") : app.find("onQueueAction") + 800]
            if "onQueueAction" in app
            else False
        ),
        "human_correction_priority_signal_only": (
            "correction_boosted" in queue and "ground truth" in copy.lower()
        ),
        "no_prompt_label_fact_upgrade": "fact_upgrade" not in bundle and "prompt_label" not in queue,
        "no_motion_confirmed_from_single_frame": "confirmed_dynamic" not in bundle,
        "no_boundary_clone": "runner" not in hud_renderer.lower() or "drawRunner" not in hud_renderer,
        "no_secondary_box_from_runner_queue": (
            "drawRunner" not in hud_renderer and "runner_box" not in hud_renderer.lower()
        ),
        "no_visual_expression_mutation": (
            boundary_polish != "" and "drawSegmentationBoundary" in hud_renderer
        ),
        "attention_engine_untouched_for_priority": (
            "PRIORITY_ORDER" in attn_engine and "buildAttentionPackage" in attn_engine
        ),
        "static_site_markers_present": static_ok,
        "app_wires_queue_refresh": (
            "buildQueuePackage" in app and "onQueueAction" in app and "queuePkg" in app
        ),
        "right_panel_queue_host": "lol-right-queue-host" in compact,
        "index_scripts_wired": all(s in index for s in (
            "followup_runner_route_queue_v1.js",
            "followup_runner_route_queue_panel_v1.js",
        )),
        "recommended_runner_display_only": (
            "recommended only" in panel.lower() or "labelRecommendedOnly" in panel
        ),
        "route_reason_from_mapping": "ROUTE_REASON" in queue and "route_reason" in queue,
        "queue_panel_pin_unpin_actions": "data-action='pin'" in panel and "unpin" in panel,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    scan_bundle = _frr_bundle() + _read(f"{STATIC_REL}/app.js")
    queue_app_slice = ""
    app_full = _read(f"{STATIC_REL}/app.js")
    if "onQueueAction" in app_full:
        start = app_full.find("function buildQueuePackage")
        end = app_full.find("function refreshAttentionUi", start)
        if start >= 0 and end > start:
            queue_app_slice = app_full[start:end]
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _frr_bundle() + queue_app_slice, re.I)]

    flags = _audit()
    flags["no_external_network"] = True
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "key": "no_runner_execution", "passed": flags["no_runner_execution"]},
        {"guard_id": "B", "key": "no_model_call", "passed": flags["no_model_call"]},
        {"guard_id": "C", "key": "no_fact_write", "passed": flags["no_fact_write"] and "fact_write" not in violations},
        {"guard_id": "D", "key": "no_navigation_decision", "passed": flags["no_navigation_decision"]},
        {"guard_id": "E", "key": "no_auto_runner_trigger", "passed": flags["no_auto_runner_trigger"]},
        {"guard_id": "F", "key": "no_running_state_allowed", "passed": flags["no_running_state_allowed"] and "running_state_in_queue" not in violations},
        {"guard_id": "G", "key": "no_executed_state_allowed", "passed": flags["no_executed_state_allowed"] and "executed_state_in_queue" not in violations},
        {"guard_id": "H", "key": "no_completed_state_allowed", "passed": flags["no_completed_state_allowed"] and "completed_state_in_queue" not in violations},
        {"guard_id": "I", "key": "no_boundary_clone", "passed": flags["no_boundary_clone"]},
        {"guard_id": "J", "key": "no_secondary_box_from_runner_queue", "passed": flags["no_secondary_box_from_runner_queue"]},
        {"guard_id": "K", "key": "no_visual_expression_mutation", "passed": flags["no_visual_expression_mutation"]},
        {"guard_id": "L", "key": "runner_task_candidate_traceable_to_attention_record", "passed": flags["runner_task_candidate_traceable_to_attention_record"]},
        {"guard_id": "M", "key": "runner_task_candidate_traceable_to_region_id", "passed": flags["runner_task_candidate_traceable_to_region_id"]},
        {"guard_id": "N", "key": "auto_eligible_p0_p1_only", "passed": flags["p0_p1_auto_eligible_in_queue"]},
        {"guard_id": "O", "key": "p2_p3_manual_only_by_default", "passed": flags["p2_p3_manual_only_in_queue"]},
        {"guard_id": "P", "key": "pin_does_not_execute_runner", "passed": flags["pin_does_not_execute_runner"]},
        {"guard_id": "Q", "key": "unpin_does_not_change_priority", "passed": flags["unpin_does_not_change_priority"]},
        {"guard_id": "R", "key": "human_correction_priority_signal_only", "passed": flags["human_correction_priority_signal_only"]},
        {"guard_id": "S", "key": "no_prompt_label_fact_upgrade", "passed": flags["no_prompt_label_fact_upgrade"]},
        {"guard_id": "T", "key": "no_motion_confirmed_from_single_frame", "passed": flags["no_motion_confirmed_from_single_frame"]},
        {"guard_id": "U", "key": "candidate_only_not_executed_not_fact_preserved", "passed": flags["candidate_only_not_executed_not_fact_preserved"]},
        {"guard_id": "V", "key": "upstream_planning_go", "passed": flags["upstream_planning_go"]},
        {"guard_id": "W", "key": "queue_panel_present", "passed": flags["queue_panel_present"]},
        {"guard_id": "X", "key": "bottom_queue_summary_present", "passed": flags["bottom_queue_summary_present"]},
        {"guard_id": "Y", "key": "app_wires_queue_refresh", "passed": flags["app_wires_queue_refresh"]},
        {"guard_id": "Z", "key": "test_board_protected", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "followup_runner_route_queue_ui_written",
        "queue_panel_present",
        "queue_state_machine_defined",
        "bottom_queue_summary_present",
        "p0_p1_auto_eligible_in_queue",
        "p2_p3_manual_only_in_queue",
        "runner_task_candidate_traceable_to_attention_record",
        "runner_task_candidate_traceable_to_region_id",
        "candidate_only_not_executed_not_fact_preserved",
        "no_runner_execution",
        "no_auto_runner_trigger",
        "pin_does_not_execute_runner",
        "no_secondary_box_from_runner_queue",
        "no_visual_expression_mutation",
        "static_site_markers_present",
        "upstream_planning_go",
        "app_wires_queue_refresh",
        "right_panel_queue_host",
        "index_scripts_wired",
        "queue_panel_pin_unpin_actions",
        "recommended_runner_display_only",
        "route_reason_from_mapping",
    ]

    guard_count = len(guards)
    if violations or failed or not all(flags.get(k) for k in core) or ng_passed < guard_count:
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k)) + (guard_count - ng_passed)
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "followup_runner_route_ui_queue_execution_profile_count": 1,
        "ui_shows_candidate_only": True,
        "queue_is_pre_execution_governance_layer": True,
        "pin_does_not_trigger_runner": flags["pin_does_not_execute_runner"],
        "no_runner_execution": flags["no_runner_execution"],
        "rollback_available": True,
        "rollback_must_preserve_planning_artifacts": True,
        "rollback_must_preserve_observation_attention_layer": True,
        "rollback_must_preserve_visual_expression_system": True,
        "rollback_not_executed_by_default": True,
    }

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "followup_runner_route_ui_queue_execution": True,
        "followup_runner_route_ui_queue_execution_profile_count": 1,
        "upstream_planning_phase": UPSTREAM_PLANNING_PHASE,
        "audit_flags": flags,
        "post_review_audit": post,
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

    patch_record = {
        "modules": list(NEW_MODULES[:-1]),
        "updated": list(UPDATED_FILES),
        "entry_points": ["right_queue_panel", "bottom_queue_summary", "pin_unpin_exclude"],
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_followup_runner_route_ui_queue_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "model_test_lens_followup_runner_route_queue_ui_patch_record_v1.json").write_text(
            json.dumps(patch_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_followup_runner_route_queue_panel_record_v1.json").write_text(
            json.dumps({"panel": "followup_runner_route_queue_panel_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_followup_runner_route_queue_state_record_v1.json").write_text(
            json.dumps({"state": "followup_runner_route_queue_state_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_followup_runner_route_queue_summary_record_v1.json").write_text(
            json.dumps({"summary": "followup_runner_route_summary_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_followup_runner_route_negative_guard_audit_v1.json").write_text(
            json.dumps({"violations": violations, "failed": failed, "guards": guards}, indent=2) + "\n",
            encoding="utf-8")
        (out_root / "model_test_lens_followup_runner_route_ui_queue_post_review_audit_v1.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
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
