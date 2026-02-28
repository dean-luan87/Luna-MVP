from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_nav_decision")
"""
Navigation Decision 测试脚本（F7）

测试导航策略决策模块
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

try:
    import cv2
    import numpy as np
except ImportError:
    log.info("❌ OpenCV 或 NumPy 未安装")
    sys.exit(1)

from vision.nav_decision import Navigator
from vision.path_detector import PathDetector
from vision.hazard_detector import HazardDetector

logger = logging.getLogger(__name__)


def create_test_walkable_grids():
    """创建各种测试场景的可走路径网格"""
    scenarios = {
        "forward": np.array([
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ]),
        "slight_right": np.array([
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 1, 1, 1],
        ]),
        "slight_left": np.array([
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
        ]),
        "hard_right": np.array([
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
        ]),
        "hard_left": np.array([
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0],
        ]),
        "narrow": np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
        ]),
        "blocked": np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]),
        "partial_blocked": np.array([
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
        ]),
    }
    return scenarios


def test_nav_decision():
    """测试导航决策器"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Decision 测试")
    log.info("=" * 80")

    try:
        # 创建导航决策器
        log.info("\n📦 正在初始化 Navigator...")
        navigator = Navigator()
        log.info("✅ Navigator 初始化成功")

        # 创建测试场景
        log.info("\n📋 创建测试场景...")
        scenarios = create_test_walkable_grids()

        # 测试各种场景
        log.info("\n🔍 测试各种导航场景:\n")

        for scenario_name, walkable_grid in scenarios.items():
            # 创建对应的分数（可选）
            walkable_scores = walkable_grid.astype(np.float32)

            # 创建风险地图（模拟）
            risk_map = np.zeros_like(walkable_grid, dtype=np.float32)

            # 生成决策
            result = navigator.decide(
                walkable_grid=walkable_grid,
                walkable_scores=walkable_scores,
                risk_map=risk_map
            )

            # 打印结果
            log.info(f"📌 场景: {scenario_name.upper()}")
            log.info(f"   可走路径网格:")
            for i, row in enumerate(walkable_grid):
                row_str = " ".join(["✅" if cell else "❌" for cell in row])
                log.info(f"     行 {i}: {row_str}")
            log.info(f"   决策: {result['decision']}")
            log.info(f"   偏移: {result['offset']:.2f}")
            log.info(f"   最佳列: {result['best_column']}")
            log.info(f"   可走空间分数: {result['free_space_score']:.2f}")
            log.info(f"   阻挡程度: {result['blockage_level']}")
            log.info(f"   窄道: {'是' if result['is_narrow'] else '否'}")
            log.info(f"   消息: {result['message']}")
            log.info("")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nav_decision_with_hazard():
    """测试导航决策器（带危险检测）"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Decision 测试（带 F4 危险检测）")
    log.info("=" * 80")

    try:
        # 创建检测器
        log.info("\n📦 正在初始化检测器...")
        hazard_detector = HazardDetector()
        path_detector = PathDetector(hazard_detector=hazard_detector)
        navigator = Navigator()
        log.info("✅ 检测器初始化成功")

        # 创建测试图像
        log.info("\n🖼️ 创建测试图像...")
        height, width = 1080, 1920
        test_image = np.ones((height, width, 3), dtype=np.uint8) * 128

        # 添加一些障碍
        cv2.rectangle(test_image, (50, 100), (300, 800), (50, 50, 50), -1)
        cv2.rectangle(test_image, (width - 300, 100), (width - 50, 800), (50, 50, 50), -1)

        # 处理图像
        log.info("\n🔍 正在处理图像...")
        walkable_grid, walkable_scores = path_detector.process(test_image)
        risk_map = hazard_detector.compute_risk(test_image)

        # 生成导航决策
        log.info("\n🚦 生成导航决策...")
        result = navigator.decide(
            walkable_grid=walkable_grid,
            walkable_scores=walkable_scores,
            risk_map=risk_map
        )

        # 打印结果
        log.info(f"\n📊 导航决策结果:")
        log.info(f"   决策: {result['decision']}")
        log.info(f"   偏移: {result['offset']:.2f}")
        log.info(f"   最佳列: {result['best_column']}")
        log.info(f"   可走空间分数: {result['free_space_score']:.2f}")
        log.info(f"   阻挡程度: {result['blockage_level']}")
        log.info(f"   窄道: {'是' if result['is_narrow'] else '否'}")
        log.info(f"   消息: {result['message']}")

        log.info(f"\n   列分数: {result['column_score']}")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nav_decision_smoothing():
    """测试导航决策平滑"""
    log.info("\n" + "=" * 80)
    log.info("🧪 Navigation Decision 平滑测试")
    log.info("=" * 80")

    try:
        navigator = Navigator()

        # 模拟快速变化的场景（可能导致抖动）
        log.info("\n📋 测试平滑效果（模拟快速变化）:\n")

        scenarios = [
            ("left", np.array([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]])),
            ("center", np.array([[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0]])),
            ("right", np.array([[0, 0, 0, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]])),
            ("center", np.array([[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0]])),
            ("left", np.array([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]])),
        ]

        log.info("帧 | 场景  | 原始偏移 | 平滑偏移 | 决策")
        log.info("-" * 60")

        for i, (scene_name, grid) in enumerate(scenarios):
            result = navigator.decide(walkable_grid=grid)
            log.info(f"{i+1:2d} | {scene_name:6s} | {result['offset']:8.2f} | {result['offset']:8.2f} | {result['decision']}")

        log.info("\n✅ 平滑测试完成（注意平滑后的偏移量变化更平稳）")

        return True

    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    log.info("🚀 Navigation Decision 测试开始")
    log.info("=" * 80")

    try:
        # 1. 基础功能测试
        success1 = test_nav_decision()

        if not success1:
            log.info("\n❌ 基础功能测试失败")
            return 1

        # 2. 带危险检测测试
        success2 = test_nav_decision_with_hazard()

        if not success2:
            log.info("\n❌ 带危险检测测试失败")
            return 1

        # 3. 平滑测试
        success3 = test_nav_decision_smoothing()

        if not success3:
            log.info("\n❌ 平滑测试失败")
            return 1

        log.info(f"\n{'='*80}")
        log.info("🎉 所有测试完成！")
        log.info(f"{'='*80}")
        log.info("\n💡 提示:")
        log.info("   - 修改 vision/nav_decision/nav_config.py 可以调整参数")
        log.info("   - 决策类型: FORWARD, SLIGHT_LEFT, SLIGHT_RIGHT, HARD_LEFT, HARD_RIGHT, STOP")
        log.info("   - 多帧平滑可以避免导航指令抖动")

        return 0

    except KeyboardInterrupt:
        log.info("\n\n👋 用户中断")
        return 0
    except Exception as e:
        log.info(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())













