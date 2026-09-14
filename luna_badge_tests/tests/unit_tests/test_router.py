from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_router")
"""
Router 完整测试脚本

测试 L1、L2 和 Router 的完整功能
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

from core.tracking import TrackingSystem, EventType
from core.qwen_loader import QwenModelLoader
from core.model_router import ModelRouter
from core.error_codes import ErrorCode

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_l1():
    """测试 L1 模型"""
    log.info("\n" + "=" * 60)
    log.info("测试 1: L1 模型推理")
    log.info("=" * 60")

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_l1")

        # 加载 L1
        loader = QwenModelLoader(tracking=tracking)
        log.info("\n📦 正在加载 L1 模型...")
        if not loader.load_l1(model_size="0.5B"):
            log.info("❌ L1 模型加载失败")
            return False

        # 获取 L1 调用函数
        l1_model = loader.get_l1_callable()
        if l1_model is None:
            log.info("❌ 无法获取 L1 模型调用函数")
            return False

        # 测试推理
        test_input = "左转"
        log.info(f"\n📝 输入: {test_input}")

        import time
        start_time = time.time()
        result = l1_model(test_input)
        latency_ms = (time.time() - start_time) * 1000

        log.info(f"✅ L1 推理成功")
        log.info(f"   意图: {result.get('intent', 'N/A')}")
        log.info(f"   置信度: {result.get('confidence', 'N/A')}")
        response_text = result.get('text', 'N/A')
        log.info(f"   响应: {response_text[:100] if len(response_text) > 100 else response_text}")
        log.info(f"   延迟: {latency_ms:.2f}ms")

        # 记录埋点
        tracking.track_inference(
            model="L1",
            user_input=test_input,
            response=response_text,
            latency_ms=latency_ms,
            success=True,
        )
        tracking.flush()

        return True

    except Exception as e:
        log.info(f"❌ L1 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_l2():
    """测试 L2 模型"""
    log.info("\n" + "=" * 60)
    log.info("测试 2: L2 模型推理")
    log.info("=" * 60")

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_l2")

        # 加载 L2
        loader = QwenModelLoader(tracking=tracking)
        log.info("\n📦 正在加载 L2 模型...")
        if not loader.load_l2(model_size="3B"):
            log.info("❌ L2 模型加载失败")
            return False

        # 获取 L2 调用函数
        l2_model = loader.get_l2_callable()
        if l2_model is None:
            log.info("❌ 无法获取 L2 模型调用函数")
            return False

        # 测试推理
        test_input = "我想去医院挂号"
        log.info(f"\n📝 输入: {test_input}")

        import time
        start_time = time.time()
        result = l2_model(test_input)
        latency_ms = (time.time() - start_time) * 1000

        log.info(f"✅ L2 推理成功")
        response_text = result.get('text', 'N/A')
        log.info(f"   响应: {response_text[:200] if len(response_text) > 200 else response_text}")
        log.info(f"   延迟: {latency_ms:.2f}ms")

        # 记录埋点
        tracking.track_inference(
            model="L2",
            user_input=test_input,
            response=response_text,
            latency_ms=latency_ms,
            success=True,
        )
        tracking.flush()

        return True

    except Exception as e:
        log.info(f"❌ L2 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_router():
    """测试 Router"""
    log.info("\n" + "=" * 60)
    log.info("测试 3: Router 路由决策")
    log.info("=" * 60")

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_router")

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
                "expected_model": "L1",
            },
            {
                "name": "复杂语义",
                "text": "先去711再去医院",
                "context": {},
                "expected_model": "L2",
            },
            {
                "name": "危险场景",
                "text": "停下",
                "context": {"critical_flag": True},
                "expected_model": "L1",
            },
        ]

        results = []
        for i, test_case in enumerate(test_cases, 1):
            log.info(f"\n--- 测试案例 {i}: {test_case['name']} ---")
            log.info(f"输入: {test_case['text']}")

            import time
            start_time = time.time()
            result = router.route(
                text=test_case['text'],
                context=test_case['context'],
            )
            latency_ms = (time.time() - start_time) * 1000

            selected_model = result.get('model', 'UNKNOWN')
            reason = result.get('reason', 'N/A')
            response_data = result.get('response', {})
            if isinstance(response_data, dict):
                response_text = response_data.get('text', 'N/A')
            else:
                response_text = str(response_data)[:150]

            log.info(f"✅ Router 决策完成")
            log.info(f"   选用模型: {selected_model}")
            log.info(f"   路由原因: {reason}")
            log.info(f"   响应: {response_text[:150] if len(str(response_text)) > 150 else response_text}")
            log.info(f"   总延迟: {latency_ms:.2f}ms")

            results.append({
                "test": test_case['name'],
                "model": selected_model,
                "expected": test_case['expected_model'],
                "match": selected_model == test_case['expected_model'],
                "latency_ms": latency_ms,
            })

        # 刷新埋点
        tracking.flush()

        # 打印总结
        log.info("\n" + "=" * 60)
        log.info("Router 测试总结")
        log.info("=" * 60")
        for r in results:
            status = "✅" if r['match'] else "❌"
            log.info(f"{status} {r['test']}: {r['model']} (期望: {r['expected']}, 延迟: {r['latency_ms']:.2f}ms)")

        return all(r['match'] for r in results)

    except Exception as e:
        log.info(f"❌ Router 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_logs():
    """检查日志文件"""
    log.info("\n" + "=" * 60)
    log.info("检查日志文件")
    log.info("=" * 60")

    log_dirs = [
        "logs",
        "logs/tracking",
    ]

    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            files = [f for f in os.listdir(log_dir) if f.endswith(('.log', '.jsonl', '.json'))]
            log.info(f"✅ {log_dir}: {len(files)} 个文件")
            for f in files[:5]:  # 只显示前5个
                filepath = os.path.join(log_dir, f)
                size = os.path.getsize(filepath)
                log.info(f"   - {f} ({size} bytes)")
        else:
            log.info(f"⚠️ {log_dir}: 目录不存在")


def main():
    """主函数"""
    log.info("🚀 开始 Router 完整测试")
    log.info("=" * 60")

    # 设置日志目录
    setup_logging()

    # 运行测试
    results = []

    # 测试 L1
    results.append(("L1 模型", test_l1()))

    # 测试 L2
    results.append(("L2 模型", test_l2()))

    # 测试 Router
    results.append(("Router", test_router()))

    # 检查日志
    check_logs()

    # 总结
    log.info("\n" + "=" * 60)
    log.info("📊 测试总结")
    log.info("=" * 60")
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        log.info(f"{status}: {name}")

    all_passed = all(result[1] for result in results)
    if all_passed:
        log.info("\n🎉 所有测试通过！")
        return 0
    else:
        log.info("\n⚠️ 部分测试失败，请检查日志")
        return 1


if __name__ == "__main__":
    sys.exit(main())









