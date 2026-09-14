# -*- coding: utf-8 -*-
"""
交互式寻物 M0/M1/M1.5：Object Search Interaction。

M0：单步人机协作搜索动作建议。
M1：最小多轮寻物子任务——子任务状态机、用户回复注入与写回、结果分级、任务链接口预留。
M1.5：药盒范式任务流增强——显式 flow（容器/遮挡/口袋/最后位置/描述启动）、超时/回退、下一步建议链、resolution path。
仅读取已有结构；不做完整对话系统、不做开放世界搜索、不正式并入 Task Chain。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .evidence_ledger import EvidenceLedger
from .hypothesis_layer import HypothesisLayer
from .object_temporal_ledger import ObjectTemporalLedger
from .recheck_planner import RecheckPlannerResult

# M1.5：显式交互流类型
INTERACTION_FLOW_TYPES = (
    "container_check_flow",
    "occlusion_clear_flow",
    "pocket_check_flow",
    "last_location_flow",
    "description_bootstrap_flow",
)

# M1.5：超时后的回退动作
FALLBACK_ACTIONS = (
    "ask_last_location",
    "continue_search_with_recheck",
    "report_not_found_yet",
    "ask_user_to_check_pocket",
    "ask_user_to_open_container",
)

SEARCH_STATES = (
    "target_unclear",
    "searching",
    "candidate_found",
    "needs_user_input",
    "needs_environment_change",
    "not_found_yet",
)

# M1：寻物子任务内部状态
SUBTASK_STATES = (
    "target_unclear",
    "gathering_description",
    "searching_from_last_confirmed",
    "checking_container_candidate",
    "clearing_occlusion",
    "rechecking",
    "waiting_user_reply",
    "candidate_found",
    "not_found_yet",
    "search_done",
)

TERMINAL_STATUSES = ("none", "found", "not_found", "blocked", "cancelled")
RESULT_LEVELS = ("confirmed", "high_probability", "weak_candidate", "unresolved")

INTERACTION_ACTIONS = (
    "ask_object_appearance",
    "ask_last_location",
    "ask_if_in_container",
    "ask_user_to_clear_occlusion",
    "ask_user_to_check_pocket",
    "ask_user_to_open_container",
    "continue_search_with_recheck",
    "report_candidate_location",
    "report_last_confirmed_location",
    "report_not_found_yet",
)

PROMPT_TEMPLATES = {
    "ask_object_appearance": "请描述一下目标的大概外观或大小",
    "ask_last_location": "你记得最后一次把它放在哪里吗",
    "ask_if_in_container": "它有可能在某个容器里吗，比如抽屉/包/冰箱",
    "ask_user_to_clear_occlusion": "当前区域有遮挡，请先清理一下前方区域",
    "ask_user_to_check_pocket": "可以看一下口袋或随身包里有没有",
    "ask_user_to_open_container": "请打开目标容器，我再继续确认",
    "continue_search_with_recheck": "继续按补证建议搜索",
    "report_candidate_location": "当前怀疑目标在某候选位置",
    "report_last_confirmed_location": "我最后确认它在某位置",
    "report_not_found_yet": "目前还未确认目标位置",
}


@dataclass
class ObjectSearchInteractionResult:
    """交互式寻物 M0/M1：单对象交互结果；M1 含子任务状态与结果分级。"""
    search_target_label: Optional[str] = None
    search_state: str = "searching"  # M0 兼容
    interaction_action: Optional[str] = None
    interaction_reason: Optional[str] = None
    interaction_prompt: Optional[str] = None
    suggested_search_zone: Optional[str] = None
    blocking_issue: Optional[str] = None
    interaction_applied: bool = False
    # M1：子任务状态与任务链接口
    search_subtask_state: str = "searching"  # one of SUBTASK_STATES
    search_waiting_user_input: bool = False
    search_terminal_status: str = "none"  # one of TERMINAL_STATUSES
    search_can_resume_main_task: bool = False
    search_summary_for_task_chain: Optional[str] = None
    last_interaction_action: Optional[str] = None
    last_user_response_type: Optional[str] = None
    last_user_response_value: Optional[str] = None
    candidate_confidence_level: float = 0.0
    search_result_level: str = "unresolved"  # one of RESULT_LEVELS
    # M1.5：任务流增强
    interaction_flow_type: Optional[str] = None  # one of INTERACTION_FLOW_TYPES
    interaction_step_index: int = 0
    interaction_expected_user_input: Optional[str] = None
    interaction_timeout_ms: Optional[float] = None
    interaction_timeout_triggered: bool = False
    fallback_action: Optional[str] = None
    fallback_reason: Optional[str] = None
    next_search_step_summary: Optional[str] = None
    search_resolution_path: List[str] = field(default_factory=list)  # 轻量路径节点
    interaction_retry_count: int = 0
    # M0.5：Spatial Expression → Search 文案接入（仅表达增强，非决策）
    search_zone_from_sidecar: bool = False


def _container_display(candidate: Optional[str]) -> str:
    """容器候选用户可见名（写死 M0.5）。"""
    if not (candidate or "").strip():
        return "容器"
    c = (candidate or "").strip().lower()
    return {"cup": "杯子", "bottle": "瓶子", "bowl": "碗"}.get(c, c)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _is_blocked(state: Any) -> tuple[bool, Optional[str]]:
    """与 recheck 一致的守底阻断判定。"""
    if state is None:
        return False, None
    if _get(state, "minimum_mode_active") is True:
        return True, "minimum_mode_active"
    if _get(state, "runtime_domain_state") == "frozen":
        return True, "runtime_domain_state=frozen"
    if _get(state, "scene_gate_action") == "freeze_to_minimum_mode":
        return True, "scene_gate_action=freeze_to_minimum_mode"
    if _get(state, "high_level_output_suppressed") is True:
        return True, "high_level_output_suppressed"
    if _get(state, "human_check_pending") is True:
        return True, "human_check_pending"
    return False, None


def build_object_search_interaction(
    focus_object_label: Optional[str],
    object_temporal_ledger: Optional[ObjectTemporalLedger],
    evidence_ledger: Optional[EvidenceLedger],
    hypothesis_layer: Optional[HypothesisLayer],
    recheck_planner: Optional[RecheckPlannerResult],
    state: Any,
    # M1：上一帧子任务状态与用户回复
    prev_subtask_state: Optional[str] = None,
    prev_last_interaction_action: Optional[str] = None,
    prev_search_terminal_status: Optional[str] = None,
    search_user_object_appearance: Optional[str] = None,
    search_user_last_location: Optional[str] = None,
    search_user_container_answer: Optional[str] = None,
    search_user_occlusion_cleared: Optional[bool] = None,
    search_user_checked_pocket: Optional[bool] = None,
    search_user_cancelled: Optional[bool] = None,
    # M1.5：流/超时/路径
    prev_flow_type: Optional[str] = None,
    prev_step_index: Optional[int] = None,
    prev_resolution_path: Optional[List[str]] = None,
    prev_retry_count: Optional[int] = None,
    interaction_timeout_ms: Optional[float] = None,
    interaction_timeout_triggered: Optional[bool] = None,
    # M0.5：Spatial Expression → Search 文案接入（仅表达，不改状态机）
    focus_target_expression: Optional[str] = None,
) -> ObjectSearchInteractionResult:
    """
    M0/M1：从已有层生成交互式寻物结果。
    M1：用户回复注入驱动子任务状态流转；结果分级；任务链接口字段仅摘要，不并入 Task Chain。
    """
    label = (focus_object_label or "").strip() or None
    blocked, block_reason = _is_blocked(state)
    recheck_blocked = bool(recheck_planner and getattr(recheck_planner, "recheck_blocked", False))
    if recheck_blocked and recheck_planner:
        block_reason = block_reason or getattr(recheck_planner, "recheck_block_reason", None) or "recheck_blocked"

    entry = None
    if object_temporal_ledger and getattr(object_temporal_ledger, "focus_object_entry", None):
        entry = object_temporal_ledger.focus_object_entry

    last_confirmed = _get(entry, "last_confirmed_location") if entry else None
    current_candidate = _get(entry, "current_candidate_location") if entry else None
    container_candidate = _get(entry, "current_container_candidate") if entry else None
    container_state = (_get(entry, "container_state") or "none") if entry else "none"
    visibility = (_get(entry, "visibility_status") or "unknown") if entry else "unknown"
    profile = _get(entry, "object_profile_summary") if entry else None
    container_confidence = _get(entry, "current_container_confidence", 0.0) or 0.0
    ledger_confidence = _get(entry, "ledger_confidence", 0.0) or 0.0

    hyp_type = None
    if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
        first = hypothesis_layer.hypotheses[0]
        hyp_type = _get(first, "hypothesis_type")

    prev_sub = (prev_subtask_state or "searching").strip() or "searching"
    if prev_sub not in SUBTASK_STATES:
        prev_sub = "searching"
    terminal = prev_search_terminal_status or "none"
    if terminal not in TERMINAL_STATUSES:
        terminal = "none"

    # 默认
    search_state = "searching"
    subtask_state = prev_sub
    action = "report_not_found_yet"
    reason = "未匹配到更具体规则"
    zone_parts = []
    result_level = "unresolved"
    waiting_input = False
    can_resume = False
    last_user_type: Optional[str] = None
    last_user_value: Optional[str] = None
    candidate_conf = 0.0

    # ----- 用户回复驱动状态切换（M1） -----
    if search_user_cancelled is True:
        subtask_state = "search_done"
        terminal = "cancelled"
        can_resume = True
        action = "report_not_found_yet"
        reason = "用户取消寻物"
        last_user_type = "search_user_cancelled"
        last_user_value = "true"
    elif search_user_object_appearance and prev_sub in ("target_unclear", "gathering_description"):
        last_user_type = "search_user_object_appearance"
        last_user_value = (search_user_object_appearance or "")[:80]
        if last_confirmed:
            subtask_state = "searching_from_last_confirmed"
            action = "report_last_confirmed_location"
            reason = "已获得外观描述，从最后可信位置继续搜索"
            zone_parts.append(last_confirmed)
        else:
            subtask_state = "not_found_yet"
            action = "ask_last_location"
            reason = "已获得外观，请提供最后放置位置"
            waiting_input = True
    elif search_user_last_location:
        last_user_type = "search_user_last_location"
        last_user_value = (search_user_last_location or "")[:80]
        subtask_state = "searching_from_last_confirmed"
        action = "report_last_confirmed_location"
        reason = "已记录用户提供的最后位置，作为搜索起点"
        zone_parts.append(search_user_last_location[:40])
    elif search_user_container_answer and prev_sub == "checking_container_candidate":
        last_user_type = "search_user_container_answer"
        last_user_value = (search_user_container_answer or "").strip().lower()[:20]
        if last_user_value in ("yes", "opened", "y", "是"):
            subtask_state = "rechecking"
            action = "continue_search_with_recheck"
            reason = "用户确认容器已打开，继续补证确认"
            zone_parts.append(container_candidate[:40] if container_candidate else "容器")
        else:
            subtask_state = "not_found_yet"
            action = "report_not_found_yet"
            reason = "用户否认在容器内，回退容器候选"
    elif search_user_occlusion_cleared is True and prev_sub == "clearing_occlusion":
        last_user_type = "search_user_occlusion_cleared"
        last_user_value = "true"
        subtask_state = "rechecking"
        action = "continue_search_with_recheck"
        reason = "用户已清理遮挡，继续补证"
        zone_parts.append("近场")
    elif search_user_checked_pocket is True:
        last_user_type = "search_user_checked_pocket"
        last_user_value = "true"
        subtask_state = "not_found_yet"
        action = "report_not_found_yet"
        reason = "用户已检查口袋/包，未找到则继续其他候选"

    # ----- 无用户回复本帧：按上下文推导子任务状态与动作 -----
    if last_user_type is None and terminal == "none":
        # 已终态则保持
        if prev_sub == "search_done":
            subtask_state = "search_done"
            terminal = terminal or "found"
            can_resume = True
            action = "report_not_found_yet"
        # A. 目标描述不足
        elif not label or label == "current_focus" or (profile and len(profile) < 10):
            subtask_state = "target_unclear"
            search_state = "target_unclear"
            action = "ask_object_appearance"
            reason = "缺少目标外观/特征信息"
            waiting_input = True
        # C. 存在容器候选
        elif container_candidate and container_state in (
            "object_inside_candidate",
            "object_inside_confirmed",
            "container_open_candidate",
            "container_closed_candidate",
        ):
            subtask_state = "checking_container_candidate"
            search_state = "candidate_found" if container_state in ("object_inside_candidate", "object_inside_confirmed") else "searching"
            if "open" in container_state or container_state == "container_open_candidate":
                action = "ask_user_to_open_container"
                reason = "当前怀疑在容器内，建议打开容器确认"
                waiting_input = True
            else:
                action = "ask_if_in_container"
                reason = "存在容器候选，询问是否在容器中"
                waiting_input = True
            zone_parts.append(container_candidate[:40] if container_candidate else "容器候选")
            candidate_conf = container_confidence
            result_level = "high_probability" if container_confidence >= 0.5 else "weak_candidate"
        # B. 有最后可信位置但当前无强候选
        elif last_confirmed and (not current_candidate or visibility in ("lost", "occluded", "unknown")):
            subtask_state = "searching_from_last_confirmed"
            search_state = "not_found_yet"
            action = "report_last_confirmed_location"
            reason = "最后可信位置可作为搜索起点"
            zone_parts.append(last_confirmed)
            result_level = "weak_candidate"
        # D. 遮挡/近场缺证
        elif hyp_type == "occluded_object_candidate" or visibility in ("occluded", "lost"):
            subtask_state = "clearing_occlusion"
            search_state = "needs_environment_change"
            action = "ask_user_to_clear_occlusion"
            reason = "当前存在遮挡或近场缺证，建议清理遮挡或补证"
            zone_parts.append("近场遮挡区")
            waiting_input = True
            # 若明确处于“寻物”上下文（label 明确且非 current_focus），优先走 occlusion_clear_flow 等用户动作，
            # 不要被 recheck_planner 的通用补证覆盖，否则会丢失 flow_type 与可审计的“清理遮挡”交互动作。
            if (not label or label == "current_focus") and recheck_planner and getattr(recheck_planner, "recheck_action", None):
                action = "continue_search_with_recheck"
                reason = "按补证建议继续搜索"
                subtask_state = "rechecking"
        # 有当前候选
        elif current_candidate:
            subtask_state = "candidate_found"
            search_state = "candidate_found"
            action = "report_candidate_location"
            reason = "当前有候选位置"
            zone_parts.append(current_candidate[:40] if current_candidate else "候选位置")
            candidate_conf = ledger_confidence
            result_level = "high_probability" if ledger_confidence >= 0.6 else "weak_candidate"
        # F. 口袋类建议
        elif visibility in ("lost", "occluded", "unknown") and (not container_candidate or container_confidence < 0.3):
            subtask_state = "not_found_yet"
            search_state = "needs_user_input"
            action = "ask_user_to_check_pocket"
            reason = "目标不可见且无强容器候选，建议检查口袋/随身包"
            zone_parts.append("口袋类候选")
            waiting_input = True
        # 仅有最后可信
        elif last_confirmed:
            subtask_state = "searching_from_last_confirmed"
            search_state = "searching"
            action = "report_last_confirmed_location"
            reason = "最后可信位置可作为搜索起点"
            zone_parts.append(last_confirmed)

    # ----- M1.5：flow_type / step_index / expected_input / timeout / fallback / path / next_step -----
    flow_type: Optional[str] = None
    if subtask_state == "checking_container_candidate":
        flow_type = "container_check_flow"
    elif subtask_state == "clearing_occlusion":
        flow_type = "occlusion_clear_flow"
    elif action == "ask_user_to_check_pocket" or (subtask_state == "not_found_yet" and prev_sub == "waiting_user_reply" and (prev_last_interaction_action or "").startswith("ask_user_to_check")):
        flow_type = "pocket_check_flow"
    elif subtask_state == "searching_from_last_confirmed" and (last_confirmed or search_user_last_location):
        flow_type = "last_location_flow"
    elif subtask_state in ("target_unclear", "gathering_description"):
        flow_type = "description_bootstrap_flow"
    elif subtask_state == "rechecking":
        flow_type = None  # 可记入 path 为 "rechecking"

    prev_flow = (prev_flow_type or "").strip() or None
    step_index = (prev_step_index if prev_step_index is not None else 0)
    if flow_type and flow_type == prev_flow:
        step_index = step_index + 1
    else:
        step_index = 0 if flow_type else step_index

    expected_user_input: Optional[str] = None
    if waiting_input:
        if flow_type == "container_check_flow":
            expected_user_input = "container_yes_no"
        elif flow_type == "occlusion_clear_flow":
            expected_user_input = "occlusion_cleared"
        elif flow_type == "pocket_check_flow":
            expected_user_input = "pocket_checked"
        elif flow_type == "description_bootstrap_flow":
            expected_user_input = "object_appearance"
        elif flow_type == "last_location_flow":
            expected_user_input = "last_location"
        else:
            expected_user_input = "user_reply"

    timeout_triggered = interaction_timeout_triggered is True
    fallback_action_val: Optional[str] = None
    fallback_reason_val: Optional[str] = None
    # 超时仅当“本帧标记为超时触发”且当前或上一帧在等待用户输入时应用
    was_waiting = waiting_input or (prev_last_interaction_action in ("ask_if_in_container", "ask_user_to_open_container", "ask_user_to_clear_occlusion", "ask_user_to_check_pocket", "ask_object_appearance", "ask_last_location"))
    if timeout_triggered and was_waiting:
        fallback_reason_val = "用户输入超时"
        if flow_type == "container_check_flow":
            fallback_action_val = "ask_last_location"
            fallback_reason_val = "容器确认超时，转为询问最后位置"
            if subtask_state == "checking_container_candidate":
                subtask_state = "not_found_yet"
                action = "ask_last_location"
                reason = fallback_reason_val
                waiting_input = True
        elif flow_type == "occlusion_clear_flow":
            fallback_action_val = "continue_search_with_recheck"
            fallback_reason_val = "遮挡清理超时，继续补证搜索"
            subtask_state = "rechecking"
            action = "continue_search_with_recheck"
            reason = fallback_reason_val
            waiting_input = False
        elif flow_type == "pocket_check_flow":
            fallback_action_val = "ask_last_location"
            fallback_reason_val = "口袋检查超时，询问最后位置"
            action = "ask_last_location"
            waiting_input = True
        else:
            fallback_action_val = "report_not_found_yet"
            fallback_reason_val = "等待用户输入超时"

    path_nodes: List[str] = list(prev_resolution_path or [])[:12]
    if flow_type and (not path_nodes or path_nodes[-1] != flow_type):
        path_nodes.append(flow_type)
    elif subtask_state == "rechecking" and (not path_nodes or path_nodes[-1] != "rechecking"):
        path_nodes.append("rechecking")
    elif subtask_state == "candidate_found":
        path_nodes.append("candidate_found")
    elif subtask_state == "search_done":
        path_nodes.append("search_done")

    retry_count = prev_retry_count if prev_retry_count is not None else 0
    if timeout_triggered and fallback_action_val:
        retry_count = retry_count + 1
        if path_nodes and path_nodes[-1] != "fallback":
            path_nodes.append("fallback")

    timeout_ms_out: Optional[float] = interaction_timeout_ms
    if waiting_input and timeout_ms_out is None:
        timeout_ms_out = 30000.0  # 默认 30s，供主循环/对话层参考

    # M0.5：粗粒度位置短语（仅文案增强，不参与状态判断）
    loc = (focus_target_expression or "").strip() or None

    next_step_parts: List[str] = []
    if action == "ask_user_to_open_container" or action == "ask_if_in_container":
        zone_short = (container_candidate or "容器")[:20]
        if loc and container_candidate:
            next_step_parts.append(f"请先检查{loc}的{_container_display(container_candidate)}")
        else:
            next_step_parts.append(f"先打开{zone_short}确认")
        next_step_parts.append("若未找到，再回到最后可信位置或继续查找")
    elif action == "ask_user_to_clear_occlusion":
        if loc:
            next_step_parts.append(f"请先清理{loc}区域的遮挡物")
        else:
            next_step_parts.append("先清理前方遮挡")
        next_step_parts.append("若仍未发现，再检查容器或口袋")
    elif action == "report_last_confirmed_location" and last_confirmed:
        if loc:
            next_step_parts.append(f"请先查看{loc}的位置")
        else:
            next_step_parts.append(f"先根据最后确认位置从{last_confirmed[:24]}开始")
        next_step_parts.append("若无结果，再检查容器候选或询问最后放置位置")
    elif action == "ask_user_to_check_pocket":
        if loc:
            next_step_parts.append(f"请先查看{loc}附近，再检查口袋/随身包")
        else:
            next_step_parts.append("先检查口袋/随身包")
        next_step_parts.append("若仍未找到，再询问最后放置位置或继续补证")
    elif action == "ask_last_location":
        if loc:
            next_step_parts.append(f"目标大致在{loc}，请提供最后放置位置")
        else:
            next_step_parts.append("先提供最后放置位置")
        next_step_parts.append("再以此为起点继续搜索")
    elif action == "continue_search_with_recheck":
        if loc:
            next_step_parts.append(f"请先查看{loc}的位置，按补证建议继续搜索")
        else:
            next_step_parts.append("按补证建议继续搜索")
        next_step_parts.append("若有遮挡或容器候选再分流处理")
    elif action == "report_candidate_location":
        if loc:
            next_step_parts.append(f"目标大致在{loc}" if current_candidate else f"请先查看{loc}的位置")
        elif current_candidate:
            next_step_parts.append(current_candidate[:40])
    if fallback_action_val and fallback_reason_val:
        next_step_parts.append(f"超时回退:{fallback_action_val}")
    next_search_step_summary_val = "；".join(next_step_parts) if next_step_parts else None

    # 阻断时终态与不可恢复
    if blocked or recheck_blocked:
        if terminal == "none":
            terminal = "blocked"
        can_resume = False

    # 结果分级：confirmed 需用户确认或强一致（此处用 result_level 已设，可再提升）
    if result_level == "high_probability" and ledger_confidence >= 0.85:
        result_level = "confirmed"
    if subtask_state == "search_done" and terminal == "found":
        result_level = "confirmed"
        can_resume = True

    prompt = PROMPT_TEMPLATES.get(action)
    if action == "report_candidate_location" and current_candidate:
        prompt = f"当前怀疑目标在：{current_candidate[:36]}"
    elif action == "report_last_confirmed_location" and last_confirmed:
        prompt = f"我最后确认它在：{last_confirmed}"

    base_zone = " / ".join(zone_parts) if zone_parts else None
    # M0.5：有 sidecar 位置表达时优先/组合进 zone，仅文案
    if loc:
        suggested_search_zone = loc if not base_zone else f"{loc}（{base_zone}）"
        search_zone_from_sidecar_val = True
    else:
        suggested_search_zone = base_zone
        search_zone_from_sidecar_val = False
    summary_for_task_chain = f"寻物子任务:{subtask_state};结果:{result_level};终端:{terminal}"
    if flow_type:
        summary_for_task_chain += f";flow:{flow_type}"
    if fallback_action_val:
        summary_for_task_chain += f";fallback:{fallback_action_val}"

    return ObjectSearchInteractionResult(
        search_target_label=label or "current_focus",
        search_state=search_state,
        interaction_action=action,
        interaction_reason=reason,
        interaction_prompt=prompt,
        suggested_search_zone=suggested_search_zone,
        blocking_issue=block_reason if (blocked or recheck_blocked) else None,
        interaction_applied=not (blocked or recheck_blocked),
        search_subtask_state=subtask_state,
        search_waiting_user_input=waiting_input,
        search_terminal_status=terminal,
        search_can_resume_main_task=can_resume,
        search_summary_for_task_chain=summary_for_task_chain,
        last_interaction_action=action,
        last_user_response_type=last_user_type,
        last_user_response_value=last_user_value,
        candidate_confidence_level=candidate_conf,
        search_result_level=result_level,
        interaction_flow_type=flow_type,
        interaction_step_index=step_index,
        interaction_expected_user_input=expected_user_input,
        interaction_timeout_ms=timeout_ms_out,
        interaction_timeout_triggered=timeout_triggered,
        fallback_action=fallback_action_val,
        fallback_reason=fallback_reason_val,
        next_search_step_summary=next_search_step_summary_val,
        search_resolution_path=path_nodes,
        interaction_retry_count=retry_count,
        search_zone_from_sidecar=search_zone_from_sidecar_val,
    )
