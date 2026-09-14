# -*- coding: utf-8 -*-
"""Luna Project Structure Consolidation Planning v1.

Planning-only phase:
- Consume Structure Map DryRun inventory and freeze merge/archive/split/keep/defer plans.
- Preserve future_life_system_mapping on every consolidation row.
- Define batch sequence and dependency graph without executing any file moves.

Hard constraints:
- No runtime, no file moves/renames/deletes.
- No writes to WorldModel/Memory/Fact/Library.
- Planning outputs only under _eval_out.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Planning-v1-001"
PLANNING_SCOPE = "luna_project_structure_consolidation_planning_only"
SOURCE_CHAIN = "luna_project_structure_consolidation_planning_v1"
PLANNING_ID = "luna_proj_struct_consolidation_planning_v1_001"

FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001"

STRUCTURE_MAP_DRYRUN_FINAL_DECISION = (
    "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
)

ROOT_SPECS = [
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "module_inventory.json",
            "current_to_target_structure_map.json",
            "life_system_mapping_matrix.json",
            "migration_risk_register.json",
            "no_file_move_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "project_structure_governance_planning",
        "arg": "project_structure_governance_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "module_consolidation_candidate_register.json"],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gate_constitution.json"],
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


def _consolidation_row(entry: Dict[str, Any], *, plan_id: str, action: str) -> Dict[str, Any]:
    return {
        "plan_row_id": plan_id,
        "current_path": entry.get("current_path"),
        "current_module": entry.get("current_module"),
        "asset_type": entry.get("asset_type"),
        "current_engineering_domain": entry.get("current_engineering_domain"),
        "future_target_module": entry.get("future_target_module"),
        "future_life_system_mapping": entry.get("future_life_system_mapping"),
        "planned_action": action,
        "execution_status": "planning_only",
        "actual_move_executed": False,
        "versioning_required": entry.get("versioning_required", True),
        "is_client": entry.get("is_client", False),
        "is_developer_backend": entry.get("is_developer_backend", False),
        "is_midplatform_organ": entry.get("is_midplatform_organ", False),
        "is_capability_organ": entry.get("is_capability_organ", False),
        "is_cognition_placeholder": entry.get("is_cognition_placeholder", False),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _group_by_target(entries: List[Dict[str, Any]], action: str) -> List[Dict[str, Any]]:
    by_target: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in entries:
        by_target[e.get("future_target_module", "tbd")].append(e)
    groups = []
    for i, (target, items) in enumerate(sorted(by_target.items(), key=lambda x: -len(x[1]))):
        groups.append(
            {
                "consolidation_group_id": f"{action.upper()}_G{i:03d}",
                "planned_action": action,
                "future_target_module": target,
                "future_life_system_mapping": items[0].get("future_life_system_mapping") if items else "UnclassifiedLegacyLayer",
                "asset_count": len(items),
                "sample_current_paths": [x.get("current_path") for x in items[:8]],
                "execution_status": "planning_only",
                "actual_move_executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return groups


def _batch_sequence(merge_g: List, archive_g: List, split_g: List, keep_g: List, defer_g: List) -> Dict[str, Any]:
    batches = [
        {"batch_id": "B0", "phase": "freeze_plans", "actions": ["keep"], "description": "freeze stable assets first", "execution_status": "planning_only"},
        {"batch_id": "B1", "phase": "developer_backend_extraction", "actions": ["merge"], "target_modules": ["developer_backend/evaluation", "developer_backend/whitebox", "developer_backend/test_center"], "execution_status": "planning_only"},
        {"batch_id": "B2", "phase": "midplatform_organ_consolidation", "actions": ["merge"], "target_modules": ["midplatform/orchestration", "midplatform/task", "midplatform/context"], "execution_status": "planning_only"},
        {"batch_id": "B3", "phase": "capability_organ_consolidation", "actions": ["merge", "split"], "target_modules": ["capabilities/vision", "capabilities/ocr", "capabilities/voice"], "execution_status": "planning_only"},
        {"batch_id": "B4", "phase": "cognition_placeholder_formalization", "actions": ["split"], "target_modules": ["cognition/world_model", "cognition/memory_center", "cognition/library"], "execution_status": "planning_only"},
        {"batch_id": "B5", "phase": "legacy_archive", "actions": ["archive", "defer"], "target_modules": ["archive/legacy"], "execution_status": "planning_only"},
        {"batch_id": "B6", "phase": "doc_reorganization", "actions": ["merge"], "target_modules": ["docs/modules", "docs/governance", "docs/evaluation"], "execution_status": "planning_only"},
    ]
    return {
        "batches": batches,
        "batch_count": len(batches),
        "merge_group_count": len(merge_g),
        "archive_group_count": len(archive_g),
        "split_group_count": len(split_g),
        "keep_group_count": len(keep_g),
        "defer_group_count": len(defer_g),
        "actual_batch_execution": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _dependency_graph() -> Dict[str, Any]:
    edges = [
        ("B0", "B1", "keep_before_extract"),
        ("B1", "B2", "dev_backend_before_midplatform"),
        ("B2", "B3", "midplatform_before_capability"),
        ("B3", "B4", "capability_before_cognition"),
        ("B4", "B5", "cognition_before_legacy_archive"),
        ("B5", "B6", "archive_before_doc_reorg"),
    ]
    return {
        "edges": [{"from_batch": a, "to_batch": b, "reason": r, "source_chain": SOURCE_CHAIN, **_not_fact()} for a, b, r in edges],
        "edge_count": len(edges),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _life_system_consolidation_matrix(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_life: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in entries:
        by_life[e.get("future_life_system_mapping", "UnclassifiedLegacyLayer")].append(e)
    rows = []
    for ls, items in sorted(by_life.items(), key=lambda x: -len(x[1])):
        action_counts = Counter(i.get("disposition_action", "keep") for i in items)
        rows.append(
            {
                "life_system_id": ls,
                "asset_count": len(items),
                "future_life_system_mapping": ls,
                "merge_count": action_counts.get("merge", 0),
                "archive_count": action_counts.get("archive", 0),
                "split_count": action_counts.get("split", 0),
                "keep_count": action_counts.get("keep", 0),
                "defer_count": action_counts.get("defer", 0),
                "consolidation_priority": "P0" if ls in {"GovernanceLayer", "DeveloperBackendLayer"} else "P1",
                "execution_status": "planning_only",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "life_system_rows": rows,
        "row_count": len(rows),
        "all_rows_have_future_life_system_mapping": all(r.get("future_life_system_mapping") for r in rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _domain_plan(entries: List[Dict[str, Any]], *, filter_key: str, filter_val: bool, plan_name: str) -> Dict[str, Any]:
    matched = [e for e in entries if e.get(filter_key) == filter_val]
    groups = _group_by_target(matched, "merge")
    return {
        "plan_name": plan_name,
        "asset_count": len(matched),
        "consolidation_groups": groups[:30],
        "group_count": len(groups),
        "execution_status": "planning_only",
        "actual_move_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _consolidation_risk_register(dryrun_risks: List[Dict[str, Any]], entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    risks = []
    for r in dryrun_risks:
        risks.append({**r, "consolidation_mitigation": "plan frozen; execution deferred to consolidation dryrun", "source_chain": SOURCE_CHAIN})
    risks.extend(
        [
            {
                "risk_id": "CP1",
                "risk_topic": "premature_consolidation_execution",
                "risk_level": "critical",
                "description": "executing merge/archive before consolidation dryrun",
                "consolidation_mitigation": "planning_only boundary",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "risk_id": "CP2",
                "risk_topic": "life_system_mapping_drift",
                "risk_level": "high",
                "description": "consolidation plan rows missing future_life_system_mapping",
                "consolidation_mitigation": "verifier hard check",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ]
    )
    missing = [e for e in entries if not e.get("future_life_system_mapping")]
    return {
        "risks": risks,
        "risk_count": len(risks),
        "plan_rows_missing_life_system_mapping": len(missing),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _no_file_move_boundary_report() -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "actual_rename_executed": False,
        "actual_delete_executed": False,
        "runtime_enabled": False,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "no_runtime_executed": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_luna_project_structure_consolidation_planning_v1(
    *,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

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

    dryrun_loaded = (
        roots["structure_map_dryrun"]["loaded"]
        and roots["structure_map_dryrun"]["summary"].get("final_decision") == STRUCTURE_MAP_DRYRUN_FINAL_DECISION
    )
    governance_loaded = roots["project_structure_governance_planning"]["loaded"]

    blockers: List[str] = []
    if not dryrun_loaded:
        blockers.append("structure_map_dryrun_missing_or_invalid")
    if not governance_loaded:
        blockers.append("project_structure_governance_planning_missing")

    dryrun_root = roots["structure_map_dryrun"]["root"]
    inventory_payload = _try_read_json(dryrun_root / "module_inventory.json") if dryrun_root else {}
    map_payload = _try_read_json(dryrun_root / "current_to_target_structure_map.json") if dryrun_root else {}
    dryrun_risks = (_try_read_json(dryrun_root / "migration_risk_register.json") or {}).get("risks", []) if dryrun_root else []

    entries: List[Dict[str, Any]] = inventory_payload.get("inventory_entries") or map_payload.get("map_rows") or []

    by_action: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in entries:
        by_action[e.get("disposition_action", "keep")].append(e)

    def _register(action: str) -> Dict[str, Any]:
        items = by_action.get(action, [])
        rows = [_consolidation_row(e, plan_id=f"{action}_{i:05d}", action=action) for i, e in enumerate(items)]
        groups = _group_by_target(items, action)
        return {
            "planned_action": action,
            "row_count": len(rows),
            "rows": rows,
            "consolidation_groups": groups,
            "group_count": len(groups),
            "all_rows_have_future_life_system_mapping": all(r.get("future_life_system_mapping") for r in rows),
            "execution_status": "planning_only",
            "actual_move_executed": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

    merge_plan_register = _register("merge")
    archive_plan_register = _register("archive")
    split_plan_register = _register("split")
    keep_plan_register = _register("keep")
    defer_plan_register = _register("defer")

    consolidation_batch_sequence = _batch_sequence(
        merge_plan_register.get("consolidation_groups", []),
        archive_plan_register.get("consolidation_groups", []),
        split_plan_register.get("consolidation_groups", []),
        keep_plan_register.get("consolidation_groups", []),
        defer_plan_register.get("consolidation_groups", []),
    )
    consolidation_dependency_graph = _dependency_graph()
    life_system_consolidation_matrix = _life_system_consolidation_matrix(entries)

    developer_backend_consolidation_plan = _domain_plan(entries, filter_key="is_developer_backend", filter_val=True, plan_name="developer_backend")
    midplatform_consolidation_plan = _domain_plan(entries, filter_key="is_midplatform_organ", filter_val=True, plan_name="midplatform")
    cognition_placeholder_consolidation_plan = _domain_plan(entries, filter_key="is_cognition_placeholder", filter_val=True, plan_name="cognition_placeholder")
    client_boundary_consolidation_plan = _domain_plan(entries, filter_key="is_client", filter_val=True, plan_name="client_boundary")

    consolidation_risk_register = _consolidation_risk_register(dryrun_risks, entries)
    no_file_move_boundary_report = _no_file_move_boundary_report()

    all_registers = [merge_plan_register, archive_plan_register, split_plan_register, keep_plan_register, defer_plan_register]
    all_rows_have_life = all(r.get("all_rows_have_future_life_system_mapping") for r in all_registers)
    boundary_ok = not blockers and all_rows_have_life and life_system_consolidation_matrix.get("all_rows_have_future_life_system_mapping")

    consolidation_planning_policy = {
        "planning_id": PLANNING_ID,
        "planning_scope": PLANNING_SCOPE,
        "source_structure_map_dryrun_ref": "structure_map_dryrun_root",
        "merge_plan_register_ref": "merge_plan_register.json",
        "archive_plan_register_ref": "archive_plan_register.json",
        "split_plan_register_ref": "split_plan_register.json",
        "keep_plan_register_ref": "keep_plan_register.json",
        "defer_plan_register_ref": "defer_plan_register.json",
        "consolidation_batch_sequence_ref": "consolidation_batch_sequence.json",
        "life_system_consolidation_matrix_ref": "life_system_consolidation_matrix.json",
        "no_file_move_boundary_ref": "no_file_move_boundary_report.json",
        "future_life_system_mapping_required": True,
        "actual_consolidation_execution": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "structure_map_dryrun_input_loaded": dryrun_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_planning_input_loaded": roots["gate_taxonomy_planning"]["loaded"],
        "merge_plan_register_generated": True,
        "archive_plan_register_generated": True,
        "split_plan_register_generated": True,
        "keep_plan_register_generated": True,
        "defer_plan_register_generated": True,
        "consolidation_batch_sequence_generated": True,
        "consolidation_dependency_graph_generated": True,
        "life_system_consolidation_matrix_generated": True,
        "developer_backend_consolidation_plan_generated": True,
        "midplatform_consolidation_plan_generated": True,
        "cognition_placeholder_consolidation_plan_generated": True,
        "client_boundary_consolidation_plan_generated": True,
        "consolidation_risk_register_generated": True,
        "no_file_move_boundary_report_generated": True,
        "inventory_entry_count": len(entries),
        "merge_row_count": merge_plan_register.get("row_count", 0),
        "archive_row_count": archive_plan_register.get("row_count", 0),
        "split_row_count": split_plan_register.get("row_count", 0),
        "keep_row_count": keep_plan_register.get("row_count", 0),
        "defer_row_count": defer_plan_register.get("row_count", 0),
        "consolidation_batch_count": consolidation_batch_sequence.get("batch_count", 0),
        "life_system_consolidation_row_count": life_system_consolidation_matrix.get("row_count", 0),
        "all_plan_rows_have_future_life_system_mapping": all_rows_have_life,
        "future_life_system_mapping_required": True,
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "actual_consolidation_execution": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "consolidation plans frozen; next is consolidation dryrun to simulate batch execution without file moves",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "consolidation_planning_policy": consolidation_planning_policy,
        "merge_plan_register": merge_plan_register,
        "archive_plan_register": archive_plan_register,
        "split_plan_register": split_plan_register,
        "keep_plan_register": keep_plan_register,
        "defer_plan_register": defer_plan_register,
        "consolidation_batch_sequence": consolidation_batch_sequence,
        "consolidation_dependency_graph": consolidation_dependency_graph,
        "life_system_consolidation_matrix": life_system_consolidation_matrix,
        "developer_backend_consolidation_plan": developer_backend_consolidation_plan,
        "midplatform_consolidation_plan": midplatform_consolidation_plan,
        "cognition_placeholder_consolidation_plan": cognition_placeholder_consolidation_plan,
        "client_boundary_consolidation_plan": client_boundary_consolidation_plan,
        "consolidation_risk_register": consolidation_risk_register,
        "no_file_move_boundary_report": no_file_move_boundary_report,
        "next_phase_recommendation": next_phase_recommendation,
    }
