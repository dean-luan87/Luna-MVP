# -*- coding: utf-8 -*-
"""P1 Luna Attention-Gated RI — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Gated-Region-Intelligence-DryRun-v1-001"
DRY_REL = "capabilities/midplatform/situation_understanding/attention_gated_ri/dryrun"
SU_REL = "capabilities/midplatform/situation_understanding"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_situation_understanding_attention_gated_region_intelligence_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_allocation_planning_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_attention_allocation_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRY_REL}/dryrun_goal_profiles_v1.py",
    f"{DRY_REL}/attention_gate_v1.py",
    f"{DRY_REL}/observation_priority_graph_v1.py",
    f"{DRY_REL}/gated_region_intelligence_v1.py",
    f"{DRY_REL}/scene_graph_merger_v1.py",
    f"{DRY_REL}/information_efficiency_score_v1.py",
    f"{DRY_REL}/attention_gated_ri_dryrun_adapter_v1.py",
    f"{DRY_REL}/attention_gated_ri_dryrun_metrics_v1.py",
    f"{DRY_REL}/attention_gated_ri_dryrun_policy_v1.json",
    f"{SU_REL}/luna_situation_understanding_attention_gated_ri_dryrun_types_v1.py",
    f"{SU_REL}/luna_situation_understanding_attention_gated_ri_dryrun_processor_v1.py",
    f"{TB_REL}/luna_situation_understanding_attention_gated_ri_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_situation_understanding_attention_gated_ri_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_situation_understanding_attention_gated_ri_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("attention_gate", "Attention Gate"),
        ("priority_graph", "Observation Priority Graph"),
        ("gated_ri", "Gated Region Intelligence"),
        ("scene_graph", "Scene Graph Merger"),
        ("efficiency_score", "Information Efficiency"),
        ("dryrun_adapter", "DryRun Adapter"),
        ("dryrun_policy", "DryRun Policy"),
        ("attention_controls_not_label", "Attention 是控制系统"),
        ("case_a_gate", "Case A 门控模型"),
        ("case_b_exit_goal", "Case B 找出口"),
        ("case_c_coffee", "Case C 找咖啡店"),
        ("case_d_danger", "Case D 危险评估"),
        ("case_e_scene_graph", "Case E Scene Graph"),
        ("case_f_efficiency", "Case F 效率指标"),
        ("upstream_go", "上游 GO"),
        ("dryrun_pass", "dryrun 通过"),
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
    policy = _load_json(_detect_repo_root() / f"{DRY_REL}/attention_gated_ri_dryrun_policy_v1.json")

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_attention_gated_region_intelligence_dryrun_v1_001.luna_situation_understanding_attention_gated_ri_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        dryrun_result = run_all_dryrun_cases()
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "attention_gate": "apply_attention_gate" in _read(f"{DRY_REL}/attention_gate_v1.py"),
        "priority_graph": "build_observation_priority_graph" in _read(f"{DRY_REL}/observation_priority_graph_v1.py"),
        "gated_ri": "run_gated_region_intelligence" in _read(f"{DRY_REL}/gated_region_intelligence_v1.py"),
        "scene_graph": "merge_scene_graph" in _read(f"{DRY_REL}/scene_graph_merger_v1.py"),
        "efficiency_score": "compute_information_efficiency" in _read(f"{DRY_REL}/information_efficiency_score_v1.py"),
        "dryrun_adapter": "run_attention_gated_ri_dryrun" in _read(f"{DRY_REL}/attention_gated_ri_dryrun_adapter_v1.py"),
        "dryrun_policy": policy.get("schema_id") == "AttentionGatedRegionIntelligenceDryrunPolicyV1",
        "attention_controls_not_label": policy.get("boundary_flags", {}).get("attention_gates_region_intelligence") is True,
        "case_a_gate": _case(cases, "case_a_attention_gate_blocks_models").get("passed") is True,
        "case_b_exit_goal": _case(cases, "case_b_goal_find_exit_budget").get("passed") is True,
        "case_c_coffee": _case(cases, "case_c_goal_find_coffee_shop").get("passed") is True,
        "case_d_danger": _case(cases, "case_d_goal_assess_danger").get("passed") is True,
        "case_e_scene_graph": _case(cases, "case_e_scene_graph_ownership_attention").get("passed") is True,
        "case_f_efficiency": _case(cases, "case_f_information_efficiency_score").get("passed") is True,
        "upstream_go": upstream_ok,
        "dryrun_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "L1_Attention_Gated_Region_Intelligence",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["dryrun_fixture_only", "no_real_perception_models"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_review_v1.json"
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
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
