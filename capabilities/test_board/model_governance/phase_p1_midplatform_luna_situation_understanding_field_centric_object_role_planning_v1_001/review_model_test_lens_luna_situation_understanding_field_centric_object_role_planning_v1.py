# -*- coding: utf-8 -*-
"""P1 Field-Centric Object Role — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-Planning-v1-001"
FC_REL = "capabilities/midplatform/situation_understanding/field_centric/planning"
SU_REL = "capabilities/midplatform/situation_understanding"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_situation_understanding_field_centric_object_role_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{FC_REL}/field_centric_object_role_plan_v1.md",
    f"{FC_REL}/field_centric_object_role_policy_v1.json",
    f"{FC_REL}/field_profiles_v1.py",
    f"{FC_REL}/field_understanding_v1.py",
    f"{FC_REL}/interaction_graph_v1.py",
    f"{FC_REL}/object_role_inference_v1.py",
    f"{FC_REL}/unresolved_object_memory_v1.py",
    f"{FC_REL}/attention_from_field_v1.py",
    f"{FC_REL}/field_centric_adapter_v1.py",
    f"{SU_REL}/luna_situation_understanding_field_centric_object_role_planning_types_v1.py",
    f"{SU_REL}/luna_situation_understanding_field_centric_object_role_planning_processor_v1.py",
    f"{TB_REL}/luna_situation_understanding_field_centric_object_role_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_situation_understanding_field_centric_object_role_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_situation_understanding_field_centric_object_role_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("plan_present", "Field-Centric 规划"),
        ("field_profiles", "Field Profiles"),
        ("field_understanding", "Field Understanding"),
        ("interaction_graph", "Interaction Graph"),
        ("object_role", "Object Role Inference"),
        ("unresolved_memory", "Unresolved Object Memory"),
        ("attention_field", "Attention from Field"),
        ("adapter", "Field-Centric Adapter"),
        ("policy", "Planning Policy"),
        ("field_not_scene", "场非 scene label"),
        ("case_a_role", "Case A 同物不同场"),
        ("case_b_risk", "Case B 同行为不同风险"),
        ("case_c_interaction", "Case C 交互推断"),
        ("case_d_unresolved", "Case D 未解析记忆"),
        ("case_e_attention", "Case E Field+Goal Attention"),
        ("case_f_constrain", "Case F 场约束未知"),
        ("upstream_go", "上游 GO"),
        ("smoke_pass", "smoke 通过"),
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
    plan = _read(f"{FC_REL}/field_centric_object_role_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{FC_REL}/field_centric_object_role_policy_v1.json")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_field_centric_object_role_planning_v1_001.luna_situation_understanding_field_centric_object_role_planning_smoke_v1 import (  # noqa: WPS433
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
        "plan_present": "Field-Centric" in plan and "不是识别世界" in plan,
        "field_profiles": "FIELD_PROFILES" in _read(f"{FC_REL}/field_profiles_v1.py"),
        "field_understanding": "understand_field" in _read(f"{FC_REL}/field_understanding_v1.py"),
        "interaction_graph": "build_interaction_graph" in _read(f"{FC_REL}/interaction_graph_v1.py"),
        "object_role": "infer_object_roles" in _read(f"{FC_REL}/object_role_inference_v1.py"),
        "unresolved_memory": "record_unresolved_objects" in _read(f"{FC_REL}/unresolved_object_memory_v1.py"),
        "attention_field": "allocate_attention_from_field" in _read(f"{FC_REL}/attention_from_field_v1.py"),
        "adapter": "run_field_centric_object_role_planning" in _read(f"{FC_REL}/field_centric_adapter_v1.py"),
        "policy": policy.get("schema_id") == "FieldCentricObjectRolePlanningPolicyV1",
        "field_not_scene": policy.get("field_not_scene_label") is True,
        "case_a_role": _case(cases, "case_a_same_object_different_field_role").get("passed") is True,
        "case_b_risk": _case(cases, "case_b_same_behavior_different_field_risk").get("passed") is True,
        "case_c_interaction": _case(cases, "case_c_unknown_interaction_infers_role").get("passed") is True,
        "case_d_unresolved": _case(cases, "case_d_unknown_no_interaction_unresolved").get("passed") is True,
        "case_e_attention": _case(cases, "case_e_attention_field_goal_not_saliency").get("passed") is True,
        "case_f_constrain": _case(cases, "case_f_field_constrains_unknown_space").get("passed") is True,
        "upstream_go": upstream_ok,
        "smoke_pass": smoke_result.get("final_decision", "").endswith("_GO"),
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_field_centric_object_role_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L1_Field_Understanding",
        "core_principle": "不是识别世界，而是在场中理解世界",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["planning_fixture_only"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_situation_understanding_field_centric_object_role_planning_review_v1.json"
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
