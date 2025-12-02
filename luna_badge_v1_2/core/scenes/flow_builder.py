# flow_builder.py

"""
FlowBuilder V2：动态任务链生成器

根据场景、标签、模板库自动生成任务链
"""

from typing import Optional, Dict, Any, List
from templates import TEMPLATE_LIBRARY


class Step:
    """
    任务步骤节点
    """
    def __init__(self, description: str, action=None, step_type: str = "action"):
        self.description = description
        self.action = action
        self.step_type = step_type
    
    def __repr__(self):
        return f"Step({self.description})"


class FlowBuilder:
    """
    动态任务链生成器
    """
    
    def __init__(self, template_library: Optional[Dict] = None, scene_classifier=None):
        self.template_library = template_library or TEMPLATE_LIBRARY
        self.scene_classifier = scene_classifier
    
    def build(self, scene: str, label: str, context_info: Optional[Dict[str, Any]] = None) -> Optional[List[Step]]:
        """
        构建任务链
        
        参数：
        - scene: 当前场景类型
        - label: 检测到的节点标签
        - context_info: 上下文信息（OCR/YOLO/地图节点等）
        
        返回：
        - 任务链步骤列表，如果无法匹配则返回 None
        """
        if context_info is None:
            context_info = {}
        
        # 获取场景模板库
        scene_templates_data = self.template_library.get(scene)
        if not scene_templates_data:
            return None
        
        templates = scene_templates_data.get("templates", {})
        
        # 找到匹配的模板
        matched_template = None
        for name, tpl in templates.items():
            if label in tpl.get("trigger", []):
                matched_template = tpl
                break
        
        if not matched_template:
            return None
        
        # 用模板步骤生成任务链
        steps = matched_template.get("steps", [])
        return self._generate_steps(steps, context_info)
    
    def _generate_steps(self, steps: List[str], info: Dict[str, Any]) -> List[Step]:
        """
        根据步骤名称列表生成任务链
        """
        chain = []
        for step_name in steps:
            node = self._make_step(step_name, info)
            if node:
                chain.append(node)
        return chain
    
    def _make_step(self, step_name: str, info: Dict[str, Any]) -> Optional[Step]:
        """
        根据步骤名称创建步骤节点
        
        核心：不同 step_name 对应不同子逻辑
        
        优先使用医院步骤工厂（如果是医院场景）
        """
        # 检查是否是医院场景的步骤
        scene = info.get("scene", "")
        if scene == "HospitalHall":
            try:
                from core.scenes.hospital_step_factory import build_hospital_step
                return build_hospital_step(step_name, info)
            except ImportError:
                pass  # 如果导入失败，继续使用通用步骤
        
        # 通用步骤描述
        step_descriptions = {
            # 医院相关步骤
            "locate_window": "正在为您查找窗口…",
            "check_queue": "正在为您判断排队情况…",
            "guide_to_window": "正在引导您前往窗口…",
            "wait_for_turn": "正在等待叫号…",
            "assist_communication": "正在协助您沟通…",
            "identify_floor": "正在识别楼层信息…",
            "find_elevator_or_stairs": "正在查找电梯或楼梯…",
            "navigate_to_area": "正在导航到目标区域…",
            "locate_room": "正在定位诊室…",
            "locate_payment_window": "正在查找缴费窗口…",
            "queue_and_wait": "正在排队等待…",
            "navigate_to_pharmacy": "正在导航到药房…",
            "find_waiting_seat": "正在查找候诊座位…",
            "monitor_call": "正在监听叫号…",
            
            # 商场相关步骤
            "find_floor": "正在查找楼层…",
            "navigate_to_location": "正在导航到目标位置…",
            "navigate_to_toilet": "正在导航到卫生间…",
            "navigate_to_exit": "正在导航到出口…",
            "navigate_to_elevator": "正在导航到电梯…",
            "select_floor": "正在选择楼层…",
            
            # 地铁相关步骤
            "identify_direction": "正在识别方向…",
            "follow_signs": "正在跟随指示牌…",
            "guide_to_gate": "正在引导您前往闸机…",
            "navigate_to_platform": "正在导航到站台…",
            "identify_transfer_line": "正在识别换乘线路…",
            "navigate_to_transfer": "正在导航到换乘通道…",
            
            # 政务大厅相关步骤
            "identify_service_type": "正在识别服务类型…",
            "locate_target_window": "正在定位目标窗口…",
            "navigate_to_inquiry": "正在导航到咨询台…",
        }
        
        description = step_descriptions.get(step_name, f"执行：{step_name}")
        
        # 这里可以添加具体的 action 逻辑
        # 当前为占位实现
        action = self._create_action(step_name, info)
        
        return Step(description, action=action, step_type="action")
    
    def _create_action(self, step_name: str, info: Dict[str, Any]):
        """
        创建步骤的具体执行逻辑（占位）
        
        实际实现中，这里应该返回可执行的函数或对象
        """
        # TODO: 根据 step_name 创建对应的 action
        return lambda: print(f"[Action] {step_name}")

