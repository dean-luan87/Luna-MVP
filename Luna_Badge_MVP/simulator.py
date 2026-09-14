#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地模拟测试工具
支持无摄像头时模拟测试整套流程
"""

import sys
import os
import time
import argparse
import threading
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.dummy_data import DummyDataGenerator, get_dummy_generator
from core.debug_logger import DebugLogger, get_debug_logger, EventType, LogLevel
from core.cooldown_manager import CooldownManager
from core.state_tracker import StateTracker
from speech.speech_engine import SpeechEngine
from luna_hub.action import ActionContext, SpeakGuard

class LunaSimulator:
    """Luna模拟器"""
    
    def __init__(self):
        """初始化模拟器"""
        self.running = False
        self.dummy_generator = get_dummy_generator()
        self.debug_logger = get_debug_logger("LunaSimulator", debug_mode=True)
        self.cooldown_manager = CooldownManager()
        self.state_tracker = StateTracker()
        self.speech_engine = SpeechEngine()
        
        # 初始化 Action 层（Step 2）
        self.speak_guard = SpeakGuard()
        
        # 模拟状态
        self.current_scenario = "normal"
        self.frame_count = 0
        self.auto_mode = False
        self.auto_interval = 3  # 自动模式间隔（秒）
        
        # 初始化组件
        self._initialize_components()
        
        logger.info("✅ Luna模拟器初始化完成")
    
    def _initialize_components(self):
        """初始化组件"""
        try:
            # 初始化冷却管理器
            self.cooldown_manager.initialize()
            
            # 初始化状态跟踪器
            self.state_tracker.initialize()
            
            # 初始化语音引擎
            self.speech_engine.initialize()
            
            logger.info("✅ 组件初始化完成")
            
        except Exception as e:
            logger.error(f"❌ 组件初始化失败: {e}")
    
    def simulate_scenario(self, scenario: str) -> Dict[str, Any]:
        """
        模拟指定场景
        
        Args:
            scenario: 场景名称
            
        Returns:
            Dict[str, Any]: 模拟结果
        """
        try:
            # 生成场景数据
            data = self.dummy_generator.generate_scenario_data(scenario)
            
            # 记录检测事件
            self.debug_logger.log_detection(data["detections"])
            
            # 记录跟踪事件
            self.debug_logger.log_tracking(data["tracks"])
            
            # 记录预测事件
            if data["path_prediction"]:
                self.debug_logger.log_prediction(data["path_prediction"])
            
            # 判断是否需要播报
            should_speak = False
            speech_text = None
            priority = 1
            
            if data["path_prediction"]["obstructed"]:
                if self.cooldown_manager.can_trigger("path_obstructed"):
                    should_speak = True
                    speech_text = "前方有障碍物，请注意安全"
                    priority = 0  # 高优先级
                    self.cooldown_manager.trigger("path_obstructed")
                    self.state_tracker.set_flag("path_obstructed_announced", True)
                    
                    # 记录语音事件
                    self.debug_logger.log_speech(speech_text, priority, "queued")
                    
                    # 记录冷却事件
                    self.debug_logger.log_cooldown("path_obstructed", False, 
                                                 self.cooldown_manager.get_remaining_time("path_obstructed"))
            else:
                if self.cooldown_manager.can_trigger("path_clear"):
                    should_speak = True
                    speech_text = "前方路径畅通"
                    priority = 1
                    self.cooldown_manager.trigger("path_clear")
                    self.state_tracker.set_flag("path_clear_announced", True)
                    
                    # 记录语音事件
                    self.debug_logger.log_speech(speech_text, priority, "queued")
                    
                    # 记录冷却事件
                    self.debug_logger.log_cooldown("path_clear", False, 
                                                 self.cooldown_manager.get_remaining_time("path_clear"))
            
            # 播报语音（通过 Action 层，Step 2）
            if should_speak and speech_text:
                # 构造 ActionContext
                is_speaking = not self.speech_engine.speech_queue.empty() if hasattr(self.speech_engine, 'speech_queue') else False
                
                context = ActionContext(
                    is_speaking=is_speaking,
                    source="task_engine",
                    action_type="speak",
                    intent="task_result_speak"
                )
                
                # 通过 SpeakGuard 判断
                decision = self.speak_guard.should_speak(context)
                
                if decision.allow:
                    self.speech_engine.speak(speech_text, priority)
                else:
                    # 不补播、不重试
                    logger.info(
                        f"[ACTION-DROP] speak rejected by {decision.dropped_by}: {decision.reason}"
                    )
            
            # 更新帧计数
            self.frame_count += 1
            
            result = {
                "scenario": scenario,
                "frame_count": self.frame_count,
                "detections": data["detections"],
                "tracks": data["tracks"],
                "path_prediction": data["path_prediction"],
                "should_speak": should_speak,
                "speech_text": speech_text,
                "priority": priority
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 场景模拟失败: {e}")
            self.debug_logger.log_error(f"场景模拟失败: {e}")
            return {}
    
    def run_interactive_mode(self):
        """运行交互模式"""
        print("🎮 Luna模拟器 - 交互模式")
        print("=" * 50)
        print("可用命令:")
        print("  normal      - 正常场景")
        print("  crowded     - 拥挤场景")
        print("  obstacle    - 障碍物场景")
        print("  clear       - 路径畅通场景")
        print("  approaching - 靠近场景")
        print("  vehicle     - 车辆场景")
        print("  person      - 人员场景")
        print("  mixed       - 混合场景")
        print("  auto        - 自动模式")
        print("  status      - 显示状态")
        print("  quit        - 退出")
        print("=" * 50)
        
        self.running = True
        
        while self.running:
            try:
                command = input("\n请输入命令: ").strip().lower()
                
                if command == "quit":
                    self.running = False
                    break
                elif command == "status":
                    self._show_status()
                elif command == "auto":
                    self._run_auto_mode()
                elif command in self.dummy_generator.get_available_scenarios():
                    result = self.simulate_scenario(command)
                    self._display_result(result)
                else:
                    print(f"❌ 未知命令: {command}")
                    
            except KeyboardInterrupt:
                print("\n⚠️ 用户中断")
                break
            except Exception as e:
                print(f"❌ 命令执行失败: {e}")
        
        print("✅ 模拟器已退出")
    
    def _run_auto_mode(self):
        """运行自动模式"""
        print("🤖 自动模式启动")
        print("按 Ctrl+C 停止自动模式")
        
        scenarios = self.dummy_generator.get_available_scenarios()
        
        try:
            while True:
                scenario = scenarios[self.frame_count % len(scenarios)]
                result = self.simulate_scenario(scenario)
                self._display_result(result)
                
                time.sleep(self.auto_interval)
                
        except KeyboardInterrupt:
            print("\n⚠️ 自动模式已停止")
    
    def _display_result(self, result: Dict[str, Any]):
        """显示模拟结果"""
        if not result:
            return
        
        print(f"\n📊 场景: {result['scenario']}")
        print(f"帧数: {result['frame_count']}")
        print(f"检测数量: {len(result['detections'])}")
        print(f"跟踪数量: {len(result['tracks'])}")
        print(f"路径状态: {'阻塞' if result['path_prediction']['obstructed'] else '畅通'}")
        
        if result['should_speak']:
            print(f"🗣️ 播报: {result['speech_text']} (优先级: {result['priority']})")
        
        # 显示检测详情
        if result['detections']:
            print("检测详情:")
            for i, detection in enumerate(result['detections']):
                print(f"  {i+1}. {detection['class_name']} (置信度: {detection['confidence']:.2f})")
    
    def _show_status(self):
        """显示状态"""
        print("\n📊 系统状态:")
        print(f"当前场景: {self.current_scenario}")
        print(f"帧数: {self.frame_count}")
        print(f"自动模式: {'启用' if self.auto_mode else '禁用'}")
        
        # 显示冷却状态
        cooldown_status = self.cooldown_manager.get_cooldown_status()
        print(f"冷却状态: {cooldown_status}")
        
        # 显示状态跟踪
        state_count = self.state_tracker.get_state_count()
        print(f"状态数量: {state_count}")
        
        # 显示语音引擎状态
        speech_status = self.speech_engine.get_status()
        print(f"语音引擎状态: {speech_status}")
    
    def run_command_mode(self, scenario: str, count: int = 1):
        """运行命令模式"""
        print(f"🎮 Luna模拟器 - 命令模式")
        print(f"场景: {scenario}")
        print(f"次数: {count}")
        print("=" * 50)
        
        for i in range(count):
            result = self.simulate_scenario(scenario)
            self._display_result(result)
            
            if i < count - 1:
                time.sleep(1)
        
        print("✅ 命令模式完成")
    
    def run_test_suite(self):
        """运行测试套件"""
        print("🧪 Luna模拟器 - 测试套件")
        print("=" * 50)
        
        scenarios = self.dummy_generator.get_available_scenarios()
        
        for scenario in scenarios:
            print(f"\n测试场景: {scenario}")
            result = self.simulate_scenario(scenario)
            self._display_result(result)
            time.sleep(2)
        
        print("\n✅ 测试套件完成")
    
    def cleanup(self):
        """清理资源"""
        try:
            # 停止语音引擎
            if self.speech_engine:
                self.speech_engine.stop()
            
            # 保存状态
            if self.state_tracker:
                self.state_tracker.save()
            
            # 导出调试日志
            if self.debug_logger:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                log_file = f"logs/simulator_debug_{timestamp}.json"
                self.debug_logger.export_logs(log_file)
            
            logger.info("✅ 模拟器清理完成")
            
        except Exception as e:
            logger.error(f"❌ 模拟器清理失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Luna模拟器 - 本地模拟测试工具")
    parser.add_argument("--scenario", "-s", help="指定场景名称")
    parser.add_argument("--count", "-c", type=int, default=1, help="执行次数")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--test", "-t", action="store_true", help="运行测试套件")
    parser.add_argument("--auto", "-a", action="store_true", help="自动模式")
    
    args = parser.parse_args()
    
    # 创建模拟器
    simulator = LunaSimulator()
    
    try:
        if args.interactive:
            # 交互模式
            simulator.run_interactive_mode()
        elif args.test:
            # 测试套件
            simulator.run_test_suite()
        elif args.scenario:
            # 命令模式
            simulator.run_command_mode(args.scenario, args.count)
        else:
            # 默认交互模式
            simulator.run_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"❌ 模拟器运行失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulator.cleanup()

if __name__ == "__main__":
    main()
