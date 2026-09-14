# -*- coding: utf-8 -*-
"""语音输入接线 v1：VoiceInputEvent → BridgeDecision → Core 占位。"""

from __future__ import annotations

from capabilities.voice.bridge.route_types import BridgeRouteType
from capabilities.voice.bridge.voice_input_core_placeholder import dispatch_voice_bridge_to_core_placeholder
from capabilities.voice.bridge.voice_input_to_bridge import voice_input_to_bridge_decision
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
from capabilities.voice.schemas.confirmation_response import ConfirmationResponse
from capabilities.voice.schemas.device_action_proposal import DeviceActionProposal
from capabilities.voice.schemas.task_action_proposal import TaskActionProposal
from capabilities.voice.schemas.task_context_query import TaskContextQuery
from capabilities.voice.schemas.voice_input_rejection_result import VoiceInputRejectionResult


def test_scenario1_wake_then_task_query() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达，开始导航去医院", now=0.0, is_task_mode=False, session_id="s1")
    ev2 = sm.process_final_text("现在到哪了", now=10.0, is_task_mode=True, session_id="s1")
    d = voice_input_to_bridge_decision(ev2)
    assert d.route == BridgeRouteType.TASK_CONTEXT_ENHANCEMENT
    assert isinstance(d.proposal, TaskContextQuery)
    assert getattr(d.proposal, "query_type") == "where_am_i"


def test_scenario2_task_pause_task_action_proposal() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("暂停任务", now=0.0, is_task_mode=True, session_id="s1")
    d = voice_input_to_bridge_decision(ev)
    assert d.route == BridgeRouteType.TASK_LIFECYCLE
    assert isinstance(d.proposal, TaskActionProposal)
    assert d.proposal.task_action == "pause_task"
    assert d.execution_class == "confirm_then_execute"


def test_scenario3_volume_device_proposal() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("音量大一点", now=0.0, is_task_mode=True, session_id="s1")
    d = voice_input_to_bridge_decision(ev)
    assert d.route == BridgeRouteType.DEVICE_CONTROL
    assert isinstance(d.proposal, DeviceActionProposal)
    assert d.proposal.device_action == "volume_up"
    assert d.execution_class == "direct"


def test_scenario4_shutdown_confirmation_degrade() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("关机", now=0.0, is_task_mode=True, session_id="s1")
    d = voice_input_to_bridge_decision(ev)
    assert d.route == BridgeRouteType.DEVICE_CONTROL
    assert isinstance(d.proposal, DeviceActionProposal)
    assert d.proposal.needs_confirmation is True
    assert d.execution_class == "confirm_then_execute"


def test_scenario5_confirmation_yes() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("是", now=0.0, is_task_mode=False, session_id="s1")
    d = voice_input_to_bridge_decision(ev, pending_confirmation_id="pc-001")
    assert d.route == BridgeRouteType.CONFIRMATION
    assert isinstance(d.proposal, ConfirmationResponse)
    assert d.proposal.response == "yes"
    assert d.proposal.pending_confirmation_id == "pc-001"


def test_scenario6_reject_traceable() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("这是一段不在白名单里的很长的话", now=0.0, is_task_mode=False, session_id="s1")
    d = voice_input_to_bridge_decision(ev)
    assert d.route == BridgeRouteType.INPUT_REJECTED
    assert isinstance(d.proposal, VoiceInputRejectionResult)
    assert d.proposal.reason_code == "no_wake_no_window"
    trace = dispatch_voice_bridge_to_core_placeholder(d)
    assert trace["received"] is True
    assert trace["trace"]["route"] == BridgeRouteType.INPUT_REJECTED.value


def test_wake_only_session_wake() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    d = voice_input_to_bridge_decision(ev)
    assert d.route == BridgeRouteType.SESSION_WAKE
    assert d.proposal is None
