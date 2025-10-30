"""
公共设施营业时间判断模块
判断医院、政务大厅等设施的营业状态
"""

import logging
import os
import yaml
from datetime import datetime, time as dt_time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SchedulePeriod:
    """营业时段"""
    start: str  # "08:00"
    end: str    # "12:00"
    
    def contains(self, check_time: dt_time) -> bool:
        """检查时间是否在时段内"""
        start_parts = self.start.split(':')
        end_parts = self.end.split(':')
        start_time = dt_time(int(start_parts[0]), int(start_parts[1]))
        end_time = dt_time(int(end_parts[0]), int(end_parts[1]))
        
        return start_time <= check_time <= end_time
    
    def get_next_open_time(self, check_time: dt_time) -> Optional[str]:
        """获取下次开放时间"""
        start_parts = self.start.split(':')
        start_time = dt_time(int(start_parts[0]), int(start_parts[1]))
        
        if check_time < start_time:
            return self.start
        
        return None


@dataclass
class FacilitySchedule:
    """设施营业时间表"""
    facility_type: str
    periods: List[SchedulePeriod]
    lunch_break: Optional[SchedulePeriod] = None
    
    def is_open_now(self, check_time: Optional[dt_time] = None) -> bool:
        """检查当前是否营业"""
        if check_time is None:
            check_time = datetime.now().time()
        
        for period in self.periods:
            if period.contains(check_time):
                # 检查是否在午休时间
                if self.lunch_break and self.lunch_break.contains(check_time):
                    return False
                return True
        
        return False
    
    def get_next_open_time(self, check_time: Optional[dt_time] = None) -> Optional[str]:
        """获取下次开放时间"""
        if check_time is None:
            check_time = datetime.now().time()
        
        # 如果当前在营业中，返回None
        if self.is_open_now(check_time):
            return None
        
        # 查找下一个营业时段
        for period in self.periods:
            next_time = period.get_next_open_time(check_time)
            if next_time:
                return next_time
        
        # 如果今天没有，返回明天的第一个时段
        if self.periods:
            return self.periods[0].start
        
        return None


class FacilityScheduleChecker:
    """公共设施营业时间检查器"""
    
    def __init__(self, config_file: str = "config/facility_schedule.yaml"):
        """
        初始化设施营业时间检查器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.schedules: Dict[str, FacilitySchedule] = {}
        
        # 默认营业时间（如果配置文件不存在）
        self.default_schedules = {
            "hospital": FacilitySchedule(
                facility_type="hospital",
                periods=[
                    SchedulePeriod("08:00", "12:00"),
                    SchedulePeriod("14:00", "17:30")
                ],
                lunch_break=SchedulePeriod("12:00", "14:00")
            ),
            "government_office": FacilitySchedule(
                facility_type="government_office",
                periods=[
                    SchedulePeriod("09:00", "12:00"),
                    SchedulePeriod("13:30", "17:00")
                ],
                lunch_break=SchedulePeriod("12:00", "13:30")
            ),
            "bank": FacilitySchedule(
                facility_type="bank",
                periods=[
                    SchedulePeriod("09:00", "12:00"),
                    SchedulePeriod("14:00", "17:00")
                ],
                lunch_break=SchedulePeriod("12:00", "14:00")
            )
        }
        
        self._load_schedules()
        logger.info("🏢 公共设施营业时间检查器初始化完成")
    
    def _load_schedules(self):
        """加载营业时间配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    for facility_type, schedule_data in config.items():
                        periods = [
                            SchedulePeriod(p['start'], p['end'])
                            for p in schedule_data.get('periods', [])
                        ]
                        lunch = None
                        if 'lunch_break' in schedule_data:
                            lb_data = schedule_data['lunch_break']
                            lunch = SchedulePeriod(lb_data['start'], lb_data['end'])
                        self.schedules[facility_type] = FacilitySchedule(
                            facility_type=facility_type,
                            periods=periods,
                            lunch_break=lunch
                        )
                logger.info(f"✅ 已加载设施营业时间配置: {len(self.schedules)}个")
            except Exception as e:
                logger.error(f"❌ 加载配置失败: {e}，使用默认配置")
                self.schedules = self.default_schedules.copy()
        else:
            logger.info("⚠️ 配置文件不存在，使用默认配置")
            self.schedules = self.default_schedules.copy()
    
    def check_facility_status(self, 
                             facility_type: str,
                             current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        检查设施营业状态
        
        Args:
            facility_type: 设施类型（hospital/government_office/bank等）
            current_time: 当前时间（如果为None则使用系统时间）
        
        Returns:
            Dict[str, Any]: 营业状态信息
        """
        if current_time is None:
            current_time = datetime.now()
        
        schedule = self.schedules.get(facility_type)
        if not schedule:
            logger.warning(f"⚠️ 未知的设施类型: {facility_type}")
            return {
                "is_open": False,
                "facility_type": facility_type,
                "message": None,
                "next_open_time": None
            }
        
        check_time = current_time.time()
        is_open = schedule.is_open_now(check_time)
        next_open_time = schedule.get_next_open_time(check_time)
        
        # 构建提示消息
        message = None
        if not is_open:
            current_time_str = self._format_time(current_time)
            if next_open_time:
                message = f"当前时间为{current_time_str}，该{facility_type}将于{next_open_time}开始营业，请确认是否仍前往。"
            else:
                message = f"当前时间为{current_time_str}，该{facility_type}目前不在营业时间，请确认是否仍前往。"
        
        return {
            "is_open": is_open,
            "facility_type": facility_type,
            "message": message,
            "next_open_time": next_open_time,
            "current_time": current_time_str if not is_open else None
        }
    
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


# 全局设施时间检查器实例
_global_schedule_checker: Optional[FacilityScheduleChecker] = None


def get_schedule_checker() -> FacilityScheduleChecker:
    """获取全局设施时间检查器实例"""
    global _global_schedule_checker
    if _global_schedule_checker is None:
        _global_schedule_checker = FacilityScheduleChecker()
    return _global_schedule_checker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏢 公共设施营业时间检查器测试")
    print("=" * 70)
    
    checker = get_schedule_checker()
    
    # 测试医院营业状态
    print("\n1. 测试医院营业状态（当前时间）...")
    status = checker.check_facility_status("hospital")
    print(f"   是否营业: {status['is_open']}")
    if status['message']:
        print(f"   提示消息: {status['message']}")
    
    # 测试非营业时间
    print("\n2. 测试医院非营业时间（中午12点30分）...")
    test_time = datetime.now().replace(hour=12, minute=30)
    status = checker.check_facility_status("hospital", test_time)
    print(f"   是否营业: {status['is_open']}")
    if status['message']:
        print(f"   提示消息: {status['message']}")
    
    print("\n" + "=" * 70)
