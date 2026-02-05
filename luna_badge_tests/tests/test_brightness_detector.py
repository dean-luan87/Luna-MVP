from core.logging import get_logger

log = get_logger("test_brightness_detector")
"""
测试 A 模块：BrightnessDetector

用法：
    python3 tests/test_brightness_detector.py

如果没有摄像头，会使用模拟图像进行测试。
"""

import sys
import os
import numpy as np
import cv2

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision.brightness_detector import BrightnessDetector, BrightnessState


def create_test_frame(brightness_level: str) -> np.ndarray:
    """
    创建测试用的模拟图像帧
    
    Args:
        brightness_level: "DARK", "NORMAL", "BRIGHT"
    
    Returns:
        模拟的 BGR 图像帧
    """
    height, width = 480, 640
    
    if brightness_level == "DARK":
        # 暗环境：低亮度
        gray_value = 50  # 0-255
    elif brightness_level == "NORMAL":
        # 正常环境：中等亮度
        gray_value = 128
    else:  # BRIGHT
        # 明亮环境：高亮度
        gray_value = 200
    
    # 创建灰度图像
    gray = np.full((height, width), gray_value, dtype=np.uint8)
    
    # 转换为 BGR（三通道）
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    return frame


def test_brightness_detection():
    """测试亮度检测功能"""
    log.info("=" * 60")
    log.info("测试 A 模块：BrightnessDetector")
    log.info("=" * 60")
    
    detector = BrightnessDetector(
        on_threshold=0.35,
        off_threshold=0.45,
        sample_interval_frames=5
    )
    
    # 测试场景
    test_cases = [
        ("DARK", False, "暗环境，未开灯"),
        ("DARK", True, "暗环境，已开灯"),
        ("NORMAL", False, "正常环境，未开灯"),
        ("NORMAL", True, "正常环境，已开灯"),
        ("BRIGHT", False, "明亮环境，未开灯"),
        ("BRIGHT", True, "明亮环境，已开灯"),
    ]
    
    log.info("\n【测试用例】")
    log.info("-" * 60")
    
    for brightness_level, fill_light_on, description in test_cases:
        frame = create_test_frame(brightness_level)
        state = detector.update(frame, fill_light_on=fill_light_on)
        
        log.info(f"\n场景: {description}")
        log.info(f"  亮度值: {state.value:.3f}")
        log.info(f"  亮度等级: {state.level}")
        log.info(f"  补光灯状态: {'开启' if fill_light_on else '关闭'}")
        log.info(f"  建议补光: {'是' if state.need_fill_light else '否'}")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 测试完成")
    log.info("=" * 60")


def test_hysteresis_logic():
    """测试迟滞逻辑（防抖）"""
    log.info("\n" + "=" * 60)
    log.info("测试迟滞逻辑（防抖）")
    log.info("=" * 60")
    
    detector = BrightnessDetector(
        on_threshold=0.35,
        off_threshold=0.45,
        sample_interval_frames=1  # 每帧都计算，方便测试
    )
    
    # 模拟亮度在阈值附近变化
    brightness_values = [0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48]
    
    log.info("\n模拟亮度在阈值附近变化（0.30 → 0.48）")
    log.info("-" * 60")
    log.info(f"开灯阈值: {detector.on_threshold:.2f}")
    log.info(f"关灯阈值: {detector.off_threshold:.2f}")
    log.info("-" * 60")
    
    fill_light_on = False
    
    for brightness in brightness_values:
        # 创建对应亮度的测试帧
        gray_value = int(brightness * 255)
        frame = np.full((480, 640, 3), gray_value, dtype=np.uint8)
        
        state = detector.update(frame, fill_light_on=fill_light_on)
        
        # 更新补光灯状态（模拟硬件响应）
        if state.need_fill_light != fill_light_on:
            fill_light_on = state.need_fill_light
            action = "开灯" if fill_light_on else "关灯"
            log.info(f"亮度 {brightness:.2f} → {action} (状态变化)")
        else:
            log.info(f"亮度 {brightness:.2f} → 保持 {'开启' if fill_light_on else '关闭'}")
    
    log.info("\n" + "=" * 60)
    log.info("✅ 迟滞逻辑测试完成")
    log.info("=" * 60")


def test_with_camera():
    """使用真实摄像头测试（如果可用）"""
    log.info("\n" + "=" * 60)
    log.info("尝试使用真实摄像头测试")
    log.info("=" * 60")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        log.info("❌ 无法打开摄像头，跳过真实摄像头测试")
        return
    
    log.info("✅ 摄像头已打开，按 'q' 退出测试")
    
    detector = BrightnessDetector()
    fill_light_on = False
    
    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # 更新亮度检测
            state = detector.update(frame, fill_light_on=fill_light_on)
            
            # 模拟补光灯控制
            if state.need_fill_light != fill_light_on:
                fill_light_on = state.need_fill_light
                action = "💡 开灯" if fill_light_on else "🔌 关灯"
                log.info(f"帧 {frame_count}: {action} | 亮度 {state.value:.3f} ({state.level})")
            
            # 在图像上显示信息
            cv2.putText(frame, f"Brightness: {state.value:.3f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Level: {state.level}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Fill Light: {'ON' if fill_light_on else 'OFF'}", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Brightness Detector Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        log.info("✅ 摄像头测试结束")


if __name__ == "__main__":
    # 运行测试
    test_brightness_detection()
    test_hysteresis_logic()
    
    # 可选：使用真实摄像头测试
    # test_with_camera()














