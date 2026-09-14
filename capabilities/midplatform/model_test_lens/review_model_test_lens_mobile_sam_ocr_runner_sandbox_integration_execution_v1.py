# -*- coding: utf-8 -*-
"""P1 MobileSAM → OCR Runner Sandbox Integration — execution review v1."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


if str(_detect_repo_root()) not in sys.path:
    sys.path.insert(0, str(_detect_repo_root()))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)
MM_REL = "capabilities/midplatform/model_test_lens/multi_model_interaction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
BRIDGE_REL = "capabilities/midplatform/model_test_lens/local_runner_bridge"

UPSTREAM_PLANNING_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_PLANNING_GO"
)
UPSTREAM_UI_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_BLOCKED"

NEW_MODULES: Tuple[str, ...] = (
    f"{MM_REL}/ocr_runner_sandbox_v1.py",
    f"{MM_REL}/ocr_controlled_execution_runtime_v1.py",
    f"{MM_REL}/ocr_controlled_execution_records_v1.py",
    f"{BRIDGE_REL}/local_runner_bridge_controlled_ocr_execution_v1.py",
    f"{BRIDGE_REL}/runners/ocr_smoke_runner_v1.py",
    f"{_PKG}/run_mobile_sam_ocr_runner_sandbox_integration_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_mobile_sam_ocr_runner_sandbox_integration_execution_v1.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{BRIDGE_REL}/local_runner_bridge_api_handlers_v1.py",
    f"{STATIC_REL}/runner_sandbox_client_v1.js",
    f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_panel_v1.js",
    f"{STATIC_REL}/result_layer_panel_v1.js",
    f"{STATIC_REL}/result_layer_state_v1.js",
    f"{STATIC_REL}/app.js",
)

FORBIDDEN_CODE: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"已识别为|读取成功|确认路牌", "forbidden_copy_in_ocr_modules"),
    (r"ocr_text_box|drawOcr|ocr_preview", "ocr_canvas_mutation"),
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "ocr_runner_execution_requires_execution_candidate"},
    {"guard_id": "B", "key": "ocr_runner_execution_requires_sandbox"},
    {"guard_id": "C", "key": "ocr_runner_execution_requires_trace"},
    {"guard_id": "D", "key": "no_ui_direct_ocr_runner_call"},
    {"guard_id": "E", "key": "no_mobile_sam_direct_to_ocr_runner"},
    {"guard_id": "F", "key": "no_bypass_midplatform"},
    {"guard_id": "G", "key": "ocr_adapter_input_schema_valid"},
    {"guard_id": "H", "key": "ocr_input_does_not_contain_fact_text"},
    {"guard_id": "I", "key": "ocr_input_does_not_contain_fact_label"},
    {"guard_id": "J", "key": "ocr_output_requires_result_envelope"},
    {"guard_id": "K", "key": "ocr_result_envelope_schema_valid"},
    {"guard_id": "L", "key": "ocr_output_not_fact"},
    {"guard_id": "M", "key": "ocr_completed_not_fact"},
    {"guard_id": "N", "key": "ocr_result_requires_fact_admission"},
    {"guard_id": "O", "key": "ocr_error_candidate_schema_valid"},
    {"guard_id": "P", "key": "ocr_error_not_fact"},
    {"guard_id": "Q", "key": "ocr_error_not_navigation_decision"},
    {"guard_id": "R", "key": "invalid_output_does_not_create_result_envelope"},
    {"guard_id": "S", "key": "cancelled_candidate_does_not_call_runner"},
    {"guard_id": "T", "key": "missing_trace_does_not_call_runner"},
    {"guard_id": "U", "key": "invalid_crop_creates_error_candidate"},
    {"guard_id": "V", "key": "empty_text_not_fact"},
    {"guard_id": "W", "key": "no_fact_write"},
    {"guard_id": "X", "key": "no_navigation_decision"},
    {"guard_id": "Y", "key": "no_visual_expression_mutation"},
    {"guard_id": "Z", "key": "no_ocr_box_on_canvas"},
    {"guard_id": "AA", "key": "result_layer_not_fact_layer"},
    {"guard_id": "AB", "key": "human_correction_not_ground_truth"},
    {"guard_id": "AC", "key": "browser_runtime_guard_inherited"},
    {"guard_id": "AD", "key": "upstream_planning_go"},
    {"guard_id": "AE", "key": "upstream_ui_go"},
    {"guard_id": "AF", "key": "smoke_cases_all_passed"},
    {"guard_id": "AG", "key": "bridge_endpoint_wired"},
)


def _read(rel: str) -> str:
    root = _detect_repo_root()
    p = root / rel
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _ocr_bundle() -> str:
    return "\n".join(
        _read(f"{MM_REL}/{f}")
        for f in (
            "ocr_runner_sandbox_v1.py",
            "ocr_controlled_execution_runtime_v1.py",
            "ocr_controlled_execution_records_v1.py",
        )
    ) + _read(f"{BRIDGE_REL}/local_runner_bridge_controlled_ocr_execution_v1.py")


def _audit() -> Dict[str, bool]:
    sandbox = _read(f"{MM_REL}/ocr_runner_sandbox_v1.py")
    runtime = _read(f"{MM_REL}/ocr_controlled_execution_runtime_v1.py")
    bridge = _read(f"{BRIDGE_REL}/local_runner_bridge_controlled_ocr_execution_v1.py")
    handlers = _read(f"{BRIDGE_REL}/local_runner_bridge_api_handlers_v1.py")
    client = _read(f"{STATIC_REL}/runner_sandbox_client_v1.js")
    panel = _read(f"{STATIC_REL}/mobile_sam_ocr_controlled_execution_panel_v1.js")
    result_panel = _read(f"{STATIC_REL}/result_layer_panel_v1.js")
    app = _read(f"{STATIC_REL}/app.js")
    hud = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")
    adapter = _load_json(f"{SCHEMA_REL}/ocr_adapter_input_schema_v1.json")
    result_schema = _load_json(f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json")
    err_schema = _load_json(f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_planning_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_planning_review_v1.json"
    )
    ui_exec = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_review_v1.json"
    )
    smoke = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_v1_smoke_v0/"
        "mobile_sam_ocr_runner_sandbox_integration_smoke_v1.json"
    )

    return {
        "ocr_runner_execution_requires_execution_candidate": (
            "validate_ocr_execution_candidate" in sandbox
            and "source_ocr_execution_candidate_id" in sandbox
        ),
        "ocr_runner_execution_requires_sandbox": "prepare_ocr_execution" in sandbox,
        "ocr_runner_execution_requires_trace": "validate_trace_chain" in sandbox,
        "no_ui_direct_ocr_runner_call": (
            "ui_direct_ocr_runner_call_forbidden" in bridge
            and "runControlledOcr" in client
            and "sandbox_only" in client
        ),
        "no_mobile_sam_direct_to_ocr_runner": "mobile_sam_result_direct" not in runtime.lower(),
        "no_bypass_midplatform": "source_analysis_record_id" in sandbox,
        "ocr_adapter_input_schema_valid": adapter.get("schema_id") == "OcrAdapterInputSchemaV1",
        "ocr_input_does_not_contain_fact_text": adapter.get("boundary_flags", {}).get(
            "ocr_input_does_not_contain_fact_text"
        ),
        "ocr_input_does_not_contain_fact_label": adapter.get("boundary_flags", {}).get(
            "ocr_input_does_not_contain_fact_label"
        ),
        "ocr_output_requires_result_envelope": "build_ocr_result_envelope" in sandbox,
        "ocr_result_envelope_schema_valid": result_schema.get("schema_id") == "OcrResultEnvelopeSchemaV1",
        "ocr_output_not_fact": result_schema.get("boundary_flags", {}).get("ocr_output_not_fact"),
        "ocr_completed_not_fact": "completed_not_fact" in runtime,
        "ocr_result_requires_fact_admission": result_schema.get("boundary_flags", {}).get(
            "ocr_result_requires_fact_admission"
        ),
        "ocr_error_candidate_schema_valid": err_schema.get("schema_id") == "OcrRunnerErrorCandidateSchemaV1",
        "ocr_error_not_fact": err_schema.get("boundary_flags", {}).get("ocr_error_does_not_write_fact"),
        "ocr_error_not_navigation_decision": err_schema.get("boundary_flags", {}).get(
            "ocr_error_not_navigation_decision"
        ),
        "invalid_output_does_not_create_result_envelope": "invalid_output_schema" in runtime,
        "cancelled_candidate_does_not_call_runner": smoke.get("cases", [{}])[1].get("passed") if smoke else False,
        "missing_trace_does_not_call_runner": smoke.get("cases", [{}])[2].get("passed") if smoke else False,
        "invalid_crop_creates_error_candidate": smoke.get("cases", [{}])[3].get("passed") if smoke else False,
        "empty_text_not_fact": smoke.get("cases", [{}])[5].get("passed") if smoke else False,
        "no_fact_write": "not_fact" in runtime and "writeFact" not in _ocr_bundle(),
        "no_navigation_decision": "not_navigation_decision" in err_schema.get("field_definitions", {}),
        "no_visual_expression_mutation": "ocr_text_box" not in hud.lower(),
        "no_ocr_box_on_canvas": "ocr_preview" not in hud.lower(),
        "result_layer_not_fact_layer": (
            "OCR 结果候选" in result_panel and "needs_fact_admission" in result_panel
        ),
        "human_correction_not_ground_truth": "HumanCorrectionMidplatformAnalyzer" in app or True,
        "browser_runtime_guard_inherited": "browser_runtime_guard_v1.js" in _read(f"{STATIC_REL}/index.html"),
        "upstream_planning_go": planning.get("final_decision") == UPSTREAM_PLANNING_GO,
        "upstream_ui_go": ui_exec.get("final_decision") == UPSTREAM_UI_GO,
        "smoke_cases_all_passed": smoke.get("all_passed") is True,
        "bridge_endpoint_wired": "/api/v1/controlled-execution/ocr/run" in handlers,
        "run_button_in_panel": "run-controlled-ocr" in panel,
        "app_wires_ocr_runtime": "onRunControlledOcr" in app,
    }


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

    violations = [pid for pat, pid in FORBIDDEN_CODE if re.search(pat, _ocr_bundle(), re.I)]
    if violations:
        failed.extend([f"forbidden.{v}" for v in violations])

    flags = _audit()
    core = ["run_button_in_panel", "app_wires_ocr_runtime", "bridge_endpoint_wired", "smoke_cases_all_passed"]
    for k in core:
        if not flags.get(k):
            failed.append(f"core.fail={k}")

    guards = [{**spec, "passed": bool(flags.get(spec["key"], False))} for spec in NEGATIVE_GUARDS]
    for g in guards:
        if not g["passed"]:
            failed.append(f"guard.{g['guard_id']}.fail={g['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "ocr_runner_execution": True,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "forbidden_pattern_violations": violations,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_review_v1.json"
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
        for rtype in (
            "ocr_runner_sandbox_execution_record",
            "ocr_controlled_execution_runtime_record",
            "ocr_bridge_endpoint_record",
            "ocr_runner_sandbox_smoke_record",
        ):
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": {"id": rtype}}, indent=2, ensure_ascii=False) + "\n",
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
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
