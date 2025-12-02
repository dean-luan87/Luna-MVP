# core/task_dispatcher.py
from __future__ import annotations

from typing import Dict, Any, Optional
from .task_intent import TaskIntent


class TaskDispatcher:
    """
    把 TaskIntent 转换成可执行的任务计划（task_plan）。

    task_plan 最终会交给前端的 taskChain.enqueue() 使用。

    这里不做复杂场景区分，只根据 intent_type 和 target_category 生成通用步骤。
    """

    @staticmethod
    def build_task_plan(intent: TaskIntent) -> Optional[Dict[str, Any]]:
        if intent is None:
            return None

        if intent.intent_type == "CROSS_STREET":
            return TaskDispatcher._build_cross_street_plan(intent)

        if intent.intent_type == "NAVIGATE":
            # 有明确 category 的先用 category
            if intent.target_category == "toilet":
                return TaskDispatcher._build_toilet_plan(intent)
            # 否则走通用"导航到XXX"
            return TaskDispatcher._build_generic_navigate_plan(intent)

        # 其它类型未来可以扩展
        return None

    @staticmethod
    def _base_plan(intent: TaskIntent) -> Dict[str, Any]:
        """
        基础任务结构，方便前端 taskChain 统一处理。
        """
        return {
            "taskId": intent.intent_id,
            "intent": intent.to_dict(),
            "priority": intent.priority,
            "status": "pending",
            "steps": [],  # 后面填充
        }

    @staticmethod
    def _build_toilet_plan(intent: TaskIntent) -> Dict[str, Any]:
        """
        导航到厕所 / 卫生间 的任务计划（通用模板）
        """
        plan = TaskDispatcher._base_plan(intent)
        plan["type"] = "NAVIGATE_TO_TOILET"

        plan["steps"] = [
            {
                "type": "SCAN_OCR_FOR_KEYWORDS",
                "keywords": ["厕所", "卫生间", "洗手间", "WC", "Toilet", "Restroom"],
                "timeoutSec": 30,
                "description": "在视野中查找厕所/卫生间相关指示牌文字",
            },
            {
                "type": "FOLLOW_DIRECTION_SIGN",
                "source": "OCR_OR_ARROW",
                "maxDistanceMeters": 50,
                "description": "根据指示牌箭头和走廊方向进行导航",
            },
            {
                "type": "AVOID_OBSTACLES_WHILE_MOVING",
                "description": "导航过程中持续避开障碍物/人群/车辆",
            },
            {
                "type": "CONFIRM_ARRIVAL_BY_OCR",
                "keywords": ["厕所", "卫生间", "洗手间", "WC"],
                "description": "接近目标区域后，通过 OCR 再次确认已经到达",
            },
            {
                "type": "ANNOUNCE_ARRIVAL",
                "message": "已经为你找到卫生间附近，如果需要我可以继续帮你引导。",
            },
        ]
        return plan

    @staticmethod
    def _build_cross_street_plan(intent: TaskIntent) -> Dict[str, Any]:
        """
        过马路任务计划（通用模板，不依赖城市交通规则细节）
        """
        plan = TaskDispatcher._base_plan(intent)
        plan["type"] = "CROSS_STREET"

        plan["steps"] = [
            {
                "type": "FIND_CROSSWALK_OR_SAFE_POINT",
                "description": "寻找斑马线或安全的过街位置（视觉检测 + 场景理解）",
            },
            {
                "type": "CHECK_TRAFFIC_LIGHT_OR_VEHICLES",
                "description": "观察车辆和路口状态，尽量在安全时机引导过街",
            },
            {
                "type": "GUIDE_USER_ACROSS",
                "description": "在过街过程中保持语音引导，提示方向、距离和潜在危险",
            },
            {
                "type": "CONFIRM_FINISH",
                "message": "已经安全穿过马路。",
            },
        ]
        return plan

    @staticmethod
    def _build_generic_navigate_plan(intent: TaskIntent) -> Dict[str, Any]:
        """
        通用导航任务：
        例如"带我去挂号窗口"、"带我去711"、"带我去地铁站"等。

        不预设行业规则，只做：
        - 用 OCR/标识 找目标名称
        - 朝目标方向导航
        """
        plan = TaskDispatcher._base_plan(intent)
        plan["type"] = "NAVIGATE_GENERIC"

        target = intent.target_name or "目标位置"

        plan["steps"] = [
            {
                "type": "SCAN_OCR_FOR_TARGET_NAME",
                "targetText": target,
                "fuzzy": True,
                "timeoutSec": 40,
                "description": f"在指示牌/招牌/门牌上查找与"{target}"相关的文本",
            },
            {
                "type": "MOVE_TOWARDS_TARGET",
                "description": "根据目标位置和箭头方向进行导航",
            },
            {
                "type": "AVOID_OBSTACLES_WHILE_MOVING",
                "description": "导航过程中持续避开障碍物/人群/车辆",
            },
            {
                "type": "CONFIRM_ARRIVAL_BY_DISTANCE_OR_OCR",
                "description": f"接近"{target}"附近后，通过距离/OCR 再次确认已到达",
            },
            {
                "type": "ANNOUNCE_ARRIVAL",
                "message": f"已经接近你说的"{target}"，如果需要我可以帮你继续识别周围环境。",
            },
        ]
        return plan

