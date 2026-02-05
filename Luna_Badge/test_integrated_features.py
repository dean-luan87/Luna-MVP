#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 集成功能测试
测试故障处理机制、日志持久化和可视化显示功能
"""

import asyncio
import logging
import time
import numpy as np
from core.fault_handler import FaultHandler, FaultType, FaultSeverity, handle_fault
from core.log_manager import LogManager, LogLevel, EventType, log_voice_broadcast, log_path_status, log_ai_detection
from core.visual_display import VisualDisplayManager, DetectionBox, PathRegion, PathStatus, update_display

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class IntegratedTestManager:
    """集成测试管理器"""
    
    def __init__(self):
        """初始化集成测试管理器"""
        self.fault_handler = FaultHandler()
        self.log_manager = LogManager()
        self.visual_display = VisualDisplayManager(enable_display=False)  # 测试时禁用显示
        
        logger.info("🧪 集成测试管理器初始化完成")
    
    async def test_fault_handling(self):
        """测试故障处理机制"""
        logger.info("🧪 开始测试故障处理机制")
        
        # 添加故障回调
        def fault_callback(fault_info):
            logger.info(f"📊 故障回调: {fault_info.fault_id} - {fault_info.error_message}")
        
        self.fault_handler.add_fault_callback(fault_callback)
        
        # 模拟不同类型的故障
        fault_id1 = self.fault_handler.handle_fault(
            FaultType.CAMERA, FaultSeverity.HIGH, "Camera", "摄像头初始化失败"
        )
        
        fault_id2 = self.fault_handler.handle_fault(
            FaultType.AI_MODEL, FaultSeverity.CRITICAL, "YOLO", "模型加载失败"
        )
        
        fault_id3 = self.fault_handler.handle_fault(
            FaultType.NETWORK, FaultSeverity.MEDIUM, "Network", "网络连接超时"
        )
        
        # 等待故障处理
        await asyncio.sleep(3)
        
        # 显示故障统计
        stats = self.fault_handler.get_fault_stats()
        logger.info(f"📊 故障统计: {stats}")
        
        # 显示活跃故障
        active_faults = self.fault_handler.get_active_faults()
        logger.info(f"📊 活跃故障数量: {len(active_faults)}")
        
        return True
    
    def test_log_persistence(self):
        """测试日志持久化"""
        logger.info("🧪 开始测试日志持久化")
        
        # 测试不同类型的日志
        self.log_manager.log(LogLevel.INFO, EventType.SYSTEM_START, "System", "系统启动")
        
        log_voice_broadcast("你好，我是Luna", "tts", True, 1.5)
        log_voice_broadcast("前方检测到行人", "tts", False, 0.0)
        
        log_path_status("blocked", 3, 0, ["行人", "车辆", "障碍物"])
        log_path_status("clear", 0, 5, [])
        
        log_ai_detection("person", [{"type": "person", "confidence": 0.95}], 0.95, 0.1)
        log_ai_detection("car", [{"type": "car", "confidence": 0.87}], 0.87, 0.08)
        
        # 等待日志写入
        time.sleep(2)
        
        # 显示日志统计
        stats = self.log_manager.get_log_stats()
        logger.info(f"📊 日志统计: {stats}")
        
        # 导出日志
        logs = self.log_manager.export_logs()
        logger.info(f"📝 导出日志数量: {len(logs)}")
        
        # 显示最近的日志
        if logs:
            recent_log = logs[-1]
            logger.info(f"📝 最近日志: {recent_log['message']}")
        
        return True
    
    def test_visual_display(self):
        """测试可视化显示"""
        logger.info("🧪 开始测试可视化显示")
        
        # 创建测试帧
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 创建测试检测框
        detections = [
            DetectionBox(100, 100, 200, 300, 0.95, "person", (255, 0, 0)),
            DetectionBox(300, 150, 400, 250, 0.87, "car", (255, 165, 0))
        ]
        
        # 创建测试路径区域
        path_regions = [
            PathRegion(50, 400, 590, 470, PathStatus.CLEAR, (0, 255, 0)),
            PathRegion(100, 200, 200, 400, PathStatus.BLOCKED, (0, 0, 255))
        ]
        
        # 创建测试性能信息
        performance_info = {
            "FPS": 30,
            "Detection Time": "0.05s",
            "Memory Usage": "256MB"
        }
        
        # 更新显示
        self.visual_display.update_display(
            frame=frame,
            detections=detections,
            path_regions=path_regions,
            path_status=PathStatus.WARNING,
            broadcast_message="前方检测到行人，请注意安全",
            performance_info=performance_info
        )
        
        # 显示配置
        config = self.visual_display.get_display_config()
        logger.info(f"📊 显示配置: {config}")
        
        return True
    
    async def test_integrated_workflow(self):
        """测试集成工作流"""
        logger.info("🧪 开始测试集成工作流")
        
        # 模拟完整的检测和处理流程
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # 模拟AI检测
        detections = [
            DetectionBox(100, 100, 200, 300, 0.95, "person", (255, 0, 0)),
            DetectionBox(300, 150, 400, 250, 0.87, "car", (255, 165, 0))
        ]
        
        # 记录AI检测日志
        log_ai_detection("person", [{"type": "person", "confidence": 0.95}], 0.95, 0.1)
        
        # 判断路径状态
        if len(detections) > 0:
            path_status = PathStatus.BLOCKED
            broadcast_message = "前方检测到障碍物，请注意安全"
            
            # 记录路径状态日志
            log_path_status("blocked", len(detections), 0, [det.label for det in detections])
            
            # 记录语音播报日志
            log_voice_broadcast(broadcast_message, "tts", True, 1.5)
            
            # 处理故障（如果有）
            if len(detections) > 2:
                handle_fault(FaultType.AI_MODEL, FaultSeverity.MEDIUM, "AI", "检测到过多障碍物")
        else:
            path_status = PathStatus.CLEAR
            broadcast_message = "路径畅通"
            
            # 记录路径状态日志
            log_path_status("clear", 0, 1, [])
        
        # 更新可视化显示
        self.visual_display.update_display(
            frame=frame,
            detections=detections,
            path_status=path_status,
            broadcast_message=broadcast_message,
            performance_info={"FPS": 30, "Detection Time": "0.05s"}
        )
        
        # 等待处理完成
        await asyncio.sleep(1)
        
        logger.info("✅ 集成工作流测试完成")
        return True
    
    async def run_all_tests(self):
        """运行所有测试"""
        logger.info("🚀 开始运行集成功能测试")
        
        test_results = {}
        
        # 测试故障处理机制
        try:
            test_results["fault_handling"] = await self.test_fault_handling()
        except Exception as e:
            logger.error(f"❌ 故障处理测试失败: {e}")
            test_results["fault_handling"] = False
        
        # 测试日志持久化
        try:
            test_results["log_persistence"] = self.test_log_persistence()
        except Exception as e:
            logger.error(f"❌ 日志持久化测试失败: {e}")
            test_results["log_persistence"] = False
        
        # 测试可视化显示
        try:
            test_results["visual_display"] = self.test_visual_display()
        except Exception as e:
            logger.error(f"❌ 可视化显示测试失败: {e}")
            test_results["visual_display"] = False
        
        # 测试集成工作流
        try:
            test_results["integrated_workflow"] = await self.test_integrated_workflow()
        except Exception as e:
            logger.error(f"❌ 集成工作流测试失败: {e}")
            test_results["integrated_workflow"] = False
        
        # 显示测试结果
        logger.info("=" * 50)
        logger.info("测试结果总结")
        logger.info("=" * 50)
        
        for test_name, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            logger.info(f"{test_name}: {status}")
        
        # 计算总体结果
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        success_rate = (passed_tests / total_tests) * 100
        
        logger.info(f"总体成功率: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        if success_rate == 100:
            logger.info("🎉 所有测试通过！")
        else:
            logger.warning("⚠️ 部分测试失败，请检查相关功能")
        
        return test_results
    
    def cleanup(self):
        """清理测试环境"""
        logger.info("🧹 清理测试环境")
        
        # 停止各个管理器
        self.visual_display.stop()
        self.log_manager.stop()
        
        # 清理日志文件
        self.log_manager.clear_logs()
        
        logger.info("✅ 测试环境清理完成")

async def main():
    """主测试函数"""
    logger.info("🌟 开始Luna Badge集成功能测试")
    
    # 创建测试管理器
    test_manager = IntegratedTestManager()
    
    try:
        # 运行所有测试
        test_results = await test_manager.run_all_tests()
        
        # 清理测试环境
        test_manager.cleanup()
        
        return test_results
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {e}")
        test_manager.cleanup()
        return None

if __name__ == "__main__":
    # 运行测试
    try:
        results = asyncio.run(main())
        if results:
            print("\n🎉 集成功能测试完成！")
        else:
            print("\n❌ 集成功能测试失败！")
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
