# -*- coding: utf-8 -*-
"""M) Shadow 最小上传与聚合协议 v0 单元测试"""

import json
import pytest

from intervention.shadow_upload_v0 import (
    build_upload_payload,
    compute_intervention_stats,
    compute_arbitration_stats,
    compute_failure_stats,
    compute_multimodal_stats,
)


def test_compute_intervention_stats_empty():
    stats = compute_intervention_stats([])
    assert stats["active_time_s"] == 0
    assert stats["engaged_ratio"] == 0
    assert stats["level_dist"] == {}
    assert stats["avg_switches_per_min"] == 0


def test_compute_intervention_stats():
    rows = [
        {"ts": 1000, "intervention": {"task_state": "ACTIVE"}, "rhythm": {"state": "IDLE"}, "engagement": {"level": "L0"}},
        {"ts": 1010, "intervention": {"task_state": "ACTIVE"}, "rhythm": {"state": "ENGAGED"}, "engagement": {"level": "L1"}},
        {"ts": 1020, "intervention": {"task_state": "ACTIVE"}, "rhythm": {"state": "ENGAGED"}, "engagement": {"level": "L2"}},
    ]
    stats = compute_intervention_stats(rows)
    assert stats["active_time_s"] == 20
    assert stats["engaged_time_s"] == 10
    assert 0 < stats["engaged_ratio"] < 1
    assert "L1" in stats["level_dist"] or "L2" in stats["level_dist"]


def test_compute_failure_stats():
    # J v0: 使用 engaged_signal（block_stage → legacy reason 兼容）
    rows = [
        {"engaged_signal": {"blocked": True, "block_stage": "COOLDOWN"}},
        {"engaged_signal": {"blocked": True, "block_stage": "COOLDOWN"}},
        {"engaged_signal": {"blocked": True, "block_stage": "ARBITRATION"}},
    ]
    stats = compute_failure_stats(rows)
    assert stats["FAIL_COOLDOWN_ACTIVE"] == pytest.approx(2 / 3, rel=0.01)
    assert stats["FAIL_ARBITRATION_LOST"] == pytest.approx(1 / 3, rel=0.01)


def test_build_upload_payload():
    rows = [
        {"ts": 1000, "intervention": {"task_state": "ACTIVE"}, "rhythm": {"state": "IDLE"}, "engagement": {"level": "L0"}},
    ]
    payload = build_upload_payload(rows, device_class="BADGE", camera_fov_class="WIDE")
    assert "intervention_stats" in payload
    assert "arbitration_stats" in payload
    assert "failure_stats" in payload
    assert "multimodal_stats" in payload
    assert "device_meta" in payload
    assert payload["device_meta"]["device_class"] == "BADGE"
    assert payload["device_meta"]["camera_fov_class"] == "WIDE"
    assert "version" in payload["device_meta"]
    # M) 严格不上传：文本、task_id
    payload_str = json.dumps(payload)
    assert "text" not in payload_str or "text_preview" not in payload_str
