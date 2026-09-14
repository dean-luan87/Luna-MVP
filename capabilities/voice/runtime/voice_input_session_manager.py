# -*- coding: utf-8 -*-
"""
输入会话协调器：串联 ASR（可选）、唤醒窗口、白名单、路由器 → VoiceInputEvent。

本模块不调用主链；仅组装标准输入对象。切段（3s）由上游在静默满足后调用 process_final_text。
"""

from __future__ import annotations

import uuid
from typing import Optional

from capabilities.voice.bridge.voice_input_router import VoiceInputRouteDecision, route_voice_text
from capabilities.voice.runtime.voice_final_text_dispatch_result import VoiceFinalTextDispatchResult
from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
from capabilities.voice.runtime.vision_semantic_bridge_v3 import build_vision_semantic_input_pack_v0
from capabilities.voice.runtime.semantic_converter_v2 import get_default_semantic_converter_v2, semantic_v2_stub_enabled
from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutRegistry
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor
from capabilities.voice.runtime.voice_time_governance_v1 import VoiceTimeGovernanceRuntime
from capabilities.voice.runtime.voice_wake_window_manager import VoiceWakeWindowManager
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


class VoiceInputSessionManager:
    """
    - process_final_text：在「当前句已结束」（例如静默≥3s）后调用，传入本句文本。
    - 最小短期承接：context_resume_hint 保留上一轮 strip 后摘要。
    - v1_session_anchor：最小会话事实锚（非状态机）；不用于发明缺失信息（见 voice_v1_session_state_anchor）。
    """

    def __init__(
        self,
        *,
        registry: Optional[VoiceShortcutRegistry] = None,
        window: Optional[VoiceWakeWindowManager] = None,
        governance: Optional[VoiceTimeGovernanceRuntime] = None,
    ) -> None:
        self.registry = registry or VoiceShortcutRegistry()
        if governance is not None:
            self.governance = governance
        elif window is not None:
            self.governance = VoiceTimeGovernanceRuntime(window=window)
        else:
            self.governance = VoiceTimeGovernanceRuntime()
        self._last_accepted_normalized: str = ""
        self.v1_session_anchor: VoiceV1SessionStateAnchor = VoiceV1SessionStateAnchor()

    @property
    def window(self) -> VoiceWakeWindowManager:
        return self.governance.window

    def on_capture_started(self, now: float) -> None:
        """ASR 开始接收本段输入时调用（capturing_input + 挂起 30s 会话时钟）。"""
        self.governance.on_capture_started(now)

    def process_final_text(
        self,
        raw_text: str,
        *,
        now: float,
        is_task_mode: bool,
        session_id: str,
        source_type: str = "asr",
        asr_confidence: Optional[float] = None,
        provider_name: str = "",
        model_name: str = "",
        is_forced_cutoff: bool = False,
        cutoff_reason: str = "",
    ) -> VoiceInputEvent:
        """对「一句已结束」的文本做路由并更新窗口/承接 hint。"""
        self.governance.on_before_process_final_text(now)
        try:
            window_active = self.governance.is_window_active_for_routing(now)
            rd = route_voice_text(
                raw_text,
                now=now,
                window_active=window_active,
                is_task_mode=is_task_mode,
                registry=self.registry,
            )

            eid = str(uuid.uuid4())
            norm = (raw_text or "").strip()

            if rd.decision == "reject":
                return VoiceInputEvent(
                    event_id=eid,
                    request_id=eid,
                    timestamp=now,
                    session_id=session_id,
                    turn_id=eid,
                    source="voice_input_pipeline",
                    text=raw_text,
                    raw_text=raw_text,
                    normalized_text=norm,
                    asr_confidence=asr_confidence,
                    provider_name=provider_name,
                    model_name=model_name,
                    source_type=source_type,
                    is_task_mode=is_task_mode,
                    active_window=window_active,
                    router_decision="reject",
                    is_forced_cutoff=is_forced_cutoff,
                    cutoff_reason=cutoff_reason,
                    continuation_allowed=False,
                    voice_runtime_phase=self.governance.phase.value,
                    metadata={
                        "reject_reason": rd.reject_reason,
                        "reason_code": rd.reason_code,
                        "session_window_suspended": self.governance.session_window_suspended,
                    },
                )

            return self._build_accept(
                raw_text=raw_text,
                now=now,
                session_id=session_id,
                eid=eid,
                rd=rd,
                is_task_mode=is_task_mode,
                window_active_before=window_active,
                source_type=source_type,
                asr_confidence=asr_confidence,
                provider_name=provider_name,
                model_name=model_name,
                is_forced_cutoff=is_forced_cutoff,
                cutoff_reason=cutoff_reason,
            )
        finally:
            self.governance.on_after_process_final_text(now)

    def process_final_text_with_dispatch(
        self,
        raw_text: str,
        *,
        now: float,
        is_task_mode: bool,
        session_id: str,
        pending_confirmation_context: bool = False,
        pending_confirmation_id: Optional[str] = None,
        runtime_context: Optional[VoiceRuntimeContext] = None,
        source_type: str = "asr",
        asr_confidence: Optional[float] = None,
        provider_name: str = "",
        model_name: str = "",
        is_forced_cutoff: bool = False,
        cutoff_reason: str = "",
    ) -> VoiceFinalTextDispatchResult:
        """
        切段完成后：先组装 VoiceInputEvent，再经 voice_final_text_dispatcher 统一分流。

        短链 → BridgeDecision；长链 → task_plan_v1；reject → 结构化拒绝。不接执行层。
        """
        ev = self.process_final_text(
            raw_text,
            now=now,
            is_task_mode=is_task_mode,
            session_id=session_id,
            source_type=source_type,
            asr_confidence=asr_confidence,
            provider_name=provider_name,
            model_name=model_name,
            is_forced_cutoff=is_forced_cutoff,
            cutoff_reason=cutoff_reason,
        )
        self.v1_session_anchor.begin_from_event(ev)
        # V3 (vision→semantic bridge) stub: read-only pack from runtime_context.metadata.
        # Must not fabricate facts; must not generate time/space anchors; must not pass raw detector/OCR through.
        try:
            pack = build_vision_semantic_input_pack_v0(runtime_context)
            if pack is not None:
                ev.metadata["luna_voice_vision_semantic_v3_input"] = pack
        except Exception:
            # V3 stub must never block V1/V2 mainline.
            pass
        if semantic_v2_stub_enabled():
            try:
                payload = get_default_semantic_converter_v2().convert(
                    ev,
                    session_state_anchor=self.v1_session_anchor,
                    runtime_context=runtime_context,
                )
                if payload is not None:
                    ev.metadata["luna_voice_semantic_v2"] = payload
            except Exception:
                # V2 stub must never block V1 mainline.
                pass
        out = dispatch_voice_final_text(
            ev,
            pending_confirmation_context=pending_confirmation_context,
            pending_confirmation_id=pending_confirmation_id,
            registry=self.registry,
            runtime_context=runtime_context,
            session_state_anchor=self.v1_session_anchor,
        )
        self.v1_session_anchor.apply_no_submit_conservative()
        return out

    def _build_accept(
        self,
        *,
        raw_text: str,
        now: float,
        session_id: str,
        eid: str,
        rd: VoiceInputRouteDecision,
        is_task_mode: bool,
        window_active_before: bool,
        source_type: str,
        asr_confidence: Optional[float],
        provider_name: str,
        model_name: str,
        is_forced_cutoff: bool = False,
        cutoff_reason: str = "",
    ) -> VoiceInputEvent:
        wake_detected = rd.wake_word_detected
        stripped = rd.wake_word_stripped if wake_detected else (raw_text or "").strip()

        # 会话结束白名单：清窗口
        if rd.shortcut is not None and rd.shortcut.shortcut_id == "session_end":
            self.governance.on_session_end_clear()
            win_after = False
        else:
            if wake_detected:
                self.governance.on_wake_route_accept(now)
            elif rd.decision == "accept":
                self.governance.on_valid_input_route_accept(now)
            win_after = self.governance.is_window_active_for_routing(now)

        hint = self._make_resume_hint(stripped, is_task_mode)
        self._last_accepted_normalized = stripped

        sc = rd.shortcut
        continuation = bool(is_forced_cutoff and cutoff_reason == "max_capture_duration")
        return VoiceInputEvent(
            event_id=eid,
            request_id=eid,
            timestamp=now,
            session_id=session_id,
            turn_id=eid,
            source="voice_input_pipeline",
            text=raw_text,
            raw_text=raw_text,
            normalized_text=stripped,
            asr_confidence=asr_confidence,
            provider_name=provider_name,
            model_name=model_name,
            source_type=source_type,
            is_task_mode=is_task_mode,
            active_window=win_after,
            task_shortcut=sc is not None,
            wake_word_detected=wake_detected,
            wake_word_stripped=stripped,
            wake_word="艾达" if wake_detected else "",
            shortcut_id=sc.shortcut_id if sc else None,
            router_decision="accept",
            requires_confirmation_candidate=bool(sc and sc.requires_confirmation),
            context_resume_hint=hint,
            is_forced_cutoff=is_forced_cutoff,
            cutoff_reason=cutoff_reason,
            continuation_allowed=continuation,
            voice_runtime_phase=self.governance.phase.value,
            metadata={
                "route_reason_code": rd.reason_code,
                "mapped_route_type": sc.mapped_route_type if sc else "",
                "window_active_before": window_active_before,
                "session_window_suspended": self.governance.session_window_suspended,
            },
        )

    def _make_resume_hint(self, stripped: str, is_task_mode: bool) -> str:
        prev = self._last_accepted_normalized
        if not stripped and not prev:
            return ""
        if not prev:
            return f"task_mode={is_task_mode}; last={stripped[:80]}"
        return f"prev={prev[:60]}; now={stripped[:80]}"

    def on_shutdown_or_standby(self) -> None:
        self.governance.on_shutdown()
        self._last_accepted_normalized = ""
