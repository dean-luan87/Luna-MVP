from core.logging import get_logger

log = get_logger("test_frame_scheduler")
"""
测试 B 模块：FrameScheduler

用法：
    python3 tests/test_frame_scheduler.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision.frame_scheduler import FrameScheduler


def test_basic_functionality():
    """测试基本功能"""
    log.info("=" * 60")
    log.info("测试 B 模块：FrameScheduler - 基本功能")
    log.info("=" * 60")
    
    scheduler = FrameScheduler()
    
    # 测试用例：(scene_complexity, motion_speed, brightness, expected_range)
    test_cases = [
        (0.0, 0.0, 0.8, "低复杂度+静止+明亮", (2, 8)),
        (1.0, 1.0, 0.2, "高复杂度+快速+黑暗", (10, 15)),
        (0.5, 0.5, 0.5, "中等环境", (6, 12)),
        (0.2, 0.1, 0.9, "简单环境+慢速+明亮", (2, 8)),
        (0.8, 0.9, 0.3, "复杂环境+快速+较暗", (12, 15)),
    ]
    
    log.info("\n【测试用例】")
    log.info("-" * 60")
    
    for sc, ms, br, desc, expected_range in test_cases:
        fps = scheduler.suggest_fps(sc, ms, br)
        min_expected, max_expected = expected_range
        status = "✅" if min_expected <= fps <= max_expected else "⚠️"
        
        log.info(f"\n{status} 场景: {desc}")
        log.info(f"  输入: 复杂度={sc:.2f}, 速度={ms:.2f}, 亮度={br:.2f}")
        log.info(f"  输出: FPS={fps} (期望范围: {min_expected}~{max_expected})")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 基本功能测试完成")
    log.info("=" * 60")


def test_smoothing():
    """测试平滑机制"""
    log.info("\n" + "=" * 60)
    log.info("测试平滑机制（避免频繁跳变）")
    log.info("=" * 60")
    
    scheduler = FrameScheduler(smoothing_alpha=0.5)
    
    # 模拟场景突然变化
    log.info("\n模拟场景从简单突然变复杂：")
    log.info("-" * 60")
    
    # 先简单环境
    for i in range(3):
        fps = scheduler.suggest_fps(0.1, 0.1, 0.8)
        log.info(f"  步骤 {i+1}: FPS={fps}")
    
    # 突然变复杂
    log.info("\n  场景突然变复杂 →")
    for i in range(5):
        fps = scheduler.suggest_fps(0.9, 0.9, 0.2)
        log.info(f"  步骤 {i+3}: FPS={fps}")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 平滑机制测试完成")
    log.info("=" * 60")


def test_static_stable():
    """测试静态稳定降频"""
    log.info("\n" + "=" * 60)
    log.info("测试静态稳定 + 记忆可复用降频")
    log.info("=" * 60")
    
    scheduler = FrameScheduler()
    
    log.info("\n场景：静态环境 + 有记忆可复用")
    log.info("-" * 60")
    
    # 正常情况
    fps_normal = scheduler.suggest_fps(0.2, 0.1, 0.7, static_stable=False)
    log.info(f"  未启用静态稳定: FPS={fps_normal}")
    
    # 启用静态稳定
    fps_static = scheduler.suggest_fps(0.2, 0.1, 0.7, static_stable=True)
    log.info(f"  启用静态稳定: FPS={fps_static}")
    
    if fps_static < fps_normal:
        log.info(f"  ✅ 成功降频（降低 {fps_normal - fps_static} FPS）")
    else:
        log.info(f"  ⚠️ 未降频（可能不满足降频条件）")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 静态稳定测试完成")
    log.info("=" * 60")


def test_brightness_boost():
    """测试亮度影响"""
    log.info("\n" + "=" * 60)
    log.info("测试亮度影响（暗环境提高 FPS）")
    log.info("=" * 60")
    
    scheduler = FrameScheduler()
    
    log.info("\n相同复杂度/速度，不同亮度：")
    log.info("-" * 60")
    
    brightness_levels = [
        (0.1, "极暗"),
        (0.3, "较暗"),
        (0.5, "正常"),
        (0.8, "明亮"),
    ]
    
    for br, desc in brightness_levels:
        fps = scheduler.suggest_fps(0.5, 0.5, br)
        log.info(f"  亮度 {desc} ({br:.2f}): FPS={fps}")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 亮度影响测试完成")
    log.info("=" * 60")


def test_edge_cases():
    """测试边界情况"""
    log.info("\n" + "=" * 60)
    log.info("测试边界情况（输入越界处理）")
    log.info("=" * 60")
    
    scheduler = FrameScheduler()
    
    edge_cases = [
        (-0.1, 0.5, 0.5, "负复杂度"),
        (1.5, 0.5, 0.5, "超范围复杂度"),
        (0.5, -0.2, 0.5, "负速度"),
        (0.5, 0.5, 2.0, "超范围亮度"),
    ]
    
    log.info("\n测试输入越界处理：")
    log.info("-" * 60")
    
    for sc, ms, br, desc in edge_cases:
        try:
            fps = scheduler.suggest_fps(sc, ms, br)
            log.info(f"  ✅ {desc}: FPS={fps} (已自动限制)")
        except Exception as e:
            log.info(f"  ❌ {desc}: 错误 - {e}")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 边界情况测试完成")
    log.info("=" * 60")


def test_integration_with_brightness_detector():
    """测试与 A 模块（BrightnessDetector）的集成"""
    log.info("\n" + "=" * 60)
    log.info("测试与 A 模块集成")
    log.info("=" * 60")
    
    try:
        from vision.brightness_detector import BrightnessDetector
        import numpy as np
        
        brightness_detector = BrightnessDetector()
        frame_scheduler = FrameScheduler()
        
        # 创建模拟帧
        dark_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # 全黑
        bright_frame = np.full((480, 640, 3), 200, dtype=np.uint8)  # 明亮
        
        log.info("\n测试暗环境：")
        log.info("-" * 60")
        brightness_state = brightness_detector.update(dark_frame)
        fps = frame_scheduler.suggest_fps(
            scene_complexity=0.5,
            motion_speed=0.5,
            brightness=brightness_state.value
        )
        log.info(f"  亮度: {brightness_state.value:.3f} ({brightness_state.level})")
        log.info(f"  建议 FPS: {fps}")
        
        log.info("\n测试明亮环境：")
        log.info("-" * 60")
        brightness_state = brightness_detector.update(bright_frame)
        fps = frame_scheduler.suggest_fps(
            scene_complexity=0.5,
            motion_speed=0.5,
            brightness=brightness_state.value
        )
        log.info(f"  亮度: {brightness_state.value:.3f} ({brightness_state.level})")
        log.info(f"  建议 FPS: {fps}")
        
        log.info("\n" + "=" * 60)
        log.info("✅ 集成测试完成")
        log.info("=" * 60")
        
    except ImportError:
        log.info("⚠️ 无法导入 BrightnessDetector，跳过集成测试")


if __name__ == "__main__":
    # 运行所有测试
    test_basic_functionality()
    test_smoothing()
    test_static_stable()
    test_brightness_boost()
    test_edge_cases()
    test_integration_with_brightness_detector()
    
    log.info("\n" + "=" * 60)
    log.info("🎉 所有测试完成！")
    log.info("=" * 60")

























