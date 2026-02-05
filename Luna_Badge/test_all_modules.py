#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 完整模块测试
测试所有6个核心模块的功能
"""

import logging
import numpy as np
import cv2
import math

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_all_modules():
    """测试所有模块"""
    print("=" * 70)
    print("🎯 Luna Badge 完整模块测试")
    print("=" * 70)
    
    test_results = {}
    
    # ==================== 测试1: 标识牌识别 ====================
    print("\n" + "=" * 70)
    print("📋 测试1: 标识牌识别模块")
    print("=" * 70)
    try:
        from core.signboard_detector import SignboardDetector
        
        detector = SignboardDetector()
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)  # 浅灰色背景
        
        # 绘制一些测试区域
        cv2.rectangle(test_img, (50, 50), (150, 150), (0, 255, 255), -1)  # 橙色（洗手间标识）
        
        results = detector.detect_signboard(test_img)
        
        print(f"✅ 检测器初始化成功")
        print(f"✅ 检测到 {len(results)} 个标识牌")
        test_results['signboard'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['signboard'] = False
    
    # ==================== 测试2: 公共设施识别 ====================
    print("\n" + "=" * 70)
    print("📋 测试2: 公共设施识别模块")
    print("=" * 70)
    try:
        from core.facility_detector import FacilityDetector
        
        detector = FacilityDetector()
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)
        
        results = detector.detect_facility(test_img)
        
        print(f"✅ 检测器初始化成功")
        print(f"✅ 检测到 {len(results)} 个设施")
        test_results['facility'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['facility'] = False
    
    # ==================== 测试3: 隐私保护 ====================
    print("\n" + "=" * 70)
    print("📋 测试3: 隐私保护模块")
    print("=" * 70)
    try:
        from core.privacy_protection import (PrivacyProtectionManager, 
                                            PrivacyZonePOI, GPSCoordinate, 
                                            PrivacyZoneType)
        
        manager = PrivacyProtectionManager('data/test_privacy.json')
        
        # 添加隐私区域POI
        toilet_poi = PrivacyZonePOI(
            zone_type=PrivacyZoneType.TOILET,
            name="测试洗手间",
            position=GPSCoordinate(39.9040, 116.4070),
            radius=5.0
        )
        manager.add_privacy_poi(toilet_poi)
        
        # 更新GPS位置
        manager.update_gps(39.9040, 116.4071)  # 接近但未触发
        
        # 检查隐私区域
        triggered = manager.check_privacy_zone()
        
        print(f"✅ 管理器初始化成功")
        print(f"✅ 隐私区域检查: {'触发' if triggered else '未触发'}")
        test_results['privacy'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['privacy'] = False
    
    # ==================== 测试4: 危险环境识别 ====================
    print("\n" + "=" * 70)
    print("📋 测试4: 危险环境识别模块")
    print("=" * 70)
    try:
        from core.hazard_detector import HazardDetector
        
        detector = HazardDetector()
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)
        
        # 绘制蓝色水域
        cv2.rectangle(test_img, (50, 50), (200, 200), (255, 150, 0), -1)
        
        results = detector.detect_hazards(test_img)
        
        print(f"✅ 检测器初始化成功")
        print(f"✅ 检测到 {len(results)} 个危险区域")
        
        # 获取摘要
        summary = detector.get_detection_summary(results)
        print(f"✅ 高风险区域: {summary['critical_count']} 个")
        test_results['hazard'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['hazard'] = False
    
    # ==================== 测试5: 地点纠错 ====================
    print("\n" + "=" * 70)
    print("📋 测试5: 地点纠错模块")
    print("=" * 70)
    try:
        from core.location_correction import LocationCorrectionManager
        
        manager = LocationCorrectionManager('data/test_location_correction.json')
        
        # 提交纠错
        correction = manager.submit_correction(
            original_name="洗手间",
            corrected_name="测试洗手间A",
            latitude=39.9040,
            longitude=116.4070,
            user_id="test_user_001"
        )
        
        # 获取统计信息
        stats = manager.get_statistics()
        
        print(f"✅ 管理器初始化成功")
        print(f"✅ 提交纠错: {correction.original_name} -> {correction.corrected_name}")
        print(f"✅ 总纠错数: {stats['total_corrections']}")
        test_results['location_correction'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['location_correction'] = False
    
    # ==================== 测试6: 局部地图生成 ====================
    print("\n" + "=" * 70)
    print("📋 测试6: 局部地图生成模块")
    print("=" * 70)
    try:
        from core.local_map_generator import LocalMapGenerator, LandmarkType
        
        generator = LocalMapGenerator(map_size=(50.0, 50.0))
        
        # 移动和添加地标
        generator.update_position(5.0, 0.0)  # 向前移动5米
        generator.add_landmark_from_vision(
            None,
            LandmarkType.ENTRANCE,
            relative_position=(3.0, 0.0),
            label="测试入口"
        )
        generator.update_position(5.0, 0.0)  # 再向前移动5米
        
        # 完成路径
        generator.finish_path()
        
        # 获取地图
        map_obj = generator.get_map()
        
        print(f"✅ 地图生成器初始化成功")
        print(f"✅ 地图地标数: {len(map_obj.landmarks)}")
        print(f"✅ 地图路径数: {len(map_obj.paths)}")
        test_results['local_map'] = True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        test_results['local_map'] = False
    
    # ==================== 综合集成测试 ====================
    print("\n" + "=" * 70)
    print("📋 综合集成测试: 多模块协作")
    print("=" * 70)
    try:
        # 模拟一个完整的检测场景
        from core.hazard_detector import HazardDetector
        from core.local_map_generator import LocalMapGenerator, LandmarkType
        
        # 1. 检测危险
        hazard_detector = HazardDetector()
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)
        cv2.rectangle(test_img, (100, 100), (300, 300), (0, 150, 255), -1)  # 橙色（工地）
        hazards = hazard_detector.detect_hazards(test_img)
        
        # 2. 添加到地图
        map_generator = LocalMapGenerator()
        map_generator.update_position(5.0, 0.0)
        
        for hazard in hazards:
            if hazard.severity.value in ['high', 'critical']:
                map_generator.add_landmark_direct(
                    LandmarkType.HAZARD_EDGE,
                    hazard.center,
                    label=f"{hazard.type.value}危险区",
                    confidence=hazard.confidence
                )
        
        map_obj = map_generator.get_map()
        
        print(f"✅ 检测到危险: {len(hazards)} 个")
        print(f"✅ 添加到地图: {len(map_obj.landmarks)} 个地标")
        print(f"✅ 综合集成测试通过")
        test_results['integration'] = True
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        test_results['integration'] = False
    
    # ==================== 测试总结 ====================
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name:20s}: {status}")
    
    print(f"\n总计: {passed_tests}/{total_tests} 测试通过")
    print(f"成功率: {passed_tests * 100 // total_tests}%")
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！系统运行正常！")
    else:
        print(f"\n⚠️  有 {total_tests - passed_tests} 个测试失败")
    
    print("=" * 70)
    
    return test_results

if __name__ == "__main__":
    test_all_modules()
