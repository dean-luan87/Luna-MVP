# -*- coding: utf-8 -*-
"""Model workflow protocol reuse and cleanup review — scanner v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_items_v1 import (
    ACTIVE_MAINLINE_PATTERNS,
    DEFERRED_PATTERNS,
    KEEP_AS_REFERENCE_PATTERNS,
    REJECT_FROM_MAINLINE_PATTERNS,
)


def _match_any(name: str, patterns: Tuple[str, ...]) -> bool:
    nl = name.lower()
    return any(p in nl for p in patterns)


def classify_file(rel_path: str) -> Tuple[str, str]:
    name = Path(rel_path).name
    rel_l = rel_path.lower()
    if _match_any(name, REJECT_FROM_MAINLINE_PATTERNS) or "field_simulation" in rel_l:
        if _match_any(name, KEEP_AS_REFERENCE_PATTERNS) or "field_simulation_planning" in rel_l or "field_simulation_skeleton" in rel_l:
            return "keep_as_reference", "field_simulation_historical_archive_reject_from_mainline"
        return "reject_from_mainline", "field_simulation_deactivated_from_mainline"
    if _match_any(name, DEFERRED_PATTERNS):
        return "disabled", "task_reasoning_deferred_not_current_scope"
    if _match_any(name, ACTIVE_MAINLINE_PATTERNS):
        return "active", "real_model_and_field_construction_mainline"
    if "spatial_view_model" in name.lower():
        return "cleanup_required", "spatial_view_model_not_started_must_align_with_slam_priority"
    if "model_role_registry" in name.lower():
        return "cleanup_required", "model_role_registry_deferred_until_cleanup_complete"
    if "world_model" in name.lower() and "candidate" not in name.lower():
        return "cleanup_required", "world_model_entry_scope_requires_candidate_only_rewrite"
    return "keep_as_reference", "supporting_midplatform_module_review_periodically"


def scan_scope(
    repo_root: Path,
    *,
    scope_dirs: Tuple[str, ...],
) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for scope in scope_dirs:
        base = repo_root / scope
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix not in (".py", ".md", ".json"):
                continue
            if "__pycache__" in path.parts:
                continue
            rel = str(path.relative_to(repo_root))
            status, reason = classify_file(rel)
            entries.append({
                "path": rel,
                "status": status,
                "reason": reason,
                "scope": scope,
            })
    return entries


def partition_registries(entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    registries = {
        "active": [],
        "keep_as_reference": [],
        "deprecated": [],
        "disabled": [],
        "cleanup_required": [],
        "reject_from_mainline": [],
    }
    for e in entries:
        st = e.get("status", "keep_as_reference")
        path_l = e.get("path", "").lower()
        if "field_simulation" in path_l:
            registries["deprecated"].append({**e, "mainline_status": "reject_from_mainline"})
            if st == "keep_as_reference":
                registries["keep_as_reference"].append(e)
            else:
                registries["reject_from_mainline"].append(e)
            continue
        if st == "reject_from_mainline":
            registries["reject_from_mainline"].append(e)
            registries["deprecated"].append({**e, "status": "deprecated"})
        elif st in registries:
            registries[st].append(e)
        else:
            registries["keep_as_reference"].append(e)
    return registries
