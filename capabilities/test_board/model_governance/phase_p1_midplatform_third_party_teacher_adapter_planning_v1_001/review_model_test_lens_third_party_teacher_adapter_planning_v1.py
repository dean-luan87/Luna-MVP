# -*- coding: utf-8
"""P1 Third-Party Teacher Adapter — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-Planning-v1-001"
TA_REL = "capabilities/midplatform/teacher_adapter"
SCHEMA_REL = f"{TA_REL}/schemas"
GOV_REL = f"{TA_REL}/governance"
PROV_REL = f"{TA_REL}/providers"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_third_party_teacher_adapter_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_testboard_ui_execution_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_dryrun_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_agent_planning_layer_concept_planning_v1_review_v0/"
        "p1_midplatform_luna_agent_planning_layer_concept_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_NETWORK_ASSISTED_SITUATION_LEARNING_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_network_assisted_situation_learning_planning_v1_review_v0/"
        "p1_midplatform_network_assisted_situation_learning_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001"

SCHEMA_FILES = (
    f"{SCHEMA_REL}/teacher_assistance_request_schema_v1.json",
    f"{SCHEMA_REL}/teacher_adapter_input_schema_v1.json",
    f"{SCHEMA_REL}/teacher_admission_decision_schema_v1.json",
    f"{SCHEMA_REL}/teacher_evidence_candidate_schema_v1.json",
    f"{SCHEMA_REL}/perception_teacher_output_schema_v1.json",
    f"{SCHEMA_REL}/planning_teacher_output_schema_v1.json",
    f"{SCHEMA_REL}/learning_teacher_output_schema_v1.json",
)

PROVIDER_FILES = (
    f"{PROV_REL}/gemini_adapter_v1.py",
    f"{PROV_REL}/qwen_vl_adapter_v1.py",
    f"{PROV_REL}/gpt_vision_adapter_v1.py",
    f"{PROV_REL}/internvl_adapter_v1.py",
    f"{PROV_REL}/__init__.py",
)

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TA_REL}/third_party_teacher_adapter_concept_plan_v1.md",
    f"{TA_REL}/luna_teacher_adapter_types_v1.py",
    f"{TA_REL}/luna_teacher_adapter_processor_v1.py",
    f"{GOV_REL}/luna_teacher_adapter_policy_v1.json",
    *SCHEMA_FILES,
    *PROVIDER_FILES,
    f"{TB_REL}/luna_teacher_adapter_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_teacher_adapter_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_third_party_teacher_adapter_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("teacher_adapter_doc_present", "规划文档存在"),
        ("teacher_adapter_types_present", "types 存在"),
        ("teacher_adapter_processor_present", "processor 存在"),
        ("teacher_adapter_policy_present", "policy 存在"),
        ("all_schema_files_present", "schema 齐全"),
        ("provider_stubs_present", "provider stub 齐全"),
        ("unified_interface_present", "统一接口 request_teacher_assistance"),
        ("admission_policy_present", "Teacher Admission Policy"),
        ("teacher_evidence_not_fact", "teacher evidence 非 fact"),
        ("no_direct_l1_scene_override", "不直接覆盖 L1 scene"),
        ("no_direct_l2_selected_plan_override", "不覆盖 L2 selected plan"),
        ("no_runner_invocation", "不触发 runner"),
        ("no_tool_execution", "不执行工具"),
        ("no_fact_write", "不写 fact"),
        ("no_direct_training", "不直接训练"),
        ("specialized_tool_preferred_over_vlm", "专业工具优先于 VLM"),
        ("alternative_plan_only", "Planning Teacher 仅 alternative"),
        ("learning_requires_policy_review", "Learning 需 policy review"),
        ("case_a_shopfront_ocr_no_teacher", "Case A 店招 OCR noop"),
        ("case_b_unknown_teacher_candidate", "Case B unknown teacher"),
        ("case_c_alternative_plan_only", "Case C alternative only"),
        ("case_d_bad_teacher_reject", "Case D policy reject"),
        ("case_e_learning_chain", "Case E learning chain"),
        ("no_real_network", "无真实网络"),
        ("no_existing_runner_mutation", "未改 runner"),
        ("provider_routed_via_adapter", "经 Adapter 路由 provider"),
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
    plan_md = _read(f"{TA_REL}/third_party_teacher_adapter_concept_plan_v1.md")
    types_py = _read(f"{TA_REL}/luna_teacher_adapter_types_v1.py")
    processor = _read(f"{TA_REL}/luna_teacher_adapter_processor_v1.py")
    policy = _load_json(f"{GOV_REL}/luna_teacher_adapter_policy_v1.json")
    smoke_py = _read(f"{TB_REL}/luna_teacher_adapter_planning_smoke_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_third_party_teacher_adapter_planning_v1_001.luna_teacher_adapter_planning_smoke_v1 import (  # noqa: WPS433
            run_smoke_cases,
        )
        smoke_result = run_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    case_a = _case(cases, "case_a_shopfront_ocr_no_teacher")
    case_b = _case(cases, "case_b_unknown_scene_teacher_candidate")
    case_c = _case(cases, "case_c_planning_conflict_alternative_only")
    case_d = _case(cases, "case_d_bad_teacher_policy_reject")
    case_e = _case(cases, "case_e_learning_teacher_candidate_chain")

    upstream_ok = all(
        _load_json_path(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "teacher_adapter_doc_present": "Teacher Adapter" in plan_md and "顾问" in plan_md,
        "teacher_adapter_types_present": "TeacherEvidenceCandidate" in types_py,
        "teacher_adapter_processor_present": "request_teacher_assistance" in processor,
        "teacher_adapter_policy_present": bool(policy.get("boundary_flags")),
        "all_schema_files_present": all(_read(s) for s in SCHEMA_FILES),
        "provider_stubs_present": all(_read(p) for p in PROVIDER_FILES),
        "unified_interface_present": "request_teacher_assistance" in processor,
        "admission_policy_present": "evaluate_teacher_admission" in processor,
        "teacher_evidence_not_fact": flags.get("teacher_evidence_not_fact") is True,
        "no_direct_l1_scene_override": flags.get("no_direct_l1_scene_override") is True,
        "no_direct_l2_selected_plan_override": flags.get("no_direct_l2_selected_plan_override") is True,
        "no_runner_invocation": flags.get("no_runner_invocation") is True,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "no_fact_write": flags.get("no_fact_write") is True,
        "no_direct_training": flags.get("no_direct_training") is True,
        "specialized_tool_preferred_over_vlm": flags.get("specialized_tool_preferred_over_vlm") is True,
        "alternative_plan_only": flags.get("alternative_plan_only") is True,
        "learning_requires_policy_review": flags.get("learning_requires_policy_review") is True,
        "case_a_shopfront_ocr_no_teacher": case_a.get("passed") is True,
        "case_b_unknown_teacher_candidate": case_b.get("passed") is True,
        "case_c_alternative_plan_only": case_c.get("passed") is True,
        "case_d_bad_teacher_reject": case_d.get("passed") is True,
        "case_e_learning_chain": case_e.get("passed") is True,
        "no_real_network": "requests." not in processor and "urllib" not in processor and "fetch(" not in processor,
        "no_existing_runner_mutation": "teacher_adapter" not in runner,
        "provider_routed_via_adapter": "PROVIDER_REGISTRY" in processor and "route_teacher_provider" in processor,
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

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_third_party_teacher_adapter_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    known_limits = [
        "teacher_adapter_planning_only_no_real_api_calls",
        "provider_stubs_are_deterministic_not_production_adapters",
        "no_network",
        "no_runner_invocation",
        "no_fact_write",
        "no_direct_training",
        "does_not_replace_l2_selected_plan_ownership",
        "does_not_replace_l1_scene_ownership",
        "does_not_replace_tool_os",
    ]

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Adapter",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "smoke_cases_passed": flags.get("smoke_cases_passed", False),
        "review_guards_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": known_limits,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_third_party_teacher_adapter_planning_review_v1.json"
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
        "review_guards_passed": r.get("review_guards_passed"),
        "generated_files_count": len(r.get("generated_files", [])),
        "known_limits": r.get("known_limits", []),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
