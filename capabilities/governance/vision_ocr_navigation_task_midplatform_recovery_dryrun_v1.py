# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Midplatform Recovery DryRun v1.

Simulated consumption of recovery planning artifacts. Dry-run only; no runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-DryRun-v1-001"
DRYRUN_SCOPE = "recovery_dryrun_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_midplatform_recovery_dryrun_v1"

UPSTREAM_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING_READY_FOR_DRYRUN"
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-DryRun-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Post-DryRun-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Recovery DryRun GO ≠ feature implementation started",
    "Recovery DryRun GO ≠ runtime enabled",
    "Vision dry-run pass ≠ camera invoked",
    "OCR dry-run pass ≠ OCR provider invoked",
    "Navigation dry-run pass ≠ navigation action triggered",
    "Task Midplatform dry-run pass ≠ task manager committed",
    "Dependency matrix pass ≠ WorldModel write allowed",
    "Midplatform risk registered ≠ midplatform refactored",
    "Stub registered ≠ stub implemented",
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "camera_runtime_enabled_now",
    "vision_model_invoked_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_manager_committed_now",
    "task_state_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)

REQUIRED_DEPENDENCY_RULES: Tuple[str, ...] = (
    "Vision 是 Navigation / OCR task trigger 的上游之一",
    "OCR 是任务型辅助能力，不是世界模型默认主通道",
    "Navigation 依赖视觉安全评估、任务状态、只读地图上下文",
    "Task Midplatform 负责状态、生命周期、guidance candidate，不直接执行 runtime action",
    "Voice / Emotion 暂为 P1/P2，下游接入",
)

POST_DRYRUN_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "minimal_recovery_execution_planning",
        "phase_id": "Phase-Vision-OCR-Navigation-Task-Minimal-Recovery-Execution-Planning-v1-001",
        "label": "Vision-OCR-Nav-Task Minimal Recovery Execution Planning",
        "priority": "P0",
        "recommendation": "preferred_if_dryrun_no_high_risk",
    },
    {
        "candidate_id": "midplatform_cleanup_planning",
        "phase_id": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001",
        "label": "Midplatform Structure Cleanup Planning",
        "priority": "P1",
        "recommendation": "deferred_parallel",
    },
    {
        "candidate_id": "post_recovery_minimal_smoke",
        "phase_id": "Phase-Post-Recovery-Minimal-Smoke-v1-001",
        "label": "Post-Recovery Minimal Smoke",
        "priority": "P1",
        "recommendation": "after_minimal_execution_planning",
    },
    {
        "candidate_id": "voice_integration_planning",
        "phase_id": "Phase-Voice-Interaction-Runtime-Integration-Planning-v1-001",
        "label": "Voice Interaction Runtime Integration Planning",
        "priority": "P1",
        "recommendation": "deferred",
    },
    {
        "candidate_id": "emotion_pre_runtime_planning",
        "phase_id": "Phase-Emotional-Engine-Pre-Runtime-Planning-v1-001",
        "label": "Emotional Engine Pre-Runtime Planning",
        "priority": "P2",
        "recommendation": "deferred",
    },
)

PLANNING_REQUIRED_FILES: Tuple[str, ...] = (
    "recovery_planning_policy_v1.json",
    "p0_function_chain_inventory_v1.json",
    "vision_recovery_scope_planning_v1.json",
    "ocr_recovery_scope_planning_v1.json",
    "navigation_recovery_scope_planning_v1.json",
    "task_midplatform_recovery_scope_planning_v1.json",
    "vision_ocr_navigation_task_dependency_matrix_v1.json",
    "recovery_runtime_boundary_matrix_v1.json",
    "midplatform_structure_risk_register_v1.json",
    "recovery_phase_sequence_plan_v1.json",
    "recovery_planning_readiness_decision_v1.json",
    "summary.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "recovery_dryrun_only": True,
        "simulated": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "vision_model_invoked_now": False,
        "ocr_runtime_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_runtime_enabled_now": False,
        "navigation_action_triggered_now": False,
        "task_midplatform_runtime_enabled_now": False,
        "task_manager_committed_now": False,
        "task_state_committed_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "midplatform_refactor_executed_now": False,
        "low_severity_candidates_fixed_now": False,
        "reserved_modules_implemented_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _consume_inventory(inventory: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    chains = inventory.get("chains") or []
    if len(chains) < 4:
        issues.append(
            {
                "issue_id": "inventory_missing_chains",
                "severity": "high",
                "detail": f"expected 4 chains, got {len(chains)}",
            }
        )
    chain_summaries: List[Dict[str, Any]] = []
    for chain in chains:
        cid = chain.get("chain_id")
        counts = chain.get("classification_counts") or {}
        entry_count = chain.get("entry_count", 0)
        if entry_count == 0:
            issues.append(
                {
                    "issue_id": f"inventory_empty:{cid}",
                    "severity": "high",
                    "detail": "chain has zero entries",
                }
            )
        unknown = counts.get("unknown", 0)
        stub = counts.get("stub_placeholder", 0)
        if unknown > 0 or stub > 0:
            issues.append(
                {
                    "issue_id": f"inventory_non_blocking:{cid}",
                    "severity": "low",
                    "detail": f"unknown={unknown} stub={stub} recorded not blocking",
                }
            )
        chain_summaries.append(
            {
                "chain_id": cid,
                "entry_count": entry_count,
                "classification_counts": counts,
                "consumable": entry_count > 0,
            }
        )
    runners = inventory.get("runner_verifier_hits") or []
    configs = inventory.get("config_hits") or []
    if len(runners) == 0:
        issues.append(
            {
                "issue_id": "inventory_no_runners",
                "severity": "medium",
                "detail": "no runner/verifier hits registered",
            }
        )
    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "dryrun_id": "p0_function_chain_inventory_consumption_v1",
        "chain_summaries": chain_summaries,
        "runner_verifier_count": len(runners),
        "config_count": len(configs),
        "runner_verifier_consumable": len(runners) > 0,
        "config_consumable": len(configs) > 0,
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
    }


def _dryrun_vision_scope(scope: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    required_flags = (
        ("camera_runtime_enabled_now", False),
        ("new_visual_model_inference_now", False),
        ("runtime_enabled_now", False),
    )
    for field, expected in required_flags:
        if scope.get(field) is not expected:
            issues.append(
                {
                    "issue_id": f"vision_flag:{field}",
                    "severity": "high",
                    "detail": f"expected {expected}, got {scope.get(field)}",
                }
            )
    if not scope.get("priority_capabilities"):
        issues.append(
            {
                "issue_id": "vision_missing_priorities",
                "severity": "high",
                "detail": "priority_capabilities empty",
            }
        )
    if not scope.get("recovery_order"):
        issues.append(
            {
                "issue_id": "vision_missing_recovery_order",
                "severity": "high",
                "detail": "recovery_order empty",
            }
        )
    high = [i for i in issues if i.get("severity") == "high"]
    ready = len(high) == 0
    return {
        "dryrun_id": "vision_recovery_scope_dryrun_v1",
        "simulated_checks": [
            "controlled_frame_scope_consumable",
            "visual_focus_plan_consumable",
            "tracking_plan_consumable",
            "no_camera_runtime",
            "no_vision_model_inference",
            "no_real_image_read",
            "no_new_visual_fact",
        ],
        "issues": issues,
        "vision_recovery_ready_for_next_dryrun": ready,
        "consumption_pass": ready,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_ocr_scope(scope: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    if "OCR" not in str(scope.get("inherits", "")):
        issues.append(
            {
                "issue_id": "ocr_missing_mainline_closure_inherit",
                "severity": "medium",
                "detail": "inherits should reference OCR Mainline Closure",
            }
        )
    for field in ("ocr_provider_invoked_now", "fact_layer_write_now", "ocr_runtime_enabled_now"):
        if scope.get(field) is not False:
            issues.append(
                {
                    "issue_id": f"ocr_flag:{field}",
                    "severity": "high",
                    "detail": f"must be false, got {scope.get(field)}",
                }
            )
    required_caps = ("OCRRequest", "ROI", "Evidence Pack")
    caps = " ".join(scope.get("priority_capabilities") or [])
    for cap in required_caps:
        if cap not in caps:
            issues.append(
                {
                    "issue_id": f"ocr_missing_cap:{cap}",
                    "severity": "high",
                    "detail": f"{cap} not in priority_capabilities",
                }
            )
    high = [i for i in issues if i.get("severity") == "high"]
    ready = len(high) == 0
    return {
        "dryrun_id": "ocr_recovery_scope_dryrun_v1",
        "simulated_checks": [
            "ocr_request_roi_evidence_pack_consumable",
            "text_region_pipeline_consumable",
            "mainline_closure_boundary_respected",
            "provider_closed",
            "no_fact_write",
        ],
        "issues": issues,
        "ocr_recovery_ready_for_next_dryrun": ready,
        "consumption_pass": ready,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_navigation_scope(scope: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    if scope.get("map_authority") != "readonly_hint_only":
        issues.append(
            {
                "issue_id": "navigation_map_authority",
                "severity": "high",
                "detail": "map must be readonly_hint_only",
            }
        )
    for field in ("navigation_action_triggered_now", "navigation_runtime_enabled_now"):
        if scope.get(field) is not False:
            issues.append(
                {
                    "issue_id": f"navigation_flag:{field}",
                    "severity": "high",
                    "detail": f"must be false, got {scope.get(field)}",
                }
            )
    high = [i for i in issues if i.get("severity") == "high"]
    ready = len(high) == 0
    return {
        "dryrun_id": "navigation_recovery_scope_dryrun_v1",
        "simulated_checks": [
            "navigation_policy_consumable",
            "guidance_plan_consumable",
            "map_readonly_hint_consumable",
            "no_navigation_action",
            "no_map_write",
        ],
        "issues": issues,
        "navigation_recovery_ready_for_next_dryrun": ready,
        "consumption_pass": ready,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_task_scope(scope: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    if not scope.get("duplicate_or_parallel_structure"):
        issues.append(
            {
                "issue_id": "task_midplatform_duplicate_not_registered",
                "severity": "medium",
                "detail": "expected duplicate_or_parallel_structure=true",
            }
        )
    for field in (
        "task_manager_committed_now",
        "task_midplatform_runtime_enabled_now",
        "midplatform_refactor_executed_now",
    ):
        if scope.get(field) is not False:
            issues.append(
                {
                    "issue_id": f"task_flag:{field}",
                    "severity": "high",
                    "detail": f"must be false, got {scope.get(field)}",
                }
            )
    high = [i for i in issues if i.get("severity") == "high"]
    ready = len(high) == 0
    return {
        "dryrun_id": "task_midplatform_recovery_scope_dryrun_v1",
        "simulated_checks": [
            "task_state_lifecycle_consumable",
            "guidance_observation_consumable",
            "speech_candidate_consumable_no_tts",
            "no_task_commit",
            "no_runtime_action",
            "midplatform_dual_dir_medium_only",
        ],
        "issues": issues,
        "task_midplatform_recovery_ready_for_next_dryrun": ready,
        "consumption_pass": ready,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_dependency_matrix(deps: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    rules = deps.get("rules") or []
    for required in REQUIRED_DEPENDENCY_RULES:
        if required not in rules:
            issues.append(
                {
                    "issue_id": f"dependency_rule_missing",
                    "severity": "high",
                    "detail": required,
                }
            )
    edges = deps.get("edges") or []
    edge_from_to = {(e.get("from"), e.get("to")) for e in edges}
    expected_edges = (
        ("vision", "navigation"),
        ("vision", "ocr"),
        ("ocr", "task_midplatform"),
        ("voice", "task_midplatform"),
    )
    for frm, to in expected_edges:
        if (frm, to) not in edge_from_to:
            issues.append(
                {
                    "issue_id": f"dependency_edge_missing:{frm}->{to}",
                    "severity": "high",
                    "detail": "required edge not in matrix",
                }
            )
    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "dryrun_id": "dependency_matrix_consumption_dryrun_v1",
        "rules_verified": [r for r in REQUIRED_DEPENDENCY_RULES if r in rules],
        "edge_count": len(edges),
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_runtime_boundary(planning_runtime: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    planning_flags = planning_runtime.get("flags") or {}
    dryrun_flags = {f: False for f in RUNTIME_BOUNDARY_FIELDS}
    for field in RUNTIME_BOUNDARY_FIELDS:
        plan_val = planning_flags.get(field)
        if plan_val is not None and plan_val is not False:
            issues.append(
                {
                    "issue_id": f"planning_runtime_flag:{field}",
                    "severity": "high",
                    "detail": "planning runtime flag must be false",
                }
            )
        if meta.get(field) is not False:
            issues.append(
                {
                    "issue_id": f"dryrun_meta_flag:{field}",
                    "severity": "high",
                    "detail": "dryrun boundary meta must be false",
                }
            )
    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "dryrun_id": "runtime_boundary_dryrun_v1",
        "flags": dryrun_flags,
        "all_runtime_flags_false": len(high) == 0,
        "planning_all_false": planning_runtime.get("all_runtime_flags_false") is True,
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_midplatform_risk(risk_reg: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    if not risk_reg.get("duplicate_or_parallel_structure"):
        issues.append(
            {
                "issue_id": "midplatform_duplicate_not_registered",
                "severity": "high",
                "detail": "duplicate structure must be registered",
            }
        )
    risks = risk_reg.get("risks") or []
    has_medium = any(r.get("severity") == "medium" for r in risks)
    if not has_medium:
        issues.append(
            {
                "issue_id": "midplatform_medium_missing",
                "severity": "medium",
                "detail": "expected medium severity dual-directory risk",
            }
        )
    if risk_reg.get("midplatform_refactor_executed_now") is True:
        issues.append(
            {
                "issue_id": "midplatform_refactor_executed",
                "severity": "high",
                "detail": "refactor must not execute in dryrun",
            }
        )
    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "dryrun_id": "midplatform_structure_risk_dryrun_v1",
        "duplicate_or_parallel_structure": risk_reg.get("duplicate_or_parallel_structure"),
        "severity": "medium",
        "refactor_executed_now": False,
        "risks_carried": len(risks),
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
        **meta,
    }


def _dryrun_phase_sequence(sequence: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    sequences = sequence.get("sequences") or []
    dryrun_entry = next(
        (s for s in sequences if s.get("phase_id") == UPSTREAM_NEXT_PHASE),
        None,
    )
    issues: List[Dict[str, Any]] = []
    if not dryrun_entry:
        issues.append(
            {
                "issue_id": "sequence_missing_dryrun",
                "severity": "medium",
                "detail": "planning sequence should include dryrun phase",
            }
        )
    high = [i for i in issues if i.get("severity") == "high"]
    return {
        "dryrun_id": "recovery_phase_sequence_dryrun_v1",
        "planning_sequences_consumed": len(sequences),
        "recommended_next_phase": NEXT_PHASE,
        "post_dryrun_review_phase": NEXT_PHASE,
        "post_dryrun_candidates": list(POST_DRYRUN_CANDIDATES),
        "execution_planning_preference": (
            "If dry-run has no high-risk, prefer Minimal Recovery Execution Planning before Midplatform Cleanup"
        ),
        "issues": issues,
        "consumption_pass": len(high) == 0,
        "high_risk_count": len(high),
        **meta,
    }


def _collect_high_risk(*parts: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set = set()
    for part in parts:
        for item in part.get("issues") or []:
            if item.get("severity") == "high":
                key = item.get("issue_id") or str(item)
                if key not in seen:
                    seen.add(key)
                    out.append(item)
    return out


def run_vision_ocr_navigation_task_midplatform_recovery_dryrun_v1(
    *,
    repo_root: str,
    vision_ocr_navigation_task_midplatform_recovery_planning_root: str,
    post_migration_engineering_smoke_test_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    repo = Path(repo_root).expanduser().resolve()
    planning_root = Path(vision_ocr_navigation_task_midplatform_recovery_planning_root).expanduser().resolve()
    smoke_root = (
        Path(post_migration_engineering_smoke_test_root).expanduser().resolve()
        if post_migration_engineering_smoke_test_root
        else planning_root.parent / "post_migration_engineering_smoke_test"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(planning_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "repo_root": str(repo),
        "upstream_planning_root": str(planning_root),
        "upstream_smoke_test_root": str(smoke_root),
    }

    planning_sm = _try_read_json(planning_root / "summary.json") or {}
    planning_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    smoke_sm = _try_read_json(smoke_root / "summary.json") or {}

    planning_verifier_trusted = planning_vr.get("verifier") == "GO" and planning_vr.get("passed") is True
    planning_summary_trusted = (
        planning_sm.get("boundary_ok") is True
        and planning_sm.get("phase") == UPSTREAM_PHASE
        and planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
    )
    if not planning_verifier_trusted and not planning_summary_trusted:
        blockers.append("planning verifier must be GO")
    if planning_sm.get("feature_implementation_started_now") is True:
        blockers.append("feature_implementation_started_now must be false")
    if planning_sm.get("runtime_enabled_now") is True:
        blockers.append("runtime_enabled_now must be false")
    if planning_sm.get("midplatform_refactor_executed_now") is True:
        blockers.append("midplatform_refactor_executed_now must be false")

    if (smoke_sm.get("high_risk_count") or 0) != 0:
        blockers.append("smoke test high_risk_count must be 0")
    if smoke_sm.get("migration_chain_reopened_now") is True:
        blockers.append("migration_chain_reopened_now must be false")

    for fname in PLANNING_REQUIRED_FILES:
        if not (planning_root / fname).is_file():
            blockers.append(f"missing planning artifact: {fname}")

    policy = {
        "policy_id": "recovery_dryrun_policy_v1",
        "scope": DRYRUN_SCOPE,
        "mode": "simulated_recovery_consumption_dryrun",
        **meta,
    }

    planning_input_review = {
        "review_id": "recovery_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier": planning_vr.get("verifier"),
        "upstream_verifier_trusted": planning_verifier_trusted,
        "upstream_summary_trusted": planning_summary_trusted,
        "upstream_final_decision": planning_sm.get("final_decision"),
        "upstream_recommended_next_phase": planning_sm.get("recommended_next_phase"),
        "smoke_high_risk_count": smoke_sm.get("high_risk_count"),
        "smoke_duplicate_midplatform": smoke_sm.get("duplicate_or_parallel_midplatform"),
        "review_pass": not blockers,
        "blockers": blockers,
        **meta,
    }

    inventory = _try_read_json(planning_root / "p0_function_chain_inventory_v1.json") or {}
    vision_scope = _try_read_json(planning_root / "vision_recovery_scope_planning_v1.json") or {}
    ocr_scope = _try_read_json(planning_root / "ocr_recovery_scope_planning_v1.json") or {}
    navigation_scope = _try_read_json(planning_root / "navigation_recovery_scope_planning_v1.json") or {}
    task_scope = _try_read_json(planning_root / "task_midplatform_recovery_scope_planning_v1.json") or {}
    deps = _try_read_json(planning_root / "vision_ocr_navigation_task_dependency_matrix_v1.json") or {}
    runtime_plan = _try_read_json(planning_root / "recovery_runtime_boundary_matrix_v1.json") or {}
    mid_risk = _try_read_json(planning_root / "midplatform_structure_risk_register_v1.json") or {}
    sequence = _try_read_json(planning_root / "recovery_phase_sequence_plan_v1.json") or {}

    inventory_dry = _consume_inventory(inventory)
    vision_dry = _dryrun_vision_scope(vision_scope, meta)
    ocr_dry = _dryrun_ocr_scope(ocr_scope, meta)
    navigation_dry = _dryrun_navigation_scope(navigation_scope, meta)
    task_dry = _dryrun_task_scope(task_scope, meta)
    deps_dry = _dryrun_dependency_matrix(deps, meta)
    runtime_dry = _dryrun_runtime_boundary(runtime_plan, meta)
    mid_dry = _dryrun_midplatform_risk(mid_risk, meta)
    sequence_dry = _dryrun_phase_sequence(sequence, meta)

    high_issues = _collect_high_risk(
        inventory_dry,
        vision_dry,
        ocr_dry,
        navigation_dry,
        task_dry,
        deps_dry,
        runtime_dry,
        mid_dry,
        sequence_dry,
    )
    if blockers:
        for b in blockers:
            high_issues.append(
                {
                    "issue_id": f"upstream_blocker:{b}",
                    "severity": "high",
                    "category": "recovery_planning_input_review",
                    "detail": b,
                }
            )

    high_count = len(high_issues)
    boundary_ok = not blockers and high_count == 0

    non_claims = {
        "register_id": "recovery_dryrun_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    readiness = {
        "decision_id": "recovery_dryrun_readiness_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "high_risk_count": high_count,
        "upstream_blockers": blockers,
        "all_chain_ready": boundary_ok
        and vision_dry.get("vision_recovery_ready_for_next_dryrun")
        and ocr_dry.get("ocr_recovery_ready_for_next_dryrun")
        and navigation_dry.get("navigation_recovery_ready_for_next_dryrun")
        and task_dry.get("task_midplatform_recovery_ready_for_next_dryrun"),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": high_count,
        "vision_recovery_ready_for_next_dryrun": vision_dry.get("vision_recovery_ready_for_next_dryrun"),
        "ocr_recovery_ready_for_next_dryrun": ocr_dry.get("ocr_recovery_ready_for_next_dryrun"),
        "navigation_recovery_ready_for_next_dryrun": navigation_dry.get("navigation_recovery_ready_for_next_dryrun"),
        "task_midplatform_recovery_ready_for_next_dryrun": task_dry.get(
            "task_midplatform_recovery_ready_for_next_dryrun"
        ),
        "inventory_consumption_pass": inventory_dry.get("consumption_pass"),
        "midplatform_dual_directory_severity": "medium",
        **meta,
    }

    return {
        "recovery_dryrun_policy": policy,
        "recovery_planning_input_review": planning_input_review,
        "p0_function_chain_inventory_consumption": inventory_dry,
        "vision_recovery_scope_dryrun": vision_dry,
        "ocr_recovery_scope_dryrun": ocr_dry,
        "navigation_recovery_scope_dryrun": navigation_dry,
        "task_midplatform_recovery_scope_dryrun": task_dry,
        "dependency_matrix_consumption_dryrun": deps_dry,
        "runtime_boundary_dryrun": runtime_dry,
        "midplatform_structure_risk_dryrun": mid_dry,
        "recovery_phase_sequence_dryrun": sequence_dry,
        "recovery_dryrun_non_claims_register": non_claims,
        "recovery_dryrun_readiness_decision": readiness,
        "summary": summary,
    }
