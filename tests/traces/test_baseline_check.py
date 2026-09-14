# -*- coding: utf-8 -*-
"""基线校验：medium_long_01 四指标、stress_oscillate_01 抖动约束；合并前必跑。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
BASELINE_MEDIUM = _ROOT / "tests" / "traces" / "baselines" / "medium_long_01.json"
BASELINE_STRESS = _ROOT / "tests" / "traces" / "baselines" / "stress_oscillate_01.json"
REPORT_CANDIDATES = [
    _ROOT / "logs" / "trace_report_6m42s.json",
    _ROOT / "logs" / "trace_report.json",
]


def _find_report_with_label(label: str) -> Path | None:
    for p in REPORT_CANDIDATES:
        if not p.exists():
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if label in data.get("videos", {}):
                return p
        except Exception:
            continue
    return None


@pytest.mark.trace_anchor
@pytest.mark.skipif(not BASELINE_MEDIUM.exists(), reason="baseline medium_long_01 not found")
def test_medium_long_01_baseline_constraints() -> None:
    """稳定性锚：suite 后 medium_long_01 必须满足四指标约束。"""
    report_path = _find_report_with_label("medium_long_01")
    if report_path is None:
        pytest.skip("no trace_report with videos['medium_long_01']; run: make trace-suite (or --label medium_long_01)")
    proc = subprocess.run(
        [sys.executable, str(_ROOT / "tests" / "traces" / "check_baseline.py"), str(BASELINE_MEDIUM), str(report_path)],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"check_baseline failed: {proc.stderr or proc.stdout}"


@pytest.mark.trace_anchor
@pytest.mark.skipif(not BASELINE_STRESS.exists(), reason="baseline stress_oscillate_01 not found")
def test_stress_oscillate_01_baseline_constraints() -> None:
    """抖动治理锚：suite 后 stress_oscillate_01 必须满足 short_caution_run_ratio / switch_per_min 约束。"""
    report_path = _find_report_with_label("stress_oscillate_01")
    if report_path is None:
        pytest.skip("no trace_report with videos['stress_oscillate_01']; run: make trace-suite (or --label stress_oscillate_01)")
    proc = subprocess.run(
        [sys.executable, str(_ROOT / "tests" / "traces" / "check_baseline.py"), str(BASELINE_STRESS), str(report_path)],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"check_baseline failed: {proc.stderr or proc.stdout}"
