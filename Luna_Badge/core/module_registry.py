"""
Luna Badge 模块注册表
负责模块的注册、调度和管理
"""

import logging
import os
import json
import time
from typing import Dict, List, Optional, Type
from pathlib import Path

from base_module import BaseModule, ModuleState

logger = logging.getLogger(__name__)


class ModuleRegistry:
    """模块注册表"""
    
    def __init__(self, runtime_state_file: str = "core/runtime_state.json"):
        """
        初始化模块注册表
        
        Args:
            runtime_state_file: 运行时状态文件路径
        """
        self.modules: Dict[str, BaseModule] = {}
        self.module_order: List[str] = []  # 模块加载顺序
        self.runtime_state_file = runtime_state_file
        self.dependencies: Dict[str, List[str]] = {}  # 模块依赖关系
        
        # 确保日志目录存在
        log_dir = Path("logs/modules")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("📚 模块注册表初始化完成")
    
    def register(self, name: str, module: BaseModule, dependencies: Optional[List[str]] = None):
        """
        注册模块
        
        Args:
            name: 模块名称
            module: 模块实例
            dependencies: 依赖的模块列表
        """
        if name in self.modules:
            logger.warning(f"⚠️ 模块 {name} 已存在，将被覆盖")
        
        self.modules[name] = module
        if name not in self.module_order:
            self.module_order.append(name)
        
        if dependencies:
            self.dependencies[name] = dependencies
        
        logger.info(f"✅ 模块 {name} 已注册")
    
    def unregister(self, name: str) -> bool:
        """
        注销模块
        
        Args:
            name: 模块名称
        
        Returns:
            bool: 是否注销成功
        """
        if name not in self.modules:
            logger.warning(f"⚠️ 模块 {name} 不存在")
            return False
        
        # 停止模块
        if self.modules[name].state == ModuleState.ACTIVE:
            self.modules[name].stop()
        
        del self.modules[name]
        if name in self.module_order:
            self.module_order.remove(name)
        
        if name in self.dependencies:
            del self.dependencies[name]
        
        logger.info(f"✅ 模块 {name} 已注销")
        return True
    
    def get_module(self, name: str) -> Optional[BaseModule]:
        """获取模块实例"""
        return self.modules.get(name)
    
    def list_registered(self) -> List[str]:
        """列出所有已注册的模块"""
        return self.module_order.copy()
    
    def start_module(self, name: str) -> bool:
        """
        启动模块
        
        Args:
            name: 模块名称
        
        Returns:
            bool: 是否启动成功
        """
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        
        # 检查依赖
        if name in self.dependencies:
            for dep_name in self.dependencies[name]:
                if dep_name not in self.modules:
                    logger.error(f"❌ 模块 {name} 的依赖 {dep_name} 不存在")
                    return False
                if self.modules[dep_name].state != ModuleState.ACTIVE:
                    logger.warning(f"⚠️ 依赖模块 {dep_name} 未运行，正在启动...")
                    if not self.start_module(dep_name):
                        logger.error(f"❌ 无法启动依赖模块 {dep_name}")
                        return False
        
        return self.modules[name].start()
    
    def stop_module(self, name: str) -> bool:
        """
        停止模块
        
        Args:
            name: 模块名称
        
        Returns:
            bool: 是否停止成功
        """
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        
        # 检查是否有其他模块依赖此模块
        dependents = [m for m, deps in self.dependencies.items() if name in deps]
        if dependents:
            logger.warning(f"⚠️ 以下模块依赖 {name}，停止可能导致问题: {dependents}")
        
        return self.modules[name].stop()
    
    def restart_module(self, name: str) -> bool:
        """
        重启模块
        
        Args:
            name: 模块名称
        
        Returns:
            bool: 是否重启成功
        """
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        
        logger.info(f"🔄 重启模块 {name}...")
        return self.modules[name].restart()
    
    def suspend_module(self, name: str) -> bool:
        """挂起模块"""
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        return self.modules[name].suspend()
    
    def resume_module(self, name: str) -> bool:
        """恢复模块"""
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        return self.modules[name].resume()
    
    def start_all(self, order: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        启动所有模块（按顺序）
        
        Args:
            order: 启动顺序，如果为None则使用注册顺序
        
        Returns:
            Dict[str, bool]: 每个模块的启动结果
        """
        if order is None:
            order = self.module_order
        
        results = {}
        for name in order:
            if name in self.modules:
                results[name] = self.start_module(name)
                time.sleep(0.1)  # 短暂延迟，避免资源竞争
        
        logger.info(f"📊 启动完成: {sum(results.values())}/{len(results)} 个模块成功")
        return results
    
    def stop_all(self, reverse_order: bool = True) -> Dict[str, bool]:
        """
        停止所有模块
        
        Args:
            reverse_order: 是否按反向顺序停止
        
        Returns:
            Dict[str, bool]: 每个模块的停止结果
        """
        order = reversed(self.module_order) if reverse_order else self.module_order
        results = {}
        
        for name in order:
            if name in self.modules:
                results[name] = self.stop_module(name)
                time.sleep(0.1)
        
        logger.info(f"📊 停止完成: {sum(results.values())}/{len(results)} 个模块成功")
        return results
    
    def get_all_status(self) -> Dict[str, dict]:
        """
        获取所有模块状态
        
        Returns:
            Dict[str, dict]: 所有模块的状态信息
        """
        status = {}
        for name, module in self.modules.items():
            status[name] = module.get_status().to_dict()
        return status
    
    def get_runtime_state(self) -> Dict[str, any]:
        """
        获取运行时状态
        
        Returns:
            Dict[str, any]: 运行时状态信息
        """
        return {
            "timestamp": time.time(),
            "modules": self.get_all_status(),
            "module_count": len(self.modules),
            "active_count": sum(1 for m in self.modules.values() if m.state == ModuleState.ACTIVE),
            "suspended_count": sum(1 for m in self.modules.values() if m.state == ModuleState.SUSPENDED),
            "error_count": sum(1 for m in self.modules.values() if m.state == ModuleState.ERROR)
        }
    
    def save_runtime_state(self):
        """保存运行时状态到文件"""
        try:
            state = self.get_runtime_state()
            with open(self.runtime_state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            logger.debug(f"💾 运行时状态已保存: {self.runtime_state_file}")
        except Exception as e:
            logger.error(f"❌ 保存运行时状态失败: {e}")
    
    def load_runtime_state(self) -> Optional[Dict]:
        """从文件加载运行时状态"""
        try:
            if os.path.exists(self.runtime_state_file):
                with open(self.runtime_state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"❌ 加载运行时状态失败: {e}")
        return None


# 全局模块注册表实例
_global_registry: Optional[ModuleRegistry] = None


def get_module_registry() -> ModuleRegistry:
    """获取全局模块注册表实例"""
    global _global_registry
    if _global_registry is None:
        _global_registry = ModuleRegistry()
    return _global_registry


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📚 模块注册表测试")
    print("=" * 70)
    
    from base_module import BaseModule, ModuleState
    
    # 创建测试模块
    class TestModule(BaseModule):
        def _initialize(self):
            return True
        def _cleanup(self):
            pass
    
    # 测试注册表
    registry = ModuleRegistry()
    
    # 注册模块
    module1 = TestModule("module1", "1.0.0")
    module2 = TestModule("module2", "1.0.0")
    
    registry.register("module1", module1)
    registry.register("module2", module2, dependencies=["module1"])
    
    print(f"\n已注册模块: {registry.list_registered()}")
    
    # 启动模块
    registry.start_all()
    
    # 获取状态
    status = registry.get_all_status()
    print(f"\n模块状态:")
    for name, state in status.items():
        print(f"  - {name}: {state['state']}")
    
    # 运行时状态
    runtime_state = registry.get_runtime_state()
    print(f"\n运行时状态: 总计{runtime_state['module_count']}个模块，"
          f"活跃{runtime_state['active_count']}个")
    
    print("\n" + "=" * 70)
