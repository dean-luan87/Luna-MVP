# -*- coding: utf-8 -*-
"""
V1 最小会话状态锚（规则版，非状态机）。

只记录可观测事实，用于稳住最小语音闭环；不发明缺失信息。
No Fabrication Rule 高于状态层便利（见 VoiceInputSessionManager / guard_v1_speakable_text）。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from capabilities.voice.schemas.voice_input_event import VoiceInputEvent

# conversation_status 允许值（字符串，V1 保持简单）
V1_CONV_IDLE = "idle"
V1_CONV_LISTENING = "listening"
V1_CONV_THINKING = "thinking"
V1_CONV_SPEAKING = "speaking"
V1_CONV_WAITING_USER = "waiting_user"
V1_CONV_INTERRUPTED = "interrupted"
V1_CONV_TIMEOUT_CLOSED = "timeout_closed"


@dataclass
class VoiceV1SessionStateAnchor:
    """
    单会话、单实例锚点（本轮不支持 Dict[session_id] 并发）。

    字段为事实快照；不因「同会话延续」推断用户未说出内容。
    """

    session_id: str = ""
    turn_id: str = ""
    conversation_status: str = V1_CONV_IDLE
    current_mode: str = "normal"  # "normal" | "task"
    last_user_text: str = ""
    last_system_text: str = ""
    waiting_for_user: bool = False
    interrupted: bool = False
    last_output_request_id: str = ""
    _did_submit_this_call: bool = field(default=False, repr=False)

    def begin_from_event(self, ev: VoiceInputEvent) -> None:
        """本句进入 dispatch 前：写入输入侧事实，准备本轮 submit 标记。"""
        self._did_submit_this_call = False
        self.session_id = str(ev.session_id or "")
        self.turn_id = str(ev.turn_id or ev.request_id or ev.event_id or "")
        self.current_mode = "task" if ev.is_task_mode else "normal"
        raw_u = (ev.wake_word_stripped or ev.normalized_text or ev.effective_raw_text() or "").strip()
        self.last_user_text = raw_u[:500]
        self.interrupted = bool(ev.interrupt_requested)
        self.conversation_status = V1_CONV_THINKING

    def record_successful_output(self, *, spoken_text: str, request_id: str) -> None:
        """VoiceOutputPlane.submit 成功返回后：记录系统侧已提交播报文本（事实）。"""
        self.last_system_text = (spoken_text or "").strip()[:500]
        self.last_output_request_id = str(request_id or "")
        self.waiting_for_user = True
        self.conversation_status = V1_CONV_WAITING_USER
        self._did_submit_this_call = True

    def apply_no_submit_conservative(self) -> None:
        """
        本轮未发生成功 output submit 时由 SessionManager 调用：
        不伪造 last_system_text；不把 waiting_user 当成「系统已说」。
        """
        if self._did_submit_this_call:
            return
        self.waiting_for_user = False
        self.conversation_status = V1_CONV_IDLE
