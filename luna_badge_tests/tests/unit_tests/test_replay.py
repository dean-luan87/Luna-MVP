from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_replay")
"""
Router 全链路追踪测试脚本（E2）

测试 Router 的 trace_id 全链路埋点和 ReplayManager 回放功能
"""

import sys
import os
import logging
from pathlib import Path

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
from core.replay_manager import ReplayManager

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_router_with_trace():
    """测试 Router 全链路追踪"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Router 全链路追踪测试")
    log.info("=" * 80")

    # 初始化埋点
    tracking = TrackingSystem(log_dir="logs/tracking")
    tracking.start_session("test_replay_session")

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
            "context": {},
        },
        {
            "name": "复杂语义",
            "text": "我要去医院挂号",
            "context": {},
        },
        {
            "name": "多步骤意图",
            "text": "先去711再去医院",
            "context": {},
        },
    ]

    trace_ids = []

    for i, test_case in enumerate(test_cases, 1):
        log.info(f"\n{'='*80}")
        log.info(f"测试 {i}/{len(test_cases)}: {test_case['name']}")
        log.info(f"{'='*80}")
        log.info(f"输入: {test_case['text']}")

        import time
        start_time = time.time()
        result = router.route(
            text=test_case['text'],
            context=test_case['context'],
        )
        latency_ms = (time.time() - start_time) * 1000

        # 提取 trace_id
        trace_id = result.get('trace_id', 'N/A')
        trace_ids.append(trace_id)

        selected_model = result.get('model', 'UNKNOWN')
        reason = result.get('reason', 'N/A')
        response_data = result.get('response', {})
        if isinstance(response_data, dict):
            response_text = response_data.get('text', 'N/A')
        else:
            response_text = str(response_data)[:200] if response_data else 'N/A'

        log.info(f"\n✅ Router 决策完成")
        log.debug(f"   Trace ID: {trace_id}")
        log.info(f"   选用模型: {selected_model}")
        log.info(f"   路由原因: {reason}")
        log.info(f"   响应: {response_text[:150]}...")
        log.info(f"   总延迟: {latency_ms:.2f}ms")

    # 刷新埋点
    tracking.flush()

    log.info(f"\n{'='*80}")
    log.info("📊 测试总结")
    log.info(f"{'='*80}")
    log.debug(f"总共生成 {len(trace_ids)} 个 trace_id:")
    for i, tid in enumerate(trace_ids, 1):
        log.info(f"  {i}. {tid}")

    return trace_ids


def test_replay_manager(trace_ids: List[str]):
    """测试 ReplayManager 回放功能"""
    log.info(f"\n{'='*80}")
    log.info("🔍 ReplayManager 回放测试")
    log.info(f"{'='*80}")

    if not trace_ids:
        log.debug("⚠️ 没有 trace_id 可回放")
        return

    # 使用第一个 trace_id 进行演示
    trace_id = trace_ids[0]
    log.debug(f"\n📋 回放 trace_id: {trace_id}")

    # 加载 trace
    events = ReplayManager.load_trace(trace_id)

    if not events:
        log.debug(f"❌ 未找到 trace_id={trace_id} 的事件")
        log.debug(f"   请检查 logs/trace_events.log 文件是否存在且包含该 trace_id")
        return

    log.info(f"✅ 成功加载 {len(events)} 个事件")

    # 打印 trace 链路
    ReplayManager.print_trace(events)

    # 如果有多个 trace_id，也演示其他
    if len(trace_ids) > 1:
        log.info(f"\n{'='*80}")
        log.debug("📋 回放其他 trace_id（简要）")
        log.info(f"{'='*80}")

        for i, tid in enumerate(trace_ids[1:], 2):
            events = ReplayManager.load_trace(tid)
            if events:
                log.debug(f"\n[{i}] trace_id: {tid} ({len(events)} 个事件)")
                # 只显示关键事件
                for event in events:
                    phase = event.get("phase", "unknown")
                    event_name = event.get("event", "unknown")
                    log.info(f"    - {phase}.{event_name}")


def check_trace_file():
    """检查 trace_events.log 文件"""
    log.info(f"\n{'='*80}")
    log.debug("📁 检查 trace_events.log 文件")
    log.info(f"{'='*80}")

    trace_file = "logs/trace_events.log"

    if not os.path.exists(trace_file):
        log.debug(f"⚠️ 文件不存在: {trace_file}")
        return

    # 统计文件信息
    file_size = os.path.getsize(trace_file)
    log.debug(f"✅ 文件存在: {trace_file}")
    log.info(f"   文件大小: {file_size} bytes")

    # 统计事件数量
    event_count = 0
    unique_trace_ids = set()

    try:
        import json
        with open(trace_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event_data = json.loads(line)
                    event_count += 1

                    # 提取 trace_id
                    trace_id = None
                    if "trace_id" in event_data:
                        trace_id = event_data["trace_id"]
                    elif "payload" in event_data and isinstance(event_data["payload"], dict):
                        trace_id = event_data["payload"].get("trace_id")

                    if trace_id:
                        unique_trace_ids.add(trace_id)

                except json.JSONDecodeError:
                    continue

        log.info(f"   总事件数: {event_count}")
        log.debug(f"   唯一 trace_id 数: {len(unique_trace_ids)}")

        if unique_trace_ids:
            log.debug(f"\n   Trace IDs:")
            for tid in sorted(list(unique_trace_ids))[:10]:  # 只显示前10个
                log.info(f"     - {tid}")
            if len(unique_trace_ids) > 10:
                log.debug(f"     ... 还有 {len(unique_trace_ids) - 10} 个")

    except Exception as e:
        log.info(f"❌ 读取文件失败: {e}")


def main():
    """主函数"""
    log.info("🚀 Router 全链路追踪测试开始")
    log.info("=" * 80")

    # 设置日志目录
    setup_logging()

    try:
        # 1. 测试 Router（生成 trace）
        trace_ids = test_router_with_trace()

        # 2. 检查 trace_events.log 文件
        check_trace_file()

        # 3. 测试 ReplayManager
        test_replay_manager(trace_ids)

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.debug("   - 查看完整 trace: python -c \"from core.replay_manager import ReplayManager; events = ReplayManager.load_trace('YOUR_TRACE_ID'); ReplayManager.print_trace(events)\")
        log.debug("   - trace_events.log 位置: logs/trace_events.log")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())









