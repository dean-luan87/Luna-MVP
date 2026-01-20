"""
NavPhraseMapper: 结构化事件 → speech_event(dict) 映射器

将 NavigationEngineV13 的结构化事件转换为标准化的 speech_event，
供 NavigationVoiceAdapter 处理。
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger("NavPhraseMapper")


class NavPhraseMapper:
    """
    NavigationEngineV13 的结构化事件 → speech_event(dict) 映射器。

    输入: { 'type': 'danger', 'code': 'obstacle_front', 'distance': 0.7 }
    输出: { 'text': '前方 0.7 米有障碍物，请注意', 'decision': 'STOP', ... }
    """

    def __init__(self):
        # 根据 code 映射决策方向
        self.code_to_decision = {
            "obstacle_front": "STOP",
            "obstacle_left": "HARD_LEFT",
            "obstacle_right": "HARD_RIGHT",
            "stairs_up": "CAUTION",
            "stairs_down": "CAUTION",
            "road_narrow": "SLOW",
            "water_puddle": "CAUTION",
            "crowded_ahead": "SLOW",
            "complex_environment": "CAUTION",
        }

        # 文案模板（可后续扩展）
        self.templates = {
            "obstacle_front": "前方 {distance} 米有障碍物，请注意",
            "obstacle_left": "左侧 {distance} 米有障碍物，请注意",
            "obstacle_right": "右侧 {distance} 米有障碍物，请注意",
            "stairs_up": "前方 {distance} 米有上台阶",
            "stairs_down": "前方 {distance} 米有下台阶",
            "road_narrow": "前方道路变窄，请小心通过",
            "water_puddle": "前方有积水，请注意脚下",
            "crowded_ahead": "前方人多，请减速并注意避让",
            "complex_environment": "前方环境较复杂，请您放慢脚步，注意安全",
        }

    def convert_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        输入结构化事件 → 输出 speech_event(dict) 列表

        Args:
            events: 结构化事件列表，每个事件包含：
                - type: str - 事件类型（'danger', 'navigation', 'system'）
                - code: str - 事件代码（'obstacle_front', 'stairs_down' 等）
                - distance: float - 距离（可选）
                - 其他自定义字段

        Returns:
            speech_event 字典列表，每个包含：
                - text: str - 播报文本
                - decision: str - 决策类型（'STOP', 'CAUTION' 等）
                - category: str - 类别（'safety', 'navigation'）
                - priority: int - 优先级（1-3）
                - interruptible: bool - 是否可打断
                - raw_event: dict - 原始事件（保留）
        """
        results = []

        for ev in events:
            if not isinstance(ev, dict):
                logger.warning(f"跳过非字典类型的事件: {type(ev)}")
                continue

            code = ev.get("code")
            if not code:
                logger.debug(f"事件缺少 code 字段，跳过: {ev}")
                continue

            if code not in self.templates:
                logger.debug(f"未知的事件代码: {code}，跳过")
                continue

            # 文本模板
            text = self.templates[code]
            distance = ev.get("distance", None)

            # 格式化文本（如果有距离参数）
            if "{distance}" in text:
                if distance is not None:
                    try:
                        d = float(distance)
                        text = text.format(distance=f"{d:.1f}")
                    except (ValueError, TypeError):
                        # 距离格式错误，使用默认值
                        text = text.replace("{distance} ", "").replace("{distance}", "")
                else:
                    # 没有距离信息，移除占位符
                    text = text.replace("{distance} ", "").replace("{distance}", "")

            # 推断决策
            decision = self.code_to_decision.get(code, "")

            # 推断类别
            event_type = ev.get("type", "navigation")
            if event_type == "danger":
                category = "safety"
                priority = 2  # 高优先级
                interruptible = True
            elif event_type == "system":
                category = "system"
                priority = 1
                interruptible = False
            else:  # navigation
                category = "navigation"
                priority = 1
                interruptible = False

            speech_event = {
                "text": text,
                "decision": decision,
                "category": category,
                "priority": priority,
                "interruptible": interruptible,
                "raw_event": ev,  # 保留原始事件，便于调试
            }

            results.append(speech_event)

        return results


# 便于全局复用的单例
nav_phrase_mapper = NavPhraseMapper()












