#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Voice V1 最小闭环端到端验证（当前仅 session_wake / reject 两类可说话路径）。

不扩功能：只验证
  VoiceInputSessionManager.process_final_text_with_dispatch
  → dispatch_voice_final_text
  → _maybe_submit_real_output_v1
  → guard_v1_speakable_text
  → VoiceOutputPlaneV1.submit

并校验 VoiceInputSessionManager.v1_session_anchor（最小会话状态锚）。

用法（在 Luna-Core 根目录）：
  PYTHONPATH=. python3 tools/verify_voice_v1_minimal_flow.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, List
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _patch_submit() -> tuple[MagicMock, List[str]]:
    """拦截 get_voice_output_plane_v1().submit，记录 text_candidate。"""
    texts: List[str] = []

    def _submit(req: Any) -> tuple[bool, str]:
        texts.append(str(getattr(req, "text_candidate", "") or ""))
        return True, "ok"

    plane = MagicMock()
    plane.submit = _submit
    return plane, texts


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "0"
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"] = "0"

    from capabilities.voice.runtime.voice_final_text_dispatcher import (  # noqa: E402
        _maybe_submit_real_output_v1,
    )
    from capabilities.voice.runtime.voice_final_text_dispatch_result import (  # noqa: E402
        VoiceFinalTextDispatchResult,
    )
    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_v1_session_state_anchor import (  # noqa: E402
        V1_CONV_IDLE,
        V1_CONV_WAITING_USER,
        VoiceV1SessionStateAnchor,
    )
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
    from capabilities.voice.schemas.voice_input_rejection_result import VoiceInputRejectionResult  # noqa: E402

    now = time.time()
    ok_all = True

    # —— 场景 A：完整主链 session_wake → 我在。 ——
    plane_a, texts_a = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_a):
        mgr = VoiceInputSessionManager()
        _ = mgr.process_final_text_with_dispatch("艾达", now=now, is_task_mode=False, session_id="verify_v1_a")
        ac = mgr.v1_session_anchor
    print("=== A session_wake（主链）===")
    print("  input raw_text:", repr("艾达"))
    print("  submit 次数:", len(texts_a), "text_candidate(s):", texts_a)
    print(
        "  anchor:",
        "last_user_text=",
        repr(ac.last_user_text),
        "last_system_text=",
        repr(ac.last_system_text),
        "waiting=",
        ac.waiting_for_user,
        "status=",
        ac.conversation_status,
    )
    a_ok = (
        len(texts_a) == 1
        and texts_a[0] == "我在。"
        and ac.last_system_text == "我在。"
        and ac.waiting_for_user is True
        and ac.conversation_status == V1_CONV_WAITING_USER
    )
    print("  预期: submit+anchor 对齐 →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    # —— 场景 B：完整主链 reject + 正常 reason ——
    plane_b, texts_b = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b):
        mgr = VoiceInputSessionManager()
        _ = mgr.process_final_text_with_dispatch("你好", now=now, is_task_mode=False, session_id="verify_v1_b")
        bc = mgr.v1_session_anchor
    print("=== B reject 正常 reason（主链）===")
    print("  input raw_text:", repr("你好"))
    print("  submit 次数:", len(texts_b), "text_candidate(s):", texts_b)
    print("  anchor last_user_text:", repr(bc.last_user_text), "last_system_text:", repr(bc.last_system_text))
    b_ok = (
        len(texts_b) == 1
        and len(texts_b[0]) > 0
        and "需要唤醒词" in texts_b[0]
        and bc.last_user_text == "你好"
        and "需要唤醒词" in bc.last_system_text
        and bc.waiting_for_user is True
        and bc.conversation_status == V1_CONV_WAITING_USER
    )
    print("  预期: submit+anchor 对齐 →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    # —— 场景 C：占位 reason —— 构造 + _maybe_submit（带 anchor）——
    plane_c, texts_c = _patch_submit()
    mini_ev = VoiceInputEvent(request_id="r_c", session_id="s_c", timestamp=now)
    res_c = VoiceFinalTextDispatchResult(
        request_id="r_c",
        session_id="s_c",
        dispatch_type="rejected_input",
        rejected_input=True,
        voice_input_event=mini_ev,
        rejection_result=VoiceInputRejectionResult(
            request_id="r_c",
            reason="TODO",
            router_stage="verify",
            raw_text=None,
            normalized_text=None,
            is_task_mode=False,
            source_type="asr",
            reason_code="verify",
        ),
    )
    anchor_c = VoiceV1SessionStateAnchor()
    anchor_c.begin_from_event(mini_ev)
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_c):
        _maybe_submit_real_output_v1(res_c, event=mini_ev, runtime_context=None, session_state_anchor=anchor_c)
    anchor_c.apply_no_submit_conservative()
    print("=== C reject 占位 reason（构造 + _maybe_submit_real_output_v1 + anchor）===")
    print("  rejection reason:", repr("TODO"))
    print("  submit 次数:", len(texts_c), "text_candidate(s):", texts_c)
    c_ok = (
        len(texts_c) == 1
        and texts_c[0] == "这个我现在不能确定。"
        and anchor_c.last_system_text == "这个我现在不能确定。"
        and anchor_c.waiting_for_user is True
        and anchor_c.conversation_status == V1_CONV_WAITING_USER
    )
    print("  预期: 降级句 + anchor →", "OK" if c_ok else "FAIL")
    ok_all = ok_all and c_ok

    # —— 场景 D：空 reason ——
    plane_d, texts_d = _patch_submit()
    mini_ev_d = VoiceInputEvent(request_id="r_d", session_id="s_d", timestamp=now)
    res_d = VoiceFinalTextDispatchResult(
        request_id="r_d",
        session_id="s_d",
        dispatch_type="rejected_input",
        rejected_input=True,
        voice_input_event=mini_ev_d,
        rejection_result=VoiceInputRejectionResult(
            request_id="r_d",
            reason="",
            router_stage="verify",
            raw_text=None,
            normalized_text=None,
            is_task_mode=False,
            source_type="asr",
            reason_code="verify",
        ),
    )
    anchor_d = VoiceV1SessionStateAnchor()
    anchor_d.begin_from_event(mini_ev_d)
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_d):
        _maybe_submit_real_output_v1(res_d, event=mini_ev_d, runtime_context=None, session_state_anchor=anchor_d)
    anchor_d.apply_no_submit_conservative()
    print("=== D reject 空 reason（构造 + anchor）===")
    print("  rejection reason:", repr(""))
    print("  submit 次数:", len(texts_d))
    print(
        "  anchor last_system_text:",
        repr(anchor_d.last_system_text),
        "waiting=",
        anchor_d.waiting_for_user,
        "status=",
        anchor_d.conversation_status,
    )
    d_ok = len(texts_d) == 0 and anchor_d.last_system_text == "" and anchor_d.waiting_for_user is False and anchor_d.conversation_status == V1_CONV_IDLE
    print("  预期: 不 submit、不伪造系统句、保守 idle →", "OK" if d_ok else "FAIL")
    ok_all = ok_all and d_ok

    print("")
    if ok_all:
        print("VERIFY_VOICE_V1_MINIMAL_FLOW: ALL_OK")
        return 0
    print("VERIFY_VOICE_V1_MINIMAL_FLOW: FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
