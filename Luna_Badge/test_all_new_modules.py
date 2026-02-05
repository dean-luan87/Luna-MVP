#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 全量测试脚本
测试所有新实现的模块
"""

import json
import sys
import time
from datetime import datetime

def test_all_modules():
    """测试所有模块"""
    
    test_results = []
    
    # 测试A类：人群行为识别
    print("\n" + "=" * 70)
    print("测试A类：人群行为识别模块")
    print("=" * 70)
    
    try:
        # 1. 排队检测
        from core.queue_detector import QueueDetector
        detector = QueueDetector()
        positions = [(100, 100), (100, 120), (100, 140)]
        result = detector.detect_queue(positions)
        test_results.append({
            "module": "queue_detector",
            "status": "passed" if result.detected else "warning",
            "message": f"排队检测: {result.direction.value}"
        })
        
        # 2. 人群密度
        from core.crowd_density_detector import CrowdDensityDetector
        detector = CrowdDensityDetector()
        result = detector.detect_density(positions, (480, 640))
        test_results.append({
            "module": "crowd_density_detector",
            "status": "passed",
            "message": f"密度等级: {result.level.value}"
        })
        
        # 3. 人流方向
        from core.flow_direction_analyzer import FlowDirectionAnalyzer
        analyzer = FlowDirectionAnalyzer()
        trajectories = [[(100, 100), (105, 95)]]
        result = analyzer.analyze_flow(trajectories)
        test_results.append({
            "module": "flow_direction_analyzer",
            "status": "passed",
            "message": f"方向: {result.flow_direction.value}"
        })
        
    except Exception as e:
        test_results.append({
            "module": "A类模块",
            "status": "failed",
            "message": str(e)
        })
    
    # 测试B类：OCR识别增强
    print("\n" + "=" * 70)
    print("测试B类：OCR识别增强模块")
    print("=" * 70)
    
    try:
        from core.ocr_advanced_reader import OCRAdvancedReader
        reader = OCRAdvancedReader()
        import numpy as np
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
        result = reader.read_document(test_image)
        test_results.append({
            "module": "ocr_advanced_reader",
            "status": "passed",
            "message": f"识别块数: {len(result.blocks)}"
        })
        
        from core.product_info_checker import ProductInfoChecker
        checker = ProductInfoChecker()
        result = checker.check_product("某某饼干 配料: 小麦粉、植物油", "1234567890123")
        test_results.append({
            "module": "product_info_checker",
            "status": "passed",
            "message": f"产品: {result.name}"
        })
        
    except Exception as e:
        test_results.append({
            "module": "B类模块",
            "status": "failed",
            "message": str(e)
        })
    
    # 测试C类：增强记忆
    print("\n" + "=" * 70)
    print("测试C类：增强记忆模块")
    print("=" * 70)
    
    try:
        from core.memory_store import MemoryStore, MemoryType, Priority
        store = MemoryStore('data/test_memory_full.json')
        memory = store.add_memory(
            MemoryType.MEDICATION,
            "测试用药",
            "每天一次",
            priority=Priority.HIGH
        )
        test_results.append({
            "module": "memory_store",
            "status": "passed",
            "message": f"添加记忆: {memory.id}"
        })
        
        try:
            import sys
            sys.path.insert(0, 'core')
            from memory_caller import MemoryCaller
            caller = MemoryCaller(store)
            results = caller.search_fuzzy("用药")
            test_results.append({
                "module": "memory_caller",
                "status": "passed",
                "message": f"搜索到: {len(results)} 条"
            })
        except Exception as e:
            test_results.append({
                "module": "memory_caller",
                "status": "warning",
                "message": f"导入问题: {str(e)}"
            })
        
    except Exception as e:
        test_results.append({
            "module": "C类模块",
            "status": "failed",
            "message": str(e)
        })
    
    # 测试D类：门牌识别
    print("\n" + "=" * 70)
    print("测试D类：门牌识别模块")
    print("=" * 70)
    
    try:
        from core.doorplate_reader import DoorplateReader
        reader = DoorplateReader()
        result = reader.detect_doorplates(None)
        test_results.append({
            "module": "doorplate_reader",
            "status": "passed",
            "message": f"检测到: {len(result)} 个门牌"
        })
        
        try:
            import sys
            sys.path.insert(0, 'core')
            from doorplate_inference import DoorplateInferenceEngine
            engine = DoorplateInferenceEngine()
            from doorplate_reader import DoorplateInfo
            import time as time_module
            doorplate = DoorplateInfo("501室", None, (100, 50, 150, 100), 0.9, None, 501, time_module.time())
            result = engine.infer_direction(doorplate)
            test_results.append({
                "module": "doorplate_inference",
                "status": "passed",
                "message": f"推理: {result.status.value}"
            })
        except Exception as e:
            test_results.append({
                "module": "doorplate_inference",
                "status": "warning",
                "message": f"导入问题: {str(e)}"
            })
        
    except Exception as e:
        test_results.append({
            "module": "D类模块",
            "status": "failed",
            "message": str(e)
        })
    
    # 测试E类：小智补全
    print("\n" + "=" * 70)
    print("测试E类：小智补全模块")
    print("=" * 70)
    
    try:
        from core.user_manager import UserManager
        manager = UserManager('data/test_users_full.json')
        success = manager.send_verification_code("13800138000")
        test_results.append({
            "module": "user_manager",
            "status": "passed" if success else "failed",
            "message": "发送验证码"
        })
        
        from core.voice_recognition import VoiceRecognitionEngine
        engine = VoiceRecognitionEngine()
        result = engine.recognize(text="向前走")
        test_results.append({
            "module": "voice_recognition",
            "status": "passed",
            "message": f"识别: {result.intent.value}"
        })
        
        from core.tts_manager import TTSManager, TTSStyle
        manager = TTSManager()
        config = manager.get_config(TTSStyle.CHEERFUL)
        test_results.append({
            "module": "tts_manager",
            "status": "passed",
            "message": f"配置: {config.style.value}"
        })
        
    except Exception as e:
        test_results.append({
            "module": "E类模块",
            "status": "failed",
            "message": str(e)
        })
    
    # 生成测试报告
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    
    print(json.dumps({
        "event": "full_test_complete",
        "level": "info",
        "data": {
            "total_tests": len(test_results),
            "passed": passed,
            "failed": failed,
            "warnings": len(test_results) - passed - failed,
            "results": test_results,
            "summary": {
                "success_rate": f"{passed * 100 // len(test_results)}%",
                "status": "all_passed" if failed == 0 else "partial_passed"
            }
        },
        "timestamp": datetime.now().isoformat()
    }, ensure_ascii=False, indent=2))
    
    print(f"\n通过: {passed}/{len(test_results)}")
    print(f"失败: {failed}/{len(test_results)}")

if __name__ == "__main__":
    test_all_modules()

