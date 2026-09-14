import json
import pytest
from pathlib import Path

from luna_badge_v1_2.governance.risk_center.evaluation.evaluator import evaluate_metrics
from luna_badge_v1_2.governance.risk_center.evaluation.reader import read_timeline_from_jsonl


def test_evaluation_deterministic():
    timeline = [
        {
            "authority_panel": {"effective": "A3"},
            "risk_panel": {"level": "LOW", "time_to_risk": 3.0},
            "envelope": {"status": "WITHIN_ENVELOPE"},
        },
        {
            "authority_panel": {"effective": "A3"},
            "risk_panel": {"level": "LOW", "time_to_risk": 4.0},
            "envelope": {"status": "SAFE_ENOUGH"},
        },
    ]
    r1 = evaluate_metrics(timeline, "last_2")
    r2 = evaluate_metrics(timeline, "last_2")
    assert r1.metrics == r2.metrics


def test_reader_rejects_control_fields(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    record = {"decision_trace": {"bc_snapshot": {"decision": "execute", "debug_view": {}}}}
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(AssertionError):
        read_timeline_from_jsonl(str(path))
