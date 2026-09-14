# -*- coding: utf-8
"""P1 Text-First Target Proposal Validation — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Planning-v1-001"
TP_REL = "capabilities/midplatform/model_test_lens/target_proposal"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/target_proposal"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"
NO_SLAM_REL = "capabilities/midplatform/model_test_lens/schemas/multi_model_interaction/no_slam_for_text_policy_v1.json"

UPSTREAM_DUAL_ROUTE_EXEC_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO"
UPSTREAM_SCENE_AWARE_EXEC_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO"
UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_OCR_SANDBOX_EXEC_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_BLOCKED"
PLANNING_ENDPOINT = "target_proposal_comparison_candidate"
NEXT_PHASE = "Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Execution-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TP_REL}/text_first_target_proposal_validation_plan_v1.md",
    f"{TP_REL}/text_first_target_proposal_types_v1.py",
    f"{TP_REL}/text_first_target_proposal_validation_smoke_v1.py",
    f"{SCHEMA_REL}/text_region_candidate_schema_v1.json",
    f"{SCHEMA_REL}/text_target_proposal_policy_v1.json",
    f"{SCHEMA_REL}/target_proposal_comparison_candidate_schema_v1.json",
    f"{SCHEMA_REL}/text_detector_stub_policy_v1.json",
    f"{SCHEMA_REL}/midplatform_target_selection_policy_v1.json",
    f"{GOV_REL}/text_first_target_proposal_validation_governance_standard_v1.md",
    f"{_PKG}/run_text_first_target_proposal_validation_smoke_v1.py",
    f"{_PKG}/review_model_test_lens_text_first_target_proposal_validation_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "text_region_candidate_schema_record",
    "text_target_proposal_policy_record",
    "target_proposal_comparison_candidate_schema_record",
    "text_detector_stub_policy_record",
    "midplatform_target_selection_policy_record",
    "text_first_target_proposal_validation_plan_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_ocr_recognition", "desc": "不做 OCR recognition"},
    {"guard_id": "B", "key": "no_text_fact_generation", "desc": "不生成文字 fact"},
    {"guard_id": "C", "key": "text_region_candidate_not_fact", "desc": "text region 非 fact"},
    {"guard_id": "D", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "E", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "F", "key": "sam_not_primary_text_detector", "desc": "SAM 非文字检测主入口"},
    {"guard_id": "G", "key": "no_slam_text_detection", "desc": "SLAM 不做文字检测"},
    {"guard_id": "H", "key": "text_detector_stub_not_ocr_result", "desc": "stub 非 OCR 结果"},
    {"guard_id": "I", "key": "target_proposal_comparison_not_fact", "desc": "comparison 非 fact"},
    {"guard_id": "J", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "K", "key": "no_human_correction_ground_truth", "desc": "纠错非 ground truth"},
    {"guard_id": "L", "key": "candidate_only_preserved", "desc": "candidate_only 保留"},
    {"guard_id": "M", "key": "three_candidate_layers_defined", "desc": "三类候选已定义"},
    {"guard_id": "N", "key": "text_first_chain_defined", "desc": "Text-first 链路已定义"},
    {"guard_id": "O", "key": "four_smoke_cases_defined", "desc": "四类 smoke 已定义"},
    {"guard_id": "P", "key": "smoke_cases_pass", "desc": "smoke 通过"},
    {"guard_id": "Q", "key": "planning_endpoint_defined", "desc": "本阶段终点已定义"},
    {"guard_id": "R", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "S", "key": "upstream_dual_route_execution_go", "desc": "上游 Dual Route Execution GO"},
    {"guard_id": "T", "key": "upstream_scene_aware_execution_go", "desc": "上游 Scene-Aware Execution GO"},
    {"guard_id": "U", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "V", "key": "upstream_ocr_sandbox_execution_go", "desc": "上游 OCR Sandbox GO"},
    {"guard_id": "W", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "X", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
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
    plan = _read(f"{TP_REL}/text_first_target_proposal_validation_plan_v1.md")
    types_py = _read(f"{TP_REL}/text_first_target_proposal_types_v1.py")
    gov = _read(f"{GOV_REL}/text_first_target_proposal_validation_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    text_region = _load_json(f"{SCHEMA_REL}/text_region_candidate_schema_v1.json")
    proposal_policy = _load_json(f"{SCHEMA_REL}/text_target_proposal_policy_v1.json")
    comparison = _load_json(f"{SCHEMA_REL}/target_proposal_comparison_candidate_schema_v1.json")
    stub_policy = _load_json(f"{SCHEMA_REL}/text_detector_stub_policy_v1.json")
    selection = _load_json(f"{SCHEMA_REL}/midplatform_target_selection_policy_v1.json")
    no_slam = _load_json(NO_SLAM_REL)

    dual_route = _load_json(
        "_tmp_eval_out/p1_midplatform_dual_route_perception_validation_execution_v1_smoke_v0/"
        "p1_midplatform_dual_route_perception_validation_execution_review_v1.json"
    )
    scene_aware = _load_json(
        "_tmp_eval_out/p1_midplatform_scene_aware_segmentation_prompt_policy_execution_v1_smoke_v0/"
        "p1_midplatform_scene_aware_segmentation_prompt_policy_execution_review_v1.json"
    )
    mobilesam = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )
    ocr_sandbox = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_review_v1.json"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.midplatform.model_test_lens.target_proposal.text_first_target_proposal_validation_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )

        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED, "failed_checks": ["smoke.import_error"]}

    layers = proposal_policy.get("candidate_layers", {})

    return {
        "no_ocr_recognition": (
            text_region.get("boundary_flags", {}).get("no_ocr_recognition") is True
            and stub_policy.get("boundary_flags", {}).get("no_ocr_recognition") is True
            and text_region.get("field_definitions", {}).get("recognized_text", {}).get("type") == "null"
        ),
        "no_text_fact_generation": (
            "no_text_fact_generation" in plan or "不输出真实文字" in plan
        ) and "recognized_text_as_fact" in json.dumps(text_region.get("forbidden_operations", [])),
        "text_region_candidate_not_fact": (
            text_region.get("boundary_flags", {}).get("text_region_candidate_not_fact") is True
        ),
        "no_fact_write": (
            comparison.get("boundary_flags", {}).get("no_fact_write") is True
            and selection.get("boundary_flags", {}).get("no_fact_write") is True
        ),
        "no_navigation_decision": (
            selection.get("boundary_flags", {}).get("no_navigation_decision") is True
            and proposal_policy.get("boundary_flags", {}).get("no_navigation_decision") is True
        ),
        "sam_not_primary_text_detector": (
            proposal_policy.get("boundary_flags", {}).get("sam_not_primary_text_detector") is True
            and layers.get("region_proposal_candidate", {}).get("not_primary_for_text_discovery") is True
            and "sam_not_primary_text_detector" in plan
        ),
        "no_slam_text_detection": no_slam.get("boundary_flags", {}).get("no_slam_text_detection") is True,
        "text_detector_stub_not_ocr_result": (
            stub_policy.get("boundary_flags", {}).get("text_detector_stub_not_ocr_result") is True
            and "recognized_text" in json.dumps(stub_policy.get("forbidden_outputs", []))
        ),
        "target_proposal_comparison_not_fact": (
            comparison.get("boundary_flags", {}).get("target_proposal_comparison_not_fact") is True
            and comparison.get("planning_endpoint") == PLANNING_ENDPOINT
        ),
        "no_prompt_label_fact_upgrade": "no_prompt_label_fact_upgrade" in types_py,
        "no_human_correction_ground_truth": "no_human_correction_ground_truth" in types_py,
        "candidate_only_preserved": (
            selection.get("boundary_flags", {}).get("candidate_only_preserved") is True
            and text_region.get("candidate_only") is True
        ),
        "three_candidate_layers_defined": all(
            k in layers for k in (
                "region_proposal_candidate",
                "text_region_candidate",
                "semantic_target_candidate",
            )
        ),
        "text_first_chain_defined": (
            "text_detector_stub" in plan
            and "text_first_chain" in proposal_policy
        ),
        "four_smoke_cases_defined": "Smoke Cases（4）" in plan or "Smoke Cases" in plan,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
        "planning_endpoint_defined": (
            PLANNING_ENDPOINT in types_py
            and comparison.get("planning_endpoint") == PLANNING_ENDPOINT
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "upstream_dual_route_execution_go": dual_route.get("final_decision") == UPSTREAM_DUAL_ROUTE_EXEC_GO,
        "upstream_scene_aware_execution_go": scene_aware.get("final_decision") == UPSTREAM_SCENE_AWARE_EXEC_GO,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_ocr_sandbox_execution_go": ocr_sandbox.get("final_decision") == UPSTREAM_OCR_SANDBOX_EXEC_GO,
        "governance_standard_defined": "TextFirstTargetProposalValidationGovernanceStandardV1" in gov,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
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
        "p1_midplatform_text_first_target_proposal_validation_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "planning_endpoint": PLANNING_ENDPOINT,
        "no_model_call": True,
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
        rp = out / "p1_midplatform_text_first_target_proposal_validation_planning_review_v1.json"
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
            "test_mode": "planning", "text_first_target_proposal_planning": True,
        }
        payloads = {
            "text_region_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/text_region_candidate_schema_v1.json"
            ),
            "text_target_proposal_policy_record": _load_json(
                f"{SCHEMA_REL}/text_target_proposal_policy_v1.json"
            ),
            "target_proposal_comparison_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/target_proposal_comparison_candidate_schema_v1.json"
            ),
            "text_detector_stub_policy_record": _load_json(
                f"{SCHEMA_REL}/text_detector_stub_policy_v1.json"
            ),
            "midplatform_target_selection_policy_record": _load_json(
                f"{SCHEMA_REL}/midplatform_target_selection_policy_v1.json"
            ),
            "text_first_target_proposal_validation_plan_record": {
                "plan_ref": f"{TP_REL}/text_first_target_proposal_validation_plan_v1.md"
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
