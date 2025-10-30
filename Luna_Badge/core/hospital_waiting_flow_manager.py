"""
医院候诊智能引导模块
管理候诊全流程：区域确认、排队监测、叫号监听、进门引导
"""

import logging
import time
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class WaitingState(Enum):
    """候诊状态"""
    LOCATING_AREA = "locating_area"       # 定位区域
    CONFIRMING_POSITION = "confirming_position"  # 确认位置
    WAITING_FOR_NUMBER = "waiting_for_number"     # 等待叫号
    NUMBER_CALLED = "number_called"       # 已叫号
    APPROACHING_ROOM = "approaching_room" # 接近诊室
    ENTERING_ROOM = "entering_room"       # 进入诊室
    COMPLETED = "completed"               # 完成


class AreaDirection(Enum):
    """区域方向"""
    EAST = "东"
    WEST = "西"
    SOUTH = "南"
    NORTH = "北"
    CENTER = "中心"
    UNKNOWN = "未知"


@dataclass
class WaitingInfo:
    """候诊信息"""
    department: str
    room: str
    floor: int
    user_number: int
    current_called: int
    user_position: str
    room_position: str
    area_direction: AreaDirection
    estimated_wait_time: int = 0  # 预估等待时间（分钟）
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "department": self.department,
            "room": self.room,
            "floor": self.floor,
            "user_number": self.user_number,
            "current_called": self.current_called,
            "user_position": self.user_position,
            "room_position": self.room_position,
            "area_direction": self.area_direction.value,
            "estimated_wait_time": self.estimated_wait_time
        }


class HospitalWaitingFlowManager:
    """医院候诊流程管理器"""
    
    def __init__(self):
        """初始化候诊流程管理器"""
        self.logger = logging.getLogger(__name__)
        
        # 当前候诊状态
        self.current_state: WaitingState = WaitingState.LOCATING_AREA
        self.waiting_info: Optional[WaitingInfo] = None
        
        # 区域关键词映射
        self.area_keywords = {
            AreaDirection.EAST: ["东", "东区", "东侧", "东边"],
            AreaDirection.WEST: ["西", "西区", "西侧", "西边"],
            AreaDirection.SOUTH: ["南", "南区", "南侧", "南边"],
            AreaDirection.NORTH: ["北", "北区", "北侧", "北边"],
            AreaDirection.CENTER: ["中心", "中央", "中区"]
        }
        
        # 叫号监听关键词
        self.calling_keywords = ["号", "请", "到", "诊室"]
        
        # 门口状态检测
        self.doorway_check_timeout = 15  # 门口等待超时时间（秒）
        self.last_doorway_check = 0
        
        self.logger.info("🏥 医院候诊流程管理器初始化完成")
    
    def start_waiting_flow(self, waiting_info: WaitingInfo) -> Dict[str, Any]:
        """
        开始候诊流程
        
        Args:
            waiting_info: 候诊信息
        
        Returns:
            Dict[str, Any]: 流程启动结果
        """
        self.waiting_info = waiting_info
        self.current_state = WaitingState.LOCATING_AREA
        
        self.logger.info(f"🏥 开始候诊流程: {waiting_info.department} - {waiting_info.room}")
        
        return {
            "success": True,
            "current_state": self.current_state.value,
            "waiting_info": waiting_info.to_dict(),
            "next_action": "开始区域定位"
        }
    
    def check_area_positioning(self, detected_signs: List[str]) -> Dict[str, Any]:
        """
        检查区域定位
        
        Args:
            detected_signs: 检测到的标识文字
        
        Returns:
            Dict[str, Any]: 区域定位结果
        """
        if not self.waiting_info:
            return {"success": False, "error": "未初始化候诊信息"}
        
        # 提取当前区域信息
        current_area = self._extract_area_from_signs(detected_signs)
        target_area = self._extract_area_from_position(self.waiting_info.room_position)
        
        # 判断区域是否匹配
        area_matched = self._check_area_match(current_area, target_area)
        
        if area_matched:
            self.current_state = WaitingState.CONFIRMING_POSITION
            message = f"您当前在{current_area.value}区，目标科室{self.waiting_info.room}也在{target_area.value}区，方向正确。"
            next_action = "引导靠近科室门牌"
        else:
            message = f"您当前在{current_area.value}区，但目标科室{self.waiting_info.room}在{target_area.value}区，请调整方向。"
            next_action = "提醒用户校正方向"
        
        return {
            "success": True,
            "area_matched": area_matched,
            "current_area": current_area.value,
            "target_area": target_area.value,
            "message": message,
            "next_action": next_action,
            "current_state": self.current_state.value
        }
    
    def monitor_queue_status(self, current_called_number: int) -> Dict[str, Any]:
        """
        监测排队状态
        
        Args:
            current_called_number: 当前叫号
        
        Returns:
            Dict[str, Any]: 排队状态监测结果
        """
        if not self.waiting_info:
            return {"success": False, "error": "未初始化候诊信息"}
        
        # 更新当前叫号
        self.waiting_info.current_called = current_called_number
        
        # 计算等待人数
        wait_count = self.waiting_info.user_number - current_called_number
        
        # 判断等待建议
        if wait_count <= 0:
            # 已叫到或过号
            self.current_state = WaitingState.NUMBER_CALLED
            message = f"您的号码{self.waiting_info.user_number}已被叫到，请立即前往{self.waiting_info.room}诊室。"
            suggestion = "立即前往诊室"
        elif wait_count <= 2:
            # 即将叫到
            message = f"当前叫号{current_called_number}，您的号码{self.waiting_info.user_number}即将被叫到，请准备。"
            suggestion = "在诊室附近等待"
        else:
            # 还需等待
            estimated_time = wait_count * 3  # 假设每人3分钟
            self.waiting_info.estimated_wait_time = estimated_time
            message = f"当前叫号{current_called_number}，您的号码{self.waiting_info.user_number}还需等待{wait_count}人，预计{estimated_time}分钟。"
            suggestion = "建议寻找附近座椅休息"
        
        return {
            "success": True,
            "wait_count": wait_count,
            "estimated_wait_time": self.waiting_info.estimated_wait_time,
            "message": message,
            "suggestion": suggestion,
            "current_state": self.current_state.value
        }
    
    def listen_for_calling(self, audio_text: str) -> Dict[str, Any]:
        """
        监听叫号
        
        Args:
            audio_text: 音频识别文本
        
        Returns:
            Dict[str, Any]: 叫号监听结果
        """
        if not self.waiting_info:
            return {"success": False, "error": "未初始化候诊信息"}
        
        # 检查是否包含叫号关键词
        has_calling_keywords = any(keyword in audio_text for keyword in self.calling_keywords)
        
        if not has_calling_keywords:
            return {
                "success": True,
                "number_called": False,
                "message": "未检测到叫号信息"
            }
        
        # 提取号码
        number_match = re.search(r'(\d+)号', audio_text)
        if not number_match:
            return {
                "success": True,
                "number_called": False,
                "message": "未检测到具体号码"
            }
        
        called_number = int(number_match.group(1))
        
        # 检查是否是用户的号码
        if called_number == self.waiting_info.user_number:
            self.current_state = WaitingState.NUMBER_CALLED
            message = f"您的号码{called_number}已被叫到，请立即前往{self.waiting_info.room}诊室。"
            
            return {
                "success": True,
                "number_called": True,
                "called_number": called_number,
                "message": message,
                "current_state": self.current_state.value
            }
        
        return {
            "success": True,
            "number_called": False,
            "called_number": called_number,
            "message": f"叫到{called_number}号，您的号码{self.waiting_info.user_number}还需等待"
        }
    
    def check_doorway_status(self, detected_objects: List[str]) -> Dict[str, Any]:
        """
        检查门口状态
        
        Args:
            detected_objects: 检测到的对象列表
        
        Returns:
            Dict[str, Any]: 门口状态检查结果
        """
        if not self.waiting_info:
            return {"success": False, "error": "未初始化候诊信息"}
        
        current_time = time.time()
        
        # 检查门口是否有人员
        has_person = any(obj in ["person", "人", "医生", "护士"] for obj in detected_objects)
        has_door = any(obj in ["door", "门", "诊室门"] for obj in detected_objects)
        
        if has_person:
            # 门口有人，可以进入
            self.current_state = WaitingState.ENTERING_ROOM
            message = "诊室门口有工作人员，您可以进入。"
            suggestion = "轻敲门并进入"
            
            return {
                "success": True,
                "can_enter": True,
                "has_person": True,
                "message": message,
                "suggestion": suggestion,
                "current_state": self.current_state.value
            }
        
        # 门口无人，检查等待时间
        if self.last_doorway_check == 0:
            self.last_doorway_check = current_time
        
        wait_duration = current_time - self.last_doorway_check
        
        if wait_duration >= self.doorway_check_timeout:
            # 等待超时，给出建议
            message = "诊室门口暂时无人，您可以轻敲门并确认是否可进入，或在门外稍等片刻。"
            suggestion = "轻敲门确认或继续等待"
            
            return {
                "success": True,
                "can_enter": False,
                "has_person": False,
                "wait_duration": wait_duration,
                "message": message,
                "suggestion": suggestion,
                "current_state": self.current_state.value
            }
        
        # 继续等待
        remaining_time = self.doorway_check_timeout - wait_duration
        message = f"诊室门口暂时无人，请再等待{remaining_time:.0f}秒。"
        
        return {
            "success": True,
            "can_enter": False,
            "has_person": False,
            "wait_duration": wait_duration,
            "remaining_time": remaining_time,
            "message": message,
            "suggestion": "继续等待",
            "current_state": self.current_state.value
        }
    
    def _extract_area_from_signs(self, signs: List[str]) -> AreaDirection:
        """从标识中提取区域信息"""
        for sign in signs:
            for direction, keywords in self.area_keywords.items():
                if any(keyword in sign for keyword in keywords):
                    return direction
        return AreaDirection.UNKNOWN
    
    def _extract_area_from_position(self, position: str) -> AreaDirection:
        """从位置描述中提取区域信息"""
        for direction, keywords in self.area_keywords.items():
            if any(keyword in position for keyword in keywords):
                return direction
        return AreaDirection.UNKNOWN
    
    def _check_area_match(self, current: AreaDirection, target: AreaDirection) -> bool:
        """检查区域是否匹配"""
        if current == AreaDirection.UNKNOWN or target == AreaDirection.UNKNOWN:
            return False
        return current == target
    
    def get_current_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "current_state": self.current_state.value,
            "waiting_info": self.waiting_info.to_dict() if self.waiting_info else None
        }


# 全局候诊流程管理器实例
_global_waiting_manager: Optional[HospitalWaitingFlowManager] = None


def get_waiting_flow_manager() -> HospitalWaitingFlowManager:
    """获取全局候诊流程管理器实例"""
    global _global_waiting_manager
    if _global_waiting_manager is None:
        _global_waiting_manager = HospitalWaitingFlowManager()
    return _global_waiting_manager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏥 医院候诊流程管理器测试")
    print("=" * 70)
    
    manager = get_waiting_flow_manager()
    
    # 测试1: 开始候诊流程
    print("\n1. 开始候诊流程...")
    waiting_info = WaitingInfo(
        department="牙科",
        room="305",
        floor=3,
        user_number=28,
        current_called=26,
        user_position="3F西区",
        room_position="3F西区",
        area_direction=AreaDirection.WEST
    )
    result = manager.start_waiting_flow(waiting_info)
    print(f"   流程启动: {result['success']}")
    print(f"   当前状态: {result['current_state']}")
    
    # 测试2: 检查区域定位
    print("\n2. 检查区域定位...")
    area_result = manager.check_area_positioning(["3F西区", "牙科", "305室"])
    print(f"   区域匹配: {area_result['area_matched']}")
    print(f"   消息: {area_result['message']}")
    
    # 测试3: 监测排队状态
    print("\n3. 监测排队状态...")
    queue_result = manager.monitor_queue_status(27)
    print(f"   等待人数: {queue_result['wait_count']}")
    print(f"   建议: {queue_result['suggestion']}")
    
    # 测试4: 监听叫号
    print("\n4. 监听叫号...")
    calling_result = manager.listen_for_calling("请28号患者到305诊室")
    print(f"   号码被叫: {calling_result['number_called']}")
    if calling_result['number_called']:
        print(f"   消息: {calling_result['message']}")
    
    # 测试5: 检查门口状态
    print("\n5. 检查门口状态...")
    doorway_result = manager.check_doorway_status(["door", "诊室门"])
    print(f"   可以进入: {doorway_result['can_enter']}")
    print(f"   建议: {doorway_result['suggestion']}")
    
    print("\n" + "=" * 70)
