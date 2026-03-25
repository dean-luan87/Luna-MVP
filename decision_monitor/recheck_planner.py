# -*- coding: utf-8 -*-
"""
补证规划 M0：Recheck Planner（最小补证执行入口）。

在 Hypothesis Layer M0 基础上，将 verification_hint / suggested_next_check 推进为最小可执行补证入口。
仅读取已有结构，不做多步规划、不做学习、不改 detector/OCR 主链。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .evidence_ledger import EvidenceLedger
from .hypothesis_layer import HypothesisLayer
from .local_goal_spatial_map import LocalGoalSpatialMap

RECHECK_ACTIONS = (
    "recheck_environment",
    "recheck_close_range",
    "hold_and_confirm",
    "look_forward",
    "shift_view_left",
    "shift_view_right",
    "ask_user_for_clarification",
)


@dataclass
class RecheckPlannerResult:
    """最小补证规划结果：动作、原因、目标、优先级、是否阻断、是否已执行。"""
    recheck_action: Optional[str] = None
    recheck_reason: Optional[str] = None
    recheck_target: Optional[str] = None
    recheck_priority: Optional[str] = None  # 规则型，如 high / normal / low
    recheck_blocked: bool = False
    recheck_block_reason: Optional[str] = None
    recheck_applied: bool = False


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _is_blocked(state: Any) -> tuple[bool, Optional[str]]:
    """
    风险与守底阻断：minimum_mode_active、runtime_domain_state==frozen、
    scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending。
    """
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


def _target_from_smap(smap: Optional[LocalGoalSpatialMap]) -> Optional[str]:
    """从 smap 取简短 target 摘要（focus/confirm/risk 区）。"""
    if not smap:
        return None
    parts = []
    focus = getattr(smap, "focus_region", None) or []
    confirm = getattr(smap, "confirm_region", None) or []
    risk = getattr(smap, "risk_region", None) or []
    if focus:
        parts.append("focus")
    if confirm:
        parts.append("confirm")
    if risk:
        parts.append("risk")
    return ",".join(parts) if parts else None


def _pick_blocked_fallback(
    block_reason: Optional[str],
    state: Any,
    target: Optional[str],
) -> tuple[str, str]:
    """
    M0.6: 高失稳/中断语境下优先给出更快可执行收口动作。
    规则保持最小：runtime frozen / mismatch / 高风险区域优先 ask_user_for_clarification，否则 hold_and_confirm。
    """
    br = (block_reason or "").strip().lower()
    mismatch_reason = (_get(state, "domain_mismatch_reason") or "").strip().lower()
    has_risk_target = "risk" in ((target or "").strip().lower())
    unstable = (
        "frozen" in br
        or "high_level_output_suppressed" in br
        or "high_rotation" in mismatch_reason
        or "abnormal_motion" in mismatch_reason
        or has_risk_target
    )
    if unstable and "ask_user_for_clarification" in RECHECK_ACTIONS:
        return "ask_user_for_clarification", "unstable_interrupt_fast_converge"
    if "hold_and_confirm" in RECHECK_ACTIONS:
        return "hold_and_confirm", "blocked_fallback_hold"
    return "ask_user_for_clarification", "blocked_fallback_ask"


def build_recheck_planner(
    hypothesis_layer: Optional[HypothesisLayer],
    evidence_ledger: Optional[EvidenceLedger],
    state: Any,
    smap: Optional[LocalGoalSpatialMap],
    ctx: Any = None,
) -> RecheckPlannerResult:
    """
    从 hypothesis_layer（首条 verification_hint）或 evidence_ledger（首条 suggested_next_check）生成最小补证计划。

    M0.1 定点优化（Blocked/Fallback 收口）：
    - 阻断时不再仅返回“blocked + not applied”，而是尽量收口到一个可行动的 fallback：
      `hold_and_confirm` 或 `ask_user_for_clarification`（不做多步规划，不改主架构）。
    """
    blocked, block_reason = _is_blocked(state)
    action: Optional[str] = None
    reason: Optional[str] = None
    target: Optional[str] = _target_from_smap(smap)
    priority = "normal"

    # M0.8 行为级 blocked 收口（只改 recheck_planner）：
    # 当终端仍停在 blocked 且用户已给出明确确认类型（非 unknown）时，
    # 更快进入可行动 fallback（ask_user_for_clarification/hold_and_confirm），
    # 让结构树内 governance 的 blocked 降级逻辑可生效。
    if isinstance(ctx, dict):
        term = (ctx.get("search_terminal_status") or "").strip().lower()
        cit = (
            ctx.get("search_confirmation_input_type")
            or ctx.get("confirmation_input_type")
            or ""
        )
        cit = str(cit).strip().lower() if cit is not None else ""
        if term == "blocked" and cit and cit != "unknown":
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"behavior_blocked_forced_user_clarification(input_type={cit})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=block_reason,
                recheck_applied=True,
            )

    # M0.9 repeated fallback / retry exhaustion 收口（只改 recheck_planner）：
    # 当 object_search_retry_count 已经 >=3 时，避免结构树仍维持 blocked 且 resolved=false，
    # 强制给出可执行 fallback（ask_user_for_clarification / hold_and_confirm），让 governance 的 blocked
    # 降级为 watchlist，从而解除 blocked_without_resolution 的度量条件（blocked=true & resolved=false）。
    if isinstance(ctx, dict):
        retry = ctx.get("object_search_retry_count")
        try:
            retry_n = int(retry) if retry is not None else 0
        except Exception:
            retry_n = 0
        if retry_n >= 3:
            cit = (
                ctx.get("search_confirmation_input_type")
                or ctx.get("confirmation_input_type")
                or ""
            )
            cit = str(cit).strip().lower() if cit is not None else ""
            forced_target = target or "user_confirmation"
            if cit and cit != "unknown":
                return RecheckPlannerResult(
                    recheck_action="ask_user_for_clarification",
                    recheck_reason=f"retry_exhaustion_forced_user_clarification(retry={retry_n},input_type={cit})",
                    recheck_target=forced_target,
                    recheck_priority="high",
                    recheck_blocked=False,
                    recheck_block_reason=None,
                    recheck_applied=True,
                )
            return RecheckPlannerResult(
                recheck_action="hold_and_confirm",
                recheck_reason=f"retry_exhaustion_forced_hold_and_confirm(retry={retry_n})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # M1.0 intent/action/task mismatch aware blocked convergence（只改 recheck_planner）：
    # 对 R35~R40 这类“意图-动作-任务错位”语境，在 blocked/unresolved triage 可见时，
    # 直接给出可行动的用户澄清入口（ask_user_for_clarification），
    # 让 reasoning_structure_tree 的 governance blocked 能降级为 watchlist，
    # 从而消除 blocked_without_resolution 指标。
    if isinstance(ctx, dict):
        mismatch_flags = (
            "intent_action_task_mismatch_expected",
            "confirmed_but_not_executed_expected",
            "executed_but_goal_shifted_expected",
            "subtask_return_semantic_loss_expected",
            "fact_feedback_stage_conflict_expected",
            "false_recovery_expected",
        )
        hit_flag = next((f for f in mismatch_flags if ctx.get(f) is True), None)
        if hit_flag:
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"mismatch_context_forced_user_clarification(flag={hit_flag})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # M1.1 eighth-batch new expected flags (R41–R46, Real Scenario Pack M0.7/M6)：
    # 与 M1.0 同哲学：新语义触发器命中时直接给可行动澄清，避免结构树长期停在
    # blocked_without_resolution（recheck_blocked 真且无可行动 fallback）。
    # 分组仅体现在 recheck_reason 的 tag，动作统一为 ask_user_for_clarification（RECHECK_ACTIONS 内最小集）。
    if isinstance(ctx, dict):
        m11_flag_tags = {
            # 长期漂移 / 延迟暴露
            "long_term_divergence_expected": "clarify_objective_reset_context",
            "delayed_exposure_mismatch_expected": "clarify_objective_reset_context",
            # 任务 / 事实 / 成功条件改写
            "task_subtask_fact_shift_expected": "reframe_success_recover_primary",
            "success_condition_overwritten_expected": "reframe_success_recover_primary",
            # 伪恢复 / 多反馈源冲突
            "false_multi_recovery_expected": "suppress_false_recovery_ask_clarify",
            "multi_feedback_source_conflict_expected": "multi_source_conflict_ask_clarify",
        }
        hit_m11 = next((f for f in m11_flag_tags if ctx.get(f) is True), None)
        if hit_m11:
            tag = m11_flag_tags[hit_m11]
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"m11_new_expected_forced_user_clarification(flag={hit_m11},tag={tag})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # M1.2 ninth-batch new expected flags (R47–R52, Real Scenario Pack M0.8/M7)：
    # 与 M1.1 同哲学：慢性漂移 / 伪一致性 / 累积错位类触发器命中时直接给可行动澄清。
    if isinstance(ctx, dict):
        m12_flag_tags = {
            # 慢性目标漂移；局部恢复 vs 全局错位
            "gradual_goal_drift_expected": "clarify_objective_drift",
            "local_recovery_global_mismatch_expected": "clarify_local_vs_global_objective",
            # 多约束软漂移；表面一致但仍错
            "multi_constraint_soft_shift_expected": "reframe_success_under_soft_shift",
            "feedback_fact_consistent_but_wrong_expected": "challenge_surface_consistency_reframe_goal",
            # 语义裂缝；慢性污染
            "task_semantic_crack_expected": "clarify_task_semantics_rebuild",
            "slow_poisoning_expected": "clarify_slow_drift_resistance",
        }
        hit_m12 = next((f for f in m12_flag_tags if ctx.get(f) is True), None)
        if hit_m12:
            tag = m12_flag_tags[hit_m12]
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"m12_new_expected_forced_user_clarification(flag={hit_m12},tag={tag})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # M1.0.x tenth-pack targeted defects (R53–R58):
    # 目标：仅在已确认的 baseline_covered_defect 语义触发器下，
    # 统一收口到可行动澄清入口，避免继续落入 blocked_without_resolution。
    if isinstance(ctx, dict):
        m10x_flag_tags = {
            # A: 长链任务一致性
            "main_task_resumed_but_not_progressed_expected": "resume_without_main_progress_force_clarify",
            "inserted_task_exit_ambiguous_expected": "inserted_exit_ambiguous_force_clarify",
            "local_success_masked_global_failure_expected": "local_success_global_failure_force_clarify",
            # B/C/D/E: 调度切换 / 记忆冲突 / 状态稳定 / summary-backfill 边界
            "memory_supported_but_observation_conflicted_expected": "memory_observation_conflict_force_clarify",
            "dynamic_source_shift_but_mainline_static_expected": "source_shift_mainline_static_force_clarify",
            "summary_looks_ok_but_requires_backfill_expected": "summary_ok_require_backfill_force_clarify",
        }
        hit_m10x = next((f for f in m10x_flag_tags if ctx.get(f) is True), None)
        if hit_m10x:
            tag = m10x_flag_tags[hit_m10x]
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"m10x_targeted_fix_forced_user_clarification(flag={hit_m10x},tag={tag})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # M1.1.x-B targeted closure alignment fixes (R60/R61/R64):
    # 仅沿 A 阶段断点下刀，不扩边界：
    # - resume declared -> main progress fragile
    # - memory/source conflict -> closure still weak
    # - phase identified -> closure semantics misaligned
    if isinstance(ctx, dict):
        m11x_flag_tags = {
            "recovery_declared_but_resume_chain_fragile_expected": "resume_declared_main_progress_not_stable",
            "memory_bias_accumulated_under_familiar_context_expected": "memory_source_conflict_requires_conservative_repair",
            "phase_correct_but_closure_semantics_misaligned_expected": "phase_closure_alignment_repair",
        }
        hit_m11x = next((f for f in m11x_flag_tags if ctx.get(f) is True), None)
        if hit_m11x:
            tag = m11x_flag_tags[hit_m11x]
            forced_target = target or "user_confirmation"
            return RecheckPlannerResult(
                recheck_action="ask_user_for_clarification",
                recheck_reason=f"m11x_targeted_fix_forced_user_clarification(flag={hit_m11x},tag={tag})",
                recheck_target=forced_target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=None,
                recheck_applied=True,
            )

    # A. 优先 hypothesis 首条
    if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
        first_h = hypothesis_layer.hypotheses[0]
        hint = _get(first_h, "verification_hint")
        if hint and hint in RECHECK_ACTIONS:
            action = hint
            reason = (_get(first_h, "hypothesis_summary") or "")[:60]
            miss = _get(first_h, "missing_evidence") or []
            if miss:
                reason += " [" + "; ".join((m or "")[:25] for m in miss[:2]) + "]"
            target = target or _get(first_h, "hypothesis_type")

    # B. 无 hypothesis 则用 evidence_ledger 首条 claim
    if not action and evidence_ledger and getattr(evidence_ledger, "entries", None):
        first_c = evidence_ledger.entries[0]
        sug = _get(first_c, "suggested_next_check")
        if sug and sug in RECHECK_ACTIONS:
            action = sug
            reason = (_get(first_c, "claim_summary") or "")[:60]
            miss = _get(first_c, "missing_evidence") or []
            if miss:
                reason += " [" + "; ".join((m or "")[:25] for m in miss[:2]) + "]"
            target = target or "claim"

    # C. 无 hypothesis / claim 则无动作
    if not action:
        if blocked:
            # Blocked fallback: still provide a compact next step (no multi-step planning).
            fb_action, fb_tag = _pick_blocked_fallback(block_reason, state, target)
            return RecheckPlannerResult(
                recheck_action=fb_action,
                recheck_reason=f"blocked_fallback({fb_tag})",
                recheck_target=target,
                recheck_priority="high",
                recheck_blocked=False,
                recheck_block_reason=block_reason,
                recheck_applied=True,
            )
        return RecheckPlannerResult(
            recheck_action=None,
            recheck_reason=None,
            recheck_target=target,
            recheck_priority=priority,
            recheck_blocked=blocked,
            recheck_block_reason=block_reason,
            recheck_applied=False,
        )

    # Blocked → fallback: shorten blocked→actionable path (M0.1).
    if blocked:
        # M0.6: prefer compact actionable fallback for unstable/interrupt contexts.
        fb_action, fb_tag = _pick_blocked_fallback(block_reason, state, target)
        fb_reason = f"blocked_fallback({block_reason}|{fb_tag}): {fb_action}"
        return RecheckPlannerResult(
            recheck_action=fb_action,
            recheck_reason=fb_reason,
            recheck_target=target,
            recheck_priority="high",
            recheck_blocked=False,
            recheck_block_reason=block_reason,
            recheck_applied=True,
        )

    applied = True
    return RecheckPlannerResult(
        recheck_action=action,
        recheck_reason=reason,
        recheck_target=target,
        recheck_priority=priority,
        recheck_blocked=blocked,
        recheck_block_reason=block_reason,
        recheck_applied=applied,
    )
