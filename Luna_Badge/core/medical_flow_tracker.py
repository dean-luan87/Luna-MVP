"""
医疗流程追踪模块
识别就医流程并判断当前环节
"""

import logging
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class MedicalPhase(Enum):
    """医疗流程阶段"""
    NOT_STARTED = "not_started"           # 未开始
    REGISTERED = "registered"             # 已挂号
    TRIAGE = "triage"                     # 分诊
    WAITING = "waiting"                   # 候诊
    CALLED = "called"                     # 已叫号
    IN_CONSULTATION = "in_consultation"   # 就诊中
    EXAM_APPOINTED = "exam_appointed"     # 检查预约
    EXAM_WAITING = "exam_waiting"         # 检查候诊
    PAYMENT = "payment"                   # 缴费
    COMPLETED = "completed"               # 完成
    REGISTRATION_ERROR = "registration_error"  # 挂号错误


@dataclass
class FlowStep:
    """流程步骤"""
    phase: MedicalPhase
    location: str                         # 位置描述
    required: bool = True                 # 是否必需
    estimated_time: int = 0               # 预估时间（分钟）
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "phase": self.phase.value,
            "location": self.location,
            "required": self.required,
            "estimated_time": self.estimated_time
        }


class MedicalFlowTracker:
    """医疗流程追踪器"""
    
    def __init__(self):
        """初始化医疗流程追踪器"""
        self.logger = logging.getLogger(__name__)
        
        # 标准就医流程
        self.standard_flow = [
            FlowStep(MedicalPhase.REGISTERED, "挂号处", required=True, estimated_time=5),
            FlowStep(MedicalPhase.TRIAGE, "分诊台", required=True, estimated_time=3),
            FlowStep(MedicalPhase.WAITING, "候诊区", required=True, estimated_time=30),
            FlowStep(MedicalPhase.CALLED, "诊室", required=True, estimated_time=0),
            FlowStep(MedicalPhase.IN_CONSULTATION, "诊室内", required=True, estimated_time=10),
            FlowStep(MedicalPhase.PAYMENT, "缴费处", required=False, estimated_time=5),
            FlowStep(MedicalPhase.COMPLETED, "完成", required=False, estimated_time=0)
        ]
        
        # 当前流程状态
        self.current_phase: MedicalPhase = MedicalPhase.NOT_STARTED
        self.registration_info: Dict[str, Any] = {}  # 挂号信息
        self.completed_steps: List[MedicalPhase] = []
        
        self.logger.info("🏥 医疗流程追踪器初始化完成")
    
    def detect_current_phase(self,
                            detected_signs: List[str],
                            current_location: Optional[str] = None) -> Dict[str, Any]:
        """
        检测当前医疗流程阶段
        
        Args:
            detected_signs: 检测到的标识文字列表（如["挂号处", "候诊区"]）
            current_location: 当前位置描述
        
        Returns:
            Dict[str, Any]: 当前阶段信息
        """
        # 根据检测到的标识判断阶段
        phase_keywords = {
            MedicalPhase.REGISTERED: ["挂号处", "挂号", "注册"],
            MedicalPhase.TRIAGE: ["分诊", "分诊台", "导诊"],
            MedicalPhase.WAITING: ["候诊", "候诊区", "等候"],
            MedicalPhase.CALLED: ["叫号", "请", "号"],
            MedicalPhase.IN_CONSULTATION: ["诊室", "科室", "医生"],
            MedicalPhase.PAYMENT: ["缴费", "收费", "结算"]
        }
        
        detected_phase = None
        confidence = 0.0
        
        for phase, keywords in phase_keywords.items():
            matches = sum(1 for sign in detected_signs if any(kw in sign for kw in keywords))
            if matches > 0:
                phase_confidence = matches / len(keywords)
                if phase_confidence > confidence:
                    confidence = phase_confidence
                    detected_phase = phase
        
        if detected_phase:
            self.current_phase = detected_phase
            if detected_phase not in self.completed_steps:
                self.completed_steps.append(detected_phase)
        
        # 检查流程完整性
        missing_steps = self._check_missing_steps()
        
        return {
            "current_phase": self.current_phase.value,
            "confidence": confidence,
            "detected_location": current_location,
            "missing_steps": [s.value for s in missing_steps],
            "next_step": self._get_next_step()
        }
    
    def check_registration_match(self,
                                registered_dept: str,
                                current_location: str,
                                detected_signs: List[str]) -> Dict[str, Any]:
        """
        检查挂号科室与当前位置是否匹配
        
        Args:
            registered_dept: 挂号科室（如"内科"）
            current_location: 当前位置
            detected_signs: 检测到的标识
        
        Returns:
            Dict[str, Any]: 匹配检查结果
        """
        # 提取当前位置的科室信息
        dept_keywords = ["内科", "外科", "儿科", "妇科", "牙科", "口腔科", 
                        "眼科", "耳鼻喉科", "皮肤科", "精神科"]
        
        current_dept = None
        for sign in detected_signs:
            for dept in dept_keywords:
                if dept in sign:
                    current_dept = dept
                    break
            if current_dept:
                break
        
        # 判断是否匹配
        matched = False
        if current_dept:
            # 简化匹配逻辑（实际应使用更智能的匹配）
            if registered_dept == current_dept or registered_dept in current_dept or current_dept in registered_dept:
                matched = True
        
        if not matched and current_dept:
            self.current_phase = MedicalPhase.REGISTRATION_ERROR
            
            return {
                "matched": False,
                "registered_dept": registered_dept,
                "current_dept": current_dept,
                "message": f"您的挂号记录为{registered_dept}，但当前楼层是{current_dept}，是否需要我帮您确认挂号情况并前往咨询台？",
                "requires_confirmation": True
            }
        
        return {
            "matched": matched,
            "registered_dept": registered_dept,
            "current_dept": current_dept,
            "message": None
        }
    
    def _check_missing_steps(self) -> List[MedicalPhase]:
        """检查缺失的流程步骤"""
        if self.current_phase == MedicalPhase.NOT_STARTED:
            return [MedicalPhase.REGISTERED]
        
        missing = []
        for step in self.standard_flow:
            if step.phase not in self.completed_steps and step.required:
                # 只检查在当前阶段之前的必需步骤
                phase_index = next((i for i, s in enumerate(self.standard_flow) if s.phase == self.current_phase), 0)
                step_index = next((i for i, s in enumerate(self.standard_flow) if s.phase == step.phase), 0)
                if step_index < phase_index:
                    missing.append(step.phase)
        
        return missing
    
    def _get_next_step(self) -> Optional[FlowStep]:
        """获取下一步流程"""
        current_index = next((i for i, s in enumerate(self.standard_flow) 
                            if s.phase == self.current_phase), -1)
        
        if current_index >= 0 and current_index < len(self.standard_flow) - 1:
            return self.standard_flow[current_index + 1]
        
        return None
    
    def get_flow_status(self) -> Dict[str, Any]:
        """获取流程状态"""
        return {
            "current_phase": self.current_phase.value,
            "completed_steps": [s.value for s in self.completed_steps],
            "next_step": self._get_next_step().to_dict() if self._get_next_step() else None,
            "registration_info": self.registration_info
        }


# 全局医疗流程追踪器实例
_global_flow_tracker: Optional[MedicalFlowTracker] = None


def get_medical_flow_tracker() -> MedicalFlowTracker:
    """获取全局医疗流程追踪器实例"""
    global _global_flow_tracker
    if _global_flow_tracker is None:
        _global_flow_tracker = MedicalFlowTracker()
    return _global_flow_tracker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏥 医疗流程追踪器测试")
    print("=" * 70)
    
    tracker = get_medical_flow_tracker()
    
    # 测试1: 检测当前阶段
    print("\n1. 检测当前阶段...")
    result = tracker.detect_current_phase(["候诊区", "请301号患者前往3号诊室"], "3楼候诊区")
    print(f"   当前阶段: {result['current_phase']}")
    print(f"   下一步: {result['next_step']}")
    
    # 测试2: 检查挂号匹配
    print("\n2. 检查挂号匹配...")
    match_result = tracker.check_registration_match("内科", "4楼", ["口腔科", "牙科诊室"])
    print(f"   匹配: {match_result['matched']}")
    if match_result['message']:
        print(f"   消息: {match_result['message']}")
    
    # 测试3: 获取流程状态
    print("\n3. 获取流程状态...")
    status = tracker.get_flow_status()
    print(f"   状态: {status}")
    
    print("\n" + "=" * 70)

