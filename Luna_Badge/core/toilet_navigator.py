"""
统一洗手间引导策略调度模块
封装完整的洗手间导航流程：地图POI → 推测设施 → 人工辅助 → 替代方案
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)

# 导入依赖模块
try:
    from .facility_locator import FacilityLocator, get_facility_locator
    from .facility_detector import FacilityDetector
    from .signboard_detector import SignboardDetector
    from .navigation_manager import NavigationManager, get_navigation_manager
    from .memory_store import MemoryStore, global_memory_store
except ImportError:
    from facility_locator import FacilityLocator, get_facility_locator
    from facility_detector import FacilityDetector
    from signboard_detector import SignboardDetector
    from navigation_manager import NavigationManager, get_navigation_manager
    from memory_store import MemoryStore, global_memory_store


class NavigationStrategy(Enum):
    """导航策略"""
    MAP_POI = "map_poi"           # 地图POI直接导航
    INFERRED_FACILITY = "inferred_facility"  # 推测设施导航
    HUMAN_ASSISTANCE = "human_assistance"  # 人工辅助
    ALTERNATIVE = "alternative"   # 替代方案
    UNAVAILABLE = "unavailable"   # 无可用方案


class ToiletNavigator:
    """洗手间导航调度器"""
    
    def __init__(self):
        """初始化洗手间导航器"""
        self.logger = logging.getLogger(__name__)
        self.facility_locator = get_facility_locator()
        self.navigation_manager = get_navigation_manager()
        self.memory_store = global_memory_store
        
        # 保存主导航状态
        self.main_navigation_status = None
        self.main_destination = None
        
        self.logger.info("🚻 洗手间导航器初始化完成")
    
    def navigate_to_toilet(self,
                          current_position: tuple,
                          tts_broadcast: Optional[callable] = None) -> Dict[str, Any]:
        """
        导航到洗手间（统一调度入口）
        
        Args:
            current_position: 当前位置 (lat, lng)
            tts_broadcast: TTS播报函数
        
        Returns:
            Dict[str, Any]: 导航结果
        """
        self.logger.info("🚻 开始洗手间导航流程...")
        
        # 保存当前主导航状态
        self._save_main_navigation_state()
        
        # 策略1: 直接查询地图POI
        strategy, result = self._try_map_poi_strategy(current_position, tts_broadcast)
        if strategy == NavigationStrategy.MAP_POI:
            return result
        
        # 策略2: 推测性设施匹配
        if strategy == NavigationStrategy.UNAVAILABLE:
            strategy, result = self._try_inferred_facility_strategy(current_position, tts_broadcast)
            if strategy == NavigationStrategy.INFERRED_FACILITY:
                return result
        
        # 策略3: 人工辅助策略
        if strategy == NavigationStrategy.UNAVAILABLE:
            strategy, result = self._try_human_assistance_strategy(tts_broadcast)
            if strategy == NavigationStrategy.HUMAN_ASSISTANCE:
                return result
        
        # 策略4: 替代方案
        if strategy == NavigationStrategy.UNAVAILABLE:
            strategy, result = self._try_alternative_strategy(current_position, tts_broadcast)
        
        return {
            "strategy": strategy.value,
            "success": strategy != NavigationStrategy.UNAVAILABLE,
            "message": result.get("message") if result else "未找到可用的洗手间导航方案",
            "facility": result.get("facility") if result else None
        }
    
    def _try_map_poi_strategy(self,
                              current_position: tuple,
                              tts_broadcast: Optional[callable]) -> tuple:
        """尝试地图POI策略"""
        toilets = self.facility_locator.find_toilets(current_position)
        
        # 筛选直接标注的洗手间
        direct_toilets = [t for t in toilets if t.has_toilet and t.source == "map"]
        
        if direct_toilets:
            best = direct_toilets[0]
            
            # 播报隐私保护提醒
            if tts_broadcast:
                tts_broadcast(f"已找到附近洗手间，距离{best.distance_meters:.0f}米。隐私保护功能已开启，开始导航。")
            
            # 启动导航
            self._start_toilet_navigation(best)
            
            return NavigationStrategy.MAP_POI, {
                "facility": best.to_dict(),
                "message": f"正在导航至{best.name}"
            }
        
        return NavigationStrategy.UNAVAILABLE, None
    
    def _try_inferred_facility_strategy(self,
                                       current_position: tuple,
                                       tts_broadcast: Optional[callable]) -> tuple:
        """尝试推测性设施策略"""
        inferred = self.facility_locator._infer_toilet_facilities(current_position, 500)
        
        if inferred:
            best = inferred[0]
            
            facility_type_names = {
                "mall": "商场",
                "metro_station": "地铁站",
                "service_center": "服务中心",
                "park": "公园"
            }
            type_name = facility_type_names.get(best.type.value, best.type.value)
            
            if tts_broadcast:
                tts_broadcast(f"前方有一处{type_name}，通常配有洗手间，我将引导您前往。")
            
            self._start_toilet_navigation(best)
            
            return NavigationStrategy.INFERRED_FACILITY, {
                "facility": best.to_dict(),
                "message": f"正在导航至{type_name}"
            }
        
        return NavigationStrategy.UNAVAILABLE, None
    
    def _try_human_assistance_strategy(self,
                                      tts_broadcast: Optional[callable]) -> tuple:
        """尝试人工辅助策略"""
        # TODO: 实际应查询咨询台位置和检测工作人员
        
        if tts_broadcast:
            tts_broadcast("未找到明确的洗手间标识，建议您：1.寻找附近的工作人员询问 2.前往服务台或咨询处")
        
        return NavigationStrategy.HUMAN_ASSISTANCE, {
            "message": "建议人工询问",
            "suggestions": ["寻找工作人员", "前往服务台"]
        }
    
    def _try_alternative_strategy(self,
                                 current_position: tuple,
                                 tts_broadcast: Optional[callable]) -> tuple:
        """尝试替代方案"""
        # 查询便利店等替代场所
        alternatives = [f for f in self.facility_locator.find_toilets(current_position)
                       if f.type.value == "convenience_store"]
        
        if alternatives:
            best = alternatives[0]
            
            if tts_broadcast:
                tts_broadcast(f"附近有{best.name}，但可能无洗手间保障。是否前往？")
            
            return NavigationStrategy.ALTERNATIVE, {
                "facility": best.to_dict(),
                "message": "替代方案：便利店",
                "requires_confirmation": True
            }
        
        return NavigationStrategy.UNAVAILABLE, None
    
    def _save_main_navigation_state(self):
        """保存主导航状态"""
        nav_status = self.navigation_manager.get_status()
        if nav_status:
            self.main_navigation_status = nav_status.get("status")
            self.main_destination = nav_status.get("destination")
            self.logger.debug(f"💾 已保存主导航状态: {self.main_navigation_status}")
    
    def _start_toilet_navigation(self, facility):
        """启动洗手间导航"""
        # 暂停主导航
        if self.main_navigation_status == "active":
            self.navigation_manager.pause_navigation("临时前往洗手间")
        
        # 标记导航状态
        self.memory_store.set_navigation_status("toilet_navigation")
        
        # 启动临时导航（TODO: 实际应调用路径规划）
        self.logger.info(f"🧭 开始导航至洗手间: {facility.name}")
    
    def restore_main_navigation(self):
        """恢复主导航"""
        if self.main_navigation_status == "paused":
            self.navigation_manager.resume_navigation()
            self.memory_store.set_navigation_status("active")
            self.logger.info("🧭 已恢复主导航")


# 全局洗手间导航器实例
_global_toilet_navigator: Optional[ToiletNavigator] = None


def get_toilet_navigator() -> ToiletNavigator:
    """获取全局洗手间导航器实例"""
    global _global_toilet_navigator
    if _global_toilet_navigator is None:
        _global_toilet_navigator = ToiletNavigator()
    return _global_toilet_navigator


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🚻 洗手间导航器测试")
    print("=" * 70)
    
    navigator = get_toilet_navigator()
    
    # 模拟TTS播报
    def mock_tts(text):
        print(f"📢 TTS: {text}")
    
    # 测试导航流程
    print("\n1. 测试洗手间导航流程...")
    current_pos = (31.2304, 121.4737)
    result = navigator.navigate_to_toilet(current_pos, mock_tts)
    
    print(f"\n导航结果:")
    print(f"  策略: {result['strategy']}")
    print(f"  成功: {result['success']}")
    print(f"  消息: {result['message']}")
    
    print("\n" + "=" * 70)
