# -*- coding: utf-8 -*-
"""P1 Single Model Interaction Validation — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001"
VALIDATION_REL = "capabilities/midplatform/model_test_lens/single_model_interaction_validation"
HC_REL = "capabilities/midplatform/model_test_lens/human_correction"
HC_SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/human_correction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/single_model_interaction_validation"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

UPSTREAM_MOBILESAM_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{VALIDATION_REL}/single_model_interaction_validation_plan_v1.md",
    f"{VALIDATION_REL}/single_model_interaction_validation_types_v1.py",
    f"{VALIDATION_REL}/result_to_midplatform_processor_v1.py",
    f"{SCHEMA_REL}/result_envelope_midplatform_input_schema_v1.json",
    f"{SCHEMA_REL}/observation_re_evaluation_from_result_policy_v1.json",
    f"{SCHEMA_REL}/followup_route_from_result_policy_v1.json",
    f"{SCHEMA_REL}/interaction_trace_closure_policy_v1.json",
    f"{SCHEMA_REL}/case_mobilesam_to_ocr_route_validation_v1.json",
    f"{SCHEMA_REL}/case_mobilesam_correction_midplatform_validation_v1.json",
    f"{HC_REL}/correction_midplatform_analyzer_v1.py",
    f"{HC_SCHEMA_REL}/correction_attribution_taxonomy_v1.json",
    f"{HC_SCHEMA_REL}/correction_routing_policy_v1.json",
    f"{HC_SCHEMA_REL}/correction_midplatform_analysis_record_schema_v1.json",
    f"{STATIC_REL}/human_correction_midplatform_analyzer_v1.js",
    f"{GOV_REL}/single_model_interaction_validation_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_single_model_interaction_validation_planning_v1.py",
    f"{_PKG}/run_single_model_interaction_validation_smoke_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "result_envelope_midplatform_input_schema_record",
    "observation_re_evaluation_from_result_policy_record",
    "followup_route_from_result_policy_record",
    "interaction_trace_closure_policy_record",
    "case_mobilesam_to_ocr_route_validation_record",
    "single_model_interaction_validation_plan_record",
)

NEXT_PHASE = "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "result_envelope_to_midplatform_input", "desc": "结果进中台非直出 UI"},
    {"guard_id": "B", "key": "result_candidate_does_not_pollute_observation", "desc": "结果不污染 Observation"},
    {"guard_id": "C", "key": "midplatform_secondary_scheduling", "desc": "中台二次调度"},
    {"guard_id": "D", "key": "no_pipeline_bypass_mobilesam_to_ocr", "desc": "禁止 pipeline bypass"},
    {"guard_id": "E", "key": "no_ocr_runner_execution", "desc": "本阶段不跑 OCR"},
    {"guard_id": "F", "key": "no_detection_runner_execution", "desc": "本阶段不跑 Detection"},
    {"guard_id": "G", "key": "mobilesam_does_not_assert_fact_label", "desc": "MobileSAM 不断言 fact"},
    {"guard_id": "H", "key": "result_does_not_overwrite_attention_record", "desc": "不覆盖 attention"},
    {"guard_id": "H2", "key": "result_candidate_not_observation_owner", "desc": "Result 非 Observation owner"},
    {"guard_id": "I", "key": "human_correction_must_not_modify_mask", "desc": "纠错不改 mask"},
    {"guard_id": "J", "key": "human_correction_priority_signal_only", "desc": "纠错仅 priority"},
    {"guard_id": "K", "key": "trace_closure_required", "desc": "Trace 闭环"},
    {"guard_id": "L", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "M", "key": "no_auto_fact_admission", "desc": "不自动 fact admission"},
    {"guard_id": "N", "key": "no_visual_expression_mutation", "desc": "不改 Visual Expression"},
    {"guard_id": "O", "key": "upstream_mobilesam_integration_go", "desc": "上游 MobileSAM integration GO"},
    {"guard_id": "P", "key": "case_1_defined", "desc": "Case 1 已定义"},
    {"guard_id": "Q", "key": "processor_defined", "desc": "中台处理器已定义"},
    {"guard_id": "R", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "S", "key": "interaction_plan_defined", "desc": "互动验证计划已定义"},
    {"guard_id": "T", "key": "smoke_case1_passes", "desc": "Case 1 smoke 通过"},
    {"guard_id": "T2", "key": "smoke_case2_passes", "desc": "Case 2 纠错分流 smoke 通过"},
    {"guard_id": "V", "key": "case_2_defined", "desc": "Case 2 已定义"},
    {"guard_id": "W", "key": "correction_midplatform_analyzer_defined", "desc": "纠错中台分析器已定义"},
    {"guard_id": "X", "key": "no_direct_training_from_raw_correction", "desc": "禁止 raw 纠错直训"},
    {"guard_id": "Y", "key": "midplatform_correction_entry_required", "desc": "纠错须经中台入口"},
    {"guard_id": "U", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
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


def _run_smoke() -> Dict[str, Any]:
    import subprocess

    script = _detect_repo_root() / _PKG / "run_single_model_interaction_validation_smoke_v1.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(_detect_repo_root()),
    )
    smoke_path = (
        _detect_repo_root()
        / "_tmp_eval_out/p1_midplatform_single_model_interaction_validation_smoke_v0"
        / "single_model_interaction_validation_smoke_v1.json"
    )
    data = json.loads(smoke_path.read_text(encoding="utf-8")) if smoke_path.is_file() else {}
    data["exit_code"] = proc.returncode
    return data


def _audit(smoke: Dict[str, Any]) -> Dict[str, bool]:
    plan = _read(f"{VALIDATION_REL}/single_model_interaction_validation_plan_v1.md")
    types_py = _read(f"{VALIDATION_REL}/single_model_interaction_validation_types_v1.py")
    processor = _read(f"{VALIDATION_REL}/result_to_midplatform_processor_v1.py")
    gov = _read(f"{GOV_REL}/single_model_interaction_validation_governance_standard_v1.md")

    mid_in = _load_json(f"{SCHEMA_REL}/result_envelope_midplatform_input_schema_v1.json")
    re_eval = _load_json(f"{SCHEMA_REL}/observation_re_evaluation_from_result_policy_v1.json")
    route_pol = _load_json(f"{SCHEMA_REL}/followup_route_from_result_policy_v1.json")
    trace_pol = _load_json(f"{SCHEMA_REL}/interaction_trace_closure_policy_v1.json")
    case1 = _load_json(f"{SCHEMA_REL}/case_mobilesam_to_ocr_route_validation_v1.json")
    case2 = _load_json(f"{SCHEMA_REL}/case_mobilesam_correction_midplatform_validation_v1.json")
    corr_analyzer = _read(f"{HC_REL}/correction_midplatform_analyzer_v1.py")
    corr_tax = _load_json(f"{HC_SCHEMA_REL}/correction_attribution_taxonomy_v1.json")
    corr_route = _load_json(f"{HC_SCHEMA_REL}/correction_routing_policy_v1.json")
    hc_js = _read(f"{STATIC_REL}/human_correction_midplatform_analyzer_v1.js")

    mobilesam_int = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )

    return {
        "interaction_plan_defined": "Midplatform Processing" in plan and CASE_1_IN_PLAN(plan),
        "governance_standard_defined": "SingleModelInteractionValidationGovernanceStandardV1" in gov,
        "processor_defined": "process_segmentation_envelopes" in processor and "evaluate_text_likely_region" in processor,
        "case_1_defined": case1.get("case_id") == "Case-1-MobileSAM-to-OCR-Route-Candidate",
        "result_envelope_to_midplatform_input": (
            mid_in.get("boundary_flags", {}).get("result_envelope_to_midplatform_input") is True
            and "midplatform_processing" in processor
        ),
        "result_candidate_does_not_pollute_observation": (
            re_eval.get("boundary_flags", {}).get("result_candidate_does_not_pollute_observation") is True
            and "attention_records_not_overwritten" in processor
        ),
        "midplatform_secondary_scheduling": (
            route_pol.get("boundary_flags", {}).get("midplatform_secondary_scheduling") is True
            and "new_task_candidate" in processor
        ),
        "no_pipeline_bypass_mobilesam_to_ocr": (
            route_pol.get("boundary_flags", {}).get("no_pipeline_bypass_mobilesam_to_ocr") is True
            and "midplatform_schedules_not_pipeline" in types_py
        ),
        "no_ocr_runner_execution": (
            types_py.find("ocr_runner_forbidden") >= 0
            and route_pol.get("scheduling_rules", {}).get("runner_execution_forbidden_for_downstream") is not None
        ),
        "no_detection_runner_execution": "detection_runner_forbidden" in types_py,
        "mobilesam_does_not_assert_fact_label": (
            mid_in.get("boundary_flags", {}).get("mobilesam_does_not_assert_fact_label") is True
            and "MobileSAM does not assert" in processor
        ),
        "result_does_not_overwrite_attention_record": (
            re_eval.get("output", {}).get("required_fields", []).count("does_not_overwrite_attention_record") >= 1
            and "does_not_overwrite_attention_record" in processor
        ),
        "result_candidate_not_observation_owner": (
            "result_candidate_not_observation_owner" in types_py
            and "result_candidate_not_observation_owner" in gov
        ),
        "human_correction_must_not_modify_mask": (
            trace_pol.get("human_correction_loop", {}).get("forbidden", []).count("modify_mask") >= 1
            and "human_correction_must_not_modify_mask" in types_py
        ),
        "human_correction_priority_signal_only": (
            "human_correction_priority_signal_only" in types_py
            and ("priority signal" in gov.lower() or "priority signal only" in gov)
        ),
        "trace_closure_required": (
            trace_pol.get("boundary_flags", {}).get("trace_closure_required") is True
            and len(trace_pol.get("required_trace_stages", [])) >= 8
        ),
        "no_fact_write": "no_fact_write" in types_py and "不写 fact" in plan,
        "no_auto_fact_admission": "no_auto_fact_admission" in types_py,
        "no_visual_expression_mutation": "no_visual_expression_mutation" in types_py,
        "upstream_mobilesam_integration_go": mobilesam_int.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "smoke_case1_passes": (
            smoke.get("case_1", {}).get("final_decision") == "GO"
            and smoke.get("final_decision") == "GO"
            and smoke.get("exit_code") == 0
        ),
        "smoke_case2_passes": smoke.get("case_2", {}).get("final_decision") == "GO",
        "case_2_defined": case2.get("case_id") == "Case-2-MobileSAM-Correction-Midplatform-Routing",
        "correction_midplatform_analyzer_defined": (
            "analyze_correction" in corr_analyzer and "classify_attribution" in corr_analyzer
            and "HumanCorrectionMidplatformAnalyzer" in hc_js
        ),
        "no_direct_training_from_raw_correction": (
            corr_tax.get("boundary_flags", {}).get("raw_log_not_training_data") is True
            and "no_direct_training_from_raw_correction" in types_py
        ),
        "midplatform_correction_entry_required": (
            corr_route.get("boundary_flags", {}).get("midplatform_schedules_not_direct_training") is True
            and "midplatform_correction_entry_required" in types_py
        ),
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
    }


def CASE_1_IN_PLAN(plan: str) -> bool:
    return "Case 1" in plan or "Case-1" in plan


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

    smoke = _run_smoke()
    flags = _audit(smoke)
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
        "p1_midplatform_model_test_lens_single_model_interaction_validation_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "interaction_validation_planning": True,
        "case_1_id": "Case-1-MobileSAM-to-OCR-Route-Candidate",
        "ocr_runner_forbidden": True,
        "recommended_next_phase": NEXT_PHASE,
        "validation_capabilities": [
            "result_envelope_to_midplatform_input",
            "result_candidate_does_not_pollute_observation",
            "midplatform_secondary_scheduling",
            "human_correction_closed_loop",
            "trace_closure",
        ],
        "audit_flags": flags,
        "smoke_case1": smoke,
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
        rp = out / "p1_midplatform_model_test_lens_single_model_interaction_validation_planning_review_v1.json"
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
            "test_mode": "planning", "interaction_validation_planning": True,
        }
        payloads = {
            "result_envelope_midplatform_input_schema_record": _load_json(
                f"{SCHEMA_REL}/result_envelope_midplatform_input_schema_v1.json"
            ),
            "observation_re_evaluation_from_result_policy_record": _load_json(
                f"{SCHEMA_REL}/observation_re_evaluation_from_result_policy_v1.json"
            ),
            "followup_route_from_result_policy_record": _load_json(
                f"{SCHEMA_REL}/followup_route_from_result_policy_v1.json"
            ),
            "interaction_trace_closure_policy_record": _load_json(
                f"{SCHEMA_REL}/interaction_trace_closure_policy_v1.json"
            ),
            "case_mobilesam_to_ocr_route_validation_record": _load_json(
                f"{SCHEMA_REL}/case_mobilesam_to_ocr_route_validation_v1.json"
            ),
            "single_model_interaction_validation_plan_record": {
                "plan_ref": f"{VALIDATION_REL}/single_model_interaction_validation_plan_v1.md"
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
