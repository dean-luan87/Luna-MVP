# -*- coding: utf-8 -*-
"""
Verify: risk_summary_v1 gate-ready eval v0 (read-only).

Coverage:
- A: complete + legal fields -> gate_ready_passed True
- B: missing fields -> gate_ready_passed False + missing_fields
- C: invalid values -> gate_ready_passed False + invalid_fields
- D: absent risk_summary -> not_present True (or still false) and no behavior impact
Also ensures V1 minimal flow script still passes (run separately by caller).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text  # noqa: E402
from capabilities.voice.runtime.voice_v1_session_state_anchor import VoiceV1SessionStateAnchor  # noqa: E402
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent  # noqa: E402
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext  # noqa: E402


def _mk_event(text: str = "艾达") -> VoiceInputEvent:
    # Stable short_controlled_input path (wake word).
    return VoiceInputEvent(
        event_id="ev_test",
        request_id="req_test",
        timestamp=1.0,
        session_id="sess_test",
        turn_id="turn_test",
        source="test",
        text=text,
        raw_text=text,
        normalized_text="",
        source_type="simulated",
        is_task_mode=False,
        router_decision="accept",
        wake_word_detected=True,
        wake_word_stripped="",
        wake_word="艾达",
        active_window=False,
        metadata={},
    )


def _get_eval(res) -> dict:
    md = res.metadata or {}
    ev = md.get("risk_summary_v1_gate_ready_eval_v0")
    assert isinstance(ev, dict), f"eval missing or not dict: {type(ev).__name__}"
    return ev


def main() -> None:
    # Ensure submit side effects are off for this verification.
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    anchor = VoiceV1SessionStateAnchor()
    ev = _mk_event()

    # A: complete legal
    ctx_a = VoiceRuntimeContext(
        metadata={
            "risk_summary_v1": {
                "risk_level": "high",
                "risk_type": "traffic",
                "risk_reason": "test_reason",
                "confidence": 0.9,
                "source": "upstream_test",
                "is_gate_ready": True,
            }
        }
    )
    res_a = dispatch_voice_final_text(ev, runtime_context=ctx_a, session_state_anchor=anchor)
    eva = _get_eval(res_a)
    assert eva.get("gate_ready_passed") is True
    assert eva.get("risk_level_seen") == "high"
    assert eva.get("source_seen") == "upstream_test"
    assert res_a.dispatch_type == "short_controlled_input"

    # B: missing fields
    ctx_b = VoiceRuntimeContext(
        metadata={
            "risk_summary_v1": {
                "risk_level": "high",
                "risk_type": "traffic",
                "confidence": 0.9,
                "is_gate_ready": True,
            }
        }
    )
    res_b = dispatch_voice_final_text(ev, runtime_context=ctx_b, session_state_anchor=anchor)
    evb = _get_eval(res_b)
    assert evb.get("gate_ready_passed") is False
    mf = evb.get("missing_fields") or []
    assert "risk_reason" in mf
    assert "source" in mf
    assert res_b.dispatch_type == "short_controlled_input"

    # C: invalid values
    ctx_c = VoiceRuntimeContext(
        metadata={
            "risk_summary_v1": {
                "risk_level": "maybe",
                "risk_type": "traffic",
                "risk_reason": "test_reason",
                "confidence": "high",
                "source": "upstream_test",
                "is_gate_ready": "true",
            }
        }
    )
    res_c = dispatch_voice_final_text(ev, runtime_context=ctx_c, session_state_anchor=anchor)
    evc = _get_eval(res_c)
    assert evc.get("gate_ready_passed") is False
    inv = evc.get("invalid_fields") or []
    assert "risk_level" in inv
    assert "confidence" in inv
    assert "is_gate_ready" in inv
    assert res_c.dispatch_type == "short_controlled_input"

    # D: absent
    ctx_d = VoiceRuntimeContext(metadata={})
    res_d = dispatch_voice_final_text(ev, runtime_context=ctx_d, session_state_anchor=anchor)
    evd = _get_eval(res_d)
    assert evd.get("gate_ready_passed") is False
    assert evd.get("not_present") is True
    assert res_d.dispatch_type == "short_controlled_input"

    print("ALL_OK")


if __name__ == "__main__":
    main()

