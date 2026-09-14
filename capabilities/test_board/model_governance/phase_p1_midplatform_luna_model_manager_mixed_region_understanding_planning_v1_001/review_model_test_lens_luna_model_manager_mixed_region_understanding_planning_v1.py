# -*- coding: utf-8 -*-
"""P1 Luna Mixed Region Understanding — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001"
MR_REL = "capabilities/midplatform/model_manager/runtime/mixed_region"
OWN_REL = "capabilities/midplatform/model_manager/runtime/mixed_region/ownership_understanding"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_mixed_region_understanding_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{MR_REL}/region_intelligence_plan_v1.md",
    f"{MR_REL}/mixed_region_analyzer_v1.py",
    f"{MR_REL}/information_channel_activation_v1.py",
    f"{MR_REL}/text_evidence_builder_v1.py",
    f"{MR_REL}/visual_evidence_builder_v1.py",
    f"{MR_REL}/spatial_evidence_builder_v1.py",
    f"{MR_REL}/context_evidence_builder_v1.py",
    f"{MR_REL}/evidence_completeness_v1.py",
    f"{MR_REL}/semantic_fusion_adapter_v1.py",
    f"{MR_REL}/mixed_region_understanding_adapter_v1.py",
    f"{MR_REL}/mixed_region_understanding_policy_v1.json",
    f"{OWN_REL}/region_owner_analyzer_v1.py",
    f"{OWN_REL}/occlusion_graph_v1.py",
    f"{OWN_REL}/text_owner_assignment_v1.py",
    f"{OWN_REL}/ownership_evidence_builder_v1.py",
    f"{MM_REL}/luna_model_manager_mixed_region_understanding_types_v1.py",
    f"{MM_REL}/luna_model_manager_mixed_region_understanding_processor_v1.py",
    f"{TB_REL}/luna_model_manager_mixed_region_understanding_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_mixed_region_understanding_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_mixed_region_understanding_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("region_intelligence_plan", "Region Intelligence 规划"),
        ("mixed_region_analyzer", "Mixed Region Analyzer"),
        ("channel_activation", "Information Channel Activation"),
        ("evidence_completeness", "Evidence Completeness"),
        ("ownership_analyzer", "Region Owner Analyzer"),
        ("occlusion_graph", "Occlusion Graph"),
        ("text_owner_assignment", "Text Owner Assignment"),
        ("five_channel_ownership", "五通道含 Ownership"),
        ("ownership_before_ocr", "Ownership 先于 OCR"),
        ("region_capabilities", "understand_region_* 能力"),
        ("not_ocr_extension", "非 OCR 扩展"),
        ("not_fixed_ocr_vlm", "非固定 OCR+VLM"),
        ("fusion_not_answer_merge", "Fusion 非答案合并"),
        ("analyzer_not_recognizer", "Analyzer 非识别器"),
        ("case_a_shopfront", "Case A 店招 slots"),
        ("case_b_metro", "Case B 地铁多通道"),
        ("case_f_occlusion", "Case F 遮挡"),
        ("case_g_conflict", "Case G 冲突"),
        ("case_h_artistic", "Case H 艺术字"),
        ("case_i_logo_only", "Case I Logo 主导"),
        ("case_j_ocr_wrong", "Case J OCR 错误"),
        ("case_k_multi_object", "Case K 多对象"),
        ("case_l_stacked_docs", "Case L 叠放纸张"),
        ("case_m_glass_reflection", "Case M 玻璃反光"),
        ("case_n_shelf", "Case N 货架分离"),
        ("upstream_gos_confirmed", "上游 GO"),
        ("smoke_cases_passed", "smoke 通过"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    plan = _read(f"{MR_REL}/region_intelligence_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{MR_REL}/mixed_region_understanding_policy_v1.json")
    types_src = _read(f"{MM_REL}/luna_model_manager_mixed_region_understanding_types_v1.py")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_mixed_region_understanding_planning_v1_001.luna_model_manager_mixed_region_understanding_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "region_intelligence_plan": "Region Intelligence" in plan and "信息载体" in plan,
        "mixed_region_analyzer": "information_slots" in _read(f"{MR_REL}/mixed_region_analyzer_v1.py"),
        "channel_activation": "activate_information_channels" in _read(f"{MR_REL}/information_channel_activation_v1.py"),
        "evidence_completeness": "ownership_completeness" in _read(f"{MR_REL}/evidence_completeness_v1.py"),
        "ownership_analyzer": "analyze_region_owners" in _read(f"{OWN_REL}/region_owner_analyzer_v1.py"),
        "occlusion_graph": "build_occlusion_graph" in _read(f"{OWN_REL}/occlusion_graph_v1.py"),
        "text_owner_assignment": "assign_text_owners" in _read(f"{OWN_REL}/text_owner_assignment_v1.py"),
        "five_channel_ownership": "ownership_channel" in json.dumps(policy.get("architecture", {}).get("channels", {})),
        "ownership_before_ocr": policy.get("boundary_flags", {}).get("ownership_before_ocr") is True,
        "region_capabilities": "understand_region_ownership" in types_src,
        "not_ocr_extension": policy.get("boundary_flags", {}).get("not_ocr_extension") is True,
        "not_fixed_ocr_vlm": "fixed_ocr_plus_vlm" in json.dumps(policy.get("forbidden", [])),
        "fusion_not_answer_merge": "not_answer_merge" in _read(f"{MR_REL}/semantic_fusion_adapter_v1.py"),
        "analyzer_not_recognizer": "not_recognizer" in _read(f"{OWN_REL}/region_owner_analyzer_v1.py"),
        "case_a_shopfront": _case(cases, "case_a_shopfront_information_slots").get("passed") is True,
        "case_b_metro": _case(cases, "case_b_metro_multi_channel").get("passed") is True,
        "case_f_occlusion": _case(cases, "case_f_occlusion_visual_supplement").get("passed") is True,
        "case_g_conflict": _case(cases, "case_g_text_visual_conflict").get("passed") is True,
        "case_h_artistic": _case(cases, "case_h_artistic_text_visual_gap").get("passed") is True,
        "case_i_logo_only": _case(cases, "case_i_logo_only_no_text_fact").get("passed") is True,
        "case_j_ocr_wrong": _case(cases, "case_j_ocr_wrong_visual_support").get("passed") is True,
        "case_k_multi_object": _case(cases, "case_k_multi_object_multi_slots").get("passed") is True,
        "case_l_stacked_docs": _case(cases, "case_l_stacked_documents_ownership").get("passed") is True,
        "case_m_glass_reflection": _case(cases, "case_m_glass_reflection_ownership").get("passed") is True,
        "case_n_shelf": _case(cases, "case_n_shelf_entity_separation").get("passed") is True,
        "upstream_gos_confirmed": upstream_ok,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
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

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_mixed_region_understanding_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Region_Intelligence_Layer",
        "planning_only": True,
        "ownership_understanding": True,
        "five_channel_with_ownership": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["visual_spatial_context_fixture_only", "dryrun_deferred"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_mixed_region_understanding_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
