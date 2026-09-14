# -*- coding: utf-8 -*-
"""
Environment & Task Context Reserve M0（环境信息 / 任务链信息白盒占位层）

定位（写死）：
- 推理「前提条件」占位：在什么环境下、处于任务链哪一步、哪些人为/系统动作影响当前判断
- 只读 frame 已有字段粗映射；不做复杂环境建模、不做完整任务引擎、不做历史对比

约束：
- 不反写主逻辑；不引入评分系统
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


@dataclass
class EnvironmentContextReserve:
    environment_scene_type: str = "unknown"  # container / occlusion / general / blocked / unknown
    environment_context_summary: Optional[str] = None
    environment_constraints: List[str] = field(default_factory=list)
    environment_risk_factors: List[str] = field(default_factory=list)
    environment_visibility_state: str = "unknown"  # clear / partial / occluded / unknown
    environment_context_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment_scene_type": self.environment_scene_type,
            "environment_context_summary": self.environment_context_summary,
            "environment_constraints": list(self.environment_constraints),
            "environment_risk_factors": list(self.environment_risk_factors),
            "environment_visibility_state": self.environment_visibility_state,
            "environment_context_applied": bool(self.environment_context_applied),
        }


@dataclass
class TaskChainContextReserve:
    task_chain_id: Optional[str] = None
    task_chain_stage: str = "search"  # search / recheck / confirmation / fallback / unresolved / resolved
    task_chain_previous_step: Optional[str] = None
    task_chain_current_action: Optional[str] = None
    task_chain_user_action_effect: Optional[str] = None
    task_chain_system_action_effect: Optional[str] = None
    task_chain_context_summary: Optional[str] = None
    task_chain_context_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_chain_id": self.task_chain_id,
            "task_chain_stage": self.task_chain_stage,
            "task_chain_previous_step": self.task_chain_previous_step,
            "task_chain_current_action": self.task_chain_current_action,
            "task_chain_user_action_effect": self.task_chain_user_action_effect,
            "task_chain_system_action_effect": self.task_chain_system_action_effect,
            "task_chain_context_summary": self.task_chain_context_summary,
            "task_chain_context_applied": bool(self.task_chain_context_applied),
        }


@dataclass
class EnvironmentTaskContextReserveResult:
    environment_context: EnvironmentContextReserve
    task_chain_context: TaskChainContextReserve
    context_premise_summary: Optional[str] = None
    context_premise_applied: bool = False
    # 供 Console/Viewer 在白盒区展示的「单行前提」，与 context_premise_summary 一致（M0）
    whitebox_context_premise_line: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment_context": self.environment_context.to_dict(),
            "task_chain_context": self.task_chain_context.to_dict(),
            "context_premise_summary": self.context_premise_summary,
            "context_premise_applied": bool(self.context_premise_applied),
            "whitebox_context_premise_line": self.whitebox_context_premise_line,
        }


def _timeline_previous_step(frame: Dict[str, Any]) -> Optional[str]:
    tv = frame.get("reasoning_timeline_view") if isinstance(frame.get("reasoning_timeline_view"), dict) else None
    if not tv:
        return None
    evs = tv.get("events")
    if not isinstance(evs, list) or len(evs) < 2:
        return None
    prev = evs[-2]
    if isinstance(prev, dict):
        return _s(prev.get("event_summary"))
    return None


def build_environment_task_context_reserve(frame: Dict[str, Any]) -> EnvironmentTaskContextReserveResult:
    """
    M0 最小规则：从 object_search_interaction / metrics / continuity / confirmation / recheck / action_hint 粗映射。
    """
    if not isinstance(frame, dict):
        return EnvironmentTaskContextReserveResult(
            environment_context=EnvironmentContextReserve(),
            task_chain_context=TaskChainContextReserve(),
            context_premise_applied=False,
        )

    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    metrics = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else {}
    cont = frame.get("spatiotemporal_continuity_reserve") if isinstance(frame.get("spatiotemporal_continuity_reserve"), dict) else {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    ah = frame.get("action_hint_copy") if isinstance(frame.get("action_hint_copy"), dict) else {}
    side = frame.get("spatial_expression_sidecar") if isinstance(frame.get("spatial_expression_sidecar"), dict) else {}

    flow = _s(_get(osi, "interaction_flow_type")) or _s(_get(cib, "confirmation_bridge_target_flow")) or ""
    issue = _s(_get(metrics, "possible_tree_issue_type"))
    term = _s(_get(osi, "search_terminal_status")) or "none"

    raw_fb = _s(cib.get("confirmation_input_raw_text"))
    next_effect = _s(cib.get("confirmation_bridge_next_effect")) or "none"
    mapped = _s(cib.get("confirmation_input_type"))

    rec_action = _s(rp.get("recheck_action"))
    rec_blocked = rp.get("recheck_blocked") is True

    # --- environment_scene_type ---
    scene = "general"
    if issue == "blocked_without_resolution" or (term == "blocked"):
        scene = "blocked"
    elif flow == "container_check_flow":
        scene = "container"
    elif flow == "occlusion_clear_flow":
        scene = "occlusion"
    elif not flow:
        scene = "unknown"

    # --- visibility ---
    vis = "unknown"
    if flow == "occlusion_clear_flow" or _get(side, "occlusion_hint_active") is True:
        vis = "occluded"
    elif cont.get("continuity_broken") is True or issue == "feedback_not_effective":
        vis = "partial"
    elif flow == "container_check_flow" and scene != "blocked":
        vis = "partial"
    elif scene in ("general", "unknown") and flow not in ("occlusion_clear_flow",):
        vis = "clear"
    elif flow in ("pocket_check_flow", "last_location_flow", "description_bootstrap_flow"):
        vis = "partial"

    constraints: List[str] = []
    if _get(side, "container_candidate_label") or "容器" in (_s(ah.get("action_hint_primary")) or ""):
        constraints.append("container_candidate_present")
    if flow == "occlusion_clear_flow":
        constraints.append("occlusion_present")
    if term == "blocked" or issue == "blocked_without_resolution":
        constraints.append("blocked_state_present")
    if raw_fb or (mapped and mapped != "none"):
        constraints.append("feedback_active")
    if cont.get("continuity_broken") is True:
        constraints.append("continuity_broken")

    risks: List[str] = []
    if issue == "high_dead_branch_ratio":
        risks.append("high_dead_branch_ratio")
    if issue == "blocked_without_resolution":
        risks.append("blocked_without_resolution")
    if issue == "feedback_not_effective":
        risks.append("feedback_not_effective")
    if vis in ("occluded", "partial"):
        risks.append("weak_visibility")

    env_summary = f"场景≈{scene}，可见性≈{vis}"
    if constraints:
        env_summary += f"；约束：{', '.join(constraints[:3])}"

    env = EnvironmentContextReserve(
        environment_scene_type=scene,
        environment_context_summary=env_summary,
        environment_constraints=constraints[:3],
        environment_risk_factors=risks[:3],
        environment_visibility_state=vis,
        environment_context_applied=True,
    )

    # --- task chain ---
    seq = _get(frame, "inputs", "frame_seq")
    anchor = _s(frame.get("trace_anchor_id")) or (f"f{seq}" if seq is not None else "tc_unknown")
    tc_id = f"tc:{anchor}"

    stage = "search"
    if term in ("found", "cancelled"):
        stage = "resolved"
    elif term == "blocked" or issue == "blocked_without_resolution":
        stage = "unresolved"
    elif rec_blocked or rec_action in ("hold_and_confirm", "ask_user_for_clarification"):
        stage = "fallback"
    elif rec_action and rec_action not in ("none", None, ""):
        stage = "recheck"
    elif raw_fb or (mapped and mapped != "none"):
        stage = "confirmation"

    prev_step = _timeline_previous_step(frame)
    if not prev_step:
        if rec_action:
            prev_step = f"recheck_hint:{rec_action}"
        elif _s(ah.get("action_hint_followup")):
            prev_step = "action_hint_followup_ready"
        else:
            prev_step = "observation_and_hypothesis"

    cur_action = rec_action or _s(ah.get("action_hint_primary")) or next_effect
    if cur_action and len(cur_action) > 120:
        cur_action = cur_action[:117] + "..."

    user_eff: Optional[str] = None
    if raw_fb or mapped:
        if next_effect and next_effect not in ("none", "", None):
            user_eff = "user feedback changed path"
        elif issue == "feedback_not_effective":
            user_eff = "user feedback had weak effect"
        else:
            user_eff = "user feedback confirmed current path"
    else:
        user_eff = "none"

    sys_eff = "no strong system action"
    if rec_blocked:
        sys_eff = "triggered fallback"
    elif rec_action == "recheck_environment":
        sys_eff = "entered recheck"
    elif next_effect == "advance_to_recheck":
        sys_eff = "advanced to recheck"
    elif mapped in ("confirmed_no", "target_not_found") and flow == "container_check_flow":
        sys_eff = "rejected container path signal"

    tc_sum = f"阶段={stage}；当前动作={cur_action or '—'}；用户侧={user_eff}；系统侧={sys_eff}"

    task = TaskChainContextReserve(
        task_chain_id=tc_id,
        task_chain_stage=stage,
        task_chain_previous_step=prev_step,
        task_chain_current_action=cur_action,
        task_chain_user_action_effect=user_eff,
        task_chain_system_action_effect=sys_eff,
        task_chain_context_summary=tc_sum,
        task_chain_context_applied=True,
    )

    # --- one-line premise (human readable) ---
    scene_cn = {"container": "容器搜索", "occlusion": "遮挡清理", "general": "一般搜索", "blocked": "受阻/收口", "unknown": "未细分"}.get(scene, scene)
    stage_cn = {
        "search": "搜索推进",
        "recheck": "补证",
        "confirmation": "等待或处理你的确认/反馈",
        "fallback": "转入兜底澄清",
        "unresolved": "尚未收口",
        "resolved": "已收口",
    }.get(stage, stage)

    vis_cn = {"clear": "可见性尚可", "partial": "可见性一般", "occluded": "存在遮挡或视线受阻", "unknown": "可见性不确定"}.get(vis, vis)

    premise = (
        f"当前更像「{scene_cn}」场景（{vis_cn}），任务链处在「{stage_cn}」。"
        f"系统侧：{sys_eff}；你这边：{user_eff}。"
    )
    if risks:
        premise += f" 需要留意的风险信号：{', '.join(risks[:2])}。"

    return EnvironmentTaskContextReserveResult(
        environment_context=env,
        task_chain_context=task,
        context_premise_summary=premise,
        context_premise_applied=True,
        whitebox_context_premise_line=premise,
    )
