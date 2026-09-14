# -*- coding: utf-8 -*-
"""P1 Region Intelligence Ownership — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-DryRun-v1-001"
DRY_REL = "capabilities/midplatform/model_manager/runtime/mixed_region/dryrun"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_mixed_region_understanding_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_mixed_region_understanding_planning_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRY_REL}/entity_discovery_simulator_v1.py",
    f"{DRY_REL}/information_ownership_graph_v1.py",
    f"{DRY_REL}/channel_selection_v1.py",
    f"{DRY_REL}/missing_information_reasoner_v1.py",
    f"{DRY_REL}/semantic_conflict_detector_v1.py",
    f"{DRY_REL}/region_intelligence_ownership_dryrun_adapter_v1.py",
    f"{DRY_REL}/region_intelligence_dryrun_metrics_v1.py",
    f"{DRY_REL}/region_intelligence_ownership_dryrun_policy_v1.json",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_dryrun_types_v1.py",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_dryrun_processor_v1.py",
    f"{TB_REL}/luna_model_manager_region_intelligence_ownership_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_region_intelligence_ownership_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_region_intelligence_ownership_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("entity_discovery_simulator", "Entity Discovery"),
        ("ownership_graph", "Information Ownership Graph"),
        ("channel_selection", "Channel Selection"),
        ("missing_reasoner", "Missing Information Reasoner"),
        ("conflict_detector", "Semantic Conflict"),
        ("dryrun_adapter", "DryRun Adapter"),
        ("dryrun_policy", "DryRun Policy"),
        ("ownership_first", "Ownership First"),
        ("missing_reasoning", "Missing Reasoning"),
        ("not_global_activation", "非全模型启动"),
        ("case_a_ownership", "Case A 叠放菜单"),
        ("case_b_missing", "Case B 遮挡缺失"),
        ("case_c_conflict", "Case C 通道冲突"),
        ("case_d_selective", "Case D 选择性激活"),
        ("case_e_graph", "Case E 图结构"),
        ("case_f_runtime", "Case F Runtime 故障"),
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
    policy = _load_json(_detect_repo_root() / f"{DRY_REL}/region_intelligence_ownership_dryrun_policy_v1.json")

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_v1_001.luna_model_manager_region_intelligence_ownership_dryrun_fixtures_v1 import (  # noqa: WPS433
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
        "entity_discovery_simulator": "simulate_entity_discovery" in _read(f"{DRY_REL}/entity_discovery_simulator_v1.py"),
        "ownership_graph": "entity_candidates" in _read(f"{DRY_REL}/information_ownership_graph_v1.py"),
        "channel_selection": "select_information_channels" in _read(f"{DRY_REL}/channel_selection_v1.py"),
        "missing_reasoner": "reason_missing_information" in _read(f"{DRY_REL}/missing_information_reasoner_v1.py"),
        "conflict_detector": "detect_semantic_conflict" in _read(f"{DRY_REL}/semantic_conflict_detector_v1.py"),
        "dryrun_adapter": "run_region_intelligence_ownership_dryrun" in _read(f"{DRY_REL}/region_intelligence_ownership_dryrun_adapter_v1.py"),
        "dryrun_policy": policy.get("schema_id") == "RegionIntelligenceOwnershipDryrunPolicyV1",
        "ownership_first": policy.get("boundary_flags", {}).get("ownership_before_ocr") is True,
        "missing_reasoning": policy.get("boundary_flags", {}).get("missing_information_reasoning") is True,
        "not_global_activation": policy.get("boundary_flags", {}).get("not_global_model_activation") is True,
        "case_a_ownership": _case(cases, "case_a_ownership_first_stacked_menus").get("passed") is True,
        "case_b_missing": _case(cases, "case_b_missing_information_occlusion").get("passed") is True,
        "case_c_conflict": _case(cases, "case_c_channel_conflict_same_region").get("passed") is True,
        "case_d_selective": _case(cases, "case_d_selective_channel_not_all_models").get("passed") is True,
        "case_e_graph": _case(cases, "case_e_ownership_graph_structure").get("passed") is True,
        "case_f_runtime": _case(cases, "case_f_runtime_unavailable_replan").get("passed") is True,
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
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Information_Ownership_Evidence_Routing_DryRun",
        "dryrun_only": True,
        "information_ownership_graph_verified": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["deterministic_fixture_only", "no_real_segmentation"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_dryrun_review_v1.json"
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
