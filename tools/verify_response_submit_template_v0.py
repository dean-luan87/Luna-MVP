#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Response Submit Template Interface v0 (unified response-kind submit).

Focus:
- Only unifies existing continue-request + information gate template
- Adds result.metadata["response_submit_template_v0"]
- Does not change gate/route/proposal decisions
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

    # A: info gate hit + continue phrasing -> response template submit + unified metadata
    plane_a, texts_a = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_a):
        mgr = VoiceInputSessionManager()
        res_a = mgr.process_final_text_with_dispatch("艾达继续那个", now=now, is_task_mode=True, session_id="rst_a")
    ig_a = res_a.metadata.get("information_confirmation_gate_v0") or {}
    rs_a = res_a.metadata.get("response_submit_template_v0") or {}
    a_ok = (
        ig_a.get("gate_passed") is False
        and ig_a.get("requires_confirmation") is True
        and rs_a.get("response_submitted") is True
        and rs_a.get("template_id") == "continue_request_info_confirm_v0"
        and any(tpl in x for x in texts_a)
        and _digest(res_a)[0] == "short_controlled_input"
    )
    print("=== A info gate + continue ===")
    print("  digest:", _digest(res_a), "texts:", texts_a, "response_submit:", rs_a)
    print("  预期: 模板播报 + response_submit_template_v0 →", "OK" if a_ok else "FAIL")
    ok_all = ok_all and a_ok

    # B: info gate hit but not continue phrasing -> no unified metadata
    plane_b, texts_b = _patch_submit()
    with patch("capabilities.voice.output.voice_output_plane_v1.get_voice_output_plane_v1", return_value=plane_b):
        mgr = VoiceInputSessionManager()
        res_b = mgr.process_final_text_with_dispatch("去那里", now=now, is_task_mode=False, session_id="rst_b")
    b_ok = (res_b.metadata.get("response_submit_template_v0") is None) and (len([t for t in texts_b if tpl in t]) == 0)
    print("=== B info gate but not continue ===")
    print("  texts:", texts_b, "response_submit:", res_b.metadata.get("response_submit_template_v0"))
    print("  预期: 不触发 →", "OK" if b_ok else "FAIL")
    ok_all = ok_all and b_ok

    if ok_all:
        print("\nVERIFY_RESPONSE_SUBMIT_TEMPLATE_V0: ALL_OK")
        return 0
    print("\nVERIFY_RESPONSE_SUBMIT_TEMPLATE_V0: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

