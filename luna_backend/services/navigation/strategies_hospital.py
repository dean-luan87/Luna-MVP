"""
医院场景策略 (Hospital Strategies) v1.2.0
挂号/候诊/科室导航等医院场景专用策略
"""

from typing import Optional, Dict, Any
from .strategies_base import BaseStrategy
from .context import NavigationContext

# 延迟导入
def _get_error_reporter():
    try:
        from luna_backend.services.log.error_reporter import ErrorReporter
        return ErrorReporter
    except ImportError:
        try:
            from services.log.error_reporter import ErrorReporter
            return ErrorReporter
        except ImportError:
            return None

def _get_error_codes():
    try:
        from luna_backend.config.error_codes import ERR
        return ERR
    except ImportError:
        try:
            from config.error_codes import ERR
            return ERR
        except ImportError:
            class DummyERR:
                NAV_HOSPITAL_TICKET_PARSE_FAIL = 400009
            return DummyERR()


class HospitalStageGuardStrategy(BaseStrategy):
    """
    总控：根据 hospital_stage 决定当前使用哪一组策略
    """
    
    STRATEGY_NAME = "HOSPITAL_STAGE_GUARD"
    
    def should_execute(self) -> bool:
        """判断是否应该执行"""
        return self.ctx.scene_type == "hospital"
    
    def execute(self) -> Dict[str, Any]:
        """
        执行医院阶段守卫策略
        
        Returns:
            策略执行结果
        """
        # 这里只做"状态检查/纠偏"，不直接播报导航指令
        if self.ctx.hospital_stage == "unknown":
            return {
                "success": True,
                "action": "ASK_CLARIFY_HOSPITAL_STAGE",
                "text": "我们现在是在挂号、等候，还是已经到科室门口了呢？",
                "strategy": self.STRATEGY_NAME,
            }
        return {
            "success": True,
            "action": "NO_ACTION",
            "text": "",
            "strategy": self.STRATEGY_NAME,
        }


class HospitalRegistrationStrategy(BaseStrategy):
    """
    挂号阶段：优先引导到咨询台 / 挂号窗口
    """
    
    STRATEGY_NAME = "HOSPITAL_REGISTRATION"
    
    def should_execute(self) -> bool:
        """判断是否应该执行"""
        return (
            self.ctx.scene_type == "hospital" and
            self.ctx.hospital_stage in ("entering", "registration") and
            not self.ctx.has_registered
        )
    
    def execute(self) -> Dict[str, Any]:
        """
        执行挂号策略
        
        Returns:
            策略执行结果
        """
        # 已挂号则不处理
        if self.ctx.has_registered:
            return {
                "success": True,
                "action": "NO_ACTION",
                "text": "",
                "strategy": self.STRATEGY_NAME,
            }
        
        # 简单版本：如果人很多 & path_blocked → 建议找工作人员
        if self.ctx.people_density > 0.7 or self.ctx.path_blocked:
            return {
                "success": True,
                "action": "GO_TO_STAFF",
                "text": "现在大厅人比较多，建议先找到前台或穿制服的工作人员，让他们帮你挂号。",
                "strategy": self.STRATEGY_NAME,
            }
        
        # 默认：引导去挂号区域
        return {
            "success": True,
            "action": "NAV_TO_REGISTRATION_AREA",
            "text": "我们先去挂号窗口，你可以跟着大厅里的"挂号收费处"或"门诊大厅"的指示牌走。",
            "strategy": self.STRATEGY_NAME,
        }


class HospitalWaitingStrategy(BaseStrategy):
    """
    候诊阶段：根据叫号屏 / 当前号码，决定是休息还是靠近门口
    """
    
    STRATEGY_NAME = "HOSPITAL_WAITING"
    
    def should_execute(self) -> bool:
        """判断是否应该执行"""
        return (
            self.ctx.scene_type == "hospital" and
            self.ctx.hospital_stage == "waiting"
        )
    
    def execute(self) -> Dict[str, Any]:
        """
        执行候诊策略
        
        Returns:
            策略执行结果
        """
        if not self.ctx.registration_ticket_no:
            return {
                "success": True,
                "action": "ASK_TICKET_NO",
                "text": "你现在手里有排队号码吗？可以念给我听，我帮你记住。",
                "strategy": self.STRATEGY_NAME,
            }
        
        if not self.ctx.called_ticket_no:
            # 没有叫号信息，只提醒"注意叫号"
            return {
                "success": True,
                "action": "WAIT_IN_SITTING_AREA",
                "text": "你可以先在候诊区找个地方坐下休息，我会提醒你注意叫号。",
                "strategy": self.STRATEGY_NAME,
            }
        
        # 简单差值判断
        try:
            my_no = int(self.ctx.registration_ticket_no)
            called = int(self.ctx.called_ticket_no)
            delta = my_no - called
        except ValueError:
            ErrorReporter = _get_error_reporter()
            ERR = _get_error_codes()
            if ErrorReporter:
                ErrorReporter.report(
                    ERR.NAV_HOSPITAL_TICKET_PARSE_FAIL,
                    {
                        "ticket": self.ctx.registration_ticket_no,
                        "called": self.ctx.called_ticket_no
                    }
                )
            return {
                "success": True,
                "action": "WAIT_UNCERTAIN",
                "text": "现在叫号信息有点看不清，你可以稍微靠近门口一点，注意听叫号。",
                "strategy": self.STRATEGY_NAME,
            }
        
        if delta > 3:
            return {
                "success": True,
                "action": "WAIT_AND_REST",
                "text": f"你前面大约还有 {delta} 位，可以在候诊区坐一会儿，我帮你留意情况。",
                "strategy": self.STRATEGY_NAME,
            }
        elif 1 <= delta <= 3:
            return {
                "success": True,
                "action": "MOVE_NEAR_DOOR",
                "text": f"已经快轮到你了，建议你慢慢走到诊室门口附近等候。",
                "strategy": self.STRATEGY_NAME,
            }
        else:
            return {
                "success": True,
                "action": "READY_TO_ENTER",
                "text": "已经轮到你或者马上就轮到了，你可以轻轻敲门，确认一下是否可以进去。",
                "strategy": self.STRATEGY_NAME,
            }


class HospitalDepartmentNavigationStrategy(BaseStrategy):
    """
    目标科室导航：根据 OCR 的楼层/门牌信息指导方向（简版）
    """
    
    STRATEGY_NAME = "HOSPITAL_DEPARTMENT_NAV"
    
    def should_execute(self) -> bool:
        """判断是否应该执行"""
        return (
            self.ctx.scene_type == "hospital" and
            self.ctx.hospital_stage in ("registration_done", "finding_dept")
        )
    
    def execute(self) -> Dict[str, Any]:
        """
        执行科室导航策略
        
        Returns:
            策略执行结果
        """
        if not self.ctx.department_name:
            return {
                "success": True,
                "action": "ASK_DEPARTMENT_NAME",
                "text": "你挂的是哪个科？比如眼科、骨科、心内科，我帮你记一下。",
                "strategy": self.STRATEGY_NAME,
            }
        
        # 这里可以结合 OCR 的 zone_state / sign_text 做更复杂逻辑
        if self.ctx.zone_state and self.ctx.department_name in (self.ctx.zone_state or ""):
            return {
                "success": True,
                "action": "IN_CORRECT_ZONE",
                "text": f"你已经在{self.ctx.zone_state}区域了，可以沿着走廊慢慢找 {self.ctx.department_name} 的诊室。",
                "strategy": self.STRATEGY_NAME,
            }
        
        # 默认提示：先找到楼层，再找区域
        return {
            "success": True,
            "action": "NAV_FLOOR_THEN_ZONE",
            "text": f"我们先确认 {self.ctx.department_name} 在几楼，如果有楼层导览图，可以靠近一点，我帮你看。",
            "strategy": self.STRATEGY_NAME,
        }



