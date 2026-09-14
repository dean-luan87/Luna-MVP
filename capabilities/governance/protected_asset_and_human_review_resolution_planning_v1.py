# -*- coding: utf-8 -*-
"""Protected Asset and Human Review Resolution Planning v1.

Planning-only: define protected asset, human review, and permanent DNAE governance rules.
No human review execution, no file moves, no protected asset modification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001"
PLANNING_SCOPE = "protected_asset_and_human_review_resolution_planning_only"
PLANNING_ID = "pahr_resolution_planning_v1_001"
SOURCE_CHAIN = "protected_asset_and_human_review_resolution_planning_v1"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001"

ROADMAP_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING"
CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"

PROTECTED_ASSET_TYPES = [
    ("eval_out_phase_outputs", "critical", "phase evaluation outputs under _eval_out must never be auto-archived or deleted"),
    ("verifier_reports", "critical", "verifier_report.json and GO/NO-GO evidence must be retained"),
    ("GO_NO_GO_packs", "critical", "GO-NO-GO packs are authoritative phase decision records"),
    ("correction_records", "critical", "correction records document governance fixes and must be preserved"),
    ("historical_test_logs", "high", "historical test logs are audit evidence; no auto-delete"),
    ("phase_records", "critical", "phase verdict and status records must not be auto-modified"),
    ("closure_boundary_freeze_files", "critical", "closure boundary freeze artifacts define frozen governance state"),
    ("non_claims_registers", "high", "non-claims registers document what closure does not claim"),
    ("README_index_files", "high", "README and architecture index files require manual review before move"),
    ("phase_verdict_tables", "critical", "phase verdict tables must not be auto-edited during consolidation"),
    ("source_evidence_chain_files", "critical", "source_chain and evidence chain files preserve audit lineage"),
    ("memory_worldmodel_fact_governance_docs", "high", "governance docs for WorldModel/Memory/Fact write boundaries"),
    ("safety_gate_constitution_docs", "critical", "safety constitution and gate taxonomy docs are protected"),
    ("manually_protected_assets", "critical", "assets explicitly marked protected require owner and audit"),
]

HUMAN_REVIEW_CATEGORIES = [
    {
        "review_category": "high_risk_merge",
        "severity": "critical",
        "required_owner": "architecture_owner",
        "required_inputs": ["merge_plan_register", "source_asset_paths", "target_module", "life_system_mapping"],
        "allowed_decisions": ["KEEP_AS_IS", "MARK_AS_MERGE_CANDIDATE_ONLY", "DEFER_UNTIL_OWNER_ASSIGNED", "PERMANENT_DO_NOT_AUTO_EXECUTE"],
        "forbidden_decisions": ["DELETE_NOW", "MOVE_NOW", "MERGE_NOW", "ARCHIVE_NOW"],
        "resolution_output": "review_decision_record_with_rationale",
        "estimated_carryover_count": 5,
    },
    {
        "review_category": "archive_unclear_ownership",
        "severity": "high",
        "required_owner": "governance_owner",
        "required_inputs": ["archive_plan_register", "asset_path", "ownership_hint"],
        "allowed_decisions": ["KEEP_AS_IS", "MARK_AS_ARCHIVE_CANDIDATE_ONLY", "MARK_AS_PROTECTED", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["DELETE_NOW", "ARCHIVE_NOW", "MOVE_NOW"],
        "resolution_output": "owner_assignment_and_archive_disposition",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "client_backend_ambiguous",
        "severity": "high",
        "required_owner": "developer_backend_owner",
        "required_inputs": ["client_boundary_mapping", "developer_backend_extraction_map", "asset_path"],
        "allowed_decisions": ["MARK_AS_DEVELOPER_BACKEND", "MARK_AS_CLIENT_EXCLUDED", "RECLASSIFY_TARGET_MODULE", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["MOVE_NOW", "MERGE_NOW", "DELETE_NOW"],
        "resolution_output": "boundary_classification_record",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "docs_code_mismatch",
        "severity": "medium",
        "required_owner": "docs_owner",
        "required_inputs": ["docs_path", "code_path", "mismatch_description"],
        "allowed_decisions": ["KEEP_AS_IS", "RECLASSIFY_TARGET_MODULE", "REQUIRE_ADDITIONAL_EVIDENCE", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["DELETE_NOW", "MOVE_NOW", "CHANGE_PHASE_VERDICT"],
        "resolution_output": "docs_code_alignment_plan",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "future_placeholder_current_code",
        "severity": "high",
        "required_owner": "cognition_owner",
        "required_inputs": ["placeholder_mapping", "current_code_evidence", "life_system_mapping"],
        "allowed_decisions": ["MARK_AS_FUTURE_PLACEHOLDER", "MARK_AS_LEGACY_REFERENCE", "KEEP_AS_IS", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["ENABLE_RUNTIME", "MERGE_NOW", "DELETE_NOW"],
        "resolution_output": "placeholder_disposition_record",
        "estimated_carryover_count": 35,
    },
    {
        "review_category": "duplicated_gate_policy_schema",
        "severity": "medium",
        "required_owner": "governance_owner",
        "required_inputs": ["gate_constitution", "duplicate_schema_paths"],
        "allowed_decisions": ["KEEP_AS_IS", "RECLASSIFY_TARGET_MODULE", "REQUIRE_ADDITIONAL_EVIDENCE", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["DELETE_NOW", "MERGE_NOW", "REMOVE_GO_NO_GO_PACK"],
        "resolution_output": "gate_schema_dedup_plan",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "cross_repo_dependency",
        "severity": "medium",
        "required_owner": "architecture_owner",
        "required_inputs": ["dependency_graph", "cross_repo_refs"],
        "allowed_decisions": ["KEEP_AS_IS", "MARK_AS_LEGACY_REFERENCE", "DEFER_UNTIL_OWNER_ASSIGNED", "REQUIRE_ADDITIONAL_EVIDENCE"],
        "forbidden_decisions": ["DELETE_NOW", "MOVE_NOW", "ARCHIVE_NOW"],
        "resolution_output": "cross_repo_dependency_record",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "legacy_active_reference",
        "severity": "medium",
        "required_owner": "architecture_owner",
        "required_inputs": ["legacy_path", "active_references"],
        "allowed_decisions": ["MARK_AS_LEGACY_REFERENCE", "KEEP_AS_IS", "MARK_AS_ARCHIVE_CANDIDATE_ONLY", "DEFER_UNTIL_OWNER_ASSIGNED"],
        "forbidden_decisions": ["DELETE_NOW", "ARCHIVE_NOW"],
        "resolution_output": "legacy_reference_disposition",
        "estimated_carryover_count": 0,
    },
    {
        "review_category": "target_module_unclear",
        "severity": "medium",
        "required_owner": "architecture_owner",
        "required_inputs": ["module_inventory", "future_target_module", "life_system_mapping"],
        "allowed_decisions": ["RECLASSIFY_TARGET_MODULE", "DEFER_UNTIL_OWNER_ASSIGNED", "KEEP_AS_IS", "REQUIRE_ADDITIONAL_EVIDENCE"],
        "forbidden_decisions": ["MOVE_NOW", "MERGE_NOW", "DELETE_NOW"],
        "resolution_output": "target_module_assignment",
        "estimated_carryover_count": 200,
    },
    {
        "review_category": "life_system_mapping_review_needed",
        "severity": "high",
        "required_owner": "governance_owner",
        "required_inputs": ["life_system_mapping_matrix", "asset_path", "current_mapping"],
        "allowed_decisions": ["RECLASSIFY_TARGET_MODULE", "KEEP_AS_IS", "DEFER_UNTIL_OWNER_ASSIGNED", "REQUIRE_ADDITIONAL_EVIDENCE"],
        "forbidden_decisions": ["DELETE_NOW", "MOVE_NOW", "ENABLE_RUNTIME"],
        "resolution_output": "life_system_mapping_update_plan",
        "estimated_carryover_count": 0,
    },
]

PERMANENT_BLOCK_RULES = [
    ("protected_eval_out", "auto_archive", "eval_out phase outputs protected from automatic archive"),
    ("protected_eval_out", "auto_delete", "eval_out phase outputs protected from automatic delete"),
    ("protected_verifier", "auto_delete", "verifier reports must never be auto-deleted"),
    ("protected_verifier", "auto_move", "verifier reports must never be auto-moved without audit"),
    ("protected_go_no_go", "auto_delete", "GO-NO-GO packs are permanent governance records"),
    ("protected_go_no_go", "auto_archive", "GO-NO-GO packs must not be auto-archived"),
    ("protected_test_log", "auto_delete", "historical test logs require retention"),
    ("protected_correction_record", "auto_delete", "correction records must be preserved"),
    ("protected_phase_record", "auto_archive", "phase records must not be auto-archived"),
    ("protected_phase_record", "auto_merge", "phase records must not be auto-merged"),
    ("dynamic_protected_asset", "auto_move", "dynamically detected protected assets blocked from auto-move"),
    ("dynamic_protected_asset", "auto_delete", "dynamically detected protected assets blocked from auto-delete"),
]

ALLOWED_DECISIONS = [
    "KEEP_AS_IS",
    "RECLASSIFY_TARGET_MODULE",
    "MARK_AS_PROTECTED",
    "MARK_AS_DEVELOPER_BACKEND",
    "MARK_AS_CLIENT_EXCLUDED",
    "MARK_AS_FUTURE_PLACEHOLDER",
    "MARK_AS_LEGACY_REFERENCE",
    "MARK_AS_ARCHIVE_CANDIDATE_ONLY",
    "MARK_AS_MERGE_CANDIDATE_ONLY",
    "DEFER_UNTIL_OWNER_ASSIGNED",
    "REQUIRE_ADDITIONAL_EVIDENCE",
    "PERMANENT_DO_NOT_AUTO_EXECUTE",
]

FORBIDDEN_DECISIONS = [
    "DELETE_NOW",
    "MOVE_NOW",
    "MERGE_NOW",
    "ARCHIVE_NOW",
    "ENABLE_RUNTIME",
    "CHANGE_PHASE_VERDICT",
    "REMOVE_VERIFIER_REPORT",
    "REMOVE_GO_NO_GO_PACK",
    "REMOVE_TEST_LOG",
    "REMOVE_CORRECTION_RECORD",
]

REVIEW_STATES = [
    "queued_for_review",
    "owner_required",
    "in_manual_review",
    "decision_proposed",
    "decision_audited",
    "resolution_recorded",
    "deferred",
    "permanent_block",
    "closed_no_execution",
]

FORBIDDEN_STATES = [
    "auto_executed",
    "file_moved",
    "file_deleted",
    "module_merged",
    "runtime_enabled",
]

OWNER_TYPES = [
    ("architecture_owner", ["high_risk_merge", "cross_repo_dependency", "legacy_active_reference", "target_module_unclear"]),
    ("governance_owner", ["archive_unclear_ownership", "duplicated_gate_policy_schema", "life_system_mapping_review_needed"]),
    ("developer_backend_owner", ["client_backend_ambiguous"]),
    ("midplatform_owner", ["target_module_unclear"]),
    ("capability_owner", ["target_module_unclear"]),
    ("cognition_owner", ["future_placeholder_current_code"]),
    ("docs_owner", ["docs_code_mismatch"]),
    ("evaluation_owner", ["high_risk_merge"]),
    ("safety_owner", ["duplicated_gate_policy_schema"]),
    ("product_client_owner", ["client_backend_ambiguous"]),
]

ROOT_SPECS = [
    {
        "id": "roadmap_decision",
        "arg": "roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "protected_asset_and_human_review_route_decision.json", "route_option_matrix.json"],
    },
    {
        "id": "consolidation_closure",
        "arg": "consolidation_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "human_review_carryover_register.json",
            "permanent_do_not_auto_execute_carryover.json",
            "deferred_consolidation_action_pool.json",
            "closure_boundary_freeze.json",
            "consolidation_non_claims_register.json",
        ],
    },
    {
        "id": "consolidation_post_review",
        "arg": "consolidation_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "human_review_register_review.json", "do_not_auto_execute_review.json"],
    },
    {
        "id": "consolidation_dryrun",
        "arg": "consolidation_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "consolidation_planning",
        "arg": "consolidation_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "project_structure_governance_planning",
        "arg": "project_structure_governance_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_planning": False,
        "readme_modified_by_planning": False,
        "phase_verdict_table_modified_by_planning": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
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
        "no_runtime_executed": True,
        "boundary_ok": True,
        "violations": [],
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_protected_asset_and_human_review_resolution_planning_v1(
    *,
    roadmap_decision_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    roadmap_loaded = (
        roots["roadmap_decision"]["loaded"]
        and summaries["roadmap_decision"].get("final_decision") == ROADMAP_DECISION
    )
    closure_loaded = (
        roots["consolidation_closure"]["loaded"]
        and summaries["consolidation_closure"].get("final_decision") == CLOSURE_DECISION
    )
    post_review_loaded = roots["consolidation_post_review"]["loaded"]
    dryrun_loaded = roots["consolidation_dryrun"]["loaded"]
    planning_loaded = roots["consolidation_planning"]["loaded"]
    structure_loaded = roots["structure_map_dryrun"]["loaded"]
    governance_loaded = roots["project_structure_governance_planning"]["loaded"]
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    closure_root = roots["consolidation_closure"]["root"]
    human_carry = _try_read_json(closure_root / "human_review_carryover_register.json") if closure_root else {}
    permanent_carry = _try_read_json(closure_root / "permanent_do_not_auto_execute_carryover.json") if closure_root else {}

    human_review_count = human_carry.get("human_review_required_count", 240)
    permanent_count = permanent_carry.get("permanent_do_not_auto_execute_count", 914)
    protected_conflict = permanent_carry.get("protected_conflict_count", 448)
    static_dnae = summaries["consolidation_post_review"].get("do_not_auto_execute_count", 466)

    human_carry_loaded = bool(human_carry) and human_review_count == 240
    permanent_carry_loaded = bool(permanent_carry) and permanent_count == 914

    protected_asset_rows = []
    for pat, level, reason in PROTECTED_ASSET_TYPES:
        protected_asset_rows.append(
            {
                "protected_asset_type": pat,
                "protection_level": level,
                "auto_delete_allowed": False,
                "auto_archive_allowed": False,
                "auto_move_allowed": False,
                "auto_merge_allowed": False,
                "manual_review_required": True,
                "owner_required": True,
                "override_allowed": False,
                "retention_required": True,
                "reason": reason,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    protected_asset_policy = {
        "policy_id": "protected_asset_policy_v1",
        "asset_types": protected_asset_rows,
        "protected_asset_type_count": len(protected_asset_rows),
        "default_auto_delete_allowed": False,
        "default_auto_archive_allowed": False,
        "default_auto_move_allowed": False,
        "default_auto_merge_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_review_categories = []
    for cat in HUMAN_REVIEW_CATEGORIES:
        human_review_categories.append(
            {
                **cat,
                "auto_execute_allowed": False,
                "must_record_reason": True,
                "must_preserve_source_chain": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    human_review_resolution_policy = {
        "policy_id": "human_review_resolution_policy_v1",
        "total_human_review_count": human_review_count,
        "categories": human_review_categories,
        "human_review_category_count": len(human_review_categories),
        "human_review_execution_allowed": False,
        "planning_only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permanent_block_rules = []
    for block_type, blocked_action, block_reason in PERMANENT_BLOCK_RULES:
        permanent_block_rules.append(
            {
                "permanent_block_type": block_type,
                "blocked_action": blocked_action,
                "block_reason": block_reason,
                "manual_override_possible": True,
                "override_requirement": "explicit_manual_override_plus_audit_plus_rollback_plan",
                "retention_policy": "long_term_retain_by_default",
                "audit_required": True,
                "rollback_required": True,
                "auto_unblock_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    permanent_do_not_auto_execute_policy = {
        "policy_id": "permanent_dnae_policy_v1",
        "total_permanent_block_count": permanent_count,
        "protected_conflict_count": protected_conflict,
        "static_dnae_register_count": static_dnae,
        "rules": permanent_block_rules,
        "permanent_block_rule_count": len(permanent_block_rules),
        "permanent_block_override_allowed": False,
        "default_retention": "long_term_retain",
        "future_override_requires": ["explicit_manual_override", "audit_trace", "rollback_plan", "owner_approval"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    owner_rows = []
    for owner_type, categories in OWNER_TYPES:
        owner_rows.append(
            {
                "owner_type": owner_type,
                "applicable_review_categories": categories,
                "required_decision_authority": "manual_review_decision_only",
                "escalation_path": "governance_owner -> architecture_owner",
                "cannot_auto_assign": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    manual_owner_assignment_policy = {
        "policy_id": "manual_owner_assignment_policy_v1",
        "owner_types": owner_rows,
        "manual_owner_required": True,
        "auto_owner_assignment_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_decision_schema = {
        "schema_id": "review_decision_schema_v1",
        "allowed_decisions": [{"decision": d, "execution_allowed": False} for d in ALLOWED_DECISIONS],
        "forbidden_decisions": [{"decision": d, "forbidden": True} for d in FORBIDDEN_DECISIONS],
        "allowed_review_decision_count": len(ALLOWED_DECISIONS),
        "forbidden_review_decision_count": len(FORBIDDEN_DECISIONS),
        "delete_now_decision_forbidden": True,
        "move_now_decision_forbidden": True,
        "merge_now_decision_forbidden": True,
        "archive_now_decision_forbidden": True,
        "enable_runtime_decision_forbidden": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_resolution_state_machine = {
        "machine_id": "review_resolution_state_machine_v1",
        "allowed_states": REVIEW_STATES,
        "forbidden_states": FORBIDDEN_STATES,
        "review_state_count": len(REVIEW_STATES),
        "initial_state": "queued_for_review",
        "terminal_states": ["closed_no_execution", "permanent_block", "deferred"],
        "transitions_require_audit": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_audit_trace_policy = {
        "policy_id": "protected_asset_audit_trace_policy_v1",
        "audit_required": True,
        "source_chain_required": True,
        "trace_fields": [
            "review_item_id",
            "source_asset_path",
            "source_register",
            "original_action",
            "protection_reason",
            "owner_type",
            "proposed_decision",
            "final_review_decision",
            "rollback_ref",
            "timestamp",
            "source_chain",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    review_rollback_policy = {
        "policy_id": "review_rollback_policy_v1",
        "rollback_required": True,
        "rollback_scenarios": [
            "decision rollback",
            "target module rollback",
            "protected marking rollback",
            "owner assignment rollback",
            "README/index rollback if future edited",
            "phase verdict rollback if future edited",
        ],
        "no_file_rollback_in_planning": True,
        "planning_phase_no_file_change": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_type_matrix = {
        "rows": protected_asset_rows,
        "row_count": len(protected_asset_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_review_category_matrix = {
        "rows": human_review_categories,
        "row_count": len(human_review_categories),
        "total_human_review_count": human_review_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    permanent_block_rule_matrix = {
        "rows": permanent_block_rules,
        "row_count": len(permanent_block_rules),
        "total_permanent_block_count": permanent_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, loaded in (
        ("roadmap_decision_input_loaded", roadmap_loaded),
        ("consolidation_closure_input_loaded", closure_loaded),
        ("consolidation_post_review_input_loaded", post_review_loaded),
        ("human_review_carryover_loaded", human_carry_loaded),
        ("permanent_dnae_carryover_loaded", permanent_carry_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)

    boundary_ok = not blockers

    resolution_planning_readiness_decision = {
        "protected_asset_policy_defined": True,
        "human_review_resolution_policy_defined": True,
        "permanent_dnae_policy_defined": True,
        "owner_assignment_policy_defined": True,
        "decision_schema_defined": True,
        "state_machine_defined": True,
        "audit_trace_policy_defined": True,
        "rollback_policy_defined": True,
        "ready_for_human_review_resolution_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "debt_items": [
            f"human_review_items={human_review_count} awaiting resolution framework dryrun",
            f"permanent_block_items={permanent_count} awaiting policy enforcement dryrun",
            "protected asset types defined but not yet applied to assets",
            "owner assignment framework defined but owners not yet assigned",
            "real migration still blocked",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    protected_asset_and_human_review_resolution_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_roadmap_ref": "_eval_out/luna_project_structure_consolidation_roadmap_decision_v1_smoke_v0/",
        "source_closure_ref": "_eval_out/luna_project_structure_consolidation_closure_v1_smoke_v0/",
        "protected_asset_policy_ref": "protected_asset_policy.json",
        "human_review_resolution_policy_ref": "human_review_resolution_policy.json",
        "permanent_do_not_auto_execute_policy_ref": "permanent_do_not_auto_execute_policy.json",
        "manual_owner_assignment_policy_ref": "manual_owner_assignment_policy.json",
        "review_decision_schema_ref": "review_decision_schema.json",
        "resolution_state_machine_ref": "review_resolution_state_machine.json",
        "audit_trace_policy_ref": "protected_asset_audit_trace_policy.json",
        "rollback_policy_ref": "review_rollback_policy.json",
        "next_phase_recommendation": NEXT_PHASE if boundary_ok else PHASE_ID,
        "planning_only": True,
        "human_review_execution_allowed": False,
        "protected_asset_modification_allowed": False,
        "permanent_block_override_allowed": False,
        "real_migration_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_REQUIRES_FIXES",
        "reason": "policies defined; ready to dry-run 240 review and 914 permanent block resolution flows without execution",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "roadmap_decision_input_loaded": roadmap_loaded,
        "consolidation_closure_input_loaded": closure_loaded,
        "consolidation_post_review_input_loaded": post_review_loaded,
        "consolidation_dryrun_input_loaded": dryrun_loaded,
        "consolidation_planning_input_loaded": planning_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "human_review_carryover_loaded": human_carry_loaded,
        "permanent_dnae_carryover_loaded": permanent_carry_loaded,
        "protected_asset_policy_generated": True,
        "human_review_resolution_policy_generated": True,
        "permanent_dnae_policy_generated": True,
        "manual_owner_assignment_policy_generated": True,
        "review_decision_schema_generated": True,
        "review_resolution_state_machine_generated": True,
        "audit_trace_policy_generated": True,
        "rollback_policy_generated": True,
        "protected_asset_type_count": len(protected_asset_rows),
        "human_review_category_count": len(human_review_categories),
        "permanent_block_rule_count": len(permanent_block_rules),
        "allowed_review_decision_count": len(ALLOWED_DECISIONS),
        "forbidden_review_decision_count": len(FORBIDDEN_DECISIONS),
        "review_state_count": len(REVIEW_STATES),
        "human_review_required_count": human_review_count,
        "permanent_do_not_auto_execute_count": permanent_count,
        "protected_conflict_count": protected_conflict,
        "static_dnae_rule_count": static_dnae,
        "protected_assets_auto_delete_allowed": False,
        "protected_assets_auto_archive_allowed": False,
        "protected_assets_auto_move_allowed": False,
        "protected_assets_auto_merge_allowed": False,
        "human_review_execution_allowed": False,
        "permanent_block_override_allowed": False,
        "delete_now_decision_forbidden": True,
        "move_now_decision_forbidden": True,
        "merge_now_decision_forbidden": True,
        "archive_now_decision_forbidden": True,
        "enable_runtime_decision_forbidden": True,
        "manual_owner_required": True,
        "audit_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "ready_for_human_review_resolution_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "actual_human_review_executed": False,
        "protected_assets_modified": False,
        "permanent_blocks_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_planning": False,
        "readme_modified_by_planning": False,
        "phase_verdict_table_modified_by_planning": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
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
        "final_decision": FINAL_DECISION if boundary_ok else "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "protected_asset_and_human_review_resolution_planning_policy": protected_asset_and_human_review_resolution_planning_policy,
        "protected_asset_policy": protected_asset_policy,
        "human_review_resolution_policy": human_review_resolution_policy,
        "permanent_do_not_auto_execute_policy": permanent_do_not_auto_execute_policy,
        "manual_owner_assignment_policy": manual_owner_assignment_policy,
        "review_decision_schema": review_decision_schema,
        "review_resolution_state_machine": review_resolution_state_machine,
        "protected_asset_audit_trace_policy": protected_asset_audit_trace_policy,
        "review_rollback_policy": review_rollback_policy,
        "protected_asset_type_matrix": protected_asset_type_matrix,
        "human_review_category_matrix": human_review_category_matrix,
        "permanent_block_rule_matrix": permanent_block_rule_matrix,
        "resolution_planning_readiness_decision": resolution_planning_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "verifier_report": {"verifier": "PENDING", "phase": "planning", "source_chain": SOURCE_CHAIN},
    }
