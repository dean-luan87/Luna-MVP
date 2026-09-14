# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Multi-Model Collaboration — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"
COLLAB_REL = "capabilities/midplatform/model_manager/collaboration"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_multi_model_collaboration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_provider_registry_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_provider_registry_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_local_model_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_local_model_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{COLLAB_REL}/multi_model_collaboration_plan_v1.md",
    f"{COLLAB_REL}/collaboration_types_v1.py",
    f"{COLLAB_REL}/collaboration_planner_v1.py",
    f"{COLLAB_REL}/evidence_fusion_processor_v1.py",
    f"{COLLAB_REL}/model_conflict_processor_v1.py",
    f"{COLLAB_REL}/collaboration_policy_v1.json",
    f"{COLLAB_REL}/schemas/collaboration_plan_schema.json",
    f"{COLLAB_REL}/schemas/evidence_fusion_schema.json",
    f"{COLLAB_REL}/schemas/conflict_schema.json",
    f"{MM_REL}/luna_model_manager_collaboration_types_v1.py",
    f"{MM_REL}/luna_model_manager_collaboration_processor_v1.py",
    f"{TB_REL}/luna_model_manager_multi_model_collaboration_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_multi_model_collaboration_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_multi_model_collaboration_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("collaboration_plan_present", "协作规划文档"),
        ("collaboration_planner_present", "Collaboration Planner"),
        ("evidence_fusion_present", "Evidence Fusion Processor"),
        ("conflict_processor_present", "Conflict Processor"),
        ("collaboration_policy_present", "Collaboration Policy"),
        ("schemas_present", "Schemas 齐全"),
        ("collaboration_not_competition", "协作≠竞争"),
        ("no_voting", "禁止投票"),
        ("no_auto_answer_fusion", "禁止自动答案融合"),
        ("no_simultaneous_all_models", "禁止全模型同时调用"),
        ("three_collaboration_modes", "三种协作模式"),
        ("case_a_pipeline", "Case A Pipeline"),
        ("case_b_parallel", "Case B Parallel Evidence"),
        ("case_c_conflict", "Case C 模型冲突"),
        ("case_d_degradation", "Case D 资源降级"),
        ("registry_distinct", "Registry 与 Collaboration 分离"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
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
    plan = _read(f"{COLLAB_REL}/multi_model_collaboration_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{COLLAB_REL}/collaboration_policy_v1.json")
    planner_src = _read(f"{COLLAB_REL}/collaboration_planner_v1.py")
    fusion_src = _read(f"{COLLAB_REL}/evidence_fusion_processor_v1.py")
    conflict_src = _read(f"{COLLAB_REL}/model_conflict_processor_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_multi_model_collaboration_planning_v1_001.luna_model_manager_multi_model_collaboration_planning_smoke_v1 import (  # noqa: WPS433
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

    schemas_ok = all(
        _read(f"{COLLAB_REL}/schemas/{name}").strip()
        for name in ("collaboration_plan_schema.json", "evidence_fusion_schema.json", "conflict_schema.json")
    )

    return {
        "collaboration_plan_present": "Multi-Model Collaboration" in plan and "Planning" in plan,
        "collaboration_planner_present": "plan_pipeline_collaboration" in planner_src,
        "evidence_fusion_present": "build_fusion_candidate" in fusion_src,
        "conflict_processor_present": "build_model_conflict_candidate" in conflict_src,
        "collaboration_policy_present": policy.get("schema_id") == "CollaborationPolicyV1",
        "schemas_present": schemas_ok,
        "collaboration_not_competition": policy.get("boundary_flags", {}).get("collaboration_not_competition") is True,
        "no_voting": "no_voting" in policy.get("forbidden", []) or policy.get("boundary_flags", {}).get("collaboration_not_voting") is True,
        "no_auto_answer_fusion": policy.get("boundary_flags", {}).get("no_auto_answer_fusion") is True,
        "no_simultaneous_all_models": policy.get("boundary_flags", {}).get("no_simultaneous_all_models") is True,
        "three_collaboration_modes": len(policy.get("collaboration_modes") or []) >= 3,
        "case_a_pipeline": _case(cases, "case_a_shopfront_pipeline_collaboration").get("passed") is True,
        "case_b_parallel": _case(cases, "case_b_unknown_scene_parallel_evidence").get("passed") is True,
        "case_c_conflict": _case(cases, "case_c_model_conflict_validation").get("passed") is True,
        "case_d_degradation": _case(cases, "case_d_resource_collaboration_degradation").get("passed") is True,
        "registry_distinct": policy.get("boundary_flags", {}).get("registry_distinct_from_collaboration") is True,
        "upstream_gos_confirmed": upstream_ok,
        "smoke_cases_passed": smoke_result.get("final_decision", "").endswith("_GO"),
        "no_runner_mutation": "collaboration_planner" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_model_collaboration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Collaboration_Planning",
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
            "planning_no_real_multi_model_inference",
            "challenge_mode_stub_only",
            "dryrun_deferred_to_next_phase",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_multi_model_collaboration_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
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
