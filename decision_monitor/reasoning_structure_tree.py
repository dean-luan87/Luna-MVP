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

    # continuity influence (M0 reserve): attach one-line summary to root
    cont = frame.get("spatiotemporal_continuity_reserve") if isinstance(frame.get("spatiotemporal_continuity_reserve"), dict) else None
    if cont:
        lvl = _s(_g(cont, "continuity_support_level")) or "unknown"
        inf = _s(_g(cont, "continuity_influence_reason")) or ""
        if inf:
            root.node_summary = (root.node_summary or "") + f" | continuity={lvl}: {inf}"
        else:
            root.node_summary = (root.node_summary or "") + f" | continuity={lvl}"

    # memory vs novel channel (M0): attach one-line dominant channel summary
    mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
    if mn:
        dom_r = _s(_g(mn, "dominant_reasoning_channel")) or "—"
        dom_d = _s(_g(mn, "dominant_decision_channel")) or "—"
        root.node_summary = (root.node_summary or "") + f" | channel=reasoning:{dom_r}/decision:{dom_d}"

    # Environment & task chain premise (M0 reserve): one-line on root
    envr = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
    if envr:
        est = _s(_g(envr, "environment_context", "environment_scene_type")) or "—"
        tst = _s(_g(envr, "task_chain_context", "task_chain_stage")) or "—"
        root.node_summary = (root.node_summary or "") + f" | env={est} task_stage={tst}"

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

    # Layer 2: hypothesis (top 1 + optional pruned alternative)
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

    pruned_id: Optional[str] = None
    # M0.3: 若假设层已强约束到单一主假设，则不再强行合成 pruned alternative（避免低价值 dead branch 污染指标）。
    if isinstance(hyps, list) and len(hyps) >= 2:
        pruned_id = f"hypothesis:{anchor}:alt_pruned"
        nodes.append(
            ReasoningTreeNode(
                node_id=pruned_id,
                parent_node_id=n_ev.node_id,
                node_type="hypothesis",
                node_title="Hypothesis · alternative",
                node_summary="(pruned) alternative hypothesis not selected",
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
    rp_for_gov = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else None
    gov_node_id = None
    if exp:
        cands = _g(exp, "candidates") or []
        cand0 = cands[0] if isinstance(cands, list) and cands else None
        if isinstance(cand0, dict):
            evo_status = _s(_g(cand0, "evolution_status")) or "candidate"
            evo_scope = _s(_g(cand0, "future_use_scope")) or "local_only"
            evo_reason = _s(_g(cand0, "evolution_reason"))
            # M0.6: 当 recheck_planner 已给出可行动 fallback（applied=True, blocked=False）时，
            # governance 的 blocked 更接近“审计保守”而非“执行阻断”，降级为 watchlist，
            # 避免 metrics 将其误计为 blocked_without_resolution。
            cib_for_gov = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else None
            feedback_stalled = bool(
                cib_for_gov
                and (_s(_g(cib_for_gov, "confirmation_input_type")) in ("unknown", None) or _s(_g(cib_for_gov, "confirmation_input_type")) is None)
                and (_s(_g(cib_for_gov, "confirmation_bridge_next_effect")) == "none")
            )
            actionable_fallback = bool(
                rp_for_gov
                and _g(rp_for_gov, "recheck_applied") is True
                and _g(rp_for_gov, "recheck_blocked") is False
                and (
                    _s(_g(rp_for_gov, "recheck_action")) in ("hold_and_confirm", "ask_user_for_clarification")
                    or feedback_stalled
                )
            )
            if evo_status == "blocked" and actionable_fallback:
                evo_status = "watchlist"
                evo_reason = ((evo_reason or "").strip() + "；planner 已给出可行动 fallback，治理状态降级为 watchlist").strip("；")
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
    # explicit exclusion node linked to pruned hypothesis (only when pruned exists)
    if pruned_id:
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
    pruned_ids: List[str] = []
    if pruned_id:
        pruned_ids.extend([pruned_id, f"exclusion:{anchor}:0"])
    if gov_node_id:
        pruned_ids.append(f"exclusion:{anchor}:gov0")
    metrics = _compute_metrics(nodes, root_id)

    tree_summary = f"root={focus or '—'} flow={flow or '—'} active_path={len(active_path)} pruned={len(pruned_ids)}"
    envr2 = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
    if envr2:
        prem = _s(envr2.get("context_premise_summary"))
        if prem:
            tree_summary = tree_summary + f" | premise={prem[:160]}"
    dc = frame.get("decision_contamination_guard_reserve") if isinstance(frame.get("decision_contamination_guard_reserve"), dict) else None
    if dc and dc.get("contamination_guard_applied"):
        tree_summary = tree_summary + " | contamination_reserved=true"
    pp = frame.get("post_processing_intelligence_reserve") if isinstance(frame.get("post_processing_intelligence_reserve"), dict) else None
    if pp and pp.get("post_processing_reserve_applied"):
        tree_summary = tree_summary + " | post_processing_reserved=true"
    tc_raw = frame.get("task_chain_state_snapshot")
    tcsn: Optional[Dict[str, Any]] = None
    if tc_raw is not None and hasattr(tc_raw, "to_dict"):
        tcsn = tc_raw.to_dict()
    elif isinstance(tc_raw, dict):
        tcsn = tc_raw
    if tcsn and tcsn.get("task_chain_state_snapshot_applied"):
        stg2 = _s(tcsn.get("task_chain_stage"))
        md2 = _s(tcsn.get("task_mode"))
        sub2 = _s(tcsn.get("active_subtask_id"))
        rt2 = _s(tcsn.get("task_resume_target"))
        warn2 = _s(tcsn.get("task_position_warning_summary")) or "none"
        sub_tag = "sub=y" if sub2 else "sub=n"
        if rt2 and "resume" in rt2:
            rt_tag = "resume=pending"
        elif rt2:
            rt_tag = "resume=hint"
        else:
            rt_tag = "resume=n"
        crit_hint = "crit=node" if (md2 == "subtask" and "terminal=" in (tcsn.get("task_success_criteria_summary") or "")) else "crit=mix"
        if stg2 or md2:
            tree_summary = (
                tree_summary
                + f" | task_pos={stg2 or '—'}/{md2 or '—'}|{sub_tag}|{rt_tag}|{crit_hint}|warn={warn2[:48]}"
            )
    sss = frame.get("scheduled_source_state") if isinstance(frame.get("scheduled_source_state"), dict) else None
    if sss and sss.get("scheduled_source_state_applied"):
        ds = _s(sss.get("dominant_source"))
        cfx = _s(sss.get("source_conflict_summary"))
        over = _s(sss.get("priority_override_summary"))
        tml = _s(sss.get("timeliness_pressure"))
        conf = _s(sss.get("source_confidence_summary"))
        if ds:
            tree_summary = tree_summary + f" | source={ds}"
        if cfx:
            tree_summary = tree_summary + f" | source_conflict={cfx}"
        if over:
            tree_summary = tree_summary + f" | source_override={over}"
        if tml:
            tree_summary = tree_summary + f" | source_t={tml}"
        if conf:
            tree_summary = tree_summary + f" | source_conf={conf}"

    mie_raw = frame.get("memory_invocation_explanation")
    mie: Optional[Dict[str, Any]] = None
    if mie_raw is not None and hasattr(mie_raw, "to_dict"):
        mie = mie_raw.to_dict()
    elif isinstance(mie_raw, dict):
        mie = mie_raw
    if mie and mie.get("memory_invocation_explanation_applied"):
        mt = _s(mie.get("memory_type_summary")) or "—"
        ef = _s(mie.get("memory_invocation_effect_summary")) or "—"
        inv = "y" if mie.get("memory_invoked") else "n"
        tree_summary = tree_summary + f" | mem=inv={inv}|{mt[:48]}|eff={ef[:32]}"

    mls_raw = frame.get("mainline_state_snapshot")
    mls: Optional[Dict[str, Any]] = None
    if mls_raw is not None and hasattr(mls_raw, "to_dict"):
        mls = mls_raw.to_dict()
    elif isinstance(mls_raw, dict):
        mls = mls_raw
    if mls and mls.get("mainline_state_snapshot_applied"):
        mst = _s(mls.get("mainline_state")) or "—"
        mph = _s(mls.get("mainline_phase")) or "—"
        tree_summary = tree_summary + f" | state={mst}|phase={mph}"
    # M1.1.x-A: process observation anchor (tree-side, no rule change)
    inp = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    if any(
        bool(inp.get(k))
        for k in (
            "recovery_declared_but_resume_chain_fragile_expected",
            "memory_bias_accumulated_under_familiar_context_expected",
            "phase_correct_but_closure_semantics_misaligned_expected",
        )
    ):
        rp_obs = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
        mls_obs = frame.get("mainline_state_snapshot") if isinstance(frame.get("mainline_state_snapshot"), dict) else {}
        phase_obs = _s(mls_obs.get("mainline_phase")) or "unknown"
        ract_obs = _s(rp_obs.get("recheck_action")) or "none"
        tree_summary = tree_summary + f" | proc=m11x_ctx_observed|phase={phase_obs}|recheck={ract_obs}"
    rsr_raw = frame.get("run_summary_reference")
    rsr = rsr_raw.to_dict() if rsr_raw is not None and hasattr(rsr_raw, "to_dict") else (rsr_raw if isinstance(rsr_raw, dict) else None)
    if isinstance(rsr, dict):
        proc = _s(rsr.get("process_observation_summary"))
        if proc:
            tree_summary = tree_summary + f" | proc={proc[:160]}"
        rfrag = _s(rsr.get("resume_chain_fragility_summary"))
        if rfrag and rfrag != "none":
            tree_summary = tree_summary + f" | resume_frag={rfrag[:64]}"
        mmis = _s(rsr.get("closure_semantics_misalignment_summary"))
        if mmis and mmis != "none":
            tree_summary = tree_summary + f" | phase_closure_mis={mmis[:64]}"

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

