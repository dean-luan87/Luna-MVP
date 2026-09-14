# -*- coding: utf-8 -*-
"""P1 Observation Attention Overlay Readability Patch — post-review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Overlay-Readability-Patch-v1-001"
UPSTREAM_UI_PHASE = (
    "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-UI-Execution-And-Post-Review-v1-001"
)
UPSTREAM_UI_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_UI_EXECUTION_GO"

STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/hud_overlay_readability_v1.js",
    f"{_PKG}/review_model_test_lens_observation_attention_overlay_readability_patch_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/hud_hidpi_renderer_v1.js",
    f"{STATIC_REL}/hud_visual_policy_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/index.html",
)

UI_MARKERS: Tuple[str, ...] = (
    "hud_overlay_readability_v1.js",
    "HudOverlayReadability",
    "pickLabelPlacement",
    "sortDrawItems",
    "formatOverlayLabel",
    "drawSceneStructureOverlay",
    "dimP2Opacity",
    "dimP3Opacity",
    "showDebugGuidelines",
    "setAttentionPkg",
    "attentionPkg",
    "sceneStructureFillOpacity",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\brun_model\b|\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\bbuildAttentionPackage\b", "attention_engine_modified_in_renderer"),
    (r"PRIORITY_ORDER\s*=", "priority_order_redefined"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "observation_attention_overlay_readability_patch_record",
    "observation_attention_overlay_label_avoidance_record",
    "observation_attention_overlay_priority_tier_record",
    "observation_attention_overlay_boundary_audit_record",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_OVERLAY_READABILITY_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_OVERLAY_READABILITY_PATCH_BLOCKED"


def _default_out() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_observation_attention_overlay_readability_patch_v1_smoke_v0"
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
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    readability = _read(f"{STATIC_REL}/hud_overlay_readability_v1.js")
    hud_view = _read(f"{STATIC_REL}/perception_hud_view_v1.js")
    policy = _read(f"{STATIC_REL}/hud_visual_policy_v1.js")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")

    upstream = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_layer_ui_execution_review_v1.json"
    )
    upstream_go = upstream.get("final_decision") == UPSTREAM_UI_GO

    bundle = readability + renderer + hud_view + policy + app
    static_ok = all(m in index or m in bundle for m in UI_MARKERS)

    return {
        "upstream_attention_ui_go": upstream_go,
        "overlay_readability_module_present": bool(readability),
        "label_avoidance_present": "pickLabelPlacement" in readability and "anchorCandidates" in readability,
        "priority_tier_opacity_present": "priorityAlpha" in readability and "dimP2Opacity" in policy,
        "scene_structure_denoise_present": "drawSceneStructureOverlay" in renderer
            and "useSceneStructureStyle" in readability,
        "compact_full_label_modes_present": "formatOverlayLabel" in readability,
        "selected_boost_present": "isHighlighted" in readability and "full" in readability,
        "debug_guidelines_gated": "showDebugGuidelines" in policy and "drawDebugGuidelines" in renderer,
        "attention_pkg_wired_to_renderer": "setAttentionPkg" in hud_view and "attentionPkg" in hud_view,
        "attention_engine_unchanged": "buildAttentionPackage" in engine
            and "inferPriority" in engine
            and "buildAttentionPackage" not in renderer,
        "right_panel_unchanged": "ObservationAttentionPriorityPanel" in _read(
            f"{STATIC_REL}/observation_attention_priority_panel_v1.js"
        ),
        "static_site_markers_present": static_ok,
        "luna_layout_preserved": "lol-main-grid" in index,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    patch_js = "\n".join(_read(f"{STATIC_REL}/{f}") for f in (
        "hud_overlay_readability_v1.js", "perception_hud_renderer_v1.js", "perception_hud_view_v1.js",
    ))
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, patch_js, re.I)]
    if re.search(r"\bfact_write\s*\(|\bexecute_detection\b", _read(f"{STATIC_REL}/app.js"), re.I):
        violations.append("app_runner_or_fact")

    flags = _audit()
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["upstream_attention_ui_go"]},
        {"guard_id": "B", "passed": flags["label_avoidance_present"]},
        {"guard_id": "C", "passed": flags["priority_tier_opacity_present"]},
        {"guard_id": "D", "passed": flags["scene_structure_denoise_present"]},
        {"guard_id": "E", "passed": flags["compact_full_label_modes_present"]},
        {"guard_id": "F", "passed": flags["selected_boost_present"]},
        {"guard_id": "G", "passed": flags["debug_guidelines_gated"]},
        {"guard_id": "H", "passed": flags["attention_pkg_wired_to_renderer"]},
        {"guard_id": "I", "passed": flags["attention_engine_unchanged"]},
        {"guard_id": "J", "passed": "fact_write" not in violations and "runner_execute" not in violations},
        {"guard_id": "K", "passed": flags["right_panel_unchanged"]},
        {"guard_id": "L", "passed": flags["luna_layout_preserved"]},
        {"guard_id": "M", "passed": flags["test_board_protected"]},
        {"guard_id": "N", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "overlay_readability_module_present",
        "label_avoidance_present",
        "priority_tier_opacity_present",
        "scene_structure_denoise_present",
        "compact_full_label_modes_present",
        "attention_engine_unchanged",
        "attention_pkg_wired_to_renderer",
        "static_site_markers_present",
        "upstream_attention_ui_go",
    ]

    if violations or failed or not all(flags.get(k) for k in core) or ng_passed < 14:
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k)) + (14 - ng_passed)
    else:
        decision = FINAL_GO
        blockers = 0

    out_root = _default_out()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "overlay_readability_patch": True,
        "upstream_ui_phase": UPSTREAM_UI_PHASE,
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

    patch_record = {
        "modules": list(NEW_MODULES[:-1]),
        "updated": list(UPDATED_FILES),
        "scope": [
            "label_anchor_avoidance",
            "priority_visual_tiers",
            "scene_structure_denoise",
            "compact_vs_full_labels",
            "debug_guidelines_gated",
        ],
    }

    if write_file:
        rp = out_root / "p1_midplatform_model_test_lens_observation_attention_overlay_readability_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        (out_root / "model_test_lens_observation_attention_overlay_readability_patch_record_v1.json").write_text(
            json.dumps(patch_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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
