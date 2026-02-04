from tools.debug.dump_debug_view import build_debug_view_payload
from tools.observe.ra_view_helpers import build_ra_view
from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController


def _run_once(freeze_inputs, fixed_time):
    ctrl = ModelOutputController()
    result = ctrl.process(
        task_domain="nav",
        model_outputs=freeze_inputs["model_outputs"],
        system_snapshot=freeze_inputs["system_snapshot"],
    )
    timeline = [snap["debug_view"] for snap in ctrl._bc_snapshot_history]
    debug = build_debug_view_payload(timeline, fixed_time)
    ra = build_ra_view(
        [
            {
                "ts": item.get("authority_panel", {}).get("since", 0.0),
                "authority_effective": item.get("authority_panel", {}).get("effective"),
                "risk_level": item.get("risk_panel", {}).get("level"),
                "envelope_status": item.get("envelope", {}).get("status"),
                "risk_vo_level": item.get("risk_panel", {}).get("vo", {}).get("level"),
                "gate": item.get("gate"),
                "distortion_distorted": item.get("distortion", {}).get("distorted", False),
                "distortion_codes": item.get("distortion", {}).get("codes", []),
                "c_decision": item.get("c_decision"),
                "bc_action": item.get("bc_action"),
                "authority_blocked_by": item.get("authority_panel", {}).get("blocked_by"),
            }
            for item in timeline
        ],
        window="last_1",
        generated_at=fixed_time,
    )
    return result, debug, ra


def test_replay_determinism(freeze_inputs, fixed_time):
    r1, d1, ra1 = _run_once(freeze_inputs, fixed_time)
    r2, d2, ra2 = _run_once(freeze_inputs, fixed_time)
    assert r1 == r2
    assert d1 == d2
    assert ra1 == ra2
