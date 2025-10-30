"""
医生服务时间检查器
判断医生服务时间，避免用户错过就诊
"""

import logging
import json
import os
from datetime import datetime, time as dt_time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DoctorSchedule:
    """医生排班信息"""
    department: str
    doctor_name: str
    working_hours: List[str]  # ["08:00-12:00", "13:30-17:30"]
    rest_periods: List[str]   # ["12:00-13:30"]
    special_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "department": self.department,
            "doctor_name": self.doctor_name,
            "working_hours": self.working_hours,
            "rest_periods": self.rest_periods,
            "special_notes": self.special_notes
        }


class DoctorScheduleChecker:
    """医生服务时间检查器"""
    
    def __init__(self, storage_file: str = "data/doctor_schedules.json"):
        """初始化医生服务时间检查器"""
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        self.doctor_schedules: Dict[str, Dict[str, DoctorSchedule]] = {}
        
        # 默认医生排班
        self.default_schedules = {
            "牙科": DoctorSchedule(
                department="牙科",
                doctor_name="默认医生",
                working_hours=["08:00-12:00", "13:30-17:30"],
                rest_periods=["12:00-13:30"]
            ),
            "内科": DoctorSchedule(
                department="内科",
                doctor_name="默认医生",
                working_hours=["08:00-12:00", "14:00-18:00"],
                rest_periods=["12:00-14:00"]
            ),
            "外科": DoctorSchedule(
                department="外科",
                doctor_name="默认医生",
                working_hours=["08:30-12:00", "14:00-17:30"],
                rest_periods=["12:00-14:00"]
            )
        }
        
        self._load_data()
        self.logger.info("👨‍⚕️ 医生服务时间检查器初始化完成")
    
    def check_doctor_availability(self,
                                 department: str,
                                 current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        检查医生服务时间
        
        Args:
            department: 科室名称
            current_time: 当前时间
        
        Returns:
            Dict[str, Any]: 医生服务状态
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 获取科室排班信息
        schedule = self._get_department_schedule(department)
        if not schedule:
            return {
                "available": False,
                "reason": "未找到科室排班信息",
                "message": None
            }
        
        current_time_obj = current_time.time()
        
        # 检查是否在服务时间内
        is_working = self._is_working_time(current_time_obj, schedule.working_hours)
        is_rest_time = self._is_rest_time(current_time_obj, schedule.rest_periods)
        
        if is_working and not is_rest_time:
            # 正常服务时间
            return {
                "available": True,
                "is_working": True,
                "is_rest_time": False,
                "message": None,
                "schedule": schedule.to_dict()
            }
        elif is_rest_time:
            # 休息时间
            next_work_time = self._get_next_work_time(current_time_obj, schedule.working_hours)
            message = f"医生正在休息时间，下次服务时间为{next_work_time}。"
            
            return {
                "available": False,
                "is_working": False,
                "is_rest_time": True,
                "message": message,
                "next_work_time": next_work_time,
                "schedule": schedule.to_dict()
            }
        else:
            # 非服务时间
            next_work_time = self._get_next_work_time(current_time_obj, schedule.working_hours)
            message = f"医生服务时间已结束，下次服务时间为{next_work_time}。"
            
            return {
                "available": False,
                "is_working": False,
                "is_rest_time": False,
                "message": message,
                "next_work_time": next_work_time,
                "schedule": schedule.to_dict()
            }
    
    def check_approaching_rest_time(self,
                                   department: str,
                                   current_time: Optional[datetime] = None,
                                   warning_minutes: int = 30) -> Dict[str, Any]:
        """
        检查是否接近休息时间
        
        Args:
            department: 科室名称
            current_time: 当前时间
            warning_minutes: 提前警告时间（分钟）
        
        Returns:
            Dict[str, Any]: 休息时间警告
        """
        if current_time is None:
            current_time = datetime.now()
        
        schedule = self._get_department_schedule(department)
        if not schedule:
            return {
                "approaching_rest": False,
                "message": None
            }
        
        current_time_obj = current_time.time()
        
        # 检查是否接近休息时间
        for rest_period in schedule.rest_periods:
            rest_start = self._parse_time_range(rest_period)[0]
            
            # 计算距离休息时间的时间差
            time_diff = self._time_diff_minutes(current_time_obj, rest_start)
            
            if 0 < time_diff <= warning_minutes:
                message = f"医生可能即将休息（{rest_period}），建议您稍作休息，我会持续监测叫号状态。"
                
                return {
                    "approaching_rest": True,
                    "rest_period": rest_period,
                    "minutes_until_rest": time_diff,
                    "message": message,
                    "schedule": schedule.to_dict()
                }
        
        return {
            "approaching_rest": False,
            "message": None
        }
    
    def update_doctor_schedule(self,
                              department: str,
                              doctor_name: str,
                              working_hours: List[str],
                              rest_periods: List[str],
                              special_notes: str = "") -> bool:
        """
        更新医生排班信息
        
        Args:
            department: 科室名称
            doctor_name: 医生姓名
            working_hours: 工作时间
            rest_periods: 休息时间
            special_notes: 特殊说明
        
        Returns:
            bool: 是否成功更新
        """
        schedule = DoctorSchedule(
            department=department,
            doctor_name=doctor_name,
            working_hours=working_hours,
            rest_periods=rest_periods,
            special_notes=special_notes
        )
        
        if department not in self.doctor_schedules:
            self.doctor_schedules[department] = {}
        
        self.doctor_schedules[department][doctor_name] = schedule
        self._save_data()
        
        self.logger.info(f"👨‍⚕️ 已更新医生排班: {department} - {doctor_name}")
        return True
    
    def _get_department_schedule(self, department: str) -> Optional[DoctorSchedule]:
        """获取科室排班信息"""
        if department in self.doctor_schedules:
            # 返回第一个医生的排班（简化处理）
            schedules = self.doctor_schedules[department]
            if schedules:
                return list(schedules.values())[0]
        
        # 使用默认排班
        if department in self.default_schedules:
            return self.default_schedules[department]
        
        return None
    
    def _is_working_time(self, current_time: dt_time, working_hours: List[str]) -> bool:
        """检查是否在工作时间内"""
        for time_range in working_hours:
            start_time, end_time = self._parse_time_range(time_range)
            if start_time <= current_time <= end_time:
                return True
        return False
    
    def _is_rest_time(self, current_time: dt_time, rest_periods: List[str]) -> bool:
        """检查是否在休息时间内"""
        for rest_period in rest_periods:
            start_time, end_time = self._parse_time_range(rest_period)
            if start_time <= current_time <= end_time:
                return True
        return False
    
    def _parse_time_range(self, time_range: str) -> tuple:
        """解析时间范围"""
        start_str, end_str = time_range.split('-')
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.strptime(end_str, '%H:%M').time()
        return start_time, end_time
    
    def _time_diff_minutes(self, time1: dt_time, time2: dt_time) -> int:
        """计算两个时间的分钟差"""
        dt1 = datetime.combine(datetime.today(), time1)
        dt2 = datetime.combine(datetime.today(), time2)
        
        if dt2 < dt1:
            dt2 = datetime.combine(datetime.today().replace(day=datetime.today().day + 1), time2)
        
        diff = dt2 - dt1
        return int(diff.total_seconds() / 60)
    
    def _get_next_work_time(self, current_time: dt_time, working_hours: List[str]) -> str:
        """获取下次工作时间"""
        for time_range in working_hours:
            start_time, end_time = self._parse_time_range(time_range)
            if current_time < start_time:
                return start_time.strftime('%H:%M')
        
        # 如果今天没有更多工作时间，返回明天第一个工作时间
        if working_hours:
            first_start, _ = self._parse_time_range(working_hours[0])
            return f"明天{first_start.strftime('%H:%M')}"
        
        return "未知"
    
    def _load_data(self):
        """加载数据"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for dept, doctors in data.items():
                        self.doctor_schedules[dept] = {}
                        for doctor_name, schedule_data in doctors.items():
                            schedule = DoctorSchedule(**schedule_data)
                            self.doctor_schedules[dept][doctor_name] = schedule
                self.logger.info("✅ 已加载医生排班数据")
            except Exception as e:
                self.logger.error(f"❌ 加载医生排班数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {}
            for dept, doctors in self.doctor_schedules.items():
                data[dept] = {}
                for doctor_name, schedule in doctors.items():
                    data[dept][doctor_name] = schedule.to_dict()
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug("💾 医生排班数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存医生排班数据失败: {e}")


# 全局医生服务时间检查器实例
_global_doctor_checker: Optional[DoctorScheduleChecker] = None


def get_doctor_schedule_checker() -> DoctorScheduleChecker:
    """获取全局医生服务时间检查器实例"""
    global _global_doctor_checker
    if _global_doctor_checker is None:
        _global_doctor_checker = DoctorScheduleChecker()
    return _global_doctor_checker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("👨‍⚕️ 医生服务时间检查器测试")
    print("=" * 70)
    
    checker = get_doctor_schedule_checker()
    
    # 测试1: 检查医生服务时间
    print("\n1. 检查医生服务时间...")
    result = checker.check_doctor_availability("牙科")
    print(f"   服务状态: {result['available']}")
    if result['message']:
        print(f"   消息: {result['message']}")
    
    # 测试2: 检查接近休息时间
    print("\n2. 检查接近休息时间...")
    rest_result = checker.check_approaching_rest_time("牙科")
    print(f"   接近休息: {rest_result['approaching_rest']}")
    if rest_result['message']:
        print(f"   消息: {rest_result['message']}")
    
    # 测试3: 更新医生排班
    print("\n3. 更新医生排班...")
    success = checker.update_doctor_schedule(
        "牙科", "李医生",
        ["08:30-12:00", "14:00-17:30"],
        ["12:00-14:00"],
        "周二休息"
    )
    print(f"   更新成功: {success}")
    
    print("\n" + "=" * 70)
