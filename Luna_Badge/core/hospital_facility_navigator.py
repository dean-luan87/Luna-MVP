"""
医院功能区导航器
支持用户语音指令导航至医院内功能区
"""

import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FacilityType(Enum):
    """功能区类型"""
    BLOOD_DRAWING = "抽血室"
    REPORT_PRINTING = "报告打印"
    PHARMACY = "药房"
    RESTROOM = "洗手间"
    CAFETERIA = "茶水间"
    REGISTRATION = "挂号处"
    PAYMENT = "缴费处"
    EMERGENCY = "急诊科"
    UNKNOWN = "未知"


@dataclass
class FacilityInfo:
    """功能区信息"""
    name: str
    facility_type: FacilityType
    floor: int
    area: str
    description: str
    coordinates: Optional[Tuple[float, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "facility_type": self.facility_type.value,
            "floor": self.floor,
            "area": self.area,
            "description": self.description,
            "coordinates": self.coordinates
        }


class HospitalFacilityNavigator:
    """医院功能区导航器"""
    
    def __init__(self):
        """初始化医院功能区导航器"""
        self.logger = logging.getLogger(__name__)
        
        # 功能区关键词映射
        self.facility_keywords = {
            FacilityType.BLOOD_DRAWING: ["抽血", "验血", "采血", "血检"],
            FacilityType.REPORT_PRINTING: ["报告", "取报告", "打印报告", "化验单"],
            FacilityType.PHARMACY: ["药房", "取药", "拿药", "药品"],
            FacilityType.RESTROOM: ["洗手间", "厕所", "卫生间", "WC"],
            FacilityType.CAFETERIA: ["茶水间", "休息区", "饮水", "咖啡"],
            FacilityType.REGISTRATION: ["挂号", "挂号处", "注册"],
            FacilityType.PAYMENT: ["缴费", "收费", "结算", "付款"],
            FacilityType.EMERGENCY: ["急诊", "急救", "急诊科"]
        }
        
        # 默认功能区信息
        self.default_facilities = {
            FacilityType.BLOOD_DRAWING: FacilityInfo(
                name="抽血室",
                facility_type=FacilityType.BLOOD_DRAWING,
                floor=2,
                area="检验科",
                description="血液检验采样区域"
            ),
            FacilityType.REPORT_PRINTING: FacilityInfo(
                name="报告打印处",
                facility_type=FacilityType.REPORT_PRINTING,
                floor=1,
                area="大厅",
                description="化验报告自助打印区域"
            ),
            FacilityType.PHARMACY: FacilityInfo(
                name="药房",
                facility_type=FacilityType.PHARMACY,
                floor=1,
                area="门诊大厅",
                description="药品领取区域"
            ),
            FacilityType.RESTROOM: FacilityInfo(
                name="洗手间",
                facility_type=FacilityType.RESTROOM,
                floor=0,
                area="各楼层",
                description="公共洗手间"
            ),
            FacilityType.CAFETERIA: FacilityInfo(
                name="茶水间",
                facility_type=FacilityType.CAFETERIA,
                floor=0,
                area="休息区",
                description="饮水休息区域"
            )
        }
        
        self.logger.info("🏥 医院功能区导航器初始化完成")
    
    def parse_voice_command(self, voice_text: str) -> Dict[str, Any]:
        """
        解析语音指令
        
        Args:
            voice_text: 语音识别文本
        
        Returns:
            Dict[str, Any]: 解析结果
        """
        # 提取功能区类型
        facility_type = self._extract_facility_type(voice_text)
        
        if facility_type == FacilityType.UNKNOWN:
            return {
                "success": False,
                "facility_type": None,
                "message": "未识别到有效的功能区指令",
                "suggestions": self._get_suggestions()
            }
        
        # 获取功能区信息
        facility_info = self._get_facility_info(facility_type)
        
        return {
            "success": True,
            "facility_type": facility_type.value,
            "facility_info": facility_info.to_dict(),
            "message": f"正在为您导航到{facility_info.name}",
            "navigation_needed": True
        }
    
    def navigate_to_facility(self,
                           facility_type: FacilityType,
                           current_position: Optional[Tuple[float, float]] = None) -> Dict[str, Any]:
        """
        导航到功能区
        
        Args:
            facility_type: 功能区类型
            current_position: 当前位置坐标
        
        Returns:
            Dict[str, Any]: 导航结果
        """
        facility_info = self._get_facility_info(facility_type)
        
        # 检查是否有场内地图
        has_map = self._check_internal_map()
        
        if has_map:
            # 使用现有地图进行路径规划
            route = self._plan_route_with_map(facility_info, current_position)
            navigation_method = "map_based"
        else:
            # 启动视觉构建地图
            route = self._plan_route_with_vision(facility_info)
            navigation_method = "vision_based"
        
        return {
            "success": True,
            "facility_info": facility_info.to_dict(),
            "route": route,
            "navigation_method": navigation_method,
            "message": f"正在导航到{facility_info.name}，位于{facility_info.floor}楼{facility_info.area}",
            "estimated_time": self._estimate_navigation_time(route)
        }
    
    def detect_facility_signs(self, detected_signs: List[str]) -> List[FacilityInfo]:
        """
        检测功能区标识
        
        Args:
            detected_signs: 检测到的标识文字
        
        Returns:
            List[FacilityInfo]: 检测到的功能区信息
        """
        detected_facilities = []
        
        for sign in detected_signs:
            for facility_type, keywords in self.facility_keywords.items():
                if any(keyword in sign for keyword in keywords):
                    facility_info = self._get_facility_info(facility_type)
                    detected_facilities.append(facility_info)
                    break
        
        return detected_facilities
    
    def _extract_facility_type(self, voice_text: str) -> FacilityType:
        """从语音文本中提取功能区类型"""
        voice_lower = voice_text.lower()
        
        for facility_type, keywords in self.facility_keywords.items():
            if any(keyword in voice_lower for keyword in keywords):
                return facility_type
        
        return FacilityType.UNKNOWN
    
    def _get_facility_info(self, facility_type: FacilityType) -> FacilityInfo:
        """获取功能区信息"""
        if facility_type in self.default_facilities:
            return self.default_facilities[facility_type]
        
        # 返回默认信息
        return FacilityInfo(
            name=facility_type.value,
            facility_type=facility_type,
            floor=0,
            area="未知区域",
            description="功能区信息待确认"
        )
    
    def _check_internal_map(self) -> bool:
        """检查是否有场内地图"""
        # 简化实现：实际应检查地图数据
        return False
    
    def _plan_route_with_map(self,
                           facility_info: FacilityInfo,
                           current_position: Optional[Tuple[float, float]]) -> List[str]:
        """使用地图规划路径"""
        # 简化实现：返回基本路径
        return [
            "从当前位置出发",
            f"前往{facility_info.floor}楼",
            f"到达{facility_info.area}",
            f"找到{facility_info.name}"
        ]
    
    def _plan_route_with_vision(self, facility_info: FacilityInfo) -> List[str]:
        """使用视觉构建路径"""
        return [
            "启动视觉导航",
            "识别导向标识",
            f"寻找{facility_info.name}指示牌",
            f"跟随标识前往{facility_info.floor}楼",
            f"到达{facility_info.name}"
        ]
    
    def _estimate_navigation_time(self, route: List[str]) -> int:
        """估算导航时间（分钟）"""
        # 简化估算：每步1-2分钟
        return len(route) * 1.5
    
    def _get_suggestions(self) -> List[str]:
        """获取建议的功能区"""
        return [
            "抽血室",
            "报告打印处",
            "药房",
            "洗手间",
            "茶水间"
        ]


# 全局医院功能区导航器实例
_global_facility_navigator: Optional[HospitalFacilityNavigator] = None


def get_facility_navigator() -> HospitalFacilityNavigator:
    """获取全局医院功能区导航器实例"""
    global _global_facility_navigator
    if _global_facility_navigator is None:
        _global_facility_navigator = HospitalFacilityNavigator()
    return _global_facility_navigator


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏥 医院功能区导航器测试")
    print("=" * 70)
    
    navigator = get_facility_navigator()
    
    # 测试1: 解析语音指令
    print("\n1. 解析语音指令...")
    result = navigator.parse_voice_command("Luna，我要去抽血室")
    print(f"   解析成功: {result['success']}")
    if result['success']:
        print(f"   功能区: {result['facility_type']}")
        print(f"   消息: {result['message']}")
    
    # 测试2: 导航到功能区
    print("\n2. 导航到功能区...")
    nav_result = navigator.navigate_to_facility(FacilityType.BLOOD_DRAWING)
    print(f"   导航成功: {nav_result['success']}")
    print(f"   导航方法: {nav_result['navigation_method']}")
    print(f"   预估时间: {nav_result['estimated_time']}分钟")
    
    # 测试3: 检测功能区标识
    print("\n3. 检测功能区标识...")
    facilities = navigator.detect_facility_signs(["抽血室", "报告打印", "药房"])
    print(f"   检测到功能区: {len(facilities)}个")
    for facility in facilities:
        print(f"   - {facility.name} ({facility.floor}楼)")
    
    print("\n" + "=" * 70)
