#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Continue Request Response v0 (Information Gate blocked + continue-request phrasing).

Scenarios:
- A: info gate hit + continue phrase -> fixed template submit + metadata
- B: info gate hit + 按我说的做 -> template
- C: info gate hit but no continue phrase -> no template
- D: no info gate (session_wake) + no template path
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, List, Tuple
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from capabilities.voice.runtime.voice_continue_request_response_v0 import (  # noqa: E402
    CONTINUE_REQUEST_INFO_CONFIRM_TEMPLATE_V0,
)


def _patch_submit() -> tuple[MagicMock, List[str]]:
    texts: List[str] = []

    def _submit(req: Any) -> tuple[bool, str]:
        texts.append(str(getattr(req, "text_candidate", "") or ""))
        return True, "ok"

    plane = MagicMock()
    plane.submit = _submit
    return plane, texts


def _digest(res: Any) -> Tuple[str, str]:
    dt = str(getattr(res, "dispatch_type", "") or "")
    route = ""
    bd = getattr(res, "bridge_decision", None)
    if bd is not None:
        r = getattr(bd, "route", None)
        route = str(getattr(r, "value", "") or r or "")
    return dt, route


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "1"
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"] = "0"
    os.environ["LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402

    now = time.time()
    ok_all = True
    tpl = CONTINUE_REQUEST_INFO_CONFIRM_TEMPLATE_V0

    # A: task_mode + 继续 + deictic -> gate blocks normal submit; template path speaks
    plane_a, texts_a = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_a):
        mgr = VoiceInputSessionManager()
        res_a = mgr.process_final_text_with_dispatch(
            "艾达继续那个",
            now=now,
            is_task_mode=True,
            session_id="cr_a",
        )
    dig_a = _digest(res_a)
    ig_a = res_a.metadata.get("information_confirmation_gate_v0") or {}
    cr_a = res_a.metadata.get("continue_request_response_v0") or {}
    a_ok = (
        ig_a.get("gate_passed") is False
        and ig_a.get("requires_confirmation") is True
        and cr_a.get("response_triggered") is True
        and any(tpl in x for x in texts_a)
        and dig_a[0] == "short_controlled_input"
    )
    print("=== A gate + 继续那个 ===")
    print("  digest:", dig_a, "submits:", texts_a, "cr:", cr_a)
    print("  预期: 模板播报 + metadata →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    # B: 按我说的做 + deictic
    plane_b, texts_b = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b):
        mgr = VoiceInputSessionManager()
        res_b = mgr.process_final_text_with_dispatch(
            "艾达按我说的做这个",
            now=now,
            is_task_mode=True,
            session_id="cr_b",
        )
    cr_b = res_b.metadata.get("continue_request_response_v0") or {}
    b_ok = cr_b.get("response_triggered") is True and any(tpl in x for x in texts_b)
    print("=== B 按我说的做这个 ===")
    print("  submits:", texts_b, "cr:", cr_b)
    print("  预期: 模板 →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    # C: deictic but no continue phrase (same as confirmation gate B style)
    plane_c, texts_c = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_c):
        mgr = VoiceInputSessionManager()
        res_c = mgr.process_final_text_with_dispatch("去那里", now=now, is_task_mode=False, session_id="cr_c")
    cr_c = res_c.metadata.get("continue_request_response_v0")
    c_ok = (cr_c is None) and (len([t for t in texts_c if tpl in t]) == 0)
    print("=== C 去那里（无继续语气）===")
    print("  submits:", len(texts_c), "cr:", cr_c)
    print("  预期: 无 continue_request_response_v0、无模板 →", "OK" if c_ok else "FAIL")
    ok_all = ok_all and c_ok

    # D: session_wake only — no info gate write, no template
    plane_d, texts_d = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_d):
        mgr = VoiceInputSessionManager()
        res_d = mgr.process_final_text_with_dispatch("艾达", now=now, is_task_mode=False, session_id="cr_d")
    cr_d = res_d.metadata.get("continue_request_response_v0")
    d_ok = cr_d is None and res_d.metadata.get("information_confirmation_gate_v0") is None
    print("=== D 仅唤醒 ===")
    print("  gate:", res_d.metadata.get("information_confirmation_gate_v0"), "cr:", cr_d)
    print("  预期: 不由本专题接管 →", "OK" if d_ok else "FAIL")
    ok_all = ok_all and d_ok

    if ok_all:
        print("\nVERIFY_CONTINUE_REQUEST_RESPONSE_V0: ALL_OK")
        return 0
    print("\nVERIFY_CONTINUE_REQUEST_RESPONSE_V0: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
