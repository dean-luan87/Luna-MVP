#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 视觉OCR引擎测试
测试 PaddleOCR + YOLOv8n 集成
"""

import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_vision_ocr_engine():
    """测试视觉OCR引擎"""
    print("=" * 60)
    print("🎯 视觉OCR引擎测试")
    print("=" * 60)
    
    try:
        from core.vision_ocr_engine import VisionOCREngine
        
        # 初始化引擎
        print("\n1. 初始化引擎...")
        engine = VisionOCREngine(use_yolo=True, use_ocr=True)
        
        # 加载模型
        print("   加载模型...")
        if engine.load_models():
            print("   ✅ 模型加载成功")
            print(f"   - YOLO: {engine.yolo_model is not None}")
            print(f"   - OCR: {engine.ocr_model is not None}")
        else:
            print("   ⚠️ 模型加载失败（可能需要安装依赖）")
        
        # 创建测试图像（黑色背景，白色文字）
        print("\n2. 创建测试图像...")
        test_image = np.ones((640, 480, 3), dtype=np.uint8) * 255  # 白色背景
        cv2.putText(test_image, "Hello", (50, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        cv2.putText(test_image, "Exit", (50, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        print("   ✅ 测试图像创建成功")
        
        # 测试YOLO检测
        if engine.use_yolo:
            print("\n3. 测试YOLO物体检测...")
            detections = engine.detect_objects(test_image)
            print(f"   检测到 {len(detections)} 个物体")
            for det in detections[:3]:  # 只显示前3个
                print(f"   - {det['class']}: {det['confidence']:.2f}")
        
        # 测试OCR识别
        if engine.use_ocr:
            print("\n4. 测试OCR文字识别...")
            ocr_results = engine.recognize_text(test_image)
            print(f"   识别到 {len(ocr_results)} 段文字")
            for ocr in ocr_results:
                print(f"   - {ocr.text}: {ocr.confidence:.2f}")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成")
        
    except ImportError as e:
        print(f"\n❌ 导入错误: {e}")
        print("   需要安装: pip install paddleocr ultralytics")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_dependencies():
    """检查依赖是否安装"""
    print("=" * 60)
    print("📦 检查依赖")
    print("=" * 60)
    
    dependencies = {
        "ultralytics": "YOLOv8",
        "paddleocr": "PaddleOCR",
        "paddlepaddle": "PaddlePaddle",
        "cv2": "OpenCV"
    }
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} 已安装")
        except ImportError:
            print(f"❌ {name} 未安装")
    
    print("\n" + "=" * 60)

def main():
    """主测试函数"""
    print("\n")
    print("🎯 Luna Badge 视觉OCR引擎测试")
    print("=" * 60)
    print()
    
    # 检查依赖
    test_dependencies()
    print()
    
    # 测试引擎
    test_vision_ocr_engine()
    
    print()
    print("=" * 60)
    print("📝 测试完成")
    print("=" * 60)
    print()
    print("💡 提示:")
    print("  1. 如果依赖未安装，运行:")
    print("     pip install paddleocr paddlepaddle ultralytics")
    print("  2. 首次运行会自动下载模型")
    print("  3. 需要摄像头权限进行实时测试")
    print()

if __name__ == "__main__":
    # 导入cv2
    try:
        import cv2
    except ImportError:
        print("❌ OpenCV未安装，请运行: pip install opencv-python")
        exit(1)
    
    main()

