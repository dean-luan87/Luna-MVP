#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify destination_bound_materialization_eval_v0 (read-only evaluator).

Scenarios:
- A: candidate present but no confirmation -> materialize_ready=false, reason=missing_confirmation_fact
- B: candidate+confirmation present but no binding evidence -> materialize_ready=false, reason=missing_binding_evidence
- C: candidate+confirmation+destination_id+upgrade_eligible but needs_confirmation=true -> materialize_ready=false, reason=confirmation_or_ambiguity_blocker
- D: candidate+confirmation+destination_id+upgrade_eligible and no blockers -> materialize_ready=true
- E: ordinary input via mainline -> not written by dispatcher
- F: V1 minimal flow remains OK (run separately)
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _stub_res(
    *,
    has_confirmation: bool,
    has_binding: bool,
    upgrade_eligible: bool,
    needs_confirmation: bool,
) -> Any:
    from capabilities.voice.bridge.route_types import BridgeRouteType

    proposal = SimpleNamespace(task_action="start_navigation")
    if has_binding:
        setattr(proposal, "destination_id", "dest_123")
    bd = SimpleNamespace(route=BridgeRouteType.TASK_LIFECYCLE, proposal=proposal)

    md: Dict[str, Any] = {
        "destination_candidate_v0": {
            "candidate_present": True,
            "candidate_text": "人民广场",
            "candidate_scope": "navigation_destination_candidate_v0",
            "requires_confirmation": True,
            "binding_reason": "candidate_captured_but_not_bound",
        }
    }

    if has_confirmation:
        md["destination_confirmation_fact_v0"] = {
            "confirmation_ready": True,
            "check_scope": "navigation_destination_confirmation_fact_v0",
            "confirmation_target": "current_destination_candidate",
            "needs_confirmation": bool(needs_confirmation),
        }

    if has_binding:
        md["destination_bound_check_v0"] = {
            "bound_ready": True,
            "check_scope": "navigation_destination_bound_check_v0",
            "binding_key_seen": "destination_id",
            "needs_confirmation": False,
        }
    else:
        md["destination_bound_check_v0"] = {
            "bound_ready": False,
            "check_scope": "navigation_destination_bound_check_v0",
            "reason": "missing_binding_evidence",
        }

    if upgrade_eligible:
        md["destination_bound_upgrade_eval_v0"] = {
            "eligible": True,
            "eval_scope": "navigation_destination_bound_upgrade_v0",
            "upgrade_scope": "future_bound_candidate_only",
            **({"needs_confirmation": True} if needs_confirmation else {}),
        }
    else:
        md["destination_bound_upgrade_eval_v0"] = {
            "eligible": False,
            "eval_scope": "navigation_destination_bound_upgrade_v0",
            "reason": "missing_binding_evidence",
        }

    return SimpleNamespace(
        dispatch_type="short_controlled_input",
        bridge_decision=bd,
        metadata=md,
    )


def _stub_event(text: str, *, has_ambiguities: bool = False, requires_followup: bool = False) -> Any:
    md = {}
    if has_ambiguities or requires_followup:
        md["luna_voice_semantic_v2"] = {
            "ambiguities": (["x"] if has_ambiguities else []),
            "requires_followup": bool(requires_followup),
        }
    return SimpleNamespace(wake_word_stripped=text, normalized_text=text, raw_text=text, metadata=md)


def main() -> int:
    os.environ["LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"] = "0"

    from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager  # noqa: E402
    from capabilities.voice.runtime.voice_navigation_destination_bound_materialization_eval_v0 import (  # noqa: E402
        evaluate_destination_bound_materialization_eval_v0,
    )

    # A
    res_a = _stub_res(has_confirmation=False, has_binding=True, upgrade_eligible=True, needs_confirmation=False)
    app_a, out_a = evaluate_destination_bound_materialization_eval_v0(res=res_a, event=_stub_event("对"))
    assert app_a is True
    assert isinstance(out_a, dict)
    assert out_a.get("materialize_ready") is False
    assert out_a.get("reason") == "missing_confirmation_fact"

    # B
    res_b = _stub_res(has_confirmation=True, has_binding=False, upgrade_eligible=False, needs_confirmation=False)
    app_b, out_b = evaluate_destination_bound_materialization_eval_v0(res=res_b, event=_stub_event("对"))
    assert app_b is True
    assert isinstance(out_b, dict)
    assert out_b.get("materialize_ready") is False
    assert out_b.get("reason") == "missing_binding_evidence"

    # C (blocker from needs_confirmation)
    res_c = _stub_res(has_confirmation=True, has_binding=True, upgrade_eligible=True, needs_confirmation=True)
    app_c, out_c = evaluate_destination_bound_materialization_eval_v0(res=res_c, event=_stub_event("对"))
    assert app_c is True
    assert isinstance(out_c, dict)
    assert out_c.get("materialize_ready") is False
    assert out_c.get("reason") == "confirmation_or_ambiguity_blocker"

    # D (no blockers)
    res_d = _stub_res(has_confirmation=True, has_binding=True, upgrade_eligible=True, needs_confirmation=False)
    app_d, out_d = evaluate_destination_bound_materialization_eval_v0(res=res_d, event=_stub_event("对"))
    assert app_d is True
    assert isinstance(out_d, dict)
    assert out_d.get("materialize_ready") is True
    assert out_d.get("materialization_scope") == "future_bound_materialization_candidate_only"
    assert (res_d.metadata or {}).get("destination_bound") is None

    # E (ordinary input via mainline should not write the field)
    mgr = VoiceInputSessionManager()
    res_e = mgr.process_final_text_with_dispatch(
        "你好",
        now=time.time(),
        is_task_mode=False,
        session_id="bound_materialization_eval_e",
        source_type="simulated",
    )
    md_e: Dict[str, Any] = dict(getattr(res_e, "metadata", {}) or {})
    assert md_e.get("destination_bound_materialization_eval_v0") is None

    print("VERIFY_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_EVAL_V0: ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

