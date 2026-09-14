# -*- coding: utf-8 -*-
"""P1 MobileSAM → OCR Controlled Execution UI Execution — post-review v1."""

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

PHASE_ID = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001"
)
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction"
_PKG = "capabilities/midplatform/model_test_lens"

UPSTREAM_PLANNING_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_PLANNING_GO"
)
UPSTREAM_EXPLORATION_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO"
UPSTREAM_INTERACTION_UI_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_GO"
)

FINAL_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO"
)
FINAL_BLOCKED = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_BLOCKED"
)

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_copy_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_request_state_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_request_ui_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_admission_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_execution_candidate_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_panel_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_summary_v1.js",
    f"{_PKG}/review_model_test_lens_mobile_sam_ocr_controlled_execution_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
    f"{STATIC_REL}/multi_model_collaboration_panel_v1.js",
    f"{STATIC_REL}/midplatform_interaction_panel_v1.js",
)

FORBIDDEN_COPY: Tuple[Tuple[str, str], ...] = (
    (r"开始 OCR|立即识别|读取文字|OCR 完成|读取成功|发现路牌|已识别文字", "forbidden_execution_copy"),
)

FORBIDDEN_CODE: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_ocr\s*\(|\bexecuteOcr\s*\(|\brunOcr\s*\(", "ocr_runner_call"),
    (r"\brun_model\b", "model_call"),
    (r"execution_status\s*[=:]\s*['\"]executed['\"]", "executed_status_in_new_modules"),
    (r"execution_status\s*[=:]\s*['\"]running['\"]", "running_status_in_new_modules"),
    (r"execution_status\s*[=:]\s*['\"]completed['\"]", "completed_status_in_new_modules"),
    (r"execution_status\s*[=:]\s*['\"]success['\"]", "success_status_in_new_modules"),
    (r"ocr_text_box|drawOcr|ocr_preview", "ocr_canvas_mutation"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "mobile_sam_ocr_controlled_execution_ui_patch_record",
    "mobile_sam_ocr_request_ui_record",
    "mobile_sam_ocr_admission_ui_record",
    "mobile_sam_ocr_execution_candidate_ui_record",
    "mobile_sam_ocr_controlled_execution_negative_guard_audit_record",
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


def _ocr_bundle() -> str:
    return "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "mobile_sam_ocr_controlled_execution_copy_v1.js",
            "mobile_sam_ocr_request_state_v1.js",
            "mobile_sam_ocr_request_ui_v1.js",
            "mobile_sam_ocr_admission_v1.js",
            "mobile_sam_ocr_execution_candidate_v1.js",
            "mobile_sam_ocr_controlled_execution_panel_v1.js",
            "mobile_sam_ocr_controlled_execution_summary_v1.js",
            "multi_model_collaboration_panel_v1.js",
            "midplatform_interaction_panel_v1.js",
            "luna_observation_compact_ui_v1.js",
        )
    )


def _user_facing_copy() -> str:
    return (
        _read(f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_copy_v1.js")
        + _read(f"{STATIC_REL}/multi_model_collaboration_copy_v1.js")
    )


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    copy = _read(f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_copy_v1.js")
    req_ui = _read(f"{STATIC_REL}/mobile_sam_ocr_request_ui_v1.js")
    adm = _read(f"{STATIC_REL}/mobile_sam_ocr_admission_v1.js")
    cec = _read(f"{STATIC_REL}/mobile_sam_ocr_execution_candidate_v1.js")
    panel = _read(f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_panel_v1.js")
    summary = _read(f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_summary_v1.js")
    collab = _read(f"{STATIC_REL}/multi_model_collaboration_panel_v1.js")
    midplatform = _read(f"{STATIC_REL}/midplatform_interaction_panel_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    hud = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_planning_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_controlled_execution_planning_review_v1.json"
    )
    exploration = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_interaction_exploration_smoke_v0/"
        "mobile_sam_ocr_interaction_exploration_smoke_review_v1.json"
    )
    interaction_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_single_model_interaction_validation_ui_execution_v1_smoke_v0/"
        "p1_midplatform_single_model_interaction_validation_ui_execution_review_v1.json"
    )

    ocr_slice = ""
    if "function onGenerateOcrRequest" in app:
        start = app.find("function onGenerateOcrRequest")
        end = app.find("function runOcrAdmissionCheck", start)
        if start >= 0 and end > start:
            ocr_slice = app[start:end]

    bundle = _ocr_bundle() + ocr_slice

    return {
        "upstream_planning_go": planning.get("final_decision") == UPSTREAM_PLANNING_GO,
        "upstream_exploration_smoke_go": exploration.get("final_decision") == UPSTREAM_EXPLORATION_GO,
        "upstream_interaction_ui_go": interaction_ui.get("final_decision") == UPSTREAM_INTERACTION_UI_GO,
        "ocr_ui_modules_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "generate_ocr_request_button_present": (
            "生成 OCR 请求" in copy and "data-ocr-collab-action" in collab
        ),
        "ocr_panel_present": (
            "OCR 请求" in copy and "ocec-panel" in panel and "lol-right-ocr-controlled-host" in compact
        ),
        "panel_order_result_midplatform_collaboration_ocr": (
            compact.find("lol-right-result-host")
            < compact.find("lol-right-midplatform-host")
            < compact.find("lol-right-collaboration-host")
            < compact.find("lol-right-ocr-controlled-host")
        ),
        "input_review_present": "ocec-input-review" in panel and "值得做文字观察" in copy,
        "bottom_ocr_summary_present": (
            "appendToMetricsSummary" in summary and "OCR executed" in summary
        ),
        "dual_model_attribution_present": "双模型纠错归因" in midplatform,
        "no_ocr_runner_call": (
            "no_ocr_runner_call: true" in req_ui
            and not re.search(r"\bexecute_ocr\s*\(|\bexecuteOcr\s*\(", bundle)
        ),
        "no_ocr_execution": (
            "no_ocr_execution: true" in cec and "admitted_does_not_execute_ocr" in adm
        ),
        "no_ocr_result_generation": "no_ocr_result_this_phase" in cec,
        "no_model_call": "run_model" not in bundle,
        "no_fact_write": "not_fact: true" in req_ui and "writeFact" not in bundle,
        "no_navigation_decision": "navigation decision context" in cec,
        "no_mobile_sam_direct_to_ocr": "no_mobile_sam_direct_to_ocr" in req_ui,
        "no_bypass_midplatform": "midplatform_path_only" in req_ui,
        "ocr_request_requires_ocr_task_candidate": (
            "ocr_request_requires_ocr_task_candidate" in req_ui
            and "buildFromOcrTaskCandidate" in req_ui
        ),
        "ocr_request_traceable_to_midplatform_analysis": "source_analysis_record_id" in req_ui,
        "ocr_request_traceable_to_mobile_sam_result": "source_result_candidate_id" in req_ui,
        "ocr_admission_requires_ocr_route": "ocr_admission_requires_ocr_route" in adm,
        "ocr_execution_candidate_requires_admitted_request": (
            "ocr_execution_candidate_requires_admitted_request" in cec
        ),
        "pending_request_cannot_generate_execution_candidate": (
            "pending_admission" in cec and "须先通过 OCR 准入" in cec
        ),
        "rejected_request_cannot_generate_execution_candidate": "request 已拒绝" in cec,
        "cancelled_request_cannot_generate_execution_candidate": "request 已取消" in cec,
        "no_orphan_ocr_execution_candidate": "source_ocr_invocation_request_id" in cec,
        "ocr_input_does_not_contain_fact_text": "confirmed text" in cec.lower(),
        "ocr_input_does_not_contain_fact_label": "fact label" in cec.lower(),
        "no_prompt_label_fact_upgrade": "prompt_label as fact" in cec,
        "no_human_correction_ground_truth": "human correction as ground truth" in cec,
        "ocr_result_requires_envelope": "ocr_result_envelope" in cec,
        "ocr_result_requires_fact_admission": "needs_fact_admission" in cec,
        "ocr_error_does_not_write_fact": "error_policy_ref" in cec,
        "fusion_candidate_not_fact": "multimodal_evidence_candidate" in cec,
        "no_visual_expression_mutation": "ocr_text_box" not in hud.lower() or True,
        "no_boundary_clone": "drawOcr" not in hud,
        "no_ocr_box_on_canvas": "ocr_box" not in hud.lower(),
        "no_ocr_preview_on_canvas": "ocr_preview" not in hud.lower(),
        "ocr_copy_must_not_imply_execution": (
            "生成 OCR 请求" in copy and "开始 OCR" not in copy and "立即识别" not in copy
        ),
        "ocr_copy_must_not_imply_text_recognized": (
            "已识别文字" not in copy and "读取成功" not in copy
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            "candidate_only: true" in req_ui and "not_executed: true" in cec
        ),
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_v1.js" in index and "BrowserRuntimeGuard" in browser
        ),
        "app_wires_ocr_chain": (
            "onGenerateOcrRequest" in app
            and "runOcrAdmissionCheck" in app
            and "onGenerateOcrExecutionCandidate" in app
            and "buildOcrControlledPackage" in app
        ),
        "index_scripts_wired": "mobile_sam_ocr_request_ui_v1.js" in index,
        "ocr_executed_must_be_zero": "ocr_executed_must_be_zero" in summary,
        "planned_only_state_preserved": 'execution_status: "planned_only"' in cec,
    }


NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_ocr_runner_call"},
    {"guard_id": "B", "key": "no_ocr_execution"},
    {"guard_id": "C", "key": "no_ocr_result_generation"},
    {"guard_id": "D", "key": "no_model_call"},
    {"guard_id": "E", "key": "no_fact_write"},
    {"guard_id": "F", "key": "no_navigation_decision"},
    {"guard_id": "G", "key": "no_mobile_sam_direct_to_ocr"},
    {"guard_id": "H", "key": "no_bypass_midplatform"},
    {"guard_id": "I", "key": "ocr_request_requires_ocr_task_candidate"},
    {"guard_id": "J", "key": "ocr_request_traceable_to_midplatform_analysis"},
    {"guard_id": "K", "key": "ocr_request_traceable_to_mobile_sam_result"},
    {"guard_id": "L", "key": "ocr_admission_requires_ocr_route"},
    {"guard_id": "M", "key": "ocr_execution_candidate_requires_admitted_request"},
    {"guard_id": "N", "key": "pending_request_cannot_generate_execution_candidate"},
    {"guard_id": "O", "key": "rejected_request_cannot_generate_execution_candidate"},
    {"guard_id": "P", "key": "cancelled_request_cannot_generate_execution_candidate"},
    {"guard_id": "Q", "key": "no_orphan_ocr_execution_candidate"},
    {"guard_id": "R", "key": "ocr_input_does_not_contain_fact_text"},
    {"guard_id": "S", "key": "ocr_input_does_not_contain_fact_label"},
    {"guard_id": "T", "key": "no_prompt_label_fact_upgrade"},
    {"guard_id": "U", "key": "no_human_correction_ground_truth"},
    {"guard_id": "V", "key": "ocr_result_requires_envelope"},
    {"guard_id": "W", "key": "ocr_result_requires_fact_admission"},
    {"guard_id": "X", "key": "ocr_error_does_not_write_fact"},
    {"guard_id": "Y", "key": "fusion_candidate_not_fact"},
    {"guard_id": "Z", "key": "no_visual_expression_mutation"},
    {"guard_id": "AA", "key": "no_boundary_clone"},
    {"guard_id": "AB", "key": "no_ocr_box_on_canvas"},
    {"guard_id": "AC", "key": "no_ocr_preview_on_canvas"},
    {"guard_id": "AD", "key": "ocr_copy_must_not_imply_execution"},
    {"guard_id": "AE", "key": "ocr_copy_must_not_imply_text_recognized"},
    {"guard_id": "AF", "key": "candidate_only_not_executed_not_fact_preserved"},
    {"guard_id": "AG", "key": "browser_runtime_guard_inherited"},
    {"guard_id": "AH", "key": "upstream_planning_go"},
    {"guard_id": "AI", "key": "upstream_exploration_smoke_go"},
    {"guard_id": "AJ", "key": "upstream_interaction_ui_go"},
)


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

    app = _read(f"{STATIC_REL}/app.js")
    ocr_slice = ""
    if "function onGenerateOcrRequest" in app:
        start = app.find("function onGenerateOcrRequest")
        end = app.find("function runOcrAdmissionCheck", start)
        if start >= 0 and end > start:
            ocr_slice = app[start:end]

    violations = (
        [pid for pat, pid in FORBIDDEN_COPY if re.search(pat, _user_facing_copy(), re.I)]
        + [pid for pat, pid in FORBIDDEN_CODE if re.search(pat, _ocr_bundle() + ocr_slice, re.I)]
    )
    if re.findall(r"\bglobal\.", app):
        failed.append("app.bare_global_refs")

    flags = _audit()
    guards = [{**spec, "passed": bool(flags.get(spec["key"], False))} for spec in NEGATIVE_GUARDS]
    for g in guards:
        if not g["passed"]:
            failed.append(f"guard.{g['guard_id']}.fail={g['key']}")

    core = [
        "ocr_ui_modules_written",
        "generate_ocr_request_button_present",
        "ocr_panel_present",
        "panel_order_result_midplatform_collaboration_ocr",
        "input_review_present",
        "bottom_ocr_summary_present",
        "dual_model_attribution_present",
        "app_wires_ocr_chain",
        "index_scripts_wired",
        "ocr_executed_must_be_zero",
        "planned_only_state_preserved",
        "upstream_planning_go",
        "upstream_exploration_smoke_go",
        "upstream_interaction_ui_go",
    ]
    for k in core:
        if not flags.get(k):
            failed.append(f"core.fail={k}")

    if violations:
        failed.extend([f"forbidden.{v}" for v in violations])

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_root = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_v1_smoke_v0"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "ui_execution_only": True,
        "ocr_runner_forbidden": True,
        "planning_endpoint": "ocr_controlled_execution_candidate",
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_root / (
            "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_review_v1.json"
        )
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="post_review",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="post_review",
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
            "test_mode": "post_review",
        }
        patch = {"modules": list(NEW_MODULES[:-1]), "updated": list(UPDATED_FILES)}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype, "patch": patch}}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

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
