# task_chain_router.py

from core.taskchain.behavior_map import BEHAVIOR_MAP
from core.taskchain.label_event import LabelEvent
from decision.task_chain.task_chain import TaskChain


class TaskChainRouter:
    """
    任务链路由器：根据标签事件决定任务链切换
    """
    
    def __init__(self, task_manager=None, tts=None):
        self.task_manager = task_manager
        self.tts = tts
        self.min_confidence = 0.6  # 最低置信度阈值
    
    def on_label_detected(self, event: LabelEvent):
        """
        处理标签检测事件
        
        参数：
        - event: LabelEvent 对象
        """
        label = event.label
        
        if label not in BEHAVIOR_MAP:
            return  # 未知标签，忽略
        
        rule = BEHAVIOR_MAP[label]
        
        # 信心不足忽略
        if event.confidence < self.min_confidence:
            return
        
        mode = rule["mode"]
        chain_name = rule["task_chain"]
        priority = rule.get("priority", 0)
        
        if mode == "force":
            # 强制模式：危险情况，立即停止
            if self.tts:
                self.tts.speak("注意危险！请立即停下。")
            if self.task_manager:
                chain = TaskChain(chain_name)
                self.task_manager.force_start(chain_name, chain)
        
        elif mode == "switch":
            # 切换模式：完整替换主任务链
            if self.tts:
                label_name = self._get_label_name(label)
                self.tts.speak(f"检测到{label_name}，我将为您执行相关流程。")
            if self.task_manager:
                chain = TaskChain(chain_name)
                self.task_manager.switch_to(chain_name, chain)
        
        elif mode == "insert":
            # 插入模式：插入任务链，保留主任务
            if self.task_manager:
                chain = TaskChain(chain_name)
                self.task_manager.insert_task(chain_name, chain)
        
        elif mode == "continue":
            # 继续模式：追加上下文任务
            if self.task_manager:
                chain = TaskChain(chain_name)
                self.task_manager.append_contextual(chain_name, chain)
    
    def _get_label_name(self, label):
        """
        获取标签的中文名称（用于语音播报）
        """
        label_names = {
            "Toilet": "厕所",
            "Elevator": "电梯",
            "Stair": "楼梯",
            "Registration": "挂号窗口",
            "Payment": "缴费窗口",
            "InquiryDesk": "咨询台",
            "SubwayEntrance": "地铁入口",
            "BusStop": "公交站",
            "Danger": "危险"
        }
        return label_names.get(label, label)

