# -*- coding: utf-8 -*-
"""
Reasoning Tree Metrics M0（结构树指标化 / 决策质量度量）

定位：
- 指标层是优化抓手，不是展示装饰
- M0 规则版：能算/能展示/能比较/能抓明显问题
- 指标来源必须基于 Reasoning Structure Tree（树本身的 nodes/parent/status/path）

约束：
- 只读输入 tree dict（ReasoningStructureTreeResult.to_dict()）
- 不改主逻辑
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _as_bool(x: Any) -> bool:
    return bool(x is True)


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class ReasoningTreeMetricsResult:
    tree_depth: int = 0
    branch_count: int = 0
    dead_branch_count: int = 0
    active_path_length: int = 0
    resolution_path_length: int = 0
    feedback_node_count: int = 0
    effective_feedback_count: int = 0
    prune_rate: float = 0.0
    resolved: bool = False
    blocked: bool = False
    possible_tree_issue_type: Optional[str] = None
    possible_tree_issue_reason: Optional[str] = None
    metrics_summary: Optional[str] = None
    metrics_applied: bool = False
    # optional counts
    active_node_count: int = 0
    pruned_node_count: int = 0
    resolved_node_count: int = 0
    watchlist_node_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tree_depth": int(self.tree_depth),
            "branch_count": int(self.branch_count),
            "dead_branch_count": int(self.dead_branch_count),
            "active_path_length": int(self.active_path_length),
            "resolution_path_length": int(self.resolution_path_length),
            "feedback_node_count": int(self.feedback_node_count),
            "effective_feedback_count": int(self.effective_feedback_count),
            "prune_rate": float(self.prune_rate),
            "resolved": bool(self.resolved),
            "blocked": bool(self.blocked),
            "possible_tree_issue_type": self.possible_tree_issue_type,
            "possible_tree_issue_reason": self.possible_tree_issue_reason,
            "metrics_summary": self.metrics_summary,
            "metrics_applied": bool(self.metrics_applied),
            "active_node_count": int(self.active_node_count),
            "pruned_node_count": int(self.pruned_node_count),
            "resolved_node_count": int(self.resolved_node_count),
            "watchlist_node_count": int(self.watchlist_node_count),
        }


def _build_index(tree: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, List[str]]]:
    nodes = tree.get("nodes") or []
    by_id: Dict[str, Dict[str, Any]] = {}
    children: Dict[str, List[str]] = {}
    for n in nodes:
        if isinstance(n, dict) and n.get("node_id"):
            by_id[str(n["node_id"])] = n
    for nid, n in by_id.items():
        pid = n.get("parent_node_id")
        if pid and str(pid) in by_id:
            children.setdefault(str(pid), []).append(nid)
    return by_id, children


def _compute_depth(children: Dict[str, List[str]], root_id: str) -> int:
    if not root_id:
        return 0
    max_depth = 1
    stack = [(root_id, 1)]
    seen = set()
    while stack:
        nid, d = stack.pop()
        if (nid, d) in seen:
            continue
        seen.add((nid, d))
        max_depth = max(max_depth, d)
        for ch in children.get(nid, []):
            stack.append((ch, d + 1))
    return max_depth


def _path_len_to_root(by_id: Dict[str, Dict[str, Any]], node_id: str, root_id: str) -> int:
    if not node_id or node_id not in by_id or not root_id:
        return 0
    cur = node_id
    steps = 1
    guard = 0
    while cur and cur != root_id and guard < 200:
        guard += 1
        pid = by_id.get(cur, {}).get("parent_node_id")
        if not pid:
            break
        cur = str(pid)
        steps += 1
    return steps if cur == root_id else steps


def build_reasoning_tree_metrics(tree: Dict[str, Any]) -> ReasoningTreeMetricsResult:
    """
    M0 指标计算：只基于 tree nodes/path/status。
    """
    root_id = _s(tree.get("root_node_id")) or ""
    resolved_id = _s(tree.get("resolved_node_id"))
    active_path = tree.get("active_path_node_ids") or []
    pruned_ids = set([str(x) for x in (tree.get("pruned_node_ids") or []) if x is not None])

    by_id, children = _build_index(tree)

    # node counts
    active_node_count = 0
    pruned_node_count = 0
    resolved_node_count = 0
    watchlist_node_count = 0
    blocked_any = False
    resolved_any = False

    for n in by_id.values():
        st = (n.get("status") or "").strip().lower()
        if st == "active":
            active_node_count += 1
        if st in ("pruned", "rejected"):
            pruned_node_count += 1
        if st == "resolved":
            resolved_node_count += 1
            resolved_any = True
        if st == "watchlist":
            watchlist_node_count += 1
        if st == "blocked":
            blocked_any = True

    # depth & branching
    depth = _compute_depth(children, root_id) if root_id else 0
    branch_count = sum(1 for pid, kids in children.items() if len(kids) >= 2)

    # dead branches: leaf nodes (or pruned ids) that are pruned/rejected/blocked and not in active path
    active_set = set([str(x) for x in active_path if x is not None])
    has_children = set(children.keys())
    leaf_ids = [nid for nid in by_id.keys() if nid not in has_children]
    dead = 0
    for nid in leaf_ids:
        st = (by_id.get(nid, {}).get("status") or "").strip().lower()
        if nid in active_set:
            continue
        if st in ("pruned", "rejected", "blocked") or nid in pruned_ids:
            dead += 1

    # path lengths
    active_path_length = len(active_set) if active_path else 0
    resolution_path_length = 0
    if resolved_id:
        resolution_path_length = _path_len_to_root(by_id, resolved_id, root_id)

    # feedback counts (tree-native)
    feedback_nodes = []
    for nid, n in by_id.items():
        if _as_bool(n.get("is_user_feedback_driven")):
            feedback_nodes.append(n)
    feedback_node_count = len(feedback_nodes)

    # effective feedback (rule): feedback-driven node that either advances next_effect, or changes status to resolved/blocked/watchlist,
    # or becomes part of active path beyond root.
    eff = 0
    for n in feedback_nodes:
        st = (n.get("status") or "").strip().lower()
        ne = (n.get("next_effect") or "").strip().lower()
        nid = str(n.get("node_id") or "")
        if ne and ne != "none":
            eff += 1
            continue
        if st in ("resolved", "blocked", "watchlist"):
            eff += 1
            continue
        if nid and nid in active_set and nid != root_id:
            eff += 1
            continue

    prune_rate = float(dead / max(branch_count, 1))
    resolved_flag = bool(resolved_any or (resolved_id and (by_id.get(resolved_id, {}).get("status") or "").strip().lower() == "resolved"))

    # minimal issue rules (M0)
    issue_type = None
    issue_reason = None
    if depth > 5:
        issue_type = "tree_too_deep"
        issue_reason = f"tree_depth={depth} > 5"
    elif branch_count > 5:
        issue_type = "too_many_branches"
        issue_reason = f"branch_count={branch_count} > 5"
    elif prune_rate > 0.6:
        issue_type = "high_dead_branch_ratio"
        issue_reason = f"prune_rate={prune_rate:.2f} > 0.60"
    elif feedback_node_count > 0 and eff == 0:
        issue_type = "feedback_not_effective"
        issue_reason = "存在反馈节点但未观察到推进/收敛信号（规则版）"
    elif resolved_flag and resolution_path_length > 5:
        issue_type = "long_resolution_path"
        issue_reason = f"resolution_path_length={resolution_path_length} > 5"
    elif blocked_any and not resolved_flag:
        issue_type = "blocked_without_resolution"
        issue_reason = "blocked=true 且 resolved=false"

    summary = (
        f"depth={depth} branch={branch_count} dead={dead} "
        f"active_path={active_path_length} resolved_path={resolution_path_length} "
        f"fb={feedback_node_count}/{eff} prune_rate={prune_rate:.2f}"
    )

    return ReasoningTreeMetricsResult(
        tree_depth=depth,
        branch_count=branch_count,
        dead_branch_count=dead,
        active_path_length=active_path_length,
        resolution_path_length=resolution_path_length,
        feedback_node_count=feedback_node_count,
        effective_feedback_count=eff,
        prune_rate=round(prune_rate, 3),
        resolved=resolved_flag,
        blocked=blocked_any,
        possible_tree_issue_type=issue_type,
        possible_tree_issue_reason=issue_reason,
        metrics_summary=summary,
        metrics_applied=True,
        active_node_count=active_node_count,
        pruned_node_count=pruned_node_count,
        resolved_node_count=resolved_node_count,
        watchlist_node_count=watchlist_node_count,
    )

