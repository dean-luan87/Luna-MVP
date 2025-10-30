"""
公共设施定位模块
查找洗手间等公共设施的位置
"""

import logging
import os
import json
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FacilityType(Enum):
    """设施类型"""
    TOILET = "toilet"           # 洗手间
    MALL = "mall"               # 商场
    CONVENIENCE_STORE = "convenience_store"  # 便利店
    METRO_STATION = "metro_station"  # 地铁站
    SERVICE_CENTER = "service_center"  # 服务中心
    PARK = "park"               # 公园
    HOSPITAL = "hospital"       # 医院


@dataclass
class FacilityPOI:
    """设施POI信息"""
    type: FacilityType
    name: str
    position: Tuple[float, float]  # (lat, lng)
    distance_meters: float
    has_toilet: bool = False  # 是否确认有洗手间
    toilet_probability: float = 0.0  # 有洗手间的概率（0-1）
    source: str = "map"  # 数据来源：map/inference/detection
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "name": self.name,
            "position": self.position,
            "distance_meters": self.distance_meters,
            "has_toilet": self.has_toilet,
            "toilet_probability": self.toilet_probability,
            "source": self.source
        }


class FacilityLocator:
    """设施定位器"""
    
    def __init__(self):
        """初始化设施定位器"""
        self.logger = logging.getLogger(__name__)
        
        # 洗手间概率配置（不同类型设施的洗手间可能性）
        self.toilet_probability_map = {
            FacilityType.MALL: 0.95,
            FacilityType.HOSPITAL: 0.99,
            FacilityType.METRO_STATION: 0.90,
            FacilityType.SERVICE_CENTER: 0.85,
            FacilityType.PARK: 0.70,
            FacilityType.CONVENIENCE_STORE: 0.30,
            FacilityType.TOILET: 1.0
        }
        
        # 搜索范围（米）
        self.search_radius = 500
        
        # POI数据存储（实际应从地图API获取）
        self.poi_data: List[Dict[str, Any]] = []
        
        self.logger.info("📍 设施定位器初始化完成")
    
    def find_toilets(self,
                    current_position: Tuple[float, float],
                    radius: Optional[float] = None) -> List[FacilityPOI]:
        """
        查找附近的洗手间
        
        Args:
            current_position: 当前位置 (lat, lng)
            radius: 搜索半径（米），默认500米
        
        Returns:
            List[FacilityPOI]: 找到的设施列表
        """
        if radius is None:
            radius = self.search_radius
        
        results = []
        
        # 方法1: 直接查询地图中的洗手间POI
        direct_toilets = self._query_map_toilets(current_position, radius)
        results.extend(direct_toilets)
        
        # 方法2: 推测性查询（如果直接查询结果不足）
        if len(direct_toilets) == 0:
            inferred_facilities = self._infer_toilet_facilities(current_position, radius)
            results.extend(inferred_facilities)
        
        # 按距离排序
        results.sort(key=lambda x: x.distance_meters)
        
        self.logger.info(f"📍 找到 {len(results)} 个可能的洗手间位置")
        
        return results
    
    def _query_map_toilets(self,
                          position: Tuple[float, float],
                          radius: float) -> List[FacilityPOI]:
        """
        直接查询地图中的洗手间POI
        
        Args:
            position: 当前位置
            radius: 搜索半径
        
        Returns:
            List[FacilityPOI]: 洗手间POI列表
        """
        toilets = []
        
        # TODO: 实际应调用地图API（如高德、百度、OpenStreetMap）
        # 这里使用模拟数据
        
        # 模拟数据示例
        mock_toilets = [
            {
                "name": "商场洗手间",
                "position": (31.2310, 121.4740),
                "type": FacilityType.TOILET
            },
            {
                "name": "地铁站洗手间",
                "position": (31.2320, 121.4750),
                "type": FacilityType.TOILET
            }
        ]
        
        for toilet_data in mock_toilets:
            distance = self._calculate_distance(position, toilet_data["position"])
            if distance <= radius:
                toilets.append(FacilityPOI(
                    type=FacilityType.TOILET,
                    name=toilet_data["name"],
                    position=toilet_data["position"],
                    distance_meters=distance,
                    has_toilet=True,
                    toilet_probability=1.0,
                    source="map"
                ))
        
        return toilets
    
    def _infer_toilet_facilities(self,
                                position: Tuple[float, float],
                                radius: float) -> List[FacilityPOI]:
        """
        推测可能包含洗手间的设施
        
        Args:
            position: 当前位置
            radius: 搜索半径
        
        Returns:
            List[FacilityPOI]: 推测的设施列表
        """
        inferred = []
        
        # 查询周边设施
        nearby_facilities = self._query_nearby_facilities(position, radius)
        
        for facility_data in nearby_facilities:
            facility_type = facility_data["type"]
            probability = self.toilet_probability_map.get(facility_type, 0.5)
            
            # 只返回概率较高的设施
            if probability >= 0.7:
                inferred.append(FacilityPOI(
                    type=facility_type,
                    name=facility_data["name"],
                    position=facility_data["position"],
                    distance_meters=facility_data["distance"],
                    has_toilet=False,
                    toilet_probability=probability,
                    source="inference"
                ))
        
        return inferred
    
    def _query_nearby_facilities(self,
                                position: Tuple[float, float],
                                radius: float) -> List[Dict[str, Any]]:
        """
        查询周边设施（简化实现）
        
        Args:
            position: 当前位置
            radius: 搜索半径
        
        Returns:
            List[Dict[str, Any]]: 设施列表
        """
        # TODO: 实际应调用地图API
        
        # 模拟数据
        mock_facilities = [
            {
                "type": FacilityType.MALL,
                "name": "附近商场",
                "position": (31.2315, 121.4745),
                "distance": 300
            },
            {
                "type": FacilityType.CONVENIENCE_STORE,
                "name": "7-11便利店",
                "position": (31.2308, 121.4735),
                "distance": 150
            },
            {
                "type": FacilityType.METRO_STATION,
                "name": "地铁站",
                "position": (31.2325, 121.4755),
                "distance": 400
            }
        ]
        
        return mock_facilities
    
    def _calculate_distance(self,
                           pos1: Tuple[float, float],
                           pos2: Tuple[float, float]) -> float:
        """计算两点间距离（米）- Haversine公式"""
        from math import radians, cos, sin, asin, sqrt
        
        R = 6371000
        lat1, lng1 = pos1
        lat2, lng2 = pos2
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lng = radians(lng2 - lng1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        return R * c
    
    def get_best_toilet_route(self,
                             current_position: Tuple[float, float]) -> Optional[FacilityPOI]:
        """
        获取最佳洗手间路径
        
        Args:
            current_position: 当前位置
        
        Returns:
            Optional[FacilityPOI]: 最佳洗手间选项
        """
        facilities = self.find_toilets(current_position)
        
        if not facilities:
            return None
        
        # 优先选择确认有洗手间的，其次选择概率高的，最后选择距离近的
        best = max(facilities, key=lambda x: (
            x.has_toilet,
            x.toilet_probability,
            -x.distance_meters
        ))
        
        return best


# 全局设施定位器实例
_global_facility_locator: Optional[FacilityLocator] = None


def get_facility_locator() -> FacilityLocator:
    """获取全局设施定位器实例"""
    global _global_facility_locator
    if _global_facility_locator is None:
        _global_facility_locator = FacilityLocator()
    return _global_facility_locator


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📍 设施定位器测试")
    print("=" * 70)
    
    locator = get_facility_locator()
    
    # 测试查找洗手间
    print("\n1. 查找附近洗手间...")
    current_pos = (31.2304, 121.4737)
    toilets = locator.find_toilets(current_pos)
    
    for i, toilet in enumerate(toilets[:3], 1):
        print(f"\n选项 {i}:")
        print(f"  名称: {toilet.name}")
        print(f"  类型: {toilet.type.value}")
        print(f"  距离: {toilet.distance_meters:.0f}米")
        print(f"  概率: {toilet.toilet_probability:.0%}")
        print(f"  来源: {toilet.source}")
    
    # 测试最佳路径
    print("\n2. 获取最佳洗手间路径...")
    best = locator.get_best_toilet_route(current_pos)
    if best:
        print(f"   推荐: {best.name} ({best.distance_meters:.0f}米)")
    
    print("\n" + "=" * 70)
