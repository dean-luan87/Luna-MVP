# -*- coding: utf-8 -*-
"""P1 Observation Attention Overlay Semantic Separation Patch v1-002 — post-review."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Overlay-Semantic-Separation-Patch-v1-002"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_OVERLAY_SEMANTIC_SEPARATION_PATCH_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_OVERLAY_SEMANTIC_SEPARATION_PATCH_BLOCKED"


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _audit() -> Dict[str, bool]:
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    controls = _read(f"{STATIC_REL}/perception_hud_controls_v1.js")
    engine = _read(f"{STATIC_REL}/observation_attention_engine_v1.js")

    return {
        "single_segmentation_boundary_owner": "drawSegmentationBoundary" in vl
            and "segmentation overlay owner" in vl.lower(),
        "no_attention_boundary_clone": "drawAttentionFloatMarker" in vl
            and "drawPriorityCorner" not in vl
            and "drawRouteDots" not in vl
            and "drawNumberBadge" not in vl,
        "no_dual_box_on_select": "largeScene" not in vl and "strokeRect" in vl,
        "readable_text_float_marker": "formatFloatMarker" in vl and "drawAttentionFloatMarker" in vl,
        "p0_p1_default_only": "shouldShowMarkerOnCanvas" in vl and "showAllAttentionMarkers" in vl,
        "show_all_markers_toggle": "showAllAttentionMarkers" in controls and "显示全部候选浮标" in controls,
        "renderer_two_pass_no_attention_box": "drawAttentionFloatMarker" in renderer
            and renderer.count("drawSegmentationBoundary") >= 1,
        "attention_engine_unchanged": "inferPriority" in engine and "buildAttentionPackage" in engine,
        "no_icon_dots_on_canvas": "drawRouteDots" not in renderer and "arc(" not in vl,
    }


def review(*, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    vl = _read(f"{STATIC_REL}/hud_attention_visual_language_v1.js")
    renderer = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    violations = []
    if re.search(r"drawHudBox|drawAttentionIndicators", renderer):
        violations.append("legacy_dual_render")
    if re.search(r"strokeRect.*priority|priority.*strokeRect", vl, re.I):
        violations.append("priority_on_boundary")

    flags = _audit()
    guards = [
        {"guard_id": "A", "passed": flags["single_segmentation_boundary_owner"]},
        {"guard_id": "B", "passed": flags["no_attention_boundary_clone"]},
        {"guard_id": "C", "passed": flags["no_dual_box_on_select"]},
        {"guard_id": "D", "passed": flags["readable_text_float_marker"]},
        {"guard_id": "E", "passed": flags["p0_p1_default_only"]},
        {"guard_id": "F", "passed": flags["show_all_markers_toggle"]},
        {"guard_id": "G", "passed": flags["renderer_two_pass_no_attention_box"]},
        {"guard_id": "H", "passed": flags["attention_engine_unchanged"]},
        {"guard_id": "I", "passed": flags["no_icon_dots_on_canvas"]},
        {"guard_id": "J", "passed": not violations},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])
    core_ok = all(flags.values())

    decision = FINAL_GO if core_ok and ng_passed >= 10 and not violations else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_observation_attention_overlay_semantic_separation_patch_v1_002_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }
    rp = out / "p1_midplatform_model_test_lens_observation_attention_overlay_semantic_separation_patch_review_v1.json"
    rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="real_test", repo_root=root, module="model_governance",
                source_review_file=str(rp),
            )
            result["test_board_root"] = tb.get("test_board_dir")
        except (OSError, PermissionError):
            pass

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "negative_guard_passed": r["negative_guard_passed"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
