from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_task_chain")
"""
Task Chain 测试脚本（E3）

测试 Router × TaskChain 集成功能
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

from core.tracking import TrackingSystem
from core.model_router import ModelRouter
from core.task_chain_manager import TaskChainManager

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_router_with_task_chain():
    """测试 Router 与 TaskChain 集成"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Router × TaskChain 集成测试")
    log.info("=" * 80")

    # 初始化埋点
    tracking = TrackingSystem(log_dir="logs/tracking")
    tracking.start_session("test_task_chain_session")

    # 创建任务链管理器
    task_manager = TaskChainManager()
    log.info("✅ TaskChainManager 初始化完成")

    # 创建 Router（自动加载模型）
    log.info("\n📦 正在初始化 Router（自动加载模型）...")
    router = ModelRouter(
        auto_load=True,
        tracking=tracking,
        l1_model_size="0.5B",
        l2_model_size="3B",
    )

    # 测试案例
    test_cases = [
        {
            "name": "简单导航",
            "text": "左转",
            "context": {"scene_type": "navigation"},
        },
        {
            "name": "医院任务",
            "text": "我要去医院挂号",
            "context": {"scene_type": "hospital"},
        },
        {
            "name": "多步骤任务",
            "text": "先去711再去医院",
            "context": {"scene_type": "navigation"},
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
        
        # 调用 Router，传入 task_manager
        result = router.route(
            text=test_case['text'],
            context=test_case['context'],
            task_manager=task_manager,  # 传入任务链管理器
        )
        
        latency_ms = (time.time() - start_time) * 1000

        # 提取结果信息
        trace_id = result.get('trace_id', 'N/A')
        selected_model = result.get('model', 'UNKNOWN')
        reason = result.get('reason', 'N/A')
        intent = result.get('intent', 'N/A')
        response_data = result.get('response', {})
        if isinstance(response_data, dict):
            response_text = response_data.get('text', 'N/A')
        else:
            response_text = str(response_data)[:200] if response_data else 'N/A'

        log.info(f"\n✅ Router 决策完成")
        log.debug(f"   Trace ID: {trace_id}")
        log.info(f"   选用模型: {selected_model}")
        log.info(f"   路由原因: {reason}")
        log.info(f"   意图: {intent}")
        log.info(f"   响应: {response_text[:150]}...")
        log.info(f"   总延迟: {latency_ms:.2f}ms")

        # 获取任务链快照
        chain_snapshot = task_manager.get_current_chain_snapshot()
        if chain_snapshot:
            log.info(f"\n📋 任务链状态:")
            log.info(f"   链ID: {chain_snapshot.get('chain_id', 'N/A')}")
            log.info(f"   场景类型: {chain_snapshot.get('scene_type', 'N/A')}")
            log.info(f"   状态: {chain_snapshot.get('status', 'N/A')}")
            log.info(f"   当前索引: {chain_snapshot.get('current_index', 0)}")
            log.info(f"   节点数: {len(chain_snapshot.get('nodes', []))}")
            log.debug(f"   关联 trace_ids: {len(chain_snapshot.get('trace_ids', []))}")
            
            nodes = chain_snapshot.get('nodes', [])
            if nodes:
                log.info(f"\n   节点详情:")
                for j, node in enumerate(nodes, 1):
                    log.info(f"     [{j}] {node.get('node_type', 'N/A')} - {node.get('description', 'N/A')}")
                    log.info(f"         状态: {node.get('status', 'N/A')}")
        else:
            log.info(f"\n⚠️ 当前没有活跃的任务链")

        results.append({
            "test_case": test_case,
            "result": result,
            "chain_snapshot": chain_snapshot,
        })

    # 刷新埋点
    tracking.flush()

    log.info(f"\n{'='*80}")
    log.info("📊 测试总结")
    log.info(f"{'='*80}")
    log.info(f"总共执行 {len(results)} 个测试用例")
    log.info(f"任务链状态: {task_manager.get_current_chain_snapshot() is not None and '是' or '否'}")

    return results


def check_task_chain_events():
    """检查任务链相关的事件日志"""
    log.info(f"\n{'='*80}")
    log.info("📁 检查任务链事件日志")
    log.info(f"{'='*80}")

    trace_file = "logs/trace_events.log"

    if not os.path.exists(trace_file):
        log.debug(f"⚠️ 文件不存在: {trace_file}")
        return

    # 统计任务链事件
    task_chain_events = []

    try:
        with open(trace_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event_data = json.loads(line)
                    if event_data.get("phase") == "task_chain":
                        task_chain_events.append(event_data)
                except json.JSONDecodeError:
                    continue

        log.info(f"✅ 找到 {len(task_chain_events)} 个任务链事件")

        if task_chain_events:
            log.info(f"\n   事件列表:")
            for i, event in enumerate(task_chain_events[-10:], 1):  # 只显示最后10个
                event_name = event.get("event", "unknown")
                chain_id = event.get("payload", {}).get("chain_id", "N/A")
                scene_type = event.get("payload", {}).get("scene_type", "N/A")
                log.info(f"     [{i}] {event_name} - chain_id={chain_id}, scene_type={scene_type}")

    except Exception as e:
        log.info(f"❌ 读取文件失败: {e}")


def main():
    """主函数"""
    log.info("🚀 Router × TaskChain 集成测试开始")
    log.info("=" * 80")

    # 设置日志目录
    setup_logging()

    try:
        # 1. 测试 Router 与 TaskChain 集成
        results = test_router_with_task_chain()

        # 2. 检查任务链事件日志
        check_task_chain_events()

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 查看任务链: task_manager.get_current_chain_snapshot()")
        log.debug("   - 查看事件日志: logs/trace_events.log")
        log.info("   - 过滤任务链事件: phase == 'task_chain")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())









