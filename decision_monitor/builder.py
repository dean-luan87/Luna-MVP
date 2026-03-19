# -*- coding: utf-8 -*-
"""
DecisionMonitorBuilder：从现有 runtime 信息拼成一条 DecisionMonitorFrame。

允许部分字段轻量占位；必须能标出最后拍板者（controller / sampling_gate / module_gate / b2_impact / floor_guard）。
"""

from __future__ import annotations

import time
from dataclasses import replace
from typing import Any, Dict, Optional

from .schema import (
    DecisionMonitorFrame,
    GoalLayer,
    InputsLayer,
    StateLayer,
    DecisionLayer,
    OutputsLayer,
    ConsequenceLayer,
)
from . import goal_resolver
from . import consequence_evaluator
from . import state_tracker
from . import view_guard
from . import predictive_hold
from . import runtime_domain_guard
from . import scene_gate
from . import interaction_calibrator
from . import local_goal_state_builder
from . import local_goal_spatial_map_builder
from . import local_goal_spatial_relations
from . import skeleton_mix
from . import skeleton_filter
from . import spatial_memory_pools
from . import spatial_forgetting
from . import evidence_ledger
from . import hypothesis_layer
from . import recheck_planner
from . import object_temporal_ledger
from . import object_search_interaction
from . import task_arbitration
from . import task_bundle
from . import task_chain_bridge
from . import experience_evolution
from . import mainline_integration
from . import visual_candidate_audit
from . import spatial_expression_sidecar
from . import action_hint_copy
from . import confirmation_input_bridge
from . import local_task_space_grid
from . import grid_search_expansion
from . import grid_search_whitebox_trace
from . import recheck_whitebox_trace
from . import action_hint_whitebox_trace
from . import confirmation_whitebox_trace
from . import evidence_hypothesis_whitebox_trace
from . import experience_governance_whitebox_trace
from .spatial_expression_sidecar import build_focus_target_actionable_expression


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _append_grid_suffix(text: Optional[str], grid_label: Optional[str]) -> Optional[str]:
    """风格 A：{原文案}（{格标签}）。保持原主体，Grid 只补位。"""
    if not (text or "").strip():
        return text
    if not (grid_label or "").strip():
        return text
    t = (text or "").strip()
    gl = (grid_label or "").strip()
    # 避免重复追加
    if f"（{gl}）" in t:
        return t
    return f"{t}（{gl}）"


def _append_hint_suffix(text: Optional[str], hint: Optional[str]) -> Optional[str]:
    """把扩搜建议作为附加建议追加到末尾，不替代原文案。"""
    if not (hint or "").strip():
        return text
    if not (text or "").strip():
        return (hint or "").strip()
    t = (text or "").strip()
    h = (hint or "").strip()
    if h in t:
        return t
    return f"{t}；{h}"


def _bbox_contains(outer: Any, inner: Any, min_iou: float = 0.0) -> bool:
    """
    very small helper: returns True when inner bbox center is inside outer bbox.
    bbox format accepted: [x1,y1,x2,y2] or dict{"x1","y1","x2","y2"}.
    """
    def _to_xyxy(b: Any) -> Optional[tuple[float, float, float, float]]:
        if b is None:
            return None
        if isinstance(b, (list, tuple)) and len(b) >= 4:
            return float(b[0]), float(b[1]), float(b[2]), float(b[3])
        if isinstance(b, dict):
            if all(k in b for k in ("x1", "y1", "x2", "y2")):
                return float(b["x1"]), float(b["y1"]), float(b["x2"]), float(b["y2"])
        return None

    o = _to_xyxy(outer)
    i = _to_xyxy(inner)
    if not o or not i:
        return False
    ox1, oy1, ox2, oy2 = o
    ix1, iy1, ix2, iy2 = i
    cx = (ix1 + ix2) / 2.0
    cy = (iy1 + iy2) / 2.0
    if not (min(ox1, ox2) <= cx <= max(ox1, ox2) and min(oy1, oy2) <= cy <= max(oy1, oy2)):
        return False
    if min_iou <= 0:
        return True
    # optional: tiny IoU check (rarely used, keep simple)
    ax1, ay1, ax2, ay2 = min(ox1, ox2), min(oy1, oy2), max(ox1, ox2), max(oy1, oy2)
    bx1, by1, bx2, by2 = min(ix1, ix2), min(iy1, iy2), max(ix1, ix2), max(iy1, iy2)
    inter_x1, inter_y1 = max(ax1, bx1), max(ay1, by1)
    inter_x2, inter_y2 = min(ax2, bx2), min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter = inter_w * inter_h
    a_area = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    b_area = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    denom = (a_area + b_area - inter) or 1.0
    iou = inter / denom
    return iou >= float(min_iou)


def _bbox_intersection_ratio(a: Any, b: Any) -> float:
    """Return intersection area / area(b). 0 when unknown."""
    def _to_xyxy(x: Any) -> Optional[tuple[float, float, float, float]]:
        if x is None:
            return None
        if isinstance(x, (list, tuple)) and len(x) >= 4:
            return float(x[0]), float(x[1]), float(x[2]), float(x[3])
        if isinstance(x, dict) and all(k in x for k in ("x1", "y1", "x2", "y2")):
            return float(x["x1"]), float(x["y1"]), float(x["x2"]), float(x["y2"])
        return None
    aa = _to_xyxy(a)
    bb = _to_xyxy(b)
    if not aa or not bb:
        return 0.0
    ax1, ay1, ax2, ay2 = min(aa[0], aa[2]), min(aa[1], aa[3]), max(aa[0], aa[2]), max(aa[1], aa[3])
    bx1, by1, bx2, by2 = min(bb[0], bb[2]), min(bb[1], bb[3]), max(bb[0], bb[2]), max(bb[1], bb[3])
    inter_x1, inter_y1 = max(ax1, bx1), max(ay1, by1)
    inter_x2, inter_y2 = min(ax2, bx2), min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter = inter_w * inter_h
    b_area = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    return float(inter / (b_area or 1.0))


def _infer_object_search_hint_evidence(ctx: Dict[str, Any]) -> Optional[evidence_ledger.EvidenceLedgerEntry]:
    """
    Object-search hint (M0): when focus label exists and vision suggests container/occlusion,
    inject a high-signal evidence entry so hypothesis_layer/object_temporal_ledger can trigger flows.
    """
    focus = (ctx.get("focus_object_label") or "").strip()
    if not focus:
        return None

    objects = ctx.get("visual_audit_objects") or ctx.get("visual_audit_objects_main") or ctx.get("objects") or []
    if not isinstance(objects, list) or not objects:
        return None

    # normalize labels
    def _lab(o: Any) -> str:
        if isinstance(o, dict):
            return (o.get("label") or o.get("class") or "").strip()
        return str(getattr(o, "label", "") or getattr(o, "class", "") or "").strip()

    def _bbox(o: Any) -> Any:
        if isinstance(o, dict):
            return o.get("bbox")
        return getattr(o, "bbox", None)

    cups = [o for o in objects if _lab(o) in ("cup", "bowl", "wine glass")]
    bottles = [o for o in objects if _lab(o) in ("bottle",)]
    texts = ctx.get("visual_audit_texts") or []
    has_ocr_text = bool(texts)

    # container: bottle center inside a cup => treat as in-container candidate
    for c in cups:
        for b in bottles:
            if _bbox_contains(_bbox(c), _bbox(b)):
                cup_label = _lab(c) or "cup"
                return evidence_ledger.EvidenceLedgerEntry(
                    claim_summary=f"容器候选：{cup_label} | 目标疑似在容器内（object_search_hint）",
                    supporting_evidence=[
                        f"focus_object_label={focus[:24]}",
                        f"vision:container={cup_label}",
                        "vision:target=bottle_in_container",
                    ],
                    conflicting_evidence=[],
                    missing_evidence=["需要打开容器确认目标是否在杯子/容器内"],
                    evidence_confidence=0.72,
                    risk_if_wrong="误判容器可能导致搜索动作错误",
                    suggested_next_check="recheck_close_range",
                )

    # occlusion: bottle overlaps cup significantly => treat as occlusion candidate (even if bottle detected)
    if cups and bottles:
        cup0 = cups[0]
        b0 = bottles[0]
        ratio = _bbox_intersection_ratio(_bbox(cup0), _bbox(b0))
        if ratio >= 0.35:
            cup_label = _lab(cup0) or "cup"
            return evidence_ledger.EvidenceLedgerEntry(
                claim_summary=f"遮挡候选：{cup_label} | 目标与容器显著重叠，疑似遮挡（object_search_hint）",
                supporting_evidence=[
                    f"focus_object_label={focus[:24]}",
                    f"vision:overlap_ratio={ratio:.2f}",
                    f"vision:container={cup_label}",
                ],
                conflicting_evidence=[],
                missing_evidence=["需要清理遮挡或调整视角复核目标"],
                evidence_confidence=0.62,
                risk_if_wrong="遮挡误判可能导致搜索动作错误",
                suggested_next_check="recheck_environment",
            )

    # occlusion: "维生素/药瓶" 这类细粒度目标，只有 bottle 粗类但无 OCR 文本证据时，引导用户补证（近场/遮挡清理）
    if bottles and (("维生素" in focus) or ("药" in focus)) and (not has_ocr_text):
        return evidence_ledger.EvidenceLedgerEntry(
            claim_summary="遮挡候选：需文字/近场补证 | 目标为药瓶类但缺少 OCR 证据（object_search_hint）",
            supporting_evidence=[
                f"focus_object_label={focus[:24]}",
                "vision:detected=bottle",
                "ocr:empty",
            ],
            conflicting_evidence=[],
            missing_evidence=["需要靠近或调整视角以获取文字证据，或清理遮挡复核"],
            evidence_confidence=0.58,
            risk_if_wrong="补证建议不当可能增加交互成本",
            suggested_next_check="recheck_close_range",
        )

    # occlusion: if focus exists but target not detected in main while container exists, suggest occlusion/need recheck
    if cups and not bottles:
        cup_label = _lab(cups[0]) or "cup"
        return evidence_ledger.EvidenceLedgerEntry(
            claim_summary=f"遮挡候选：{cup_label} | 目标未直接出现，疑似遮挡/在容器附近（object_search_hint）",
            supporting_evidence=[
                f"focus_object_label={focus[:24]}",
                f"vision:has_container={cup_label}",
                "vision:target_not_in_main",
            ],
            conflicting_evidence=[],
            missing_evidence=["需要清理遮挡或打开容器复核目标"],
            evidence_confidence=0.55,
            risk_if_wrong="遮挡误判可能导致漏检目标",
            suggested_next_check="recheck_environment",
        )

    return None


class DecisionMonitorBuilder:
    """
    从主循环上下文拼装一帧 monitor。
    ctx 建议包含（来自 main process_frame 与 obs_loop.step 之后）：
    - frame_seq, current_ts, delta_t_ms, sampled
    - obs (ObservationFrame: motion, path, branch, ...)
    - policy_intent (PolicyIntent: mode, sampling_target_fps, heavy_infer_stride, ocr_stride, b2_impact_applied, ...)
    - policy_should_sample, policy_run_detector, policy_run_ocr
    - detector_floor_due, ocr_floor_due, escape_hatch (detector/ocr fired)
    - pipeline_result / telemetry
    - decision (A3: safety_level, risk_score)
    - risk_score, safe_edge_state
    - b2_impact_frame_telem (weak_evidence_level 等)
    """

    def __init__(self, trace_anchor_id_prefix: str = "frame"):
        self._trace_anchor_id_prefix = trace_anchor_id_prefix
        self._frame_seq = 0
        self._state_tracker = state_tracker.StateTracker()
        self._predictive_hold = predictive_hold.PredictiveHold()

    def build(self, ctx: Dict[str, Any]) -> DecisionMonitorFrame:
        self._frame_seq += 1
        seq = ctx.get("frame_seq") if ctx.get("frame_seq") is not None else self._frame_seq
        now = ctx.get("current_ts") if ctx.get("current_ts") is not None else time.time()
        obs = ctx.get("obs")
        policy_intent = ctx.get("policy_intent")
        policy_should_sample = ctx.get("policy_should_sample")
        policy_run_detector = ctx.get("policy_run_detector", True)
        policy_run_ocr = ctx.get("policy_run_ocr", True)
        detector_floor_due = ctx.get("detector_floor_due", False)
        ocr_floor_due = ctx.get("ocr_floor_due", False)
        escape_hatch_triggered = bool(
            ctx.get("detector_escape_hatch_fired", False) or ctx.get("ocr_escape_hatch_fired", False)
        )
        floor_forced = detector_floor_due or ocr_floor_due

        # 最后拍板者
        decision_owner = self._resolve_decision_owner(
            policy_should_sample=policy_should_sample,
            floor_forced=floor_forced,
            escape_hatch_triggered=escape_hatch_triggered,
            b2_impact_applied=bool(_get(policy_intent, "b2_impact_applied", False)),
        )
        decision_type = self._resolve_decision_type(
            policy_should_sample=policy_should_sample,
            floor_forced=floor_forced,
            policy_run_detector=policy_run_detector,
            policy_run_ocr=policy_run_ocr,
        )

        goal = goal_resolver.resolve(ctx)
        inputs = self._build_inputs(ctx, seq, now, obs, policy_intent)
        state = self._build_state(ctx, obs, policy_intent)
        decision = self._build_decision(
            ctx, seq, decision_owner, decision_type,
            policy_intent, policy_should_sample, escape_hatch_triggered, floor_forced,
        )
        # 主线 1.3：状态层连续化（上一帧镜像 + 差分 + 趋势）
        continuous = self._state_tracker.update(state, decision, goal, ctx)
        state = self._enrich_state_continuity(state, continuous)
        # 主线 1.3A：视线/视觉连续性守护
        state = self._enrich_state_view_guard(state, view_guard.evaluate(ctx))
        # 主线 1.3B：短时预演容错
        state = self._enrich_state_predictive_hold(
            state, self._predictive_hold.evaluate(ctx, state, decision)
        )
        # 主线 1.3C：运行域守卫
        state = self._enrich_state_runtime_domain_guard(
            state, runtime_domain_guard.evaluate(ctx, state, decision)
        )
        # Scene Gate v1：日常场景分类 + 非支持场景挂起
        state = self._enrich_state_scene_gate(
            state, scene_gate.evaluate(ctx, state, goal)
        )
        # Scene Gate 轻量控制：根据 scene_gate_action 写入 4 个控制字段并 patch goal
        state, goal = self._apply_scene_gate_control(state, goal)
        # 人工沟通校准：若需要确认则暂缓高代价动作，等待用户回复或超时（测试可传 skip_human_check 跳过）
        if not ctx.get("skip_human_check"):
            cal = interaction_calibrator.evaluate(ctx, state)
            state, goal = self._apply_interaction_calibrator(state, goal, cal, ctx)
        outputs = self._build_outputs(ctx, policy_intent, policy_run_detector, policy_run_ocr)
        consequence = consequence_evaluator.evaluate(ctx, decision, outputs)
        # 主线 2.0：局部时空状态图
        local_goal_state = local_goal_state_builder.build(ctx, goal, state, inputs, outputs, consequence)
        # 主线 2 第二阶段 M0/M1.5：局部目标空间图 + 标尺层
        local_goal_spatial_map = local_goal_spatial_map_builder.build(ctx, local_goal_state, state, inputs)
        scene_profile = getattr(local_goal_spatial_map, "scene_profile", None) or "outdoor"
        spatial_scale = local_goal_spatial_map_builder.build_spatial_scale(ctx, state, scene_profile)
        # M2：区域关系
        relations_list = local_goal_spatial_relations.build_relations(local_goal_spatial_map)
        # Skeleton Mix M0：当前帧骨架配比（规则型）
        mix = skeleton_mix.build_skeleton_mix(goal, state, local_goal_spatial_map)
        # 骨架过滤 M0：基于 mix 生成当前帧过滤策略结果
        filt = skeleton_filter.build_skeleton_filter(mix)
        # 骨架记忆分池 M0：基于 mix / filt / smap / relations 分流到四层记忆池
        pools = spatial_memory_pools.build_spatial_memory_pools(
            mix, filt, local_goal_spatial_map, relations_list, goal
        )
        # 空间遗忘 M0：对 pools 应用 TTL / task-end collapse / episode 过期，得到更新后池与遗忘摘要
        pools, forgetting_summary = spatial_forgetting.apply_spatial_forgetting(
            pools,
            goal,
            state,
            now,
            prev_goal_type=ctx.get("prev_goal_type"),
            prev_goal_status=ctx.get("prev_goal_status"),
            prev_dominant=ctx.get("prev_dominant"),
        )
        # 证据账本 M0：从 smap/relations/mix/filt/pools/forgetting 生成证据账本
        ledger = evidence_ledger.build_evidence_ledger(
            local_goal_spatial_map,
            relations_list,
            mix,
            filt,
            pools,
            forgetting_summary,
            goal,
            state,
        )
        # Object-search hint evidence (M0): inject high-signal container/occlusion hint from real vision
        try:
            hint_entry = _infer_object_search_hint_evidence(ctx)
            if hint_entry:
                ledger.entries = [hint_entry] + (list(getattr(ledger, "entries", None) or []))
        except Exception:
            # best-effort only; do not break monitor building
            pass
        # 假设层 M0：从 ledger/smap/relations/mix/filt/pools 生成受约束候选假设
        hyp_layer = hypothesis_layer.build_hypothesis_layer(
            ledger,
            local_goal_spatial_map,
            relations_list,
            mix,
            filt,
            pools,
            state,
        )
        # 补证规划 M0：将 verification_hint / suggested_next_check 推进为最小可执行补证
        recheck_result = recheck_planner.build_recheck_planner(
            hyp_layer,
            ledger,
            state,
            local_goal_spatial_map,
        )
        # 对象时空账本 M1.5：单对象优先；最小容器逻辑；用户确认/否认写回（含 M1 寻物用户回复映射）
        search_user_last = ctx.get("search_user_last_location")
        search_container_no = (ctx.get("search_user_container_answer") or "").strip().lower() in ("no", "n", "否")
        object_user_confirmed = ctx.get("object_user_confirmed_location") or (search_user_last if search_user_last else None)
        object_user_denied = ctx.get("object_user_denied_location")
        if search_container_no and ctx.get("object_container_candidate"):
            object_user_denied = object_user_denied or ctx.get("object_container_candidate")
        obj_ledger = object_temporal_ledger.build_object_temporal_ledger(
            ctx.get("focus_object_label"),
            local_goal_spatial_map,
            ledger,
            hyp_layer,
            recheck_result,
            pools,
            now,
            prev_last_confirmed_location=ctx.get("object_last_confirmed_location"),
            prev_last_confirmed_ts=ctx.get("object_last_confirmed_ts"),
            prev_container_candidate=ctx.get("object_container_candidate"),
            prev_container_confidence=ctx.get("object_container_confidence"),
            prev_container_state=ctx.get("object_container_state"),
            prev_container_last_event_ts=ctx.get("object_container_last_event_ts"),
            prev_visibility_status=ctx.get("object_visibility_status"),
            object_user_confirmed_location=object_user_confirmed,
            object_user_denied_location=object_user_denied,
        )
        # 静态图输入桥 + 候选审计 M0（提前以便 sidecar → search 文案 M0.5 使用）
        audit_result = visual_candidate_audit.build_visual_candidate_audit(
            ctx.get("visual_audit_objects"),
            ctx.get("visual_audit_objects_probe"),
            ctx.get("visual_audit_texts"),
            ctx.get("visual_audit_description"),
            ctx.get("focus_object_label"),
            ctx.get("input_source_type"),
            ctx.get("input_source_path"),
            ctx.get("visual_audit_detector_mode"),
            ctx.get("visual_audit_detector_model_name"),
        )
        # 坐标/方位表达旁路 M0：仅基于真实视觉候选 + 映射结果生成二维相对表达
        sidecar = spatial_expression_sidecar.build_spatial_expression_sidecar(
            focus_target_label=ctx.get("focus_object_label"),
            objects_main=ctx.get("visual_audit_objects"),
            objects_probe=ctx.get("visual_audit_objects_probe"),
            mapped_candidate_labels=getattr(audit_result, "mapped_candidate_labels", None),
            image_width=ctx.get("input_image_width"),
            image_height=ctx.get("input_image_height"),
            max_candidates=5,
        )
        # 交互式寻物 M1/M1.5：子任务状态机 + 用户回复注入 + flow/timeout/fallback/path；M0.5 文案接入 sidecar
        _path_raw = ctx.get("object_search_resolution_path")
        _path_list = _path_raw.split(",") if isinstance(_path_raw, str) and _path_raw.strip() else (list(_path_raw) if isinstance(_path_raw, list) else None)
        search_interaction = object_search_interaction.build_object_search_interaction(
            ctx.get("focus_object_label"),
            obj_ledger,
            ledger,
            hyp_layer,
            recheck_result,
            state,
            prev_subtask_state=ctx.get("search_subtask_state"),
            prev_last_interaction_action=ctx.get("last_interaction_action"),
            prev_search_terminal_status=ctx.get("search_terminal_status"),
            search_user_object_appearance=ctx.get("search_user_object_appearance"),
            search_user_last_location=ctx.get("search_user_last_location"),
            search_user_container_answer=ctx.get("search_user_container_answer"),
            search_user_occlusion_cleared=ctx.get("search_user_occlusion_cleared"),
            search_user_checked_pocket=ctx.get("search_user_checked_pocket"),
            search_user_cancelled=ctx.get("search_user_cancelled"),
            prev_flow_type=ctx.get("object_search_flow_type"),
            prev_step_index=ctx.get("object_search_step_index"),
            prev_resolution_path=_path_list,
            prev_retry_count=ctx.get("object_search_retry_count"),
            interaction_timeout_ms=ctx.get("object_search_timeout_ms"),
            interaction_timeout_triggered=ctx.get("object_search_timeout_triggered"),
            focus_target_expression=getattr(sidecar, "focus_target_expression", None),
        )
        # Level 2 口语化行动表达 M0：在 sidecar + search 基础上生成 actionable，并回写 sidecar / search 文案
        act_expr, act_dbg, zone_ov, step_ov = build_focus_target_actionable_expression(
            sidecar, search_interaction, obj_ledger
        )
        if act_expr is not None:
            sidecar = replace(
                sidecar,
                focus_target_actionable_expression=act_expr,
                focus_target_actionable_debug_reason=act_dbg,
            )
        if zone_ov is not None:
            search_interaction = replace(search_interaction, suggested_search_zone=zone_ov)
        if step_ov is not None:
            search_interaction = replace(search_interaction, next_search_step_summary=step_ov)
        # Action Hint Copy M0：推理→引导→确认 文案链（只读 search/sidecar/ledger 等，不反写）
        action_hint_result = action_hint_copy.build_action_hint_copy(
            search_interaction,
            sidecar,
            obj_ledger,
            evidence_ledger=ledger,
            hypothesis_layer=hyp_layer,
            recheck_planner=recheck_result,
        )
        # Confirmation Input Bridge M0：用户反馈 → 最小推进（只读 search，不反写主逻辑）
        import os as _os
        confirmation_type = (
            ctx.get("search_confirmation_input_type")
            or ctx.get("confirmation_input_type")
            or _os.environ.get("CONFIRMATION_INPUT_TYPE", "").strip() or None
        )
        confirmation_raw = (
            ctx.get("search_confirmation_input_raw_text")
            or ctx.get("confirmation_input_raw_text")
            or _os.environ.get("CONFIRMATION_INPUT_RAW_TEXT", "").strip() or None
        )
        confirmation_bridge_result = confirmation_input_bridge.build_confirmation_input_bridge(
            search_interaction,
            confirmation_input_type=confirmation_type,
            confirmation_input_raw_text=confirmation_raw,
        )
        # 最小推进：仅对 terminal 类效果改写 search_interaction 本帧
        next_eff = getattr(confirmation_bridge_result, "confirmation_bridge_next_effect", None)
        if next_eff == "mark_target_found":
            search_interaction = replace(
                search_interaction,
                search_terminal_status="found",
                search_can_resume_main_task=True,
            )
        elif next_eff == "cancel_search":
            search_interaction = replace(
                search_interaction,
                search_terminal_status="cancelled",
                search_can_resume_main_task=True,
            )
        # Local Task Space Grid M0：局部任务二维空间格（组织层；不反写主事实）
        task_grid_result = local_task_space_grid.build_local_task_space_grid(
            spatial_expression_sidecar=sidecar,
            object_search_interaction=search_interaction,
            object_temporal_ledger=obj_ledger,
        )
        # Grid M0.5：轻量消费（组合式增强，不替代原 zone/next_step）
        rec_human = getattr(task_grid_result, "recommended_search_cell_human_label", None)
        if rec_human:
            search_interaction = replace(
                search_interaction,
                suggested_search_zone=_append_grid_suffix(
                    getattr(search_interaction, "suggested_search_zone", None), rec_human
                ),
                next_search_step_summary=_append_grid_suffix(
                    getattr(search_interaction, "next_search_step_summary", None), rec_human
                ),
            )
            action_hint_result = replace(
                action_hint_result,
                action_hint_primary=_append_grid_suffix(
                    getattr(action_hint_result, "action_hint_primary", None), rec_human
                ),
            )
        # Grid-driven Search Expansion M0：基于 grid 产出最小扩搜建议（建议层）
        grid_expansion_result = grid_search_expansion.build_grid_search_expansion(
            local_task_space_grid=task_grid_result,
            object_search_interaction=search_interaction,
        )
        exp_hint = getattr(grid_expansion_result, "grid_search_expansion_hint", None)
        # 轻接入：next_search_step_summary 末尾追加扩搜建议；Action Hint followup 优先使用扩搜建议
        if exp_hint:
            search_interaction = replace(
                search_interaction,
                next_search_step_summary=_append_hint_suffix(
                    getattr(search_interaction, "next_search_step_summary", None), exp_hint
                ),
            )
            action_hint_result = replace(
                action_hint_result,
                action_hint_followup=_append_hint_suffix(
                    getattr(action_hint_result, "action_hint_followup", None), exp_hint
                ),
            )
        # Grid Search Whitebox Trace M0：为扩搜建议层提供白盒轨迹（不改变 expansion 结果）
        whitebox_result = grid_search_whitebox_trace.build_grid_search_whitebox_trace(
            local_task_space_grid=task_grid_result,
            grid_search_expansion=grid_expansion_result,
            object_search_interaction=search_interaction,
            action_hint_copy=action_hint_result,
            confirmation_input_bridge=confirmation_bridge_result,
        )
        # Recheck Whitebox Trace M0：补证链路白盒（仅解释 recheck_planner 结果，不改主逻辑）
        recheck_whitebox_result = recheck_whitebox_trace.build_recheck_whitebox_trace(
            recheck_planner=recheck_result,
            object_search_interaction=search_interaction,
            evidence_ledger=ledger,
            hypothesis_layer=hyp_layer,
            confirmation_input_bridge=confirmation_bridge_result,
            action_hint_copy=action_hint_result,
            local_task_space_grid=task_grid_result,
            state=state,
        )
        # Action Hint Whitebox Trace M0：引导话术白盒（仅解释 action_hint_copy 结果，不改主逻辑；含用户可见解释层）
        action_hint_whitebox_result = action_hint_whitebox_trace.build_action_hint_whitebox_trace(
            action_hint_copy=action_hint_result,
            object_search_interaction=search_interaction,
            spatial_expression_sidecar=sidecar,
            grid_search_expansion=grid_expansion_result,
            confirmation_input_bridge=confirmation_bridge_result,
            local_task_space_grid=task_grid_result,
            evidence_ledger=ledger,
            hypothesis_layer=hyp_layer,
        )
        # Confirmation Whitebox Trace M0：确认输入白盒（仅解释 confirmation_input_bridge 结果，不改主逻辑；含用户可见解释层）
        confirmation_whitebox_result = confirmation_whitebox_trace.build_confirmation_whitebox_trace(
            confirmation_input_bridge=confirmation_bridge_result,
            object_search_interaction=search_interaction,
            action_hint_copy=action_hint_result,
            grid_search_expansion=grid_expansion_result,
            recheck_planner=recheck_result,
        )
        # Evidence / Hypothesis Whitebox Trace M0：证据×假设白盒（仅解释 evidence_ledger/hypothesis_layer，不改主逻辑；含用户可见解释层）
        evidence_hypothesis_whitebox_result = evidence_hypothesis_whitebox_trace.build_evidence_hypothesis_whitebox_trace(
            evidence_ledger=ledger,
            hypothesis_layer=hyp_layer,
            confirmation_input_bridge=confirmation_bridge_result,
        )
        # 任务仲裁 M0：五维判断，仅产出仲裁结果不改 Task Chain
        arb_result = task_arbitration.build_task_arbitration(
            goal,
            state,
            mix,
            search_interaction,
            recheck_result,
            obj_ledger,
            incoming_task_type=ctx.get("incoming_task_type"),
            incoming_task_zone=ctx.get("incoming_task_zone"),
            incoming_task_risk=ctx.get("incoming_task_risk"),
            incoming_task_requires_user_attention=ctx.get("incoming_task_requires_user_attention"),
        )
        # 联合任务包 M0：仅当 arbitration_action == merge_into_bundle 时生成
        bundle_result = task_bundle.build_task_bundle(
            arb_result,
            state,
            mix,
            local_goal_spatial_map,
            search_interaction,
            recheck_result,
            obj_ledger,
            incoming_task_type=ctx.get("incoming_task_type"),
            incoming_task_zone=ctx.get("incoming_task_zone"),
            frame_seq=seq,
        )
        # 任务链桥接 M0：arbitration / bundle / search -> 任务链可读摘要
        bridge_result = task_chain_bridge.build_task_chain_bridge(
            arb_result,
            bundle_result,
            search_interaction,
            state,
            current_foreground_task_type=_get(arb_result, "foreground_task_type"),
        )
        # 经验演化 M0/M1：经验候选审计与治理；M1 需上一轮 snapshot 与 current_ts 做聚合
        _prev_snap = ctx.get("experience_evolution_prev_snapshot")
        try:
            import json as _json
            prev_snapshot = _json.loads(_prev_snap) if isinstance(_prev_snap, str) and _prev_snap.strip() else None
        except Exception:
            prev_snapshot = None
        evolution_result = experience_evolution.build_experience_evolution(
            ledger,
            hyp_layer,
            recheck_result,
            obj_ledger,
            search_interaction,
            state,
            object_user_confirmed_location=object_user_confirmed,
            object_user_denied_location=object_user_denied,
            prev_candidates_snapshot=prev_snapshot,
            current_ts=ctx.get("current_ts"),
        )
        # Experience Governance Whitebox Trace M0：经验治理白盒（仅解释 experience_evolution，不改主逻辑；含用户可见解释层）
        experience_governance_whitebox_result = experience_governance_whitebox_trace.build_experience_governance_whitebox_trace(
            experience_evolution=evolution_result,
            confirmation_input_bridge=confirmation_bridge_result,
        )
        # 主线接入 M0：汇总 6 模块摘要与轻量控制，不重构主流程
        mainline_result = mainline_integration.build_mainline_integration(
            bridge_result,
            arb_result,
            bundle_result,
            search_interaction,
            recheck_result,
            evolution_result,
            state,
        )
        trace_anchor_id = ctx.get("trace_anchor_id") or f"{self._trace_anchor_id_prefix}_{seq}"
        return DecisionMonitorFrame(
            goal=goal,
            inputs=inputs,
            state=state,
            decision=decision,
            outputs=outputs,
            consequence=consequence,
            local_goal_state=local_goal_state,
            local_goal_spatial_map=local_goal_spatial_map,
            local_goal_spatial_relations=relations_list,
            spatial_scale=spatial_scale,
            skeleton_mix=mix,
            skeleton_filter=filt,
            spatial_memory_pools=pools,
            spatial_forgetting=forgetting_summary,
            evidence_ledger=ledger,
            hypothesis_layer=hyp_layer,
            recheck_planner=recheck_result,
            object_temporal_ledger=obj_ledger,
            object_search_interaction=search_interaction,
            task_arbitration=arb_result,
            task_bundle=bundle_result,
            task_chain_bridge=bridge_result,
            experience_evolution=evolution_result,
            mainline_integration=mainline_result,
            visual_candidate_audit=audit_result,
            spatial_expression_sidecar=sidecar,
            action_hint_copy=action_hint_result,
            confirmation_input_bridge=confirmation_bridge_result,
            confirmation_whitebox_trace=confirmation_whitebox_result,
            evidence_hypothesis_whitebox_trace=evidence_hypothesis_whitebox_result,
            local_task_space_grid=task_grid_result,
            grid_search_expansion=grid_expansion_result,
            grid_search_whitebox_trace=whitebox_result,
            recheck_whitebox_trace=recheck_whitebox_result,
            action_hint_whitebox_trace=action_hint_whitebox_result,
            experience_governance_whitebox_trace=experience_governance_whitebox_result,
            monitor_version="1.0",
            trace_anchor_id=trace_anchor_id,
        )

    def _resolve_decision_owner(
        self,
        policy_should_sample: Optional[bool],
        floor_forced: bool,
        escape_hatch_triggered: bool,
        b2_impact_applied: bool,
    ) -> str:
        if escape_hatch_triggered or floor_forced:
            return "floor_guard"
        if policy_should_sample is False:
            return "sampling_gate"
        if b2_impact_applied:
            return "b2_impact"
        return "controller"

    def _resolve_decision_type(
        self,
        policy_should_sample: Optional[bool],
        floor_forced: bool,
        policy_run_detector: bool,
        policy_run_ocr: bool,
    ) -> str:
        if floor_forced:
            return "floor_forced"
        if policy_should_sample is False:
            return "skip"
        parts = []
        if policy_run_detector:
            parts.append("run_detector")
        if policy_run_ocr:
            parts.append("run_ocr")
        if parts:
            return "+".join(parts)
        return "sample"

    def _build_inputs(
        self,
        ctx: Dict[str, Any],
        seq: int,
        now: float,
        obs: Any,
        policy_intent: Any,
    ) -> InputsLayer:
        dt_ms = None
        if obs is not None:
            dt = getattr(obs, "dt", None)
            if dt is not None:
                dt_ms = dt * 1000.0
        produced_ts = getattr(obs, "ts", now) if obs is not None else now
        route = ctx.get("route")
        if route is None and obs is not None:
            path = getattr(obs, "path", None)
            route = str(path) if path is not None else None
        active_b2 = ctx.get("active_b2_impact")
        if active_b2 is None and policy_intent is not None:
            active_b2 = bool(_get(policy_intent, "b2_impact_applied", False))
        raw_summary = None
        if obs is not None:
            m = getattr(obs, "motion", None)
            p = getattr(obs, "path", None)
            b = getattr(obs, "branch", None)
            raw_summary = f"motion={m} path={p} branch={b}"
        return InputsLayer(
            frame_seq=seq,
            produced_ts=produced_ts,
            current_ts=now,
            delta_t_ms=dt_ms,
            sampled=_get(obs, "sampled") if obs is not None else ctx.get("sampled"),
            route=route,
            active_b2_impact=active_b2,
            raw_observation_summary=raw_summary,
            goal_relevant_observations=ctx.get("goal_relevant_observations"),
            sensor_notes=ctx.get("sensor_notes"),
        )

    def _build_state(self, ctx: Dict[str, Any], obs: Any, policy_intent: Any) -> StateLayer:
        decision = ctx.get("decision")
        safety_level = None
        risk_score = ctx.get("risk_score")
        if decision is not None:
            safety_level = getattr(decision, "safety_level", None) or getattr(decision, "mode", None)
            if safety_level is not None and hasattr(safety_level, "value"):
                safety_level = safety_level.value
            if safety_level is None:
                safety_level = str(decision) if decision else None
        if risk_score is None and decision is not None:
            risk_score = getattr(decision, "risk_score", None)
        motion = diff = None
        if obs is not None:
            motion = getattr(obs, "motion", None)
            diff = getattr(obs, "path", None)
        weak = ctx.get("weak_evidence_level")
        if weak is None and ctx.get("b2_impact_frame_telem") is not None:
            weak = getattr(ctx["b2_impact_frame_telem"], "b2_impact_weak_evidence_level", None)
        return StateLayer(
            c1_state=ctx.get("c1_state"),
            motion=motion,
            diff=diff,
            risk_score=risk_score,
            safety_level=safety_level,
            weak_evidence_level=weak,
            traversability_state=ctx.get("traversability_state"),
            local_risk_summary=ctx.get("local_risk_summary"),
            goal_progress_state=ctx.get("goal_progress_state") or "advancing",
            state_confidence=ctx.get("state_confidence"),
            state_notes=ctx.get("state_notes"),
            focus_region_hint=ctx.get("focus_region_hint"),
            view_behavior_hint=ctx.get("view_behavior_hint"),
            local_goal_action_applied=ctx.get("local_goal_action_applied"),
            local_goal_focus_applied=ctx.get("local_goal_focus_applied"),
            local_goal_recheck_applied=ctx.get("local_goal_recheck_applied"),
            local_goal_recheck_mode=ctx.get("local_goal_recheck_mode"),
            local_goal_recheck_type=ctx.get("local_goal_recheck_type"),
            local_goal_recheck_executed=ctx.get("local_goal_recheck_executed"),
            local_goal_view_priority=ctx.get("local_goal_view_priority"),
            local_goal_view_priority_applied=ctx.get("local_goal_view_priority_applied"),
        )

    def _enrich_state_continuity(
        self,
        state: StateLayer,
        continuous: Dict[str, str],
    ) -> StateLayer:
        """主线 1.3：将 state_tracker 产出的 4 个连续字段写入 state。"""
        return replace(
            state,
            prev_state_summary=continuous.get("prev_state_summary"),
            state_delta_summary=continuous.get("state_delta_summary"),
            state_trend=continuous.get("state_trend"),
            goal_progress_delta=continuous.get("goal_progress_delta"),
        )

    def _enrich_state_view_guard(
        self,
        state: StateLayer,
        vg: Dict[str, Any],
    ) -> StateLayer:
        """主线 1.3A：将 view_guard 产出的 10 个字段写入 state。"""
        return replace(
            state,
            view_alignment_state=vg.get("view_alignment_state"),
            view_alignment_score=vg.get("view_alignment_score"),
            view_misaligned=vg.get("view_misaligned"),
            view_correction_needed=vg.get("view_correction_needed"),
            view_correction_hint=vg.get("view_correction_hint"),
            vision_quality_state=vg.get("vision_quality_state"),
            vision_reliability_score=vg.get("vision_reliability_score"),
            vision_degraded=vg.get("vision_degraded"),
            vision_degrade_reason=vg.get("vision_degrade_reason"),
            vision_recovery_eta_ms=vg.get("vision_recovery_eta_ms"),
        )

    def _enrich_state_predictive_hold(
        self,
        state: StateLayer,
        ph: Dict[str, Any],
    ) -> StateLayer:
        """主线 1.3B：将 predictive_hold 产出的 7 个字段写入 state。"""
        return replace(
            state,
            predictive_hold_allowed=ph.get("predictive_hold_allowed"),
            predictive_hold_active=ph.get("predictive_hold_active"),
            predictive_hold_remaining_ms=ph.get("predictive_hold_remaining_ms"),
            predictive_hold_reason=ph.get("predictive_hold_reason"),
            predictive_hold_confidence=ph.get("predictive_hold_confidence"),
            predictive_hold_expired=ph.get("predictive_hold_expired"),
            predictive_recovery_action=ph.get("predictive_recovery_action"),
        )

    def _enrich_state_runtime_domain_guard(
        self,
        state: StateLayer,
        rdg: Dict[str, Any],
    ) -> StateLayer:
        """主线 1.3C：将 runtime_domain_guard 产出的 8 个字段写入 state。"""
        return replace(
            state,
            runtime_domain_state=rdg.get("runtime_domain_state"),
            runtime_domain_confidence=rdg.get("runtime_domain_confidence"),
            domain_mismatch_detected=rdg.get("domain_mismatch_detected"),
            domain_mismatch_reason=rdg.get("domain_mismatch_reason"),
            cognitive_degrade_level=rdg.get("cognitive_degrade_level"),
            cognitive_output_allowed=rdg.get("cognitive_output_allowed"),
            degrade_action=rdg.get("degrade_action"),
            recovery_condition=rdg.get("recovery_condition"),
        )

    def _enrich_state_scene_gate(
        self,
        state: StateLayer,
        sg: Dict[str, Any],
    ) -> StateLayer:
        """Scene Gate v1：将 scene_gate 产出的 5 个字段写入 state。"""
        return replace(
            state,
            scene_type=sg.get("scene_type"),
            scene_supported=sg.get("scene_supported"),
            scene_gate_state=sg.get("scene_gate_state"),
            scene_gate_reason=sg.get("scene_gate_reason"),
            scene_gate_action=sg.get("scene_gate_action"),
        )

    def _apply_scene_gate_control(
        self,
        state: StateLayer,
        goal: GoalLayer,
    ) -> tuple[StateLayer, GoalLayer]:
        """
        Scene Gate 轻量控制：根据 scene_gate_action 设置 4 个控制字段；
        pause_goal_progress / freeze_to_minimum_mode 时将 goal_status 置为 paused。
        """
        action = getattr(state, "scene_gate_action", None)
        goal_progress_paused = False
        minimum_mode_active = False
        high_level_output_suppressed = False
        scene_gate_control_applied = action is not None

        if action == "continue_normal":
            pass
        elif action == "pause_goal_progress":
            goal_progress_paused = True
        elif action == "freeze_to_minimum_mode":
            goal_progress_paused = True
            minimum_mode_active = True
            high_level_output_suppressed = True
        elif action == "continue_cautious":
            pass
        elif action == "ignore_high_level_input":
            high_level_output_suppressed = True

        state = replace(
            state,
            goal_progress_paused=goal_progress_paused,
            minimum_mode_active=minimum_mode_active,
            high_level_output_suppressed=high_level_output_suppressed,
            scene_gate_control_applied=scene_gate_control_applied,
        )
        if action in ("pause_goal_progress", "freeze_to_minimum_mode"):
            goal = replace(goal, goal_status="paused")
        return state, goal

    def _apply_interaction_calibrator(
        self,
        state: StateLayer,
        goal: GoalLayer,
        cal: Dict[str, Any],
        ctx: Dict[str, Any],
    ) -> tuple[StateLayer, GoalLayer]:
        """
        人工沟通校准：若 human_check_needed 且尚未收到回复，暂缓高代价动作（不置 pause/freeze）；
        若已有 human_check_response，按回复或 default_action 落盘。
        """
        needed = cal.get("human_check_needed") is True
        response = ctx.get("human_check_response")
        resolved = ctx.get("human_check_resolved") is True
        default_action = cal.get("human_check_default_action")

        # 写入校准器输出到 state（供 Viewer 与主循环使用）
        state = replace(
            state,
            human_check_needed=needed,
            human_check_reason=cal.get("human_check_reason"),
            human_check_question=cal.get("human_check_question"),
            human_check_blocking_level=cal.get("human_check_blocking_level"),
            human_check_timeout_ms=cal.get("human_check_timeout_ms"),
            human_check_default_action=default_action,
            human_check_response=response,
            human_check_resolved=resolved or (response is not None),
            human_check_pending=needed and response is None and not resolved,
            human_check_timeout_triggered=ctx.get("human_check_timeout_triggered"),
        )
        # 有回复或已解析时一律按回复/默认落盘（含超时触发的 default_action）
        if response is not None or resolved:
            # 按回复或默认动作落盘（含超时触发的 default_action）
            timeout_triggered = ctx.get("human_check_timeout_triggered") is True
            action_to_apply = self._resolve_calibrator_action(response, default_action)
            if action_to_apply == "continue_normal":
                state = replace(
                    state,
                    goal_progress_paused=False,
                    minimum_mode_active=False,
                    high_level_output_suppressed=False,
                    human_check_timeout_triggered=timeout_triggered,
                )
                goal = replace(goal, goal_status="active")
            elif action_to_apply == "pause_goal_progress":
                state = replace(
                    state,
                    goal_progress_paused=True,
                    minimum_mode_active=False,
                    high_level_output_suppressed=False,
                    human_check_timeout_triggered=timeout_triggered,
                )
                goal = replace(goal, goal_status="paused")
            elif action_to_apply == "freeze_to_minimum_mode":
                state = replace(
                    state,
                    goal_progress_paused=True,
                    minimum_mode_active=True,
                    high_level_output_suppressed=True,
                    human_check_timeout_triggered=timeout_triggered,
                )
                goal = replace(goal, goal_status="paused")
            elif action_to_apply == "continue_cautious":
                state = replace(
                    state,
                    goal_progress_paused=False,
                    minimum_mode_active=False,
                    high_level_output_suppressed=False,
                    human_check_timeout_triggered=timeout_triggered,
                )
                goal = replace(goal, goal_status="active")
            return state, goal

        if not needed:
            return state, goal

        # 需要确认且未收到回复：暂缓高代价动作
        state = replace(
            state,
            goal_progress_paused=False,
            minimum_mode_active=False,
            high_level_output_suppressed=False,
            human_check_pending=True,
        )
        goal = replace(goal, goal_status="active")
        return state, goal

    @staticmethod
    def _resolve_calibrator_action(
        response: Optional[str],
        default_action: Optional[str],
    ) -> str:
        """将 human_check_response 或超时默认映射为 scene_gate_action。"""
        if not response:
            return default_action or "continue_normal"
        r = (response or "").strip().lower()
        if r in ("continue", "继续", "adjusted", "已调整"):
            return "continue_normal"
        if r in ("pause", "暂停", "not_adjusted", "暂不调整"):
            return "pause_goal_progress"
        if r in ("freeze", "冻结"):
            return "freeze_to_minimum_mode"
        return default_action or "continue_normal"

    def _build_decision(
        self,
        ctx: Dict[str, Any],
        seq: int,
        decision_owner: str,
        decision_type: str,
        policy_intent: Any,
        policy_should_sample: Optional[bool],
        escape_hatch_triggered: bool,
        floor_forced: bool,
    ) -> DecisionLayer:
        mode_before = _get(policy_intent, "policy_mode_before_b2") or _get(policy_intent, "mode")
        if mode_before is not None and hasattr(mode_before, "value"):
            mode_before = mode_before.value
        mode_after = _get(policy_intent, "policy_mode_after_b2") or _get(policy_intent, "mode")
        if mode_after is not None and hasattr(mode_after, "value"):
            mode_after = mode_after.value
        reason_parts = []
        if decision_owner == "floor_guard":
            reason_parts.append("escape_hatch")
        elif decision_owner == "sampling_gate":
            reason_parts.append("policy_skip")
        else:
            reason_parts.append(f"mode={mode_after or 'N/A'}")
        if _get(policy_intent, "b2_impact_applied"):
            reason_parts.append("b2_applied")
        return DecisionLayer(
            decision_id=f"dec_{seq}_{decision_owner}",
            for_goal_id=ctx.get("goal_id") or "default",
            decision_owner=decision_owner,
            decision_type=decision_type,
            decision_reason="; ".join(reason_parts),
            policy_mode_before=mode_before,
            policy_mode_after=mode_after,
            b2_impact_applied=bool(_get(policy_intent, "b2_impact_applied", False)),
            escape_hatch_triggered=escape_hatch_triggered,
            floor_forced=floor_forced,
            decision_confidence=ctx.get("decision_confidence"),
        )

    def _build_outputs(
        self,
        ctx: Dict[str, Any],
        policy_intent: Any,
        policy_run_detector: bool,
        policy_run_ocr: bool,
    ) -> OutputsLayer:
        mode = _get(policy_intent, "mode")
        if mode is not None and hasattr(mode, "value"):
            mode = mode.value
        policy_intent_summary = str(mode) if mode else None
        fps = _get(policy_intent, "sampling_target_fps")
        det_s = _get(policy_intent, "heavy_infer_stride")
        ocr_s = _get(policy_intent, "ocr_stride")
        modules_run = []
        modules_skipped = []
        if policy_run_detector:
            modules_run.append("detector")
        else:
            modules_skipped.append("detector")
        if policy_run_ocr:
            modules_run.append("ocr")
        else:
            modules_skipped.append("ocr")
        action = "sample_and_run" if (policy_run_detector or policy_run_ocr) else "skip"
        return OutputsLayer(
            policy_intent_summary=policy_intent_summary,
            sampling_target_fps=fps,
            detector_stride=det_s,
            ocr_stride=ocr_s,
            modules_run=modules_run if modules_run else None,
            modules_skipped=modules_skipped if modules_skipped else None,
            action_summary=action,
            user_facing_output=ctx.get("user_facing_output"),
            output_notes=ctx.get("output_notes"),
        )

