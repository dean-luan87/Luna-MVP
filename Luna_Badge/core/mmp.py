"""
Luna Badge 模块管理平台 (Module Management Platform)
核心控制系统，负责模块的状态管理、调度和监控
"""

import logging
import threading
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from module_registry import ModuleRegistry, get_module_registry
from base_module import BaseModule, ModuleState

logger = logging.getLogger(__name__)


class ModuleManagementPlatform:
    """模块管理平台"""
    
    def __init__(self):
        """初始化MMP"""
        self.registry = get_module_registry()
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_running = False
        self.monitor_interval = 30  # 30秒监控一次
        
        logger.info("🎯 模块管理平台 (MMP) 初始化完成")
    
    def register_module(self, name: str, module: BaseModule, dependencies: Optional[List[str]] = None):
        """
        注册模块
        
        Args:
            name: 模块名称
            module: 模块实例
            dependencies: 依赖的模块列表
        """
        self.registry.register(name, module, dependencies)
    
    def unregister_module(self, name: str) -> bool:
        """注销模块"""
        return self.registry.unregister(name)
    
    def list_registered(self) -> List[str]:
        """列出所有已注册的模块"""
        return self.registry.list_registered()
    
    def start_module(self, name: str) -> bool:
        """启动指定模块"""
        return self.registry.start_module(name)
    
    def stop_module(self, name: str) -> bool:
        """停止指定模块"""
        return self.registry.stop_module(name)
    
    def restart_module(self, name: str) -> bool:
        """重启指定模块"""
        return self.registry.restart_module(name)
    
    def suspend_module(self, name: str) -> bool:
        """挂起指定模块"""
        return self.registry.suspend_module(name)
    
    def resume_module(self, name: str) -> bool:
        """恢复指定模块"""
        return self.registry.resume_module(name)
    
    def get_module_status(self, name: str) -> Optional[Dict[str, Any]]:
        """获取指定模块状态"""
        module = self.registry.get_module(name)
        if module:
            return module.get_status().to_dict()
        return None
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """获取所有模块状态"""
        return self.registry.get_all_status()
    
    def inject_config(self, module_name: str, config: Dict[str, Any]) -> bool:
        """
        向指定模块注入配置
        
        Args:
            module_name: 模块名称
            config: 配置字典
        
        Returns:
            bool: 是否注入成功
        """
        module = self.registry.get_module(module_name)
        if module:
            return module.inject_config(config)
        logger.error(f"❌ 模块 {module_name} 不存在")
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        系统健康检查
        
        Returns:
            Dict[str, Any]: 健康检查结果
        """
        status = self.get_all_status()
        
        total_modules = len(status)
        active_modules = sum(1 for s in status.values() if s['state'] == 'active')
        error_modules = sum(1 for s in status.values() if s['state'] == 'error')
        
        total_health_score = sum(s.get('health_score', 0) for s in status.values())
        avg_health_score = total_health_score / total_modules if total_modules > 0 else 0
        
        # 计算系统整体健康度
        system_health = "healthy" if error_modules == 0 and avg_health_score > 80 else \
                       "degraded" if error_modules < total_modules / 2 else "critical"
        
        return {
            "system_health": system_health,
            "total_modules": total_modules,
            "active_modules": active_modules,
            "suspended_modules": sum(1 for s in status.values() if s['state'] == 'suspended'),
            "stopped_modules": sum(1 for s in status.values() if s['state'] == 'stopped'),
            "error_modules": error_modules,
            "average_health_score": avg_health_score,
            "timestamp": time.time()
        }
    
    def start_monitor(self):
        """启动监控线程"""
        if self.monitor_running:
            logger.warning("⚠️ 监控线程已在运行")
            return
        
        self.monitor_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("📊 模块监控线程已启动")
    
    def stop_monitor(self):
        """停止监控线程"""
        self.monitor_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("📊 模块监控线程已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitor_running:
            try:
                # 保存运行时状态
                self.registry.save_runtime_state()
                
                # 执行健康检查
                health = self.health_check()
                
                # 如果有错误模块，记录日志
                if health['error_modules'] > 0:
                    logger.warning(f"⚠️ 检测到 {health['error_modules']} 个模块处于错误状态")
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                logger.error(f"❌ 监控循环异常: {e}")
                time.sleep(self.monitor_interval)
    
    def start_all_modules(self, order: Optional[List[str]] = None) -> Dict[str, bool]:
        """启动所有模块"""
        return self.registry.start_all(order)
    
    def stop_all_modules(self, reverse_order: bool = True) -> Dict[str, bool]:
        """停止所有模块"""
        return self.registry.stop_all(reverse_order)
    
    def get_runtime_state(self) -> Dict[str, Any]:
        """获取运行时状态"""
        return self.registry.get_runtime_state()
    
    def print_status_report(self):
        """打印状态报告"""
        print("=" * 80)
        print(f"📊 Luna Badge 模块管理平台状态报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # 健康检查
        health = self.health_check()
        print(f"\n🏥 系统健康: {health['system_health'].upper()}")
        print(f"   总模块数: {health['total_modules']}")
        print(f"   活跃模块: {health['active_modules']}")
        print(f"   错误模块: {health['error_modules']}")
        print(f"   平均健康分数: {health['average_health_score']:.1f}")
        
        # 模块状态
        print("\n📦 模块状态:")
        status = self.get_all_status()
        for name, module_status in status.items():
            state_icon = {
                "active": "✅",
                "suspended": "⏸️",
                "stopped": "🛑",
                "error": "❌",
                "registered": "📝"
            }.get(module_status['state'], "❓")
            
            print(f"   {state_icon} {name:<20} {module_status['state']:<12} "
                  f"健康分数: {module_status.get('health_score', 0):.1f}")
            if module_status.get('last_error'):
                print(f"      ⚠️  最后错误: {module_status['last_error']}")
        
        print("\n" + "=" * 80)


# 全局MMP实例
_global_mmp: Optional[ModuleManagementPlatform] = None


def get_mmp() -> ModuleManagementPlatform:
    """获取全局MMP实例"""
    global _global_mmp
    if _global_mmp is None:
        _global_mmp = ModuleManagementPlatform()
    return _global_mmp


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    from base_module import BaseModule
    
    # 创建测试模块
    class TestModule(BaseModule):
        def _initialize(self):
            return True
        def _cleanup(self):
            pass
    
    # 初始化MMP
    mmp = ModuleManagementPlatform()
    
    # 注册测试模块
    mmp.register_module("test1", TestModule("test1"))
    mmp.register_module("test2", TestModule("test2"))
    
    # 启动所有模块
    print("\n🚀 启动所有模块...")
    mmp.start_all_modules()
    
    # 打印状态报告
    mmp.print_status_report()
    
    # 测试重启
    print("\n🔄 重启模块 test1...")
    mmp.restart_module("test1")
    
    # 测试挂起/恢复
    print("\n⏸️ 挂起模块 test2...")
    mmp.suspend_module("test2")
    
    print("\n▶️ 恢复模块 test2...")
    mmp.resume_module("test2")
    
    # 打印最终状态
    print("\n📊 最终状态:")
    mmp.print_status_report()
    
    # 停止所有模块
    print("\n🛑 停止所有模块...")
    mmp.stop_all_modules()

