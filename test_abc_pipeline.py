#!/usr/bin/env python3
"""
测试 A+B+C 模块集成
"""

import sys
sys.path.insert(0, '.')

import numpy as np
import cv2
from luna_badge_v1_2.vision.brightness_detector import BrightnessDetector
from luna_badge_v1_2.vision.scene_complexity import SceneComplexityEstimator
from luna_badge_v1_2.vision.frame_scheduler import FrameScheduler


def test_abc_pipeline():
    """测试 A+B+C 模块集成"""
    
    print("=" * 60)
    print("A+B+C 模块集成测试")
    print("=" * 60)
    
    # 初始化模块
    brightness_detector = BrightnessDetector()
    scene_complexity = SceneComplexityEstimator()
    frame_scheduler = FrameScheduler()
    
    frame_count = 0
    
    # 测试场景1: 室内简单场景（明亮、低复杂度）
    print("\n【场景1: 室内简单场景】")
    for i in range(3):
        frame_count += 1
        # 创建明亮的简单图像
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        cv2.rectangle(frame, (100, 100), (200, 200), (150, 150, 150), 2)
        
        # A: 亮度检测
        brightness_state = brightness_detector.update(frame)
        
        # C: 环境复杂度
        complexity = scene_complexity.evaluate(frame)
        
        # B: 抽帧建议
        suggested_fps = frame_scheduler.suggest_fps(
            scene_complexity=complexity,
            motion_speed=0.0,
            brightness=brightness_state.value,
            is_turning=False,
            static_stable=False,
        )
        
        should_process = frame_scheduler.should_process(frame_count, suggested_fps)
        
        result = {
            "brightness": brightness_state.value,
            "scene_complexity": complexity,
            "suggested_fps": suggested_fps,
            "should_process": should_process,
        }
        
        print(f"  帧 {frame_count}: {result}")
    
    # 测试场景2: 复杂街道场景（中等亮度、高复杂度）
    print("\n【场景2: 复杂街道场景】")
    for i in range(3):
        frame_count += 1
        # 创建复杂的图像（随机噪声模拟复杂场景）
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        # 添加一些边缘
        cv2.line(frame, (0, 240), (640, 240), (255, 255, 255), 3)
        cv2.line(frame, (320, 0), (320, 480), (255, 255, 255), 3)
        
        # A: 亮度检测
        brightness_state = brightness_detector.update(frame)
        
        # C: 环境复杂度
        complexity = scene_complexity.evaluate(frame)
        
        # B: 抽帧建议
        suggested_fps = frame_scheduler.suggest_fps(
            scene_complexity=complexity,
            motion_speed=0.5,  # 中等速度
            brightness=brightness_state.value,
            is_turning=False,
            static_stable=False,
        )
        
        should_process = frame_scheduler.should_process(frame_count, suggested_fps)
        
        result = {
            "brightness": brightness_state.value,
            "scene_complexity": complexity,
            "suggested_fps": suggested_fps,
            "should_process": should_process,
        }
        
        print(f"  帧 {frame_count}: {result}")
    
    # 测试场景3: 暗环境（低亮度、中等复杂度）
    print("\n【场景3: 暗环境】")
    for i in range(3):
        frame_count += 1
        # 创建暗图像
        frame = np.random.randint(0, 80, (480, 640, 3), dtype=np.uint8)
        
        # A: 亮度检测
        brightness_state = brightness_detector.update(frame)
        
        # C: 环境复杂度
        complexity = scene_complexity.evaluate(frame)
        
        # B: 抽帧建议
        suggested_fps = frame_scheduler.suggest_fps(
            scene_complexity=complexity,
            motion_speed=0.0,
            brightness=brightness_state.value,
            is_turning=False,
            static_stable=False,
        )
        
        should_process = frame_scheduler.should_process(frame_count, suggested_fps)
        
        result = {
            "brightness": brightness_state.value,
            "scene_complexity": complexity,
            "suggested_fps": suggested_fps,
            "should_process": should_process,
        }
        
        print(f"  帧 {frame_count}: {result}")
    
    print("\n" + "=" * 60)
    print("✅ A+B+C 模块集成测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_abc_pipeline()
























