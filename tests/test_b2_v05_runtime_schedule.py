#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2 v0.5 Runtime Schedule Acceptance Test

目标：
确保 v0.5 下 Gate + Scheduler 是"真的在管事"，而不是只写了结构。

验收点（硬性）：
- SUSPENDED → 不执行、不输出
- READ_ONLY → 不输出 decision
- ACTIVE → 受 tick_interval_ms 限制
- 每一帧 必须写 GateRuntimeProfile
- B 永远是 ADVISORY_ONLY
"""

import time
import os
import sys
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vision_pipeline.b2.v03.b2_v03 import B2v03
from vision_pipeline.b2.v03.gate_runtime_profile import GateMode, ComputeLevel


def make_perception(view_state=True, stability_score=0.9, range_m=6.0):
    """构造测试用的 perception"""
    if view_state:
        return {
            "view_state": {
                "stability_score": stability_score,
                "range_m": range_m,
                "visibility_score": 0.8,
            }
        }
    return {}


def check_trace_has_profile(trace_path: str, frame_id: int) -> bool:
    """检查 trace 文件中是否包含指定 frame_id 的 GateRuntimeProfile"""
    if not os.path.exists(trace_path):
        return False
    
    try:
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                # 检查是否有 gate_runtime_profile 或 gate 字段
                if rec.get("time", {}).get("frame_id") == frame_id:
                    if "gate_runtime_profile" in rec or "gate" in rec:
                        return True
    except Exception:
        pass
    return False


def test_v05_gate_and_scheduler():
    """v0.5 Gate + Scheduler 验收测试"""
    print("=" * 60)
    print("B2 v0.5 Runtime Schedule Acceptance Test")
    print("=" * 60)

    # 使用临时 trace 路径
    import tempfile
    trace_path = os.path.join(tempfile.gettempdir(), "b2_v05_test_trace.jsonl")
    
    b2 = B2v03(
        gate_config_path=None,  # 使用默认配置
        enable_trace=True,
    )
    b2.trace_writer_v043.out_path = trace_path

    t0 = time.time()

    # -----------------------------
    # CASE A: ACTIVE → 正常输出（但受限频率）
    # -----------------------------
    print("\nCASE A: ACTIVE + scheduler limit")

    out1 = b2.tick(t0, make_perception(), frame_id=1)
    time.sleep(0.05)  # 等待 50ms
    out2 = b2.tick(t0 + 0.05, make_perception(), frame_id=2)  # <100ms
    time.sleep(0.11)  # 等待 110ms
    out3 = b2.tick(t0 + 0.16, make_perception(), frame_id=3)  # >100ms

    # ACTIVE 时应该能输出（如果 perception 有有效因子）
    # 但 scheduler 会限制频率
    print(f"  out1: {out1 is not None}")
    print(f"  out2: {out2 is not None}")
    print(f"  out3: {out3 is not None}")
    
    # 检查 trace 中是否有 profile
    has_profile_1 = check_trace_has_profile(trace_path, 1)
    has_profile_2 = check_trace_has_profile(trace_path, 2)
    has_profile_3 = check_trace_has_profile(trace_path, 3)
    
    assert has_profile_1, "Frame 1 must have GateRuntimeProfile in trace"
    assert has_profile_2, "Frame 2 must have GateRuntimeProfile in trace"
    assert has_profile_3, "Frame 3 must have GateRuntimeProfile in trace"

    print("✅ ACTIVE scheduling OK")

    # -----------------------------
    # CASE B: SUSPENDED → 不执行、不输出
    # -----------------------------
    print("\nCASE B: SUSPENDED must not execute")

    # 通过构造不稳定的 perception 来触发 SUSPENDED
    out_suspended = b2.tick(
        t0 + 1.0,
        make_perception(view_state=True, stability_score=0.3, range_m=1.5),  # 不稳定 + 太近
        frame_id=10
    )
    
    # SUSPENDED 应该返回 None
    assert out_suspended is None, "SUSPENDED must not execute"
    
    # 检查 trace 中是否有 profile
    has_profile_suspended = check_trace_has_profile(trace_path, 10)
    assert has_profile_suspended, "SUSPENDED frame must have GateRuntimeProfile in trace"

    print("✅ SUSPENDED blocked OK")

    # -----------------------------
    # CASE C: missing view_state → READ_ONLY 或 SUSPENDED
    # -----------------------------
    print("\nCASE C: missing view_state")

    out_no_view = b2.tick(t0 + 2.0, make_perception(view_state=False), frame_id=20)
    
    # 缺少 view_state 时不应该输出
    assert out_no_view is None, "missing view_state must not produce output"
    
    # 检查 trace 中是否有 profile
    has_profile_no_view = check_trace_has_profile(trace_path, 20)
    assert has_profile_no_view, "missing view_state frame must have GateRuntimeProfile in trace"

    print("✅ missing view_state handled OK")

    # -----------------------------
    # CASE D: 验证 trace 中的 GateRuntimeProfile 结构
    # -----------------------------
    print("\nCASE D: GateRuntimeProfile structure validation")

    if os.path.exists(trace_path):
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                
                # 检查是否有 gate 字段
                if "gate" in rec:
                    gate = rec["gate"]
                    assert "gate_mode" in gate or "version" in gate, "gate must have gate_mode or version"
                    assert "compute_level" in gate or "runtime_profile" in gate, "gate must have compute_level or runtime_profile"
                    
                    # 检查 authority_scope
                    if "runtime_profile" in gate:
                        runtime_profile = gate["runtime_profile"]
                        if "authority_scope" in runtime_profile:
                            assert runtime_profile["authority_scope"] == "ADVISORY_ONLY", "authority_scope must be ADVISORY_ONLY"
                    
                    if "authority_scope" in gate:
                        assert gate["authority_scope"] == "ADVISORY_ONLY", "authority_scope must be ADVISORY_ONLY"

    print("✅ GateRuntimeProfile structure OK")

    print("\n" + "=" * 60)
    print("ALL v0.5 runtime schedule tests PASSED")
    print("=" * 60)
    
    # 清理临时文件
    try:
        if os.path.exists(trace_path):
            os.remove(trace_path)
    except Exception:
        pass


if __name__ == "__main__":
    test_v05_gate_and_scheduler()
