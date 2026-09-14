# -*- coding: utf-8 -*-
"""Engineering Mainline Roadmap Decision v1.

Route adjudication after Engineering Mainline Resume re-sign. No feature code, smoke, or refactor.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Engineering-Mainline-Roadmap-Decision-v1-001"
DECISION_SCOPE = "engineering_mainline_roadmap_decision_only"
SOURCE_CHAIN = "engineering_mainline_roadmap_decision_v1"

FINAL_DECISION = "ENGINEERING_MAINLINE_ROADMAP_DECISION_READY_FOR_VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Planning-v1-001"
NEXT_TEST_PHASE = "Phase-Post-Migration-Engineering-Smoke-Test-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Engineering-Mainline-Resume-v1-001"
UPSTREAM_REQUIRED_FINAL = "ENGINEERING_MAINLINE_RESUME_READY_FOR_ROADMAP_DECISION"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

SELECTED_ROUTE_ID = "Route A — Vision / OCR / Navigation / Task Midplatform Recovery Roadmap"

ROUTE_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "route_id": "Route A — Vision / OCR / Navigation / Task Midplatform Recovery Roadmap",
        "short_id": "route_a_vision_ocr_navigation_task_recovery",
        "status": "selected",
        "priority_tier": "P0",
        "rationale": "Luna 近期工程价值核心是“看、读、走、理解任务”；感知与任务链应先于语音/情感",
        "modules": ["vision", "ocr", "navigation", "task_midplatform"],
    },
    {
        "route_id": "Route B — Post-Migration Engineering Smoke Test First",
        "short_id": "route_b_smoke_test_first",
        "status": "parallel_next_after_decision",
        "priority_tier": "P1",
        "rationale": "工程 smoke test 单独 phase；可在 recovery planning 前或并行准备，但不替代 Route A",
        "recommended_phase": NEXT_TEST_PHASE,
    },
    {
        "route_id": "Route C — Task Midplatform Structure Cleanup Roadmap",
        "short_id": "route_c_midplatform_cleanup",
        "status": "deferred",
        "priority_tier": "deferred",
        "rationale": "中台是后续重点，但应先建立功能主线与 smoke 基线",
    },
    {
        "route_id": "Route D — Voice Interaction Runtime Roadmap",
        "short_id": "route_d_voice",
        "status": "deferred",
        "priority_tier": "P1",
        "rationale": "依赖任务中台与感知链稳定",
    },
    {
        "route_id": "Route E — Emotional Engine Pre-Runtime Roadmap",
        "short_id": "route_e_emotion",
        "status": "deferred",
        "priority_tier": "P2",
        "rationale": "视觉/OCR/任务链恢复后再接入",
    },
    {
        "route_id": "Route F — Low-Severity Refactor Cleanup",
        "short_id": "route_f_low_severity",
        "status": "deferred",
        "priority_tier": "deferred",
        "rationale": "50 条 low-severity 不阻塞主线恢复",
    },
    {
        "route_id": "Route G — Reserved Stub Implementation",
        "short_id": "route_g_reserved_stub",
        "status": "deferred",
        "priority_tier": "deferred",
        "rationale": "120 stub/placeholder 不在当前恢复阶段实现",
    },
    {
        "route_id": "Route H — Resume Feature Coding Directly",
        "short_id": "route_h_direct_coding",
        "status": "blocked",
        "priority_tier": "blocked",
        "rationale": "禁止无 roadmap / smoke test 直接进入功能实现",
    },
)

MODULE_PRIORITY: Tuple[Tuple[str, str, str], ...] = (
    ("vision", "Vision / 视觉", "P0"),
    ("ocr", "OCR", "P0"),
    ("navigation", "Navigation / 导航", "P0"),
    ("task_midplatform", "Task Midplatform / 任务中台", "P0"),
    ("voice_interaction", "Voice Interaction / 语音交互", "P1"),
    ("world_model_memory", "World Model / Memory read-only lookup", "P1"),
    ("post_migration_smoke_test", "Post-Migration Engineering Smoke Test", "P1"),
    ("emotion_engine", "Emotional Engine pre-runtime planning", "P2"),
    ("low_severity_cleanup", "Low-severity refactor cleanup", "P2"),
    ("reserved_implementation_planning", "Reserved module implementation planning", "P2"),
)

LAYER_PRIORITY: Tuple[Tuple[str, str, List[str]], ...] = (
    ("foundation", "P0", ["能看", "能读", "能定位", "能理解任务"]),
    ("survival", "P0", ["安全", "降级", "异常恢复", "最小可用"]),
    ("enhancement", "P1", ["长期记忆", "场景学习", "世界模型", "个性化", "情感联结"]),
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ feature implementation started",
    "Route A selected ≠ runtime enabled",
    "Midplatform focus deferred ≠ midplatform refactor executed",
    "Smoke test planned ≠ smoke test executed",
    "Low-severity handoff ≠ low-severity fixed",
    "Reserved module handoff ≠ stub implemented",
    "Engineering mainline resume ≠ bypass phase planning",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "engineering_mainline_roadmap_decision_only": True,
        "feature_implementation_started_now": False,
        "smoke_test_executed_now": False,
        "runtime_refactor_executed_now": False,
        "midplatform_refactor_executed_now": False,
        "migration_chain_reopened_now": False,
        "governance_recursion_reopened_now": False,
        "structure_migration_work_continued_now": False,
        "low_severity_candidates_fixed_now": False,
        "reserved_modules_implemented_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "feature_runtime_enabled_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def run_engineering_mainline_roadmap_decision_v1(
    *,
    engineering_mainline_resume_root: str,
    post_migration_engineering_state_sync_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    resume_root = Path(engineering_mainline_resume_root).expanduser().resolve()
    sync_root = (
        Path(post_migration_engineering_state_sync_root).expanduser().resolve()
        if post_migration_engineering_state_sync_root
        else resume_root.parent / "post_migration_engineering_state_sync"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(resume_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_resume_root": str(resume_root),
    }

    resume_sm = _try_read_json(resume_root / "summary.json") or {}
    resume_vr = _try_read_json(resume_root / "verifier_report.json") or {}
    resume_decision = _try_read_json(resume_root / "engineering_mainline_resume_decision_v1.json") or {}
    focus = _try_read_json(resume_root / "engineering_focus_module_matrix_v1.json") or {}
    deferred = _try_read_json(resume_root / "deferred_registers_handoff_v1.json") or {}
    test_handoff = _try_read_json(resume_root / "engineering_resume_test_handoff_v1.json") or {}
    sync_review = _try_read_json(resume_root / "post_migration_state_sync_input_review_v1.json") or {}

    if resume_vr.get("verifier") != "GO" or resume_vr.get("passed") is not True:
        blockers.append("resume verifier must be GO")
    if resume_sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("resume phase mismatch")
    if resume_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("resume final_decision mismatch")
    if resume_sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("resume recommended_next_phase mismatch")
    if resume_sm.get("boundary_ok") is not True:
        blockers.append("resume boundary_ok must be true")
    if resume_sm.get("resume_resign_after_state_sync") is not True:
        blockers.append("resume_resign_after_state_sync must be true")
    if resume_sm.get("state_sync_upstream_confirmed") is not True:
        blockers.append("state_sync_upstream_confirmed must be true")
    if resume_sm.get("migration_chain_reopened_now") is True:
        blockers.append("migration_chain_reopened_now must be false")
    if resume_sm.get("structure_migration_work_continued_now") is True:
        blockers.append("structure_migration_work_continued_now must be false")
    if resume_sm.get("feature_runtime_enabled_now") is True:
        blockers.append("feature_runtime_enabled_now must be false")
    if resume_sm.get("smoke_test_executed_now") is True:
        blockers.append("smoke_test_executed_now must be false")

    resume_input_trusted = resume_sm.get("boundary_ok") is True and not blockers
    route_b_override = False

    boundary_ok = not blockers

    resume_input_review = {
        "review_id": "engineering_mainline_resume_input_review_v1",
        "upstream_root": str(resume_root),
        "upstream_verifier": resume_vr.get("verifier"),
        "upstream_final_decision": resume_sm.get("final_decision"),
        "resume_resign_after_state_sync": resume_sm.get("resume_resign_after_state_sync"),
        "state_sync_upstream_confirmed": resume_sm.get("state_sync_upstream_confirmed"),
        "migration_chain_closed": resume_sm.get("migration_chain_closed_now"),
        "low_severity_count": deferred.get("low_severity", {}).get("count"),
        "reserved_module_count": deferred.get("reserved_modules", {}).get("count"),
        "resume_input_trusted": resume_input_trusted,
        "review_pass": resume_input_trusted,
        **meta,
    }

    module_matrix = {
        "matrix_id": "feature_module_priority_matrix_v1",
        "modules": [
            {"module_id": mid, "label": label, "priority_tier": tier, "selected_route_alignment": SELECTED_ROUTE_ID}
            for mid, label, tier in MODULE_PRIORITY
        ],
        "p0_modules": [m[0] for m in MODULE_PRIORITY if m[2] == "P0"],
        "deferred_modules": [m[0] for m in MODULE_PRIORITY if m[2] in ("P2", "deferred")],
        **meta,
    }

    layer_matrix = {
        "matrix_id": "capability_layer_priority_matrix_v1",
        "layers": [{"layer_id": lid, "priority_tier": tier, "focus_capabilities": caps} for lid, tier, caps in LAYER_PRIORITY],
        **meta,
    }

    midplatform_review = {
        "review_id": "midplatform_focus_readiness_review_v1",
        "status": "deferred_not_selected",
        "rationale": "Route C deferred；中台整理在功能主线与 smoke 基线后推进",
        "midplatform_refactor_executed_now": False,
        "priority_direction_from_resume": (
            deferred.get("midplatform_structure", {}).get("priority_directions") or []
        ),
        "review_pass": True,
        **meta,
    }

    smoke_route_review = {
        "review_id": "post_migration_smoke_test_route_review_v1",
        "route_b_status": "parallel_next_after_decision",
        "not_selected_as_primary_route": True,
        "recommended_parallel_or_next_test_phase": NEXT_TEST_PHASE,
        "smoke_test_executed_now": False,
        "execution_sequence_note": "建议先完成 Roadmap Decision，再执行 Smoke Test，再进入 Recovery Planning dry-run",
        "resume_input_requires_smoke_before_coding": resume_input_trusted,
        "route_b_selected_only_if_resume_untrusted": route_b_override,
        **meta,
    }

    route_matrix = {
        "matrix_id": "roadmap_route_matrix_v1",
        "routes": list(ROUTE_CANDIDATES),
        "selected_route_id": SELECTED_ROUTE_ID if boundary_ok else None,
        "blocked_routes": [r["route_id"] for r in ROUTE_CANDIDATES if r.get("status") == "blocked"],
        "deferred_routes": [r["route_id"] for r in ROUTE_CANDIDATES if r.get("status") == "deferred"],
        **meta,
    }

    selected_route = {
        "selected_route_id": SELECTED_ROUTE_ID,
        "short_id": "route_a_vision_ocr_navigation_task_recovery",
        "status": "selected",
        "modules": ["vision", "ocr", "navigation", "task_midplatform"],
        "goal": "把“看、读、走、理解任务”重新拉回功能工程主线",
        "final_decision": FINAL_DECISION if boundary_ok else "ENGINEERING_MAINLINE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "recommended_parallel_or_next_test_phase": NEXT_TEST_PHASE,
        "execution_order_note": "Roadmap Decision → Smoke Test（建议）→ Recovery Planning dry-run",
        **meta,
    }

    policy = {
        "policy_id": "engineering_mainline_roadmap_decision_policy_v1",
        "scope": DECISION_SCOPE,
        "mode": "route_adjudication_only",
        "primary_upstream": UPSTREAM_REQUIRED_PHASE,
        **meta,
    }

    non_claims = {
        "register_id": "roadmap_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "selected_route_id": SELECTED_ROUTE_ID if boundary_ok else None,
        "resume_input_trusted": resume_input_trusted,
        "final_decision": selected_route.get("final_decision"),
        "recommended_next_phase": selected_route.get("recommended_next_phase"),
        "recommended_parallel_or_next_test_phase": NEXT_TEST_PHASE,
        **meta,
    }

    return {
        "summary": summary,
        "engineering_mainline_roadmap_decision_policy": policy,
        "engineering_mainline_resume_input_review": resume_input_review,
        "feature_module_priority_matrix": module_matrix,
        "capability_layer_priority_matrix": layer_matrix,
        "midplatform_focus_readiness_review": midplatform_review,
        "post_migration_smoke_test_route_review": smoke_route_review,
        "roadmap_route_matrix": route_matrix,
        "selected_route_decision": selected_route,
        "roadmap_non_claims_register": non_claims,
    }
