# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Foundation — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-Planning-v1-001"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = "capabilities/test_board/model_governance/phase_p1_midplatform_luna_model_manager_foundation_planning_v1_001"

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_teacher_routing_layer_planning_v1_review_v0/"
        "p1_midplatform_teacher_routing_layer_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO": (
        "_tmp_eval_out/p1_midplatform_teacher_performance_evaluation_v1_review_v0/"
        "p1_midplatform_teacher_performance_evaluation_review_v1.json"
    ),
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_real_provider_integration_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{MM_REL}/luna_model_manager_foundation_plan_v1.md",
    f"{MM_REL}/luna_model_manager_types_v1.py",
    f"{MM_REL}/luna_model_manager_processor_v1.py",
    f"{MM_REL}/registries/model_registry_v1.json",
    f"{MM_REL}/registries/capability_registry_v1.json",
    f"{MM_REL}/governance/model_admission_policy_v1.json",
    f"{MM_REL}/governance/model_lifecycle_policy_v1.json",
    f"{MM_REL}/engines/model_routing_engine_v1.py",
    f"{MM_REL}/engines/model_evaluation_engine_v1.py",
    f"{MM_REL}/schemas/model_routing_result_schema_v1.json",
    f"{MM_REL}/schemas/model_evaluation_profile_schema_v1.json",
    f"{TB_REL}/luna_model_manager_foundation_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_foundation_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_foundation_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("foundation_plan_present", "foundation 规划文档"),
        ("model_registry_present", "Model Registry"),
        ("capability_registry_present", "Capability Registry"),
        ("routing_engine_present", "Routing Engine"),
        ("evaluation_engine_present", "Evaluation Engine"),
        ("admission_policy_present", "Admission Policy"),
        ("lifecycle_policy_present", "Lifecycle Policy"),
        ("capability_first_routing", "能力优先路由"),
        ("unified_not_fragmented", "统一不碎片化"),
        ("teacher_system_subsumed", "Teacher 体系收拢"),
        ("no_auto_execution", "不自动执行"),
        ("no_auto_admission", "不自动准入"),
        ("case_a_shopfront_ocr", "Case A 店招 OCR"),
        ("case_b_unknown_qwen", "Case B unknown Qwen"),
        ("case_c_capability_lookup", "Case C 能力查找"),
        ("case_d_admission_candidate", "Case D Admission"),
        ("case_e_unified_eval", "Case E 统一评估"),
        ("frozen_prerequisites_referenced", "前置成果冻结引用"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("smoke_cases_passed", "smoke 通过"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
    ], start=1)
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


def _load_json_path(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    plan = _read(f"{MM_REL}/luna_model_manager_foundation_plan_v1.md")
    processor = _read(f"{MM_REL}/luna_model_manager_processor_v1.py")
    model_reg = _load_json(f"{MM_REL}/registries/model_registry_v1.json")
    cap_reg = _load_json(f"{MM_REL}/registries/capability_registry_v1.json")
    admission = _load_json(f"{MM_REL}/governance/model_admission_policy_v1.json")
    lifecycle = _load_json(f"{MM_REL}/governance/model_lifecycle_policy_v1.json")
    routing = _read(f"{MM_REL}/engines/model_routing_engine_v1.py")
    evaluation = _read(f"{MM_REL}/engines/model_evaluation_engine_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_foundation_planning_v1_001.luna_model_manager_foundation_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "foundation_plan_present": "Model Manager" in plan and "Capability Registry" in plan,
        "model_registry_present": bool(model_reg.get("models")) and any(m.get("model_id") == "qwen_vl" for m in model_reg.get("models", [])),
        "capability_registry_present": bool(cap_reg.get("capabilities")),
        "routing_engine_present": "route_model_request" in routing,
        "evaluation_engine_present": "evaluate_model_performance" in evaluation,
        "admission_policy_present": bool(admission.get("admission_pipeline")),
        "lifecycle_policy_present": bool(lifecycle.get("lifecycle_states")),
        "capability_first_routing": "capability_first" in routing and "resolve_capability_need" in routing,
        "unified_not_fragmented": "unified_manager_not_fragmented" in _read(f"{MM_REL}/luna_model_manager_types_v1.py"),
        "teacher_system_subsumed": "teacher_adapter" in processor and "qwen_vl" in _read(f"{MM_REL}/registries/model_registry_v1.json"),
        "no_auto_execution": "no_auto_execution" in routing and admission.get("boundary_flags", {}).get("no_auto_execution"),
        "no_auto_admission": admission.get("boundary_flags", {}).get("no_auto_admission") is True,
        "case_a_shopfront_ocr": _case(cases, "case_a_shopfront_ocr_routing").get("passed") is True,
        "case_b_unknown_qwen": _case(cases, "case_b_unknown_scene_qwen_routing").get("passed") is True,
        "case_c_capability_lookup": _case(cases, "case_c_capability_first_lookup").get("passed") is True,
        "case_d_admission_candidate": _case(cases, "case_d_model_admission_candidate").get("passed") is True,
        "case_e_unified_eval": _case(cases, "case_e_unified_evaluation_profile").get("passed") is True,
        "frozen_prerequisites_referenced": "FROZEN_PREREQUISITES" in _read(f"{MM_REL}/luna_model_manager_types_v1.py"),
        "no_existing_runner_mutation": "model_manager" not in runner,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "upstream_gos_confirmed": upstream_ok,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]
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

    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_foundation_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "frozen_prerequisites": [
            "Teacher_Adapter",
            "Teacher_Routing",
            "Teacher_Performance_Evaluation",
            "Qwen_VL_Real_Provider",
        ],
        "known_limits": [
            "planning_only_no_execution",
            "teacher_modules_not_removed_frozen_as_prerequisites",
            "multi_teacher_validation_deferred",
            "gemini_gpt_admission_pending",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_foundation_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
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
