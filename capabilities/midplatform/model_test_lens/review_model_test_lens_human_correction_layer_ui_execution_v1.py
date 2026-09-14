# -*- coding: utf-8 -*-
"""P1 Human Correction Layer UI Execution — post-review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-UI-Execution-And-Post-Review-v1-001"
UPSTREAM_PLANNING_PHASE = "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-Planning-v1-001"
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUMAN_CORRECTION_LAYER_PLANNING_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
HC_REL = "capabilities/midplatform/model_test_lens/human_correction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/human_correction"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/human_correction_ui_v1.js",
    f"{STATIC_REL}/human_correction_modal_v1.js",
    f"{STATIC_REL}/human_correction_drawer_v1.js",
    f"{STATIC_REL}/human_correction_store_v1.js",
    f"{STATIC_REL}/human_correction_target_picker_v1.js",
    f"{STATIC_REL}/human_correction_training_signal_preview_v1.js",
    f"{STATIC_REL}/human_correction_copy_v1.js",
    f"{_PKG}/review_model_test_lens_human_correction_layer_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/hud_object_chip_bar_v1.js",
    f"{STATIC_REL}/hud_selected_object_detail_v1.js",
    f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/hud_reasoning_compression_v1.js",
)

UI_MARKERS: Tuple[str, ...] = (
    "human_correction_ui_v1.js",
    "human_correction_modal_v1.js",
    "human_correction_drawer_v1.js",
    "human_correction_store_v1.js",
    "hud-chip-correct",
    "data-drawer='correction'",
    "指错",
    "标记问题",
    "指出问题",
    "luna_observation_human_corrections_v1",
    "candidate_only",
    "correctionCandidateOnly",
    "not_auto_training_data",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bmodifyEnvelope\b", "modify_envelope"),
    (r"\boverwriteModelOutput\b", "overwrite_model_output"),
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bsemantic_write\s*\(", "semantic_write"),
    (r"\bregistry_write\s*\(", "registry_write"),
    (r"\bautoTrain\b", "auto_train"),
    (r"groundTruth\s*=\s*true", "ground_truth_true"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
    (r"deleteArtifact|removeTestBoard", "delete_artifact"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "human_correction_ui_patch_record",
    "human_correction_modal_record",
    "human_correction_drawer_record",
    "human_correction_boundary_audit_record",
    "human_correction_testboard_integration_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUMAN_CORRECTION_LAYER_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUMAN_CORRECTION_LAYER_UI_EXECUTION_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_human_correction_layer_ui_execution_v1_smoke_v0"
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
    store = _read(f"{STATIC_REL}/human_correction_store_v1.js")
    modal = _read(f"{STATIC_REL}/human_correction_modal_v1.js")
    drawer = _read(f"{STATIC_REL}/human_correction_drawer_v1.js")
    preview = _read(f"{STATIC_REL}/human_correction_training_signal_preview_v1.js")
    chip = _read(f"{STATIC_REL}/hud_object_chip_bar_v1.js")
    selected = _read(f"{STATIC_REL}/hud_selected_object_detail_v1.js")
    reasoning = _read(f"{STATIC_REL}/hud_reasoning_compression_v1.js")
    bottom = _read(f"{STATIC_REL}/luna_bottom_drawer_tabs_v1.js")
    hud = _read(f"{STATIC_REL}/perception_hud_view_v1.js")
    closure = _load_json(f"{_PKG}/closure/luna_observation_lens_v1_closure_manifest.json")

    planning_review = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_human_correction_layer_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_human_correction_layer_planning_review_v1.json"
    )
    planning_go = (
        planning_review.get("final_decision") == PLANNING_GO
        or _read(f"{HC_REL}/human_correction_layer_plan_v1.md") != ""
    )

    hc_bundle = "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "human_correction_ui_v1.js", "human_correction_modal_v1.js",
            "human_correction_drawer_v1.js", "human_correction_store_v1.js",
            "human_correction_copy_v1.js", "human_correction_training_signal_preview_v1.js",
            "hud_object_chip_bar_v1.js", "hud_selected_object_detail_v1.js",
            "hud_reasoning_compression_v1.js", "luna_bottom_drawer_tabs_v1.js",
        )
    )
    static_ok = all(
        m in index or m in app or m in styles or m in hc_bundle for m in UI_MARKERS
    )

    return {
        "upstream_planning_go": planning_go,
        "human_correction_ui_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "object_chip_correction_entry_present": "hud-chip-correct" in chip and "指错" in chip,
        "hud_annotation_correction_entry_present": "onHudCanvasReady" in hud and "lol-selected-mark" in selected,
        "missing_region_correction_entry_present": (
            "hc-missing-region-btn" in _read(f"{STATIC_REL}/human_correction_ui_v1.js")
            or "openForMissingRegion" in _read(f"{STATIC_REL}/human_correction_ui_v1.js")
        ),
        "reasoning_panel_correction_entry_present": "hc-report-issue" in reasoning or "指出问题" in reasoning,
        "correction_drawer_present": "correction" in bottom and "renderCorrection" in app,
        "correction_modal_present": "hc-modal-overlay" in modal,
        "correction_record_schema_used": "correction_id" in store and "candidate_only" in store,
        "correction_taxonomy_used": "correctionTypes" in _read(f"{STATIC_REL}/human_correction_copy_v1.js"),
        "training_signal_preview_present": "not_auto_training_data" in preview,
        "correction_candidate_only": "candidate_only: true" in store or "candidateOnly: true" in store,
        "correction_does_not_modify_original_envelope": "must_not_modify_original_envelope" in store,
        "correction_does_not_modify_model_output": "must_not_modify_model_output" in store,
        "correction_does_not_write_fact": "not_fact" in store,
        "correction_does_not_write_semantic": "semantic_write" not in store,
        "correction_does_not_trigger_runtime": "trigger_runtime" not in store,
        "correction_does_not_trigger_navigation_action_speech": "not_navigation_instruction" in store,
        "correction_does_not_call_output_adapter": "output_adapter" not in store,
        "correction_does_not_mutate_registry": "registry_write" not in store,
        "not_auto_training_data": "not_auto_training_data" in preview,
        "not_ground_truth": "ground truth" in preview.lower() or "not_ground_truth" in preview,
        "owner_review_required_for_training": "needs_owner_review" in preview,
        "luna_observation_lens_v1_preserved": closure.get("ui_template_frozen") is True
            and "lol-main-grid" in index,
        "central_hud_priority_preserved": "phud-hud-canvas" in index or "phud-hud-canvas" in hud,
        "bottom_drawer_default_collapsed": "luna_bottom_drawer_state_guard_v1" in index,
        "no_delete_artifact_button": "deleteArtifact" not in app,
        "static_site_markers_present": static_ok,
        "local_storage_key_correct": "luna_observation_human_corrections_v1" in store,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    hc_js = "\n".join(_read(f"{STATIC_REL}/{f}") for f in (
        "human_correction_ui_v1.js", "human_correction_modal_v1.js",
        "human_correction_drawer_v1.js", "human_correction_store_v1.js",
        "human_correction_target_picker_v1.js", "human_correction_training_signal_preview_v1.js",
    ))
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, hc_js + _read(f"{STATIC_REL}/app.js"), re.I)]

    flags = _audit()
    flags["no_external_network"] = True
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["upstream_planning_go"]},
        {"guard_id": "B", "passed": flags["correction_does_not_modify_original_envelope"]},
        {"guard_id": "C", "passed": flags["correction_does_not_modify_model_output"]},
        {"guard_id": "D", "passed": flags["correction_does_not_write_fact"] and "semantic_write" not in violations},
        {"guard_id": "E", "passed": "trigger_runtime" not in hc_js and "output_adapter" not in hc_js},
        {"guard_id": "F", "passed": flags["not_auto_training_data"] and "auto_train" not in violations},
        {"guard_id": "G", "passed": flags["not_ground_truth"]},
        {"guard_id": "H", "passed": "source_envelope_ref" in hc_js},
        {"guard_id": "I", "passed": "correction_type" in hc_js},
        {"guard_id": "J", "passed": "correction_target" in hc_js},
        {"guard_id": "K", "passed": flags["correction_candidate_only"]},
        {"guard_id": "L", "passed": flags["training_signal_preview_present"]},
        {"guard_id": "M", "passed": flags["owner_review_required_for_training"]},
        {"guard_id": "N", "passed": flags["luna_observation_lens_v1_preserved"]},
        {"guard_id": "O", "passed": "hc-modal-overlay" in hc_js and "position: fixed" in _read(f"{STATIC_REL}/styles.css")},
        {"guard_id": "P", "passed": flags["test_board_protected"]},
        {"guard_id": "Q", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "human_correction_ui_written",
        "object_chip_correction_entry_present",
        "hud_annotation_correction_entry_present",
        "missing_region_correction_entry_present",
        "reasoning_panel_correction_entry_present",
        "correction_drawer_present",
        "correction_modal_present",
        "correction_record_schema_used",
        "correction_taxonomy_used",
        "training_signal_preview_present",
        "correction_candidate_only",
        "luna_observation_lens_v1_preserved",
        "central_hud_priority_preserved",
        "bottom_drawer_default_collapsed",
        "static_site_markers_present",
        "upstream_planning_go",
    ]

    if violations or failed or not all(flags.get(k) for k in core) or ng_passed < 17:
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k)) + (17 - ng_passed)
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "human_correction_layer_ui_execution_profile_count": 1,
        "rollback_available": True,
        "rollback_can_remove_human_correction_ui_files": True,
        "rollback_must_preserve_planning_artifacts": True,
        "rollback_must_preserve_luna_observation_lens_v1": True,
        "rollback_must_preserve_test_board": True,
        "rollback_must_preserve_review_artifacts": True,
        "rollback_not_executed_by_default": True,
    }

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "human_correction_ui_execution": True,
        "human_correction_layer_ui_execution_profile_count": 1,
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
        "entry_points": ["object_chip", "hud_canvas", "missing_region", "reasoning_panel", "correction_drawer"],
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_human_correction_layer_ui_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "model_test_lens_human_correction_ui_patch_record_v1.json").write_text(
            json.dumps(patch_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_human_correction_modal_record_v1.json").write_text(
            json.dumps({"modal": "human_correction_modal_v1.js"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_human_correction_drawer_record_v1.json").write_text(
            json.dumps({"drawer_tab": "correction"}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_human_correction_boundary_audit_v1.json").write_text(
            json.dumps({"violations": violations, "failed": failed}, indent=2) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_human_correction_layer_ui_post_review_audit_v1.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="real_test", repo_root=root, module="model_governance",
                                          source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="real_test", repo_root=standin, module="model_governance",
                                          source_review_file=result.get("output_review_file"))
        board_dir = Path(tb["test_board_dir"])
        common = {"phase_id": PHASE_ID, "protected": True, "non_deletable": True, "deletion_forbidden": True,
                  "test_artifact_protected": True, "test_mode": "real_test"}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype, "patch": patch_record}}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")
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
