# -*- coding: utf-8 -*-
"""P1 MobileSAM Single Model Execution Integration v1-002 — post-review."""

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
    "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002"
)
PLANNING_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_PLANNING_GO"
)
CONTROLLED_EXEC_UI_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_UI_EXECUTION_GO"
)

INTEGRATION_REL = (
    "capabilities/midplatform/model_test_lens/mobile_sam_single_model_execution_integration"
)
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/mobile_sam_single_model_execution"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
_PKG = "capabilities/midplatform/model_test_lens"
_BRIDGE = "capabilities/midplatform/model_test_lens/local_runner_bridge"

NEW_MODULES: Tuple[str, ...] = (
    f"{INTEGRATION_REL}/controlled_execution_records_v1.py",
    f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_executor_v1.py",
    f"{_BRIDGE}/local_runner_bridge_controlled_execution_v1.py",
    f"{STATIC_REL}/runner_sandbox_client_v1.js",
    f"{STATIC_REL}/result_layer_copy_v1.js",
    f"{STATIC_REL}/result_layer_state_v1.js",
    f"{STATIC_REL}/result_layer_panel_v1.js",
    f"{STATIC_REL}/result_layer_summary_v1.js",
    f"{SCHEMA_REL}/runner_execution_record_schema_v1.json",
    f"{SCHEMA_REL}/runner_error_candidate_schema_v1.json",
    f"{SCHEMA_REL}/result_envelope_record_schema_v1.json",
    f"{_PKG}/run_mobile_sam_controlled_execution_integration_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_mobile_sam_single_model_execution_integration_v1_002.py",
)

UPDATED_FILES: Tuple[str, ...] = (
    f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_v1.py",
    f"{_BRIDGE}/local_runner_bridge_api_handlers_v1.py",
    f"{STATIC_REL}/index.html",
    f"{STATIC_REL}/app.js",
    f"{STATIC_REL}/styles.css",
    f"{STATIC_REL}/controlled_runner_execution_ui_v1.js",
    f"{STATIC_REL}/controlled_runner_execution_panel_v1.js",
    f"{STATIC_REL}/runner_invocation_admission_panel_v1.js",
    f"{STATIC_REL}/luna_observation_compact_ui_v1.js",
)

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"\bwriteFact\b|\bfact_write\s*\(", "fact_write"),
    (r"\bexecute_detection\b|\bexecute_ocr\b", "other_runner_execute"),
    (r"run_model\s*\(", "ui_direct_model_call"),
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_BLOCKED"

EXTRA_RECORDS: Tuple[str, ...] = (
    "mobile_sam_controlled_execution_integration_patch_record",
    "runner_execution_record_schema_record",
    "runner_error_candidate_schema_record",
    "result_envelope_record_schema_record",
    "mobile_sam_controlled_execution_negative_guard_audit_record",
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
            "runner_sandbox_client_v1.js",
            "result_layer_panel_v1.js",
            "controlled_runner_execution_ui_v1.js",
            "controlled_runner_execution_panel_v1.js",
            "app.js",
        )
    )


def _audit() -> Dict[str, bool]:
    executor = _read(f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_executor_v1.py")
    sandbox = _read(f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_v1.py")
    bridge = _read(f"{_BRIDGE}/local_runner_bridge_controlled_execution_v1.py")
    handlers = _read(f"{_BRIDGE}/local_runner_bridge_api_handlers_v1.py")
    app = _read(f"{STATIC_REL}/app.js")
    client = _read(f"{STATIC_REL}/runner_sandbox_client_v1.js")
    result_panel = _read(f"{STATIC_REL}/result_layer_panel_v1.js")
    exec_ui = _read(f"{STATIC_REL}/controlled_runner_execution_ui_v1.js")
    rex_schema = _load_json(f"{SCHEMA_REL}/runner_execution_record_schema_v1.json")
    err_schema = _load_json(f"{SCHEMA_REL}/runner_error_candidate_schema_v1.json")
    res_schema = _load_json(f"{SCHEMA_REL}/result_envelope_record_schema_v1.json")
    sb_pol = _load_json(f"{SCHEMA_REL}/runner_sandbox_policy_v1.json")
    hud = _read(f"{STATIC_REL}/perception_hud_renderer_v1.js")

    planning = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_planning_review_v1.json"
    )
    smoke = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "mobile_sam_controlled_execution_integration_smoke_v1.json"
    )

    return {
        "upstream_planning_go": planning.get("final_decision") == PLANNING_GO,
        "integration_modules_written": all(_read(f) for f in NEW_MODULES[:-1]),
        "runner_sandbox_executor_defined": "execute_controlled_mobilesam" in executor,
        "controlled_execution_api_wired": "/api/v1/controlled-execution/run" in handlers,
        "runner_sandbox_client_defined": "runControlledMobileSam" in client,
        "result_layer_panel_defined": "result_layer_not_observation_layer" in result_panel,
        "mobile_sam_candidate_builder_defined": "buildMobileSamFromAdmittedRequest" in exec_ui,
        "runner_execution_record_schema_defined": rex_schema.get("schema_id") == "RunnerExecutionRecordSchemaV1",
        "runner_error_candidate_schema_defined": err_schema.get("schema_id") == "RunnerErrorCandidateSchemaV1",
        "result_envelope_record_schema_defined": res_schema.get("schema_id") == "ResultEnvelopeRecordSchemaV1",
        "smoke_all_passed": smoke.get("all_passed") is True,
        "runner_execution_allowed_mobile_sam_only": sb_pol.get("allowed_models") == ["mobile_sam"],
        "runner_execution_requires_execution_candidate": (
            sb_pol.get("entry_requirements", {}).get("controlled_runner_execution_candidate_required") is True
        ),
        "runner_execution_requires_sandbox": "prepare_execution" in sandbox and "execute_controlled_mobilesam" in executor,
        "runner_execution_requires_admission_trace": "validate_trace_chain" in sandbox,
        "runner_output_requires_result_envelope": "build_segmentation_result_envelope" in executor,
        "runner_output_not_fact": res_schema.get("boundary_flags", {}).get("runner_output_not_fact") is True,
        "runner_error_not_fact": err_schema.get("boundary_flags", {}).get("runner_error_not_fact") is True,
        "result_layer_not_observation_layer": (
            "result_layer_not_observation_layer" in result_panel
        ),
        "result_layer_not_segmentation_owner": (
            "resultLayerNotSegmentationOwner" in result_panel
        ),
        "no_direct_fact_write_from_runner": (
            "noDirectFactWriteFromRunner" in result_panel and "no_direct_fact_write_from_runner" in res_schema.get("boundary_flags", {})
        ),
        "no_ui_direct_model_call": "noUiDirectModelCall" in client and "run_model" not in client,
        "completed_not_fact": "completed_not_fact" in executor,
        "cancelled_execution_candidate_no_runner_execution": "execution_candidate_cancelled" in sandbox,
        "trace_chain_validation_strict": "trace_missing_attention_record_id" in sandbox,
        "human_correction_must_not_modify_model_result": "human_correction_modify_model_result" in _read(
            f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_types_v1.py"
        ),
        "no_visual_expression_mutation": "execution_box" not in hud.lower(),
        "app_wires_controlled_execution": "onRunControlledMobileSam" in app,
        "index_scripts_wired": "runner_sandbox_client_v1.js" in _read(f"{STATIC_REL}/index.html"),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in NEW_MODULES + UPDATED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    violations = [pid for pat, pid in FORBIDDEN if re.search(pat, _bundle(), re.I)]
    flags = _audit()

    guards = [
        {"guard_id": "A", "key": "runner_execution_requires_execution_candidate", "passed": flags["runner_execution_requires_execution_candidate"]},
        {"guard_id": "B", "key": "runner_execution_requires_sandbox", "passed": flags["runner_execution_requires_sandbox"]},
        {"guard_id": "C", "key": "runner_execution_requires_admission_trace", "passed": flags["runner_execution_requires_admission_trace"]},
        {"guard_id": "D", "key": "runner_output_requires_result_envelope", "passed": flags["runner_output_requires_result_envelope"]},
        {"guard_id": "E", "key": "runner_output_not_fact", "passed": flags["runner_output_not_fact"]},
        {"guard_id": "F", "key": "runner_error_not_fact", "passed": flags["runner_error_not_fact"]},
        {"guard_id": "G", "key": "result_layer_not_observation_layer", "passed": flags["result_layer_not_observation_layer"]},
        {"guard_id": "H", "key": "result_layer_not_segmentation_owner", "passed": flags["result_layer_not_segmentation_owner"]},
        {"guard_id": "I", "key": "no_direct_fact_write_from_runner", "passed": flags["no_direct_fact_write_from_runner"]},
        {"guard_id": "J", "key": "no_ui_direct_model_call", "passed": flags["no_ui_direct_model_call"]},
        {"guard_id": "K", "key": "completed_not_fact", "passed": flags["completed_not_fact"]},
        {"guard_id": "L", "key": "cancelled_execution_candidate_no_runner_execution", "passed": flags["cancelled_execution_candidate_no_runner_execution"]},
        {"guard_id": "M", "key": "trace_chain_validation_strict", "passed": flags["trace_chain_validation_strict"]},
        {"guard_id": "N", "key": "runner_execution_allowed_mobile_sam_only", "passed": flags["runner_execution_allowed_mobile_sam_only"]},
        {"guard_id": "O", "key": "upstream_planning_go", "passed": flags["upstream_planning_go"]},
        {"guard_id": "P", "key": "smoke_all_passed", "passed": flags["smoke_all_passed"]},
    ]
    ng_passed = sum(1 for g in guards if g["passed"])

    core = [
        "integration_modules_written",
        "runner_sandbox_executor_defined",
        "controlled_execution_api_wired",
        "result_layer_panel_defined",
        "smoke_all_passed",
        "app_wires_controlled_execution",
        "upstream_planning_go",
    ]

    blockers = len(failed) + len(violations) + sum(1 for k in core if not flags.get(k)) + (len(guards) - ng_passed)
    decision = FINAL_GO if blockers == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "real_execution_integration": True,
        "runner_execution_allowed": True,
        "mobile_sam_only": True,
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
        rp = out / "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
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
    # Run smoke first
    from capabilities.midplatform.model_test_lens.run_mobile_sam_controlled_execution_integration_smoke_v1 import (
        run_smoke,
    )
    run_smoke()
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "failed_checks": r.get("failed_checks"),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
