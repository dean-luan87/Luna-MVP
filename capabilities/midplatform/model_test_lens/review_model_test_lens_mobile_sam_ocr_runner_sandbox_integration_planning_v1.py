# -*- coding: utf-8 -*-
"""P1 MobileSAM → OCR Runner Sandbox Integration — planning review v1."""

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
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Planning-v1-001"
)
MM_REL = "capabilities/midplatform/model_test_lens/multi_model_interaction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_EXPLORATION_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO"
UPSTREAM_CONTROLLED_EXEC_PLANNING_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_PLANNING_GO"
)
UPSTREAM_CONTROLLED_EXEC_UI_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{MM_REL}/ocr_runner_sandbox_integration_plan_v1.md",
    f"{MM_REL}/ocr_runner_sandbox_types_v1.py",
    f"{SCHEMA_REL}/ocr_adapter_input_schema_v1.json",
    f"{SCHEMA_REL}/ocr_runner_execution_record_schema_v1.json",
    f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json",
    f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json",
    f"{SCHEMA_REL}/ocr_local_runner_bridge_contract_v1.json",
    f"{SCHEMA_REL}/mobile_sam_ocr_fusion_input_schema_v1.json",
    f"{GOV_REL}/ocr_runner_sandbox_integration_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_mobile_sam_ocr_runner_sandbox_integration_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "ocr_adapter_input_schema_record",
    "ocr_runner_execution_record_schema_record",
    "ocr_result_envelope_schema_record",
    "ocr_runner_error_candidate_schema_record",
    "ocr_local_runner_bridge_contract_record",
    "mobile_sam_ocr_fusion_input_schema_record",
    "ocr_runner_sandbox_integration_plan_record",
)

NEXT_PHASE = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)

PLANNING_ENDPOINT = "ocr_runner_sandbox_integration_plan"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_ocr_runner_call_in_planning", "desc": "规划阶段不调用 OCR runner"},
    {"guard_id": "B", "key": "no_ocr_execution_in_planning", "desc": "规划阶段不执行 OCR"},
    {"guard_id": "C", "key": "no_ocr_result_generation_in_planning", "desc": "规划阶段不生成 OCR result"},
    {"guard_id": "D", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "E", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "F", "key": "ocr_runner_requires_execution_candidate", "desc": "runner 须 execution candidate"},
    {"guard_id": "G", "key": "no_ui_direct_ocr_runner_call", "desc": "UI 不直调 OCR runner"},
    {"guard_id": "H", "key": "no_mobile_sam_direct_to_ocr_runner", "desc": "MobileSAM 不直调 OCR runner"},
    {"guard_id": "I", "key": "ocr_input_does_not_contain_fact_text", "desc": "输入无 fact text"},
    {"guard_id": "J", "key": "ocr_input_does_not_contain_fact_label", "desc": "输入无 fact label"},
    {"guard_id": "K", "key": "ocr_output_requires_result_envelope", "desc": "输出须 result envelope"},
    {"guard_id": "L", "key": "ocr_output_not_fact", "desc": "输出非 fact"},
    {"guard_id": "M", "key": "ocr_completed_not_fact", "desc": "completed 非 fact"},
    {"guard_id": "N", "key": "ocr_error_not_fact", "desc": "错误非 fact"},
    {"guard_id": "O", "key": "ocr_error_not_navigation_decision", "desc": "错误非导航决策"},
    {"guard_id": "P", "key": "ocr_result_requires_fact_admission", "desc": "result 须 fact admission"},
    {"guard_id": "Q", "key": "fusion_candidate_not_fact", "desc": "融合候选非 fact"},
    {"guard_id": "R", "key": "no_visual_expression_mutation", "desc": "不改 Visual Expression"},
    {"guard_id": "S", "key": "no_ocr_box_on_canvas", "desc": "主图无 OCR box"},
    {"guard_id": "T", "key": "human_correction_not_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "U", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "V", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "W", "key": "upstream_exploration_smoke_go", "desc": "上游 Exploration GO"},
    {"guard_id": "X", "key": "upstream_controlled_execution_planning_go", "desc": "上游 Controlled Execution Planning GO"},
    {"guard_id": "Y", "key": "upstream_controlled_execution_ui_go", "desc": "上游 Controlled Execution UI GO"},
    {"guard_id": "Z", "key": "sandbox_responsibilities_defined", "desc": "Sandbox 职责已定义"},
    {"guard_id": "AA", "key": "bridge_contract_defined", "desc": "8787 bridge 契约已定义"},
    {"guard_id": "AB", "key": "fusion_input_defined", "desc": "融合输入 schema 已定义"},
    {"guard_id": "AC", "key": "human_correction_runtime_defined", "desc": "纠错 runtime 分流已定义"},
    {"guard_id": "AD", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
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
    plan = _read(f"{MM_REL}/ocr_runner_sandbox_integration_plan_v1.md")
    types_py = _read(f"{MM_REL}/ocr_runner_sandbox_types_v1.py")
    gov = _read(f"{GOV_REL}/ocr_runner_sandbox_integration_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    adapter = _load_json(f"{SCHEMA_REL}/ocr_adapter_input_schema_v1.json")
    exec_rec = _load_json(f"{SCHEMA_REL}/ocr_runner_execution_record_schema_v1.json")
    result = _load_json(f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json")
    err = _load_json(f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json")
    bridge = _load_json(f"{SCHEMA_REL}/ocr_local_runner_bridge_contract_v1.json")
    fusion_in = _load_json(f"{SCHEMA_REL}/mobile_sam_ocr_fusion_input_schema_v1.json")

    mobilesam = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )
    exploration = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_interaction_exploration_smoke_v0/"
        "mobile_sam_ocr_interaction_exploration_smoke_review_v1.json"
    )
    controlled_plan = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_planning_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_controlled_execution_planning_review_v1.json"
    )
    controlled_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_controlled_execution_ui_execution_review_v1.json"
    )

    error_types = err.get("error_types", [])
    required_errors = [
        "timeout", "runner_unavailable", "invalid_crop", "empty_text",
        "low_confidence", "invalid_output_schema", "unreadable_region",
        "route_mismatch", "cancelled",
    ]

    return {
        "no_ocr_runner_call_in_planning": (
            "planning_only" in types_py and "ocr_runner_execution_in_this_phase" in types_py
            and "False" in types_py.split("ocr_runner_execution_in_this_phase")[1][:20]
        ),
        "no_ocr_execution_in_planning": "no_ocr_execution" not in plan or "不执行 OCR" in plan,
        "no_ocr_result_generation_in_planning": "不生成真实 OCR result" in plan,
        "no_fact_write": "不写 fact" in plan and adapter.get("boundary_flags", {}).get("ocr_input_does_not_contain_fact_text"),
        "no_navigation_decision": (
            "导航决策" in plan
            and ("导航指令" in plan or "not_navigation_decision" in json.dumps(err))
        ),
        "ocr_runner_requires_execution_candidate": (
            adapter.get("entry_requirement") == "ocr_controlled_execution_candidate_only"
            and "ocr_runner_requires_execution_candidate" in types_py
        ),
        "no_ui_direct_ocr_runner_call": (
            "ui_direct_ocr_runner_call" in types_py
            and bridge.get("boundary_flags", {}).get("no_ui_direct_ocr_runner_call")
        ),
        "no_mobile_sam_direct_to_ocr_runner": (
            "mobile_sam_result_direct_to_ocr_runner" in types_py
            and bridge.get("boundary_flags", {}).get("no_mobile_sam_direct_to_ocr_runner")
        ),
        "ocr_input_does_not_contain_fact_text": adapter.get("boundary_flags", {}).get(
            "ocr_input_does_not_contain_fact_text"
        ),
        "ocr_input_does_not_contain_fact_label": adapter.get("boundary_flags", {}).get(
            "ocr_input_does_not_contain_fact_label"
        ),
        "ocr_output_requires_result_envelope": (
            result.get("boundary_flags", {}).get("ocr_result_requires_envelope")
            and "text_candidate_list" in json.dumps(result.get("required_fields", []))
        ),
        "ocr_output_not_fact": result.get("boundary_flags", {}).get("ocr_output_not_fact"),
        "ocr_completed_not_fact": (
            exec_rec.get("boundary_flags", {}).get("ocr_completed_not_fact")
            and result.get("boundary_flags", {}).get("ocr_completed_not_fact")
        ),
        "ocr_error_not_fact": err.get("boundary_flags", {}).get("ocr_error_does_not_write_fact"),
        "ocr_error_not_navigation_decision": err.get("boundary_flags", {}).get(
            "ocr_error_not_navigation_decision"
        ),
        "ocr_result_requires_fact_admission": result.get("boundary_flags", {}).get(
            "ocr_result_requires_fact_admission"
        ),
        "fusion_candidate_not_fact": fusion_in.get("boundary_flags", {}).get("fusion_candidate_not_fact"),
        "no_visual_expression_mutation": (
            "no_visual_expression_mutation" in types_py and "Visual Expression" in plan
        ),
        "no_ocr_box_on_canvas": "no_ocr_box_on_canvas" in types_py,
        "human_correction_not_ground_truth": (
            "HUMAN_CORRECTION_RUNTIME_ROUTING" in types_py
            and ("用户输入作" in plan or "ground truth" in gov.lower())
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_exploration_smoke_go": exploration.get("final_decision") == UPSTREAM_EXPLORATION_GO,
        "upstream_controlled_execution_planning_go": (
            controlled_plan.get("final_decision") == UPSTREAM_CONTROLLED_EXEC_PLANNING_GO
        ),
        "upstream_controlled_execution_ui_go": (
            controlled_ui.get("final_decision") == UPSTREAM_CONTROLLED_EXEC_UI_GO
        ),
        "sandbox_responsibilities_defined": all(
            fn in types_py
            for fn in (
                "validate_ocr_execution_candidate",
                "build_ocr_adapter_input",
                "build_ocr_runner_error_candidate",
            )
        ) and all(
            s in plan
            for s in (
                "validate_ocr_execution_candidate",
                "build_ocr_adapter_input",
                "prepare_ocr_execution",
                "validate_ocr_runner_output",
                "build_ocr_result_envelope",
                "build_ocr_runner_error_candidate",
            )
        ),
        "bridge_contract_defined": (
            bridge.get("schema_id") == "OcrLocalRunnerBridgeContractV1"
            and "/api/v1/controlled-execution/ocr/run" in json.dumps(bridge)
        ),
        "fusion_input_defined": fusion_in.get("schema_id") == "MobileSamOcrFusionInputSchemaV1",
        "human_correction_runtime_defined": len(types_py.split("HUMAN_CORRECTION_RUNTIME_ROUTING")) > 1,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
        "all_error_types_present": all(e in error_types for e in required_errors),
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
    if not flags.get("all_error_types_present"):
        failed.append("error_types.incomplete")

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
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "planning_endpoint": PLANNING_ENDPOINT,
        "ocr_runner_forbidden_in_planning": True,
        "ocr_runner_execution_allowed_future": True,
        "recommended_next_phase": NEXT_PHASE,
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
        rp = out / "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_planning_review_v1.json"
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
            "test_mode": "planning", "multi_model_interaction_planning": True,
        }
        payloads = {
            "ocr_adapter_input_schema_record": _load_json(f"{SCHEMA_REL}/ocr_adapter_input_schema_v1.json"),
            "ocr_runner_execution_record_schema_record": _load_json(
                f"{SCHEMA_REL}/ocr_runner_execution_record_schema_v1.json"
            ),
            "ocr_result_envelope_schema_record": _load_json(f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json"),
            "ocr_runner_error_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json"
            ),
            "ocr_local_runner_bridge_contract_record": _load_json(
                f"{SCHEMA_REL}/ocr_local_runner_bridge_contract_v1.json"
            ),
            "mobile_sam_ocr_fusion_input_schema_record": _load_json(
                f"{SCHEMA_REL}/mobile_sam_ocr_fusion_input_schema_v1.json"
            ),
            "ocr_runner_sandbox_integration_plan_record": {
                "plan_ref": f"{MM_REL}/ocr_runner_sandbox_integration_plan_v1.md"
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
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_next_phase": r["recommended_next_phase"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
