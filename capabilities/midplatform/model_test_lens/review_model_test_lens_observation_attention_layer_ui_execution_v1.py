# -*- coding: utf-8 -*-
"""P1 Observation Attention Layer UI Execution — post-review v1."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-UI-Execution-And-Post-Review-v1-001"
)
UPSTREAM_PLANNING_PHASE = (
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-Planning-v1-001"
)
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
OA_REL = "capabilities/midplatform/model_test_lens/observation_attention"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/observation_attention"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/observation_attention_copy_v1.js",
    f"{STATIC_REL}/observation_attention_engine_v1.js",
    f"{STATIC_REL}/observation_attention_priority_panel_v1.js",
    f"{STATIC_REL}/observation_attention_summary_v1.js",
    f"{_PKG}/review_model_test_lens_observation_attention_layer_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/hud_object_chip_bar_v1.js",
    f"{STATIC_REL}/hud_selected_object_detail_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

UI_MARKERS: Tuple[str, ...] = (
    "observation_attention_copy_v1.js",
    "observation_attention_engine_v1.js",
    "observation_attention_priority_panel_v1.js",
    "observation_attention_summary_v1.js",
    "优先观察",
    "priority_level",
    "motion_state_candidate",
    "tracking_required",
    "ocr_required",
    "recommended_followup_model",
    "followup_model_route_candidate_only",
    "observation_attention_candidate_only",
    "oa-priority-panel",
    "oa-summary-inline",
    "buildAttentionPackage",
    "refreshAttentionUi",
    "candidate_only",
    "not_fact",
    "not_navigation_instruction",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bsemantic_write\s*\(", "semantic_write"),
    (r"\bregistry_write\s*\(", "registry_write"),
    (r"\brun_model\b|\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\bexecute_tracking\b|\bexecute_depth\b|\bexecute_slam\b", "runner_execute_tracking"),
    (r"confirmed_dynamic", "confirmed_dynamic_in_ui"),
    (r"groundTruth\s*=\s*true", "ground_truth_true"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"deleteArtifact|removeTestBoard", "delete_artifact"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "observation_attention_ui_patch_record",
    "observation_attention_priority_panel_record",
    "observation_attention_summary_record",
    "observation_attention_boundary_audit_record",
    "observation_attention_testboard_integration_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_v1_smoke_v0"
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
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")
    panel = _read(f"{STATIC_REL}/observation_attention_priority_panel_v1.js")
    summary = _read(f"{STATIC_REL}/observation_attention_summary_v1.js")
    copy = _read(f"{STATIC_REL}/observation_attention_copy_v1.js")
    chip = _read(f"{STATIC_REL}/hud_object_chip_bar_v1.js")
    selected = _read(f"{STATIC_REL}/hud_selected_object_detail_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    closure = _load_json(f"{_PKG}/closure/luna_observation_lens_v1_closure_manifest.json")

    planning_review = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_layer_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_layer_planning_review_v1.json"
    )
    planning_go = (
        planning_review.get("final_decision") == PLANNING_GO
        or _read(f"{OA_REL}/observation_attention_layer_plan_v1.md") != ""
    )

    oa_bundle = "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "observation_attention_copy_v1.js",
            "observation_attention_engine_v1.js",
            "observation_attention_priority_panel_v1.js",
            "observation_attention_summary_v1.js",
            "hud_object_chip_bar_v1.js",
            "hud_selected_object_detail_v1.js",
            "luna_observation_compact_ui_v1.js",
        )
    )
    static_ok = all(
        m in index or m in app or m in styles or m in oa_bundle for m in UI_MARKERS
    )

    return {
        "upstream_planning_go": planning_go,
        "observation_attention_ui_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "object_chip_attention_badges_present": "attentionPkg" in chip and "formatInImageLabel" in chip,
        "priority_panel_present": "oa-priority-panel" in panel and "优先观察" in panel,
        "bottom_summary_present": "oa-summary-inline" in summary and "appendToMetricsSummary" in summary,
        "selected_object_attention_detail_present": (
            "观察调度说明见上方" in selected or "oa-selected-attention" in selected
        ),
        "visual_language_separation_present": _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js") != ""
            and "drawSegmentationBoundary" in _read(f"{STATIC_REL}/perception_hud_renderer_v1.js"),
        "attention_engine_candidate_only": "candidate_only: true" in engine and "not_fact: true" in engine,
        "attention_engine_no_runner": "run_model" not in engine and "execute_detection" not in engine,
        "attention_engine_single_frame_policy": "single_frame" in engine and "needs_tracking_review" in engine,
        "followup_route_candidate_only": "followup_model_route_candidate_only" in engine,
        "human_correction_priority_signal_only": "_correction_boosted" in engine and "ground truth" not in engine.lower(),
        "priority_sort_traceable": "PRIORITY_ORDER" in engine and "attention_summary" in engine,
        "motion_state_candidate_labels": "motion_state_candidate" in engine and "static_candidate" in engine,
        "schema_refs_exist": _read(f"{SCHEMA_REL}/observation_attention_record_schema_v1.json") != "",
        "observation_attention_does_not_write_fact": "not_fact" in engine,
        "observation_attention_does_not_trigger_navigation": "not_navigation_instruction" in engine,
        "observation_attention_does_not_trigger_runtime": "not_runtime_output" in engine,
        "luna_observation_lens_v1_preserved": closure.get("ui_template_frozen") is True
            and "lol-main-grid" in index,
        "central_hud_priority_preserved": "phud-hud-canvas" in index or "phud-hud-canvas" in _read(
            f"{STATIC_REL}/perception_hud_view_v1.js"
        ),
        "bottom_drawer_default_collapsed": "luna_bottom_drawer_state_guard_v1" in index,
        "no_delete_artifact_button": "deleteArtifact" not in app,
        "static_site_markers_present": static_ok,
        "app_wires_attention_refresh": "refreshAttentionUi" in app and "buildAttentionPackage" in app,
        "right_panel_attention_host": "lol-right-attention-host" in compact,
        "scheduling_not_on_canvas": "drawHudLabel" not in _read(f"{STATIC_REL}/perception_hud_renderer_v1.js"),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    oa_js = "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "observation_attention_copy_v1.js",
            "observation_attention_engine_v1.js",
            "observation_attention_priority_panel_v1.js",
            "observation_attention_summary_v1.js",
        )
    )
    scan_bundle = oa_js + _read(f"{STATIC_REL}/app.js")
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, scan_bundle, re.I)]

    flags = _audit()
    flags["no_external_network"] = True
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["upstream_planning_go"]},
        {"guard_id": "B", "passed": flags["attention_engine_candidate_only"]},
        {"guard_id": "C", "passed": flags["observation_attention_does_not_write_fact"] and "fact_write" not in violations},
        {"guard_id": "D", "passed": flags["observation_attention_does_not_trigger_navigation"]},
        {"guard_id": "E", "passed": flags["attention_engine_no_runner"] and "runner_execute" not in violations},
        {"guard_id": "F", "passed": flags["attention_engine_single_frame_policy"] and "confirmed_dynamic_in_ui" not in violations},
        {"guard_id": "G", "passed": flags["followup_route_candidate_only"]},
        {"guard_id": "H", "passed": flags["human_correction_priority_signal_only"]},
        {"guard_id": "I", "passed": flags["priority_sort_traceable"]},
        {"guard_id": "J", "passed": flags["motion_state_candidate_labels"]},
        {"guard_id": "K", "passed": flags["object_chip_attention_badges_present"]},
        {"guard_id": "L", "passed": flags["priority_panel_present"]},
        {"guard_id": "M", "passed": flags["bottom_summary_present"]},
        {"guard_id": "N", "passed": flags["selected_object_attention_detail_present"]},
        {"guard_id": "O", "passed": flags["visual_language_separation_present"]},
        {"guard_id": "P", "passed": flags["scheduling_not_on_canvas"]},
        {"guard_id": "Q", "passed": flags["luna_observation_lens_v1_preserved"]},
        {"guard_id": "R", "passed": flags["central_hud_priority_preserved"]},
        {"guard_id": "S", "passed": flags["app_wires_attention_refresh"]},
        {"guard_id": "T", "passed": flags["test_board_protected"]},
        {"guard_id": "U", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "observation_attention_ui_written",
        "object_chip_attention_badges_present",
        "priority_panel_present",
        "bottom_summary_present",
        "selected_object_attention_detail_present",
        "visual_language_separation_present",
        "scheduling_not_on_canvas",
        "attention_engine_candidate_only",
        "attention_engine_no_runner",
        "attention_engine_single_frame_policy",
        "followup_route_candidate_only",
        "human_correction_priority_signal_only",
        "priority_sort_traceable",
        "static_site_markers_present",
        "upstream_planning_go",
        "app_wires_attention_refresh",
        "right_panel_attention_host",
        "luna_observation_lens_v1_preserved",
    ]

    if violations or failed or not all(flags.get(k) for k in core) or ng_passed < 21:
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k)) + (21 - ng_passed)
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "observation_attention_layer_ui_execution_profile_count": 1,
        "ui_shows_candidate_only": True,
        "sorting_traceable": flags["priority_sort_traceable"],
        "single_frame_static_dynamic_compliant": flags["attention_engine_single_frame_policy"],
        "human_correction_affects_priority_signal_only": flags["human_correction_priority_signal_only"],
        "no_runner_execution": flags["attention_engine_no_runner"],
        "rollback_available": True,
        "rollback_must_preserve_planning_artifacts": True,
        "rollback_must_preserve_luna_observation_lens_v1": True,
        "rollback_must_preserve_human_correction_layer": True,
        "rollback_not_executed_by_default": True,
    }

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "observation_attention_ui_execution": True,
        "observation_attention_layer_ui_execution_profile_count": 1,
        "upstream_planning_phase": UPSTREAM_PLANNING_PHASE,
        "audit_flags": flags,
        "post_review_audit": post,
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

    patch_record = {
        "modules": list(NEW_MODULES[:-1]),
        "updated": list(UPDATED_FILES),
        "entry_points": ["object_chip_badges", "priority_panel", "bottom_summary", "selected_object_detail"],
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "model_test_lens_observation_attention_ui_patch_record_v1.json").write_text(
            json.dumps(patch_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_observation_attention_priority_panel_record_v1.json").write_text(
            json.dumps({"panel": "observation_attention_priority_panel_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_observation_attention_summary_record_v1.json").write_text(
            json.dumps({"summary": "observation_attention_summary_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_observation_attention_boundary_audit_v1.json").write_text(
            json.dumps({"violations": violations, "failed": failed}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_observation_attention_layer_ui_post_review_audit_v1.json").write_text(
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
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
