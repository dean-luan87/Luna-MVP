# -*- coding: utf-8 -*-
"""
VoiceInputEvent → BridgeDecision + proposal/query/response 占位（输入接线 v1）。

约束：Voice 不拥有裁决权；仅提交候选与可追踪 reject。
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from capabilities.voice.bridge.bridge_decision import BridgeDecision
from capabilities.voice.bridge.route_types import BridgeRouteType
from capabilities.voice.bridge.voice_input_bridge_adapter import adapt_voice_input_for_bridge
from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutRegistry
from capabilities.voice.schemas.confirmation_response import ConfirmationResponse
from capabilities.voice.schemas.device_action_proposal import DeviceActionProposal
from capabilities.voice.schemas.task_action_proposal import TaskActionProposal
from capabilities.voice.schemas.task_context_query import TaskContextQuery
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_input_rejection_result import VoiceInputRejectionResult


# shortcut_id → 设备动作名（占位，供 Core 映射）
_DEVICE_ACTION: Dict[str, str] = {
    "dev_pause": "pause",
    "dev_stop": "stop",
    "dev_resume": "resume",
    "dev_cancel": "cancel",
    "dev_shutdown": "shutdown",
    "dev_vol_up": "volume_up",
    "dev_vol_down": "volume_down",
    "dev_tts_speed_down": "tts_speed_down",
    "dev_tts_speed_up": "tts_speed_up",
    "dev_tts_speed_set_0_25": "tts_speed_set",
    "dev_tts_speed_set_0_5": "tts_speed_set",
    "dev_tts_speed_set_0_75": "tts_speed_set",
    "dev_tts_speed_set_1_0": "tts_speed_set",
}

# shortcut_id → 任务生命周期动作名
_TASK_ACTION: Dict[str, str] = {
    "task_start_nav": "start_navigation",
    "task_end": "end_task",
    "task_switch": "switch_task",
    "task_pause": "pause_task",
    "task_resume": "resume_task",
}

# shortcut_id → 任务上下文查询类型
_TASK_QUERY_TYPE: Dict[str, str] = {
    "q_where": "where_am_i",
    "q_nearby": "nearby_poi",
    "q_status": "status",
    "q_ahead": "ahead",
    "q_distance": "distance_remaining",
}


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def voice_input_to_bridge_decision(
    event: VoiceInputEvent,
    *,
    registry: Optional[VoiceShortcutRegistry] = None,
    pending_confirmation_id: Optional[str] = None,
    default_confidence: float = 1.0,
) -> BridgeDecision:
    """
    将 VoiceInputEvent 转为 BridgeDecision（含 proposal / query / response candidate 或 reject）。

    pending_confirmation_id：当存在系统待确认项时，用于装配 ConfirmationResponse（证据语义）。
    """
    reg = registry or VoiceShortcutRegistry()
    adapted = adapt_voice_input_for_bridge(event, registry=reg)

    if event.router_decision == "reject":
        rej = VoiceInputRejectionResult(
            request_id=event.request_id or event.event_id,
            reason=str((event.metadata or {}).get("reject_reason") or "rejected"),
            router_stage="voice_input",
            raw_text=event.raw_text,
            normalized_text=event.normalized_text,
            is_task_mode=event.is_task_mode,
            source_type=event.source_type,
            reason_code=str((event.metadata or {}).get("reason_code") or ""),
        )
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=event.event_id,
            route=BridgeRouteType.INPUT_REJECTED,
            execution_class="reject_or_degrade",
            reason="input_rejected_by_voice_router",
            proposal=rej,
            metadata={"voice_input_event": event.to_dict()},
        )

    ev = adapted.event
    sc = adapted.shortcut_entry
    stripped = (ev.wake_word_stripped or ev.normalized_text or "").strip()
    conf = float(ev.asr_confidence if ev.asr_confidence is not None else default_confidence)

    # 规则 1：仅唤醒词，无正文、无白名单 → 会话激活，不生成任务提案
    if ev.wake_word_detected and not stripped and sc is None:
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.SESSION_WAKE,
            execution_class="direct",
            reason="wake_word_only_session_activation",
            proposal=None,
            metadata={"session_id": ev.session_id, "context_resume_hint": ev.context_resume_hint or ""},
        )

    # 无 shortcut：窗口内自由文本等 → 未受控扩展，不冒充任务/设备命令
    if sc is None:
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.RESERVED_OPEN_DIALOGUE,
            execution_class="reject_or_degrade",
            reason="unscoped_window_text_not_whitelisted_v1",
            proposal=None,
            metadata={
                "route_reason_code": adapted.route_reason_code,
                "normalized_text": stripped,
                "session_id": ev.session_id,
                "hint": "v1 wire only maps whitelisted shortcuts; no open intent",
            },
        )

    sid = sc.shortcut_id

    # 确认 / 反馈证据（规则 4）
    if sc.shortcut_type == "confirmation_feedback":
        resp = "yes" if sid == "cf_yes" else "no"
        pc = pending_confirmation_id or ""
        cr = ConfirmationResponse(
            response_id=_new_id("cr"),
            source_event_id=ev.event_id,
            pending_confirmation_id=pc,
            response=resp,
            confidence=conf,
            notes=stripped,
            metadata={"shortcut_id": sid, "evidence_only": True},
        )
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.CONFIRMATION,
            execution_class="direct",
            reason="confirmation_feedback_evidence",
            proposal=cr,
            metadata={"pending_confirmation_id_set": bool(pending_confirmation_id)},
        )

    # 会话结束 → 反馈域（非任务命令）
    if sc.shortcut_type == "session_control":
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.FEEDBACK_RESPONSE,
            execution_class="direct",
            reason="session_end_feedback",
            proposal=None,
            metadata={"shortcut_id": sid, "feedback_kind": "session_end", "text": stripped},
        )

    # 设备控制
    if sc.shortcut_type == "device_control":
        action = _DEVICE_ACTION.get(sid, sid)
        needs_conf = bool(sc.requires_confirmation)
        exec_class = "confirm_then_execute" if needs_conf else "direct"
        md = {"shortcut_id": sid, "mapped_route_type": sc.mapped_route_type}
        # speed set value encoded in shortcut_id
        if sid.startswith("dev_tts_speed_set_"):
            v = sid.replace("dev_tts_speed_set_", "")
            md["tts_speed_target"] = v
        prop = DeviceActionProposal(
            proposal_id=_new_id("dap"),
            source_event_id=ev.event_id,
            device_action=action,
            confidence=conf,
            needs_confirmation=needs_conf,
            rationale=f"voice_shortcut:{sid}",
            metadata=md,
        )
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.DEVICE_CONTROL,
            execution_class=exec_class,
            reason="device_action_proposal",
            proposal=prop,
        )

    # 任务问询
    if sc.shortcut_type == "task_query":
        qtype = _TASK_QUERY_TYPE.get(sid, "generic")
        tq = TaskContextQuery(
            query_id=_new_id("tcq"),
            source_event_id=ev.event_id,
            query_type=qtype,
            query_text=stripped,
            metadata={"shortcut_id": sid, "mapped_route_type": sc.mapped_route_type},
        )
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.TASK_CONTEXT_ENHANCEMENT,
            execution_class="direct",
            reason="task_context_query",
            proposal=tq,
        )

    # 任务控制
    if sc.shortcut_type == "task_control":
        action = _TASK_ACTION.get(sid, sid)
        # 「开始导航」等启动类：候选直送；结束/切换/暂停/继续任务：降级确认
        if sid == "task_start_nav":
            needs_conf = False
            exec_class = "direct"
        else:
            needs_conf = True
            exec_class = "confirm_then_execute"
        prop = TaskActionProposal(
            proposal_id=_new_id("tap"),
            source_event_id=ev.event_id,
            task_action=action,
            confidence=conf,
            needs_confirmation=needs_conf,
            may_change_task_state=True,
            rationale=f"voice_shortcut:{sid}",
            metadata={"shortcut_id": sid, "mapped_route_type": sc.mapped_route_type},
        )
        return BridgeDecision(
            decision_id=_new_id("bd"),
            source_event_id=ev.event_id,
            route=BridgeRouteType.TASK_LIFECYCLE,
            execution_class=exec_class,
            reason="task_action_proposal",
            proposal=prop,
        )

    # 兜底
    return BridgeDecision(
        decision_id=_new_id("bd"),
        source_event_id=ev.event_id,
        route=BridgeRouteType.RESERVED_OPEN_DIALOGUE,
        execution_class="reject_or_degrade",
        reason="unmapped_shortcut_type",
        proposal=None,
        metadata={"shortcut_id": sid, "shortcut_type": sc.shortcut_type},
    )


def bridge_decision_to_trace_dict(decision: BridgeDecision) -> Dict[str, Any]:
    """供白盒/测试序列化。"""
    prop = decision.proposal
    prop_summary: Any
    if prop is None:
        prop_summary = None
    elif hasattr(prop, "__dataclass_fields__"):
        prop_summary = type(prop).__name__
    else:
        prop_summary = str(type(prop))
    return {
        "decision_id": decision.decision_id,
        "source_event_id": decision.source_event_id,
        "route": decision.route.value,
        "execution_class": decision.execution_class,
        "reason": decision.reason,
        "proposal_type": prop_summary,
        "metadata": dict(decision.metadata),
    }
