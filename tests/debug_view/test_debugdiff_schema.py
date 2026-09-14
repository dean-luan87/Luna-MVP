import json

from luna_badge_v1_2.governance.output_controller.debug_diff_schema import SCHEMA_VERSION
from tools.debug.compare_runs import build_diff_report


def _snapshot_with_debug_view(debug_view: dict):
    return {"debug_view": debug_view}


def test_debugdiff_schema():
    report = build_diff_report(
        [_snapshot_with_debug_view({"risk": {"level": "LOW"}})],
        [_snapshot_with_debug_view({"risk": {"level": "MEDIUM"}})],
        "base",
        "cand",
    )
    assert report["schema_version"] == SCHEMA_VERSION
    assert "added_fields" in report
    assert "removed_fields" in report
    assert "changed_fields" in report
    assert "meta" in report
    json.dumps(report)
