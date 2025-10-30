"""
Luna Badge 模块基类
所有模块需要继承此基类并实现标准接口
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class ModuleState(Enum):
    """模块状态"""
    REGISTERED = "registered"     # 已注册
    ACTIVE = "active"             # 运行中
    SUSPENDED = "suspended"       # 已挂起
    STOPPED = "stopped"           # 已停止
    ERROR = "error"               # 错误状态


@dataclass
class ModuleStatus:
    """模块状态信息"""
    name: str
    state: ModuleState
    version: str
    start_time: Optional[float] = None
    last_update: float = time.time()
    error_count: int = 0
    last_error: Optional[str] = None
    health_score: float = 100.0  # 健康分数 0-100
    custom_info: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = asdict(self)
        result['state'] = self.state.value
        if self.custom_info is None:
            result['custom_info'] = {}
        return result


class BaseModule(ABC):
    """模块基类"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """
        初始化模块
        
        Args:
            name: 模块名称
            version: 模块版本
        """
        self.name = name
        self.version = version
        self.logger = logging.getLogger(f"module.{name}")
        self.state = ModuleState.REGISTERED
        self.start_time: Optional[float] = None
        self.error_count = 0
        self.last_error: Optional[str] = None
        self.custom_info: Dict[str, Any] = {}
        
        self.logger.info(f"📦 模块 {name} v{version} 初始化完成")
    
    @abstractmethod
    def _initialize(self) -> bool:
        """
        模块初始化逻辑（子类实现）
        
        Returns:
            bool: 是否初始化成功
        """
        pass
    
    @abstractmethod
    def _cleanup(self):
        """模块清理逻辑（子类实现）"""
        pass
    
    def start(self) -> bool:
        """
        启动模块
        
        Returns:
            bool: 是否启动成功
        """
        if self.state == ModuleState.ACTIVE:
            self.logger.warning(f"⚠️ 模块 {self.name} 已在运行中")
            return True
        
        try:
            self.logger.info(f"🚀 启动模块 {self.name}...")
            
            if self._initialize():
                self.state = ModuleState.ACTIVE
                self.start_time = time.time()
                self.logger.info(f"✅ 模块 {self.name} 启动成功")
                return True
            else:
                self.state = ModuleState.ERROR
                self.logger.error(f"❌ 模块 {self.name} 初始化失败")
                return False
                
        except Exception as e:
            self.state = ModuleState.ERROR
            self.error_count += 1
            self.last_error = str(e)
            self.logger.error(f"❌ 模块 {self.name} 启动异常: {e}")
            return False
    
    def stop(self) -> bool:
        """
        停止模块
        
        Returns:
            bool: 是否停止成功
        """
        if self.state == ModuleState.STOPPED:
            self.logger.warning(f"⚠️ 模块 {self.name} 已停止")
            return True
        
        try:
            self.logger.info(f"🛑 停止模块 {self.name}...")
            self._cleanup()
            self.state = ModuleState.STOPPED
            self.start_time = None
            self.logger.info(f"✅ 模块 {self.name} 已停止")
            return True
            
        except Exception as e:
            self.state = ModuleState.ERROR
            self.error_count += 1
            self.last_error = str(e)
            self.logger.error(f"❌ 模块 {self.name} 停止异常: {e}")
            return False
    
    def suspend(self) -> bool:
        """
        挂起模块
        
        Returns:
            bool: 是否挂起成功
        """
        if self.state != ModuleState.ACTIVE:
            self.logger.warning(f"⚠️ 模块 {self.name} 状态为 {self.state.value}，无法挂起")
            return False
        
        try:
            self.logger.info(f"⏸️ 挂起模块 {self.name}...")
            self.state = ModuleState.SUSPENDED
            self.logger.info(f"✅ 模块 {self.name} 已挂起")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 模块 {self.name} 挂起异常: {e}")
            return False
    
    def resume(self) -> bool:
        """
        恢复模块（从挂起状态恢复）
        
        Returns:
            bool: 是否恢复成功
        """
        if self.state != ModuleState.SUSPENDED:
            self.logger.warning(f"⚠️ 模块 {self.name} 状态为 {self.state.value}，无法恢复")
            return False
        
        try:
            self.logger.info(f"▶️ 恢复模块 {self.name}...")
            self.state = ModuleState.ACTIVE
            self.logger.info(f"✅ 模块 {self.name} 已恢复")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 模块 {self.name} 恢复异常: {e}")
            return False
    
    def restart(self) -> bool:
        """
        重启模块
        
        Returns:
            bool: 是否重启成功
        """
        self.logger.info(f"🔄 重启模块 {self.name}...")
        was_active = self.state == ModuleState.ACTIVE
        self.stop()
        if was_active:
            return self.start()
        return True
    
    def get_status(self) -> ModuleStatus:
        """
        获取模块状态
        
        Returns:
            ModuleStatus: 模块状态信息
        """
        # 计算健康分数
        health_score = 100.0
        if self.error_count > 0:
            health_score = max(0, 100 - (self.error_count * 10))
        
        return ModuleStatus(
            name=self.name,
            state=self.state,
            version=self.version,
            start_time=self.start_time,
            last_update=time.time(),
            error_count=self.error_count,
            last_error=self.last_error,
            health_score=health_score,
            custom_info=self.custom_info.copy()
        )
    
    def inject_config(self, config: Dict[str, Any]) -> bool:
        """
        注入动态配置
        
        Args:
            config: 配置字典
        
        Returns:
            bool: 是否注入成功
        """
        try:
            self.logger.info(f"⚙️ 向模块 {self.name} 注入配置...")
            # 子类可以实现此方法来处理配置注入
            self.custom_info.update(config)
            self.logger.info(f"✅ 配置注入成功")
            return True
        except Exception as e:
            self.logger.error(f"❌ 配置注入失败: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查（子类可重写）
        
        Returns:
            Dict[str, Any]: 健康检查结果
        """
        return {
            "healthy": self.state == ModuleState.ACTIVE,
            "state": self.state.value,
            "error_count": self.error_count,
            "uptime": time.time() - self.start_time if self.start_time else 0
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📦 模块基类测试")
    print("=" * 70)
    
    # 测试模块基类（需要子类实现）
    class TestModule(BaseModule):
        def _initialize(self):
            return True
        
        def _cleanup(self):
            pass
    
    module = TestModule("test_module", "1.0.0")
    print(f"\n模块状态: {module.get_status().to_dict()}")
    
    module.start()
    print(f"启动后状态: {module.get_status().to_dict()}")
    
    module.suspend()
    print(f"挂起后状态: {module.get_status().to_dict()}")
    
    module.resume()
    print(f"恢复后状态: {module.get_status().to_dict()}")
    
    module.stop()
    print(f"停止后状态: {module.get_status().to_dict()}")
    
    print("\n" + "=" * 70)
