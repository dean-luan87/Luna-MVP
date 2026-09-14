# -*- coding: utf-8 -*-
"""P1 MobileSAM Single Model Execution Integration — planning review v1."""

from __future__ import annotations

import json
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
    "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-001"
)
INTEGRATION_REL = (
    "capabilities/midplatform/model_test_lens/mobile_sam_single_model_execution_integration"
)
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/mobile_sam_single_model_execution"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

CONTROLLED_EXEC_UI_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_DETECTION_OCR_CONTROLLED_RUNNER_EXECUTION_UI_EXECUTION_GO"
)
LOCAL_BRIDGE_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_plan_v1.md",
    f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_types_v1.py",
    f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_v1.py",
    f"{SCHEMA_REL}/model_adapter_input_schema_v1.json",
    f"{SCHEMA_REL}/runner_sandbox_policy_v1.json",
    f"{SCHEMA_REL}/segmentation_result_envelope_schema_v1.json",
    f"{SCHEMA_REL}/mobile_sam_controlled_execution_input_policy_v1.json",
    f"{GOV_REL}/mobile_sam_single_model_execution_integration_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_mobile_sam_single_model_execution_integration_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "model_adapter_input_schema_record",
    "runner_sandbox_policy_record",
    "segmentation_result_envelope_schema_record",
    "mobile_sam_controlled_execution_input_policy_record",
    "mobile_sam_single_model_execution_integration_plan_record",
)

NEXT_PHASE = "Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "runner_execution_allowed_mobile_sam_only", "desc": "仅 MobileSAM 可执行"},
    {"guard_id": "B", "key": "test_environment_only", "desc": "仅测试环境"},
    {"guard_id": "C", "key": "execution_candidate_required", "desc": "须 execution candidate"},
    {"guard_id": "D", "key": "no_ui_direct_model_call", "desc": "UI 不直调模型"},
    {"guard_id": "E", "key": "no_bypass_admission", "desc": "不 bypass admission"},
    {"guard_id": "F", "key": "no_bypass_execution_candidate", "desc": "不 bypass execution candidate"},
    {"guard_id": "G", "key": "adapter_input_normalized", "desc": "Adapter 输入标准化"},
    {"guard_id": "H", "key": "no_internal_object_pass_through", "desc": "不传内部对象"},
    {"guard_id": "I", "key": "trace_chain_required", "desc": "须 trace_chain"},
    {"guard_id": "J", "key": "runner_output_requires_envelope", "desc": "输出须 envelope"},
    {"guard_id": "K", "key": "runner_output_not_fact", "desc": "输出非 fact"},
    {"guard_id": "L", "key": "fact_admission_required_before_fact_write", "desc": "fact 须 admission"},
    {"guard_id": "M", "key": "cancelled_execution_candidate_no_runner_execution", "desc": "cancelled 不执行"},
    {"guard_id": "N", "key": "blocked_execution_candidate_no_runner_execution", "desc": "blocked 不执行"},
    {"guard_id": "O", "key": "runner_error_does_not_write_fact", "desc": "错误不写 fact"},
    {"guard_id": "P", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "Q", "key": "human_correction_must_not_modify_model_result", "desc": "纠错不改模型结果"},
    {"guard_id": "R", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "S", "key": "no_visual_expression_mutation", "desc": "不改 Visual Expression"},
    {"guard_id": "T", "key": "no_execution_box_on_canvas", "desc": "主图无 execution box"},
    {"guard_id": "U", "key": "no_auto_fact_admission", "desc": "不自动 fact admission"},
    {"guard_id": "V", "key": "upstream_controlled_execution_ui_go", "desc": "上游 controlled execution GO"},
    {"guard_id": "W", "key": "runner_sandbox_defined", "desc": "Runner Sandbox 已定义"},
    {"guard_id": "X", "key": "model_adapter_input_schema_defined", "desc": "Adapter schema 已定义"},
    {"guard_id": "Y", "key": "segmentation_result_envelope_defined", "desc": "输出 envelope 已定义"},
    {"guard_id": "Z", "key": "error_isolation_defined", "desc": "错误隔离已定义"},
    {"guard_id": "AA", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "AB", "key": "integration_plan_defined", "desc": "集成计划已定义"},
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
    plan = _read(f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_plan_v1.md")
    types_py = _read(f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_types_v1.py")
    sandbox = _read(f"{INTEGRATION_REL}/runner_sandbox/runner_sandbox_v1.py")
    adapter = _load_json(f"{SCHEMA_REL}/model_adapter_input_schema_v1.json")
    sb_pol = _load_json(f"{SCHEMA_REL}/runner_sandbox_policy_v1.json")
    seg_env = _load_json(f"{SCHEMA_REL}/segmentation_result_envelope_schema_v1.json")
    mob_in = _load_json(f"{SCHEMA_REL}/mobile_sam_controlled_execution_input_policy_v1.json")
    gov = _read(f"{GOV_REL}/mobile_sam_single_model_execution_integration_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    controlled_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_ui_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_detection_ocr_controlled_runner_execution_ui_execution_review_v1.json"
    )
    bridge = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_review_v1.json"
    )

    return {
        "integration_plan_defined": "Runner Sandbox" in plan and "MobileSAM" in plan,
        "governance_standard_defined": "MobileSamSingleModelExecutionIntegrationGovernanceStandardV1" in gov,
        "runner_sandbox_defined": "prepare_execution" in sandbox and "validate_execution_candidate" in sandbox,
        "model_adapter_input_schema_defined": adapter.get("schema_id") == "ModelAdapterInputSchemaV1",
        "segmentation_result_envelope_defined": seg_env.get("schema_id") == "SegmentationResultEnvelopeSchemaV1",
        "runner_sandbox_policy_defined": sb_pol.get("schema_id") == "RunnerSandboxPolicyV1",
        "mobile_sam_input_policy_defined": mob_in.get("schema_id") == "MobileSamControlledExecutionInputPolicyV1",
        "upstream_controlled_execution_ui_go": controlled_ui.get("final_decision") == CONTROLLED_EXEC_UI_GO,
        "upstream_local_runner_bridge_go": bridge.get("final_decision") == LOCAL_BRIDGE_GO,
        "runner_execution_allowed_mobile_sam_only": (
            sb_pol.get("runner_execution_allowed") is True
            and sb_pol.get("allowed_models") == ["mobile_sam"]
            and "RUNNER_EXECUTION_MODEL_ALLOWLIST" in types_py
        ),
        "test_environment_only": (
            "test_environment" in json.dumps(sb_pol.get("allowed_environments", []))
            and "RUNNER_EXECUTION_ENVIRONMENT_ALLOWLIST" in types_py
        ),
        "execution_candidate_required": (
            sb_pol.get("entry_requirements", {}).get("controlled_runner_execution_candidate_required") is True
            and "execution_candidate_required" in types_py
        ),
        "no_ui_direct_model_call": (
            "ui_direct_model_call" in json.dumps(sb_pol.get("forbidden_entry_paths", []))
            and "ui_direct_model_call" in types_py
        ),
        "no_bypass_admission": "bypass_admission" in json.dumps(sb_pol.get("forbidden_entry_paths", [])),
        "no_bypass_execution_candidate": (
            "bypass_execution_candidate" in json.dumps(sb_pol.get("forbidden_entry_paths", []))
        ),
        "adapter_input_normalized": (
            adapter.get("boundary_flags", {}).get("adapter_input_normalized") is True
            and "build_adapter_input" in sandbox
        ),
        "no_internal_object_pass_through": (
            "internal_store_object" in json.dumps(adapter.get("forbidden_inputs", []))
            and "internal_store_object" in json.dumps(mob_in.get("forbidden_inputs", []))
        ),
        "trace_chain_required": (
            adapter.get("boundary_flags", {}).get("trace_chain_required") is True
            and "trace_chain" in adapter.get("required_fields", [])
        ),
        "runner_output_requires_envelope": (
            seg_env.get("boundary_flags", {}).get("runner_output_requires_envelope") is True
            and "build_segmentation_result_envelope" in sandbox
        ),
        "runner_output_not_fact": (
            seg_env.get("boundary_flags", {}).get("runner_output_not_fact") is True
            and seg_env.get("field_definitions", {}).get("not_fact", {}).get("const") is True
        ),
        "fact_admission_required_before_fact_write": (
            seg_env.get("boundary_flags", {}).get("fact_admission_required_before_fact_write") is True
            and seg_env.get("field_definitions", {}).get("needs_fact_admission", {}).get("const") is True
        ),
        "cancelled_execution_candidate_no_runner_execution": (
            "cancelled" in json.dumps(sb_pol.get("entry_requirements", {}).get("execution_candidate_status_forbidden", []))
            and "execution_cancelled" in sandbox
        ),
        "blocked_execution_candidate_no_runner_execution": (
            "blocked" in json.dumps(sb_pol.get("entry_requirements", {}).get("execution_candidate_status_forbidden", []))
        ),
        "runner_error_does_not_write_fact": (
            sb_pol.get("error_handling", {}).get("no_fact_write_on_error") is True
            and "runner_error_does_not_write_fact" in sandbox
        ),
        "no_human_correction_ground_truth": (
            "human_correction_as_ground_truth" in json.dumps(adapter.get("forbidden_inputs", []))
            or "no_human_correction_ground_truth" in types_py
        ),
        "human_correction_must_not_modify_model_result": (
            "human_correction_modify_model_result" in types_py
            and "修改模型结果" in plan
        ),
        "no_prompt_label_fact_upgrade": (
            "no_prompt_label_fact_upgrade" in types_py
            or "prompt_label_as_truth" in json.dumps(mob_in)
        ),
        "no_visual_expression_mutation": (
            seg_env.get("downstream", {}).get("must_not_override_segmentation_boundary") is True
            and "visual_expression_system_frozen" in types_py
        ),
        "no_execution_box_on_canvas": (
            seg_env.get("boundary_flags", {}).get("no_execution_box_on_canvas") is True
            and "no_execution_box_on_canvas" in plan
        ),
        "no_auto_fact_admission": (
            "no_auto_fact_admission" in types_py and "暂不自动" in plan
        ),
        "error_isolation_defined": len(sb_pol.get("error_handling", {}).get("error_types", [])) >= 8,
        "browser_runtime_guard_inherited": (
            "browser_runtime_guard_inherited" in types_py and "BrowserRuntimeGuard" in browser
        ),
        "recommended_next_phase_defined": NEXT_PHASE in plan,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "integration_planning": True,
        "runner_execution_allowed": True,
        "mobile_sam_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "pipeline_stages": [
            "controlled_runner_execution_candidate",
            "runner_sandbox",
            "model_adapter",
            "mobile_sam_inference",
            "segmentation_result_envelope",
            "result_candidate",
            "fact_admission",
        ],
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / (
            "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_planning_review_v1.json"
        )
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "test_mode": "planning", "integration_planning": True,
        }
        payloads = {
            "model_adapter_input_schema_record": _load_json(f"{SCHEMA_REL}/model_adapter_input_schema_v1.json"),
            "runner_sandbox_policy_record": _load_json(f"{SCHEMA_REL}/runner_sandbox_policy_v1.json"),
            "segmentation_result_envelope_schema_record": _load_json(
                f"{SCHEMA_REL}/segmentation_result_envelope_schema_v1.json"
            ),
            "mobile_sam_controlled_execution_input_policy_record": _load_json(
                f"{SCHEMA_REL}/mobile_sam_controlled_execution_input_policy_v1.json"
            ),
            "mobile_sam_single_model_execution_integration_plan_record": {
                "plan_ref": f"{INTEGRATION_REL}/mobile_sam_single_model_execution_integration_plan_v1.md"
            },
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(
        json.dumps(
            {
                "final_decision": r["final_decision"],
                "blocker_count": r["blocker_count"],
                "negative_guard_passed": r["negative_guard_passed"],
                "negative_guard_count": r["negative_guard_count"],
                "recommended_next_phase": r["recommended_next_phase"],
                "failed_checks": r.get("failed_checks", []),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
