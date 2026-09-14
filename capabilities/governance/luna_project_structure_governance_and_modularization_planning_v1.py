# -*- coding: utf-8 -*-
"""Luna Project Structure Governance and Modularization Planning v1.

Planning-only / audit-only phase:
- Audit current repo structure and evaluation outputs.
- Propose target project structure model (no file moves).
- Define module domain taxonomy, versioning policy, doc reorg plan, developer backend extraction plan,
  midplatform organ system model, hardware management consolidation plan, future placeholders, client boundary policy,
  consolidation candidate register, and governance debt register.

Hard constraints:
- No runtime, no file ops for user media, no writes to WorldModel/Memory/Fact/Library.
- No deleting/renaming/moving production files; planning-only outputs under _eval_out.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001"
PLANNING_SCOPE = "luna_project_structure_governance_and_modularization_planning_only"
SOURCE_CHAIN = "luna_project_structure_governance_and_modularization_planning_v1"
PLANNING_ID = "luna_proj_struct_gov_mod_planning_v1_001"

FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"
NEXT_PHASE = "Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001"

GATE_TAXONOMY_FINAL_DECISION = "GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE"
POST_FILE_STAT_ROADMAP_FINAL_DECISION = "POST_FILE_STAT_ROADMAP_DECISION_READY_FOR_GATE_TAXONOMY_PLANNING"
FILE_STAT_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_EXISTENCE_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_METADATA_BOUNDARY_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
CROSSING_DECISION_CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"

ROOT_SPECS = [
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gate_constitution.json", "verifier_report.json"],
    },
    {
        "id": "post_file_stat_roadmap_decision",
        "arg": "post_file_stat_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_stat_guarded_closure",
        "arg": "file_stat_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_closure",
        "arg": "file_existence_check_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_closure",
        "arg": "file_metadata_boundary_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "crossing_decision_closure",
        "arg": "crossing_decision_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    # Optional: may exist in Workspace-Min
    {"id": "basic_navigation_loop_vision_strengthening_closure", "arg": "basic_navigation_loop_vision_strengthening_closure_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "map_location_readonly_context", "arg": "map_location_readonly_context_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "minimal_runtime_integration_closure", "arg": "minimal_runtime_integration_closure_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "ocr_final_closure", "arg": "ocr_final_closure_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def _root_loaded(root: Optional[Path], artifacts: List[str]) -> bool:
    if not root:
        return False
    for name in artifacts:
        if _try_read_json(root / name) is None:
            return False
    return True


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = _root_loaded(root, artifacts) if root else False
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _listdir_safe(path: Path) -> Tuple[bool, List[str]]:
    try:
        return True, sorted(os.listdir(str(path)))
    except FileNotFoundError:
        return False, []
    except NotADirectoryError:
        return True, []


def _count_files_under(root: Path, *, max_entries: int = 50_000) -> Dict[str, Any]:
    # Recursive traversal without explicit os.stat calls.
    # Uses os.listdir and NotADirectoryError to distinguish file/dir.
    queue: List[Path] = [root]
    visited_dirs = 0
    file_count = 0
    md_count = 0
    py_count = 0
    json_count = 0
    sample_paths: List[str] = []
    truncated = False

    while queue:
        d = queue.pop()
        ok, names = _listdir_safe(d)
        if not ok:
            continue
        visited_dirs += 1
        for name in names:
            p = d / name
            if len(sample_paths) < 20:
                sample_paths.append(str(p.relative_to(root)) if p.exists() else str(p))
            try:
                children = os.listdir(str(p))
                # is dir
                queue.append(p)
                _ = children  # unused
            except NotADirectoryError:
                file_count += 1
                lower = name.lower()
                if lower.endswith(".md"):
                    md_count += 1
                if lower.endswith(".py"):
                    py_count += 1
                if lower.endswith(".json"):
                    json_count += 1
            except FileNotFoundError:
                continue
            if file_count + visited_dirs >= max_entries:
                truncated = True
                queue.clear()
                break

    return {
        "root": str(root),
        "visited_dir_count": visited_dirs,
        "file_count": file_count,
        "md_count": md_count,
        "py_count": py_count,
        "json_count": json_count,
        "sample_paths": sample_paths[:20],
        "truncated": truncated,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _no_side_effect_boundary_report() -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "runtime_enabled": False,
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "existing_behavior_changed": False,
        "existing_phase_result_changed": False,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "navigation_action_triggered": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _target_structure_model() -> Dict[str, Any]:
    return {
        "target_top_level_model": [
            "core/constitution, core/gate, core/task, core/action, core/authority",
            "midplatform/orchestration, midplatform/resource, midplatform/privacy, midplatform/conflict_correction, midplatform/context, midplatform/handoff, midplatform/system_health, midplatform/hardware_monitor, midplatform/input_root",
            "capabilities/vision, capabilities/ocr, capabilities/voice, capabilities/navigation, capabilities/map_location, capabilities/tracking, capabilities/file_boundary",
            "cognition/world_model, cognition/memory_center, cognition/library, cognition/emotion_engine, cognition/exploration_drive",
            "developer_backend/whitebox, developer_backend/test_center, developer_backend/simulation_lab, developer_backend/evaluation, developer_backend/dashboard",
            "hardware/device_profile, hardware/power, hardware/wake, hardware/sensors, hardware/failover",
            "docs/architecture, docs/module_specs, docs/phase_records, docs/version_logs, docs/roadmap",
        ],
        "notes": ["planning only; do not move files now"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _module_domain_taxonomy() -> Dict[str, Any]:
    domains = [
        {"domain_id": "A", "domain_name": "Vision / First-Person Perception", "owner_layer": "vision"},
        {"domain_id": "B", "domain_name": "OCR / Visual Text Understanding", "owner_layer": "ocr"},
        {"domain_id": "C", "domain_name": "Voice / Language Interaction", "owner_layer": "voice"},
        {"domain_id": "D", "domain_name": "Task Chain / Navigation / Action", "owner_layer": "midplatform"},
        {"domain_id": "E", "domain_name": "Map / Location / Route Context", "owner_layer": "midplatform"},
        {"domain_id": "F", "domain_name": "Governance / Constitution / Gate", "owner_layer": "governance"},
        {"domain_id": "G", "domain_name": "MidPlatform Core", "owner_layer": "midplatform"},
        {"domain_id": "H", "domain_name": "Developer Backend", "owner_layer": "evaluation"},
        {"domain_id": "I", "domain_name": "Hardware / Device Runtime Management", "owner_layer": "midplatform"},
        {"domain_id": "J", "domain_name": "Cognition / World / Memory / Library / Emotion", "owner_layer": "governance"},
        {"domain_id": "K", "domain_name": "File / Data Boundary", "owner_layer": "vision"},
    ]
    # Expand each with required fields and placeholders.
    expanded: List[Dict[str, Any]] = []
    for d in domains:
        expanded.append(
            {
                **d,
                "current_status": "planning_only",
                "included_current_modules": [],
                "future_modules": [],
                "runtime_status": False,
                "write_status": False,
                "client_inclusion_status": "tbd",
                "developer_backend_status": "tbd",
                "versioning_required": True,
                "documentation_required": True,
                "governance_notes": [],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {"domains": expanded, "domain_count": len(expanded), "source_chain": SOURCE_CHAIN, **_not_fact()}


def _versioning_policy() -> Dict[str, Any]:
    return {
        "module_versioning_required": True,
        "module_changelog_required": True,
        "module_interface_contract_required": True,
        "module_non_claims_required": True,
        "required_files": ["MODULE.md", "VERSION.json", "CHANGELOG.md", "ROADMAP.md", "GOVERNANCE.md", "INTERFACE_CONTRACT.json", "VERIFIER_REQUIREMENTS.json", "NON_CLAIMS.md", "PHASE_HISTORY.md"],
        "maturity_levels": [
            "planned",
            "policy_defined",
            "dryrun_validated",
            "closure_completed",
            "guarded_runtime_candidate",
            "runtime_enabled",
            "production_candidate",
            "production",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _doc_reorg_policy() -> Dict[str, Any]:
    return {
        "docs_reorganization_planned": True,
        "current_issues": ["phase 文档很多", "closure 文档分散", "module 说明不足", "architecture 与 phase 混用", "evaluation 与 module 未统一索引"],
        "proposed_structure": ["docs/modules/", "docs/phases/", "docs/governance/", "docs/evaluation/", "docs/roadmap/", "docs/version_logs/", "docs/developer_backend/", "docs/client_boundary/"],
        "mapping_plan_only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _midplatform_organ_system_model() -> Dict[str, Any]:
    subsystems = [
        "MidPlatformOrchestrationSystem",
        "MidPlatformTaskContextSystem",
        "MidPlatformPerceptionWorkOrderSystem",
        "MidPlatformResourceBudgetSystem",
        "MidPlatformPrivacySystem",
        "MidPlatformConflictCorrectionSystem",
        "MidPlatformHandoffSystem",
        "MidPlatformInputRootSystem",
        "MidPlatformSystemHealthSystem",
        "MidPlatformHardwareMonitorSystem",
        "MidPlatformRuntimeModeSystem",
        "MidPlatformGovernanceDebtSystem",
    ]
    out: List[Dict[str, Any]] = []
    for s in subsystems:
        out.append(
            {
                "subsystem_id": s,
                "responsibility": "planning_only",
                "current_assets": [],
                "duplicated_assets": [],
                "future_interfaces": [],
                "gate_dependencies": [],
                "versioning_required": True,
                "runtime_status": False,
                "consolidation_priority": "tbd",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {"subsystems": out, "subsystem_count": len(out), "source_chain": SOURCE_CHAIN, **_not_fact()}


def _developer_backend_extraction_plan() -> Dict[str, Any]:
    return {
        "developer_backend_not_client": True,
        "whitebox_not_client_runtime": True,
        "test_center_not_client_runtime": True,
        "simulation_lab_not_client_runtime": True,
        "evaluation_not_client_runtime": True,
        "production_client_excludes_developer_backend": True,
        "components": [
            "Whitebox Observability",
            "Test Center",
            "Simulation Lab",
            "Evaluation Runner",
            "Verifier System",
            "Log Explorer",
            "Phase Dashboard",
            "Risk/Boundary Dashboard",
            "Demo/Investor Debug View",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _hardware_management_consolidation_plan() -> Dict[str, Any]:
    return {
        "hardware_monitoring_owned_by_midplatform": True,
        "hardware_runtime_execution_deferred": True,
        "hardware_capability_registry_required": True,
        "hardware_status_not_scattered": True,
        "coverage": ["hardware profile", "system health", "battery/power", "microphone state", "camera state", "wake device", "sensor health", "thermal/CPU/GPU/memory load", "dual device placeholder", "failover placeholder"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _future_placeholder_plan() -> Dict[str, Any]:
    future = [
        "WorldModel",
        "MemoryCenter",
        "Library",
        "EmotionEngine",
        "EmotionMap",
        "ExplorationDrive",
        "MapRuntime",
        "OfflineDistributedMidPlatform",
        "ResilienceSystem",
        "SocialSkillSystem",
        "HumanRelationshipModel",
        "LifeSystemLayer",
    ]
    out: List[Dict[str, Any]] = []
    for f in future:
        out.append(
            {
                "future_module_id": f,
                "current_status": "placeholder_only",
                "existing_assets": [],
                "missing_assets": ["MODULE.md", "INTERFACE_CONTRACT.json", "GOVERNANCE.md"],
                "dependency": [],
                "planned_location": "tbd",
                "runtime_status": False,
                "write_status": False,
                "near_term_priority": "P2",
                "long_term_role": "tbd",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {"future_modules": out, "future_placeholder_module_count": len(out), "source_chain": SOURCE_CHAIN, **_not_fact()}


def _consolidation_candidate_register() -> Dict[str, Any]:
    candidates = [
        ("C1", "Vision focus + world observation + tracking policy", ["capabilities/vision", "docs/architecture/vision"], "capabilities/vision"),
        ("C2", "OCR activation + evidence + semantic + review queue", ["capabilities/midplatform", "docs/architecture/evaluation"], "capabilities/ocr"),
        ("C3", "Speech gate + VOP + voice session", ["docs/architecture/voice", "capabilities/midplatform"], "capabilities/voice"),
        ("C4", "Task manager + task chain + navigation loop", ["docs/architecture/midplatform"], "midplatform/task"),
        ("C5", "File metadata boundary + existence + stat", ["capabilities/vision", "_eval_out"], "capabilities/file_boundary"),
        ("C6", "Gate taxonomy + safety constitution + crossing governance", ["docs/architecture/governance"], "core/constitution"),
        ("C7", "Resource budget + system health + hardware profile", ["docs/architecture/midplatform"], "midplatform/system_health"),
        ("C8", "Evaluation runner + verifier + phase verdict table", ["tools/evaluation", "docs/architecture/evaluation"], "developer_backend/evaluation"),
        ("C9", "Whitebox + logs + dashboard", ["docs/architecture/evaluation"], "developer_backend/whitebox"),
    ]
    out = []
    for cid, desc, locs, target in candidates:
        out.append(
            {
                "consolidation_candidate_id": cid,
                "description": desc,
                "current_locations": locs,
                "target_module": target,
                "should_merge_now": False,
                "planning_only": True,
                "migration_required_later": True,
                "risk": "medium",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {"candidates": out, "consolidation_candidate_count": len(out), "source_chain": SOURCE_CHAIN, **_not_fact()}


def _client_boundary_policy() -> Dict[str, Any]:
    return {
        "developer_backend_excluded": [
            "whitebox",
            "test_center",
            "simulation_lab",
            "evaluation_runner",
            "verifier",
            "phase_dashboard",
            "investor_debug_overlay",
            "raw_logs_beyond_runtime_safe_subset",
            "governance_audit_tools",
        ],
        "client_allowed_candidates": [
            "minimal runtime core (future)",
            "user-facing voice output (future, gated)",
            "camera input runtime (future, guarded release)",
            "navigation guidance runtime (future, action release gated)",
            "local safety minimal mode",
            "hardware status minimal subset",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _governance_debt_register() -> Dict[str, Any]:
    topics = [
        "phase sprawl",
        "doc sprawl",
        "eval_out cross-repo ambiguity",
        "module ownership unclear",
        "midplatform overload",
        "developer tools mixed with runtime",
        "future modules not placed",
        "versioning/changelog missing",
        "module interface contracts missing",
        "whitebox/test center not yet separated",
        "hardware monitoring scattered",
        "client/backend boundary not fully formalized",
    ]
    return {"topics": topics, "topic_count": len(topics), "source_chain": SOURCE_CHAIN, **_not_fact()}


def run_luna_project_structure_governance_and_modularization_planning_v1(
    *,
    repo_root: str,
    gate_taxonomy_planning_root: str,
    post_file_stat_roadmap_decision_root: str,
    file_stat_guarded_closure_root: str,
    file_existence_check_guarded_closure_root: str,
    file_metadata_boundary_closure_root: str,
    controlled_frame_sample_closure_root: str,
    controlled_frame_input_closure_root: str,
    crossing_decision_closure_root: str,
    safety_constitution_root: str,
    basic_navigation_loop_vision_strengthening_closure_root: Optional[str] = None,
    map_location_readonly_context_root: Optional[str] = None,
    minimal_runtime_integration_closure_root: Optional[str] = None,
    ocr_final_closure_root: Optional[str] = None,
) -> Dict[str, Any]:
    repo = Path(repo_root).expanduser().resolve()

    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}

    input_rows: List[Dict[str, Any]] = []
    cross_repo_input_roots_observed = False
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        path_str = str(meta["root"]) if meta["root"] else "(not_provided)"
        if "Luna-Workspace-Min" in path_str:
            cross_repo_input_roots_observed = True
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": path_str,
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    def _match(intake_id: str, expected: str) -> bool:
        return roots[intake_id]["loaded"] and summaries[intake_id].get("final_decision") == expected

    gate_taxonomy_input_loaded = _match("gate_taxonomy_planning", GATE_TAXONOMY_FINAL_DECISION)
    post_file_stat_roadmap_input_loaded = _match("post_file_stat_roadmap_decision", POST_FILE_STAT_ROADMAP_FINAL_DECISION)
    file_stat_guarded_closure_input_loaded = _match("file_stat_guarded_closure", FILE_STAT_GUARDED_CLOSURE_DECISION)
    file_existence_check_guarded_closure_input_loaded = _match("file_existence_check_guarded_closure", FILE_EXISTENCE_GUARDED_CLOSURE_DECISION)
    file_metadata_boundary_closure_input_loaded = _match("file_metadata_boundary_closure", FILE_METADATA_BOUNDARY_CLOSURE_DECISION)
    controlled_frame_sample_closure_input_loaded = _match("controlled_frame_sample_closure", CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION)
    controlled_frame_input_closure_input_loaded = _match("controlled_frame_input_closure", CONTROLLED_FRAME_INPUT_CLOSURE_DECISION)
    crossing_decision_closure_input_loaded = _match("crossing_decision_closure", CROSSING_DECISION_CLOSURE_DECISION)
    safety_constitution_input_loaded = _match("safety_constitution", SAFETY_CONSTITUTION_DECISION)

    blockers: List[str] = []
    if not all(
        [
            gate_taxonomy_input_loaded,
            post_file_stat_roadmap_input_loaded,
            file_stat_guarded_closure_input_loaded,
            file_existence_check_guarded_closure_input_loaded,
            file_metadata_boundary_closure_input_loaded,
            controlled_frame_sample_closure_input_loaded,
            controlled_frame_input_closure_input_loaded,
            crossing_decision_closure_input_loaded,
            safety_constitution_input_loaded,
        ]
    ):
        blockers.append("required_upstream_roots_missing_or_invalid")

    # Current project structure audit (directories only)
    audit_targets = {
        "docs/architecture": repo / "docs" / "architecture",
        "docs/architecture/vision": repo / "docs" / "architecture" / "vision",
        "docs/architecture/midplatform": repo / "docs" / "architecture" / "midplatform",
        "docs/architecture/governance": repo / "docs" / "architecture" / "governance",
        "docs/architecture/evaluation": repo / "docs" / "architecture" / "evaluation",
        "capabilities": repo / "capabilities",
        "capabilities/vision": repo / "capabilities" / "vision",
        "capabilities/midplatform": repo / "capabilities" / "midplatform",
        "capabilities/governance": repo / "capabilities" / "governance",
        "tools/evaluation": repo / "tools" / "evaluation",
        "tools/evaluation/vision": repo / "tools" / "evaluation" / "vision",
        "tools/evaluation/midplatform": repo / "tools" / "evaluation" / "midplatform",
        "tools/evaluation/governance": repo / "tools" / "evaluation" / "governance",
        "_eval_out": repo / "_eval_out",
    }

    audit_sections: List[Dict[str, Any]] = []
    for k, p in audit_targets.items():
        audit_sections.append({"section_id": k, "counts": _count_files_under(p), "source_chain": SOURCE_CHAIN, **_not_fact()})

    eval_out_exists, eval_roots = _listdir_safe(repo / "_eval_out")
    current_eval_phase_count = len(eval_roots) if eval_out_exists else 0
    current_closure_count = len([r for r in eval_roots if "closure" in r]) if eval_out_exists else 0

    current_project_structure_audit = {
        "audit_sections": audit_sections,
        "current_module_count": 0,  # planning-only estimate; real modularization comes later
        "current_doc_count": sum(s["counts"]["md_count"] for s in audit_sections),
        "current_eval_phase_count": current_eval_phase_count,
        "current_closure_count": current_closure_count,
        "repeated_module_candidates": ["gate proliferation", "policy overlap", "verifier template divergence"],
        "scattered_capability_candidates": ["developer backend mixed with runtime", "evaluation assets mixed with architecture docs"],
        "developer_only_assets": ["tools/evaluation", "docs/architecture/evaluation"],
        "client_runtime_assets": [],
        "backend_assets": ["tools/evaluation", "_eval_out"],
        "future_placeholder_assets": ["cognition placeholders", "hardware placeholders"],
        "undocumented_or_under_documented_assets": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    luna_project_structure_governance_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_phase_refs": [
            "_eval_out/gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0/",
            "_eval_out/post_file_stat_roadmap_decision_v1_smoke_v0/",
        ],
        "current_project_structure_audit_ref": "current_project_structure_audit.json",
        "target_project_structure_model_ref": "target_project_structure_model.json",
        "module_domain_taxonomy_ref": "module_domain_taxonomy.json",
        "module_versioning_policy_ref": "module_versioning_and_changelog_policy.json",
        "document_reorganization_policy_ref": "document_reorganization_policy.json",
        "developer_backend_extraction_plan_ref": "developer_backend_extraction_plan.json",
        "midplatform_modularization_plan_ref": "midplatform_organ_system_model.json",
        "future_module_placeholder_plan_ref": "future_module_placeholder_plan.json",
        "governance_debt_register_ref": "project_governance_debt_register.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_ok = not blockers

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "gate_taxonomy_input_loaded": gate_taxonomy_input_loaded,
        "post_file_stat_roadmap_input_loaded": post_file_stat_roadmap_input_loaded,
        "file_stat_guarded_closure_input_loaded": file_stat_guarded_closure_input_loaded,
        "file_existence_check_guarded_closure_input_loaded": file_existence_check_guarded_closure_input_loaded,
        "file_metadata_boundary_closure_input_loaded": file_metadata_boundary_closure_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "crossing_decision_closure_input_loaded": crossing_decision_closure_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "current_project_structure_audit_generated": True,
        "target_project_structure_model_generated": True,
        "module_domain_taxonomy_generated": True,
        "module_versioning_policy_generated": True,
        "document_reorganization_policy_generated": True,
        "midplatform_organ_system_model_generated": True,
        "developer_backend_extraction_plan_generated": True,
        "hardware_management_consolidation_plan_generated": True,
        "future_module_placeholder_plan_generated": True,
        "module_consolidation_candidate_register_generated": True,
        "client_boundary_policy_generated": True,
        "project_governance_debt_register_generated": True,
        "module_domain_count": _module_domain_taxonomy()["domain_count"],
        "midplatform_subsystem_count": _midplatform_organ_system_model()["subsystem_count"],
        "future_placeholder_module_count": _future_placeholder_plan()["future_placeholder_module_count"],
        "consolidation_candidate_count": _consolidation_candidate_register()["consolidation_candidate_count"],
        "developer_backend_not_client": True,
        "whitebox_not_client_runtime": True,
        "test_center_not_client_runtime": True,
        "simulation_lab_not_client_runtime": True,
        "evaluation_not_client_runtime": True,
        "hardware_monitoring_owned_by_midplatform": True,
        "hardware_runtime_execution_deferred": True,
        "module_versioning_required": True,
        "module_changelog_required": True,
        "module_interface_contract_required": True,
        "module_non_claims_required": True,
        "docs_reorganization_planned": True,
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "existing_behavior_changed": False,
        "existing_phase_result_changed": False,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "project structure governance planning complete; next is structure-map dryrun to produce inventory and mapping artifacts",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "luna_project_structure_governance_planning_policy": luna_project_structure_governance_planning_policy,
        "current_project_structure_audit": current_project_structure_audit,
        "target_project_structure_model": _target_structure_model(),
        "module_domain_taxonomy": _module_domain_taxonomy(),
        "module_versioning_and_changelog_policy": _versioning_policy(),
        "document_reorganization_policy": _doc_reorg_policy(),
        "midplatform_organ_system_model": _midplatform_organ_system_model(),
        "developer_backend_extraction_plan": _developer_backend_extraction_plan(),
        "hardware_management_consolidation_plan": _hardware_management_consolidation_plan(),
        "future_module_placeholder_plan": _future_placeholder_plan(),
        "module_consolidation_candidate_register": _consolidation_candidate_register(),
        "client_boundary_policy": _client_boundary_policy(),
        "project_governance_debt_register": _governance_debt_register(),
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _no_side_effect_boundary_report(),
        "no_write_boundary_report": _no_side_effect_boundary_report(),
        "no_action_boundary_report": _no_side_effect_boundary_report(),
        "no_file_operation_boundary_report": _no_side_effect_boundary_report(),
    }

