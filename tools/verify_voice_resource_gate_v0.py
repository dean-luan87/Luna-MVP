#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Resource Sufficiency Gate v0 (pre-submit admission).

Asserts:
- dispatch_type / bridge_route remain unchanged
- submit is skipped only when resource_status_v0 present and indicates insufficient resources
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
    from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402

    now = time.time()
    ok_all = True

    # A: no resource_status_v0 -> allow submit
    plane_a, texts_a = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_a):
        mgr = VoiceInputSessionManager()
        res_a = mgr.process_final_text_with_dispatch(
            "艾达",
            now=now,
            is_task_mode=False,
            session_id="rg_a",
            runtime_context=VoiceRuntimeContext(metadata={}),
        )
    a_ok = len(texts_a) == 1 and res_a.metadata.get("resource_gate_v0") is None
    print("=== A no resource_status_v0 ===")
    print("  dispatch:", _digest(res_a), "submit:", len(texts_a), "gate:", res_a.metadata.get("resource_gate_v0"))
    print("  预期: submit=1, gate 不写 →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    # baseline digest for a submit-producing path should remain stable across resource states
    plane_b0, texts_b0 = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b0):
        mgr = VoiceInputSessionManager()
        res_b0 = mgr.process_final_text_with_dispatch(
            "艾达",
            now=now,
            is_task_mode=False,
            session_id="rg_b0",
            runtime_context=VoiceRuntimeContext(metadata={"resource_status_v0": {"battery_ok": True, "required_modules_ok": True}}),
        )
    base_digest = _digest(res_b0)

    # B: battery_ok=false -> skip submit, gate written
    plane_b, texts_b = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b):
        mgr = VoiceInputSessionManager()
        res_b = mgr.process_final_text_with_dispatch(
            "艾达",
            now=now,
            is_task_mode=False,
            session_id="rg_b",
            runtime_context=VoiceRuntimeContext(metadata={"resource_status_v0": {"battery_ok": False, "required_modules_ok": True}}),
        )
    b_gate = res_b.metadata.get("resource_gate_v0") or {}
    b_ok = _digest(res_b) == base_digest and len(texts_b) == 0 and b_gate.get("gate_passed") is False
    print("=== B battery_ok=false ===")
    print("  dispatch:", _digest(res_b), "submit:", len(texts_b), "gate:", b_gate)
    print("  预期: dispatch 不变, submit=0, gate_passed=false →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    # C: required_modules_ok=false -> skip submit
    plane_c, texts_c = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_c):
        mgr = VoiceInputSessionManager()
        res_c = mgr.process_final_text_with_dispatch(
            "艾达",
            now=now,
            is_task_mode=False,
            session_id="rg_c",
            runtime_context=VoiceRuntimeContext(metadata={"resource_status_v0": {"battery_ok": True, "required_modules_ok": False}}),
        )
    c_gate = res_c.metadata.get("resource_gate_v0") or {}
    c_ok = _digest(res_c) == base_digest and len(texts_c) == 0 and c_gate.get("gate_passed") is False
    print("=== C required_modules_ok=false ===")
    print("  dispatch:", _digest(res_c), "submit:", len(texts_c), "gate:", c_gate)
    print("  预期: dispatch 不变, submit=0, gate_passed=false →", "OK" if c_ok else "FAIL")
    ok_all = ok_all and c_ok

    # D: both ok -> submit and gate_passed=true
    plane_d, texts_d = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_d):
        mgr = VoiceInputSessionManager()
        res_d = mgr.process_final_text_with_dispatch(
            "艾达",
            now=now,
            is_task_mode=False,
            session_id="rg_d",
            runtime_context=VoiceRuntimeContext(metadata={"resource_status_v0": {"battery_ok": True, "required_modules_ok": True}}),
        )
    d_gate = res_d.metadata.get("resource_gate_v0") or {}
    d_ok = _digest(res_d) == base_digest and len(texts_d) == 1 and d_gate.get("gate_passed") is True
    print("=== D battery_ok=true & required_modules_ok=true ===")
    print("  dispatch:", _digest(res_d), "submit:", len(texts_d), "gate:", d_gate)
    print("  预期: dispatch 不变, submit=1, gate_passed=true →", "OK" if d_ok else "FAIL")
    ok_all = ok_all and d_ok

    if ok_all:
        print("\nVERIFY_VOICE_RESOURCE_GATE_V0: ALL_OK")
        return 0
    print("\nVERIFY_VOICE_RESOURCE_GATE_V0: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

