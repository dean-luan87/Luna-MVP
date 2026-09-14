# -*- coding: utf-8 -*-
"""P1 Detection/OCR Controlled Runner Execution UI Execution — post-review v1."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001"
)
PLANNING_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_PLANNING_GO"
)
ADMISSION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_RUNNER_INVOCATION_ADMISSION_EXECUTION_GO"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/controlled_runner_execution"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"

NEW_MODULES: Tuple[str, ...] = (
    f"{STATIC_REL}/controlled_runner_execution_copy_v1.js",
    f"{STATIC_REL}/controlled_runner_execution_state_v1.js",
    f"{STATIC_REL}/controlled_runner_execution_ui_v1.js",
    f"{STATIC_REL}/controlled_runner_execution_panel_v1.js",
    f"{STATIC_REL}/controlled_runner_execution_summary_v1.js",
    f"{_PKG}/review_model_test_lens_detection_ocr_controlled_runner_execution_ui_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/runner_invocation_admission_panel_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_detection\b|\bexecute_ocr\b", "runner_execute"),
    (r"\brun_model\b", "model_call"),
    (r"开始检测|开始 OCR|立即执行|运行模型|执行 runner|执行完成|识别结果", "forbidden_execution_copy"),
    (r"execution_status\s*[=:]\s*['\"]executed['\"]", "executed_status_in_code"),
    (r"execution_status\s*[=:]\s*['\"]running['\"]", "running_status_in_code"),
    (r"execution_status\s*[=:]\s*['\"]executing['\"]", "executing_status_in_code"),
    (r"execution_status\s*[=:]\s*['\"]completed['\"]", "completed_status_in_code"),
    (r"execution_status\s*[=:]\s*['\"]success['\"]", "success_status_in_code"),
    (r"execution_status\s*[=:]\s*['\"]failed_model_output['\"]", "failed_model_output_status"),
)

EXTRA_RECORDS: Tuple[str, ...] = (
    "controlled_runner_execution_ui_patch_record",
    "controlled_runner_execution_panel_record",
    "controlled_runner_execution_state_record",
    "controlled_runner_execution_negative_guard_audit_record",
)

FINAL_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_UI_EXECUTION_GO"
)
FINAL_BLOCKED = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_UI_EXECUTION_BLOCKED"
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


def _bundle() -> str:
    return "\n".join(
        _read(f"{STATIC_REL}/{f}")
        for f in (
            "controlled_runner_execution_copy_v1.js",
            "controlled_runner_execution_state_v1.js",
            "controlled_runner_execution_ui_v1.js",
            "controlled_runner_execution_panel_v1.js",
            "controlled_runner_execution_summary_v1.js",
            "runner_invocation_admission_panel_v1.js",
            "luna_observation_compact_ui_v1.js",
        )
    )


def _audit() -> Dict[str, bool]:
    index = _read(f"{STATIC_REL}/index.html")
    app = _read(f"{STATIC_REL}/app.js")
    copy = _read(f"{STATIC_REL}/controlled_runner_execution_copy_v1.js")
    ui = _read(f"{STATIC_REL}/controlled_runner_execution_ui_v1.js")
    state_js = _read(f"{STATIC_REL}/controlled_runner_execution_state_v1.js")
    panel = _read(f"{STATIC_REL}/controlled_runner_execution_panel_v1.js")
    summary = _read(f"{STATIC_REL}/controlled_runner_execution_summary_v1.js")
    adm_panel = _read(f"{STATIC_REL}/runner_invocation_admission_panel_v1.js")
    compact = _read(f"{STATIC_REL}/luna_observation_compact_ui_v1.js")
    candidate_schema = _load_json(f"{SCHEMA_REL}/controlled_runner_execution_candidate_schema_v1.json")
    hud = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_planning_review_v1.json"
    )
    admission = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_runner_invocation_admission_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_runner_invocation_admission_execution_review_v1.json"
    )

    gen_slice = ""
    if "onGenerateExecutionCandidate" in app:
        start = app.find("function onGenerateExecutionCandidate")
        end = app.find("function onExecutionAction", start)
        if start >= 0 and end > start:
            gen_slice = app[start:end]

    return {
        "upstream_planning_go": planning.get("final_decision") == PLANNING_GO,
        "upstream_admission_execution_go": admission.get("final_decision") == ADMISSION_GO,
        "execution_ui_modules_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "execution_candidate_schema_consumed": (
            candidate_schema.get("schema_id") == "ControlledRunnerExecutionCandidateSchemaV1"
        ),
        "generate_execution_candidate_button_present": (
            "generate-execution-candidate" in adm_panel and "生成受控执行候选" in copy
        ),
        "execution_panel_present": (
            "受控执行候选" in copy and "crec-panel" in panel and "lol-right-execution-host" in compact
        ),
        "input_review_present": (
            "crec-input-review" in panel and "Detection Candidate" in copy and "OCR Candidate" in copy
        ),
        "bottom_execution_summary_present": (
            "crec-summary-inline" in summary and "appendToMetricsSummary" in summary
        ),
        "no_runner_execution": "noRunnerExecution: true" in ui and "execute_detection" not in gen_slice,
        "no_detection_runner_call": "execute_detection" not in _bundle() + gen_slice,
        "no_ocr_runner_call": "execute_ocr" not in _bundle() + gen_slice,
        "no_model_call": "noModelCall: true" in ui and "run_model" not in gen_slice,
        "no_fact_write": "not_fact: true" in ui and "writeFact" not in _bundle(),
        "no_navigation_decision": "no_navigation_decision" in ui,
        "no_auto_runner_trigger": "manual_controlled" in ui,
        "no_runner_invocation": "no_runner_invocation" in ui or "noRunnerInvocation: true" in ui,
        "no_execution_candidate_equals_execution": (
            "execution_candidate_not_runner_execution" in ui and "not_runner_execution" in ui
        ),
        "no_execution_candidate_result": "execution_candidate_not_model_output" in ui,
        "no_execution_candidate_box_on_canvas": (
            "execution_box" not in hud.lower() and "noExecutionCandidateBoxOnCanvas" in panel
        ),
        "execution_candidate_requires_admitted_request": (
            'admission_decision !== "admitted"' in ui or 'admission_decision === "admitted"' in ui
        ),
        "execution_candidate_not_fact": "not_fact: true" in ui and "needs_fact_admission" in panel,
        "execution_candidate_not_model_output": "execution_candidate_not_model_output" in ui,
        "planned_only_state_preserved": (
            'execution_status: "planned_only"' in ui and "planned_only" in state_js
        ),
        "rejected_request_cannot_generate_execution_candidate": "hintRejected" in copy,
        "pending_request_cannot_generate_execution_candidate": "hintPending" in copy,
        "cancelled_request_cannot_generate_execution_candidate": "hintCancelled" in copy,
        "no_orphan_execution_candidate": "source_invocation_request_id" in ui,
        "execution_candidate_traceable_to_invocation_request": "source_invocation_request_id" in ui,
        "execution_candidate_traceable_to_admission_result": "source_admission_result_id" in ui,
        "execution_candidate_traceable_to_task_candidate": "source_runner_task_candidate_id" in ui,
        "execution_candidate_traceable_to_attention_record": "source_attention_record_id" in ui,
        "execution_candidate_traceable_to_region_id": "source_region_id" in ui,
        "detection_input_does_not_contain_fact_label": (
            "fact label" in ui.lower() or "fact label" in copy.lower()
        ),
        "ocr_input_does_not_contain_fact_text": (
            "fact text" in ui.lower() or "fact text" in copy.lower()
        ),
        "no_prompt_label_fact_upgrade": (
            "prompt_label as truth" in ui or "prompt_label as truth" in panel
        ),
        "no_human_correction_ground_truth": (
            ("ground truth" in copy.lower() or "ground truth" in ui.lower())
            and "priority signal" in ui
        ),
        "no_motion_confirmed_from_single_frame": "confirmed_dynamic" in ui,
        "runner_output_requires_envelope": "output_envelope_schema_ref" in ui,
        "runner_output_requires_fact_admission_before_fact_write": "needs_fact_admission" in panel,
        "no_visual_expression_mutation": "execution_box" not in hud.lower(),
        "no_boundary_clone": "drawRunner" not in hud,
        "no_execution_box_on_canvas": "execution_box" not in hud.lower(),
        "execution_copy_must_not_imply_execution": (
            "生成受控执行候选" in copy and "开始检测" not in copy and "开始 OCR" not in copy
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            "candidate_only: true" in ui and "not_executed: true" in ui
        ),
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_v1.js" in index and len(re.findall(r"\bglobal\.", app)) == 0
        ),
        "app_wires_execution_candidate_gate": (
            "onGenerateExecutionCandidate" in app and "buildExecutionPackage" in app
        ),
        "index_scripts_wired": "controlled_runner_execution_ui_v1.js" in index,
        "admission_panel_has_generate_button": "generate-execution-candidate" in adm_panel,
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    app = _read(f"{STATIC_REL}/app.js")
    gen_slice = ""
    if "onGenerateExecutionCandidate" in app:
        start = app.find("function onGenerateExecutionCandidate")
        end = app.find("function onExecutionAction", start)
        if start >= 0 and end > start:
            gen_slice = app[start:end]

    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _bundle() + gen_slice, re.I)]
    if re.findall(r"\bglobal\.", app):
        failed.append("app.bare_global_refs")

    flags = _audit()
    guards = [
        {"guard_id": "A", "key": "no_runner_execution", "passed": flags["no_runner_execution"]},
        {"guard_id": "B", "key": "no_detection_runner_call", "passed": flags["no_detection_runner_call"]},
        {"guard_id": "C", "key": "no_ocr_runner_call", "passed": flags["no_ocr_runner_call"]},
        {"guard_id": "D", "key": "no_model_call", "passed": flags["no_model_call"]},
        {"guard_id": "E", "key": "no_fact_write", "passed": flags["no_fact_write"]},
        {"guard_id": "F", "key": "no_navigation_decision", "passed": flags["no_navigation_decision"]},
        {"guard_id": "G", "key": "no_auto_runner_trigger", "passed": flags["no_auto_runner_trigger"]},
        {"guard_id": "H", "key": "no_runner_invocation", "passed": flags["no_runner_invocation"]},
        {"guard_id": "I", "key": "no_execution_candidate_equals_execution", "passed": flags["no_execution_candidate_equals_execution"]},
        {"guard_id": "J", "key": "no_execution_candidate_result", "passed": flags["no_execution_candidate_result"]},
        {"guard_id": "K", "key": "no_execution_candidate_box_on_canvas", "passed": flags["no_execution_candidate_box_on_canvas"]},
        {"guard_id": "L", "key": "execution_candidate_requires_admitted_request", "passed": flags["execution_candidate_requires_admitted_request"]},
        {"guard_id": "M", "key": "execution_candidate_not_fact", "passed": flags["execution_candidate_not_fact"]},
        {"guard_id": "N", "key": "execution_candidate_not_model_output", "passed": flags["execution_candidate_not_model_output"]},
        {"guard_id": "O", "key": "planned_only_state_preserved", "passed": flags["planned_only_state_preserved"]},
        {"guard_id": "P", "key": "rejected_request_cannot_generate_execution_candidate", "passed": flags["rejected_request_cannot_generate_execution_candidate"]},
        {"guard_id": "Q", "key": "pending_request_cannot_generate_execution_candidate", "passed": flags["pending_request_cannot_generate_execution_candidate"]},
        {"guard_id": "R", "key": "cancelled_request_cannot_generate_execution_candidate", "passed": flags["cancelled_request_cannot_generate_execution_candidate"]},
        {"guard_id": "S", "key": "no_orphan_execution_candidate", "passed": flags["no_orphan_execution_candidate"]},
        {"guard_id": "T", "key": "execution_candidate_traceable_to_invocation_request", "passed": flags["execution_candidate_traceable_to_invocation_request"]},
        {"guard_id": "U", "key": "execution_candidate_traceable_to_admission_result", "passed": flags["execution_candidate_traceable_to_admission_result"]},
        {"guard_id": "V", "key": "execution_candidate_traceable_to_task_candidate", "passed": flags["execution_candidate_traceable_to_task_candidate"]},
        {"guard_id": "W", "key": "execution_candidate_traceable_to_attention_record", "passed": flags["execution_candidate_traceable_to_attention_record"]},
        {"guard_id": "X", "key": "execution_candidate_traceable_to_region_id", "passed": flags["execution_candidate_traceable_to_region_id"]},
        {"guard_id": "Y", "key": "detection_input_does_not_contain_fact_label", "passed": flags["detection_input_does_not_contain_fact_label"]},
        {"guard_id": "Z", "key": "ocr_input_does_not_contain_fact_text", "passed": flags["ocr_input_does_not_contain_fact_text"]},
        {"guard_id": "AA", "key": "no_prompt_label_fact_upgrade", "passed": flags["no_prompt_label_fact_upgrade"]},
        {"guard_id": "AB", "key": "no_human_correction_ground_truth", "passed": flags["no_human_correction_ground_truth"]},
        {"guard_id": "AC", "key": "no_motion_confirmed_from_single_frame", "passed": flags["no_motion_confirmed_from_single_frame"]},
        {"guard_id": "AD", "key": "runner_output_requires_envelope", "passed": flags["runner_output_requires_envelope"]},
        {"guard_id": "AE", "key": "runner_output_requires_fact_admission_before_fact_write", "passed": flags["runner_output_requires_fact_admission_before_fact_write"]},
        {"guard_id": "AF", "key": "no_visual_expression_mutation", "passed": flags["no_visual_expression_mutation"]},
        {"guard_id": "AG", "key": "no_boundary_clone", "passed": flags["no_boundary_clone"]},
        {"guard_id": "AH", "key": "no_execution_box_on_canvas", "passed": flags["no_execution_box_on_canvas"]},
        {"guard_id": "AI", "key": "execution_copy_must_not_imply_execution", "passed": flags["execution_copy_must_not_imply_execution"]},
        {"guard_id": "AJ", "key": "candidate_only_not_executed_not_fact_preserved", "passed": flags["candidate_only_not_executed_not_fact_preserved"]},
        {"guard_id": "AK", "key": "browser_runtime_guard_inherited", "passed": flags["browser_runtime_guard_inherited"]},
        {"guard_id": "AL", "key": "upstream_planning_go", "passed": flags["upstream_planning_go"]},
        {"guard_id": "AM", "key": "upstream_admission_execution_go", "passed": flags["upstream_admission_execution_go"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "execution_ui_modules_written",
        "generate_execution_candidate_button_present",
        "execution_panel_present",
        "input_review_present",
        "bottom_execution_summary_present",
        "no_execution_candidate_equals_execution",
        "execution_candidate_requires_admitted_request",
        "planned_only_state_preserved",
        "execution_copy_must_not_imply_execution",
        "app_wires_execution_candidate_gate",
        "index_scripts_wired",
        "admission_panel_has_generate_button",
        "upstream_planning_go",
        "upstream_admission_execution_go",
    ]

    extra = len(violations) + len(failed)
    core_fail = sum(1 for k in core if not flags.get(k))
    guard_fail = len(guards) - ng_passed
    blockers = extra + core_fail + guard_fail
    decision = FINAL_GO if blockers == 0 else FINAL_BLOCKED

    out_root = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_ui_execution_v1_smoke_v0"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_phase": True,
        "controlled_runner_execution_ui_execution": True,
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

    if write_file:
        rp = out_root / (
            "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_ui_execution_review_v1.json"
        )
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
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
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True, "test_mode": "real_test",
        }
        patch = {"modules": list(NEW_MODULES[:-1]), "updated": list(UPDATED_FILES)}
        for rtype in EXTRA_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype, "patch": patch}}, indent=2, ensure_ascii=False) + "\n",
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
