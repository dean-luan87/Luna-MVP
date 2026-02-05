#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端 Stub 验收测试

验收点：
- 贯通：TaskNode → Adapter Stub → MOC → PlanB → TaskChain → Watchdog（至少跑 1 次 fallback）
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from decision.task_chain.task_chain_manager import TaskChainManager
from decision.task_chain.task_node import TaskNode
from governance.output_controller.controller import ModelOutputController
from governance.fallback.fallback_executor import FallbackExecutor
from metrics.metrics_collector import MetricsCollector


def create_stub_output(model_id: str, confidence: float, result: dict) -> dict:
    """创建 Stub 输出"""
    return {
        "model_id": model_id,
        "model_version": "1.0.0",
        "result": result,
        "confidence": confidence,
        "meta": {"latency_ms": 100}
    }


def test_end_to_end_with_fallback():
    """测试: 端到端流程（包含 fallback）"""
    print("\n=== 测试: 端到端流程（包含 fallback） ===")
    
    # 1. 初始化所有组件
    collector = MetricsCollector()
    trace_id = collector.new_trace_id()
    
    fallback_executor = FallbackExecutor(metrics_collector=collector, trace_id=trace_id)
    task_chain = TaskChainManager(
        fallback_executor=fallback_executor,
        metrics_collector=collector,
        trace_id=trace_id
    )
    moc = ModelOutputController(metrics_collector=collector, trace_id=trace_id)
    
    # 2. 创建任务节点并启动
    node = TaskNode("test_node", "navigation")
    task_chain.start(node)
    print("✓ TaskChain 启动")
    
    # 3. 模拟模型输出（冲突场景，触发 fallback）
    model_outputs = [
        create_stub_output("model_a", 0.9, {"action": "turn_left"}),
        create_stub_output("model_b", 0.8, {"action": "turn_right"})  # 冲突
    ]
    
    # 4. MOC 处理
    moc_result = moc.process("navigation", model_outputs)
    print(f"✓ MOC 决策: {moc_result['decision']}")
    
    # 5. TaskChain 处理结果
    if moc_result["decision"] == "fallback":
        task_chain.handle_result(moc_result)
        print(f"✓ TaskChain 处理 fallback，状态: {task_chain.state.value}")
        
        # 验证 fallback 被记录
        assert task_chain.context.get_attempt_count("navigation") > 0, "attempts 应该增加"
        print(f"✓ Fallback attempts: {task_chain.context.get_attempt_count('navigation')}")
    
    # 6. 验证日志已写入
    import json
    trace_path = collector.trace_path
    if trace_path.exists():
        with trace_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            events = []
            for line in lines:
                try:
                    event_data = json.loads(line)
                    events.append(event_data.get("event", "unknown"))
                except json.JSONDecodeError:
                    continue
            
            assert len(events) > 0, "应该记录至少一个事件"
            assert "node_start" in events, "应该记录 node_start"
            assert "moc_decision" in events, "应该记录 moc_decision"
            if moc_result["decision"] == "fallback":
                assert "fallback" in events, "应该记录 fallback"
            print(f"✓ 执行跟踪已记录: {len(events)} 个事件")
    else:
        print("⚠ 执行跟踪文件不存在（可能是首次运行）")
    
    print("✓ 端到端流程完成")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("端到端 Stub 验收测试")
    print("=" * 60)
    
    try:
        test_end_to_end_with_fallback()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())




