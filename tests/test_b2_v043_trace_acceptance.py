#!/usr/bin/env python3
"""
B2 v0.4.3 Trace 验收脚本（Architecture + Gate + DCS）

目标：
任何一条 trace，只要越权 / 失控 / 不透明，CI 直接报错
"""

import json
import sys
from pathlib import Path

TRACE_PATH = Path("traces/b2_gate_trace_v042.jsonl")

def load_traces(path):
    """加载 trace 文件（JSONL 格式）"""
    if not path.exists():
        print(f"⚠️ Trace 文件不存在: {path}")
        return []
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON 解析错误: {e}")
                continue

def assert_true(cond, msg):
    """断言，失败时抛出异常"""
    if not cond:
        raise AssertionError(msg)

def main():
    print("================================================")
    print("B2 v0.4.3 Trace 验收测试")
    print("================================================")
    print(f"Trace 文件: {TRACE_PATH}")
    print()

    traces = list(load_traces(TRACE_PATH))
    assert_true(len(traces) > 0, "❌ trace 为空")

    errors = []
    warnings = []

    for i, tr in enumerate(traces):
        gate_mode = tr.get("gate_mode")
        gate = tr.get("gate", {})
        view_state = tr.get("view_state", {})

        # 1️⃣ Gate 必须存在
        if gate_mode not in ("ACTIVE", "READ_ONLY", "SUSPENDED"):
            errors.append(f"[{i}] ❌ 非法 gate_mode: {gate_mode}")

        # 2️⃣ SUSPENDED 必须有 blocked_by
        if gate_mode == "SUSPENDED":
            if gate.get("blocked_by") is None:
                errors.append(f"[{i}] ❌ SUSPENDED 但没有 blocked_by")

        # 3️⃣ READ_ONLY / SUSPENDED 不允许输出决策（这里只看 trace 级别）
        # summary 不应该存在于 gate trace
        if "impact" in tr:
            errors.append(f"[{i}] ❌ Gate trace 中不应包含 impact（越权）")

        # 4️⃣ view_state 缺失必须被记录
        if not view_state or not view_state.get("stability_score"):
            if gate_mode == "ACTIVE":
                errors.append(f"[{i}] ❌ 缺少 view_state 但 Gate 仍为 ACTIVE（违反 v0.4.2 规则）")
            elif gate.get("blocked_by") not in ("missing_view_state", None):
                warnings.append(f"[{i}] ⚠️ 缺少 view_state 但 Gate 未明确感知")

        # 5️⃣ Gate trace 必须包含必要字段
        if "ts" not in tr:
            errors.append(f"[{i}] ❌ 缺少 ts 字段")
        if "frame_id" not in tr:
            warnings.append(f"[{i}] ⚠️ 缺少 frame_id 字段")

    # 输出结果
    print(f"检查了 {len(traces)} 条 trace")
    print()

    if warnings:
        print(f"⚠️ Warnings ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  {w}")
        if len(warnings) > 10:
            print(f"  ... 还有 {len(warnings) - 10} 条警告")
        print()

    if errors:
        print(f"❌ Errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        print()
        print("❌ Trace 架构验收失败")
        sys.exit(1)
    else:
        print("✅ Trace 架构验收通过")
        if warnings:
            print(f"⚠️ 但有 {len(warnings)} 条警告（不影响通过）")
        sys.exit(0)

if __name__ == "__main__":
    main()
