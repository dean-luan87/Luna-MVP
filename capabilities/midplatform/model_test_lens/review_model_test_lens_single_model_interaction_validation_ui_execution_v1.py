# -*- coding: utf-8 -*-
"""P1 Single Model Interaction Validation — UI execution review v1."""

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
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001"
PLANNING_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_PLANNING_GO"
VALIDATION_REL = "capabilities/midplatform/model_test_lens/single_model_interaction_validation"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_BLOCKED"

NEW_MODULES: Tuple[str, ...] = (
    f"{VALIDATION_REL}/single_model_interaction_validation_ui_execution_plan_v1.md",
    f"{STATIC_REL}/midplatform_interaction_copy_v1.js",
    f"{STATIC_REL}/midplatform_result_processor_v1.js",
    f"{STATIC_REL}/midplatform_interaction_panel_v1.js",
    f"{STATIC_REL}/midplatform_interaction_state_v1.js",
    f"{_PKG}/review_model_test_lens_single_model_interaction_validation_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/result_layer_panel_v1.js",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_detection\b|\bexecute_ocr\b", "other_runner_execute"),
    (r"modify_mask|modifyMask", "modify_mask"),
    (r"确认这是路牌|这是路牌", "fact_label_assertion"),
    (r"\bauto_train\b|直接训练模型", "direct_training"),
    (r"MobileSAM.*推荐.*OCR", "mobilesam_recommends_ocr_wording"),
)

NEGATIVE_GUARD_KEYS: Tuple[Tuple[str, str], ...] = (
    ("A", "result_candidate_not_fact"),
    ("B", "result_analysis_not_fact"),
    ("C", "midplatform_analysis_not_model_output"),
    ("D", "midplatform_analysis_not_training_directive"),
    ("E", "correction_analysis_not_mask_mutation"),
    ("F", "correction_training_requires_review"),
    ("G", "user_preference_not_training_data"),
    ("H", "priority_signal_not_ground_truth"),
    ("I", "route_candidate_not_execution"),
    ("J", "ocr_candidate_not_ocr_result"),
    ("K", "no_ocr_runner_execution"),
    ("L", "no_detection_runner_execution"),
    ("M", "upstream_planning_go"),
    ("N", "midplatform_panel_wired"),
    ("O", "case1_processor_wired"),
    ("P", "case2_correction_attribution_wired"),
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _bundle() -> str:
    files = (
        "midplatform_interaction_panel_v1.js",
        "midplatform_result_processor_v1.js",
        "midplatform_interaction_state_v1.js",
        "result_layer_panel_v1.js",
        "human_correction_midplatform_analyzer_v1.js",
        "app.js",
        "luna_observation_compact_ui_v1.js",
    )
    return "\n".join(_read(f"{STATIC_REL}/{f}") for f in files)


def _audit() -> Dict[str, bool]:
    panel = _read(f"{STATIC_REL}/midplatform_interaction_panel_v1.js")
    processor = _read(f"{STATIC_REL}/midplatform_result_processor_v1.js")
    state = _read(f"{STATIC_REL}/midplatform_interaction_state_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    index = _read(f"{STATIC_REL}/index.html")
    copy = _read(f"{STATIC_REL}/midplatform_interaction_copy_v1.js")
    hc = _read(f"{STATIC_REL}/human_correction_midplatform_analyzer_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_single_model_interaction_validation_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_single_model_interaction_validation_planning_review_v1.json"
    )

    return {
        "upstream_planning_go": planning.get("final_decision") == PLANNING_GO,
        "midplatform_panel_wired": (
            "MidplatformInteractionPanel" in compact
            and "lol-right-midplatform-host" in compact
            and "buildMidplatformPackage" in app
        ),
        "case1_processor_wired": "processFromUiState" in processor and "midplatform_result_processor_v1.js" in index,
        "case2_correction_attribution_wired": (
            "renderCorrectionBlock" in panel and "analyzeCorrection" in hc
        ),
        "result_candidate_not_fact": "result_candidate_not_fact" in panel and "not_fact" in processor,
        "result_analysis_not_fact": "result_analysis_not_fact" in panel,
        "midplatform_analysis_not_model_output": "midplatform_analysis_not_model_output" in panel,
        "midplatform_analysis_not_training_directive": "midplatform_analysis_not_training_directive" in panel,
        "correction_analysis_not_mask_mutation": "correction_analysis_not_mask_mutation" in panel,
        "correction_training_requires_review": "pending_review" in panel and "needs_owner_review" in hc,
        "user_preference_not_training_data": (
            "user_preference_not_training_data" in panel
            and ("not_applicable" in hc or "training_candidate" in hc)
        ),
        "priority_signal_not_ground_truth": "priority_update_signal" in panel and "priority_signal" in hc,
        "route_candidate_not_execution": "route_candidate_not_execution" in panel and "not_runner_execution" in processor,
        "ocr_candidate_not_ocr_result": "ocr_candidate_not_ocr_result" in panel and "ocr_runner_forbidden" in processor,
        "no_ocr_runner_execution": (
            "ocr_runner_forbidden" in copy and ("本阶段不跑 OCR" in copy or "ocr_runner_forbidden" in processor)
        ),
        "no_detection_runner_execution": "detection_runner_forbidden" in state,
        "mobilesam_not_ocr_wording": "MobileSAM ≠ OCR" in copy or "MobileSAM ≠ OCR" in panel,
        "index_scripts_wired": all(
            s in index for s in (
                "midplatform_interaction_panel_v1.js",
                "midplatform_result_processor_v1.js",
            )
        ),
    }


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _bundle(), re.I)]
    flags = _audit()

    guards = []
    for gid, key in NEGATIVE_GUARD_KEYS:
        passed = bool(flags.get(key, False))
        guards.append({"guard_id": gid, "key": key, "passed": passed})
        if not passed:
            failed.append(f"guard.{gid}.fail={key}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed) + len(violations)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_single_model_interaction_validation_ui_execution_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "ui_execution": True,
        "ocr_runner_forbidden": True,
        "detection_runner_forbidden": True,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_violations": violations,
        "blocker_count": blocker_count,
        "failed_checks": failed + [f"forbidden.{v}" for v in violations],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_single_model_interaction_validation_ui_execution_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="post_review", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="post_review", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(Path(tb["test_board_dir"]))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
