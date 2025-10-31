#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 增强版模块注册表
P1-2: 统一模块管理

功能:
- 模块注册和生命周期管理
- 依赖关系管理
- 自动启动顺序
- 健康监控
- 事件总线集成
"""

import logging
import time
from typing import Dict, List, Optional, Type, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

# 导入基础模块
try:
    from core.base_module import BaseModule, ModuleState
except ImportError:
    # 如果base_module不存在，定义基础类
    from enum import Enum
    
    class ModuleState(Enum):
        REGISTERED = "registered"
        ACTIVE = "active"
        SUSPENDED = "suspended"
        STOPPED = "stopped"
        ERROR = "error"
    
    class BaseModule:
        def __init__(self, name: str, version: str = "1.0.0"):
            self.name = name
            self.version = version
            self.state = ModuleState.REGISTERED
        def start(self): pass
        def stop(self): pass

logger = logging.getLogger(__name__)


@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    module: BaseModule
    dependencies: List[str]
    auto_start: bool = True
    priority: int = 0
    registered_at: float = 0


class EnhancedModuleRegistry:
    """
    增强版模块注册表
    
    功能:
    1. 模块注册和发现
    2. 依赖关系管理
    3. 自动启动顺序
    4. 健康监控
    5. 事件总线集成
    """
    
    def __init__(self):
        """初始化模块注册表"""
        # 模块字典：{name: ModuleInfo}
        self.modules: Dict[str, ModuleInfo] = {}
        
        # 依赖关系图
        self.dependencies: Dict[str, List[str]] = defaultdict(list)
        self.dependents: Dict[str, List[str]] = defaultdict(list)
        
        # 启动顺序缓存
        self.startup_order: List[str] = []
        self._order_dirty = True
        
        logger.info("📚 增强版模块注册表初始化完成")
    
    def register(self,
                 name: str,
                 module: BaseModule,
                 dependencies: Optional[List[str]] = None,
                 auto_start: bool = True,
                 priority: int = 0):
        """
        注册模块
        
        Args:
            name: 模块名称
            module: 模块实例
            dependencies: 依赖的模块列表
            auto_start: 是否自动启动
            priority: 优先级（数字越小优先级越高）
        """
        if name in self.modules:
            logger.warning(f"⚠️ 模块 {name} 已存在，将被覆盖")
        
        deps = dependencies or []
        module_info = ModuleInfo(
            name=name,
            module=module,
            dependencies=deps,
            auto_start=auto_start,
            priority=priority,
            registered_at=time.time()
        )
        
        self.modules[name] = module_info
        
        # 更新依赖关系
        self.dependencies[name] = deps
        for dep in deps:
            self.dependents[dep].append(name)
        
        # 标记启动顺序需要重新计算
        self._order_dirty = True
        
        logger.info(f"✅ 模块 {name} 已注册 (依赖: {deps if deps else '无'})")
    
    def unregister(self, name: str) -> bool:
        """
        注销模块
        
        Args:
            name: 模块名称
            
        Returns:
            是否注销成功
        """
        if name not in self.modules:
            logger.warning(f"⚠️ 模块 {name} 不存在")
            return False
        
        # 停止模块
        module_info = self.modules[name]
        if module_info.module.state == ModuleState.ACTIVE:
            module_info.module.stop()
        
        # 移除依赖关系
        if name in self.dependencies:
            del self.dependencies[name]
        
        if name in self.dependents:
            deps = self.dependents.pop(name)
            for dep in deps:
                if name in self.dependencies.get(dep, []):
                    self.dependencies[dep].remove(name)
        
        del self.modules[name]
        self._order_dirty = True
        
        logger.info(f"✅ 模块 {name} 已注销")
        return True
    
    def get_module(self, name: str) -> Optional[BaseModule]:
        """
        获取模块实例
        
        Args:
            name: 模块名称
            
        Returns:
            模块实例或None
        """
        return self.modules.get(name, ModuleInfo(name="", module=None, dependencies=[])).module
    
    def get_module_info(self, name: str) -> Optional[ModuleInfo]:
        """获取模块信息"""
        return self.modules.get(name)
    
    def _calculate_startup_order(self) -> List[str]:
        """
        计算模块启动顺序（拓扑排序）
        
        返回拓扑排序后的模块名称列表
        """
        if not self._order_dirty:
            return self.startup_order.copy()
        
        # 使用拓扑排序计算启动顺序
        order = []
        in_degree = {name: len(self.dependencies.get(name, [])) for name in self.modules}
        queue = [name for name, degree in in_degree.items() if degree == 0]
        
        while queue:
            # 按优先级排序
            queue.sort(key=lambda n: self.modules[n].priority)
            
            current = queue.pop(0)
            order.append(current)
            
            # 减少依赖此模块的其他模块的入度
            for dependent in self.dependents.get(current, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        # 检查是否有循环依赖
        if len(order) < len(self.modules):
            remaining = set(self.modules.keys()) - set(order)
            logger.error(f"❌ 检测到循环依赖: {remaining}")
        
        self.startup_order = order
        self._order_dirty = False
        
        return order
    
    def start_module(self, name: str, start_dependencies: bool = True) -> bool:
        """
        启动模块
        
        Args:
            name: 模块名称
            start_dependencies: 是否启动依赖模块
            
        Returns:
            是否启动成功
        """
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        
        module_info = self.modules[name]
        
        # 检查依赖
        if start_dependencies:
            for dep_name in module_info.dependencies:
                if dep_name not in self.modules:
                    logger.error(f"❌ 模块 {name} 的依赖 {dep_name} 不存在")
                    return False
                
                dep_module_info = self.modules[dep_name]
                if dep_module_info.module.state != ModuleState.ACTIVE:
                    logger.info(f"🔄 启动依赖模块 {dep_name}...")
                    if not self.start_module(dep_name, start_dependencies=True):
                        logger.error(f"❌ 无法启动依赖模块 {dep_name}")
                        return False
        
        # 启动模块
        return module_info.module.start()
    
    def stop_module(self, name: str) -> bool:
        """
        停止模块
        
        Args:
            name: 模块名称
            
        Returns:
            是否停止成功
        """
        if name not in self.modules:
            logger.error(f"❌ 模块 {name} 不存在")
            return False
        
        module_info = self.modules[name]
        
        # 检查是否被其他模块依赖
        dependents = self.dependents.get(name, [])
        active_dependents = [dep for dep in dependents if self.modules[dep].module.state == ModuleState.ACTIVE]
        
        if active_dependents:
            logger.warning(f"⚠️ 以下活跃模块依赖 {name}: {active_dependents}")
        
        return module_info.module.stop()
    
    def start_all(self, include_non_auto: bool = False) -> Dict[str, bool]:
        """
        启动所有模块
        
        Args:
            include_non_auto: 是否包括非自动启动的模块
            
        Returns:
            每个模块的启动结果
        """
        order = self._calculate_startup_order()
        
        if include_non_auto:
            names_to_start = order
        else:
            names_to_start = [name for name in order if self.modules[name].auto_start]
        
        results = {}
        for name in names_to_start:
            results[name] = self.start_module(name, start_dependencies=False)
            time.sleep(0.1)  # 短暂延迟
        
        logger.info(f"📊 启动完成: {sum(results.values())}/{len(results)} 个模块成功")
        return results
    
    def stop_all(self, reverse_order: bool = True) -> Dict[str, bool]:
        """
        停止所有模块
        
        Args:
            reverse_order: 是否按反向顺序停止
            
        Returns:
            每个模块的停止结果
        """
        if reverse_order:
            order = list(reversed(self._calculate_startup_order()))
        else:
            order = self._calculate_startup_order()
        
        results = {}
        for name in order:
            results[name] = self.stop_module(name)
            time.sleep(0.1)
        
        logger.info(f"📊 停止完成: {sum(results.values())}/{len(results)} 个模块成功")
        return results
    
    def list_modules(self) -> List[str]:
        """列出所有已注册的模块"""
        return list(self.modules.keys())
    
    def get_module_status(self) -> Dict[str, Dict]:
        """获取所有模块状态"""
        status = {}
        for name, info in self.modules.items():
            status[name] = {
                "name": name,
                "version": info.module.version if hasattr(info.module, 'version') else "unknown",
                "state": info.module.state.value if hasattr(info.module.state, 'value') else str(info.module.state),
                "dependencies": info.dependencies,
                "auto_start": info.auto_start,
                "priority": info.priority
            }
        return status
    
    def check_health(self) -> Dict[str, Any]:
        """
        检查模块健康状态
        
        Returns:
            健康检查结果
        """
        total = len(self.modules)
        active = sum(1 for m in self.modules.values() if m.module.state == ModuleState.ACTIVE)
        stopped = sum(1 for m in self.modules.values() if m.module.state == ModuleState.STOPPED)
        error = sum(1 for m in self.modules.values() if m.module.state == ModuleState.ERROR)
        
        return {
            "total": total,
            "active": active,
            "stopped": stopped,
            "error": error,
            "health_score": (active / total * 100) if total > 0 else 0
        }


# 全局模块注册表实例
_global_registry: Optional[EnhancedModuleRegistry] = None


def get_module_registry() -> EnhancedModuleRegistry:
    """获取全局模块注册表实例"""
    global _global_registry
    if _global_registry is None:
        _global_registry = EnhancedModuleRegistry()
    return _global_registry


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📚 增强版模块注册表测试")
    print("=" * 70)
    
    registry = EnhancedModuleRegistry()
    
    # 创建测试模块
    class TestModule(BaseModule):
        def __init__(self, name: str, version: str = "1.0.0"):
            super().__init__(name, version)
            self.state = ModuleState.REGISTERED
        def start(self):
            self.state = ModuleState.ACTIVE
            print(f"  ✅ {self.name} 启动")
            return True
        def stop(self):
            self.state = ModuleState.STOPPED
            print(f"  🛑 {self.name} 停止")
            return True
    
    # 注册模块
    module1 = TestModule("module1")
    module2 = TestModule("module2")
    module3 = TestModule("module3")
    
    registry.register("module1", module1, priority=1)
    registry.register("module2", module2, dependencies=["module1"], priority=2)
    registry.register("module3", module3, dependencies=["module1"], priority=3)
    
    print(f"\n已注册模块: {registry.list_modules()}")
    
    # 计算启动顺序
    order = registry._calculate_startup_order()
    print(f"启动顺序: {order}")
    
    # 启动所有模块
    print("\n启动所有模块:")
    registry.start_all()
    
    # 获取状态
    status = registry.get_module_status()
    print(f"\n模块状态:")
    for name, state in status.items():
        print(f"  - {name}: {state['state']}")
    
    # 健康检查
    health = registry.check_health()
    print(f"\n健康状态:")
    print(f"  总计: {health['total']}")
    print(f"  活跃: {health['active']}")
    print(f"  健康分: {health['health_score']:.1f}%")
    
    print("\n" + "=" * 70)

