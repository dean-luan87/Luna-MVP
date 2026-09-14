# -*- coding: utf-8 -*-
"""P1 Ownership Real Runtime Integration — planning review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001"
PLAN_REL = "capabilities/midplatform/model_manager/runtime/mixed_region/ownership_real_runtime/planning"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-DryRun-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{PLAN_REL}/ownership_real_runtime_plan_v1.md",
    f"{PLAN_REL}/ownership_real_runtime_policy_v1.json",
    f"{PLAN_REL}/planning_fixtures_v1.py",
    f"{PLAN_REL}/slot_ownership_discovery_v1.py",
    f"{PLAN_REL}/slot_occlusion_reasoning_v1.py",
    f"{PLAN_REL}/slot_text_owner_assignment_v1.py",
    f"{PLAN_REL}/per_entity_channel_activation_v1.py",
    f"{PLAN_REL}/ownership_evidence_package_v1.py",
    f"{PLAN_REL}/ownership_real_runtime_adapter_v1.py",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_planning_types_v1.py",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_planning_processor_v1.py",
    f"{TB_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_planning_smoke_v1.py",
    f"{TB_REL}/run_luna_model_manager_region_intelligence_ownership_real_runtime_planning_smoke_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_region_intelligence_ownership_real_runtime_planning_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("plan_present", "Real Runtime 规划"),
        ("slot_discovery", "slot_ownership_discovery"),
        ("slot_occlusion", "slot_occlusion_reasoning"),
        ("slot_text_owner", "slot_text_owner_assignment"),
        ("adapter", "Planning Adapter"),
        ("policy", "Planning Policy"),
        ("attention_gated", "Attention-Gated 输入"),
        ("case_a_stacked", "Case A 叠放纸张"),
        ("case_b_shelf", "Case B 货架价签"),
        ("case_c_reflection", "Case C 玻璃反光"),
        ("case_d_blocked", "Case D Attention Blocked"),
        ("case_e_occluded", "Case E 遮挡缺失"),
        ("case_f_runtime", "Case F Runtime 故障"),
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
    plan = _read(f"{PLAN_REL}/ownership_real_runtime_plan_v1.md")
    policy = _load_json(_detect_repo_root() / f"{PLAN_REL}/ownership_real_runtime_policy_v1.json")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_v1_001.luna_model_manager_region_intelligence_ownership_real_runtime_planning_smoke_v1 import (  # noqa: WPS433
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
        "plan_present": "Ownership Real Runtime" in plan and "slot_ownership_discovery" in plan,
        "slot_discovery": "run_slot_ownership_discovery" in _read(f"{PLAN_REL}/slot_ownership_discovery_v1.py"),
        "slot_occlusion": "run_slot_occlusion_reasoning" in _read(f"{PLAN_REL}/slot_occlusion_reasoning_v1.py"),
        "slot_text_owner": "run_slot_text_owner_assignment" in _read(f"{PLAN_REL}/slot_text_owner_assignment_v1.py"),
        "adapter": "run_ownership_real_runtime_planning" in _read(f"{PLAN_REL}/ownership_real_runtime_adapter_v1.py"),
        "policy": policy.get("schema_id") == "OwnershipRealRuntimeIntegrationPlanningPolicyV1",
        "attention_gated": policy.get("boundary_flags", {}).get("attention_gated_input") is True,
        "case_a_stacked": _case(cases, "case_a_stacked_papers_per_owner_ocr").get("passed") is True,
        "case_b_shelf": _case(cases, "case_b_shelf_distinct_owners").get("passed") is True,
        "case_c_reflection": _case(cases, "case_c_glass_reflection_separation").get("passed") is True,
        "case_d_blocked": _case(cases, "case_d_attention_blocked_no_ownership").get("passed") is True,
        "case_e_occluded": _case(cases, "case_e_occluded_title_not_absent").get("passed") is True,
        "case_f_runtime": _case(cases, "case_f_runtime_unavailable_no_fallback").get("passed") is True,
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Region_Intelligence_Ownership_Real_Runtime_Planning",
        "planning_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["planning_fixture_only", "no_real_heavy_vision_models"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_review_v1.json"
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
