#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.2-Explain E7: 构造 3 条 OBS_V1 record，调 explain_episode，断言四块/focus_fields/无外部字段/field_deltas 数值。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from library.episode_explainer import EpisodeExplainer


def main():
    fake_records = [
        {"record_type": "OBS_V1", "obs": {"motion": 0.0, "path": 0.0, "branch": 0.0, "roi": 0, "vc": 0.8, "complexity": 0.5, "pal": 0.2}, "decision": {"safety_level": "SAFE", "control_mode": "ASSISTED"}},
        {"record_type": "OBS_V1", "obs": {"motion": 0.1, "path": 0.0, "branch": 0.0, "roi": 0, "vc": 0.6, "complexity": 0.6, "pal": 0.3}, "decision": {"safety_level": "CAUTION", "control_mode": "GUARDED"}},
        {"record_type": "OBS_V1", "obs": {"motion": 0.1, "path": 0.0, "branch": 0.0, "roi": 0, "vc": 0.6, "complexity": 0.6, "pal": 0.3}, "decision": {"safety_level": "CAUTION", "control_mode": "GUARDED"}},
    ]

    explainer = EpisodeExplainer()
    out = explainer.explain_episode(
        episode_id="TEST_EP",
        trigger_type="SAFETY_CHANGE",
        records=fake_records,
    )

    if "structured_explain" not in out:
        print("FAIL: structured_explain missing")
        return 1
    se = out["structured_explain"]
    for block in ("environment", "risk_analysis", "engagement_analysis", "decision_analysis"):
        if block not in se:
            print("FAIL: structured_explain missing block", block)
            return 1

    if "focus_fields" not in out or not out["focus_fields"]:
        print("FAIL: focus_fields missing or empty")
        return 1
    if "decision.safety_level" not in out["focus_fields"]:
        print("FAIL: focus_fields must contain decision.safety_level")
        return 1

    raw = json.dumps(out)
    for bad in ("ocr_text", "map_hint", "speech_event"):
        if bad in raw:
            print("FAIL: output must not contain", bad)
            return 1

    fd = out.get("field_deltas") or {}
    for key in ("complexity_delta", "pal_delta"):
        if key not in fd:
            print("FAIL: field_deltas missing", key)
            return 1
        v = fd[key]
        if v is not None and not isinstance(v, (int, float)):
            print("FAIL: field_deltas", key, "must be numeric, got", type(v))
            return 1

    print("PASSED: episode_explainer (four blocks, focus_fields with decision.safety_level, no external keys, numeric deltas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
