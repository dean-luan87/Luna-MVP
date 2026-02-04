from tools.observe.ra_view_helpers import build_ra_view
from luna_badge_v1_2.governance.observe.ra_view.schema import SCHEMA_VERSION


def test_ra_view_stable(freeze_inputs, fixed_time):
    from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController

    ctrl = ModelOutputController()
    ctrl.process("nav", freeze_inputs["model_outputs"], freeze_inputs["system_snapshot"])
    timeline = [
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
        for item in [snap["debug_view"] for snap in ctrl._bc_snapshot_history]
    ]
    r1 = build_ra_view(timeline, "last_1", fixed_time)
    r2 = build_ra_view(timeline, "last_1", fixed_time)
    assert r1 == r2
    assert r1["schema_version"] == SCHEMA_VERSION
