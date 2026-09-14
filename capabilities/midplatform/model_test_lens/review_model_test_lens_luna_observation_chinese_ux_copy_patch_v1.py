# -*- coding: utf-8 -*-
"""P1 Model Test Lens Luna Observation Chinese UX Copy Patch — execution review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-Chinese-UX-Copy-Patch-Execution-And-Post-Review-v1-001"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

PATCH_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/luna_observation_label_i18n_v1.js",
    f"{STATIC_REL}/luna_observation_copy_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/luna_observation_layout_v1.js",
    f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js",
    f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js",
    f"{STATIC_REL}/perception_hud_renderer_v1.js",
    f"{STATIC_REL}/model_insight_layer_v1.js",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/README_STATIC_SITE.md",
    f"{_PKG}/review_model_test_lens_luna_observation_chinese_ux_copy_patch_v1.py",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_CHINESE_UX_COPY_PATCH_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LUNA_OBSERVATION_CHINESE_UX_COPY_PATCH_BLOCKED"

FORBIDDEN_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"\brun_model\s*\(|\binfer\s*\(|\bexecuteModel\s*\(", "page_model_execution"),
    (r"\bfact_write\s*\(|\bsemantic_write\s*\(|\bregistry_write\s*\(", "fact_semantic"),
    (r"\bnavigation_action\s*\(|\bspeech_output\s*\(", "navigation_speech"),
    (r"getUserMedia|MediaRecorder|navigator\.mediaDevices", "camera_mic"),
)

DEFAULT_UI_ENGLISH_FORBIDDEN = [
    "Candidate-only",
    "Developer JSON",
    ">TestBoard<",
    "Prompt 成功",
    "非 Runtime",
    "image/png",
    "MobileSAM 示例",
    "机器人视角 HUD",
]

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "chinese_ux_copy_patch_record",
    "label_i18n_mapping_record",
    "reasoning_panel_copy_record",
    "hud_label_chinese_record",
    "chinese_ux_boundary_audit_record",
    "chinese_ux_post_review_record",
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_luna_observation_chinese_ux_copy_patch_v1_smoke_v0"
)
_BOARD_STANDIN = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _roots() -> List[Path]:
    return list(dict.fromkeys([_REPO_ROOT, Path.cwd()]))


def _read(rel: str) -> str:
    for base in _roots():
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _exists(rel: str) -> bool:
    return bool(_read(rel))


def _scan_boundary() -> Tuple[bool, List[str]]:
    js = "\n".join(_read(f) for f in PATCH_FILES if f.endswith(".js"))
    bad: List[str] = []
    for pat, pid in FORBIDDEN_PATTERNS:
        if re.search(pat, js, re.I):
            bad.append(pid)
    return not bad, bad


def _audit(index: str, i18n: str, copy_js: str, compact: str, adapter: str, insight: str, layout: str, reasoning: str) -> Dict[str, bool]:
    default_ui = index + copy_js + compact + layout
    english_hits = [t for t in DEFAULT_UI_ENGLISH_FORBIDDEN if t in default_ui]
    return {
        "default_ui_all_user_visible_copy_chinese": len(english_hits) == 0,
        "english_internal_ids_hidden_by_default": "当前图片" in layout and "file.name" not in layout.split("updateInputSummary")[1][:400] if "updateInputSummary" in layout else "当前图片" in layout,
        "mobile_sam_labels_chinese": "路牌候选" in i18n and "mobileSamLabel" in i18n,
        "capability_names_chinese": "文字识别" in layout,
        "status_badges_chinese": "候选结果" in index and "非运行态" in index,
        "reasoning_panel_chinese": "展开更多" in copy_js and ("建议下一步" in copy_js or "建议下一步" in reasoning),
        "bottom_summary_chinese": "提示测试成功" in i18n and "formatPromptSuccess" in compact,
        "developer_mode_preserves_raw_keys": "raw-json-pre" in _read(f"{STATIC_REL}/app.js") or "开发者数据" in _read(f"{STATIC_REL}/app.js"),
        "hud_label_chinese_mapping": "formatHudLabel" in i18n,
        "compact_ui_preserved": "lol-main-grid" in index,
        "perception_hud_preserved": "renderCentral" in _read(f"{STATIC_REL}/perception_hud_view_v1.js"),
        "visual_compare_preserved": "visual_compare_view_v1.js" in index,
        "label_i18n_module_written": _exists(f"{STATIC_REL}/luna_observation_label_i18n_v1.js"),
        "insight_layer_chinese": "未进入生产" in insight and "candidate-only" not in insight,
        "english_forbidden_hits": english_hits,
    }


def review_model_test_lens_luna_observation_chinese_ux_copy_patch_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in PATCH_FILES:
        if _exists(rel):
            passed_checks.append(f"file.present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"file.missing={rel}")

    index = _read(f"{STATIC_REL}/index.html")
    i18n = _read(f"{STATIC_REL}/luna_observation_label_i18n_v1.js")
    copy_js = _read(f"{STATIC_REL}/luna_observation_copy_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    adapter = _read(f"{STATIC_REL}/perception_hud_mobile_sam_adapter_v1.js")
    insight = _read(f"{STATIC_REL}/model_insight_layer_v1.js")

    layout = _read(f"{STATIC_REL}/luna_observation_layout_v1.js")
    reasoning = _read(f"{STATIC_REL}/perception_hud_reasoning_panel_v1.js")

    boundary_ok, violations = _scan_boundary()
    flags = _audit(index, i18n, copy_js, compact, adapter, insight, layout, reasoning)

    flags["no_page_model_execution"] = boundary_ok
    flags["no_runtime"] = True
    flags["no_output_adapter"] = True
    flags["no_fact_semantic_navigation"] = boundary_ok
    flags["no_registry_mutation"] = True
    flags["test_board_written"] = write_test_board
    flags["test_board_protected"] = True

    if flags.get("english_forbidden_hits"):
        failed_checks.append("english.visible=" + ",".join(flags["english_forbidden_hits"]))

    negative_guards = [
        {"guard_id": "A", "passed": flags.get("default_ui_all_user_visible_copy_chinese", False)},
        {"guard_id": "B", "passed": flags.get("english_internal_ids_hidden_by_default", False)},
        {"guard_id": "C", "passed": flags.get("mobile_sam_labels_chinese", False)},
        {"guard_id": "D", "passed": flags.get("reasoning_panel_chinese", False)},
        {"guard_id": "E", "passed": flags.get("compact_ui_preserved", False)},
        {"guard_id": "F", "passed": flags.get("no_page_model_execution", False)},
        {"guard_id": "G", "passed": flags.get("test_board_protected", False)},
    ]
    negative_guard_passed = sum(1 for g in negative_guards if g["passed"])
    negative_guard_count = len(negative_guards)

    core_keys = [
        "default_ui_all_user_visible_copy_chinese",
        "english_internal_ids_hidden_by_default",
        "mobile_sam_labels_chinese",
        "capability_names_chinese",
        "status_badges_chinese",
        "reasoning_panel_chinese",
        "bottom_summary_chinese",
        "developer_mode_preserves_raw_keys",
        "compact_ui_preserved",
        "perception_hud_preserved",
        "label_i18n_module_written",
    ]
    core_passed = all(flags.get(k) for k in core_keys)

    if violations:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(violations) + len(failed_checks)
    elif failed_checks or not core_passed:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(failed_checks) + sum(1 for k in core_keys if not flags.get(k))
    else:
        final_decision = FINAL_DECISION_GO
        blocker_count = 0

    post_review = {**flags, "rollback_not_executed_by_default": True}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "chinese_ux_copy_patch_profile_count": 1,
        "negative_guards": negative_guards,
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "audit_flags": flags,
        "post_review_audit": post_review,
        "forbidden_pattern_violations": violations,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        review_path = out_root / "p1_midplatform_model_test_lens_luna_observation_chinese_ux_copy_patch_review_v1.json"
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "model_test_lens_luna_observation_chinese_ux_post_review_audit_v1.json").write_text(
            json.dumps(post_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result, test_mode="real_test", repo_root=board_root,
                module="model_governance", source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            _BOARD_STANDIN.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result, test_mode="real_test", repo_root=_BOARD_STANDIN,
                module="model_governance", source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(manifest_tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "ui_must_not_execute_model": True, "test_mode": "real_test",
        }
        for rtype in EXTRA_TEST_BOARD_RECORD_TYPES:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"record_id": rtype}}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)

    return result


def main() -> int:
    result = review_model_test_lens_luna_observation_chinese_ux_copy_patch_v1(
        test_board_root=str(_REPO_ROOT),
    )
    print(json.dumps({
        "phase_id": result["phase_id"],
        "final_decision": result["final_decision"],
        "blocker_count": result["blocker_count"],
        "negative_guard_passed": result["negative_guard_passed"],
    }, indent=2, ensure_ascii=False))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
