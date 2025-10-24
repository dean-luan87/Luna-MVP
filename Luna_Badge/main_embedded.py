#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 嵌入式运行入口
"""

import sys
import os
import time
import signal
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import (
    ConfigManager, SystemControl, SystemState, ErrorCode, 
    AINavigation, config_manager
)
from hal_embedded import EmbeddedHAL

class LunaBadgeEmbedded:
    """Luna Badge 嵌入式版本主控制器"""
    
    def __init__(self):
        """初始化Luna Badge 嵌入式版本"""
        self.config_manager = config_manager
        self.system_control = SystemControl()
        self.ai_navigation = AINavigation()
        self.hal_interface = EmbeddedHAL()
        
        self.is_running = False
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n收到信号 {signum}，正在关闭系统...")
        self.shutdown()
        sys.exit(0)
    
    def initialize(self) -> bool:
        """
        初始化系统
        
        Returns:
            初始化是否成功
        """
        try:
            print("🚀 初始化Luna Badge 嵌入式版本...")
            
            # 加载配置
            config = self.config_manager.load_config()
            print(f"✅ 配置加载成功: {config['platform']}")
            
            # 初始化硬件抽象层
            if not self.hal_interface.initialize():
                print("❌ 硬件抽象层初始化失败")
                return False
            print("✅ 硬件抽象层初始化成功")
            
            # 设置系统控制的硬件接口
            self.system_control.set_hal_interface(self.hal_interface)
            
            # 初始化AI导航
            if not self.ai_navigation.initialize_modules():
                print("❌ AI导航模块初始化失败")
                return False
            print("✅ AI导航模块初始化成功")
            
            # 设置AI导航的硬件接口
            self.ai_navigation.set_hal_interface(self.hal_interface)
            
            # 添加状态变化回调
            self.system_control.add_state_change_callback(self._on_state_change)
            self.system_control.add_error_callback(self._on_error)
            
            print("🎉 Luna Badge 嵌入式版本初始化完成")
            return True
            
        except Exception as e:
            print(f"❌ 系统初始化失败: {e}")
            return False
    
    def _on_state_change(self, previous_state: SystemState, current_state: SystemState):
        """状态变化回调"""
        print(f"🔄 系统状态变化: {previous_state.value} -> {current_state.value}")
    
    def _on_error(self, error_entry: Dict[str, str]):
        """错误回调"""
        print(f"⚠️ 系统错误: [{error_entry['code']}] {error_entry['message']}")
    
    def start(self) -> bool:
        """
        启动系统
        
        Returns:
            启动是否成功
        """
        try:
            print("🔋 启动Luna Badge系统...")
            
            # 系统开机
            if not self.system_control.power_on():
                print("❌ 系统开机失败")
                return False
            
            # 启动AI导航
            if not self.ai_navigation.start_auto_navigation():
                print("❌ AI导航启动失败")
                return False
            
            self.is_running = True
            print("🎉 Luna Badge系统启动成功")
            return True
            
        except Exception as e:
            print(f"❌ 系统启动失败: {e}")
            return False
    
    def run(self):
        """运行系统主循环"""
        try:
            print("🔄 开始系统主循环...")
            
            # 启动系统控制循环
            system_thread = threading.Thread(target=self.system_control.system_loop, daemon=True)
            system_thread.start()
            
            # 主循环
            while self.is_running:
                try:
                    # 检查系统状态
                    status = self.system_control.get_status()
                    print(f"📊 系统状态: {status['current_state']}")
                    
                    # 检查AI导航状态
                    ai_status = self.ai_navigation.get_status()
                    print(f"🤖 AI导航状态: {ai_status['is_running']}")
                    
                    # 等待一段时间
                    time.sleep(5)
                    
                except KeyboardInterrupt:
                    print("\n⚠️ 用户中断")
                    break
                except Exception as e:
                    print(f"❌ 主循环异常: {e}")
                    time.sleep(1)
            
            print("🔄 系统主循环结束")
            
        except Exception as e:
            print(f"❌ 系统运行失败: {e}")
    
    def shutdown(self):
        """关闭系统"""
        try:
            print("🔌 关闭Luna Badge系统...")
            
            self.is_running = False
            
            # 停止AI导航
            self.ai_navigation.stop_auto_navigation()
            
            # 系统关机
            self.system_control.power_off()
            
            # 清理硬件资源
            self.hal_interface.cleanup()
            
            print("✅ 系统关闭完成")
            
        except Exception as e:
            print(f"❌ 系统关闭失败: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "system": self.system_control.get_status(),
            "ai_navigation": self.ai_navigation.get_status(),
            "hardware": self.hal_interface.get_hardware_info(),
            "config": self.config_manager.get_config("platform")
        }

def main():
    """主函数"""
    print("🌟 Luna Badge - 嵌入式版本")
    print("=" * 50)
    
    # 创建Luna Badge实例
    luna_badge = LunaBadgeEmbedded()
    
    try:
        # 初始化系统
        if not luna_badge.initialize():
            print("❌ 系统初始化失败，退出")
            return 1
        
        # 启动系统
        if not luna_badge.start():
            print("❌ 系统启动失败，退出")
            return 1
        
        # 运行系统
        luna_badge.run()
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    except Exception as e:
        print(f"❌ 系统运行异常: {e}")
    finally:
        # 关闭系统
        luna_badge.shutdown()
    
    print("👋 再见！")
    return 0

if __name__ == "__main__":
    import threading
    sys.exit(main())
