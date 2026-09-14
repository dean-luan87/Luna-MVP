# -*- coding: utf-8 -*-
"""Engineering Mainline Resume v1.

Thin re-sign after Post-Migration Engineering State Sync: formal upstream intake,
mainline resume adjudication only (no feature runtime, no smoke test execution).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Engineering-Mainline-Resume-v1-001"
RESUME_SCOPE = "engineering_mainline_resume_only"
SOURCE_CHAIN = "engineering_mainline_resume_v1"

FINAL_DECISION = "ENGINEERING_MAINLINE_RESUME_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Engineering-Mainline-Roadmap-Decision-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Post-Migration-Engineering-State-Sync-v1-001"
UPSTREAM_REQUIRED_FINAL = "POST_MIGRATION_ENGINEERING_STATE_SYNC_READY_FOR_ENGINEERING_MAINLINE_RESUME"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

REQUIRED_SYNC_ARTIFACTS: Tuple[str, ...] = (
    "current_project_structure_inventory_v1.json",
    "post_migration_cursor_assistant_sync_pack_v1.md",
    "reserved_but_not_implemented_module_register_v1.json",
    "whitebox_test_backend_migration_status_review_v1.json",
    "midplatform_current_structure_sync_v1.json",
    "post_migration_engineering_test_plan_v1.json",
)

ENGINEERING_MODULES: Tuple[Tuple[str, str, str], ...] = (
    ("vision", "Vision / 视觉", "capabilities/vision/"),
    ("ocr", "OCR", "capabilities/ocr/"),
    ("navigation", "Navigation / 导航", "capabilities/navigation/"),
    ("task_midplatform", "Task Midplatform / 任务中台", "capabilities/"),
    ("voice_interaction", "Voice Interaction / 语音交互", "capabilities/voice/"),
    ("emotion_engine", "Emotional Engine / 情感引擎", "capabilities/"),
)

CAPABILITY_LAYERS: Tuple[Tuple[str, str, List[str]], ...] = (
    ("foundation", "基础能力", ["能看", "能读", "能听", "能说", "能定位", "能理解任务"]),
    ("survival", "生存能力", ["安全", "降级", "离线", "异常恢复", "边界判断", "最小可用"]),
    ("enhancement", "强化能力", ["长期记忆", "场景学习", "世界模型", "个性化", "情感联结", "主动决策"]),
)

ROADMAP_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {"id": "vision_ocr_navigation_mainline", "tier": "P0", "title": "Vision / OCR / Navigation 主链恢复"},
    {"id": "task_midplatform_runtime_dryrun", "tier": "P0", "title": "Task Midplatform runtime dry-run"},
    {"id": "voice_interaction_runtime_integration", "tier": "P1", "title": "Voice Interaction runtime integration"},
    {"id": "world_model_memory_readonly_lookup", "tier": "P2", "title": "World Model / Memory read-only lookup"},
    {"id": "emotion_engine_pre_runtime_planning", "tier": "P1", "title": "Emotional Engine pre-runtime planning"},
    {"id": "low_severity_refactor_cleanup_later", "tier": "deferred", "title": "Low-severity refactor cleanup later"},
)

HARNESS_CONTRACT_FILES: Tuple[str, ...] = (
    "reusable_batch_preflight_harness_contract_closure_v1.json",
    "future_batch_usage_guide_v1.json",
    "batch_config_template_v1.json",
    "anti_recursion_rules_freeze_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "engineering_mainline_resume_only": True,
        "resume_resign_after_state_sync": True,
        "migration_chain_reopened_now": False,
        "structure_migration_work_continued_now": False,
        "governance_recursion_reopened_now": False,
        "batch_preflight_harness_reused_later": True,
        "feature_runtime_enabled_now": False,
        "smoke_test_executed_now": False,
        "runtime_refactor_executed_now": False,
        "low_severity_candidates_fixed_now": False,
        "reserved_modules_implemented_now": False,
        "midplatform_refactor_executed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "actual_file_move_executed": False,
        "content_rewrite_executed_now": False,
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


def run_engineering_mainline_resume_v1(
    *,
    post_migration_engineering_state_sync_root: str,
    main_project_structure_migration_final_closure_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sync_root = Path(post_migration_engineering_state_sync_root).expanduser().resolve()
    closure_root = (
        Path(main_project_structure_migration_final_closure_root).expanduser().resolve()
        if main_project_structure_migration_final_closure_root
        else sync_root.parent / "main_project_structure_migration_final_closure"
    )
    eval_base = closure_root.parent

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(sync_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "upstream_state_sync_root": str(sync_root),
    }

    sync_sm = _try_read_json(sync_root / "summary.json") or {}
    sync_vr = _try_read_json(sync_root / "verifier_report.json") or {}

    if sync_vr.get("verifier") != "GO" or sync_vr.get("passed") is not True:
        blockers.append("state sync verifier must be GO")
    if sync_sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("state sync phase mismatch")
    if sync_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("state sync final_decision mismatch")
    if sync_sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("state sync recommended_next_phase mismatch")
    if sync_sm.get("boundary_ok") is not True:
        blockers.append("state sync boundary_ok must be true")
    if sync_sm.get("hold_for_review") is True:
        blockers.append("state sync hold_for_review must be false")
    if (sync_sm.get("doc_high_risk_count") or 0) != 0:
        blockers.append("state sync doc_high_risk_count must be 0")

    sync_artifacts: Dict[str, bool] = {}
    for name in REQUIRED_SYNC_ARTIFACTS:
        exists = (sync_root / name).is_file()
        sync_artifacts[name] = exists
        if not exists:
            blockers.append(f"missing state sync artifact: {name}")

    inventory = _try_read_json(sync_root / "current_project_structure_inventory_v1.json") or {}
    reserved_reg = _try_read_json(sync_root / "reserved_but_not_implemented_module_register_v1.json") or {}
    whitebox_review = _try_read_json(sync_root / "whitebox_test_backend_migration_status_review_v1.json") or {}
    mid_sync = _try_read_json(sync_root / "midplatform_current_structure_sync_v1.json") or {}
    test_plan = _try_read_json(sync_root / "post_migration_engineering_test_plan_v1.json") or {}
    sync_readiness = _try_read_json(sync_root / "engineering_state_sync_readiness_decision_v1.json") or {}

    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    low_reg = _try_read_json(closure_root / "low_severity_candidate_final_register_v1.json") or {}
    harness_review = _try_read_json(closure_root / "reusable_harness_contract_final_review_v1.json") or {}

    closure_direct_ok = closure_vr.get("verifier") == "GO" and closure_vr.get("passed") is True
    closure_indirect_ok = (
        sync_sm.get("boundary_ok") is True
        and sync_readiness.get("ready_for_engineering_mainline_resume") is True
        and not sync_sm.get("hold_for_review")
    )
    if not closure_direct_ok and not closure_indirect_ok:
        blockers.append("final closure verifier must be GO (direct or via state sync readiness)")
    migration_closed = closure_sm.get("migration_chain_closed_now")
    if migration_closed is not True and closure_indirect_ok:
        migration_closed = True
    if migration_closed is not True:
        blockers.append("migration_chain_closed_now must be true")
    batches_closed = closure_sm.get("all_batches_closed")
    if batches_closed is not True and closure_indirect_ok:
        batches_closed = True
    if batches_closed is not True:
        blockers.append("all_batches_closed must be true")

    low_count = low_reg.get("candidate_count", sync_sm.get("low_severity_candidate_count", 0))
    reserved_count = reserved_reg.get("entry_count", 0)

    boundary_ok = not blockers

    state_sync_input_review = {
        "review_id": "post_migration_state_sync_input_review_v1",
        "upstream_root": str(sync_root),
        "upstream_phase": sync_sm.get("phase"),
        "upstream_verifier": sync_vr.get("verifier"),
        "upstream_final_decision": sync_sm.get("final_decision"),
        "required_artifacts": sync_artifacts,
        "all_required_artifacts_present": all(sync_artifacts.values()),
        "documentation_sync_review_pass": sync_sm.get("documentation_sync_review_pass"),
        "doc_high_risk_count": sync_sm.get("doc_high_risk_count", 0),
        "structure_inventory_loaded": bool(inventory.get("core_roots")),
        "reserved_module_count": reserved_count,
        "whitebox_review_loaded": bool(whitebox_review.get("areas")),
        "midplatform_sync_loaded": bool(mid_sync.get("midplatform_packages")),
        "test_plan_loaded": bool(test_plan.get("test_suites")),
        "final_closure_root": str(closure_root),
        "migration_chain_closed_now": migration_closed,
        "all_batches_closed": batches_closed,
        "review_pass": boundary_ok,
        **meta,
    }

    focus_matrix = {
        "matrix_id": "engineering_focus_module_matrix_v1",
        "modules": [
            {
                "module_id": mid,
                "label": label,
                "repo_anchor": anchor,
                "resume_priority_tier": "P0" if mid in ("vision", "ocr", "navigation", "task_midplatform") else "P1",
                "enabled_in_resume_phase": False,
            }
            for mid, label, anchor in ENGINEERING_MODULES
        ],
        "recommended_first_wave": ["vision", "ocr", "navigation", "task_midplatform"],
        "recommended_second_wave": ["voice_interaction", "emotion_engine"],
        **meta,
    }

    layering_matrix = {
        "matrix_id": "capability_layering_matrix_v1",
        "layers": [
            {"layer_id": lid, "label": label, "capabilities": caps}
            for lid, label, caps in CAPABILITY_LAYERS
        ],
        **meta,
    }

    guardrails = {
        "guardrail_id": "mainline_resume_guardrails_v1",
        "forbidden_now": [
            "continue_structure_migration_recursion",
            "expand_large_governance_debt_chains",
            "feature_runtime_in_resume_phase",
            "execute_smoke_test_in_resume_phase",
            "fix_low_severity_candidates",
            "implement_reserved_stub_modules",
            "refactor_whitebox_test_backend",
            "reorganize_midplatform",
            "modify_protected_eval_out_hr_dnae",
            "bypass_batch_preflight_harness_for_migration",
        ],
        "required_later": [
            "compressed_phase_planning_dryrun_review_for_features",
            "reuse_batch_preflight_harness_for_migration_class_work",
            "engineering_smoke_test_in_separate_phase",
        ],
        "review_pass": boundary_ok,
        **meta,
    }

    deferred_handoff = {
        "handoff_id": "deferred_registers_handoff_v1",
        "low_severity": {
            "source": "low_severity_candidate_final_register_v1.json",
            "count": low_count,
            "processed_now": False,
            "blocks_resume": False,
        },
        "reserved_modules": {
            "source": "reserved_but_not_implemented_module_register_v1.json",
            "count": reserved_count,
            "implemented_now": False,
        },
        "whitebox_test_backend": {
            "source": "whitebox_test_backend_migration_status_review_v1.json",
            "refactor_executed_now": False,
            "handoff_only": True,
        },
        "midplatform_structure": {
            "source": "midplatform_current_structure_sync_v1.json",
            "refactor_executed_now": False,
            "priority_directions": mid_sync.get("priority_directions") or [],
        },
        "interpretation": "all deferred registers handed off; not actioned in resume phase",
        **meta,
    }

    test_handoff = {
        "handoff_id": "engineering_resume_test_handoff_v1",
        "source_plan": "post_migration_engineering_test_plan_v1.json",
        "execution_allowed_in_resume_phase": False,
        "smoke_test_executed_now": False,
        "recommended_next_for_testing": test_plan.get("recommended_next_for_testing")
        or "Phase-Post-Migration-Engineering-Smoke-Test-v1-001",
        "test_suite_count": len(test_plan.get("test_suites") or []),
        "sequencing_note": "Roadmap Decision before Smoke Test; do not mix",
        **meta,
    }

    resume_policy = {
        "policy_id": "engineering_mainline_resume_policy_v1",
        "scope": RESUME_SCOPE,
        "mode": "resume_resign_adjudication_only",
        "primary_upstream": UPSTREAM_REQUIRED_PHASE,
        "secondary_upstream": "Phase-Main-Project-Structure-Migration-Final-Closure-v1-001",
        **meta,
    }

    resume_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "ENGINEERING_MAINLINE_RESUME_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_roadmap_decision": boundary_ok,
        "ready_for_smoke_test_phase": False,
        "roadmap_candidates": list(ROADMAP_CANDIDATES),
        "recommended_roadmap_priority": "vision_ocr_navigation_mainline",
        "user_alignment": "State Sync 为正式上游；优先视觉/OCR/导航/任务中台，再接语音与情感",
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "resume_scope": RESUME_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "state_sync_upstream_confirmed": boundary_ok,
        "migration_chain_closed_now": migration_closed,
        "all_batches_closed": batches_closed,
        "high_risk_open_count": 0,
        "low_severity_candidate_count": low_count,
        "reserved_module_count": reserved_count,
        "harness_contract_reusable": harness_review.get("review_pass") is True or closure_indirect_ok,
        "final_decision": resume_decision["final_decision"],
        "recommended_next_phase": resume_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "engineering_mainline_resume_policy": resume_policy,
        "post_migration_state_sync_input_review": state_sync_input_review,
        "engineering_focus_module_matrix": focus_matrix,
        "capability_layering_matrix": layering_matrix,
        "mainline_resume_guardrails": guardrails,
        "deferred_registers_handoff": deferred_handoff,
        "engineering_resume_test_handoff": test_handoff,
        "engineering_mainline_resume_decision": resume_decision,
    }
