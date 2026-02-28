from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_config")
"""
配置系统测试脚本（E5）

测试配置加载和引擎使用配置
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

from core.config import CONFIG, Config
from core.luna_engine import LunaEngine

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)
    log.info("✅ 日志目录已创建")


def test_config_loading():
    """测试配置加载"""
    log.info("\n" + "=" * 80)
    log.info("🧪 配置加载测试")
    log.info("=" * 80")

    # 打印配置信息
    log.info(f"\n📋 当前配置:")
    log.info(f"   环境: {CONFIG.env}")
    log.info(f"   模型配置:")
    log.info(f"     L1 模型: {CONFIG.models.get('l1_model_name', 'N/A')}")
    log.info(f"     L2 模型: {CONFIG.models.get('l2_model_name', 'N/A')}")
    log.info(f"     启用 L1: {CONFIG.models.get('enable_l1', False)}")
    log.info(f"     启用 L2: {CONFIG.models.get('enable_l2', False)}")
    log.info(f"   功能开关:")
    log.info(f"     启用 TaskChain: {CONFIG.features.get('enable_task_chain', False)}")
    log.info(f"     启用 Replay: {CONFIG.features.get('enable_replay', False)}")
    log.info(f"   日志配置:")
    log.info(f"     日志等级: {CONFIG.logging.get('level', 'N/A')}")
    log.debug(f"     Trace 文件: {CONFIG.logging.get('trace_log_file', 'N/A')}")
    log.debug(f"     采样率: {CONFIG.logging.get('trace_sampling_rate', 1.0)}")

    # 测试路径访问
    log.info(f"\n📝 路径访问测试:")
    log.info(f"   logging.level = {CONFIG.get('logging.level', 'N/A')}")
    log.info(f"   models.enable_l1 = {CONFIG.get('models.enable_l1', False)}")

    return True


def test_engine_with_config():
    """测试引擎使用配置"""
    log.info("\n" + "=" * 80)
    log.info("🧪 引擎使用配置测试")
    log.info("=" * 80")

    try:
        # 初始化引擎（使用配置）
        log.info("\n📦 正在初始化 Luna Engine（使用配置）...")
        engine = LunaEngine(auto_load=True)

        log.info("✅ Luna Engine 初始化成功")

        # 测试调用
        log.info("\n🔄 测试引擎调用...")
        result = engine.handle_user_input(
            user_text="测试一下配置",
            sensors_context={
                "scene_type": "street",
                "critical_flag": False,
                "vision_alert": False,
                "task_state": "navigating",
            }
        )

        log.info(f"\n✅ 引擎调用成功")
        log.info(f"   输出文本: {result.get('output_text', 'N/A')}")
        log.info(f"   使用模型: {result.get('model', 'N/A')}")
        log.info(f"   意图: {result.get('intent', 'N/A')}")
        log.debug(f"   Trace ID: {result.get('trace_id', 'N/A')}")

        # 检查 TaskChain 状态
        if result.get('chain_snapshot'):
            log.info(f"   ✅ TaskChain 已启用")
        else:
            log.info(f"   ⚠️ TaskChain 未启用或为空")

        return True

    except Exception as e:
        log.info(f"\n❌ 引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 配置系统测试开始")
    log.info("=" * 80")

    # 设置日志目录
    setup_logging()

    try:
        # 1. 测试配置加载
        config_ok = test_config_loading()

        if not config_ok:
            log.info("\n❌ 配置加载测试失败")
            return 1

        # 2. 测试引擎使用配置
        engine_ok = test_engine_with_config()

        if not engine_ok:
            log.info("\n❌ 引擎测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 修改配置: config/luna_config.json")
        log.error("   - 日志等级控制: 修改 logging.level (DEBUG/INFO/WARN/ERROR)")
        log.debug("   - 采样率控制: 修改 logging.trace_sampling_rate (0.0-1.0)")
        log.info("   - 功能开关: 修改 features.enable_task_chain 等")

        return 0

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())









