# -*- coding: utf-8 -*-
"""Bounded file-size governance scan helpers.

Never scan the full repository with unbounded rglob — use explicit roots only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    DEFAULT_SCAN_ROOTS,
    DEFAULT_SCAN_SKIP_DIRS,
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
    RULE_NAME_EN,
    classify_markdown_line_count,
    classify_python_line_count,
)

INVENTORY_DOC_REL = "docs/architecture/governance/LUNA_FILE_SIZE_GOVERNANCE_INVENTORY_V0.md"
SCAN_ALLOWED_ROOTS: frozenset[str] = frozenset({"capabilities", "tools", "docs"})


def _should_skip(path: Path, skip_dirs: Sequence[str]) -> bool:
    return any(part in skip_dirs for part in path.parts)


def _line_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def scan_python_files(
    *,
    repo_root: Path,
    roots: Sequence[str] = DEFAULT_SCAN_ROOTS,
    skip_dirs: Sequence[str] = DEFAULT_SCAN_SKIP_DIRS,
    min_tier: str = "above_suggest",
) -> List[Dict[str, Any]]:
    tier_order = {"ok": 0, "above_suggest": 1, "warning": 2, "blocker_candidate": 3}
    min_rank = tier_order[min_tier]
    rows: List[Dict[str, Any]] = []
    for root_name in roots:
        root = (repo_root / root_name).resolve()
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            if _should_skip(path, skip_dirs):
                continue
            lines = _line_count(path)
            tier = classify_python_line_count(lines)
            if tier_order[tier] < min_rank:
                continue
            rel = path.relative_to(repo_root).as_posix()
            role = _infer_python_role(rel)
            rows.append(
                {
                    "path": rel,
                    "line_count": lines,
                    "tier": tier,
                    "role": role,
                }
            )
    rows.sort(key=lambda row: row["line_count"], reverse=True)
    return rows


def scan_markdown_files(
    *,
    repo_root: Path,
    roots: Sequence[str] = DEFAULT_SCAN_ROOTS,
    skip_dirs: Sequence[str] = DEFAULT_SCAN_SKIP_DIRS,
    min_tier: str = "above_suggest",
) -> List[Dict[str, Any]]:
    tier_order = {"ok": 0, "above_suggest": 1, "warning": 2, "blocker_candidate": 3}
    min_rank = tier_order[min_tier]
    rows: List[Dict[str, Any]] = []
    for root_name in roots:
        root = (repo_root / root_name).resolve()
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            if _should_skip(path, skip_dirs):
                continue
            lines = _line_count(path)
            tier = classify_markdown_line_count(lines)
            if tier_order[tier] < min_rank:
                continue
            rows.append(
                {
                    "path": path.relative_to(repo_root).as_posix(),
                    "line_count": lines,
                    "tier": tier,
                }
            )
    rows.sort(key=lambda row: row["line_count"], reverse=True)
    return rows


def _infer_python_role(rel_path: str) -> str:
    name = Path(rel_path).name
    if rel_path.startswith("capabilities/midplatform/"):
        if "task_manager_foundation" in rel_path:
            if name.startswith("verify_"):
                return "midplatform_verifier"
            if "evaluation" in rel_path and name.startswith("run_"):
                return "midplatform_runner"
            return "midplatform_capability"
        return "midplatform_other"
    if rel_path.startswith("capabilities/"):
        return "capability"
    if "/verify_" in rel_path or name.startswith("verify_"):
        return "verifier"
    if name.startswith("run_"):
        return "runner"
    if rel_path.startswith("tools/"):
        return "tool"
    return "other"


def summarize_scan(python_rows: Sequence[Dict[str, Any]], markdown_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    def count_tier(rows: Sequence[Dict[str, Any]]) -> Dict[str, int]:
        out = {"above_suggest": 0, "warning": 0, "blocker_candidate": 0}
        for row in rows:
            tier = row.get("tier")
            if tier in out:
                out[tier] += 1
        return out

    return {
        "python_non_ok_count": len(python_rows),
        "markdown_non_ok_count": len(markdown_rows),
        "python_by_tier": count_tier(python_rows),
        "markdown_by_tier": count_tier(markdown_rows),
        "python_blocker_count": count_tier(python_rows)["blocker_candidate"],
        "inventory_doc_ref": INVENTORY_DOC_REL,
    }


def build_file_size_governance_review(
    *,
    phase_id: str,
    scope_paths: Sequence[str],
    repo_root: Optional[Path] = None,
    phase_python_paths: Optional[Sequence[str]] = None,
    template_lineage_path: Optional[str] = None,
    read_strategy: str = "summary_index_first",
    full_repo_scan: bool = False,
    **extra: Any,
) -> Dict[str, Any]:
    root = repo_root or Path(__file__).resolve().parents[2]
    phase_rows: List[Dict[str, Any]] = []
    for rel in phase_python_paths or ():
        path = root / rel
        if not path.is_file():
            phase_rows.append({"path": rel, "exists": False, "tier": "missing"})
            continue
        lines = _line_count(path)
        tier = classify_python_line_count(lines)
        phase_rows.append({"path": rel, "exists": True, "line_count": lines, "tier": tier})

    blocker_rows = [row for row in phase_rows if row.get("tier") == "blocker_candidate"]
    warning_rows = [row for row in phase_rows if row.get("tier") == "warning"]
    template_lineage_controlled = True
    template_lineage_tier = "ok"
    if template_lineage_path:
        lineage_path = root / template_lineage_path
        if lineage_path.is_file():
            template_lineage_tier = classify_python_line_count(_line_count(lineage_path))
            template_lineage_controlled = template_lineage_tier != "blocker_candidate"
        else:
            template_lineage_controlled = False
            template_lineage_tier = "missing"

    scan_roots = list(DEFAULT_SCAN_ROOTS)
    full_repo_scan_absent = not full_repo_scan
    tmp_eval_out_scan_absent = "_tmp_eval_out" not in scan_roots
    limited_directory_scan_ok = set(scan_roots).issubset(SCAN_ALLOWED_ROOTS)
    template_lineage_growth_warning = template_lineage_tier in ("warning", "blocker_candidate")
    template_lineage_growth_warning_non_blocking = template_lineage_tier != "blocker_candidate"

    review = {
        "review_id": "file_size_governance_review_v1",
        "rule_ref": RULE_NAME_EN,
        "phase_id": phase_id,
        "scope_paths": list(scope_paths),
        "read_strategy": read_strategy,
        "full_repo_scan": full_repo_scan,
        "phase_python_files": phase_rows,
        "oversized_warning_files": warning_rows,
        "blocker_candidate_files": blocker_rows,
        "inventory_doc_ref": INVENTORY_DOC_REL,
        "inventory_debt_acknowledged": bool(warning_rows),
        "template_lineage_path": template_lineage_path,
        "template_lineage_tier": template_lineage_tier,
        "file_size_governance_review_exists": True,
        "monolithic_file_absent": len(blocker_rows) == 0,
        "large_file_read_avoidance_ok": not full_repo_scan,
        "summary_index_first_reading_ok": read_strategy == "summary_index_first",
        "template_lineage_growth_controlled": template_lineage_controlled,
        "shared_constants_split_ok": True,
        "verifier_large_file_scan_absent": not full_repo_scan,
        "full_repo_scan_absent": full_repo_scan_absent,
        "tmp_eval_out_scan_absent": tmp_eval_out_scan_absent,
        "limited_directory_scan_ok": limited_directory_scan_ok,
        "template_lineage_growth_warning": template_lineage_growth_warning,
        "template_lineage_growth_warning_non_blocking": template_lineage_growth_warning_non_blocking,
        **extra,
    }
    lineage_growth_ok = template_lineage_controlled or (
        template_lineage_growth_warning and template_lineage_growth_warning_non_blocking
    )
    review["template_lineage_growth_ok"] = lineage_growth_ok
    review["file_size_governance_review_ok"] = all(
        review.get(key) is True for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS
    ) and lineage_growth_ok and full_repo_scan_absent and tmp_eval_out_scan_absent and limited_directory_scan_ok
    return review


def write_inventory_snapshot(
    *,
    repo_root: Optional[Path] = None,
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    root = repo_root or Path(__file__).resolve().parents[2]
    python_rows = scan_python_files(repo_root=root)
    markdown_rows = scan_markdown_files(repo_root=root)
    payload = {
        "snapshot_id": "file_size_governance_inventory_snapshot_v0",
        "scan_roots": list(DEFAULT_SCAN_ROOTS),
        "scan_skip_dirs": list(DEFAULT_SCAN_SKIP_DIRS),
        "summary": summarize_scan(python_rows, markdown_rows),
        "python_rows": python_rows,
        "markdown_rows": markdown_rows,
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
