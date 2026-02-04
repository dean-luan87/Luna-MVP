"""
医院流程任务 (HospitalTask) v1.2.0
医院就诊任务链：进入医院 → 挂号 → 找科室 → 候诊 → 就诊 → 检查/抽血 → 取报告 → 离开
"""

from typing import Dict, Any, Optional
from .base_task import BaseTask
from services.runtime import rt

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
                HOSPITAL_FLOW_NOT_INIT = "HOSPITAL_FLOW_NOT_INIT"
            return DummyERR()


class HospitalTask(BaseTask):
    """
    医院就诊任务链：
    - 进入医院
    - 挂号
    - 找科室
    - 候诊
    - 就诊
    - 检查/取报告
    - 离开
    """
    
    def __init__(self,
                 task_id: str,
                 hospital_name: str,
                 department_name: Optional[str] = None,
                 is_first_visit: bool = True,
                 has_report_to_collect: bool = False,
                 meta: Optional[Dict[str, Any]] = None):
        """
        初始化医院任务
        
        Args:
            task_id: 任务ID
            hospital_name: 医院名称
            department_name: 科室名称（可选）
            is_first_visit: 是否首次就诊
            has_report_to_collect: 是否有报告需要取
            meta: 任务元数据
        """
        super().__init__(task_id, meta)
        self.hospital_name = hospital_name
        self.department_name = department_name
        self.is_first_visit = is_first_visit
        self.has_report_to_collect = has_report_to_collect
        
        # 阶段：entering / registration / finding_dept / waiting / in_exam / after_exam / collecting_report / leaving
        self.stage = "entering"
    
    def _get_ctx(self):
        """
        方便从导航上下文里同步医院信息
        
        Returns:
            导航上下文
        """
        if rt.navigation_manager and hasattr(rt.navigation_manager, "context"):
            return rt.navigation_manager.context
        
        # fallback：自己 new 一个（不推荐，只做兜底）
        try:
            from services.navigation.context import NavigationContext
            return NavigationContext()
        except ImportError:
            return None
    
    def _sync_ctx(self):
        """同步上下文"""
        ctx = self._get_ctx()
        if not ctx:
            return
        
        ctx.scene_type = "hospital"
        ctx.hospital_name = self.hospital_name
        ctx.hospital_stage = self.stage
        ctx.is_first_visit = self.is_first_visit
        ctx.department_name = self.department_name
        ctx.has_report_to_collect = self.has_report_to_collect
    
    # ====== 生命周期方法 ======
    
    def start(self):
        """启动任务"""
        self.state = "running"
        self.stage = "entering"
        self._sync_ctx()
        
        # 欢迎语 / 引导
        if rt.tts_manager:
            try:
                dept_text = f"再去 {self.department_name}" if self.department_name else "再去目标科室"
                welcome_text = f"好的，我们现在在 {self.hospital_name}。先帮你理一理流程：先挂号，{dept_text}。"
                if hasattr(rt.tts_manager, 'speak'):
                    rt.tts_manager.speak(welcome_text, style="calm")
            except Exception as e:
                logger = _get_logger()
                if logger:
                    logger(f"HOSPITAL_TASK_TTS_ERROR", {"error": str(e)})
    
    def handle_event(self, event: Dict[str, Any]):
        """
        根据事件推进医院流程：
        - type=voice_intent: 用户说"我挂好号了"、"我已经到三楼了"
        - type=vision: 识别到"挂号处"、"科室门牌"等
        - type=nav_update: 导航状态 / 已到达某个点
        - type=hospital_stage_update: App 主动调用，强制推进阶段（API）
        
        Args:
            event: 事件字典
        """
        if self.state not in ("running", "pending"):
            return
        
        etype = event.get("type")
        payload = event.get("payload", {})
        
        if etype == "hospital_stage_update":
            self._handle_stage_update(payload)
        elif etype == "voice_intent":
            self._handle_voice_intent(payload)
        elif etype == "vision":
            self._handle_vision_event(payload)
        elif etype == "nav_update":
            self._handle_nav_update(payload)
        
        self._sync_ctx()
    
    # ====== 具体处理逻辑（简版骨架）======
    
    def _handle_stage_update(self, payload: Dict[str, Any]):
        """
        由 API 直接调用：比如 /api/hospital/update_stage
        
        payload: { "stage": "...", "ticket_no": "...", "called_no": "..." }
        
        Args:
            payload: 阶段更新负载
        """
        new_stage = payload.get("stage")
        if new_stage:
            self.stage = new_stage
        
        ctx = self._get_ctx()
        if not ctx:
            return
        
        ticket = payload.get("ticket_no")
        if ticket is not None:
            ctx.registration_ticket_no = ticket
        
        called = payload.get("called_no")
        if called is not None:
            ctx.called_ticket_no = called
        
        if new_stage == "registration_done":
            ctx.has_registered = True
        
        if new_stage == "waiting":
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("挂号完成了，我们一起去科室附近的候诊区，找个地方坐一会儿。", style="calm")
                except:
                    pass
    
    def _handle_voice_intent(self, payload: Dict[str, Any]):
        """
        payload: { "intent": "HOSPITAL_REGISTER_DONE", "slots": {...} }
        
        Args:
            payload: 语音意图负载
        """
        intent = payload.get("intent")
        slots = payload.get("slots", {})
        
        ctx = self._get_ctx()
        if not ctx:
            return
        
        if intent == "HOSPITAL_REGISTER_DONE":
            self.stage = "registration_done"
            ticket = slots.get("ticket_no")
            ctx.has_registered = True
            ctx.registration_ticket_no = ticket
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("好的，我记住你的排队号码了，我们去对应科室楼层。", style="cheerful")
                except:
                    pass
        
        elif intent == "HOSPITAL_ARRIVE_FLOOR":
            self.stage = "finding_dept"
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("好，我们现在在正确的楼层了，可以沿着走廊慢慢靠近诊室。", style="calm")
                except:
                    pass
        
        elif intent == "HOSPITAL_IN_ROOM":
            self.stage = "in_exam"
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("已经在诊室里了，我先安静一下，你有需要再叫我。", style="gentle")
                except:
                    pass
        
        elif intent == "HOSPITAL_NEED_REPORT":
            self.has_report_to_collect = True
            ctx.has_report_to_collect = True
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("好的，后面我们记得去取报告，我帮你记着。", style="calm")
                except:
                    pass
    
    def _handle_vision_event(self, payload: Dict[str, Any]):
        """
        视觉事件：比如识别到"挂号处"、"抽血室"、"报告打印"等标识牌
        
        Args:
            payload: 视觉事件负载
        """
        ocr_texts = payload.get("ocr_texts", [])  # ["挂号处", "收费", ...]
        if not ocr_texts:
            return
        
        text_all = " ".join(ocr_texts)
        
        if "挂号" in text_all and self.stage == "entering":
            self.stage = "registration"
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("前面就是挂号收费处，我们可以靠近一些，排队办理挂号。", style="calm")
                except:
                    pass
        
        if self.department_name and self.department_name in text_all:
            # 识别到目标科室区域
            ctx = self._get_ctx()
            if ctx:
                ctx.zone_state = f"{self.department_name} 区域"
                if rt.tts_manager:
                    try:
                        if hasattr(rt.tts_manager, 'speak'):
                            rt.tts_manager.speak(f"已经到 {self.department_name} 附近了，可以找一下你的诊室编号。", style="calm")
                    except:
                        pass
    
    def _handle_nav_update(self, payload: Dict[str, Any]):
        """
        导航更新: { "status": {...}, "arrived": True/False }
        
        Args:
            payload: 导航更新负载
        """
        if payload.get("arrived") and self.stage == "registration":
            # 导航到挂号区完成
            if rt.tts_manager:
                try:
                    if hasattr(rt.tts_manager, 'speak'):
                        rt.tts_manager.speak("我们已经到挂号窗口附近了，你可以询问工作人员如何挂号。", style="calm")
                except:
                    pass


def _get_logger():
    """获取日志函数"""
    try:
        from luna_backend.utils.logger import log_navigation
        return log_navigation
    except ImportError:
        try:
            from utils.logger import log_navigation
            return log_navigation
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log



