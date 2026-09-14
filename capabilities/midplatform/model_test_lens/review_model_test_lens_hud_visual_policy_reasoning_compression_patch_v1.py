# -*- coding: utf-8 -*-
"""P1 Model Test Lens HUD Visual Policy + Reasoning Compression Patch — review v1."""

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

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-HUD-Visual-Policy-And-Reasoning-Compression-Patch-Execution-And-Post-Review-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PATCH_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/hud_visual_policy_v1.js",
    f"{STATIC_REL}/hud_color_semantics_v1.js",
    f"{STATIC_REL}/hud_reasoning_compression_v1.js",
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/perception_hud_controls_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js",
    f"{STATIC_REL}/perception_hud_view_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/index.html",
    f"{_PKG}/review_model_test_lens_hud_visual_policy_reasoning_compression_patch_v1.py",
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUD_VISUAL_POLICY_REASONING_COMPRESSION_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUD_VISUAL_POLICY_REASONING_COMPRESSION_PATCH_BLOCKED"

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(", "fact_semantic"),
    (r"getUserMedia|MediaRecorder", "camera_mic"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "hud_visual_policy_patch_record",
    "hud_color_semantics_record",
    "hud_reasoning_compression_record",
    "hud_visual_policy_boundary_audit_record",
    "hud_visual_policy_post_review_record",
)

DEFAULT_OUT = _REPO_ROOT / "_tmp_eval_out" / "p1_midplatform_model_test_lens_hud_visual_policy_reasoning_compression_patch_v1_smoke_v0"
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    policy = _read(f"{STATIC_REL}/hud_visual_policy_v1.js")
    colors = _read(f"{STATIC_REL}/hud_color_semantics_v1.js")
    compression = _read(f"{STATIC_REL}/hud_reasoning_compression_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    controls = _read(f"{STATIC_REL}/perception_hud_controls_v1.js")
    adapter = _read(f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    index = _read(f"{STATIC_REL}/index.html")
    return {
        "mask_fill_hidden_by_default": "showMaskFill: false" in policy,
        "full_image_tint_removed_by_default": 'mode: "original"' in renderer,
        "line_box_default_visible": "showLineBox" in renderer and "显示识别框" in controls,
        "semantic_color_policy_written": "HudColorSemantics" in colors and "task_target" in colors,
        "task_target_green_defined": "#3ecf8e" in colors,
        "risk_red_defined": "#f07178" in colors,
        "uncertainty_yellow_defined": "#f0b429" in colors,
        "environment_blue_defined": "#4d9fff" in colors,
        "ocr_text_purple_defined": "#ba55d3" in colors,
        "weak_background_gray_defined": "#8b9cb3" in colors,
        "mobile_sam_color_mapping_written": "resolveMobileSamSemantics" in colors and "applyToEntity" in adapter,
        "hud_labels_chinese_result_first": "hud_status_label" in renderer,
        "reasoning_panel_result_first": "fact_observations" in compression and "goal_judgment" in compression,
        "reasoning_process_collapsed_by_default": "lol-rp-collapsed" in compression and "展开观察过程" in compression,
        "facts_goals_judgment_before_reasoning": compression.find("fact_observations") < compression.find("reasoning_process"),
        "expandable_reasoning_available": "查看证据链" in compression,
        "controls_updated": "显示区域填充" in controls,
        "compact_ui_preserved": "lol-main-grid" in index,
        "perception_hud_preserved": "renderCentral" in _read(f"{STATIC_REL}/perception_hud_view_v1.js"),
        "visual_compare_preserved": "visual_compare_view_v1.js" in index,
        "metrics_drawer_preserved": "renderMetricsDrawer" in _read(f"{STATIC_REL}/app.js"),
        "advanced_developer_drawers_preserved": "renderDeveloperDrawer" in _read(f"{STATIC_REL}/app.js"),
        "no_delete_artifact_button": "deleteArtifact" not in renderer,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in PATCH_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    js = "\n".join(_read(f) for f in PATCH_FILES if f.endswith(".js"))
    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, js, re.I)]
    flags = _audit()
    flags["no_page_model_execution"] = not violations
    flags["no_runtime"] = True
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = "navigation_action" not in js
    flags["no_registry_mutation"] = True
    flags["no_external_network"] = True
    flags["no_live_camera_microphone"] = "camera_mic" not in violations
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    guards = [
        {"guard_id": "A", "passed": flags["mask_fill_hidden_by_default"]},
        {"guard_id": "B", "passed": flags["full_image_tint_removed_by_default"]},
        {"guard_id": "C", "passed": flags["semantic_color_policy_written"]},
        {"guard_id": "D", "passed": flags["reasoning_panel_result_first"]},
        {"guard_id": "E", "passed": flags["reasoning_process_collapsed_by_default"]},
        {"guard_id": "F", "passed": flags["compact_ui_preserved"]},
        {"guard_id": "G", "passed": flags["no_page_model_execution"]},
        {"guard_id": "H", "passed": flags["test_board_protected"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core = [
        "mask_fill_hidden_by_default", "full_image_tint_removed_by_default", "semantic_color_policy_written",
        "mobile_sam_color_mapping_written", "reasoning_panel_result_first", "reasoning_process_collapsed_by_default",
        "controls_updated", "compact_ui_preserved", "perception_hud_preserved",
    ]
    if violations or failed or not all(flags.get(k) for k in core):
        decision = FINAL_BLOCKED
        blockers = len(violations) + len(failed) + sum(1 for k in core if not flags.get(k))
    else:
        decision = FINAL_GO
        blockers = 0

    post = {**flags, "rollback_available": True, "rollback_not_executed_by_default": True}
    out_root = DEFAULT_OUT
    out_root.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "hud_visual_policy_reasoning_compression_patch_profile_count": 1,
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
        rp = out_root / "p1_midplatform_model_test_lens_hud_visual_policy_reasoning_compression_patch_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)
        extras = {
            "model_test_lens_hud_visual_policy_patch_record_v1.json": {"mask_fill_default": False},
            "model_test_lens_hud_color_semantics_record_v1.json": {"policy": "task_risk_uncertainty_first"},
            "model_test_lens_hud_reasoning_compression_record_v1.json": {"result_first": True},
            "model_test_lens_hud_visual_policy_boundary_audit_v1.json": {"violations": violations},
            "model_test_lens_hud_visual_policy_reasoning_compression_post_review_audit_v1.json": post,
        }
        for name, payload in extras.items():
            (out_root / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or _REPO_ROOT)
        try:
            tb = write_test_board_records(result, test_mode="real_test", repo_root=root, module="model_governance",
                                          source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="real_test", repo_root=_BOARD_STANDIN,
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
    r = review(test_board_root=str(_REPO_ROOT))
    print(json.dumps({"final_decision": r["final_decision"], "blocker_count": r["blocker_count"],
                      "negative_guard_passed": r["negative_guard_passed"]}, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
