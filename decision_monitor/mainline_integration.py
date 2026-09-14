# -*- coding: utf-8 -*-
"""
主线接入 M0：Cognitive Runtime Mainline Integration M0。

将 task_chain_bridge / task_arbitration / task_bundle / object_search_interaction /
recheck_planner / experience_evolution 以摘要先行、软控制优先、硬边界保留的方式接入主流程。
不重构主流程、不反写策略、不新增大一统状态机；仅消费摘要与轻量控制结果。

M0.6：去噪与价值分层
- observed_modules：被读到、被汇总（原 consumed）
- effective_modules：真正影响 soft/blocked/foreground/state 的模块
- 软动作门槛：look_forward / shift_view_* 仅在有 reason 或 target 时记入
- pillar_effective：search/recheck/arbitration/bundle/experience 是否为“有效值”（非默认占位）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# 软动作类型（主线接入观察与摘要，非完整执行图）
SOFT_ACTIONS = (
    "recheck_environment",
    "recheck_close_range",
    "look_forward",
    "shift_view_left",
    "shift_view_right",
    "object_search_prompt_ready",
    "bundle_summary_ready",
    "arbitration_summary_ready",
)
# 阻断动作类型
BLOCKED_ACTIONS = (
    "blocked_recheck_environment",
    "blocked_recheck_close_range",
    "blocked_search_interaction",
    "blocked_bundle_activation",
    "blocked_task_resume",
)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@dataclass
class MainlineIntegrationResult:
    """
    主线接入 M0 结果：摘要与轻量控制，非新状态机。
    供主流程消费、runtime_ctx 写回、Viewer 展示。
    M0.5：integration_observation_frame_note 供日志/统计一行观察（consumed=N soft=K blocked=L）。
    M0.6：observed vs effective 分层；pillar 有效值判定；软动作去噪。
    """
    integration_enabled: bool = True
    integration_summary: Optional[str] = None
    integration_consumed_modules: List[str] = field(default_factory=list)
    integration_soft_actions: List[str] = field(default_factory=list)
    integration_blocked_actions: List[str] = field(default_factory=list)
    integration_observation_notes: List[str] = field(default_factory=list)
    integration_applied: bool = True
    integration_observation_frame_note: Optional[str] = None
    # M0.6：observed = 被读到/汇总；effective = 真正影响 soft/blocked/foreground/state
    integration_observed_modules: List[str] = field(default_factory=list)
    integration_effective_modules: List[str] = field(default_factory=list)
    # M0.6：各支柱是否为“有效值”（非默认占位）
    integration_pillar_effective: Optional[Dict[str, bool]] = None


def build_mainline_integration(
    task_chain_bridge: Any,
    task_arbitration: Any,
    task_bundle: Any,
    object_search_interaction: Any,
    recheck_planner: Any,
    experience_evolution: Any,
    state: Any,
) -> MainlineIntegrationResult:
    """
    从 6 模块结果汇总主线接入摘要、已消费模块、软动作与阻断动作。
    不修改任何模块逻辑，仅只读汇总。
    """
    consumed: List[str] = []
    soft_actions: List[str] = []
    blocked_actions: List[str] = []
    observation_notes: List[str] = []

    # 任务链摘要
    tc_state = _get(task_chain_bridge, "task_chain_state") or "active"
    tc_substate = _get(task_chain_bridge, "task_chain_substate")
    tc_foreground = _get(task_chain_bridge, "task_chain_foreground_summary")
    tc_can_resume = _get(task_chain_bridge, "task_chain_can_resume", False)
    tc_bundle_state = _get(task_chain_bridge, "task_chain_bundle_state") or "none"
    if task_chain_bridge:
        consumed.append("task_chain_bridge")

    # 任务仲裁摘要
    arb_action = _get(task_arbitration, "arbitration_action") or "continue_current"
    arb_reason = _get(task_arbitration, "arbitration_reason")
    fg_task = _get(task_arbitration, "foreground_task_type")
    if task_arbitration:
        consumed.append("task_arbitration")
    if task_arbitration and arb_action and (arb_action or "continue_current") != "continue_current":
        soft_actions.append("arbitration_summary_ready")

    # 任务包摘要
    bundle_id = _get(task_bundle, "bundle_id")
    bundle_zone = _get(task_bundle, "bundle_zone")
    bundle_tasks = _get(task_bundle, "bundle_task_types") or []
    bundle_focus = _get(task_bundle, "bundle_shared_focus")
    bundle_status = _get(task_bundle, "bundle_status") or "closed"
    bundle_applied = _get(task_bundle, "bundle_applied", False)
    bundle_block_reason = _get(task_bundle, "bundle_block_reason")
    if task_bundle and (bundle_id or bundle_tasks):
        consumed.append("task_bundle")
    if task_bundle and bundle_id and bundle_status not in ("closed", "blocked"):
        soft_actions.append("bundle_summary_ready")
    if task_bundle and bundle_status == "blocked":
        blocked_actions.append("blocked_bundle_activation")
    if not tc_can_resume and tc_state == "blocked":
        blocked_actions.append("blocked_task_resume")

    # 寻物摘要
    search_state = _get(object_search_interaction, "search_state") or "searching"
    search_action = _get(object_search_interaction, "interaction_action")
    search_prompt = _get(object_search_interaction, "interaction_prompt")
    search_zone = _get(object_search_interaction, "suggested_search_zone")
    search_flow = _get(object_search_interaction, "interaction_flow_type")
    search_next = _get(object_search_interaction, "next_search_step_summary")
    search_terminal = _get(object_search_interaction, "search_terminal_status") or "none"
    search_waiting = _get(object_search_interaction, "search_waiting_user_input", False)
    search_terminal_ok = (search_terminal or "none") != "none"
    search_state_meaningful = (search_state or "searching") not in ("searching", "target_unclear") or search_waiting or search_terminal_ok
    if object_search_interaction:
        consumed.append("object_search_interaction")
    if object_search_interaction and (search_prompt or search_action) and search_state_meaningful:
        soft_actions.append("object_search_prompt_ready")

    # 补证摘要
    recheck_action = _get(recheck_planner, "recheck_action")
    recheck_reason = _get(recheck_planner, "recheck_reason")
    recheck_target = _get(recheck_planner, "recheck_target")
    recheck_blocked = _get(recheck_planner, "recheck_blocked", False)
    recheck_reason_ok = bool((recheck_reason or "").strip())
    recheck_target_ok = bool((recheck_target or "").strip())
    recheck_meaningful = recheck_reason_ok or recheck_target_ok
    if recheck_planner:
        consumed.append("recheck_planner")
    if recheck_planner and not recheck_blocked and recheck_action:
        if recheck_action == "recheck_environment":
            if recheck_meaningful:
                soft_actions.append("recheck_environment")
        elif recheck_action == "recheck_close_range":
            if recheck_meaningful:
                soft_actions.append("recheck_close_range")
        elif recheck_action == "look_forward":
            if recheck_meaningful:
                soft_actions.append("look_forward")
        elif recheck_action == "shift_view_left":
            if recheck_meaningful:
                soft_actions.append("shift_view_left")
        elif recheck_action == "shift_view_right":
            if recheck_meaningful:
                soft_actions.append("shift_view_right")
    if recheck_planner and recheck_blocked:
        if recheck_action == "recheck_environment":
            blocked_actions.append("blocked_recheck_environment")
        elif recheck_action == "recheck_close_range":
            blocked_actions.append("blocked_recheck_close_range")

    # 经验摘要（只读，不反写）
    exp_type = None
    exp_status = None
    exp_reason = None
    exp_hint = None
    exp_band = None
    exp_scope = None
    exp_group_key: Optional[str] = None
    exp_repeated: int = 0
    exp_contra: int = 0
    if experience_evolution and getattr(experience_evolution, "candidates", None):
        consumed.append("experience_evolution")
        first = experience_evolution.candidates[0]
        exp_type = _get(first, "experience_type")
        exp_status = _get(first, "evolution_status")
        exp_reason = _get(first, "evolution_reason")
        exp_hint = _get(first, "evolution_hint_for_future")
        exp_band = _get(first, "evolution_confidence_band")
        exp_scope = _get(first, "future_use_scope")
        exp_group_key = _get(first, "experience_group_key")
        exp_repeated = int(_get(first, "repeated_pattern_count", 0) or 0)
        exp_contra = int(_get(first, "contradiction_count", 0) or 0)
        observation_notes.append(
            f"exp_type={exp_type or '—'} status={exp_status or '—'} hint={exp_hint or '—'}"
        )

    # M0.6：effective_modules（真正影响 soft/blocked/foreground/state 的模块）
    effective: List[str] = []
    if task_chain_bridge and (tc_state in ("waiting_user", "blocked", "bundled", "paused") or (tc_bundle_state or "none") != "none"):
        effective.append("task_chain_bridge")
    if task_arbitration and (arb_action or "continue_current") != "continue_current":
        effective.append("task_arbitration")
    if task_bundle and bundle_id and (bundle_status or "closed") in ("proposed", "active"):
        effective.append("task_bundle")
    search_waiting = _get(object_search_interaction, "search_waiting_user_input", False)
    search_terminal_ok = (search_terminal or "none") != "none"
    search_state_meaningful = (search_state or "searching") not in ("searching", "target_unclear") or search_waiting or search_terminal_ok
    if object_search_interaction and (search_prompt or search_action) and search_state_meaningful:
        effective.append("object_search_interaction")
    if recheck_planner and recheck_action and recheck_meaningful:
        effective.append("recheck_planner")
    if experience_evolution and getattr(experience_evolution, "candidates", None) and (
        exp_group_key or exp_repeated > 0 or exp_contra > 0 or (exp_status or "candidate") not in ("candidate",)
    ):
        effective.append("experience_evolution")

    # M0.6：pillar 有效值（非默认占位）
    pillar_effective = {
        "search": bool(object_search_interaction and (search_prompt or search_action) and search_state_meaningful),
        "recheck": bool(recheck_action and recheck_meaningful),
        "arbitration": (arb_action or "continue_current") != "continue_current",
        "bundle": bool(bundle_id and (bundle_status or "closed") in ("proposed", "active")),
        "experience": bool(
            experience_evolution
            and getattr(experience_evolution, "candidates", None)
            and (exp_group_key or exp_repeated > 0 or exp_contra > 0 or (exp_status or "candidate") not in ("candidate",))
        ),
    }

    # 生成标准化 integration_summary
    fg = fg_task or tc_foreground or "—"
    fg = (fg or "").strip() or "—"
    arb = (arb_action or "—").strip()
    bundle_str = "none"
    if bundle_id:
        bundle_str = f"{bundle_status or '—'}"
    search_str = "none"
    if object_search_interaction and (search_state or search_action):
        search_str = f"{search_state or '—'}/{search_action or '—'}"
    recheck_str = "none"
    if recheck_action:
        recheck_str = "blocked" if recheck_blocked else (recheck_action or "—")
    exp_str = "none"
    if exp_type or exp_status:
        exp_str = exp_status or exp_type or "—"
    parts = [
        f"fg={fg}",
        f"tc_state={tc_state}",
        f"arb={arb}",
        f"bundle={bundle_str}",
        f"search={search_str}",
        f"recheck={recheck_str}",
        f"exp={exp_str}",
    ]
    integration_summary = "; ".join(parts)

    observation_frame_note = f"consumed={len(consumed)} soft={len(soft_actions)} blocked={len(blocked_actions)} eff_mod={len(effective)}"

    return MainlineIntegrationResult(
        integration_enabled=True,
        integration_summary=integration_summary,
        integration_consumed_modules=consumed,
        integration_soft_actions=soft_actions,
        integration_blocked_actions=blocked_actions,
        integration_observation_notes=observation_notes,
        integration_applied=True,
        integration_observation_frame_note=observation_frame_note,
        integration_observed_modules=consumed,
        integration_effective_modules=effective,
        integration_pillar_effective=pillar_effective,
    )
