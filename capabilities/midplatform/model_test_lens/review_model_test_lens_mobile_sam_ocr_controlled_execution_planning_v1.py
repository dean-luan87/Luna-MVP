# -*- coding: utf-8 -*-
"""P1 MobileSAM → OCR Controlled Execution — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-Planning-v1-001"
MM_REL = "capabilities/midplatform/model_test_lens/multi_model_interaction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_INTERACTION_UI_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_GO"
)
UPSTREAM_EXPLORATION_SMOKE_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO"

FINAL_GO = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{MM_REL}/mobile_sam_ocr_controlled_execution_plan_v1.md",
    f"{MM_REL}/mobile_sam_ocr_controlled_execution_types_v1.py",
    f"{SCHEMA_REL}/mobile_sam_ocr_controlled_execution_input_policy_v1.json",
    f"{SCHEMA_REL}/ocr_invocation_request_schema_v1.json",
    f"{SCHEMA_REL}/ocr_admission_policy_v1.json",
    f"{SCHEMA_REL}/ocr_controlled_execution_candidate_schema_v1.json",
    f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json",
    f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json",
    f"{SCHEMA_REL}/mobile_sam_ocr_fusion_policy_v1.json",
    f"{GOV_REL}/mobile_sam_ocr_controlled_execution_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_mobile_sam_ocr_controlled_execution_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "mobile_sam_ocr_controlled_execution_input_policy_record",
    "ocr_invocation_request_schema_record",
    "ocr_admission_policy_record",
    "ocr_controlled_execution_candidate_schema_record",
    "ocr_result_envelope_schema_record",
    "ocr_runner_error_candidate_schema_record",
    "mobile_sam_ocr_fusion_policy_record",
    "mobile_sam_ocr_controlled_execution_plan_record",
)

NEXT_PHASE = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001"
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_ocr_runner_call", "desc": "不调用 OCR runner"},
    {"guard_id": "B", "key": "no_ocr_execution", "desc": "不执行 OCR"},
    {"guard_id": "C", "key": "no_ocr_result_generation", "desc": "不生成 OCR result"},
    {"guard_id": "D", "key": "no_model_call", "desc": "不调用模型"},
    {"guard_id": "E", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "F", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "G", "key": "no_mobile_sam_direct_to_ocr", "desc": "MobileSAM 不直调 OCR"},
    {"guard_id": "H", "key": "no_bypass_midplatform", "desc": "不 bypass 中台"},
    {"guard_id": "I", "key": "ocr_request_requires_ocr_task_candidate", "desc": "OCR request 须 task candidate"},
    {"guard_id": "J", "key": "ocr_request_traceable_to_midplatform_analysis", "desc": "request 可追溯 analysis"},
    {"guard_id": "K", "key": "ocr_request_traceable_to_mobile_sam_result", "desc": "request 可追溯 MobileSAM result"},
    {"guard_id": "L", "key": "ocr_admission_requires_ocr_route", "desc": "admission 须 OCR route"},
    {"guard_id": "M", "key": "ocr_execution_candidate_requires_admitted_request", "desc": "candidate 须 admitted request"},
    {"guard_id": "N", "key": "pending_request_cannot_generate_execution_candidate", "desc": "pending 不生成 candidate"},
    {"guard_id": "O", "key": "rejected_request_cannot_generate_execution_candidate", "desc": "rejected 不生成 candidate"},
    {"guard_id": "P", "key": "cancelled_request_cannot_generate_execution_candidate", "desc": "cancelled 不生成 candidate"},
    {"guard_id": "Q", "key": "no_orphan_ocr_execution_candidate", "desc": "禁止 orphan candidate"},
    {"guard_id": "R", "key": "ocr_input_does_not_contain_fact_text", "desc": "输入无 fact text"},
    {"guard_id": "S", "key": "ocr_input_does_not_contain_fact_label", "desc": "输入无 fact label"},
    {"guard_id": "T", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "U", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "V", "key": "ocr_result_requires_envelope", "desc": "OCR result 须 envelope"},
    {"guard_id": "W", "key": "ocr_result_requires_fact_admission", "desc": "OCR result 须 fact admission"},
    {"guard_id": "X", "key": "ocr_error_does_not_write_fact", "desc": "错误不写 fact"},
    {"guard_id": "Y", "key": "fusion_candidate_not_fact", "desc": "融合候选非 fact"},
    {"guard_id": "Z", "key": "no_visual_expression_mutation", "desc": "不改 Visual Expression"},
    {"guard_id": "AA", "key": "no_boundary_clone", "desc": "不 clone boundary"},
    {"guard_id": "AB", "key": "no_ocr_box_on_canvas", "desc": "主图无 OCR box"},
    {"guard_id": "AC", "key": "candidate_only_not_executed_not_fact_preserved", "desc": "candidate 标记保留"},
    {"guard_id": "AD", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "AE", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "AF", "key": "upstream_interaction_ui_go", "desc": "上游 Interaction UI GO"},
    {"guard_id": "AG", "key": "upstream_exploration_smoke_go", "desc": "上游 Exploration Smoke GO"},
    {"guard_id": "AH", "key": "planning_endpoint_defined", "desc": "本阶段终点已定义"},
    {"guard_id": "AI", "key": "fusion_human_correction_defined", "desc": "双模型纠错分流已定义"},
    {"guard_id": "AJ", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "AK", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
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
    plan = _read(f"{MM_REL}/mobile_sam_ocr_controlled_execution_plan_v1.md")
    types_py = _read(f"{MM_REL}/mobile_sam_ocr_controlled_execution_types_v1.py")
    gov = _read(f"{GOV_REL}/mobile_sam_ocr_controlled_execution_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    inp = _load_json(f"{SCHEMA_REL}/mobile_sam_ocr_controlled_execution_input_policy_v1.json")
    req = _load_json(f"{SCHEMA_REL}/ocr_invocation_request_schema_v1.json")
    adm = _load_json(f"{SCHEMA_REL}/ocr_admission_policy_v1.json")
    cec = _load_json(f"{SCHEMA_REL}/ocr_controlled_execution_candidate_schema_v1.json")
    env = _load_json(f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json")
    err = _load_json(f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json")
    fus = _load_json(f"{SCHEMA_REL}/mobile_sam_ocr_fusion_policy_v1.json")

    mobilesam = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )
    interaction_ui = _load_json(
        "_tmp_eval_out/p1_midplatform_single_model_interaction_validation_ui_execution_v1_smoke_v0/"
        "p1_midplatform_single_model_interaction_validation_ui_execution_review_v1.json"
    )
    exploration = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_interaction_exploration_smoke_v0/"
        "mobile_sam_ocr_interaction_exploration_smoke_review_v1.json"
    )

    return {
        "no_ocr_runner_call": inp.get("boundary_flags", {}).get("planning_only") is True and "ocr_runner_forbidden" in types_py,
        "no_ocr_execution": cec.get("field_definitions", {}).get("execution_status", {}).get("enum") == ["planned_only", "not_executed"],
        "no_ocr_result_generation": env.get("planning_only") is True and "ocr_result_forbidden" in types_py,
        "no_model_call": "no_model_call" in types_py and "PLANNING_ONLY" in types_py,
        "no_fact_write": "no_fact_write" in types_py and "不写 fact" in plan,
        "no_navigation_decision": "no_navigation_decision" in types_py and err.get("field_definitions", {}).get("not_navigation_decision", {}).get("const") is True,
        "no_mobile_sam_direct_to_ocr": inp.get("boundary_flags", {}).get("no_mobile_sam_direct_to_ocr") is True,
        "no_bypass_midplatform": inp.get("boundary_flags", {}).get("no_bypass_midplatform") is True,
        "ocr_request_requires_ocr_task_candidate": req.get("boundary_flags", {}).get("ocr_request_requires_ocr_task_candidate") is True,
        "ocr_request_traceable_to_midplatform_analysis": (
            "source_analysis_record_id" in json.dumps(req.get("field_definitions", {}))
            and req.get("boundary_flags", {}).get("ocr_request_traceable_to_midplatform_analysis") is True
        ),
        "ocr_request_traceable_to_mobile_sam_result": (
            "source_result_candidate_id" in json.dumps(req.get("field_definitions", {}))
            and req.get("boundary_flags", {}).get("ocr_request_traceable_to_mobile_sam_result") is True
        ),
        "ocr_admission_requires_ocr_route": adm.get("boundary_flags", {}).get("ocr_admission_requires_ocr_route") is True,
        "ocr_execution_candidate_requires_admitted_request": (
            adm.get("execution_candidate_gates", {}).get("ocr_execution_candidate_requires_admitted_request") is True
            and cec.get("boundary_flags", {}).get("ocr_execution_candidate_requires_admitted_request") is True
        ),
        "pending_request_cannot_generate_execution_candidate": (
            adm.get("execution_candidate_gates", {}).get("pending_request_cannot_generate_execution_candidate") is True
        ),
        "rejected_request_cannot_generate_execution_candidate": (
            adm.get("execution_candidate_gates", {}).get("rejected_request_cannot_generate_execution_candidate") is True
        ),
        "cancelled_request_cannot_generate_execution_candidate": (
            adm.get("execution_candidate_gates", {}).get("cancelled_request_cannot_generate_execution_candidate") is True
        ),
        "no_orphan_ocr_execution_candidate": (
            adm.get("boundary_flags", {}).get("no_orphan_ocr_execution_candidate") is True
            and "source_ocr_invocation_request_id" in json.dumps(cec.get("required_fields", []))
        ),
        "ocr_input_does_not_contain_fact_text": inp.get("boundary_flags", {}).get("ocr_input_does_not_contain_fact_text") is True,
        "ocr_input_does_not_contain_fact_label": inp.get("boundary_flags", {}).get("ocr_input_does_not_contain_fact_label") is True,
        "no_prompt_label_fact_upgrade": inp.get("boundary_flags", {}).get("no_prompt_label_fact_upgrade") is True,
        "no_human_correction_ground_truth": (
            inp.get("boundary_flags", {}).get("no_human_correction_ground_truth") is True
            and (
                req.get("boundary_flags", {}).get("no_human_correction_ground_truth") is True
                or "human_correction_direct_ocr_request" in json.dumps(req.get("forbidden_operations", []))
            )
        ),
        "ocr_result_requires_envelope": env.get("boundary_flags", {}).get("ocr_result_requires_envelope") is True,
        "ocr_result_requires_fact_admission": env.get("boundary_flags", {}).get("ocr_result_requires_fact_admission") is True,
        "ocr_error_does_not_write_fact": err.get("boundary_flags", {}).get("ocr_error_does_not_write_fact") is True,
        "fusion_candidate_not_fact": fus.get("boundary_flags", {}).get("fusion_candidate_not_fact") is True,
        "no_visual_expression_mutation": (
            fus.get("boundary_flags", {}).get("no_visual_expression_mutation") is True
            and "no_visual_expression_mutation" in types_py
        ),
        "no_boundary_clone": fus.get("boundary_flags", {}).get("no_boundary_clone") is True,
        "no_ocr_box_on_canvas": (
            "no_ocr_box_on_canvas" in types_py
            and ("no_ocr_box_on_canvas" in plan or "OCR box" in plan)
        ),
        "candidate_only_not_executed_not_fact_preserved": (
            cec.get("boundary_flags", {}).get("candidate_only_not_executed_not_fact_preserved") is True
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_interaction_ui_go": interaction_ui.get("final_decision") == UPSTREAM_INTERACTION_UI_GO,
        "upstream_exploration_smoke_go": exploration.get("final_decision") == UPSTREAM_EXPLORATION_SMOKE_GO,
        "planning_endpoint_defined": (
            "OCR Controlled Execution Candidate" in plan
            and "ocr_controlled_execution_candidate" in types_py
        ),
        "fusion_human_correction_defined": len(fus.get("human_correction_dual_model_attributions", [])) >= 5,
        "governance_standard_defined": "MobileSamOcrControlledExecutionGovernanceStandardV1" in gov,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
    }


PLANNING_ENDPOINT = "ocr_controlled_execution_candidate"


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
        "p1_midplatform_mobile_sam_ocr_controlled_execution_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "planning_endpoint": PLANNING_ENDPOINT,
        "ocr_runner_forbidden": True,
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
        rp = out / "p1_midplatform_mobile_sam_ocr_controlled_execution_planning_review_v1.json"
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
            "mobile_sam_ocr_controlled_execution_input_policy_record": _load_json(
                f"{SCHEMA_REL}/mobile_sam_ocr_controlled_execution_input_policy_v1.json"
            ),
            "ocr_invocation_request_schema_record": _load_json(f"{SCHEMA_REL}/ocr_invocation_request_schema_v1.json"),
            "ocr_admission_policy_record": _load_json(f"{SCHEMA_REL}/ocr_admission_policy_v1.json"),
            "ocr_controlled_execution_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/ocr_controlled_execution_candidate_schema_v1.json"
            ),
            "ocr_result_envelope_schema_record": _load_json(f"{SCHEMA_REL}/ocr_result_envelope_schema_v1.json"),
            "ocr_runner_error_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/ocr_runner_error_candidate_schema_v1.json"
            ),
            "mobile_sam_ocr_fusion_policy_record": _load_json(f"{SCHEMA_REL}/mobile_sam_ocr_fusion_policy_v1.json"),
            "mobile_sam_ocr_controlled_execution_plan_record": {
                "plan_ref": f"{MM_REL}/mobile_sam_ocr_controlled_execution_plan_v1.md"
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
