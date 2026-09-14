#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Confirmation Gate v0 for missing/ambiguous references (pre-submit).

Asserts:
- dispatch_type / bridge_route remain unchanged
- submit is skipped only when deictic term is present and no unique binding facts exist (v0 conservative)
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

    # A: normal input without deictic term (reject path should still submit)
    plane_a, texts_a = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_a):
        mgr = VoiceInputSessionManager()
        res_a = mgr.process_final_text_with_dispatch("你好", now=now, is_task_mode=False, session_id="cg_a")
    a_ok = len(texts_a) == 1 and res_a.metadata.get("information_confirmation_gate_v0") is None
    print("=== A no deictic term ===")
    print("  dispatch:", _digest(res_a), "submit:", len(texts_a), "gate:", res_a.metadata.get("information_confirmation_gate_v0"))
    print("  预期: submit=1, gate 不写 →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    base_digest = _digest(res_a)

    # B: deictic term present; v0 assumes no unique binding facts -> should block submit on reject path
    plane_b, texts_b = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b):
        mgr = VoiceInputSessionManager()
        res_b = mgr.process_final_text_with_dispatch("去那里", now=now, is_task_mode=False, session_id="cg_b")
    b_gate = res_b.metadata.get("information_confirmation_gate_v0") or {}
    b_ok = _digest(res_b) == base_digest and len(texts_b) == 0 and b_gate.get("gate_passed") is False and b_gate.get("requires_confirmation") is True
    print("=== B deictic term + no binding ===")
    print("  dispatch:", _digest(res_b), "submit:", len(texts_b), "gate:", b_gate)
    print("  预期: dispatch 不变, submit=0, requires_confirmation=true →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    # C: another normal input without deictic term should pass
    plane_c, texts_c = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_c):
        mgr = VoiceInputSessionManager()
        res_c = mgr.process_final_text_with_dispatch("艾达", now=now, is_task_mode=False, session_id="cg_c")
    c_ok = len(texts_c) == 1
    print("=== C no deictic term (session_wake) ===")
    print("  dispatch:", _digest(res_c), "submit:", len(texts_c), "gate:", res_c.metadata.get("information_confirmation_gate_v0"))
    print("  预期: submit=1 →", "OK" if c_ok else "FAIL")
    ok_all = ok_all and c_ok

    if ok_all:
        print("\nVERIFY_VOICE_CONFIRMATION_GATE_V0: ALL_OK")
        return 0
    print("\nVERIFY_VOICE_CONFIRMATION_GATE_V0: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

