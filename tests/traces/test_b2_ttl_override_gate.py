# -*- coding: utf-8 -*-
"""
B2 TTL override 封版门禁：单段视频、单次运行，检查 override 已接通且密度在合理范围。

验收入口：本测试为 B2 TTL override 的唯一验收入口；通过即视为封版达标。

前置：需先用 override 跑一次 medium_long_01，生成 trace 后再跑本测试：
  B2_TTL_OVERRIDE_ENABLED=1 python3 tools/run_trace_suite.py --from-suite medium_long_01
  python3 -m pytest tests/traces/test_b2_ttl_override_gate.py -v

三条契约（Hard，回归不可破）：
  1. duration_sec 分母必须为「全 trace wall-clock」：analyze 输出 duration_sec 来自整段 trace 的 ts 范围，
     不得用仅 B2 行的 duration，避免密度被写入频率带偏。
  2. override 证据：b2_ttl_used_mean 必须落在 [B2_TTL_MEAN_MIN, B2_TTL_MEAN_MAX]，证明 runtime TTL 被吃进去。
  3. ttl_expire_density_per_sec 为硬指标：future_cache 逻辑未动，该密度应稳定在基线附近、不可爆炸。

门禁含义：
- b2_ttl_used_mean 在 [min, max]：证明 override 被吃进去
- b2_ttl_used_p95 <= 上限
- ttl_expire_density_per_sec <= 上限（硬指标）
- advisory_suppressed_density_per_sec <= 上限
- cache_hit_rate（仅 total 口径）>= baseline 或常量下限：Soft 护栏，低于则 warning 不 fail；
  cache_hit_rate_sampled 仅作报告展示，禁止作为 Hard gate。
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_TRACE = _ROOT / "logs" / "suite_medium_long_01.jsonl"
_BASELINE_OVERRIDE = _ROOT / "tests" / "traces" / "baselines" / "b2_ttl_override_medium_long_01.json"

# 默认门禁阈值（无 baseline 时使用；有 baseline 则优先读 constraints）
B2_TTL_MEAN_MIN = 1.0
B2_TTL_MEAN_MAX = 2.5
B2_TTL_P95_MAX = 3.5
TTL_EXPIRE_DENSITY_MAX = 0.05
ADVISORY_SUPPRESSED_DENSITY_MAX = 0.2
CACHE_HIT_RATE_MIN = 0.05  # soft：低于则 warning，不 fail


def _get_trace_path() -> Path:
    return Path(os.environ.get("B2_TTL_TRACE_PATH", str(_DEFAULT_TRACE)))


def _load_baseline() -> tuple[dict, dict]:
    """若存在 baseline JSON 则读 constraints 与 soft，否则返回空 dict（用模块常量）。"""
    if not _BASELINE_OVERRIDE.is_file():
        return {}, {}
    try:
        with open(_BASELINE_OVERRIDE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("constraints", {}), data.get("soft", {})
    except Exception:
        return {}, {}


@pytest.mark.trace_anchor
def test_b2_ttl_override_gate_metrics() -> None:
    """B2 TTL override 门禁：duration 全 trace wall-clock，密度与 b2_ttl_used 在可接受范围。"""
    trace_path = _get_trace_path()
    if not trace_path.is_file():
        pytest.skip(
            f"trace 不存在: {trace_path}；请先执行: "
            "B2_TTL_OVERRIDE_ENABLED=1 python3 tools/run_trace_suite.py --from-suite medium_long_01"
        )

    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))
    from tools.analyze_b2_override_effect import analyze

    out = analyze(str(trace_path))
    c, soft = _load_baseline()
    mean_min = c.get("b2_ttl_used_mean_min", B2_TTL_MEAN_MIN)
    mean_max = c.get("b2_ttl_used_mean_max", B2_TTL_MEAN_MAX)
    p95_max = c.get("b2_ttl_used_p95_max", B2_TTL_P95_MAX)
    ttl_expire_max = c.get("ttl_expire_density_per_sec_max", TTL_EXPIRE_DENSITY_MAX)
    suppressed_max = c.get("advisory_suppressed_density_per_sec_max", ADVISORY_SUPPRESSED_DENSITY_MAX)
    cache_hit_total_min = c.get("b2_cache_hit_rate_total_min") or soft.get("cache_hit_rate_min") or CACHE_HIT_RATE_MIN

    # 契约 1：密度分母必须是全 trace wall-clock
    assert out.get("duration_sec") is not None, "duration_sec 应为全 trace wall-clock，不得为 None"
    assert out["duration_sec"] > 0, "duration_sec 应 > 0"

    assert "b2_ttl_used_mean" in out, (
        "trace 中无 b2_ttl_used（telemetry.b2.ttl_used）；请确认 B2 v02 已写 telemetry 且 override 已开"
    )
    mean_ttl = out["b2_ttl_used_mean"]
    assert mean_min <= mean_ttl <= mean_max, (
        f"b2_ttl_used_mean={mean_ttl} 超出门禁区间 [{mean_min}, {mean_max}]"
    )

    if out.get("b2_ttl_used_p95") is not None:
        assert out["b2_ttl_used_p95"] <= p95_max, (
            f"b2_ttl_used_p95={out['b2_ttl_used_p95']} > {p95_max}"
        )

    if out.get("ttl_expire_density_per_sec") is not None:
        assert out["ttl_expire_density_per_sec"] <= ttl_expire_max, (
            f"ttl_expire_density_per_sec={out['ttl_expire_density_per_sec']} > {ttl_expire_max}"
        )

    if out.get("advisory_suppressed_density_per_sec") is not None:
        assert out["advisory_suppressed_density_per_sec"] <= suppressed_max, (
            f"advisory_suppressed_density_per_sec={out['advisory_suppressed_density_per_sec']} > {suppressed_max}"
        )

    # Soft 护栏：仅用 total 口径；cache_hit_rate_sampled 不参与门禁
    if out.get("cache_hit_rate") is not None and out["cache_hit_rate"] < cache_hit_total_min:
        warnings.warn(
            f"cache_hit_rate(total)={out['cache_hit_rate']} < {cache_hit_total_min}，建议检查 advisory key 稳定性",
            UserWarning,
            stacklevel=2,
        )
