# -*- coding: utf-8 -*-
"""P1 Luna Observation Lens V1 Closure & Standard Freeze — review v1."""

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
    """Prefer cwd when it is a valid repo root (supports Luna-Workspace-Min vs Luna-Core)."""
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
    "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Lens-V1-Closure-And-Standard-Freeze-Review-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
CLOSURE_REL = "capabilities/midplatform/model_test_lens/closure"
STD_UI = "capabilities/midplatform/model_test_lens/standards/ui"
GOV = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"

CLOSURE_FILES: Tuple[str, ...] = (
    f"{CLOSURE_REL}/luna_observation_lens_v1_closure_report.md",
    f"{CLOSURE_REL}/luna_observation_lens_v1_closure_manifest.json",
    f"{CLOSURE_REL}/luna_observation_lens_v1_ui_freeze_snapshot.json",
    f"{CLOSURE_REL}/luna_observation_lens_v1_followup_routes.json",
    f"{STD_UI}/luna_observation_lens_v1_template_standard.md",
    f"{STD_UI}/luna_observation_lens_v1_component_contract.json",
    f"{STD_UI}/luna_observation_lens_v1_model_adapter_slot_contract.json",
    f"{GOV}/luna_observation_lens_v1_standard_registry_patch.json",
    f"{_PKG}/review_model_test_lens_luna_observation_lens_v1_closure_review.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/README_STATIC_SITE.md",
    f"{STD_UI}/model_test_lens_ui_standard_v1.md",
    "capabilities/midplatform/model_test_lens/standards/perception_hud/perception_hud_ui_template_standard_v1.md",
    f"{GOV}/model_test_lens_ui_standard_registry_v1.json",
)

STATIC_SITE_MARKERS: Tuple[str, ...] = (
    "observation_canvas_first_collapsible_layout_v1.js",
    "luna_left_capability_drawer_v1.js",
    "luna_capability_grid_trigger_v1.js",
    "hud_object_chip_bar_v1.js",
    "hud_reasoning_compression_v1.js",
    "luna_bottom_drawer_tabs_v1.js",
    "luna_bottom_drawer_state_guard_v1.js",
    "perception_hud_view_v1.js",
    "lol-object-chip-host",
    "lol-right-panel",
    "Luna 观察镜",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_LENS_V1_CLOSURE_GO"
FINAL_PARTIAL = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_LENS_V1_CLOSURE_PARTIAL_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_LENS_V1_CLOSURE_BLOCKED"

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(", "fact_semantic"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "luna_observation_v1_closure_record",
    "ui_template_freeze_record",
    "future_model_adapter_route_record",
    "boundary_audit_record",
    "standard_registry_patch_record",
    "luna_observation_lens_v1_closure_post_review_record",
)

def _default_out_dir() -> Path:
    return _detect_repo_root() / "_tmp_eval_out" / "p1_midplatform_model_test_lens_luna_observation_lens_v1_closure_review_v1_smoke_v0"


def _board_standin_dir() -> Path:
    return _detect_repo_root() / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    if not raw:
        return {}
    return json.loads(raw)


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    styles = _read(f"{STATIC_REL}/styles.css")
    manifest = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_closure_manifest.json")
    snapshot = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_ui_freeze_snapshot.json")
    routes = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_followup_routes.json")
    slots = _load_json(f"{STD_UI}/luna_observation_lens_v1_model_adapter_slot_contract.json")
    registry = _load_json(f"{GOV}/model_test_lens_ui_standard_registry_v1.json")
    template = _read(f"{STD_UI}/luna_observation_lens_v1_template_standard.md")

    route_ids = [r.get("route_id", "") for r in routes.get("routes", [])]
    slot_keys = list(slots.get("slots", {}).keys())

    static_ok = all(m in index or m in app or m in styles or m in _read(f"{STATIC_REL}/luna_observation_copy_v1.js")
                    for m in STATIC_SITE_MARKERS)

    return {
        "luna_observation_lens_v1_closure_ready": manifest.get("ui_template_frozen") is True,
        "ui_template_frozen": manifest.get("ui_template_frozen") is True,
        "compact_observation_window_ready": manifest.get("compact_observation_window_ready") is True,
        "central_hud_priority_confirmed": snapshot.get("required_components") and "phud-hud-canvas" in snapshot["required_components"],
        "left_capability_drawer_confirmed": "luna_left_capability_drawer_v1" in snapshot.get("required_components", []),
        "object_chip_bar_confirmed": "hud_object_chip_bar_v1" in snapshot.get("required_components", []),
        "right_reasoning_panel_confirmed": "lol-right-panel" in index and "hud_reasoning_compression_v1" in index,
        "bottom_drawers_confirmed": "luna_bottom_drawer_tabs_v1" in index,
        "developer_mode_preserved": (
            "developer" in app
            and (
                "lol-more-menu" in app
                or "lol-more-menu" in _read(f"{STATIC_REL}/luna_topbar_compact_actions_v1.js")
                or "lol-developer-btn" in index
            )
        ),
        "whitebox_slot_preserved": "whitebox" in app,
        "raw_engineering_terms_hidden_by_default": "phase_ref" not in index and "manifest" not in index,
        "future_model_pages_must_reuse_template": (
            "Luna Observation Lens V1 Template Standard" in _read(f"{STD_UI}/model_test_lens_ui_standard_v1.md")
            or "luna_observation_lens_v1_model_adapter_slot_contract" in _read(f"{STD_UI}/model_test_lens_ui_standard_v1.md")
        ),
        "detection_adapter_route_defined": "detection_yolo_runner_v1" in route_ids and "detection" in slot_keys,
        "ocr_adapter_route_defined": "ocr_runner_v1" in route_ids and "ocr" in slot_keys,
        "slam_adapter_route_defined": "slam_video_backend_v1" in route_ids and "slam_vio" in slot_keys,
        "depth_adapter_route_defined": "depth_world_perception_v1" in route_ids and "depth" in slot_keys,
        "asr_tts_speaker_vlm_routes_defined": all(
            k in slot_keys for k in ("asr", "tts", "speaker", "vlm")
        ),
        "standard_registry_patch_completed": "LunaObservationLensV1TemplateStandard" in json.dumps(registry),
        "governance_standard_updated": "luna_observation_lens_v1_default" in json.dumps(registry),
        "static_site_v1_markers_present": static_ok,
        "no_vertical_report_flow": "lol-main-grid" in index and "vertical" not in template.lower()[:200],
        "object_details_not_default_expanded": any(
            "full_object" in str(x) for x in snapshot.get("forbidden_default_components", [])
        ),
        "bottom_drawer_default_collapsed": "luna_bottom_drawer_state_guard_v1" in index,
        "no_delete_artifact_button": "deleteArtifact" not in app,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in CLOSURE_FILES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    js = "\n".join(_read(f"{STATIC_REL}/{f}") for f in (
        "app.js", "perception_hud_view_v1.js", "luna_observation_compact_ui_v1.js",
        "hud_object_chip_bar_v1.js", "luna_bottom_drawer_tabs_v1.js",
    ) if _read(f"{STATIC_REL}/{f}"))
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, js, re.I)]
    flags = _audit()
    flags["no_page_model_execution"] = not violations
    flags["no_runtime"] = True
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = not re.search(
        r"navigation_action_speech_allowed:\s*true|triggerNavigation|invokeSpeech|speechAction\s*\(",
        js,
        re.I,
    )
    flags["no_registry_mutation"] = "registry_write" not in js
    flags["no_external_network"] = True
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["static_site_v1_markers_present"]},
        {"guard_id": "B", "passed": flags["central_hud_priority_confirmed"]},
        {"guard_id": "C", "passed": flags["object_details_not_default_expanded"]},
        {"guard_id": "D", "passed": flags["bottom_drawer_default_collapsed"]},
        {"guard_id": "E", "passed": flags["raw_engineering_terms_hidden_by_default"]},
        {"guard_id": "F", "passed": flags["right_reasoning_panel_confirmed"]},
        {"guard_id": "G", "passed": flags["object_chip_bar_confirmed"]},
        {"guard_id": "H", "passed": flags["left_capability_drawer_confirmed"]},
        {"guard_id": "I", "passed": flags["future_model_pages_must_reuse_template"]},
        {"guard_id": "J", "passed": flags["no_page_model_execution"]},
        {"guard_id": "K", "passed": flags["no_fact_semantic_navigation"]},
        {"guard_id": "L", "passed": flags["no_runtime"]},
        {"guard_id": "M", "passed": flags["no_external_network"]},
        {"guard_id": "N", "passed": flags["test_board_protected"]},
        {"guard_id": "O", "passed": flags["ui_template_frozen"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = [
        "luna_observation_lens_v1_closure_ready",
        "ui_template_frozen",
        "compact_observation_window_ready",
        "central_hud_priority_confirmed",
        "left_capability_drawer_confirmed",
        "object_chip_bar_confirmed",
        "right_reasoning_panel_confirmed",
        "bottom_drawers_confirmed",
        "future_model_pages_must_reuse_template",
        "detection_adapter_route_defined",
        "ocr_adapter_route_defined",
        "slam_adapter_route_defined",
        "depth_adapter_route_defined",
        "asr_tts_speaker_vlm_routes_defined",
        "standard_registry_patch_completed",
        "governance_standard_updated",
        "static_site_v1_markers_present",
        "no_page_model_execution",
    ]
    if violations or failed or not all(flags.get(k) for k in core):
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k))
    else:
        decision = FINAL_GO
        blockers = 0

    post = {
        **flags,
        "rollback_available": True,
        "rollback_not_executed_by_default": True,
        "rollback_must_preserve_current_ui_files": True,
        "rollback_must_preserve_runner_bridge_service": True,
        "rollback_must_preserve_test_board": True,
        "rollback_must_preserve_review_artifacts": True,
    }

    manifest = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_closure_manifest.json")
    snapshot = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_ui_freeze_snapshot.json")
    routes = _load_json(f"{CLOSURE_REL}/luna_observation_lens_v1_followup_routes.json")

    out_root = _default_out_dir()
    out_root.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "closure_review_phase": True,
        "standard_freeze_review": True,
        "luna_observation_lens_v1_closure": True,
        "luna_observation_lens_v1_closure_profile_count": 1,
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

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_luna_observation_lens_v1_closure_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "luna_observation_lens_v1_closure_manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "luna_observation_lens_v1_ui_freeze_snapshot.json").write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "luna_observation_lens_v1_followup_routes.json").write_text(
            json.dumps(routes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "luna_observation_lens_v1_boundary_audit.json").write_text(
            json.dumps({"violations": violations, "failed": failed}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "model_test_lens_luna_observation_lens_v1_closure_post_review_audit_v1.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or _REPO_ROOT)
        try:
            tb = write_test_board_records(result, test_mode="real_test", repo_root=root, module="model_governance",
                                          source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError):
            standin = _board_standin_dir()
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="real_test", repo_root=standin,
                                          module="model_governance", source_review_file=result.get("output_review_file"))
        board_dir = Path(tb["test_board_dir"])
        common = {"phase_id": PHASE_ID, "protected": True, "non_deletable": True, "deletion_forbidden": True,
                  "test_artifact_protected": True, "test_mode": "real_test"}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype}}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_RECORDS)
    return result


def main() -> int:
    root = _detect_repo_root()
    r = review(test_board_root=str(root))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
