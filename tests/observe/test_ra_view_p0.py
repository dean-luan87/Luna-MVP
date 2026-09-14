import json
import pytest
from pathlib import Path

from luna_badge_v1_2.governance.observe.ra_view.reader import read_timeline
from luna_badge_v1_2.governance.observe.ra_view.metrics import compute_metrics


def test_ra_view_deterministic():
    timeline = [
        {"ts": 1.0, "authority_effective": "A3", "risk_level": "LOW", "envelope_status": "WITHIN_ENVELOPE"},
        {"ts": 2.0, "authority_effective": "A3", "risk_level": "MEDIUM", "envelope_status": "ADMISSIBLE"},
    ]
    m1 = compute_metrics(timeline)
    m2 = compute_metrics(timeline)
    assert m1 == m2


def test_reader_rejects_control_fields(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    record = {"decision_trace": {"bc_snapshot": {"decision": "execute", "debug_view": {}}}}
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(AssertionError):
        read_timeline(str(path))
