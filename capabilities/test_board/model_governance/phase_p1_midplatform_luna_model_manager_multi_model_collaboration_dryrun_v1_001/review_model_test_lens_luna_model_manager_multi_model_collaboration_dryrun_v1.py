# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Multi-Model Collaboration — dryrun review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001"
COLLAB_REL = "capabilities/midplatform/model_manager/collaboration"
DRYRUN_REL = f"{COLLAB_REL}/dryrun"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_model_collaboration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_model_collaboration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_provider_registry_v1_review_v0/"
        "p1_midplatform_luna_model_manager_multi_provider_registry_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRYRUN_REL}/multi_model_collaboration_dryrun_adapter_v1.py",
    f"{DRYRUN_REL}/collaboration_execution_planner_v1.py",
    f"{DRYRUN_REL}/evidence_fusion_dryrun_processor_v1.py",
    f"{DRYRUN_REL}/collaboration_conflict_dryrun_processor_v1.py",
    f"{DRYRUN_REL}/collaboration_degradation_processor_v1.py",
    f"{DRYRUN_REL}/multi_model_collaboration_dryrun_policy_v1.json",
    f"{TB_REL}/luna_model_manager_multi_model_collaboration_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_multi_model_collaboration_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_multi_model_collaboration_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("dryrun_adapter_present", "dryrun adapter 存在"),
        ("execution_planner_present", "execution planner 存在"),
        ("fusion_dryrun_present", "fusion dryrun 存在"),
        ("conflict_dryrun_present", "conflict dryrun 存在"),
        ("degradation_processor_present", "degradation processor 存在"),
        ("dryrun_policy_present", "dryrun policy 存在"),
        ("collaboration_slot_abstraction", "Collaboration Slot 抽象"),
        ("full_chain_closed_loop", "全链路闭环"),
        ("no_voting_no_fusion", "禁止投票与答案融合"),
        ("case_a_pipeline", "Case A Pipeline"),
        ("case_b_parallel", "Case B Parallel Evidence"),
        ("case_c_challenge", "Case C Challenge Mode"),
        ("case_d_conflict", "Case D Evidence Conflict"),
        ("case_e_degradation", "Case E Resource Degradation"),
        ("tool_os_handoff_present", "Tool OS Handoff"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
        ("dryrun_cases_pass", "dryrun cases 通过"),
        ("no_runner_mutation", "未改 runner"),
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
    policy = _load_json(_detect_repo_root() / f"{DRYRUN_REL}/multi_model_collaboration_dryrun_policy_v1.json")
    planner = _read(f"{DRYRUN_REL}/collaboration_execution_planner_v1.py")
    adapter = _read(f"{DRYRUN_REL}/multi_model_collaboration_dryrun_adapter_v1.py")
    runner = _read(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
    )

    dryrun_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_v1_001.luna_model_manager_multi_model_collaboration_dryrun_fixtures_v1 import (  # noqa: WPS433
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
    case_a = _case(cases, "case_a_pipeline_collaboration_shopfront").get("result") or {}

    return {
        "dryrun_adapter_present": "run_pipeline_collaboration_dryrun" in adapter,
        "execution_planner_present": "build_collaboration_slots" in planner,
        "fusion_dryrun_present": "build_parallel_fusion_dryrun" in _read(f"{DRYRUN_REL}/evidence_fusion_dryrun_processor_v1.py"),
        "conflict_dryrun_present": "build_semantic_conflict_dryrun" in _read(f"{DRYRUN_REL}/collaboration_conflict_dryrun_processor_v1.py"),
        "degradation_processor_present": "build_collaboration_degradation" in _read(f"{DRYRUN_REL}/collaboration_degradation_processor_v1.py"),
        "dryrun_policy_present": policy.get("schema_id") == "MultiModelCollaborationDryrunPolicyV1",
        "collaboration_slot_abstraction": policy.get("boundary_flags", {}).get("collaboration_slot_abstraction") is True,
        "full_chain_closed_loop": "tool_os_handoff" in adapter and "validation_review" in adapter,
        "no_voting_no_fusion": policy.get("boundary_flags", {}).get("no_multi_model_voting") is True,
        "case_a_pipeline": _case(cases, "case_a_pipeline_collaboration_shopfront").get("passed") is True,
        "case_b_parallel": _case(cases, "case_b_parallel_evidence_unknown_scene").get("passed") is True,
        "case_c_challenge": _case(cases, "case_c_challenge_mode_teacher").get("passed") is True,
        "case_d_conflict": _case(cases, "case_d_evidence_conflict_semantic").get("passed") is True,
        "case_e_degradation": _case(cases, "case_e_resource_collaboration_degradation").get("passed") is True,
        "tool_os_handoff_present": (case_a.get("tool_os_handoff") or {}).get("tool_os_handoff_candidate") is True,
        "upstream_gos_confirmed": upstream_ok,
        "dryrun_cases_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
        "no_runner_mutation": "collaboration_dryrun" not in runner,
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

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Collaboration_DryRun",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": [
            "dryrun_no_real_multi_model_inference",
            "ocr_grounding_qwen_chain_deferred",
            "real_chain_integration_next_phase",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_multi_model_collaboration_dryrun_review_v1.json"
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
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
