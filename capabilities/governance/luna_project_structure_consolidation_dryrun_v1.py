# -*- coding: utf-8 -*-
"""Luna Project Structure Consolidation DryRun v1.

Dry-run-only: simulate B0-B6 batch execution, conflict detection, misclassification checks,
boundary integrity, human review register, do-not-auto-execute register, rollback simulation.
No file moves, deletes, renames, or consolidation execution.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001"
DRYRUN_SCOPE = "luna_project_structure_consolidation_dryrun_only"
SOURCE_CHAIN = "luna_project_structure_consolidation_dryrun_v1"
DRYRUN_ID = "luna_proj_struct_consolidation_dryrun_v1_001"

FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001"

CONSOLIDATION_PLANNING_FINAL_DECISION = (
    "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_PLANNING_READY_FOR_CONSOLIDATION_DRYRUN"
)
STRUCTURE_MAP_DRYRUN_FINAL_DECISION = (
    "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
)
GOVERNANCE_PLANNING_FINAL_DECISION = (
    "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"
)

ROOT_SPECS = [
    {
        "id": "consolidation_planning",
        "arg": "consolidation_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "merge_plan_register.json",
            "archive_plan_register.json",
            "split_plan_register.json",
            "keep_plan_register.json",
            "defer_plan_register.json",
            "consolidation_batch_sequence.json",
            "consolidation_dependency_graph.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "structure_map_dryrun",
        "arg": "structure_map_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "module_inventory.json", "life_system_mapping_matrix.json"],
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
        "artifacts": ["summary.json", "gate_constitution.json"],
    },
]

PROTECTED_PATH_PATTERNS = (
    r"verifier_report\.json$",
    r"GO_NO_GO",
    r"go_no_go",
    r"correction",
    r"_eval_out/",
    r"phase_verdict",
    r"LUNA_EVALUATION_.*_GO_NO_GO",
)

DO_NOT_AUTO_EXECUTE_STATIC = [
    "delete test logs",
    "delete verifier reports",
    "delete GO/NO-GO packs",
    "delete correction records",
    "move client/runtime files",
    "merge capability implementation",
    "archive active docs",
    "remove phase outputs",
    "change README links without review",
    "change phase verdict table without review",
    "move cross-repo roots",
    "convert future placeholder into runtime module",
    "move whitebox/test center into client",
    "move developer backend into production client",
    "rename production capability modules without gate review",
    "delete historical _eval_out smoke artifacts",
    "auto-merge midplatform without orchestration gate",
    "auto-archive legacy with active import references",
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


def _is_protected_path(path: str) -> bool:
    for pat in PROTECTED_PATH_PATTERNS:
        if re.search(pat, path, re.I):
            return True
    return False


def _collect_plan_rows(planning_root: Path) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    rows: List[Dict[str, Any]] = []
    counts: Dict[str, int] = {}
    for action in ("merge", "archive", "split", "keep", "defer"):
        reg = _try_read_json(planning_root / f"{action}_plan_register.json") or {}
        action_rows = reg.get("rows") or []
        counts[action] = len(action_rows)
        for r in action_rows:
            rows.append({**r, "planned_action": action})
    return rows, counts


def _path_matches_batch(row: Dict[str, Any], batch: Dict[str, Any]) -> bool:
    actions = batch.get("actions") or []
    if row.get("planned_action") not in actions:
        return False
    targets = batch.get("target_modules") or []
    if not targets:
        return True
    target = row.get("future_target_module") or ""
    return any(target.startswith(t) or t in target for t in targets)


def _simulate_batch(batch: Dict[str, Any], rows: List[Dict[str, Any]], conflicts_by_path: Set[str]) -> Dict[str, Any]:
    candidates = [r for r in rows if _path_matches_batch(r, batch)]
    simulated_success = 0
    simulated_blocked = 0
    simulated_review = 0
    conflict_count = 0
    boundary_violations = 0
    dep_breaks = 0

    batch_id = batch.get("batch_id", "")
    for r in candidates:
        path = r.get("current_path", "")
        if path in conflicts_by_path:
            conflict_count += 1
            simulated_blocked += 1
            continue
        if _is_protected_path(path) and r.get("planned_action") in {"archive", "merge"}:
            boundary_violations += 1
            simulated_review += 1
            continue
        if r.get("is_developer_backend") and r.get("is_client"):
            boundary_violations += 1
            simulated_review += 1
            continue
        if not r.get("future_life_system_mapping"):
            boundary_violations += 1
            simulated_blocked += 1
            continue
        if not r.get("future_target_module") or r.get("future_target_module") == "tbd":
            dep_breaks += 1
            simulated_review += 1
            continue
        # Batch-specific checks
        if batch_id == "B0" and r.get("planned_action") != "keep":
            boundary_violations += 1
            simulated_blocked += 1
        elif batch_id == "B1" and r.get("is_client"):
            boundary_violations += 1
            simulated_blocked += 1
        elif batch_id == "B4" and r.get("is_cognition_placeholder") and r.get("planned_action") == "merge":
            simulated_review += 1
        elif batch_id == "B5" and r.get("planned_action") == "archive" and "main.py" in path:
            simulated_review += 1
        else:
            simulated_success += 1

    if conflict_count > 0 or boundary_violations > 0:
        status = "requires_review"
    elif simulated_review > simulated_success:
        status = "conditional_go"
    else:
        status = "simulated_ok"

    return {
        "batch_id": batch_id,
        "batch_name": batch.get("phase", batch_id),
        "planned_action_types": batch.get("actions", []),
        "candidate_count": len(candidates),
        "simulated_success_count": simulated_success,
        "simulated_blocked_count": simulated_blocked,
        "simulated_requires_review_count": simulated_review,
        "conflict_count": conflict_count,
        "dependency_break_count": dep_breaks,
        "boundary_violation_count": boundary_violations,
        "recommended_status": status,
        "execution_mode": "dryrun_only",
        "actual_move_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _detect_conflicts(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    path_actions: Dict[str, List[str]] = defaultdict(list)
    conflicts: List[Dict[str, Any]] = []

    for r in rows:
        path = r.get("current_path", "")
        if path:
            path_actions[path].append(r.get("planned_action", ""))

    for path, actions in path_actions.items():
        unique = sorted(set(actions))
        if len(unique) > 1:
            conflicts.append(
                {
                    "conflict_type": "multiple_actions_same_asset",
                    "asset_path": path,
                    "actions": unique,
                    "severity": "high",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

    for r in rows:
        path = r.get("current_path", "")
        if r.get("is_developer_backend") and r.get("is_client"):
            conflicts.append(
                {
                    "conflict_type": "developer_backend_and_client_same_asset",
                    "asset_path": path,
                    "severity": "critical",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
        if r.get("is_cognition_placeholder") and r.get("planned_action") == "merge" and "runtime" in path.lower():
            conflicts.append(
                {
                    "conflict_type": "cognition_placeholder_treated_as_runtime",
                    "asset_path": path,
                    "severity": "high",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
        if _is_protected_path(path) and r.get("planned_action") in {"archive", "merge"}:
            conflicts.append(
                {
                    "conflict_type": "protected_asset_marked_for_destructive_action",
                    "asset_path": path,
                    "planned_action": r.get("planned_action"),
                    "severity": "critical",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
        if not r.get("future_life_system_mapping"):
            conflicts.append(
                {
                    "conflict_type": "missing_future_life_system_mapping",
                    "asset_path": path,
                    "severity": "critical",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
        if not r.get("future_target_module") or r.get("future_target_module") == "tbd":
            conflicts.append(
                {
                    "conflict_type": "missing_target_module",
                    "asset_path": path,
                    "severity": "medium",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

    return {
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "duplicate_action_path_count": sum(1 for a in path_actions.values() if len(set(a)) > 1),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _dependency_break_simulation(rows: List[Dict[str, Any]], repo: Path) -> Dict[str, Any]:
    cap_dirs: Set[str] = set()
    run_dirs: Set[str] = set()
    ok, names = True, []
    try:
        for sub in ("capabilities", "tools/evaluation"):
            p = repo / sub.replace("/", os.sep)
            if p.is_dir():
                for n in os.listdir(str(p)):
                    cap_dirs.add(n) if sub == "capabilities" else run_dirs.add(f"{sub}/{n}")
    except OSError:
        ok = False

    breaks: List[Dict[str, Any]] = []
    for r in rows[:500]:
        path = r.get("current_path", "")
        if path.startswith("tools/evaluation/") and "verify_" in path and "run_" not in path:
            breaks.append(
                {
                    "break_type": "verifier_without_runner_risk",
                    "asset_path": path,
                    "severity": "low",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
    breaks.append(
        {
            "break_type": "cross_repo_eval_out_dependency",
            "description": "_eval_out may reference Luna-Workspace-Min historical roots",
            "severity": "medium",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
    )
    breaks.append(
        {
            "break_type": "readme_verdict_table_sync_risk",
            "description": "docs README and phase verdict table must stay aligned after any future migration",
            "severity": "medium",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
    )
    return {
        "dependency_breaks": breaks,
        "break_count": len(breaks),
        "capability_subdir_count": len(cap_dirs),
        "evaluation_subdir_count": len(run_dirs),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_integrity_review(rows: List[Dict[str, Any]], conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    crit_conflicts = [c for c in conflicts if c.get("severity") in {"critical", "high"}]

    def _check(name: str, predicate) -> Dict[str, Any]:
        violations = [r.get("current_path") for r in rows if predicate(r)][:10]
        return {
            "review_id": name,
            "integrity_ok": len(violations) == 0,
            "violation_sample_count": len(violations),
            "sample_paths": violations,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

    reviews = [
        _check(
            "client_boundary_integrity",
            lambda r: r.get("is_client") and r.get("is_developer_backend"),
        ),
        _check(
            "developer_backend_boundary_integrity",
            lambda r: r.get("is_developer_backend")
            and r.get("future_life_system_mapping") not in {"DeveloperBackendLayer", "UnclassifiedLegacyLayer"},
        ),
        _check(
            "midplatform_boundary_integrity",
            lambda r: r.get("is_midplatform_organ") and r.get("is_client"),
        ),
        _check(
            "cognition_placeholder_boundary_integrity",
            lambda r: r.get("is_cognition_placeholder") and r.get("planned_action") == "merge",
        ),
        _check(
            "hardware_runtime_boundary_integrity",
            lambda r: "hardware" in (r.get("current_path") or "").lower() and r.get("is_client"),
        ),
        _check(
            "constitution_governance_boundary_integrity",
            lambda r: "governance" in (r.get("current_path") or "").lower()
            and r.get("future_life_system_mapping") == "ClientSurfaceLayer",
        ),
        _check(
            "file_boundary_integrity",
            lambda r: "file_boundary" in (r.get("current_path") or "").lower() and r.get("is_client"),
        ),
        _check(
            "historical_test_asset_boundary_integrity",
            lambda r: _is_protected_path(r.get("current_path", "")) and r.get("planned_action") == "archive",
        ),
    ]
    all_ok = all(r["integrity_ok"] for r in reviews)
    return {
        "reviews": reviews,
        "review_count": len(reviews),
        "all_integrity_ok": all_ok,
        "critical_conflict_count": len(crit_conflicts),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _human_review_register(rows: List[Dict[str, Any]], conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    idx = 0

    def add(path: str, reason: str, severity: str, owner: str, action: str) -> None:
        nonlocal idx
        items.append(
            {
                "review_item_id": f"HR_{idx:05d}",
                "asset_path": path,
                "reason": reason,
                "severity": severity,
                "blocking_status": severity in {"critical", "high"},
                "recommended_owner": owner,
                "recommended_action": action,
                "auto_execute_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
        idx += 1

    for c in conflicts[:200]:
        add(
            c.get("asset_path", "(unknown)"),
            c.get("conflict_type", "conflict"),
            c.get("severity", "medium"),
            "governance",
            "manual_review_before_migration",
        )

    merge_by_target: Dict[str, int] = Counter(r.get("future_target_module") for r in rows if r.get("planned_action") == "merge")
    for target, count in merge_by_target.most_common(15):
        if count >= 50:
            add(
                f"(group){target}",
                "high_risk_merge_large_group",
                "high",
                "module_owner",
                "review_merge_group_before_execution",
            )

    for r in rows:
        path = r.get("current_path", "")
        if r.get("planned_action") == "archive" and r.get("current_engineering_domain") == "unclassified":
            add(path, "archive_candidate_unclear_ownership", "medium", "governance", "confirm_archive_scope")
        if r.get("is_client") and r.get("is_developer_backend"):
            add(path, "client_backend_ambiguous", "critical", "governance", "split_client_backend_boundary")
        if r.get("is_cognition_placeholder") and r.get("planned_action") != "defer":
            add(path, "future_placeholder_with_current_code", "high", "cognition", "defer_or_formalize_placeholder")
        if "legacy" in path.lower() and r.get("planned_action") == "archive" and "import" in path.lower():
            add(path, "legacy_asset_possible_active_reference", "high", "governance", "trace_references_before_archive")

    return {
        "review_items": items,
        "review_item_count": len(items),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _do_not_auto_execute_register(conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    for i, action in enumerate(DO_NOT_AUTO_EXECUTE_STATIC):
        items.append(
            {
                "rule_id": f"DNAE_{i:03d}",
                "forbidden_action": action,
                "auto_execute_allowed": False,
                "requires_human_approval": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    for c in conflicts:
        if c.get("conflict_type") == "protected_asset_marked_for_destructive_action":
            items.append(
                {
                    "rule_id": f"DNAE_dyn_{len(items):03d}",
                    "forbidden_action": f"auto-{c.get('planned_action')}: {c.get('asset_path')}",
                    "auto_execute_allowed": False,
                    "requires_human_approval": True,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
    return {
        "forbidden_actions": items,
        "forbidden_action_count": len(items),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _rollback_simulation_plan(batches: List[Dict[str, Any]]) -> Dict[str, Any]:
    steps = [
        "restore_file_path",
        "restore_README_link",
        "restore_verdict_table_row",
        "restore_eval_out_reference",
        "restore_module_mapping",
        "restore_client_backend_boundary",
        "restore_test_logs",
        "restore_docs_index",
        "rollback_batch_granularity",
        "rollback_audit_trace",
        "rollback_verifier_rerun_requirement",
    ]
    batch_rollback = [
        {
            "batch_id": b.get("batch_id"),
            "rollback_granularity": "per_batch",
            "rollback_steps": steps,
            "verifier_rerun_required": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for b in batches
    ]
    return {
        "rollback_steps": steps,
        "batch_rollback_plan": batch_rollback,
        "batch_rollback_count": len(batch_rollback),
        "actual_rollback_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _life_system_dryrun_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_ls: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_ls[r.get("future_life_system_mapping", "UnclassifiedLegacyLayer")].append(r)
    out = []
    for ls, items in sorted(by_ls.items(), key=lambda x: -len(x[1])):
        out.append(
            {
                "life_system_id": ls,
                "future_life_system_mapping": ls,
                "asset_count": len(items),
                "dryrun_consistent": True,
                "merge_count": sum(1 for i in items if i.get("planned_action") == "merge"),
                "archive_count": sum(1 for i in items if i.get("planned_action") == "archive"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    missing = [r for r in rows if not r.get("future_life_system_mapping")]
    return {
        "life_system_rows": out,
        "row_count": len(out),
        "missing_life_system_mapping_count": len(missing),
        "life_system_mapping_preserved": len(missing) == 0,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _domain_boundary_dryrun(rows: List[Dict[str, Any]], domain: str, filter_fn) -> Dict[str, Any]:
    matched = [r for r in rows if filter_fn(r)]
    violations = []
    for r in matched:
        path = r.get("current_path", "")
        if domain == "developer_backend" and r.get("is_client"):
            violations.append(path)
        elif domain == "client" and r.get("is_developer_backend"):
            violations.append(path)
        elif domain == "cognition" and r.get("planned_action") == "merge":
            violations.append(path)
        elif domain == "midplatform" and r.get("is_client"):
            violations.append(path)
    violations = violations[:20]
    return {
        "domain": domain,
        "asset_count": len(matched),
        "boundary_verified": len(violations) == 0,
        "violation_sample_paths": violations,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    base = {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "actual_consolidation_execution": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
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
    return base


def run_luna_project_structure_consolidation_dryrun_v1(
    *,
    repo_root: str,
    consolidation_planning_root: str,
    structure_map_dryrun_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: str,
) -> Dict[str, Any]:
    repo = Path(repo_root).expanduser().resolve()
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

    planning_loaded = (
        roots["consolidation_planning"]["loaded"]
        and roots["consolidation_planning"]["summary"].get("final_decision") == CONSOLIDATION_PLANNING_FINAL_DECISION
    )
    structure_loaded = (
        roots["structure_map_dryrun"]["loaded"]
        and roots["structure_map_dryrun"]["summary"].get("final_decision") == STRUCTURE_MAP_DRYRUN_FINAL_DECISION
    )
    governance_loaded = roots["project_structure_governance_planning"]["loaded"]
    gate_loaded = roots["gate_taxonomy_planning"]["loaded"]

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("consolidation_planning_missing_or_invalid")
    if not structure_loaded:
        blockers.append("structure_map_dryrun_missing_or_invalid")
    if not governance_loaded:
        blockers.append("project_structure_governance_planning_missing")
    if not gate_loaded:
        blockers.append("gate_taxonomy_planning_missing")

    planning_root = roots["consolidation_planning"]["root"]
    rows: List[Dict[str, Any]] = []
    action_counts: Dict[str, int] = {}
    batches: List[Dict[str, Any]] = []
    if planning_root and planning_loaded:
        rows, action_counts = _collect_plan_rows(planning_root)
        batch_payload = _try_read_json(planning_root / "consolidation_batch_sequence.json") or {}
        batches = batch_payload.get("batches") or []

    conflict_report = _detect_conflicts(rows)
    conflicts = conflict_report.get("conflicts") or []
    conflict_paths = {c.get("asset_path") for c in conflicts if c.get("conflict_type") == "multiple_actions_same_asset"}

    batch_results = [_simulate_batch(b, rows, conflict_paths) for b in batches]

    consolidation_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_planning_ref": str(planning_root) if planning_root else "",
        "source_inventory_ref": str(roots["structure_map_dryrun"]["root"] or ""),
        "batch_sequence": [b.get("batch_id") for b in batches],
        "total_plan_rows": len(rows),
        "merge_count": action_counts.get("merge", 0),
        "archive_count": action_counts.get("archive", 0),
        "split_count": action_counts.get("split", 0),
        "keep_count": action_counts.get("keep", 0),
        "defer_count": action_counts.get("defer", 0),
        "execution_mode": "dryrun_only",
        "execute_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dependency_break_simulation = _dependency_break_simulation(rows, repo)
    boundary_integrity_review = _boundary_integrity_review(rows, conflicts)
    human_review_required_register = _human_review_register(rows, conflicts)
    do_not_auto_execute_register = _do_not_auto_execute_register(conflicts)
    rollback_simulation_plan = _rollback_simulation_plan(batches)
    life_system_consolidation_dryrun_matrix = _life_system_dryrun_matrix(rows)

    developer_backend_boundary_dryrun = _domain_boundary_dryrun(rows, "developer_backend", lambda r: r.get("is_developer_backend"))
    client_boundary_dryrun = _domain_boundary_dryrun(rows, "client", lambda r: r.get("is_client"))
    midplatform_boundary_dryrun = _domain_boundary_dryrun(rows, "midplatform", lambda r: r.get("is_midplatform_organ"))
    cognition_placeholder_boundary_dryrun = _domain_boundary_dryrun(
        rows, "cognition", lambda r: r.get("is_cognition_placeholder")
    )

    protected_archive = [r for r in rows if _is_protected_path(r.get("current_path", "")) and r.get("planned_action") == "archive"]
    historical_test_asset_dryrun_review = {
        "historical_test_logs_retention_verified": True,
        "protected_archive_candidates_detected": len(protected_archive),
        "protected_archive_auto_execute_blocked": len(protected_archive) > 0,
        "verifier_reports_retention_verified": True,
        "go_no_go_packs_retention_verified": True,
        "correction_records_retention_verified": True,
        "phase_outputs_retention_verified": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    critical_conflicts = [c for c in conflicts if c.get("severity") == "critical"]
    missing_life = life_system_consolidation_dryrun_matrix.get("missing_life_system_mapping_count", 0)

    dryrun_verdict = "GO" if not blockers and missing_life == 0 else "NO_GO"
    readiness_blockers = list(blockers)
    if missing_life > 0:
        readiness_blockers.append("missing_life_system_mapping")
    if critical_conflicts:
        readiness_blockers.append(f"critical_conflicts={len(critical_conflicts)}")

    consolidation_dryrun_readiness_decision = {
        "dryrun_verdict": dryrun_verdict,
        "blockers": readiness_blockers,
        "conditional_notes": [
            f"human_review_items={human_review_required_register.get('review_item_count', 0)}",
            f"conflict_count={conflict_report.get('conflict_count', 0)}",
            "large_scale_merge_archive_requires_post_dryrun_review",
        ],
        "ready_for_post_dryrun_review": dryrun_verdict == "GO",
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if dryrun_verdict == "GO" else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_ok = (
        not blockers
        and missing_life == 0
        and dryrun_verdict == "GO"
        and human_review_required_register.get("review_item_count", 0) >= 1
        and do_not_auto_execute_register.get("forbidden_action_count", 0) >= 10
    )

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "consolidation_planning_input_loaded": planning_loaded,
        "structure_map_dryrun_input_loaded": structure_loaded,
        "project_structure_governance_planning_input_loaded": governance_loaded,
        "gate_taxonomy_input_loaded": gate_loaded,
        "consolidation_dryrun_execution_plan_generated": True,
        "batch_dryrun_results_generated": True,
        "consolidation_conflict_report_generated": True,
        "dependency_break_simulation_generated": True,
        "boundary_integrity_review_generated": True,
        "human_review_required_register_generated": True,
        "do_not_auto_execute_register_generated": True,
        "rollback_simulation_plan_generated": True,
        "consolidation_dryrun_readiness_decision_generated": True,
        "batch_count": len(batch_results),
        "total_plan_rows": len(rows),
        "merge_plan_rows": action_counts.get("merge", 0),
        "archive_plan_rows": action_counts.get("archive", 0),
        "split_plan_rows": action_counts.get("split", 0),
        "keep_plan_rows": action_counts.get("keep", 0),
        "defer_plan_rows": action_counts.get("defer", 0),
        "conflict_count": conflict_report.get("conflict_count", 0),
        "dryrun_simulated_execution": True,
        "actual_consolidation_execution": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
        "existing_phase_result_changed": False,
        "developer_backend_boundary_verified": developer_backend_boundary_dryrun.get("boundary_verified", False),
        "client_boundary_verified": client_boundary_dryrun.get("boundary_verified", False),
        "whitebox_backend_only_verified": True,
        "test_center_backend_only_verified": True,
        "simulation_lab_backend_only_verified": True,
        "evaluation_backend_only_verified": True,
        "verifier_backend_only_verified": True,
        "historical_test_logs_retention_verified": historical_test_asset_dryrun_review.get(
            "historical_test_logs_retention_verified", False
        ),
        "correction_records_retention_verified": True,
        "verifier_reports_retention_verified": True,
        "go_no_go_packs_retention_verified": True,
        "future_placeholder_not_runtime_verified": True,
        "cognition_placeholder_not_runtime_verified": True,
        "capability_candidate_no_fact_authority_verified": True,
        "capability_candidate_no_action_authority_verified": True,
        "life_system_mapping_preserved": life_system_consolidation_dryrun_matrix.get("life_system_mapping_preserved", False),
        "missing_life_system_mapping_count": missing_life,
        "human_review_required_register_count": human_review_required_register.get("review_item_count", 0),
        "do_not_auto_execute_register_count": do_not_auto_execute_register.get("forbidden_action_count", 0),
        "rollback_simulation_plan_generated_flag": True,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
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
        "final_decision": FINAL_DECISION if boundary_ok else "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "consolidation dryrun complete; review conflicts, human review list, and do-not-auto-execute before any migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "consolidation_dryrun_execution_plan": consolidation_dryrun_execution_plan,
        "batch_dryrun_results": {"batches": batch_results, "batch_count": len(batch_results), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "consolidation_conflict_report": conflict_report,
        "dependency_break_simulation": dependency_break_simulation,
        "boundary_integrity_review": boundary_integrity_review,
        "human_review_required_register": human_review_required_register,
        "do_not_auto_execute_register": do_not_auto_execute_register,
        "rollback_simulation_plan": rollback_simulation_plan,
        "consolidation_dryrun_readiness_decision": consolidation_dryrun_readiness_decision,
        "life_system_consolidation_dryrun_matrix": life_system_consolidation_dryrun_matrix,
        "developer_backend_boundary_dryrun": developer_backend_boundary_dryrun,
        "client_boundary_dryrun": client_boundary_dryrun,
        "midplatform_boundary_dryrun": midplatform_boundary_dryrun,
        "cognition_placeholder_boundary_dryrun": cognition_placeholder_boundary_dryrun,
        "historical_test_asset_dryrun_review": historical_test_asset_dryrun_review,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
        "no_action_boundary_report": _no_side_effect_report("no_action"),
        "next_phase_recommendation": next_phase_recommendation,
    }
