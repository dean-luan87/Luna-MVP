from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_engine")
"""
Luna Engine 测试脚本（E4）

测试对外统一引擎接口 LunaEngine
"""

import sys
import os
import logging
from pathlib import Path
import json

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

from core.luna_engine import LunaEngine

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_luna_engine():
    """测试 Luna Engine"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Luna Engine 测试")
    log.info("=" * 80")

    # 初始化引擎
    log.info("\n📦 正在初始化 Luna Engine...")
    try:
        engine = LunaEngine(
            auto_load=True,
            l1_model_size="0.5B",
            l2_model_size="3B",
        )
        log.info("✅ Luna Engine 初始化成功")
    except Exception as e:
        log.info(f"❌ Luna Engine 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return None

    # 测试案例
    test_cases = [
        {
            "name": "简单导航",
            "text": "左转",
            "context": {
                "scene_type": "street",
                "critical_flag": False,
                "vision_alert": False,
                "task_state": "navigating",
            },
        },
        {
            "name": "医院任务",
            "text": "我要去医院挂号",
            "context": {
                "scene_type": "hospital",
                "critical_flag": False,
                "vision_alert": False,
                "task_state": "navigating",
            },
        },
        {
            "name": "多步骤任务",
            "text": "先去711再去医院",
            "context": {
                "scene_type": "navigation",
                "critical_flag": False,
                "vision_alert": False,
                "task_state": "navigating",
            },
        },
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        log.info(f"\n{'='*80}")
        log.info(f"测试 {i}/{len(test_cases)}: {test_case['name']}")
        log.info(f"{'='*80}")
        log.info(f"输入: {test_case['text']}")
        log.info(f"场景: {test_case['context'].get('scene_type', 'navigation')}")

        import time
        start_time = time.time()

        # 调用引擎
        result = engine.handle_user_input(
            user_text=test_case['text'],
            sensors_context=test_case['context'],
        )

        latency_ms = (time.time() - start_time) * 1000

        # 打印结果
        log.info(f"\n✅ 引擎处理完成")
        log.info(f"   输出文本: {result.get('output_text', 'N/A')}")
        log.info(f"   使用模型: {result.get('model', 'N/A')}")
        log.info(f"   意图: {result.get('intent', 'N/A')}")
        log.info(f"   路由原因: {result.get('reason', 'N/A')}")
        log.debug(f"   Trace ID: {result.get('trace_id', 'N/A')}")
        log.info(f"   处理延迟: {latency_ms:.2f}ms")

        # 打印任务链信息
        chain_snapshot = result.get('chain_snapshot')
        if chain_snapshot:
            log.info(f"\n   📋 任务链状态:")
            log.info(f"      链ID: {chain_snapshot.get('chain_id', 'N/A')}")
            log.info(f"      场景类型: {chain_snapshot.get('scene_type', 'N/A')}")
            log.info(f"      状态: {chain_snapshot.get('status', 'N/A')}")
            log.info(f"      当前索引: {chain_snapshot.get('current_index', 0)}")
            log.info(f"      节点数: {len(chain_snapshot.get('nodes', []))}")
            log.debug(f"      关联 trace_ids: {len(chain_snapshot.get('trace_ids', []))}")

            nodes = chain_snapshot.get('nodes', [])
            if nodes:
                log.info(f"\n      节点详情:")
                for j, node in enumerate(nodes, 1):
                    log.info(f"        [{j}] {node.get('node_type', 'N/A')} - {node.get('description', 'N/A')}")
                    log.info(f"            状态: {node.get('status', 'N/A')}")
        else:
            log.info(f"\n   ⚠️ 当前没有活跃的任务链")

        results.append({
            "test_case": test_case,
            "result": result,
        })

    return results


def check_engine_events():
    """检查引擎相关的事件日志"""
    log.info(f"\n{'='*80}")
    log.info("📁 检查引擎事件日志")
    log.info(f"{'='*80}")

    trace_file = "logs/trace_events.log"

    if not os.path.exists(trace_file):
        log.debug(f"⚠️ 文件不存在: {trace_file}")
        return

    # 统计各类事件
    event_types = {
        "engine": [],
        "router": [],
        "task_chain": [],
    }

    try:
        with open(trace_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event_data = json.loads(line)
                    phase = event_data.get("phase")
                    if phase in event_types:
                        event_types[phase].append(event_data)
                except json.JSONDecodeError:
                    continue

        log.info(f"✅ 事件统计:")
        for phase, events in event_types.items():
            log.info(f"   {phase}: {len(events)} 个事件")
            if events:
                # 显示最后几个事件
                recent_events = events[-3:]
                for event in recent_events:
                    event_name = event.get("event", "unknown")
                    log.info(f"     - {event_name}")

    except Exception as e:
        log.info(f"❌ 读取文件失败: {e}")


def main():
    """主函数"""
    log.info("🚀 Luna Engine 测试开始")
    log.info("=" * 80")

    # 设置日志目录
    setup_logging()

    try:
        # 1. 测试 Luna Engine
        results = test_luna_engine()

        if results is None:
            log.info("\n❌ 引擎初始化失败，无法继续测试")
            return 1

        # 2. 检查事件日志
        check_engine_events()

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 查看完整结果: result 字典")
        log.info("   - 查看原始数据: result['raw']")
        log.info("   - 查看任务链: result['chain_snapshot']")
        log.debug("   - 查看事件日志: logs/trace_events.log")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())









