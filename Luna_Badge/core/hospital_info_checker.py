"""
医院服务状态查询模块
查询医院服务开放状态和就诊流程
"""

import logging
from datetime import datetime, time as dt_time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# 导入设施营业时间检查器（复用逻辑）
try:
    from .facility_schedule_checker import get_schedule_checker
except ImportError:
    from facility_schedule_checker import get_schedule_checker


class ServiceStatus(Enum):
    """服务状态"""
    OPEN = "open"               # 正常开放
    CLOSED = "closed"           # 关闭
    LUNCH_BREAK = "lunch_break" # 午休
    AFTER_HOURS = "after_hours" # 非服务时间
    EMERGENCY_ONLY = "emergency_only"  # 仅急诊


class HospitalInfoChecker:
    """医院信息检查器"""
    
    def __init__(self):
        """初始化医院信息检查器"""
        self.logger = logging.getLogger(__name__)
        self.schedule_checker = get_schedule_checker()
        
        # 医院特殊时间（扩展默认配置）
        self.hospital_schedules = {
            "outpatient": {
                "morning": (dt_time(8, 0), dt_time(12, 0)),
                "afternoon": (dt_time(14, 0), dt_time(17, 30)),
                "lunch_break": (dt_time(12, 0), dt_time(14, 0))
            },
            "registration": {
                "morning": (dt_time(7, 30), dt_time(11, 30)),
                "afternoon": (dt_time(13, 30), dt_time(17, 0))
            },
            "emergency": {
                "24h": True  # 24小时开放
            }
        }
        
        self.logger.info("🏥 医院信息检查器初始化完成")
    
    def check_departure_materials(self, destination: str) -> Dict[str, Any]:
        """
        检查出发前所需材料
        
        Args:
            destination: 目的地（如"虹口医院"）
        
        Returns:
            Dict[str, Any]: 材料提醒信息
        """
        # 检查是否为医院
        hospital_keywords = ["医院", "门诊", "急诊", "医疗中心", "卫生院"]
        is_hospital = any(keyword in destination for keyword in hospital_keywords)
        
        if not is_hospital:
            return {
                "is_hospital": False,
                "message": None,
                "materials": None
            }
        
        # 获取医院材料清单
        try:
            from .hospital_knowledge_manager import get_hospital_knowledge_manager
            knowledge_manager = get_hospital_knowledge_manager()
            materials = knowledge_manager.get_required_materials(destination)
        except ImportError:
            # 如果无法导入，使用默认材料
            materials = {
                "required": ["医保卡", "病历本"],
                "optional": ["身份证", "现金", "银行卡"],
                "notes": "部分医院已无需身份证"
            }
        
        # 生成提醒消息
        required_items = materials.get("required", [])
        optional_items = materials.get("optional", [])
        notes = materials.get("notes", "")
        
        message_parts = []
        if required_items:
            message_parts.append(f"请携带{', '.join(required_items)}")
        if optional_items:
            message_parts.append(f"建议携带{', '.join(optional_items)}")
        if notes:
            message_parts.append(notes)
        
        message = "。".join(message_parts) + "。"
        
        return {
            "is_hospital": True,
            "message": message,
            "materials": materials
        }

    def check_hospital_service_status(self,
                                     service_type: str = "outpatient",
                                     current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        检查医院服务状态
        
        Args:
            service_type: 服务类型（outpatient/registration/emergency）
            current_time: 当前时间（如果为None则使用系统时间）
        
        Returns:
            Dict[str, Any]: 服务状态信息
        """
        if current_time is None:
            current_time = datetime.now()
        
        current_time_obj = current_time.time()
        
        # 急诊服务（24小时开放）
        if service_type == "emergency":
            return {
                "status": ServiceStatus.OPEN.value,
                "is_open": True,
                "message": None,
                "service_type": service_type
            }
        
        # 门诊服务
        if service_type == "outpatient":
            schedule = self.hospital_schedules["outpatient"]
            
            # 检查是否在服务时间内
            is_morning = schedule["morning"][0] <= current_time_obj <= schedule["morning"][1]
            is_afternoon = schedule["afternoon"][0] <= current_time_obj <= schedule["afternoon"][1]
            is_lunch = schedule["lunch_break"][0] <= current_time_obj < schedule["lunch_break"][1]
            
            if is_morning or is_afternoon:
                status = ServiceStatus.OPEN.value
                message = None
            elif is_lunch:
                status = ServiceStatus.LUNCH_BREAK.value
                message = self._format_service_message(current_time, service_type, "lunch_break")
            else:
                status = ServiceStatus.AFTER_HOURS.value
                message = self._format_service_message(current_time, service_type, "after_hours")
            
            return {
                "status": status,
                "is_open": is_morning or is_afternoon,
                "message": message,
                "service_type": service_type
            }
        
        # 挂号服务
        if service_type == "registration":
            schedule = self.hospital_schedules["registration"]
            
            is_open = (schedule["morning"][0] <= current_time_obj <= schedule["morning"][1]) or \
                     (schedule["afternoon"][0] <= current_time_obj <= schedule["afternoon"][1])
            
            if not is_open:
                message = self._format_service_message(current_time, service_type, "closed")
                return {
                    "status": ServiceStatus.CLOSED.value,
                    "is_open": False,
                    "message": message,
                    "service_type": service_type
                }
            
            return {
                "status": ServiceStatus.OPEN.value,
                "is_open": True,
                "message": None,
                "service_type": service_type
            }
        
        return {
            "status": ServiceStatus.UNKNOWN.value,
            "is_open": False,
            "message": "未知服务类型",
            "service_type": service_type
        }
    
    def _format_service_message(self,
                               current_time: datetime,
                               service_type: str,
                               reason: str) -> str:
        """格式化服务状态消息"""
        time_str = self._format_time(current_time)
        
        if reason == "lunch_break":
            return f"当前时间为{time_str}，门诊挂号可能已暂停，您可以前往急诊大厅继续看诊。"
        elif reason == "after_hours":
            return f"当前时间为{time_str}，门诊服务时间已结束，您可以前往急诊大厅继续看诊。"
        elif reason == "closed":
            return f"当前时间为{time_str}，挂号服务已暂停，请前往急诊大厅或咨询台。"
        
        return None
    
    def _format_time(self, dt: datetime) -> str:
        """格式化时间为中文"""
        hour = dt.hour
        minute = dt.minute
        
        if hour < 6:
            period = "凌晨"
        elif hour < 12:
            period = "上午"
        elif hour < 14:
            period = "中午"
        elif hour < 18:
            period = "下午"
        else:
            period = "晚上"
        
        display_hour = hour if hour <= 12 else hour - 12
        if minute == 0:
            return f"{period}{display_hour}点"
        else:
            return f"{period}{display_hour}点{minute}分"


# 全局医院信息检查器实例
_global_hospital_checker: Optional[HospitalInfoChecker] = None


def get_hospital_info_checker() -> HospitalInfoChecker:
    """获取全局医院信息检查器实例"""
    global _global_hospital_checker
    if _global_hospital_checker is None:
        _global_hospital_checker = HospitalInfoChecker()
    return _global_hospital_checker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏥 医院信息检查器测试")
    print("=" * 70)
    
    checker = get_hospital_info_checker()
    
    # 测试1: 正常服务时间
    print("\n1. 测试正常服务时间（上午10点）...")
    test_time1 = datetime.now().replace(hour=10, minute=0)
    result1 = checker.check_hospital_service_status("outpatient", test_time1)
    print(f"   状态: {result1['status']}")
    if result1['message']:
        print(f"   消息: {result1['message']}")
    
    # 测试2: 午休时间
    print("\n2. 测试午休时间（下午1点）...")
    test_time2 = datetime.now().replace(hour=13, minute=0)
    result2 = checker.check_hospital_service_status("outpatient", test_time2)
    print(f"   状态: {result2['status']}")
    if result2['message']:
        print(f"   消息: {result2['message']}")
    
    # 测试3: 挂号服务
    print("\n3. 测试挂号服务状态...")
    result3 = checker.check_hospital_service_status("registration")
    print(f"   状态: {result3['status']}")
    if result3['message']:
        print(f"   消息: {result3['message']}")
    
    print("\n" + "=" * 70)
