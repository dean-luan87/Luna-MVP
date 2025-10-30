"""
医疗复诊追踪器
记录复诊与检查任务，提供自动提醒
"""

import logging
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """任务类型"""
    FOLLOW_UP = "复诊"
    EXAMINATION = "检查"
    MEDICATION = "取药"
    REPORT = "取报告"
    APPOINTMENT = "预约"
    OTHER = "其他"


class ReminderType(Enum):
    """提醒类型"""
    ONE_DAY_BEFORE = "提前1天"
    TWO_HOURS_BEFORE = "提前2小时"
    THIRTY_MINUTES_BEFORE = "提前30分钟"
    CUSTOM = "自定义"


@dataclass
class MedicalTask:
    """医疗任务"""
    task_id: str
    task_type: TaskType
    department: str
    doctor: str
    scheduled_time: datetime
    reminder_type: ReminderType
    description: str
    status: str = "pending"  # pending/completed/cancelled
    created_at: datetime = None
    reminder_sent: bool = False
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "department": self.department,
            "doctor": self.doctor,
            "scheduled_time": self.scheduled_time.isoformat(),
            "reminder_type": self.reminder_type.value,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "reminder_sent": self.reminder_sent
        }


class MedicalFollowupTracker:
    """医疗复诊追踪器"""
    
    def __init__(self, storage_file: str = "data/medical_tasks.json"):
        """初始化医疗复诊追踪器"""
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        self.medical_tasks: List[MedicalTask] = []
        
        # 时间关键词映射
        self.time_keywords = {
            "今天": 0,
            "明天": 1,
            "后天": 2,
            "本周": 7,
            "下周": 7,
            "下周一": 7,
            "下周二": 8,
            "下周三": 9,
            "下周四": 10,
            "下周五": 11,
            "下周六": 12,
            "下周日": 13,
            "周五": 5,  # 添加周五
            "周一": 1,
            "周二": 2,
            "周三": 3,
            "周四": 4,
            "周六": 6,
            "周日": 7
        }
        
        # 科室关键词
        self.department_keywords = [
            "内科", "外科", "儿科", "妇科", "牙科", "眼科", "耳鼻喉科",
            "皮肤科", "精神科", "心内科", "消化科", "呼吸科"
        ]
        
        self._load_data()
        self.logger.info("📅 医疗复诊追踪器初始化完成")
    
    def parse_voice_task(self, voice_text: str) -> Dict[str, Any]:
        """
        解析语音任务
        
        Args:
            voice_text: 语音识别文本
        
        Returns:
            Dict[str, Any]: 解析结果
        """
        # 提取任务类型
        task_type = self._extract_task_type(voice_text)
        
        # 提取时间信息
        time_info = self._extract_time_info(voice_text)
        
        # 提取科室信息
        department = self._extract_department(voice_text)
        
        # 提取医生信息
        doctor = self._extract_doctor(voice_text)
        
        if not time_info["success"]:
            return {
                "success": False,
                "error": "无法解析时间信息",
                "message": "请提供具体时间，如'明天下午两点'或'周五复诊'"
            }
        
        # 创建任务
        task_id = f"task_{int(datetime.now().timestamp() * 1000)}"
        
        task = MedicalTask(
            task_id=task_id,
            task_type=task_type,
            department=department,
            doctor=doctor,
            scheduled_time=time_info["datetime"],
            reminder_type=ReminderType.ONE_DAY_BEFORE,
            description=voice_text
        )
        
        # 保存任务
        self.medical_tasks.append(task)
        self._save_data()
        
        return {
            "success": True,
            "task": task.to_dict(),
            "message": f"已记录{task_type.value}任务：{department} - {time_info['datetime'].strftime('%Y-%m-%d %H:%M')}"
        }
    
    def check_reminders(self, current_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        检查需要提醒的任务
        
        Args:
            current_time: 当前时间
        
        Returns:
            List[Dict[str, Any]]: 需要提醒的任务列表
        """
        if current_time is None:
            current_time = datetime.now()
        
        reminders = []
        
        for task in self.medical_tasks:
            if task.status != "pending" or task.reminder_sent:
                continue
            
            # 计算提醒时间
            reminder_time = self._calculate_reminder_time(task.scheduled_time, task.reminder_type)
            
            if current_time >= reminder_time:
                reminder_info = {
                    "task": task.to_dict(),
                    "reminder_message": self._generate_reminder_message(task),
                    "time_until_task": self._time_until_task(task.scheduled_time, current_time)
                }
                reminders.append(reminder_info)
                
                # 标记已发送提醒
                task.reminder_sent = True
        
        if reminders:
            self._save_data()
        
        return reminders
    
    def get_upcoming_tasks(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        获取即将到来的任务
        
        Args:
            days_ahead: 提前天数
        
        Returns:
            List[Dict[str, Any]]: 即将到来的任务列表
        """
        current_time = datetime.now()
        end_time = current_time + timedelta(days=days_ahead)
        
        upcoming_tasks = []
        
        for task in self.medical_tasks:
            if task.status == "pending" and current_time <= task.scheduled_time <= end_time:
                upcoming_tasks.append({
                    "task": task.to_dict(),
                    "days_until": (task.scheduled_time - current_time).days,
                    "hours_until": (task.scheduled_time - current_time).total_seconds() / 3600
                })
        
        # 按时间排序
        upcoming_tasks.sort(key=lambda x: x["task"]["scheduled_time"])
        
        return upcoming_tasks
    
    def complete_task(self, task_id: str) -> bool:
        """
        完成任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            bool: 是否成功完成
        """
        for task in self.medical_tasks:
            if task.task_id == task_id:
                task.status = "completed"
                self._save_data()
                self.logger.info(f"✅ 任务已完成: {task_id}")
                return True
        
        return False
    
    def _extract_task_type(self, voice_text: str) -> TaskType:
        """提取任务类型"""
        voice_lower = voice_text.lower()
        
        if any(keyword in voice_lower for keyword in ["复诊", "复查", "复检"]):
            return TaskType.FOLLOW_UP
        elif any(keyword in voice_lower for keyword in ["检查", "体检", "化验", "CT", "MRI"]):
            return TaskType.EXAMINATION
        elif any(keyword in voice_lower for keyword in ["取药", "拿药", "药房"]):
            return TaskType.MEDICATION
        elif any(keyword in voice_lower for keyword in ["取报告", "拿报告", "报告"]):
            return TaskType.REPORT
        elif any(keyword in voice_lower for keyword in ["预约", "挂号"]):
            return TaskType.APPOINTMENT
        else:
            return TaskType.OTHER
    
    def _extract_time_info(self, voice_text: str) -> Dict[str, Any]:
        """提取时间信息"""
        voice_lower = voice_text.lower()
        
        # 检查相对时间
        for keyword, days_offset in self.time_keywords.items():
            if keyword in voice_lower:
                base_date = datetime.now() + timedelta(days=days_offset)
                
                # 提取具体时间
                time_match = re.search(r'(\d{1,2})[点:](\d{1,2})', voice_text)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    scheduled_time = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                else:
                    # 默认时间
                    scheduled_time = base_date.replace(hour=9, minute=0, second=0, microsecond=0)
                
                return {
                    "success": True,
                    "datetime": scheduled_time,
                    "type": "relative"
                }
        
        # 检查绝对时间
        date_match = re.search(r'(\d{4})[年-](\d{1,2})[月-](\d{1,2})[日]?', voice_text)
        if date_match:
            year = int(date_match.group(1))
            month = int(date_match.group(2))
            day = int(date_match.group(3))
            
            time_match = re.search(r'(\d{1,2})[点:](\d{1,2})', voice_text)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
            else:
                hour, minute = 9, 0
            
            scheduled_time = datetime(year, month, day, hour, minute)
            
            return {
                "success": True,
                "datetime": scheduled_time,
                "type": "absolute"
            }
        
        return {"success": False}
    
    def _extract_department(self, voice_text: str) -> str:
        """提取科室信息"""
        for dept in self.department_keywords:
            if dept in voice_text:
                return dept
        return "未知科室"
    
    def _extract_doctor(self, voice_text: str) -> str:
        """提取医生信息"""
        doctor_match = re.search(r'([李王张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段雷钱汤尹黎易常武乔贺赖龚文][\u4e00-\u9fa5]{1,2})医生', voice_text)
        if doctor_match:
            return doctor_match.group(1) + "医生"
        return "未指定医生"
    
    def _calculate_reminder_time(self, scheduled_time: datetime, reminder_type: ReminderType) -> datetime:
        """计算提醒时间"""
        if reminder_type == ReminderType.ONE_DAY_BEFORE:
            return scheduled_time - timedelta(days=1)
        elif reminder_type == ReminderType.TWO_HOURS_BEFORE:
            return scheduled_time - timedelta(hours=2)
        elif reminder_type == ReminderType.THIRTY_MINUTES_BEFORE:
            return scheduled_time - timedelta(minutes=30)
        else:
            return scheduled_time - timedelta(days=1)
    
    def _generate_reminder_message(self, task: MedicalTask) -> str:
        """生成提醒消息"""
        return f"提醒：您有{task.task_type.value}任务，{task.department} - {task.doctor}，时间：{task.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
    
    def _time_until_task(self, scheduled_time: datetime, current_time: datetime) -> str:
        """计算距离任务的时间"""
        diff = scheduled_time - current_time
        if diff.days > 0:
            return f"{diff.days}天{diff.seconds // 3600}小时"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}小时{(diff.seconds % 3600) // 60}分钟"
        else:
            return f"{diff.seconds // 60}分钟"
    
    def _load_data(self):
        """加载数据"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for task_data in data.get("medical_followups", []):
                        task_data["scheduled_time"] = datetime.fromisoformat(task_data["scheduled_time"])
                        task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                        task_data["task_type"] = TaskType(task_data["task_type"])
                        task_data["reminder_type"] = ReminderType(task_data["reminder_type"])
                        task = MedicalTask(**task_data)
                        self.medical_tasks.append(task)
                self.logger.info("✅ 已加载医疗任务数据")
            except Exception as e:
                self.logger.error(f"❌ 加载医疗任务数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                "medical_followups": [task.to_dict() for task in self.medical_tasks],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug("💾 医疗任务数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存医疗任务数据失败: {e}")


# 全局医疗复诊追踪器实例
_global_followup_tracker: Optional[MedicalFollowupTracker] = None


def get_followup_tracker() -> MedicalFollowupTracker:
    """获取全局医疗复诊追踪器实例"""
    global _global_followup_tracker
    if _global_followup_tracker is None:
        _global_followup_tracker = MedicalFollowupTracker()
    return _global_followup_tracker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📅 医疗复诊追踪器测试")
    print("=" * 70)
    
    tracker = get_followup_tracker()
    
    # 测试1: 解析语音任务
    print("\n1. 解析语音任务...")
    result = tracker.parse_voice_task("Luna，医生让我周五复诊")
    print(f"   解析成功: {result['success']}")
    if result['success']:
        print(f"   任务类型: {result['task']['task_type']}")
        print(f"   时间: {result['task']['scheduled_time']}")
        print(f"   消息: {result['message']}")
    
    # 测试2: 检查提醒
    print("\n2. 检查提醒...")
    reminders = tracker.check_reminders()
    print(f"   需要提醒的任务: {len(reminders)}个")
    
    # 测试3: 获取即将到来的任务
    print("\n3. 获取即将到来的任务...")
    upcoming = tracker.get_upcoming_tasks(7)
    print(f"   即将到来的任务: {len(upcoming)}个")
    for task_info in upcoming:
        print(f"   - {task_info['task']['task_type']}: {task_info['task']['scheduled_time']}")
    
    print("\n" + "=" * 70)
