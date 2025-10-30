"""
用户出行偏好学习模块
记录和学习用户的出行偏好
"""

import logging
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class UserPreferences:
    """用户偏好数据结构"""
    prefer_walk: bool = False           # 偏好步行
    avoid_transfer: bool = False        # 避免换乘
    prefer_shortest: bool = True        # 偏好最短路径
    prefer_fastest: bool = False        # 偏好最快路径
    avoid_crowded: bool = False         # 避免拥挤
    prefer_indoor: bool = False         # 偏好室内路线
    behavior_stats: Dict[str, int] = None  # 行为统计
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        if self.behavior_stats is None:
            self.behavior_stats = {}
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """从字典创建"""
        return cls(**data)


class UserProfileManager:
    """用户偏好管理器"""
    
    def __init__(self, profile_file: str = "data/user_profile.json"):
        """
        初始化用户偏好管理器
        
        Args:
            profile_file: 配置文件路径
        """
        self.profile_file = profile_file
        self.preferences = UserPreferences()
        self.behavior_history: List[Dict[str, Any]] = []
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(profile_file), exist_ok=True)
        
        self._load_profile()
        logger.info("👤 用户偏好管理器初始化完成")
    
    def _load_profile(self):
        """加载用户偏好"""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.preferences = UserPreferences.from_dict(data)
                logger.info(f"✅ 已加载用户偏好: {self.profile_file}")
            except Exception as e:
                logger.error(f"❌ 加载用户偏好失败: {e}")
    
    def _save_profile(self):
        """保存用户偏好"""
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences.to_dict(), f, ensure_ascii=False, indent=2)
            logger.debug("💾 用户偏好已保存")
        except Exception as e:
            logger.error(f"❌ 保存用户偏好失败: {e}")
    
    def record_route_choice(self, choice: str, route_type: str):
        """
        记录用户路线选择
        
        Args:
            choice: 选择类型 ("accept" | "reject" | "modify")
            route_type: 路线类型 ("walk" | "bus" | "metro" | "transfer")
        """
        event = {
            "choice": choice,
            "route_type": route_type,
            "timestamp": time.time()
        }
        self.behavior_history.append(event)
        
        # 更新统计
        if self.preferences.behavior_stats is None:
            self.preferences.behavior_stats = {}
        
        key = f"{choice}_{route_type}"
        self.preferences.behavior_stats[key] = self.preferences.behavior_stats.get(key, 0) + 1
        
        # 学习规则
        self._learn_preferences()
        
        # 保存
        self._save_profile()
        
        logger.info(f"📝 记录路线选择: {choice} - {route_type}")
    
    def _learn_preferences(self):
        """学习用户偏好"""
        if not self.preferences.behavior_stats:
            return
        
        stats = self.preferences.behavior_stats
        
        # 规则1: 连续3次放弃公交推荐 → avoid_transfer: true
        reject_bus_count = stats.get("reject_bus", 0) + stats.get("reject_transfer", 0)
        if reject_bus_count >= 3:
            if not self.preferences.avoid_transfer:
                self.preferences.avoid_transfer = True
                logger.info("🎓 学习到: 用户避免换乘")
        
        # 规则2: 用户经常选择步行 → prefer_walk: true
        accept_walk_count = stats.get("accept_walk", 0)
        reject_walk_count = stats.get("reject_walk", 0)
        if accept_walk_count >= 3 and accept_walk_count > reject_walk_count * 2:
            if not self.preferences.prefer_walk:
                self.preferences.prefer_walk = True
                logger.info("🎓 学习到: 用户偏好步行")
        
        # 规则3: 用户频繁拒绝拥挤路线 → avoid_crowded: true
        reject_crowded_count = stats.get("reject_crowded", 0)
        if reject_crowded_count >= 3:
            if not self.preferences.avoid_crowded:
                self.preferences.avoid_crowded = True
                logger.info("🎓 学习到: 用户避免拥挤")
    
    def get_preferences(self) -> Dict[str, Any]:
        """获取用户偏好"""
        return self.preferences.to_dict()
    
    def update_preference(self, key: str, value: Any):
        """
        手动更新偏好
        
        Args:
            key: 偏好键
            value: 偏好值
        """
        if hasattr(self.preferences, key):
            setattr(self.preferences, key, value)
            self._save_profile()
            logger.info(f"⚙️ 偏好已更新: {key} = {value}")
        else:
            logger.warning(f"⚠️ 未知的偏好键: {key}")
    
    def reset_preferences(self):
        """重置所有偏好"""
        self.preferences = UserPreferences()
        self.behavior_history = []
        self._save_profile()
        logger.info("🔄 所有偏好已重置")


import time
# 全局用户偏好管理器实例
_global_profile_manager: Optional[UserProfileManager] = None


def get_user_profile_manager() -> UserProfileManager:
    """获取全局用户偏好管理器实例"""
    global _global_profile_manager
    if _global_profile_manager is None:
        _global_profile_manager = UserProfileManager()
    return _global_profile_manager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("👤 用户偏好管理器测试")
    print("=" * 70)
    
    manager = get_user_profile_manager()
    
    # 记录选择
    print("\n1. 记录路线选择...")
    manager.record_route_choice("reject", "bus")
    manager.record_route_choice("reject", "transfer")
    manager.record_route_choice("reject", "transfer")
    
    # 查看偏好
    print("\n2. 当前偏好:")
    prefs = manager.get_preferences()
    for key, value in prefs.items():
        if isinstance(value, bool) and value:
            print(f"   ✅ {key}: {value}")
    
    # 记录步行选择
    print("\n3. 记录步行选择...")
    for i in range(4):
        manager.record_route_choice("accept", "walk")
    
    # 查看更新后的偏好
    print("\n4. 更新后的偏好:")
    prefs = manager.get_preferences()
    for key, value in prefs.items():
        if isinstance(value, bool) and value:
            print(f"   ✅ {key}: {value}")
    
    print("\n" + "=" * 70)

