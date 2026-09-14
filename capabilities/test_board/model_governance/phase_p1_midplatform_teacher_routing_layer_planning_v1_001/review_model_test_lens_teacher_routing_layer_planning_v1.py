# -*- coding: utf-8 -*-
"""P1 Teacher Routing Layer — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Teacher-Routing-Layer-Planning-v1-001"
TR_REL = "capabilities/midplatform/teacher_routing"
TB_REL = "capabilities/test_board/model_governance/phase_p1_midplatform_teacher_routing_layer_planning_v1_001"

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO": (
        "_tmp_eval_out/p1_midplatform_teacher_performance_evaluation_v1_review_v0/"
        "p1_midplatform_teacher_performance_evaluation_review_v1.json"
    ),
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO": (
        "_tmp_eval_out/p1_midplatform_single_teacher_qwen_vl_real_provider_integration_v1_review_v0/"
        "p1_midplatform_single_teacher_qwen_vl_real_provider_integration_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Multi-Teacher-Validation-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{TR_REL}/teacher_routing_plan_v1.md",
    f"{TR_REL}/luna_teacher_routing_types_v1.py",
    f"{TR_REL}/teacher_capability_registry_v1.json",
    f"{TR_REL}/teacher_routing_policy_v1.json",
    f"{TR_REL}/teacher_routing_processor_v1.py",
    f"{TR_REL}/__init__.py",
    f"{TB_REL}/luna_teacher_routing_layer_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_teacher_routing_layer_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_teacher_routing_layer_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("routing_plan_present", "routing 规划文档"),
        ("types_present", "types 存在"),
        ("capability_registry_present", "Teacher Capability Registry"),
        ("routing_policy_present", "Teacher Routing Policy"),
        ("routing_processor_present", "routing processor"),
        ("route_teacher_request_api", "route_teacher_request API"),
        ("no_multi_teacher_voting", "禁止多模型投票"),
        ("router_before_adapter", "Router 在 Adapter 之前"),
        ("no_teacher_execution", "不执行 Teacher"),
        ("no_tool_execution", "不执行 Tool"),
        ("no_fact_write", "不写 fact"),
        ("no_plan_override", "不覆盖 plan"),
        ("no_scene_override", "不覆盖 scene"),
        ("case_a_shopfront_ocr", "Case A 店招 OCR"),
        ("case_b_unknown_qwen", "Case B unknown Qwen"),
        ("case_c_multi_candidate", "Case C 多 Teacher 候选"),
        ("case_d_precise_ocr", "Case D 精确 OCR"),
        ("future_multi_teacher_ready", "多 Teacher 预留"),
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
    plan = _read(f"{TR_REL}/teacher_routing_plan_v1.md")
    types_py = _read(f"{TR_REL}/luna_teacher_routing_types_v1.py")
    registry = _load_json(f"{TR_REL}/teacher_capability_registry_v1.json")
    policy = _load_json(f"{TR_REL}/teacher_routing_policy_v1.json")
    processor = _read(f"{TR_REL}/teacher_routing_processor_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )
    flags = policy.get("boundary_flags", {})

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_teacher_routing_layer_planning_v1_001.luna_teacher_routing_layer_planning_smoke_v1 import (  # noqa: WPS433
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
        "routing_plan_present": "Teacher Router" in plan and "教师选择" in plan,
        "types_present": "ROUTE_TYPES" in types_py,
        "capability_registry_present": bool(registry.get("teachers")),
        "routing_policy_present": bool(policy.get("routing_rules")),
        "routing_processor_present": "route_teacher_request" in processor,
        "route_teacher_request_api": "def route_teacher_request" in processor,
        "no_multi_teacher_voting": flags.get("no_multi_teacher_voting") is True and smoke_result.get("no_multi_teacher_voting") is True,
        "router_before_adapter": flags.get("router_before_adapter") is True,
        "no_teacher_execution": flags.get("no_teacher_execution") is True and "no_teacher_execution" in processor,
        "no_tool_execution": flags.get("no_tool_execution") is True,
        "no_fact_write": flags.get("no_fact_write") is True,
        "no_plan_override": "does_not_override_l2_plan" in processor,
        "no_scene_override": "does_not_override_l1_scene" in processor,
        "case_a_shopfront_ocr": _case(cases, "case_a_shopfront_ocr_not_qwen").get("passed") is True,
        "case_b_unknown_qwen": _case(cases, "case_b_unknown_scene_qwen_vl").get("passed") is True,
        "case_c_multi_candidate": _case(cases, "case_c_complex_multi_teacher_candidate").get("passed") is True,
        "case_d_precise_ocr": _case(cases, "case_d_precise_ocr_tool_route").get("passed") is True,
        "future_multi_teacher_ready": "teacher_multi_candidate" in processor and "gpt_vision" in _read(f"{TR_REL}/teacher_capability_registry_v1.json"),
        "no_existing_runner_mutation": "teacher_routing" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_teacher_routing_layer_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Teacher_Router",
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
        "known_limits": [
            "planning_only_deterministic_routing",
            "no_real_teacher_invocation",
            "multi_teacher_sequential_candidate_only",
            "no_voting_arbitration_yet",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_teacher_routing_layer_planning_review_v1.json"
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
