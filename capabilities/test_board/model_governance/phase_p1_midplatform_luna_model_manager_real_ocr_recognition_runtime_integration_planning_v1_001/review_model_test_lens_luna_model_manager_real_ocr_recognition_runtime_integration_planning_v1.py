# -*- coding: utf-8 -*-
"""P1 Luna OCR Recognition Runtime — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001"
OCR_REL = "capabilities/midplatform/model_manager/runtime/text_recognition"
MR_REL = "capabilities/midplatform/model_manager/runtime/mixed_region"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_real_text_detection_runtime_integration_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{OCR_REL}/text_recognition_runtime_plan_v1.md",
    f"{OCR_REL}/text_recognition_runtime_adapter_v1.py",
    f"{OCR_REL}/text_recognition_request_builder_v1.py",
    f"{OCR_REL}/text_recognition_response_parser_v1.py",
    f"{OCR_REL}/text_recognition_evidence_normalizer_v1.py",
    f"{OCR_REL}/text_recognition_runtime_metrics_v1.py",
    f"{OCR_REL}/text_recognition_runtime_policy_v1.json",
    f"{MR_REL}/mixed_region_understanding_plan_v1.md",
    f"{MR_REL}/mixed_region_analyzer_v1.py",
    f"{MR_REL}/text_evidence_builder_v1.py",
    f"{MR_REL}/visual_evidence_builder_v1.py",
    f"{MR_REL}/semantic_fusion_adapter_v1.py",
    f"{MR_REL}/mixed_region_understanding_adapter_v1.py",
    f"{MR_REL}/mixed_region_understanding_policy_v1.json",
    f"{MM_REL}/luna_model_manager_text_recognition_runtime_types_v1.py",
    f"{MM_REL}/luna_model_manager_text_recognition_runtime_processor_v1.py",
    f"{TB_REL}/luna_model_manager_real_ocr_recognition_runtime_integration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_real_ocr_recognition_runtime_integration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_real_ocr_recognition_runtime_integration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("runtime_plan_present", "Runtime 规划文档"),
        ("mixed_region_plan_present", "Mixed Region 规划"),
        ("mixed_region_analyzer_present", "Mixed Region Analyzer"),
        ("text_evidence_builder_present", "Text Evidence Builder"),
        ("visual_evidence_builder_present", "Visual Evidence Builder"),
        ("semantic_fusion_present", "Semantic Fusion Adapter"),
        ("mixed_region_adapter_present", "Mixed Region Adapter"),
        ("mixed_region_policy_present", "Mixed Region Policy"),
        ("runtime_adapter_present", "OCR Runtime Adapter"),
        ("three_layer_evidence", "三层证据模型"),
        ("text_visual_dual_processing", "Text-Visual 双路径"),
        ("ocr_is_text_branch_only", "OCR 仅 Text Branch"),
        ("recognition_only_not_detection", "只接 Recognition"),
        ("ocr_not_location_fact", "OCR 不输出空间事实"),
        ("case_a_shopfront", "Case A 店招"),
        ("case_b_metro", "Case B 地铁导视"),
        ("case_c_blurry", "Case C 模糊文字"),
        ("case_d_unsupported", "Case D OCR 幻觉"),
        ("case_e_runtime_fail", "Case E Runtime 故障"),
        ("case_f_occlusion", "Case F 遮挡 Visual 补充"),
        ("case_g_conflict", "Case G Text/Visual 冲突"),
        ("case_h_artistic", "Case H 艺术字 Visual 补充"),
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
    plan = _read(f"{OCR_REL}/text_recognition_runtime_plan_v1.md")
    mr_plan = _read(f"{MR_REL}/mixed_region_understanding_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{OCR_REL}/text_recognition_runtime_policy_v1.json")
    mr_policy = _load_json(_detect_repo_root() / f"{MR_REL}/mixed_region_understanding_policy_v1.json")
    adapter = _read(f"{OCR_REL}/text_recognition_runtime_adapter_v1.py")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_v1_001.luna_model_manager_real_ocr_recognition_runtime_integration_planning_smoke_v1 import (  # noqa: WPS433
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
        "runtime_plan_present": "Mixed Region" in plan or "Text Branch" in plan,
        "mixed_region_plan_present": "Mixed Visual Semantic Region" in mr_plan,
        "mixed_region_analyzer_present": "analyze_mixed_region" in _read(f"{MR_REL}/mixed_region_analyzer_v1.py"),
        "text_evidence_builder_present": "build_text_evidence" in _read(f"{MR_REL}/text_evidence_builder_v1.py"),
        "visual_evidence_builder_present": "build_visual_evidence" in _read(f"{MR_REL}/visual_evidence_builder_v1.py"),
        "semantic_fusion_present": "fuse_mixed_evidence" in _read(f"{MR_REL}/semantic_fusion_adapter_v1.py"),
        "mixed_region_adapter_present": "run_mixed_region_understanding" in _read(f"{MR_REL}/mixed_region_understanding_adapter_v1.py"),
        "mixed_region_policy_present": mr_policy.get("schema_id") == "MixedRegionUnderstandingPolicyV1",
        "runtime_adapter_present": "run_text_recognition_slot" in adapter,
        "three_layer_evidence": len(mr_policy.get("evidence_layers", [])) == 3,
        "text_visual_dual_processing": mr_policy.get("boundary_flags", {}).get("text_visual_dual_processing") is True,
        "ocr_is_text_branch_only": policy.get("boundary_flags", {}).get("ocr_is_text_branch_only") is True,
        "recognition_only_not_detection": policy.get("boundary_flags", {}).get("recognition_only_not_detection") is True,
        "ocr_not_location_fact": "ocr_not_location_fact" in json.dumps(policy),
        "case_a_shopfront": _case(cases, "case_a_shopfront_ocr_text_candidate").get("passed") is True,
        "case_b_metro": _case(cases, "case_b_metro_direction_ocr").get("passed") is True,
        "case_c_blurry": _case(cases, "case_c_blurry_low_confidence").get("passed") is True,
        "case_d_unsupported": _case(cases, "case_d_unsupported_ocr_claim").get("passed") is True,
        "case_e_runtime_fail": _case(cases, "case_e_ocr_runtime_failure").get("passed") is True,
        "case_f_occlusion": _case(cases, "case_f_occlusion_visual_supplement").get("passed") is True,
        "case_g_conflict": _case(cases, "case_g_text_visual_conflict").get("passed") is True,
        "case_h_artistic": _case(cases, "case_h_artistic_text_visual_gap").get("passed") is True,
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Mixed_Region_Understanding_Planning",
        "planning_only": True,
        "mixed_region_understanding_core": True,
        "text_visual_dual_processing": True,
        "ocr_is_text_branch_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["planning_fixture_not_real_paddleocr", "visual_branch_fixture_only", "qwen_context_deferred"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_real_ocr_recognition_runtime_integration_planning_review_v1.json"
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
