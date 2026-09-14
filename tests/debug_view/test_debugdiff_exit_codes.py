import json
import subprocess
from pathlib import Path


def _write_run(path: Path, debug_view: dict) -> None:
    record = {"decision_trace": {"bc_snapshot": {"debug_view": debug_view}}}
    with path.open("w") as f:
        f.write(json.dumps(record) + "\n")


def test_exit_code_added_fields(tmp_path: Path):
    baseline = tmp_path / "base.jsonl"
    candidate = tmp_path / "cand.jsonl"
    out = tmp_path / "diff.json"
    _write_run(baseline, {"risk": {"level": "LOW"}})
    _write_run(candidate, {"risk": {"level": "LOW"}, "extra": {"x": 1}})
    result = subprocess.run(
        [
            "python3",
            "tools/debug/compare_runs.py",
            "--baseline",
            str(baseline),
            "--candidate",
            str(candidate),
            "--out",
            str(out),
        ]
    )
    assert result.returncode == 2


def test_exit_code_removed_fields(tmp_path: Path):
    baseline = tmp_path / "base.jsonl"
    candidate = tmp_path / "cand.jsonl"
    out = tmp_path / "diff.json"
    _write_run(baseline, {"risk": {"level": "LOW"}, "extra": {"x": 1}})
    _write_run(candidate, {"risk": {"level": "LOW"}})
    result = subprocess.run(
        [
            "python3",
            "tools/debug/compare_runs.py",
            "--baseline",
            str(baseline),
            "--candidate",
            str(candidate),
            "--out",
            str(out),
        ]
    )
    assert result.returncode == 3
