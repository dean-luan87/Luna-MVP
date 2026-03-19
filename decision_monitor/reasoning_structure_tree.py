# -*- coding: utf-8 -*-
"""
Reasoning Structure Tree M0（推理与决策结构树）

定位：
- 白盒之上的“总组织结构”，用于把线索/假设/动作/反馈/排除/收敛结果按树组织起来
- 本文件仅做规则版聚合树（M0）：框架 + 节点模型 + 最小挂接

约束：
- 只读输入 frame（DecisionMonitorFrame.to_dict() 结果或等价 dict）
- 不反写任何主逻辑
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


def _g(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


NODE_TYPES = (
    "evidence",
    "hypothesis",
    "search_candidate",
    "grid_decision",
    "recheck_decision",
    "action_hint",
    "confirmation_input",
    "exclusion",
    "resolution",
)

NODE_STATUS = (
    "active",
    "pruned",
    "blocked",
    "confirmed",
    "rejected",
    "resolved",
    "watchlist",
)


@dataclass
class ReasoningTreeNode:
    node_id: str
    parent_node_id: Optional[str]
    node_type: str
    node_title: str
    node_summary: Optional[str] = None
    source_module: Optional[str] = None
    status: str = "active"
    confidence_score: Optional[float] = None
    confidence_band: Optional[str] = None
    is_user_feedback_driven: bool = False
    related_raw_text: Optional[str] = None
    exclusion_reason: Optional[str] = None
    next_effect: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReasoningStructureTreeResult:
    root_node_id: str
    nodes: List[ReasoningTreeNode] = field(default_factory=list)
    active_path_node_ids: List[str] = field(default_factory=list)
    pruned_node_ids: List[str] = field(default_factory=list)
    resolved_node_id: Optional[str] = None
    tree_summary: Optional[str] = None
    tree_depth: int = 0
    branch_count: int = 0
    dead_branch_count: int = 0
    tree_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "root_node_id": self.root_node_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "active_path_node_ids": list(self.active_path_node_ids),
            "pruned_node_ids": list(self.pruned_node_ids),
            "resolved_node_id": self.resolved_node_id,
            "tree_summary": self.tree_summary,
            "tree_depth": int(self.tree_depth),
            "branch_count": int(self.branch_count),
            "dead_branch_count": int(self.dead_branch_count),
            "tree_applied": bool(self.tree_applied),
        }


def _compute_metrics(nodes: List[ReasoningTreeNode], root_id: str) -> Dict[str, int]:
    children: Dict[str, List[str]] = {}
    for n in nodes:
        if n.parent_node_id:
            children.setdefault(n.parent_node_id, []).append(n.node_id)

    # depth via DFS (small N)
    max_depth = 1
    stack = [(root_id, 1)]
    visited = set()
    while stack:
        nid, dep = stack.pop()
        if (nid, dep) in visited:
            continue
        visited.add((nid, dep))
        max_depth = max(max_depth, dep)
        for ch in children.get(nid, []):
            stack.append((ch, dep + 1))

    # branch_count: nodes with >=2 children
    branch_nodes = [pid for pid, ch in children.items() if len(ch) >= 2]
    # dead_branch_count: leaf nodes that are pruned/rejected
    leaf_ids = [n.node_id for n in nodes if n.node_id not in children]
    dead = 0
    for n in nodes:
        if n.node_id in leaf_ids and n.status in ("pruned", "rejected"):
            dead += 1
    return {"tree_depth": max_depth, "branch_count": len(branch_nodes), "dead_branch_count": dead}


def build_reasoning_structure_tree(frame: Dict[str, Any]) -> ReasoningStructureTreeResult:
    """
    规则版最小树生成（M0）：
    root -> (线索/候选) -> 假设 -> 动作决策 -> 反馈 -> 结果
    并至少生成一个 pruned/exclusion 节点。
    """
    seq = _g(frame, "inputs", "frame_seq")
    anchor = _s(frame.get("trace_anchor_id")) or (str(seq) if seq is not None else "unknown")
    root_id = f"root:{anchor}"

    goal = _s(_g(frame, "goal", "goal_type")) or "goal"
    focus = _s(_g(frame, "object_search_interaction", "search_target_label")) or _s(_g(frame, "spatial_expression_sidecar", "focus_target_label"))
    flow = _s(_g(frame, "object_search_interaction", "interaction_flow_type")) or _s(_g(frame, "confirmation_input_bridge", "confirmation_bridge_target_flow"))
    term = _s(_g(frame, "object_search_interaction", "search_terminal_status")) or "none"
    next_effect = _s(_g(frame, "confirmation_input_bridge", "confirmation_bridge_next_effect")) or "none"

    nodes: List[ReasoningTreeNode] = []

    root = ReasoningTreeNode(
        node_id=root_id,
        parent_node_id=None,
        node_type="resolution",
        node_title=f"Reasoning Root · {focus or '—'}",
        node_summary=f"goal={goal} flow={flow or '—'} terminal={term} next_effect={next_effect}",
        source_module="reasoning_structure_tree",
        status="active",
    )
    nodes.append(root)

    # Layer 1: evidence/search_candidate (1~3)
    ev_entries = _g(frame, "evidence_ledger", "entries") or []
    ev0 = ev_entries[0] if isinstance(ev_entries, list) and ev_entries else None
    ev_title = _s(_g(ev0, "claim_summary")) if isinstance(ev0, dict) else None
    ev_conf = _g(ev0, "evidence_confidence") if isinstance(ev0, dict) else None
    n_ev = ReasoningTreeNode(
        node_id=f"evidence:{anchor}:0",
        parent_node_id=root_id,
        node_type="evidence",
        node_title=ev_title or "Evidence · (none)",
        node_summary=_s(_g(ev0, "suggested_next_check")) if isinstance(ev0, dict) else None,
        source_module="evidence_ledger",
        status="active",
        confidence_score=float(ev_conf) if isinstance(ev_conf, (int, float)) else None,
    )
    nodes.append(n_ev)

    # add up to 2 extra evidence nodes (growth chain visibility)
    if isinstance(ev_entries, list) and len(ev_entries) > 1:
        for i, ev in enumerate(ev_entries[1:3], start=1):
            if not isinstance(ev, dict):
                continue
            ev_title_i = _s(_g(ev, "claim_summary")) or f"Evidence · {i}"
            ev_conf_i = _g(ev, "evidence_confidence")
            nodes.append(
                ReasoningTreeNode(
                    node_id=f"evidence:{anchor}:{i}",
                    parent_node_id=root_id,
                    node_type="evidence",
                    node_title=ev_title_i,
                    node_summary=_s(_g(ev, "suggested_next_check")),
                    source_module="evidence_ledger",
                    status="active",
                    confidence_score=float(ev_conf_i) if isinstance(ev_conf_i, (int, float)) else None,
                )
            )

    vca_labels = _g(frame, "visual_candidate_audit", "mapped_candidate_labels") or _g(frame, "visual_candidate_audit", "detector_candidate_labels")
    if isinstance(vca_labels, list) and vca_labels:
        nodes.append(
            ReasoningTreeNode(
                node_id=f"search_candidate:{anchor}:visual",
                parent_node_id=root_id,
                node_type="search_candidate",
                node_title="Visual candidates",
                node_summary=",".join([str(x) for x in vca_labels[:6]]),
                source_module="visual_candidate_audit",
                status="active",
            )
        )

    # Layer 2: hypothesis (top 1 + 1 pruned)
    hyps = _g(frame, "hypothesis_layer", "hypotheses") or []
    hyp0 = hyps[0] if isinstance(hyps, list) and hyps else None
    hyp_title = _s(_g(hyp0, "hypothesis_summary")) if isinstance(hyp0, dict) else None
    hyp_type = _s(_g(hyp0, "hypothesis_type")) if isinstance(hyp0, dict) else None
    hyp_conf = _g(hyp0, "hypothesis_confidence") if isinstance(hyp0, dict) else None
    hyp_id = f"hypothesis:{anchor}:0"
    nodes.append(
        ReasoningTreeNode(
            node_id=hyp_id,
            parent_node_id=n_ev.node_id,
            node_type="hypothesis",
            node_title=f"Hypothesis · {hyp_type or '—'}",
            node_summary=hyp_title,
            source_module="hypothesis_layer",
            status="active",
            confidence_score=float(hyp_conf) if isinstance(hyp_conf, (int, float)) else None,
        )
    )

    # a pruned alternative hypothesis (minimum)
    pruned_id = f"hypothesis:{anchor}:alt_pruned"
    nodes.append(
        ReasoningTreeNode(
            node_id=pruned_id,
            parent_node_id=n_ev.node_id,
            node_type="hypothesis",
            node_title="Hypothesis · alternative",
            node_summary="(pruned) alternative path not selected in M0 rule tree",
            source_module="hypothesis_layer",
            status="pruned",
            exclusion_reason="lower_priority_or_context_mismatch",
        )
    )

    # Layer 3: decisions (grid/recheck/action_hint)
    gse = frame.get("grid_search_expansion") if isinstance(frame.get("grid_search_expansion"), dict) else None
    if gse:
        primary = _s(_g(gse, "primary_search_cell_human_label")) or _s(_g(gse, "primary_search_cell_id"))
        nodes.append(
            ReasoningTreeNode(
                node_id=f"grid_decision:{anchor}",
                parent_node_id=hyp_id,
                node_type="grid_decision",
                node_title="Grid decision",
                node_summary=f"primary={primary or '—'} hint={_s(_g(gse, 'grid_search_expansion_hint')) or '—'}",
                source_module="grid_search_expansion",
                status="active",
            )
        )

    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else None
    if rp:
        ract = _s(_g(rp, "recheck_action"))
        rblocked = _g(rp, "recheck_blocked") is True
        nodes.append(
            ReasoningTreeNode(
                node_id=f"recheck_decision:{anchor}",
                parent_node_id=hyp_id,
                node_type="recheck_decision",
                node_title="Recheck decision",
                node_summary=f"action={ract or '—'} blocked={rblocked}",
                source_module="recheck_planner",
                status="blocked" if rblocked else "active",
            )
        )

    ah = frame.get("action_hint_copy") if isinstance(frame.get("action_hint_copy"), dict) else None
    if ah:
        nodes.append(
            ReasoningTreeNode(
                node_id=f"action_hint:{anchor}",
                parent_node_id=hyp_id,
                node_type="action_hint",
                node_title="Action hint",
                node_summary=_s(_g(ah, "action_hint_primary")),
                source_module="action_hint_copy",
                status="active",
            )
        )

    # Layer 4: feedback
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else None
    if cib:
        ctype = _s(_g(cib, "confirmation_input_type"))
        craw = _s(_g(cib, "confirmation_input_raw_text"))
        cnext = _s(_g(cib, "confirmation_bridge_next_effect"))
        nodes.append(
            ReasoningTreeNode(
                node_id=f"confirmation_input:{anchor}",
                parent_node_id=hyp_id,
                node_type="confirmation_input",
                node_title=f"Confirmation · {ctype or '—'}",
                node_summary=craw,
                source_module="confirmation_input_bridge",
                status="confirmed" if (ctype and ctype != "unknown") else "active",
                is_user_feedback_driven=bool(craw),
                related_raw_text=craw,
                next_effect=cnext,
            )
        )

    # Growth-chain: experience governance outcome (watchlist/promotable/blocked/rejected)
    exp = frame.get("experience_evolution") if isinstance(frame.get("experience_evolution"), dict) else None
    gov_node_id = None
    if exp:
        cands = _g(exp, "candidates") or []
        cand0 = cands[0] if isinstance(cands, list) and cands else None
        if isinstance(cand0, dict):
            evo_status = _s(_g(cand0, "evolution_status")) or "candidate"
            evo_scope = _s(_g(cand0, "future_use_scope")) or "local_only"
            evo_reason = _s(_g(cand0, "evolution_reason"))
            gov_node_id = f"resolution:{anchor}:governance"
            nodes.append(
                ReasoningTreeNode(
                    node_id=gov_node_id,
                    parent_node_id=hyp_id,
                    node_type="resolution",
                    node_title=f"Governance · {evo_status}",
                    node_summary=(evo_reason or f"scope={evo_scope}")[:160],
                    source_module="experience_evolution",
                    status="watchlist" if evo_status == "watchlist" else ("blocked" if evo_status == "blocked" else ("rejected" if evo_status == "rejected" else ("resolved" if evo_status == "promotable" else "active"))),
                    is_user_feedback_driven=bool(_s(_g(frame, "confirmation_input_bridge", "confirmation_input_raw_text"))),
                )
            )

            # attach at least one governance exclusion (not selected outcome)
            gov_wb = frame.get("experience_governance_whitebox_trace") if isinstance(frame.get("experience_governance_whitebox_trace"), dict) else None
            excl = _g(gov_wb, "exclusion_log") if isinstance(gov_wb, dict) else None
            ex0 = excl[0] if isinstance(excl, list) and excl else None
            if isinstance(ex0, dict):
                nodes.append(
                    ReasoningTreeNode(
                        node_id=f"exclusion:{anchor}:gov0",
                        parent_node_id=gov_node_id,
                        node_type="exclusion",
                        node_title=f"Excluded governance outcome · {_s(_g(ex0, 'excluded_outcome_id')) or '—'}",
                        node_summary=_s(_g(ex0, "excluded_reason")),
                        source_module="experience_governance_whitebox_trace",
                        status="pruned",
                        exclusion_reason=_s(_g(ex0, "excluded_reason")),
                    )
                )

    # Layer 5: resolution/exclusion
    recheck_blocked = _g(frame, "recheck_planner", "recheck_blocked") is True
    if term in ("found", "cancelled"):
        resolved_status = "resolved"
    elif recheck_blocked:
        resolved_status = "blocked"
    else:
        resolved_status = "active"
    res_id = f"resolution:{anchor}"
    nodes.append(
        ReasoningTreeNode(
            node_id=res_id,
            parent_node_id=root_id,
            node_type="resolution",
            node_title="Resolution",
            node_summary=f"terminal={term} next_effect={next_effect}",
            source_module="object_search_interaction",
            status=resolved_status,
            next_effect=next_effect,
        )
    )
    # explicit exclusion node linked to pruned hypothesis
    nodes.append(
        ReasoningTreeNode(
            node_id=f"exclusion:{anchor}:0",
            parent_node_id=pruned_id,
            node_type="exclusion",
            node_title="Excluded branch",
            node_summary="pruned alternative hypothesis",
            source_module="reasoning_structure_tree",
            status="pruned",
            exclusion_reason="lower_priority_or_context_mismatch",
        )
    )

    active_path = [root_id, n_ev.node_id, hyp_id]
    if gov_node_id:
        active_path.append(gov_node_id)
    pruned_ids = [pruned_id, f"exclusion:{anchor}:0"]
    if gov_node_id:
        pruned_ids.append(f"exclusion:{anchor}:gov0")
    metrics = _compute_metrics(nodes, root_id)

    tree_summary = f"root={focus or '—'} flow={flow or '—'} active_path={len(active_path)} pruned={len(pruned_ids)}"
    return ReasoningStructureTreeResult(
        root_node_id=root_id,
        nodes=nodes,
        active_path_node_ids=active_path,
        pruned_node_ids=pruned_ids,
        resolved_node_id=res_id if resolved_status in ("resolved", "blocked") else None,
        tree_summary=tree_summary,
        tree_depth=metrics["tree_depth"],
        branch_count=metrics["branch_count"],
        dead_branch_count=metrics["dead_branch_count"],
        tree_applied=True,
    )

