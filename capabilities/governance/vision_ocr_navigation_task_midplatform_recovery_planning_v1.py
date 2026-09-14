# -*- coding: utf-8 -*-
"""Vision / OCR / Navigation / Task Midplatform Recovery Planning v1.

P0 function-chain recovery planning after post-migration smoke test GO. Planning-only.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Planning-v1-001"
PLANNING_SCOPE = "recovery_planning_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_midplatform_recovery_planning_v1"

UPSTREAM_PHASE = "Phase-Post-Migration-Engineering-Smoke-Test-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "POST_MIGRATION_ENGINEERING_SMOKE_TEST_GO_READY_FOR_VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING"
)
UPSTREAM_NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Planning-v1-001"

FINAL_DECISION = "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-DryRun-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Recovery Planning GO ≠ feature implementation started",
    "Recovery Planning GO ≠ runtime enabled",
    "Vision selected ≠ camera invoked",
    "OCR selected ≠ OCR provider invoked",
    "Navigation selected ≠ navigation action triggered",
    "Task Midplatform selected ≠ task manager committed",
    "Midplatform issue registered ≠ midplatform refactored",
    "Stub registered ≠ stub implemented",
    "Smoke Test GO ≠ all low-severity fixed",
)

RECOVERY_SEQUENCE: Tuple[Dict[str, Any], ...] = (
    {
        "sequence_id": "A",
        "phase_id": "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-DryRun-v1-001",
        "label": "Vision-OCR-Navigation-Task Recovery DryRun",
        "status": "recommended_next",
        "priority": "P0",
    },
    {
        "sequence_id": "B",
        "phase_id": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001",
        "label": "Midplatform Structure Cleanup Planning",
        "status": "deferred",
        "priority": "P1",
        "note": "不并入本 phase；双目录并存仅登记",
    },
    {
        "sequence_id": "C",
        "phase_id": "Phase-Post-Recovery-Minimal-Smoke-v1-001",
        "label": "Post-Recovery Minimal Smoke",
        "status": "deferred",
        "priority": "P1",
    },
    {
        "sequence_id": "D",
        "phase_id": "Phase-Voice-Interaction-Runtime-Integration-Planning-v1-001",
        "label": "Voice Interaction Runtime Integration Planning",
        "status": "deferred",
        "priority": "P1",
    },
    {
        "sequence_id": "E",
        "phase_id": "Phase-Emotional-Engine-Pre-Runtime-Planning-v1-001",
        "label": "Emotional Engine Pre-Runtime Planning",
        "status": "deferred",
        "priority": "P2",
    },
)

P0_CHAINS: Tuple[str, ...] = ("vision", "ocr", "navigation", "task_midplatform")

CHAIN_SCAN_ROOTS: Dict[str, Tuple[str, ...]] = {
    "vision": (
        "capabilities/vision",
        "docs/architecture",
        "tools/evaluation",
        "configs",
    ),
    "ocr": (
        "capabilities/evaluation/ocr",
        "configs/ocr",
        "configs/models/ocr",
        "configs/evaluation/ocr",
        "docs/architecture/evaluation",
        "tools/evaluation/ocr",
        "tools/evaluation/governance",
    ),
    "navigation": (
        "capabilities/navigation",
        "capabilities/midplatform",
        "capabilities/mid_platform",
        "docs/architecture",
        "tools/evaluation",
    ),
    "task_midplatform": (
        "capabilities/midplatform",
        "capabilities/mid_platform",
        "configs/midplatform",
        "tools/evaluation",
    ),
}

CHAIN_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "vision": (
        "vision",
        "visual",
        "frame",
        "tracking",
        "focus",
        "camera",
        "controlled_frame",
        "perception",
        "yolo",
    ),
    "ocr": (
        "ocr",
        "text_region",
        "evidence_pack",
        "evidence",
        "roi",
        "paddle",
        "rapidocr",
        "readability",
        "text_bearing",
    ),
    "navigation": (
        "navigation",
        "guidance",
        "crossing",
        "route",
        "map_location",
        "map_",
        "basic_navigation",
    ),
    "task_midplatform": (
        "task_",
        "task_manager",
        "lifecycle",
        "guidance",
        "observation",
        "speech",
        "stcm",
        "midplatform",
        "mid_platform",
        "user_guidance",
    ),
}

STUB_LINE_PATTERNS: Tuple[re.Pattern[str], ...] = (
    re.compile(r"raise\s+NotImplementedError\b"),
    re.compile(r"^\s*#\s*STUB\b", re.M),
    re.compile(r"present_but_not_implemented\s*=\s*True"),
)

RUNTIME_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "camera_runtime_enabled_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "task_manager_committed_now",
    "world_model_written_now",
    "memory_written_now",
    "scene_delta_generated_now",
    "tts_invoked_now",
    "llm_invoked_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "recovery_planning_only": True,
        "feature_implementation_started_now": False,
        "runtime_enabled_now": False,
        "camera_runtime_enabled_now": False,
        "ocr_runtime_enabled_now": False,
        "navigation_runtime_enabled_now": False,
        "task_midplatform_runtime_enabled_now": False,
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


def _matches_chain(chain: str, rel: str) -> bool:
    rel_l = rel.lower().replace("\\", "/")
    return any(k in rel_l for k in CHAIN_KEYWORDS[chain])


def _read_head(path: Path, limit: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return ""


def _is_stub(text: str) -> bool:
    return any(p.search(text) for p in STUB_LINE_PATTERNS)


def _classify_artifact(path: Path, chain: str) -> str:
    name = path.name.lower()
    rel = str(path).lower()
    text = _read_head(path) if path.suffix in (".py", ".md", ".json") else ""

    if _is_stub(text):
        return "stub_placeholder"
    if "dryrun" in name or "dry_run" in name:
        return "dryrun_only"
    if any(
        tag in name
        for tag in (
            "closure",
            "planning",
            "post_dryrun",
            "roadmap_decision",
            "post_review",
            "governance",
            "policy",
            "readiness",
        )
    ) and "runtime" not in name:
        return "closed_governance_only"
    if "runtime" in rel and ("dryrun" in name or "stub" in name or "disabled" in text.lower()):
        return "runtime_disabled"
    if chain == "navigation" and "executor" in name:
        return "runtime_disabled"
    if chain == "ocr" and any(
        x in rel for x in ("governance", "evaluation/ocr", "verify_ocr", "closure")
    ):
        if "smoke" in name or "dryrun" in name:
            return "dryrun_only"
        return "closed_governance_only"
    if path.suffix == ".py" and len(text) > 200 and "def " in text:
        return "implemented"
    if path.suffix in (".md", ".json", ".yaml", ".yml"):
        return "implemented" if path.is_file() else "unknown"
    return "unknown"


def _scan_chain_inventory(repo_root: Path, chain: str) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    counts: Dict[str, int] = {k: 0 for k in (
        "implemented",
        "dryrun_only",
        "stub_placeholder",
        "closed_governance_only",
        "runtime_disabled",
        "unknown",
    )}

    for root_rel in CHAIN_SCAN_ROOTS[chain]:
        base = repo_root / root_rel
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix not in (".py", ".md", ".json", ".yaml", ".yml") and "verify_" not in p.name:
                continue
            rel = str(p.relative_to(repo_root))
            if rel in seen:
                continue
            if not _matches_chain(chain, rel):
                continue
            seen.add(rel)
            classification = _classify_artifact(p, chain)
            counts[classification] = counts.get(classification, 0) + 1
            entries.append(
                {
                    "path": rel,
                    "chain": chain,
                    "classification": classification,
                    "artifact_type": p.suffix.lstrip(".") or "other",
                }
            )

    return {
        "chain_id": chain,
        "entries": entries,
        "entry_count": len(entries),
        "classification_counts": counts,
    }


def _build_p0_inventory(repo_root: Path) -> Dict[str, Any]:
    chains = [_scan_chain_inventory(repo_root, c) for c in P0_CHAINS]
    runner_hits: List[Dict[str, str]] = []
    tools_eval = repo_root / "tools/evaluation"
    if tools_eval.is_dir():
        for p in sorted(tools_eval.rglob("*.py")):
            rel = str(p.relative_to(repo_root))
            for chain in P0_CHAINS:
                if _matches_chain(chain, rel) and (
                    p.name.startswith("run_") or p.name.startswith("verify_")
                ):
                    runner_hits.append({"path": rel, "chain": chain, "kind": p.name.split("_")[0]})
    config_hits: List[Dict[str, str]] = []
    for cfg_root in ("configs/ocr", "configs/models/ocr", "configs/midplatform", "configs/evaluation/ocr"):
        base = repo_root / cfg_root
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file():
                    rel = str(p.relative_to(repo_root))
                    chain = "ocr" if "ocr" in rel else "task_midplatform"
                    config_hits.append({"path": rel, "chain": chain})
    return {
        "inventory_id": "p0_function_chain_inventory_v1",
        "chains": chains,
        "runner_verifier_hits": runner_hits,
        "config_hits": config_hits,
        "ocr_mainline_note": "OCR Mainline Governance Closure 已收口；本规划继承 readonly/gated baseline，不 reopen provider runtime",
    }


def _vision_scope_plan() -> Dict[str, Any]:
    return {
        "scope_id": "vision_recovery_scope_planning_v1",
        "priority_capabilities": [
            "controlled_frame_input",
            "visual_focus",
            "task_aware_visual_focus",
            "selective_tracking",
            "vision_recognition_evidence_readonly",
            "controlled_frame_sample_metadata",
            "return_to_vision_mainline",
        ],
        "recovery_order": [
            "1. 冻结 controlled frame / file metadata / existence guard 边界",
            "2. 恢复视觉候选与 focus 只读链路（无 camera）",
            "3. 恢复 tracking / observation 与 task 触发接口（只读）",
            "4. 与 OCR evidence ingest 对齐（仍不推理）",
        ],
        "camera_runtime_enabled_now": False,
        "new_visual_model_inference_now": False,
        "readonly_first": True,
        "runtime_enabled_now": False,
    }


def _ocr_scope_plan() -> Dict[str, Any]:
    return {
        "scope_id": "ocr_recovery_scope_planning_v1",
        "inherits": "OCR-Mainline-Final-Closure-v1-001",
        "priority_capabilities": [
            "OCRRequest",
            "ROI",
            "Evidence Pack",
            "text_region_pipeline",
            "ocr_evidence_readonly_ingest",
            "ocr_semantic_candidate",
        ],
        "recovery_order": [
            "1. 继承 OCR governance closure（gated / readonly / no-write）",
            "2. 规划 OCRRequest → ROI → Evidence Pack 边界",
            "3. 对齐 text-region / semantic candidate dry-run 链",
            "4. provider / Paddle / RapidOCR runtime 保持关闭",
        ],
        "ocr_provider_invoked_now": False,
        "fact_layer_write_now": False,
        "ocr_runtime_enabled_now": False,
    }


def _navigation_scope_plan() -> Dict[str, Any]:
    return {
        "scope_id": "navigation_recovery_scope_planning_v1",
        "priority_capabilities": [
            "basic_navigation_loop",
            "basic_navigation_guidance",
            "map_location_readonly_context",
            "crossing_decision_safety",
            "vision_navigation_feedback",
        ],
        "recovery_order": [
            "1. 基础导航闭环 policy/dry-run 对齐",
            "2. 路径提示与 guidance candidate（无 action）",
            "3. 只读地图/路线 hint（非事实权威）",
            "4. 视觉安全评估 + 任务状态联动",
        ],
        "map_authority": "readonly_hint_only",
        "navigation_action_triggered_now": False,
        "navigation_runtime_enabled_now": False,
    }


def _task_midplatform_scope_plan() -> Dict[str, Any]:
    return {
        "scope_id": "task_midplatform_recovery_scope_planning_v1",
        "priority_capabilities": [
            "task_manager_contract",
            "task_state",
            "lifecycle",
            "user_guidance",
            "observation_requirement",
            "speech_response_candidate",
            "stcm_sampling_guidance",
        ],
        "recovery_order": [
            "1. task state / lifecycle 只读恢复规划",
            "2. guidance / observation requirement 候选链",
            "3. speech response candidate（不接 TTS runtime）",
            "4. 与 Vision/OCR ingest 对齐（不 commit action）",
        ],
        "duplicate_or_parallel_structure": True,
        "midplatform_paths": ["capabilities/midplatform", "capabilities/mid_platform"],
        "midplatform_refactor_executed_now": False,
        "task_manager_committed_now": False,
        "task_midplatform_runtime_enabled_now": False,
    }


def _dependency_matrix() -> Dict[str, Any]:
    return {
        "matrix_id": "vision_ocr_navigation_task_dependency_matrix_v1",
        "edges": [
            {
                "from": "vision",
                "to": "navigation",
                "relation": "upstream_perception_and_safety_input",
            },
            {
                "from": "vision",
                "to": "ocr",
                "relation": "upstream_frame_and_roi_trigger",
            },
            {
                "from": "ocr",
                "to": "task_midplatform",
                "relation": "task_assist_channel_not_world_model_default",
            },
            {
                "from": "navigation",
                "to": "task_midplatform",
                "relation": "depends_on_task_state_and_readonly_map_context",
            },
            {
                "from": "task_midplatform",
                "to": "navigation",
                "relation": "state_and_guidance_candidate_only_no_runtime_action",
            },
            {
                "from": "voice",
                "to": "task_midplatform",
                "relation": "deferred_p1_downstream",
            },
            {
                "from": "emotion",
                "to": "task_midplatform",
                "relation": "deferred_p2_downstream",
            },
        ],
        "rules": [
            "Vision 是 Navigation / OCR task trigger 的上游之一",
            "OCR 是任务型辅助能力，不是世界模型默认主通道",
            "Navigation 依赖视觉安全评估、任务状态、只读地图上下文",
            "Task Midplatform 负责状态、生命周期、guidance candidate，不直接执行 runtime action",
            "Voice / Emotion 暂为 P1/P2，下游接入",
        ],
    }


def _runtime_boundary_matrix() -> Dict[str, Any]:
    flags = {f: False for f in RUNTIME_BOUNDARY_FIELDS}
    return {
        "matrix_id": "recovery_runtime_boundary_matrix_v1",
        "all_runtime_flags_false": True,
        "flags": flags,
        "interpretation": "Recovery Planning 阶段全部 runtime 门保持关闭",
    }


def _midplatform_risk_register(smoke: Dict[str, Any], issues: Dict[str, Any]) -> Dict[str, Any]:
    risks: List[Dict[str, Any]] = [
        {
            "risk_id": "midplatform_dual_directory",
            "severity": "medium",
            "status": "registered_not_refactored",
            "detail": "capabilities/midplatform 与 capabilities/mid_platform 并存",
            "recommended_phase": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001",
        }
    ]
    for item in issues.get("medium_issues") or []:
        if "midplatform" in str(item.get("issue_id", "")):
            risks.append(
                {
                    "risk_id": item.get("issue_id"),
                    "severity": "medium",
                    "status": "carried_from_smoke_test",
                    "detail": item.get("detail"),
                }
            )
    return {
        "register_id": "midplatform_structure_risk_register_v1",
        "duplicate_or_parallel_structure": smoke.get("duplicate_or_parallel_midplatform", True),
        "refactor_deferred_to": "Phase-Midplatform-Structure-Cleanup-Planning-v1-001",
        "risks": risks,
        "midplatform_refactor_executed_now": False,
    }


def run_vision_ocr_navigation_task_midplatform_recovery_planning_v1(
    *,
    repo_root: str,
    post_migration_engineering_smoke_test_root: str,
) -> Dict[str, Any]:
    blockers: List[str] = []
    repo = Path(repo_root).expanduser().resolve()
    smoke_root = Path(post_migration_engineering_smoke_test_root).expanduser().resolve()

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(smoke_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "repo_root": str(repo),
        "upstream_smoke_test_root": str(smoke_root),
    }

    smoke_sm = _try_read_json(smoke_root / "summary.json") or {}
    smoke_vr = _try_read_json(smoke_root / "verifier_report.json") or {}
    smoke_readiness = _try_read_json(smoke_root / "smoke_test_readiness_decision_v1.json") or {}
    smoke_issues = _try_read_json(smoke_root / "smoke_test_issue_register_v1.json") or {}

    smoke_verifier_trusted = smoke_vr.get("verifier") == "GO" and smoke_vr.get("passed") is True
    smoke_summary_trusted = (
        smoke_sm.get("boundary_ok") is True
        and smoke_sm.get("phase") == UPSTREAM_PHASE
        and smoke_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and smoke_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE
        and (smoke_sm.get("high_risk_count") or 0) == 0
    )
    if not smoke_verifier_trusted and not smoke_summary_trusted:
        blockers.append("smoke test verifier must be GO")
    if smoke_sm.get("migration_chain_reopened_now") is True:
        blockers.append("migration_chain_reopened_now must be false")
    if smoke_sm.get("feature_implementation_started_now") is True:
        blockers.append("feature_implementation_started_now must be false")
    if smoke_sm.get("runtime_refactor_executed_now") is True:
        blockers.append("runtime_refactor_executed_now must be false")
    if (smoke_sm.get("high_risk_count") or 0) != 0:
        blockers.append("high_risk_count must be 0")

    boundary_ok = not blockers

    policy = {
        "policy_id": "recovery_planning_policy_v1",
        "scope": PLANNING_SCOPE,
        "mode": "p0_function_chain_recovery_planning_only",
        "p0_chains": list(P0_CHAINS),
        **meta,
    }

    smoke_input_review = {
        "review_id": "smoke_test_input_review_v1",
        "upstream_root": str(smoke_root),
        "upstream_verifier": smoke_vr.get("verifier"),
        "upstream_verifier_trusted": smoke_verifier_trusted,
        "upstream_summary_trusted": smoke_summary_trusted,
        "upstream_final_decision": smoke_sm.get("final_decision"),
        "high_risk_count": smoke_sm.get("high_risk_count", 0),
        "medium_count": smoke_sm.get("medium_count", 0),
        "low_count": smoke_sm.get("low_count", 0),
        "duplicate_or_parallel_midplatform": smoke_sm.get("duplicate_or_parallel_midplatform"),
        "review_pass": boundary_ok,
        "blockers": blockers,
        **meta,
    }

    inventory = {**_build_p0_inventory(repo), **meta}

    vision_scope = {**_vision_scope_plan(), **meta}
    ocr_scope = {**_ocr_scope_plan(), **meta}
    navigation_scope = {**_navigation_scope_plan(), **meta}
    task_scope = {**_task_midplatform_scope_plan(), **meta}
    dependency = {**_dependency_matrix(), **meta}
    runtime_boundary = {**_runtime_boundary_matrix(), **meta}
    midplatform_risks = {**_midplatform_risk_register(smoke_sm, smoke_issues), **meta}
    sequence_plan = {
        "plan_id": "recovery_phase_sequence_plan_v1",
        "sequences": list(RECOVERY_SEQUENCE),
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **meta,
    }
    non_claims = {
        "register_id": "recovery_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }
    readiness = {
        "decision_id": "recovery_planning_readiness_decision_v1",
        "final_decision": FINAL_DECISION if boundary_ok else "VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "boundary_ok": boundary_ok,
        "upstream_blockers": blockers,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "p0_chains": list(P0_CHAINS),
        "midplatform_dual_directory_registered": True,
        "midplatform_refactor_deferred": True,
        **meta,
    }

    return {
        "recovery_planning_policy": policy,
        "smoke_test_input_review": smoke_input_review,
        "p0_function_chain_inventory": inventory,
        "vision_recovery_scope_planning": vision_scope,
        "ocr_recovery_scope_planning": ocr_scope,
        "navigation_recovery_scope_planning": navigation_scope,
        "task_midplatform_recovery_scope_planning": task_scope,
        "vision_ocr_navigation_task_dependency_matrix": dependency,
        "recovery_runtime_boundary_matrix": runtime_boundary,
        "midplatform_structure_risk_register": midplatform_risks,
        "recovery_phase_sequence_plan": sequence_plan,
        "recovery_non_claims_register": non_claims,
        "recovery_planning_readiness_decision": readiness,
        "summary": summary,
    }
